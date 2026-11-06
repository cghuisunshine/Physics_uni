# Local math assets

KaTeX 0.19.1, from the official `katex` npm package, under the included MIT license.
Upstream: https://github.com/KaTeX/KaTeX/releases/tag/v0.19.1

`katex.cjs` is the unmodified minified distribution, renamed for CommonJS build use.
The browser loads the CSS and fonts; formulas are already rendered in the HTML.
`physics-math.css` contains this project's layout rules.

Reviewed TeX and original formula text are paired in `content/math-expressions.json`.
The build rejects a changed or missing source formula and any typesetting error.
