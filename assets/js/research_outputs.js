// Progressive enhancement. All records are rendered by Jekyll and usable without JavaScript.
(() => {
  const catalogue = document.querySelector('.output-catalogue');
  if (!catalogue) return;
  const controls = catalogue.querySelector('.catalogue-filters');
  const buttons = [...controls.querySelectorAll('button[data-filter]')];
  const cards = [...catalogue.querySelectorAll('.research-output')];
  const count = catalogue.querySelector('#output-count');
  const searchPanel = catalogue.querySelector('.output-atlas-search');
  const search = catalogue.querySelector('#output-search');
  const empty = catalogue.querySelector('#output-empty');
  const reset = catalogue.querySelector('#output-reset');
  let category = 'all';
  const normalise = value => (value || '').normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const index = cards.map(card => normalise(card.textContent));
  function filter() {
    const query = normalise(search.value);
    let visible = 0;
    cards.forEach((card, i) => {
      card.hidden = !((category === 'all' || card.dataset.category === category) &&
        (!query || index[i].includes(query)));
      if (!card.hidden) visible += 1;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    count.textContent = count.dataset.countTemplate.replace('%visible%', visible).replace('%total%', cards.length);
    empty.hidden = visible !== 0;
    reset.hidden = category === 'all' && !query;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filter();
  }));
  search.addEventListener('input', filter);
  reset.addEventListener('click', () => {
    category = 'all'; search.value = ''; filter(); search.focus();
  });
  function revealLinkedResource() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const card = document.getElementById(id)?.closest('.research-output');
    if (card?.hidden) {
      category = 'all'; search.value = ''; filter(); card.scrollIntoView();
    }
  }
  controls.hidden = false;
  searchPanel.hidden = false;
  search.hidden = false;
  filter();
  window.addEventListener('hashchange', revealLinkedResource);
  revealLinkedResource();
})();
