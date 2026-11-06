"""Attach reviewed provenance to equation-bearing source glyph rows.

Neither image payloads nor selectable glyphs are rewritten. Text wrappers and
matching image overlays provide the same destinations in both reading modes.
"""
from html import escape, unescape
import json
import re
from pathlib import Path

from equation_provenance import SOURCE, LABELS

AUDIT = []
EXTRA = {(r['chapter'],r['page'],r['column'],r['baseline']):r for r in
         json.loads((Path(__file__).resolve().parents[2]/'content/review-unnumbered-equations.json').read_text())}


def strip_generated_links(svg, headings=True):
    """Unwrap owned anchors with a stack, including earlier nested wrappers.

    A regex matching an entire anchor cannot safely distinguish nested closing
    tags. Token-level removal preserves original anchors and repairs orphan
    closing tags produced by the former regex implementation.
    """
    stack = []
    def token(m):
        text = m[0]
        if text.startswith('<a '):
            owned = 'class="equation-source-text"' in text or (headings and 'data-derivation-link="true"' in text)
            stack.append(owned)
            return '' if owned else text
        if text == '</a>':
            return text if stack and not stack.pop() else ''
        return '' if stack and stack[-1] else text
    result = re.sub(r'<a\b[^>]*>|</a>|<title>.*?</title>',token,svg,flags=re.S)
    assert not stack, 'Unclosed source anchor'
    return result


def codes_in(text):
    result = []
    for group in re.findall(r'\(([^()]*)\)', text):
        group = re.sub(r'^Eq\.?\s*', '', group)
        pairs = re.findall(r'(\d+)-(\d+)', group)
        if not pairs or re.sub(r'\d+-\d+|to|[,\s]', '', group):
            continue
        if 'to' in group and len(pairs) == 2 and pairs[0][0] == pairs[1][0]:
            result.extend(f'{pairs[0][0]}-{n}' for n in range(int(pairs[0][1]), int(pairs[1][1])+1))
        else:
            result.extend(f'{c}-{n}' for c,n in pairs)
    return list(dict.fromkeys(result))


def annotate(svg, chapter):
    svg = strip_generated_links(svg, headings=False)
    layout = json.loads(unescape(re.search(r'data-copy-layout="([^"]+)"', svg)[1]))
    page = layout['page']
    x0,y0,width,height = map(float, re.search(r'viewBox="([^"]+)"', svg)[1].split())
    column = float(re.search(r'data-column="([^"]+)"', svg)[1])
    glyphs = []
    for match in re.finditer(r'<tspan\b([^>]*class="pdf-char"[^>]*)>(.*?)</tspan>', svg, re.S):
        attrs, char = match.groups()
        x,y,size,end = map(float, re.search(r'data-p="([^"]+)"', attrs)[1].split())
        glyphs.append(dict(x=x,y=y,size=size,end=end,gid=int(re.search(r'data-g="([^"]+)"', attrs)[1]),char=unescape(char)))
    rows = []
    for g in sorted(glyphs, key=lambda g:(g['y'],g['x'])):
        col = int(g['x'] >= column)
        row = next((r for r in reversed(rows) if r['col']==col and abs(r['y']-g['y'])<1.3), None)
        if row is None:
            row = dict(col=col, y=g['y'], glyphs=[])
            rows.append(row)
        row['glyphs'].append(g)
    for r in rows:
        r['text'] = ''.join(g['char'] for g in sorted(r['glyphs'],key=lambda g:g['x']))
        r['codes'] = codes_in(r['text'])
        for code in r['codes']:
            if code not in SOURCE:
                raise ValueError(f'No reviewed equation destination for {code}: {r["text"]}')
    numbered = [r for r in rows if r['codes']]
    lookup, overlays = {}, []
    for row in rows:
        if not row['codes'] and not any(c in row['text'] for c in '=≈≥≤'):
            continue
        key = (chapter,page,row['col'],round(row['y'],1))
        if row['codes']:
            records = [SOURCE[code] for code in row['codes']]
            # A block containing a definition and a consequence needs a derivation.
            status = next((r for r in records if r['kind']=='derived'), records[0]).copy()
        elif key in EXTRA:
            reviewed = EXTRA[key]
            if reviewed['text'] != row['text']:
                raise ValueError(f'Source equation changed and needs review: {key}')
            status = dict(kind=reviewed['kind'],topic=reviewed['topic'])
        else:
            raise ValueError(f'Unreviewed unnumbered equation: {key}, {row["text"]}')
        ident = f'chapter-{chapter}--equation-{page}-{row["col"]}-{round(row["y"]*10)}'
        dest = f'derivations/{status["topic"]}.html?review={ident}#proof-main'
        label = LABELS[status['kind']]
        description = f'{label}: '+(', '.join(row['codes']) if row['codes'] else 'additional relation')
        left = max(x0,min(g['x'] for g in row['glyphs']))
        right = min(x0+width,max(g['end'] for g in row['glyphs']))
        top = max(y0,min(g['y']-.92*g['size'] for g in row['glyphs']))
        bottom = min(y0+height,max(g['y']+.2*g['size'] for g in row['glyphs']))
        style = f'left:{100*(left-x0)/width:.4f}%;top:{100*(top-y0)/height:.4f}%;width:{100*(right-left)/width:.4f}%;height:{100*(bottom-top)/height:.4f}%'
        overlays.append(f'<a class="source-equation-link" id="{ident}" data-equation-id="{ident}" data-kind="{status["kind"]}" href="{dest}" title="{escape(description,quote=True)}" aria-label="{escape(description,quote=True)}" style="{style}"></a>')
        record = dict(id=ident,chapter=chapter,page=page,column=row['col'],baseline=round(row['y'],3),codes=row['codes'],text=row['text'],kind=status['kind'],topic=status['topic'],href=dest)
        AUDIT.append(record)
        for g in row['glyphs']:
            lookup[g['gid']] = record
    anchor_spans = [(m.start(),m.end()) for m in re.finditer(r'<a\b[^>]*>.*?</a>',svg,re.S)]
    def wrap(match):
        if any(start < match.start() < end for start,end in anchor_spans):
            return match[0]
        ids = [int(x) for x in re.findall(r'data-g="(\d+)"',match[0])]
        entries = [lookup[i] for i in ids if i in lookup]
        if not entries:
            return match[0]
        entry = entries[0]
        label = escape(f'{LABELS[entry["kind"]]} — open the explanation',quote=True)
        return f'<a class="equation-source-text" data-equation-id="{entry["id"]}" data-kind="{entry["kind"]}" href="{entry["href"]}" aria-label="{label}"><title>{label}</title>{match[0]}</a>'
    return re.sub(r'<text\b[^>]*>.*?</text>',wrap,svg,flags=re.S), ''.join(overlays)
