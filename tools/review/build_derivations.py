#!/usr/bin/env python3
"""Build original formula notes and attach them to the existing offline reader.

This command needs only Python's standard library, not the source PDFs. The main
review builder calls the same helpers so rebuilding excerpts preserves links.
"""
from collections import defaultdict
from html import escape, unescape
import json
from pathlib import Path
import re

from derivation_content import TOPICS
from derivation_diagrams import DIAGRAMS, build_diagrams, diagrams_for, figure_html
from derivation_reading import READINGS
from equation_provenance import NOTE_INPUTS, LABELS
from source_equations import annotate as annotate_source, strip_generated_links, AUDIT as SOURCE_AUDIT

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / 'Physics_Review_and_Summary_Tutorial.html'
OUT = ROOT / 'derivations'
SVG = 'http://www.w3.org/2000/svg'
BY_CHAPTER = defaultdict(list)
BY_SLUG = {t['slug']: t for t in TOPICS}
for topic in TOPICS:
    BY_CHAPTER[topic['chapter']].append(topic)


def anchor(topic):
    return f'chapter-{topic["chapter"]}--{topic["slug"]}'


def chapter_resources(chapter):
    topics = BY_CHAPTER[chapter]
    rows = ''.join(
        f'<li id="{anchor(t)}"><a class="formula-link" href="derivations/{t["slug"]}.html">'
        f'<span><strong>{escape(t["title"])}</strong>'
        f'<span class="formula-preview">{escape(t["formula"])}</span></span>'
        '<span class="formula-arrow" aria-hidden="true">↗</span></a></li>'
        for t in topics)
    return (f'<section class="derivation-resources" aria-labelledby="derive-title-{chapter}">'
            f'<h3 id="derive-title-{chapter}">Explain &amp; derive</h3>'
            '<p>Follow a formula into its assumptions, proof and worked example. '
            'Deeper questions branch at the step that uses them.</p>'
            '<p class="equation-legend"><span>Underlined equations: open their argument</span> · '
            '<span>Grey marks: definitions, laws or model inputs (hover for the label)</span></p>'
            f'<ul>{rows}</ul></section>')


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip().casefold().replace('’', "'")


def link_excerpt(svg, chapter):
    """Link matching source headings and mirror their glyph bounds on images.

    Existing textbook glyphs, fonts and graphics remain byte-for-byte unchanged.
    Bounds come from the embedded selectable text, so no PDF is needed here.
    """
    svg = strip_generated_links(svg)
    headings = {normalized(h): t for t in BY_CHAPTER[chapter] for h in t['headings']}
    vb = re.search(r'viewBox="([^"]+)"', svg)
    x0, y0, width, height = map(float, vb[1].split())
    overlays = []

    def replace(match):
        raw = match[0]
        # itertext-like extraction without altering the original glyph markup.
        text = unescape(re.sub(r'<[^>]+>', '', raw))
        t = headings.get(normalized(text))
        # Keep the existing interactive circular-motion proof intact.
        if not t or (chapter == 4 and normalized(text) == 'uniform circular motion'):
            return raw
        positions = [list(map(float, p.split())) for p in re.findall(r'data-p="([^"]+)"', raw)]
        if not positions:
            return raw
        left = max(x0, min(p[0] for p in positions))
        right = min(x0 + width, max(p[3] for p in positions))
        top = max(y0, min(p[1] - p[2] * .92 for p in positions))
        bottom = min(y0 + height, max(p[1] + p[2] * .2 for p in positions))
        if right <= left or bottom <= top:
            return raw
        href = f'derivations/{t["slug"]}.html'
        label = escape('Explain & derive: ' + t['title'], quote=True)
        style = (f'left:{100*(left-x0)/width:.4f}%;top:{100*(top-y0)/height:.4f}%;'
                 f'width:{100*(right-left)/width:.4f}%;height:{100*(bottom-top)/height:.4f}%')
        overlays.append(f'<a class="source-topic-link" href="{href}" aria-label="{label}" '
                        f'title="{label}" style="{style}"></a>')
        return (f'<a class="section-proof-link" data-derivation-link="true" href="{href}" '
                f'aria-label="{label}"><title>{label}</title>{raw}</a>')

    svg = re.sub(r'<text\b[^>]*>.*?</text>', replace, svg, flags=re.S)
    svg, equation_overlays = annotate_source(svg, chapter)
    return svg, ''.join(overlays) + equation_overlays


def equation(text, topic, location, main=False):
    if not text:
        return ''
    kind = NOTE_INPUTS.get(topic['slug'], {}).get(location, 'derived')
    label = ('Follow the reasoning ↓' if main else 'Read the reasoning above ↑') if kind == 'derived' else 'About this starting point'
    return (f'<div class="equation{" main-equation" if main else ""}" id="equation-{location}" data-kind="{kind}">'
            f'<span class="equation-status">{LABELS[kind]}</span>'
            f'<a class="equation-value" data-proof-link href="#proof-{location}">{escape(text)}</a>'
            f'<a class="equation-action" data-proof-link href="#proof-{location}">{label} ↓</a></div>')


def proof_sections(t):
    """One readable argument, with stable anchors at the relevant paragraphs.

    The equations and their explanations live together. A proof link returns to
    the reasoning that produces the equation instead of opening a duplicate.
    """
    reading = READINGS.get(t['slug'], {})
    main_kind = NOTE_INPUTS.get(t['slug'], {}).get('main', 'derived')
    heading = reading.get('title', 'Understanding the relation' if main_kind != 'derived' else 'Developing the argument')
    out = [f'<section class="proof-library derivation-reading equation-proof" id="proof-main" '
           f'data-kind="{main_kind}" tabindex="-1" aria-labelledby="argument-title">'
           f'<h2 id="argument-title">{escape(heading)}</h2><div class="reading-body">']
    def paragraphs(text):
        return ''.join(f'<p>{escape(p)}</p>' for p in text.split('\n\n') if p)
    if reading.get('opening'):
        out.append(paragraphs(reading['opening']))
    if main_kind != 'derived':
        explanations = {
            'definition': 'Here the starting relation defines the quantity being discussed. We can understand that definition and derive its consequences, while keeping the definition itself distinct from those consequences.',
            'law': 'The starting relation is a physical law used in this description. The argument below explains what it means and how its consequences follow under the stated assumptions.',
            'model': 'The starting relation describes the behavior assumed for this model or material. Within its range of validity, we can use it to work out the consequences below.',
            'reference': 'The starting relation fixes the reference values or conditions for this discussion. With that choice made, the following reasoning explains the resulting relationships.',
            'notation': 'The starting relation specifies the mathematical notation used here. The following argument explains how that notation connects to the physical quantities.',
        }
        out.append(f'<p class="starting-point">{escape(explanations[main_kind])}</p>')
    out.extend(figure_html(d) for d in diagrams_for(t['slug']))
    for i, step in enumerate(t['steps'], 1):
        edited = reading.get('steps', {}).get(i, {})
        title = edited.get('title', step['title'])
        location = f'step-{i}'
        kind = NOTE_INPUTS.get(t['slug'], {}).get(location, 'derived')
        out.append(f'<section class="step" id="{location}"><div class="equation-proof" '
                   f'id="proof-{location}" data-kind="{kind}" tabindex="-1" aria-labelledby="step-title-{i}">'
                   f'<h3 id="step-title-{i}">{escape(title)}</h3><div class="proof-body">')
        out.append(paragraphs(edited.get('text', step['text'])))
        out.append(equation(step['equation'], t, location))
        if not step['equation'] and any(c in edited.get('text', step['text']) for c in '=≈≥≤'):
            out.append(f'<a class="prose-equation-link" data-proof-link href="#proof-{location}">Read the argument for these relations ↑</a>')
        if edited.get('after'):
            out.append(paragraphs(edited['after']))
        out.extend(figure_html(d) for d in diagrams_for(t['slug'], i))
        if step['branch']:
            out.append(branch(*step['branch'], t['slug'], i))
        out.append('</div></div></section>')
    if reading.get('closing'):
        out.append(f'<p class="argument-closing">{escape(reading["closing"])}</p>')
    return ''.join(out)+'</div></section>'


def branch(question, target, source, step):
    return (f'<a class="branch" href="{target}.html?from={source}&amp;step=step-{step}">'
            '<span class="branch-label">A closer look</span>'
            f'<strong>{escape(question)} ↗</strong><span class="branch-target">'
            f'{escape(BY_SLUG[target]["title"])} <span aria-hidden="true">↗</span></span></a>')


def shell(title, body, chapters, sidebar='', index=False):
    nav = '<a href="../Physics_Review_and_Summary_Tutorial.html">Review &amp; Summary</a>'
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)} · Physics Inquiry</title>'
            '<meta name="description" content="Step-by-step physics explanations with assumptions, '
            'worked examples and follow-up branches at the exact step that needs them.">'
            '<link rel="stylesheet" href="assets/inquiry.css">'
            '<link rel="stylesheet" href="assets/reading.css"></head><body>'
            '<a class="skip" href="#main">Skip to explanation</a>'
            '<header><a class="brand" href="index.html"><span aria-hidden="true">φ</span>'
            '<span>Physics <small>Follow the question</small></span></a>'
            f'<nav aria-label="Study navigation">{nav}<a href="index.html">All explanations</a></nav></header>'
            f'<div class="layout"><main id="main">{body}</main>{sidebar}</div>'
            '<footer>Original teaching notes · Formulas are selectable text · Works offline</footer>'
            f'<script id="inquiry-topics" type="application/json">{json.dumps([t["slug"] for t in TOPICS])}</script>'
            '<script src="assets/inquiry.js"></script></body></html>')


def render_topic(t, chapters):
    ch = t['chapter']
    summary = f'../Physics_Review_and_Summary_Tutorial.html#{anchor(t)}'
    body = (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{summary}">Chapter {ch:02}</a>'
            f'<span aria-hidden="true">›</span><span>{escape(t["title"])}</span></nav>'
            f'<a class="context-return" data-context-return href="{summary}">← Return to this formula in the summary</a>'
            f'<div class="hero"><div class="eyebrow">Chapter {ch:02} · {escape(chapters[ch])}</div>'
            f'<h1>{escape(t["title"])}</h1><p class="lead">{escape(t["meaning"])}</p></div>'
            + equation(t['formula'], t, 'main', True)
            + '<section class="setup" aria-labelledby="symbols"><h2 id="symbols">What the symbols mean</h2>'
            f'<p>{escape(t["symbols"])}</p><h2>When this applies</h2><p>{escape(t["assumptions"])}</p></section>')
    toc = [f'<li><a href="#step-{i}">{escape(READINGS.get(t["slug"],{}).get("steps",{}).get(i,{}).get("title",s["title"]))}</a></li>'
           for i,s in enumerate(t['steps'],1)]
    body += proof_sections(t)
    if t['slug'] == 'centripetal-acceleration':
        body += ('<a class="branch" href="../centripetal-acceleration-proof.html">'
                 '<span class="branch-label">Explore visually</span><strong>Open the interactive circular-motion proof ↗</strong></a>')
    body += ('<section class="example" id="example"><div class="eyebrow">Check the result</div>'
             f'<h2>A worked example</h2><p>{escape(t["example"])}</p>'
             '<a class="prose-equation-link" data-proof-link href="#proof-main">Derivation behind this calculation ↗</a></section>'
             f'<section class="caution"><h2>A point to keep straight</h2><p>{escape(t["caution"])}</p>'
             '<a class="prose-equation-link" data-proof-link href="#proof-main">Check the assumptions and derivation ↗</a></section>'
             f'<a class="return" data-context-return href="{summary}">← Return to this formula in the summary</a>'
             f'<p class="summary-return"><a href="{summary}">Back to Chapter {ch:02} summary</a></p>')
    siblings = ''.join(f'<li><a href="{s["slug"]}.html">{escape(s["title"])}</a></li>'
                       for s in BY_CHAPTER[ch] if s != t)
    sidebar = ('<aside><div class="side-card"><div class="eyebrow">On this page</div>'
               f'<ol>{"".join(toc)}</ol><a href="#example">Worked example ↓</a></div>'
               f'<div class="side-card"><div class="eyebrow">Also in Chapter {ch:02}</div><ul>{siblings}</ul></div>'
               '<div class="side-card"><div class="eyebrow">Follow a question</div>'
               '<p>Branches open beside the step that uses them. The return link brings you back to that step.</p></div></aside>')
    return shell(t['title'], body, chapters, sidebar)


def validate_content():
    assert len(BY_SLUG) == len(TOPICS), 'Duplicate topic slug'
    assert set(BY_CHAPTER) == set(range(1, 45)), 'Every chapter needs explanations'
    for t in TOPICS:
        assert re.fullmatch(r'[a-z0-9-]+', t['slug'])
        assert len(t['steps']) >= 4, t['slug']
        assert all(t[k] for k in ['formula', 'meaning', 'symbols', 'assumptions', 'example', 'caution'])
        for s in t['steps']:
            if s['branch']:
                assert s['branch'][1] in BY_SLUG, (t['slug'], s['branch'])


def build_pages():
    validate_content()
    build_diagrams(ROOT, TOPICS)
    chapters = {int(c['title'].split()[0]): c['title'].split(' ', 1)[1]
                for c in json.loads((ROOT/'content/review-chapters.json').read_text())}
    (OUT/'assets').mkdir(parents=True, exist_ok=True)
    for name in ['inquiry.css', 'reading.css', 'inquiry.js']:
        (OUT/'assets'/name).write_text((ROOT/'tools/review'/name).read_text())
    for t in TOPICS:
        (OUT/f'{t["slug"]}.html').write_text(render_topic(t, chapters))
    sections = []
    for ch, title in chapters.items():
        items = ''.join(f'<li data-search="{escape((t["title"]+" "+t["formula"]+" "+t["meaning"]).casefold(), quote=True)}">'
                        f'<a href="{t["slug"]}.html"><strong>{escape(t["title"])}</strong>'
                        f'<span>{escape(t["formula"])}</span></a></li>' for t in BY_CHAPTER[ch])
        sections.append(f'<section class="directory-chapter"><h2><span>{ch:02}</span> {escape(title)}</h2><ul>{items}</ul></section>')
    body = (f'<div class="hero"><div class="eyebrow">44 chapters · {len(TOPICS)} explanations</div>'
            '<h1>Follow the formula.<br>Understand every step.</h1>'
            '<p class="lead">Start from a chapter summary, open a formula, and follow the question behind any step. '
            'Read the reasoning as a connected explanation, with diagrams beside the ideas they illustrate '
            'and deeper questions beside the paragraphs that raise them.</p></div>'
            '<label class="search-label" for="topic-search">Find a formula or question</label>'
            '<input id="topic-search" type="search" placeholder="Try entropy, force, photon…" autocomplete="off">'
            f'<p id="search-status" role="status" aria-live="polite">{len(TOPICS)} explanations</p>'
            + ''.join(sections) + '<p id="no-results" hidden>No matching explanations. Try a different word.</p>')
    (OUT/'index.html').write_text(shell('Formula explanations & derivations', body, chapters, index=True))
    manifest = [dict(chapter=t['chapter'], slug=t['slug'], title=t['title'],
                     file=f'derivations/{t["slug"]}.html', summaryAnchor=anchor(t),
                     diagrams=[dict(file=f'derivations/assets/diagrams/{d.filename}',step=d.step,key=d.key,title=d.title)
                               for d in DIAGRAMS if d.topic==t['slug']],
                     branches=[dict(step=i, target=s['branch'][1])
                               for i, s in enumerate(t['steps'], 1) if s['branch']],
                     equations=[dict(location=loc,kind=NOTE_INPUTS.get(t['slug'],{}).get(loc,'derived'),proof=f'proof-{loc}')
                                for loc in ['main']+[f'step-{i}' for i,s in enumerate(t['steps'],1) if s['equation']]]) for t in TOPICS]
    (ROOT/'content/derivations.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')


def update_reader():
    SOURCE_AUDIT.clear()
    text = REVIEW.read_text()
    # Only regenerate our own insertions; preserve the existing reader and images.
    text = re.sub(r'<!-- derivations:chapter-\d+:start -->.*?<!-- derivations:chapter-\d+:end -->', '', text, flags=re.S)
    text = re.sub(r'<a class="source-(?:topic|equation)-link"[^>]*></a>', '', text)
    match = re.search(r'(<script id="regenerated-data" type="application/json">)(.*?)(</script>)', text, re.S)
    data = json.loads(match[2])
    overlays = {}
    for chapter, pieces in data.items():
        linked = [link_excerpt(p, int(chapter)) for p in pieces]
        data[chapter] = [x[0] for x in linked]
        overlays[int(chapter)] = [x[1] for x in linked]
    text = text[:match.start(2)] + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + text[match.end(2):]
    def article_replace(m):
        article = m[0]
        chapter = int(re.search(r'data-chapter="(\d+)"', article)[1])
        counter = iter(overlays[chapter])
        # Overlay the original-image version using the same source glyph bounds.
        article = re.sub(r'(<div class="original-version"><img\b[^>]*>)</div>',
                         lambda img: img[1]+next(counter)+'</div>', article)
        insert = (f'<!-- derivations:chapter-{chapter}:start -->{chapter_resources(chapter)}'
                  f'<!-- derivations:chapter-{chapter}:end -->')
        return article.replace('<div class="excerpt">', insert+'<div class="excerpt">', 1)
    text = re.sub(r'<article\b.*?</article>', article_replace, text, flags=re.S)
    if 'href="assets/review-derivations.css"' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/review-derivations.css">\n</head>', 1)
    if 'href="derivations/index.html"' not in text:
        text = text.replace('<div class="header-actions">', '<div class="header-actions"><a class="explanations-index" href="derivations/index.html">Formula explanations ↗</a>', 1)
    # Install the hash behavior from its maintained source on subsequent builds too.
    text = re.sub(r'function show\(n,scroll=true\)\{.*?(?=for\(const link of links\)link.addEventListener)',
                  lambda _: maintained_show(), text, flags=re.S)
    text = re.sub(r"window.addEventListener\('hashchange',.*?\nsetTextMode\(textMode,false,false\);.*?\n", lambda _: maintained_init(), text, flags=re.S)
    REVIEW.write_text(text)
    write_equation_audit()


def write_equation_audit():
    unique = {r['id']:r for r in SOURCE_AUDIT}
    audit = dict(sourceRows=len(unique),sourceCodes=sorted({code for r in unique.values() for code in r['codes']}),
                 source=list(unique.values()),notes=[dict(topic=t['slug'],location=loc,
                 kind=NOTE_INPUTS.get(t['slug'],{}).get(loc,'derived'),href=f'derivations/{t["slug"]}.html#proof-{loc}')
                 for t in TOPICS for loc in ['main']+[f'step-{i}' for i,s in enumerate(t['steps'],1) if s['equation']]])
    (ROOT/'content/equation-provenance.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')


def maintained_show():
    template = (ROOT/'tools/review/review-template.html').read_text()
    return re.search(r'function show\(n,scroll=true\)\{.*?(?=for\(const link of links\)link.addEventListener)', template, re.S)[0]


def maintained_init():
    template = (ROOT/'tools/review/review-template.html').read_text()
    return re.search(r"window.addEventListener\('hashchange',.*?\nsetTextMode\(textMode,false,false\);.*?\n", template, re.S)[0]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pages-only', action='store_true', help='Do not update the review reader')
    args = parser.parse_args()
    build_pages()
    if not args.pages_only:
        update_reader()
    print(f'Built {len(TOPICS)} explanations across {len(BY_CHAPTER)} chapters and a searchable index.')
