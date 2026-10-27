#!/usr/bin/env python3
"""Build an offline reader from exact vector crops of textbook summaries."""
import base64
import concurrent.futures
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from selectable_text import SelectableTextBuilder

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'tmp/source-check'
SOURCE = ROOT / 'Physics text (TOC).pdf'
NS = {'x': 'http://www.w3.org/1999/xhtml'}


def command(args):
    subprocess.run([str(x) for x in args], check=True, capture_output=True)


def prepare(chapter):
    number = int(chapter['title'].split()[0])
    bbox = WORK / f'chapter-{number:02}.xml'
    if not bbox.exists():
        command(['pdftotext', '-cropbox', '-f', chapter['start'], '-l', chapter['end'],
                 '-bbox-layout', SOURCE, bbox])
    pages = ET.parse(bbox).findall('.//x:page', NS)
    pieces = []
    for offset, page in enumerate(pages):
        pnum = chapter['start'] + offset
        lines = page.findall('.//x:line', NS)
        text = lambda line: ' '.join(w.text or '' for w in line.findall('x:word', NS))
        headings = [line for line in lines if text(line) == 'Review & Summary']
        stops = [line for line in lines if text(line).upper() == chapter['stop']
                 and float(line.attrib['yMin']) > 55]
        if offset == 0:
            assert len(headings) == 1, (number, 'summary heading', [text(x) for x in lines[:5]])
            top = float(headings[0].attrib['yMin']) - 8
        else:
            top = 55
        if pnum == chapter['end']:
            assert len(stops) == 1, (number, 'stop heading', [text(x) for x in lines[:5]])
            bottom = float(stops[0].attrib['yMin']) - 2
            prior = [w for w in page.findall('.//x:word', NS)
                     if top <= float(w.attrib['yMin'])
                     and float(w.attrib['yMax']) < bottom]
            if prior:
                bottom = min(bottom, max(float(w.attrib['yMax']) for w in prior) + 3)
        else:
            bottom = float(page.attrib['height']) - 25
        if bottom <= top + 8:
            continue
        # Include the decorative section marker and both columns; exclude running heads.
        left, right = 39, float(page.attrib['width']) - 48
        words = [w for w in page.findall('.//x:word', NS)
                 if top <= float(w.attrib['yMin']) < bottom
                 and float(w.attrib['yMax']) <= bottom + 1]
        if not words:
            continue
        # Stop pages can have a column-wide heading at the very top, with no review text.
        if pnum == chapter['end'] and offset and bottom < 76:
            continue
        svg_path = WORK / f'page-{pnum}.svg'
        if not svg_path.exists():
            command(['pdftocairo', '-f', pnum, '-l', pnum, '-svg', SOURCE, svg_path])
        svg = svg_path.read_text()
        width, height = right - left, bottom - top
        svg = re.sub(r'<svg\b[^>]*>',
                     f'<svg xmlns="http://www.w3.org/2000/svg" '
                     f'xmlns:xlink="http://www.w3.org/1999/xlink" '
                     f'width="{width:.3f}" height="{height:.3f}" '
                     f'viewBox="{left:.3f} {top:.3f} {width:.3f} {height:.3f}">',
                     svg, count=1)
        crop_path = WORK / f'crop-{number:02}-{offset+1}.svg'
        crop_path.write_text(svg)
        chosen_lines = [text(line) for line in lines
                        if float(line.attrib['yMin']) >= top
                        and float(line.attrib['yMax']) <= bottom + 1]
        pieces.append({'page': pnum, 'crop': [left, top, right, bottom],
                       'width': width, 'height': height,
                       'text': '\n'.join(chosen_lines), 'file': str(crop_path.relative_to(ROOT))})
    assert pieces, chapter
    return {**chapter, 'number': number, 'pieces': pieces}


def extract():
    chapters = json.loads((ROOT / 'content/review-chapters.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(prepare, chapters))
    (WORK / 'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    for chapter in result:
        print(chapter['title'], [(x['page'], round(x['crop'][1]), round(x['crop'][3]))
                                 for x in chapter['pieces']], flush=True)
    return result


def build(chapters):
    nav, articles, search_index = [], [], []
    rebuilt = SelectableTextBuilder(SOURCE)
    text_data = {}
    for c in chapters:
        n = c['number']
        title = c['title'].split(' ', 1)[1]
        nav.append(f'<a class="chapter-link" href="#chapter-{n}" data-chapter="{n}">'
                   f'<span class="chapter-number">{n:02}</span><span class="chapter-name">'
                   f'{html.escape(title)}</span><span class="chapter-tick" aria-hidden="true"></span></a>')
        images = []
        text_data[str(n)] = []
        for piece_index, piece in enumerate(c['pieces'], 1):
            text_data[str(n)].append(rebuilt.excerpt(n, piece, piece_index))
            encoded = base64.b64encode((ROOT / piece['file']).read_bytes()).decode()
            images.append(f'<div class="excerpt"><div class="page-scroll"><div class="page-inner">'
                          f'<div class="original-version"><img class="source-image" loading="lazy" decoding="async" '
                          f'width="{piece["width"]:.3f}" height="{piece["height"]:.3f}" '
                          f'data-src="data:image/svg+xml;base64,{encoded}" '
                          f'alt="Original Review &amp; Summary excerpt for {html.escape(c["title"], quote=True)}, '
                          f'PDF page {piece["page"]}."></div><div class="regenerated-version" data-piece="{piece_index-1}" style="aspect-ratio:{piece["width"]}/{piece["height"]}" hidden></div></div></div>'
                          f'<div class="page-label">PDF PAGE {piece["page"]}</div></div>')
        page_label = ', '.join(str(p['page']) for p in c['pieces'])
        articles.append(f'<article id="chapter-{n}" data-chapter="{n}" aria-labelledby="title-{n}">'
                        f'<div class="chapter-heading"><div><div class="eyebrow">Chapter {n:02}</div>'
                        f'<h2 id="title-{n}">{html.escape(title)}</h2>'
                        f'<p>Review &amp; Summary · PDF {"pages" if len(c["pieces"]) > 1 else "page"} {page_label}</p></div>'
                        f'<button class="review-button" aria-pressed="false" aria-label="Mark chapter {n} reviewed">Mark reviewed</button></div>'
                        + ''.join(images) + '</article>')
        search_index.append({'title': c['title'], 'search':
                             (c['title'] + ' ' + ' '.join(p['text'] for p in c['pieces'])).lower()})
    template = (ROOT / 'tools/review/review-template.html').read_text()
    result = template.replace('@@NAV@@', '\n'.join(nav)).replace('@@ARTICLES@@', '\n'.join(articles))
    result = result.replace('@@SEARCH@@', json.dumps(search_index, ensure_ascii=False).replace('<', '\\u003c'))
    result = result.replace('@@FONTS@@', rebuilt.font_css())
    result = result.replace('@@REGENERATED_DATA@@', json.dumps(text_data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
    result = result.replace('@@TEXT_SCRIPT@@', (ROOT/'tools/review/review-text.js').read_text())
    (ROOT/'content/review-text-audit.json').write_text(json.dumps({'chapters':len(chapters),'excerpts':len(rebuilt.audit),'glyphs':sum(p['glyphs'] for p in rebuilt.audit),'fontFaces':len(rebuilt.fonts),'pages':rebuilt.audit},indent=2)+'\n')
    out = ROOT / 'Physics_Review_and_Summary_Tutorial.html'
    out.write_text(result)
    print(f'Built {out.name}: {out.stat().st_size / 1024**2:.1f} MB; '
          f'{len(chapters)} chapters, {sum(len(c["pieces"]) for c in chapters)} excerpts.')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',action='store_true',help='Re-extract the original SVG crops from the PDF')
    args=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True)
    manifest=WORK/'manifest.json'
    build(extract() if args.extract or not manifest.exists() else json.loads(manifest.read_text()))
