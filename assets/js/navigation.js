// Keep fixed-navigation spacing correct when menus, fonts or text size change.
(() => {
  const nav = document.querySelector('body.fixed-top-nav #navbar');
  if (!nav) return;
  const reserveSpace = () => document.documentElement.style.setProperty('--navigation-height', `${Math.ceil(nav.getBoundingClientRect().height)}px`);
  reserveSpace();
  if ('ResizeObserver' in window) new ResizeObserver(reserveSpace).observe(nav);
  else window.addEventListener('resize', reserveSpace);
})();
