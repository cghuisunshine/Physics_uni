// DOM-level navigation checks for environments that cannot launch Chrome.
// Requires jsdom; these do not substitute for browser layout/visual checks.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {resolve} = require('node:path');
const {JSDOM, VirtualConsole} = require('jsdom');
const root = resolve(__dirname, '../..');
const inquiryScript = readFileSync(resolve(__dirname, 'inquiry.js'), 'utf8');
const topics = JSON.parse(readFileSync(resolve(root, 'content/derivations.json'), 'utf8'));
const provenance = JSON.parse(readFileSync(resolve(root, 'content/equation-provenance.json'), 'utf8'));

function note(slug, query='') {
  const dom = new JSDOM(readFileSync(resolve(root, `derivations/${slug}.html`), 'utf8'), {
    url: `https://physics.test/derivations/${slug}.html${query}`, runScripts: 'outside-only'
  });
  dom.window.eval(inquiryScript);
  return dom;
}

test('every derivation has its own exact summary return and complete teaching sections', () => {
  for (const topic of topics) {
    const dom = note(topic.slug);
    const document = dom.window.document;
    assert.equal(document.querySelector('h1').textContent, topic.title);
    assert.ok(document.querySelectorAll('.step').length >= 4);
    assert.ok(document.querySelector('.setup').textContent.includes('When this applies'));
    assert.ok(document.querySelector('#example p').textContent.length > 30);
    assert.equal(document.querySelector('.summary-return a').hash, `#${topic.summaryAnchor}`);
    assert.equal(document.querySelectorAll('.equation').length, topic.equations.length);
    assert.equal(document.querySelectorAll('details.equation-proof').length,0);
    assert.equal(document.querySelectorAll('.proof-library').length,1);
    assert.ok(!document.body.textContent.includes('Earlier results used in this argument:'));
    for (const equation of topic.equations) {
      const block = document.getElementById(`equation-${equation.location}`);
      assert.equal(block.dataset.kind, equation.kind);
      const link = block.querySelector('a[data-proof-link]');
      assert.equal(link.hash, `#${equation.proof}`);
      const proof = document.getElementById(equation.proof);
      assert.ok(proof.querySelector('.proof-body').textContent.length > 100);
      assert.equal(proof.dataset.kind, equation.kind);
      link.click();
      assert.equal(proof.dataset.currentProof,'true');
      assert.equal(document.querySelectorAll('[data-current-proof]').length,1);
      assert.equal(document.activeElement,proof);
      assert.equal(proof.hidden,false);
    }
    for (const branch of topic.branches) {
      const link = document.querySelector(`#step-${branch.step} .branch`);
      const url = new URL(link.href);
      assert.equal(url.searchParams.get('from'), topic.slug);
      assert.equal(url.searchParams.get('step'), `step-${branch.step}`);
      const child = note(branch.target, url.search);
      const back = child.window.document.querySelector('[data-context-return]');
      assert.equal(back.getAttribute('href'), `${topic.slug}.html#step-${branch.step}`);
      child.window.close();
    }
    dom.window.close();
  }
});

test('the Carnot argument reads through the cancellation, with equations and illustrations in context', () => {
  const dom=note('carnot'), d=dom.window.document;
  const reading=d.querySelector('#proof-main');
  assert.ok(reading.querySelector('.reading-body>.concept-figure'));
  assert.ok(reading.querySelector('.reading-body>p').textContent.includes('adiabatic legs'));
  const explanation=d.querySelector('#proof-step-4 .proof-body');
  assert.equal(explanation.firstElementChild.tagName,'P');
  assert.ok(explanation.firstElementChild.textContent.includes('logarithms cancel'));
  const equation=explanation.querySelector('.equation');
  assert.ok(equation.previousElementSibling.textContent.includes('What remains'));
  assert.ok(equation.nextElementSibling.textContent.includes('without using an entropy formula'));
  const figure=d.querySelector('#step-3 .concept-figure');
  assert.ok(figure);
  const question=d.querySelector('#step-3 .branch');
  assert.ok(question.textContent.includes('adiabatic relation'));
  assert.equal(new URL(question.href).searchParams.get('step'),'step-3');
  dom.window.close();
});

test('malformed return contexts cannot replace the default summary destination', () => {
  for (const query of ['?from=javascript:alert(1)&step=step-1', '?from=../outside&step=step-2', '?from=ideal-gas&step=missing', '?from=ideal-gas&step=step-0']) {
    const dom = note('equipartition', query);
    assert.equal(dom.window.document.querySelector('[data-context-return]').getAttribute('href'), '../Physics_Review_and_Summary_Tutorial.html#chapter-19--equipartition');
    dom.window.close();
  }
});

test('the formula directory searches chapter names and topics, handles no results, and resets', () => {
  const dom = note('index'), w = dom.window, d = w.document;
  const input = d.querySelector('#topic-search');
  for (const [term, count] of [['', topics.length], ['entropy', 3], ['zzzz-not-physics', 0], ['', topics.length]]) {
    input.value = term;
    input.dispatchEvent(new w.Event('input'));
    const visible = [...d.querySelectorAll('.directory-chapter li')].filter(li => !li.hidden);
    if (term === 'entropy') assert.ok(visible.length >= count); else assert.equal(visible.length, count);
    assert.equal(d.querySelector('#no-results').hidden, visible.length > 0);
  }
  dom.window.close();
});

test('summary deep links restore the correct chapter and exact formula without breaking reader controls', async () => {
  // Image payloads are opaque to script behavior; omit them from this DOM-only check.
  const html = readFileSync(resolve(root, 'Physics_Review_and_Summary_Tutorial.html'), 'utf8')
    .replace(/data:image\/svg\+xml;base64,[A-Za-z0-9+/=]+/g, 'data:image/svg+xml;base64,');
  const errors = [], scrolled = [];
  const console = new VirtualConsole();
  console.on('jsdomError', e => errors.push(e.message));
  const dom = new JSDOM(html, {
    url:'https://physics.test/Physics_Review_and_Summary_Tutorial.html#chapter-19--ideal-gas',
    runScripts:'outside-only', pretendToBeVisual:true, virtualConsole:console
  });
  const w = dom.window, d = w.document;
  w.matchMedia = () => ({matches:false, addEventListener(){}});
  w.scrollTo = () => {};
  w.Element.prototype.scrollIntoView = function() {scrolled.push(this.id||this.dataset.equationId);};
  for (const script of d.querySelectorAll('script:not([type="application/json"])')) w.eval(script.textContent);
  await new Promise(r => w.requestAnimationFrame(r));
  assert.equal(d.querySelectorAll('article:not([hidden])').length,1);
  assert.equal(d.querySelector('article:not([hidden])').id,'chapter-19');
  assert.equal(w.location.hash,'#chapter-19--ideal-gas');
  assert.ok(scrolled.includes('chapter-19--ideal-gas'));
  assert.equal(d.querySelectorAll('.formula-link').length,topics.length);
  assert.equal(d.querySelectorAll('.source-equation-link').length,provenance.sourceRows);
  d.querySelector('#selectable-toggle').checked = true;
  d.querySelector('#selectable-toggle').dispatchEvent(new w.Event('change'));
  assert.ok(d.querySelector('#chapter-19 .regenerated-page a[data-derivation-link]'));
  assert.ok(d.querySelectorAll('#chapter-19 .pdf-char').length>1000);
  const source = provenance.source.find(e=>e.codes.includes('19-22'));
  w.location.hash=`#${source.id}`;
  await new Promise(r => w.setTimeout(r,0));
  await new Promise(r => w.requestAnimationFrame(r));
  assert.ok(scrolled.includes(source.id));
  const visibleSource = d.querySelector(`#chapter-19 .equation-source-text[data-equation-id="${source.id}"]`);
  assert.ok(visibleSource);
  assert.equal(visibleSource.dataset.kind,'derived');
  const child = note(source.topic,`?review=${source.id}#proof-main`);
  assert.equal(child.window.document.querySelector('#proof-main').dataset.currentProof,'true');
  assert.equal(child.window.document.querySelector('[data-context-return]').hash,`#${source.id}`);
  child.window.close();
  d.querySelector('#next').click();
  assert.equal(w.location.hash,'#chapter-20');
  assert.equal(d.querySelector('article:not([hidden])').id,'chapter-20');
  w.location.hash='#chapter-4--centripetal-acceleration';
  await new Promise(r => w.setTimeout(r,0));
  await new Promise(r => w.requestAnimationFrame(r));
  assert.equal(d.querySelector('article:not([hidden])').id,'chapter-4');
  assert.equal(w.location.hash,'#chapter-4--centripetal-acceleration');
  assert.ok(d.querySelector('a[href="centripetal-acceleration-proof.html"]'));
  d.querySelector('#selectable-toggle').checked=false;
  d.querySelector('#selectable-toggle').dispatchEvent(new w.Event('change'));
  d.querySelector('#view').value='all';
  d.querySelector('#view').dispatchEvent(new w.Event('change'));
  assert.equal(d.querySelectorAll('article:not([hidden])').length,44);
  const button = d.querySelector('#chapter-4 .review-button');
  button.click();
  assert.equal(button.getAttribute('aria-pressed'),'true');
  assert.ok(JSON.parse(w.localStorage.getItem('physics-review-v1')).includes(4));
  d.querySelector('#search').value='momentum';
  d.querySelector('#search').dispatchEvent(new w.Event('input'));
  assert.ok([...d.querySelectorAll('.chapter-link:not([hidden])')].some(a=>a.dataset.chapter==='9'));
  assert.deepEqual(errors,[]);
  dom.window.close();
});

test('every source equation has a reviewed status and a real proof destination', () => {
  const slugs = new Set(topics.map(t=>t.slug));
  const ids = new Set();
  for (const row of provenance.source) {
    assert.ok(slugs.has(row.topic),row.id);
    assert.ok(['derived','definition','law','model','reference','notation'].includes(row.kind),row.id);
    assert.ok(!ids.has(row.id));ids.add(row.id);
    const html = readFileSync(resolve(root,`derivations/${row.topic}.html`),'utf8');
    assert.ok(html.includes('id="proof-main"'));
    const href = new URL(row.href,'https://physics.test/');
    assert.equal(href.searchParams.get('review'),row.id);
  }
  assert.equal(provenance.notes.filter(e=>e.kind==='derived').length,
    topics.reduce((n,t)=>n+t.equations.filter(e=>e.kind==='derived').length,0));
});
