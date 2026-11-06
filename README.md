# University Physics

- [Practice Studio](physics-practice.html): 4,170 original end-of-chapter problems from all 44 chapters, with matching original worked solutions, chapter/topic selection, drawing tools, progress tracking, review queues, and optional AI assistance.
- [Review and Summary](Physics_Review_and_Summary_Tutorial.html): the textbook's 44 chapter summaries, with an Original image / Selectable text switch, a Copy text button, and linked formula explanations.
- [Formula explanations](derivations/index.html): 131 original notes across all 44 chapters, with 146 labeled diagrams, equation-level proof links, explicit starting assumptions, worked examples, and deeper branches at the steps that use them.
- [Contents](content.html)

The practice layout and controls reuse the Physics11 practice studio. The content comes from `Physics text (TOC).pdf`; original worked solutions come from `Physics answer (TOC).pdf`. Shared table exercises remain individually selectable. Expand **Original pages, diagrams & tables** to see context and diagrams that lie outside the problem crop.

Open the HTML files with the `assets/practice/` directory alongside them, or serve this repository as a static site. Problems and model answers are local assets; online AI checks, generation, and optional Firebase sync require internet access. University progress and sync collections use a separate `physicsUni` namespace. After a missed or partly correct textbook answer, a similar AI question appears automatically, using the original problem and worked solution. Its multiple-choice retries and explanation are saved with the missed attempt without changing the textbook score. Turn automatic follow-ups on or off in the top-right practice settings.

## Rebuild

Install `tools/practice/requirements.txt` in a Python environment, put the two original TOC PDFs in the repository root, and run:

```sh
python tools/practice/build_practice.py --rescan
```

The builder validates every chapter's continuous problem numbering and one-to-one solution numbering. It retains original equations and diagrams as WebP excerpts, records source page references in `content/`, and produces `physics-practice.html`, `physics-problems.html`, and `physics-monitor.html`.

After interface-only edits, rebuild with `--html-only`. Browser checks run with:

```sh
node tools/practice/check_practice.mjs
node --test tools/practice/physics-followup.test.cjs
```

These checks use an installed Google Chrome and keep test history in a temporary browser profile. AI and sync controls retain the reference studio's service integration; browser checks do not submit student work to those services.

## Rebuild the selectable review reader

Install `tools/review/requirements.txt` in the Python environment and provide the original `Physics text (TOC).pdf` in the repository root. Poppler (`pdftotext` and `pdftocairo`) is required to extract the original image crops.

```sh
python tools/review/build_review.py --extract
node --test tools/review/review-text.test.cjs
node tools/review/check_review.mjs
```

The selectable version uses real SVG text and embedded fonts reconstructed from the PDF glyph outlines. Original vector artwork and equation layout are preserved. Legacy math encodings are mapped to Unicode; copying reconstructs column order, superscripts, subscripts, and recognized fractions. All 65 original image payloads remain intact. `content/review-text-audit.json` records the source pages and glyph coverage.

## Formula explanations and follow-up branches

Each chapter has an **Explain & derive** panel. Matching source headings also link to the notes in both the original-image and selectable-text versions. Follow-up links occur at the exact derivation step that needs the additional explanation; the return link goes back to that step. Each note also links to its exact formula entry in the chapter summary. Existing interactive centripetal-acceleration links are retained.

Edit `tools/review/derivation_content.py` to extend the explanations and their step-level branches. Rebuild without PDFs or additional Python dependencies:

```sh
python3 tools/review/build_derivations.py
node tools/review/check_derivations.mjs
```

The original SVG illustrations are generated from `tools/review/derivation_diagrams.py`. Every topic has a concept diagram; 15 additional figures illustrate specific steps. Captions explain how to read each picture and link to its equation proof. The images include accessible descriptions, scale to phones, open at full size, print, and work offline. Curves use their stated mathematical functions; captions identify schematic drawings. To rebuild only the notes and diagrams, use `python3 tools/review/build_derivations.py --pages-only`.

Run `python3 -m unittest discover -s tools/review -p test_derivation_diagrams.py` to check image coverage, accessible descriptions, proof destinations, and scientific geometry (circular forces, lens rays, Carnot paths, terminal force balance, and velocity changes).

In environments where Chrome cannot launch, `node tools/review/check_derivations.mjs --static-only` checks every file, asset and return fragment. With `jsdom` installed, `node --test tools/review/derivation-navigation.test.cjs` additionally checks the actual navigation scripts, search, summary restoration and reader controls without a browser. Browser layout and screenshot checks still require Chrome.

Every displayed equation in the notes has a status and a link to its own explanation. Derived results open proof sections with the argument and links to earlier results; definitions, fundamental postulates, constitutive models and reference values are explicitly distinguished. Matching links are attached directly to equation-bearing rows in both textbook reading modes, including numbered and unnumbered relations. Returning from a textbook equation opens the same chapter and equation location.

`content/equation-provenance.json` records the equation audit. Numbered-source destinations are reviewed in `tools/review/equation_provenance.py`; unnumbered rows are reviewed individually in `content/review-unnumbered-equations.json`. New source equations without a reviewed assignment stop the build. `tools/review/derivation_supplements.py` contains the additional arguments needed beyond the initial selected-formula notes.

The full review builder also generates these notes and links. Equations are selectable Unicode text and the CSS/JavaScript is local, so the pages work offline. `content/derivations.json` records topic files, proof anchors, equation statuses, return anchors and branch targets. Examples of deeper chains include ideal gas → equipartition → Boltzmann weights → reservoir counting and the statistical postulate, and quantum hydrogen → Schrödinger dynamics and angular-momentum algebra.
