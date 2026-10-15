// Keep scientific material at readable size; scroll wide content locally.
(() => {
  const article = document.querySelector('d-article');
  if (!article) return;
  article.querySelectorAll('table').forEach(table => {
    const region = document.createElement('div');
    region.className = 'scientific-scroll';
    region.dataset.scrollLabel = 'Table: scroll horizontally';
    table.before(region);
    region.append(table);
  });
  function updateRegions() {
    article.querySelectorAll('.scientific-scroll, pre, mjx-container[display="true"]').forEach(region => {
      const scrollable = region.scrollWidth > region.clientWidth + 1;
      if (scrollable) {
        region.tabIndex = 0;
        region.setAttribute('role', 'region');
        region.setAttribute('aria-label', region.dataset.scrollLabel || (region.tagName === 'PRE' ? 'Code: scroll horizontally' : 'Equation: scroll horizontally'));
      } else {
        region.removeAttribute('tabindex');
        region.removeAttribute('role');
        region.removeAttribute('aria-label');
      }
    });
  }
  updateRegions();
  if (window.MathJax?.startup?.promise) window.MathJax.startup.promise.then(updateRegions);
  if (document.fonts) document.fonts.ready.then(updateRegions);
  window.addEventListener('resize', updateRegions);
})();
