// One shared disclosure menu for every layout; opening it never moves the page.
(() => {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  const button = nav.querySelector('.navbar-toggler');
  const panel = document.getElementById('navbarNav');
  const backdrop = document.querySelector('.navigation-backdrop');
  const mobile = window.matchMedia('(max-width: 991.98px)');
  let open = false;
  let previousOverflow = '';
  let savedInert = [];
  function setOpen(value, restoreFocus = true) {
    value = value && mobile.matches;
    if (value === open) return;
    open = value;
    panel.classList.toggle('show', open);
    button.classList.toggle('collapsed', !open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    backdrop.hidden = !open;
    if (open) {
      previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      savedInert = [...document.querySelectorAll('main, footer')].map(element => [element, element.inert]);
      savedInert.forEach(([element]) => { element.inert = true; });
      nav.setAttribute('role', 'dialog');
      nav.setAttribute('aria-modal', 'true');
    } else {
      document.body.style.overflow = previousOverflow;
      savedInert.forEach(([element, inert]) => { element.inert = inert; });
      savedInert = [];
      nav.removeAttribute('role');
      nav.removeAttribute('aria-modal');
      if (restoreFocus && mobile.matches) button.focus({preventScroll: true});
    }
  }
  button.addEventListener('click', () => setOpen(!open));
  backdrop.addEventListener('click', () => setOpen(false));
  panel.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setOpen(false, false)));
  document.addEventListener('keydown', event => {
    if (!open) return;
    if (event.key === 'Escape') { event.preventDefault(); setOpen(false); }
    if (event.key === 'Tab') {
      const focusable = [...nav.querySelectorAll('a[href], button')].filter(element => element.getClientRects().length);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  mobile.addEventListener('change', () => setOpen(false, false));
  function reserveSpace() {
    const height = Math.ceil(nav.getBoundingClientRect().height);
    const viewport = window.visualViewport?.height || window.innerHeight;
    const style = document.documentElement.style;
    if (document.body.classList.contains('fixed-top-nav')) style.setProperty('--navigation-height', `${height}px`);
    style.setProperty('--navigation-offset', `${height + 16}px`);
    style.setProperty('--navigation-available-height', `${Math.max(0, Math.floor(viewport - height))}px`);
  }
  reserveSpace();
  if ('ResizeObserver' in window) new ResizeObserver(reserveSpace).observe(nav);
  window.addEventListener('resize', reserveSpace);
  window.visualViewport?.addEventListener('resize', reserveSpace);
})();
