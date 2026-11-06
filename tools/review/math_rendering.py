"""Reviewed TeX sources and cached, strict offline typesetting for the notes."""
from functools import lru_cache
from html import escape
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
INLINE = {
    'Qh': r'Q_h', 'Qc': r'Q_c', 'Th': r'T_h', 'Tc': r'T_c',
    'CV': r'C_V', 'CP': r'C_P', 'kB': r'k_{\mathrm B}',
    'kBT': r'k_{\mathrm B}T', 'NA': r'N_{\mathrm A}', 'NAkB': r'N_{\mathrm A}k_{\mathrm B}',
    'nRT': r'nRT', 'nCV': r'nC_V', 'nCP': r'nC_P',
    'Wby': r'W_{\mathrm{by}}', 'Wout': r'W_{\mathrm{out}}', 'Win': r'W_{\mathrm{in}}',
    'Qrev': r'Q_{\mathrm{rev}}', 'δQrev': r'\delta Q_{\mathrm{rev}}',
    'Eint': r'E_{\mathrm{int}}', 'ΔEint': r'\Delta E_{\mathrm{int}}',
    'Sgenerated': r'S_{\mathrm{generated}}', 'Sb': r'S_b',
    'SB': r'S_B', 'SA': r'S_A', 'Tb': r'T_b',
    'Vi': r'V_i', 'Vf': r'V_f', 'Ti': r'T_i', 'Tf': r'T_f',
    'vavg': r'v_{\mathrm{avg}}', 'vrms': r'v_{\mathrm{rms}}',
    'ke': r'k_e', 'En': r'E_n', 'rn': r'r_n', 'λd': r'\lambda_d',
    'pVᵞ': r'pV^\gamma', 'TVᵞ⁻¹': r'TV^{\gamma-1}',
    '⟨v²⟩': r'\langle v^2\rangle', '⟨v⟩²': r'\langle v\rangle^2',
    'ℏ': r'\hbar',
}
INLINE_PATTERN = re.compile(r'(?<!\w)('+ '|'.join(re.escape(k) for k in sorted(INLINE,key=len,reverse=True))+r')(?!\w)')


def validate_catalog(topics):
    rows = json.loads((ROOT/'content/math-expressions.json').read_text())
    expected = {(t['slug'], loc): source for t in topics
                for loc, source in [('main', t['formula'])]+[(f'step-{i}', s['equation']) for i, s in enumerate(t['steps'], 1)] if source}
    catalog = {(r['topic'], r['location']): r for r in rows}
    assert len(catalog) == len(rows), 'Duplicate math catalog key'
    assert set(catalog) == set(expected), 'Every expression needs a reviewed TeX rendering'
    for key, source in expected.items():
        assert catalog[key]['source'] == source, f'{key}: source changed; review its TeX before rebuilding'
        assert catalog[key]['tex'].strip(), key
    return rows


@lru_cache(maxsize=1)
def rendered_math():
    from derivation_content import TOPICS
    rows = validate_catalog(TOPICS)
    rows += [dict(topic='inline',location=k,tex=tex) for k,tex in INLINE.items()]
    result = subprocess.run(['node', str(ROOT/'tools/review/render_math.cjs')],
                            input=json.dumps(rows), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def math_html(topic, location='main', inline=False):
    key = f'{topic}/{location}'
    markup = rendered_math()[key]['inline' if inline else 'display']
    return f'<span class="typeset-math" data-math-key="{escape(key,quote=True)}">{markup}</span>'


def math_text(text):
    """Typeset reviewed inline symbols without guessing at ordinary words."""
    parts=[]
    end=0
    for match in INLINE_PATTERN.finditer(text):
        parts.extend([escape(text[end:match.start()]),math_html('inline',match[0],inline=True)])
        end=match.end()
    parts.append(escape(text[end:]))
    return ''.join(parts)


def review_styles():
    return ('<link rel="stylesheet" href="assets/math/katex.min.css">'
            '<link rel="stylesheet" href="assets/math/physics-math.css">')


def write_layout_fixture(topics):
    """A developer fixture puts every displayed expression in the real layout."""
    sections=[]
    for topic in topics:
        blocks=[]
        for loc, source in [('main',topic['formula'])]+[(f'step-{i}',s['equation']) for i,s in enumerate(topic['steps'],1)]:
            if not source:
                continue
            blocks.append(f'<div class="equation{" main-equation" if loc=="main" else ""}" id="{topic["slug"]}--{loc}" data-check="{topic["slug"]}/{loc}">'
                          f'<span class="equation-status">{escape(loc)}</span>'
                          f'<a class="equation-value" href="../../../derivations/{topic["slug"]}.html#proof-{loc}" '
                          f'data-plain-math="{escape(source,quote=True)}">{math_html(topic["slug"],loc)}</a></div>')
        sections.append(f'<section><h2>{escape(topic["title"])}</h2>'+''.join(blocks)+'</section>')
    head=''.join(f'<link rel="stylesheet" href="../../../{path}">' for path in ['derivations/assets/inquiry.css','derivations/assets/reading.css','assets/math/katex.min.css','assets/math/physics-math.css'])
    path=ROOT/'tools/review/fixtures/math-layout.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    '<title>Equation layout checks</title>'+head+'</head><body><div class="layout"><main><h1>Equation layout checks</h1>'
                    '<p>All 660 reviewed expressions, using the same styles and local fonts as the explanations.</p>'
                    +''.join(sections)+'</main></div></body></html>')
