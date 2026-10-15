// Progressive enhancement: every resource is rendered by Jekyll before this runs.
(() => {
  const catalogue = document.querySelector('.output-catalogue');
  if (!catalogue) return;
  const controls = catalogue.querySelector('.catalogue-filters');
  const buttons = [...controls.querySelectorAll('button')];
  const cards = [...catalogue.querySelectorAll('.research-output')];
  const count = catalogue.querySelector('#output-count');
  function filter(category) {
    cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.category !== category; });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    const visible = cards.filter(card => !card.hidden).length;
    count.textContent = `${visible} of ${cards.length} resources shown.`;
  }
  buttons.forEach(button => button.addEventListener('click', () => filter(button.dataset.filter)));
  function revealLinkedResource() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    const card = target?.closest('.research-output');
    if (card?.hidden) {
      filter('all');
      card.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', revealLinkedResource);
  controls.hidden = false;
})();
