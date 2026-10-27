# University Physics

- [Practice Studio](physics-practice.html): 4,170 original end-of-chapter problems from all 44 chapters, with matching original worked solutions, chapter/topic selection, drawing tools, progress tracking, review queues, and optional AI assistance.
- [Review and Summary](Physics_Review_and_Summary_Tutorial.html): the textbook's 44 chapter summaries.
- [Contents](content.html)

The practice layout and controls reuse the Physics11 practice studio. The content comes from `Physics text (TOC).pdf`; original worked solutions come from `Physics answer (TOC).pdf`. Shared table exercises remain individually selectable. Expand **Original pages, diagrams & tables** to see context and diagrams that lie outside the problem crop.

Open the HTML files with the `assets/practice/` directory alongside them, or serve this repository as a static site. Problems and model answers are local assets; online AI checks, generation, and optional Firebase sync require internet access. University progress and sync collections use a separate `physicsUni` namespace.

## Rebuild

Install `tools/practice/requirements.txt` in a Python environment, put the two original TOC PDFs in the repository root, and run:

```sh
python tools/practice/build_practice.py --rescan
```

The builder validates every chapter's continuous problem numbering and one-to-one solution numbering. It retains original equations and diagrams as WebP excerpts, records source page references in `content/`, and produces `physics-practice.html`, `physics-problems.html`, and `physics-monitor.html`.

After interface-only edits, rebuild with `--html-only`. Browser checks run with:

```sh
node tools/practice/check_practice.mjs
```

These checks use an installed Google Chrome and keep test history in a temporary browser profile. AI and sync controls retain the reference studio's service integration; browser checks do not submit student work to those services.
