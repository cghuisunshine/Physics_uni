// Pre-render every reviewed expression; no client-side math engine is needed.
const fs = require('node:fs');
const katex = require('../../assets/math/katex.cjs');
const rows = JSON.parse(fs.readFileSync(0, 'utf8'));
const rendered = {};
const options = {
  throwOnError: true, strict: 'error', trust: false, output: 'htmlAndMathml',
  macros: {'\\vb': '\\boldsymbol{#1}', '\\dd': '\\mathrm{d}', '\\avg': '\\langle #1\\rangle'}
};
for (const row of rows) {
  const lines = row.tex.split(';');
  const display = lines.length > 1 ? '\\begin{gathered}'+lines.join('\\\\[0.35em]')+'\\end{gathered}' : row.tex;
  try {
    rendered[`${row.topic}/${row.location}`] = {
      display: katex.renderToString(display, {...options, displayMode: true}),
      inline: katex.renderToString(lines.join('\\quad;\\quad '), {...options, displayMode: false})
    };
  } catch (error) {
    process.stderr.write(`${row.topic}/${row.location}: ${error.message}\n`);
    process.exit(1);
  }
}
process.stdout.write(JSON.stringify(rendered));
