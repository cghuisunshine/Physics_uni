(() => {
  'use strict';
  const allowed = new Set(JSON.parse(document.getElementById('inquiry-topics').textContent));
  const query = new URLSearchParams(location.search);
  const from = query.get('from'), step = query.get('step');
  if (allowed.has(from) && /^(?:step-[1-9]\d*|proof-(?:main|step-[1-9]\d*))$/.test(step || '')) {
    for (const link of document.querySelectorAll('[data-context-return]')) {
      link.href = `${from}.html#${step}`;
      link.textContent = '← Return to the step that raised this question';
    }
  }
  const review = query.get('review');
  if (/^chapter-(?:[1-9]|[1-3]\d|4[0-4])--equation-\d+-[01]-\d+$/.test(review || '')) {
    for (const link of document.querySelectorAll('[data-context-return]')) {
      link.href = `../Physics_Review_and_Summary_Tutorial.html#${review}`;
      link.textContent = '← Return to this exact equation in the summary';
    }
  }
  function revealArgument(id = location.hash.slice(1), focus = false) {
    if (!/^proof-(?:main|step-[1-9]\d*)$/.test(id)) return;
    const target = document.getElementById(id);
    if (!target?.matches('.equation-proof')) return;
    for (const previous of document.querySelectorAll('[data-current-proof]')) {
      previous.removeAttribute('data-current-proof');
    }
    target.dataset.currentProof = 'true';
    if (focus) target.focus({preventScroll:true});
  }
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[data-proof-link]');
    if (!link) return;
    revealArgument(link.hash.slice(1), true);
  });
  window.addEventListener('hashchange', () => revealArgument());
  revealArgument();
  const search = document.getElementById('topic-search');
  if (search) search.addEventListener('input', () => {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const chapter of document.querySelectorAll('.directory-chapter')) {
      let visible = 0;
      const title = chapter.querySelector('h2').textContent.toLocaleLowerCase();
      for (const item of chapter.querySelectorAll('li')) {
        item.hidden = !terms.every(term => `${title} ${item.dataset.search}`.includes(term));
        if (!item.hidden) { visible++; count++; }
      }
      chapter.hidden = visible === 0;
    }
    document.getElementById('search-status').textContent = `${count} explanation${count === 1 ? '' : 's'}${terms.length ? ' found' : ''}`;
    document.getElementById('no-results').hidden = count > 0;
  });
})();
