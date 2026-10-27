#!/usr/bin/env python3
"""Build the university practice studio with exact textbook and solution crops.

Requires Python 3.11+, PyMuPDF 1.26.7 and Pillow. Rebuild:
  .venv-practice/bin/python tools/practice/build_practice.py
The original two TOC PDFs must remain in the repository root for rebuilding.
Only generated WebP excerpts, the inventory and HTML are needed for hosting.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
import html
import io
import json
import re
from pathlib import Path
import pymupdf as fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
WORK = ROOT / 'tmp/practice'
ASSETS = ROOT / 'assets/practice'
FLAGS = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES
SCRIPTS = ['physics-activity.js', 'physics-adaptive.js', 'physics-followup.js', 'physics-practice-core.js',
           'physics-photo-review.js', 'physics-drawing-pad.js', 'physics-students.js',
           'physics-live-share.js', 'physics-practice.js']


def lines(page):
    return [line for block in page.get_text('dict', flags=FLAGS)['blocks']
            for line in block.get('lines', [])]


def line_text(line):
    return ''.join(span['text'] for span in line['spans']).strip()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def scan_sources():
    textbook = fitz.open(ROOT / 'Physics text (TOC).pdf')
    answers = fitz.open(ROOT / 'Physics answer (TOC).pdf')
    toc = textbook.get_toc()
    chapters = []
    current = None
    for level, title, page in toc:
        if level == 1:
            if current:
                current['end'] = page - 1
                current = None
            match = re.match(r'^(\d+) (.+)', title)
            if match:
                current = {'number': int(match[1]), 'title': match[2], 'start': page, 'sections': {}}
                chapters.append(current)
        elif current and level == 2:
            if title.upper() == 'PROBLEMS':
                current['problems'] = page
            match = re.match(r'(\d+-\d+) (.+)', title)
            if match:
                current['sections'][match[1]] = match[2].title()
    answer_chapters = [{'number': int(re.match(r'^\d+', title)[0]), 'start': page}
                       for level, title, page in answers.get_toc()
                       if level == 1 and re.match(r'^\d+- ', title)]
    for i, chapter in enumerate(answer_chapters):
        chapter['end'] = answer_chapters[i+1]['start']-1 if i+1 < len(answer_chapters) else len(answers)
    for chapter, answer_chapter in zip(chapters, answer_chapters, strict=True):
        number = chapter['number']
        events, references = [], defaultdict(set)
        for pn in range(chapter['start'], chapter['end']+1):
            page_lines = lines(textbook[pn-1])
            for line in page_lines:
                text = line_text(line)
                for match in re.finditer(r'\b(Figure|Table)\s+(\d+)[–−-](\d+)', text):
                    references[f'{match[1].lower()}:{match[2]}-{match[3]}'].add(pn)
            if pn < chapter['problems']:
                continue
            spans = [s for line in page_lines for s in line['spans']]
            if pn == chapter['problems']:
                top = min(s['bbox'][1] for s in spans if s['text'].startswith(f'Module {number}-')) - 4
                chapter['problemTop'] = top
            else:
                top = 58
            for span in spans:
                x, y, _, _ = span['bbox']
                if y < top or span['font'] != 'AkzidenzGroteskBE-Bold' or not 8.5 < span['size'] < 9.5:
                    continue
                text = span['text'].strip()
                match = re.fullmatch(r'([•●]*)\s*(\d{1,3})(?:\s+through\s+(\d{1,3}))?', text)
                event = {'page': pn, 'col': int(x > 330), 'y': round(y, 3)}
                if match:
                    event.update(n=int(match[2]), last=int(match[3] or match[2]), dots=len(match[1]))
                    events.append(event)
                elif re.match(r'^Module \d+-\d+', text):
                    event['module'] = re.match(r'^Module (\d+-\d+)', text)[1]
                    events.append(event)
                elif text == 'Additional Problems':
                    event['module'] = 'additional'
                    events.append(event)
        events.sort(key=lambda e: (e['page'], e['col'], e['y']))
        module = f'{number}-1'
        starts = []
        for event in events:
            if 'module' in event:
                module = event['module']
            else:
                event['module'] = module
                starts.append(event)
        numbers = [n for start in starts for n in range(start['n'], start['last']+1)]
        assert numbers == list(range(1, numbers[-1]+1)), (number, 'Incomplete textbook sequence', numbers)
        chapter.update(starts=starts, events=events, references={k: sorted(v) for k, v in references.items()})
        candidates = []
        for pn in range(answer_chapter['start'], answer_chapter['end']+1):
            page = answers[pn-1]
            for line in lines(page):
                x, y, _, _ = line['bbox']
                match = re.match(r'^(\d{1,3})\.\s', line_text(line))
                if match and 60 < x < 110 and 45 < y < page.rect.height-45:
                    candidates.append({'n': int(match[1]), 'page': pn, 'y': round(y, 3)})
        candidates.sort(key=lambda s: (s['page'], s['y']))
        solutions = []
        for candidate in candidates:
            if not solutions or candidate['n'] > solutions[-1]['n']:
                solutions.append(candidate)
        assert [s['n'] for s in solutions] == numbers, (number, 'Solution sequence mismatch')
        chapter['answer'] = {**answer_chapter, 'starts': solutions}
        print(f'Scanned chapter {number}: {len(numbers)} problems and solutions', flush=True)
    write_json(WORK/'source-map.json', chapters)
    return chapters


@lru_cache(maxsize=24)
def page_lines(file, pn):
    # Each document has a short-lived cache; images are excluded from text extraction.
    doc = documents[file]
    return lines(doc[pn-1])


def body_rect(file, pn):
    page = documents[file][pn-1]
    if file == 'text':
        return fitz.Rect(55, 58, 607, page.rect.height-42)
    # The solutions use both Letter and A4 pages. Remove running headers/page numbers,
    # then derive bounds from real content to preserve tall equations at page boundaries.
    boxes = []
    for line in page_lines(file, pn):
        text = line_text(line)
        box = fitz.Rect(line['bbox'])
        if not text or re.fullmatch(r'\d+|CHAPTER\s+\d+', text, re.I) or text.startswith('Chapter '):
            continue
        if box.y0 > 48 and box.y1 < page.rect.height-34:
            boxes.append(box)
    if not boxes:
        return None
    top = min(r.y0 for r in boxes)-5
    bottom = max(r.y1 for r in boxes)+5
    return fitz.Rect(65, max(45, top), min(550, page.rect.width-45), min(page.rect.height-35, bottom))


def source_text(file, pn, box):
    # Text is used only as supplementary context for assistive technology and AI.
    # Exact equations and diagrams are always retained in the images.
    return documents[file][pn-1].get_text('text', clip=box, sort=True).strip()


def problem_parts(chapter, start, end):
    result = []
    for pn in range(start['page'], end['page']+1):
        first_col = start['col'] if pn == start['page'] else 0
        last_col = end['col'] if pn == end['page'] else 1
        for col in range(first_col, last_col+1):
            body = body_rect('text', pn)
            top = chapter['problemTop'] if pn == chapter['problems'] else body.y0
            if (pn, col) == (start['page'], start['col']):
                top = start['y']-6
            bottom = body.y1
            if (pn, col) == (end['page'], end['col']):
                bottom = end['y']-5
            if bottom > top+5:
                box = fitz.Rect(55 if col == 0 else 331, top, 328 if col == 0 else 607, bottom)
                result.append((pn, box))
    return result


def solution_parts(chapter, start, end):
    result = []
    for pn in range(start['page'], end['page']+1):
        box = body_rect('answer', pn)
        if box is None:
            continue
        if pn == start['page']:
            box.y0 = start['y']-4
        if pn == end['page']:
            box.y1 = min(box.y1, end['y']-5)
        if box.height > 5:
            result.append((pn, box))
    return result


def excerpt_html(parts, file, stem, jobs, label, anchor=None):
    fragments, texts = [], []
    for i, (pn, box) in enumerate(parts, 1):
        relative = f'assets/practice/{stem}-{i}.webp'
        jobs[(file, pn)].append({'path': relative, 'box': list(box), 'scale': 2.5 if file == 'text' else 1.8, **({'anchor': anchor-box.y0} if file == 'text' and i == 1 and anchor is not None else {})})
        fragments.append(f'<img class="textbook-excerpt" src="{relative}" alt="{html.escape(label)}, PDF page {pn}, excerpt {i}" style="width:{round(box.width*2)}px;max-width:100%;height:auto" decoding="async">')
        texts.append(source_text(file, pn, box))
    # The readable transcript is supplementary, never a substitute for the original crop.
    transcript = '\n'.join(texts)
    fragments.append('<span class="sr-only">'+html.escape(transcript)+'</span>')
    return ''.join(fragments), transcript


def trim_question_top(image, anchor_pixels):
    # The textbook's font boxes extend into the preceding line. Trim only through
    # a completely blank row before the selected question, preserving superscripts.
    gray = image.convert('L')
    white = [y for y in range(min(gray.height, int(anchor_pixels)+1))
             if gray.crop((0, y, gray.width, y+1)).getextrema()[0] > 245]
    return image.crop((0, white[-1]+1, image.width, image.height)) if white else image


def render_page(task):
    file, pn, specs = task
    source = ROOT / ('Physics text (TOC).pdf' if file == 'text' else 'Physics answer (TOC).pdf')
    doc = fitz.open(source)
    page = doc[pn-1]
    scale = max(s['scale'] for s in specs)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    count = 0
    for spec in specs:
        target = ROOT/spec['path']
        if target.exists():
            continue
        r = spec['box']
        crop = image.crop((max(0, int(r[0]*scale)), max(0, int(r[1]*scale)),
                           min(image.width, round(r[2]*scale)), min(image.height, round(r[3]*scale))))
        if spec['scale'] < scale:
            crop = crop.resize((round(crop.width*spec['scale']/scale), round(crop.height*spec['scale']/scale)), Image.Resampling.LANCZOS)
        if 'anchor' in spec:
            crop = trim_question_top(crop, spec['anchor']*spec['scale'])
        crop.save(target, 'WEBP', quality=88, method=4)
        count += 1
    doc.close()
    return count


def build_inventory(chapters):
    jobs = defaultdict(list)
    bank = []
    for chapter in chapters:
        number = chapter['number']
        starts = chapter['starts']
        solutions = chapter['answer']['starts']
        for i, start in enumerate(starts):
            next_question = starts[i+1] if i+1 < len(starts) else {'page': chapter['end'], 'col': 1, 'y': documents['text'][chapter['end']-1].rect.height-37}
            # A section heading marks the end of the previous question.
            before_next = [e for e in chapter['events'] if 'module' in e and
                           (start['page'], start['col'], start['y']) < (e['page'], e['col'], e['y']) <=
                           (next_question['page'], next_question['col'], next_question['y'])]
            stop = before_next[0] if before_next else next_question
            parts = problem_parts(chapter, start, stop)
            stem = f'q-{number:02}-{start["n"]:03}'
            qhtml, qtext = excerpt_html(parts, 'text', stem, jobs, f'Chapter {number}, problem {start["n"]}'+(f'–{start["last"]}' if start['last'] != start['n'] else ''), anchor=start['y'])
            context_pages = {pn for pn, _ in parts}
            # Figures and tables may sit outside a question's column or on another page.
            for match in re.finditer(r'\b(Fig(?:ure)?\.?|Table)\s*(\d+)[–−-](\d+)', qtext):
                key = f'{"table" if match[1]=="Table" else "figure"}:{match[2]}-{match[3]}'
                context_pages.update(chapter['references'].get(key, []))
            context = []
            for pn in sorted(context_pages):
                relative = f'assets/practice/page-{pn:04}.webp'
                if not any(job['path'] == relative for job in jobs[('text', pn)]):
                    jobs[('text', pn)].append({'path': relative, 'box': list(body_rect('text', pn)), 'scale': 2})
                context.append(f'<figure><img data-context="true" src="{relative}" loading="lazy" alt="Original textbook PDF page {pn}: diagrams, tables and surrounding context" style="width:1104px;max-width:100%;height:auto"><figcaption class="small">Textbook PDF page {pn}</figcaption></figure>')
            qhtml += '<details class="source-context"><summary>Original pages, diagrams &amp; tables</summary>'+''.join(context)+'</details>'
            module = start['module']
            topic_title = chapter['sections'].get(module, 'Additional Problems' if module == 'additional' else f'Module {module}')
            for n in range(start['n'], start['last']+1):
                solution_start = solutions[n-1]
                solution_end = solutions[n] if n < len(solutions) else {'page': chapter['answer']['end'], 'y': documents['answer'][chapter['answer']['end']-1].rect.height-34}
                answer_parts = solution_parts(chapter, solution_start, solution_end)
                solution, _ = excerpt_html(answer_parts, 'answer', f'a-{number:02}-{n:03}', jobs, f'Worked solution, chapter {number}, problem {n}')
                solution = f'<p class="small">Physics answer (TOC).pdf · Chapter {number}, problem {n} · PDF page {solution_start["page"]}</p>'+solution
                shared = f'<p class="shared-problem-note">This exercise shares its prompt and data table with problems {start["n"]}–{start["last"]}. Answer <strong>problem {n}</strong>, using its numbered table row.</p>' if start['n'] != start['last'] else ''
                bank.append({'id': f'uni-ch{number}-p{n}', 'sourceId': f'problem-{n}', 'kind': 'textbook',
                             'chapter': f'uni-ch{number}', 'chapterNumber': number, 'chapterTitle': chapter['title'],
                             'number': n, 'topic': f'Ch {number} · {module}', 'topicTitle': topic_title,
                             'level': start['dots'] or 2, 'questionType': 'Additional problem' if module == 'additional' else 'Textbook problem',
                             'title': f'Problem {n} · {topic_title}', 'html': shared+qhtml, 'solution': solution,
                             'answer': 'See original worked solution', 'url': f'physics-problems.html#uni-ch{number}-p{n}',
                             'sourcePages': sorted(context_pages), 'solutionPages': [pn for pn, _ in answer_parts]})
    write_json(ROOT/'content/physics-practice-bank.json', bank)
    write_json(ROOT/'content/physics-practice-chapters.json', [{
        'number': c['number'], 'title': c['title'], 'problemCount': c['starts'][-1]['last'],
        'textbookPages': [c['problems'], c['end']], 'answerPages': [c['answer']['start'], c['answer']['end']],
        'sections': c['sections']} for c in chapters])
    write_json(WORK/'render-jobs.json', [{'file': file, 'page': pn, 'specs': specs} for (file, pn), specs in jobs.items()])
    return bank, jobs


def embedded_script(name):
    source = (HERE/name).read_text()
    if name == 'physics-practice.js':
        assert source.count('// FOLLOWUP_CONTROLS') == 1
        source = source.replace('// FOLLOWUP_CONTROLS', (HERE/'physics-followup-ui.js').read_text())
    return '<script>\n'+source+'\n</script>\n'


def build_html(bank):
    data = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    scripts = '<script id="question-bank" type="application/json">'+data+'</script>\n'+''.join(embedded_script(name) for name in SCRIPTS)
    template = (HERE/'physics-practice-template.html').read_text()
    template = template.replace('</style>', '\n.textbook-excerpt{display:block;margin:8px 0}.source-context{margin:14px 0}.source-context figure{margin:14px 0}.shared-problem-note{background:#eef0e7;border-radius:8px;padding:12px;font-size:13px}\n</style>', 1)
    (ROOT/'physics-practice.html').write_text(template.replace('<!-- PRACTICE_SCRIPTS -->', scripts))
    head = re.search(r'<head>(.*?)</head>', template, re.S)[1].replace('Practice Studio', 'Student Activity')
    dialog = re.search(r'<dialog[^>]*>(.*?)</dialog>', template, re.S)[1]
    dialog = re.sub(r'<button id="activity-close".*?</button>', '', dialog)
    dialog = re.sub(r'<p><a id="activity-page-link".*?</p>', '', dialog)
    monitor = '<!doctype html><html lang="en"><head>'+head+'</head><body><header><a class="brand" href="physics-practice.html">University Physics <span>/ Practice Studio</span></a><a href="content.html">Browse chapters ↗</a></header><main style="max-width:850px">'+dialog
    monitor += '<section class="panel storage"><h3>Optional sync</h3><label for="monitor-key" class="small">Firebase API key</label><input id="monitor-key" type="password" autocomplete="off" placeholder="Use the same key as the student"><button id="monitor-connect" class="secondary" type="button">Connect to synced history</button><p class="small">Without sync, this page reads saved history on this device.</p></section></main>'
    (ROOT/'physics-monitor.html').write_text(monitor+embedded_script('physics-activity.js')+embedded_script('physics-monitor.js')+'</body></html>')
    viewer = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>University Physics · Original Problems</title><style>body{margin:0;background:#f5f5ee;color:#183832;font:16px/1.6 system-ui}main{max-width:1100px;margin:auto;padding:24px}a,summary{color:#216650}article{background:#fff;border:1px solid #dde3d9;border-radius:12px;padding:24px;margin-top:20px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}img{max-width:100%;height:auto}figure{margin:12px 0}.small{font-size:12px;color:#60736b}</style></head><body><main><a href="physics-practice.html">← Practice Studio</a><h1 id="heading">Original textbook problem</h1><p id="meta"></p><article id="problem"></article><details id="answer"><summary>Original worked solution</summary><div id="worked"></div></details></main><script id="question-bank" type="application/json">'+data+'</script><script>function show(){const bank=JSON.parse(document.getElementById("question-bank").textContent),p=bank.find(q=>q.id===location.hash.slice(1))||bank[0];document.getElementById("heading").textContent="Chapter "+p.chapterNumber+" · Problem "+p.number;document.getElementById("meta").textContent=p.chapterTitle+" · "+p.topicTitle;document.getElementById("problem").innerHTML=p.html;document.getElementById("worked").innerHTML=p.solution;document.getElementById("answer").open=false;document.title="Chapter "+p.chapterNumber+" · Problem "+p.number;document.querySelector("a").href="physics-practice.html?q="+encodeURIComponent(p.id)}show();addEventListener("hashchange",show);</script></body></html>'
    (ROOT/'physics-problems.html').write_text(viewer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rescan', action='store_true')
    parser.add_argument('--html-only', action='store_true')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    if args.html_only:
        bank = json.loads((ROOT/'content/physics-practice-bank.json').read_text())
    else:
        chapters = scan_sources() if args.rescan or not (WORK/'source-map.json').exists() else json.loads((WORK/'source-map.json').read_text())
        global documents
        documents = {'text': fitz.open(ROOT/'Physics text (TOC).pdf'), 'answer': fitz.open(ROOT/'Physics answer (TOC).pdf')}
        bank, jobs = build_inventory(chapters)
        tasks = [(file, pn, specs) for (file, pn), specs in jobs.items() if any(not (ROOT/s['path']).exists() for s in specs)]
        print(f'Rendering {len(tasks)} source pages for {len(bank)} problems', flush=True)
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            count = 0
            for i, rendered in enumerate(pool.map(render_page, tasks), 1):
                count += rendered
                if i % 100 == 0 or i == len(tasks):
                    print(f'Rendered {i}/{len(tasks)} source pages; {count} excerpts', flush=True)
    build_html(bank)
    print(f'Built practice studio: {len(bank)} problems, {len(set(p["chapter"] for p in bank))} chapters', flush=True)


if __name__ == '__main__':
    main()
