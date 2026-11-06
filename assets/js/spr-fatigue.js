// FIG. R05.1: fatigue of hybrid self-piercing-riveted joints, drawn from precomputed data
// (assets/data/figures/spr-fatigue.json). The structural stresses and S-N curves are the article's
// outputs; the browser only switches between them.
(function () {
  'use strict';
  var root = document.querySelector('[data-spr-fatigue]');
  if (!root) return;
  var svg = root.querySelector('svg'), tip = root.querySelector('[data-sp-tip]');
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var COLOURS = { LAP: '#82e2de', PEEL: '#e7b25f' };
  var W = 640, H = 420, M = { l: 62, r: 16, t: 16, b: 46 };
  var NX = [3, 6.5], yr = [0, 1];
  var data, view = 'two_parameter', nodes = [], g = {};

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n);
    return n;
  }
  function sx(N) { return M.l + (Math.log10(N) - NX[0]) / (NX[1] - NX[0]) * (W - M.l - M.r); }
  function sy(v) { return H - M.b - (Math.log10(v) - yr[0]) / (yr[1] - yr[0]) * (H - M.t - M.b); }
  function sub(node, text) {
    node.textContent = '';
    text.split(/(_\w)/).forEach(function (part) {
      if (part.charAt(0) === '_') el('tspan', { 'baseline-shift': 'sub', 'font-size': '75%' }, node).textContent = part.slice(1);
      else node.appendChild(document.createTextNode(part));
    });
  }
  function value(t) { return view === 'force' ? t.Fa : t.sigma[view]; }
  // Marker per thickness stack (Al / steel), matching the legend.
  function shape(t) {
    var k = t.t_al + '/' + t.t_steel;
    if (k === '1.5/1.5') return 'M0 -4.2a4.2 4.2 0 1 0 0.01 0z';
    if (k === '1.5/1.8') return 'M-3.7 -3.7h7.4v7.4h-7.4z';
    if (k === '2/1.5') return 'M0 -4.8l4.6 8h-9.2z';
    return 'M0 -5l5 5l-5 5l-5 -5z';
  }

  function size() {
    var w = Math.max(300, Math.round(root.querySelector('.sp-stage').clientWidth));
    W = w; H = Math.round(w < 520 ? w * 0.86 : w * 0.6); M.l = w < 520 ? 54 : 62;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  }

  function build() {
    size();
    svg.textContent = ''; nodes = [];
    var clip = el('clipPath', { id: 'sp-clip' }, el('defs', {}));
    el('rect', { x: M.l, y: M.t, width: W - M.l - M.r, height: H - M.t - M.b }, clip);
    g.grid = el('g', {}); g.band = el('g', { 'clip-path': 'url(#sp-clip)' }); g.pts = el('g', {}); g.axes = el('g', {});
    g.bandPath = el('path', { class: 'sp-band' }, g.band);
    g.lo = el('path', { class: 'sp-bound' }, g.band); g.hi = el('path', { class: 'sp-bound' }, g.band);
    g.med = el('path', { class: 'sp-median' }, g.band);
    g.ylabel = el('text', { class: 'sp-label', 'text-anchor': 'middle', transform: 'translate(14 ' + ((H - M.b + M.t) / 2) + ') rotate(-90)' }, g.axes);
    sub(el('text', { class: 'sp-label', x: (W + M.l - M.r) / 2, y: H - 8, 'text-anchor': 'middle' }, g.axes), root.dataset.xlabel);
    data.tests.forEach(function (t, i) {
      var n = el('path', { d: shape(t), class: 'sp-pt' + (t.adhesive ? ' sp-filled' : ''), tabindex: 0 }, g.pts);
      n.style.setProperty('--c', COLOURS[t.geometry]);
      var show = function () { showTip(i); }, hide = function () { tip.hidden = true; };
      n.addEventListener('pointerenter', show); n.addEventListener('focus', show);
      n.addEventListener('pointerleave', hide); n.addEventListener('blur', hide);
      nodes[i] = n;
    });
    render(false);
  }

  function curve(model, factor) {
    var d = '';
    for (var i = 0; i <= 30; i++) {
      var lg = NX[0] + i / 30 * (NX[1] - NX[0]);
      d += (i ? 'L' : 'M') + sx(Math.pow(10, lg)).toFixed(1) + ' ' + sy(Math.pow(10, model.intercept + model.slope * lg) * factor).toFixed(1);
    }
    return d;
  }

  function render(animate) {
    var model = data.models[view] || null, vals = data.tests.map(value);
    var lo = Math.log10(Math.min.apply(null, vals)), hi = Math.log10(Math.max.apply(null, vals));
    var pad = (hi - lo) * 0.12;
    yr = [lo - pad, hi + pad];
    // Grid and ticks for the current quantity.
    g.grid.textContent = '';
    g.axes.querySelectorAll('.sp-tick').forEach(function (n) { n.remove(); });
    for (var e = 3; e <= 6; e++) {
      el('line', { class: 'sp-grid', x1: sx(Math.pow(10, e)), x2: sx(Math.pow(10, e)), y1: M.t, y2: H - M.b }, g.grid);
      var tx = el('text', { class: 'sp-tick', x: sx(Math.pow(10, e)), y: H - M.b + 18, 'text-anchor': 'middle' }, g.axes);
      tx.appendChild(document.createTextNode('10')); el('tspan', { 'baseline-shift': 'super', 'font-size': '9' }, tx).textContent = e;
    }
    [1, 2, 5].forEach(function (m) {
      for (var d = -1; d <= 4; d++) {
        var v = m * Math.pow(10, d), y = Math.log10(v);
        if (y < yr[0] || y > yr[1]) continue;
        el('line', { class: 'sp-grid', x1: M.l, x2: W - M.r, y1: sy(v), y2: sy(v) }, g.grid);
        el('text', { class: 'sp-tick', x: M.l - 8, y: sy(v) + 4, 'text-anchor': 'end' }, g.axes).textContent = v >= 1 ? String(v) : v.toFixed(1);
      }
    });
    el('rect', { class: 'sp-frame', x: M.l, y: M.t, width: W - M.l - M.r, height: H - M.t - M.b }, g.grid);
    sub(g.ylabel, view === 'force' ? root.dataset.ylabelForce : root.dataset.ylabelStress);
    // Median S-N curve and its +/- 2s band, in log10 of the plotted quantity; none for the raw force.
    g.band.style.display = model ? '' : 'none';
    if (model) {
      var f = Math.pow(10, model.n_std * model.sd_log10);
      g.bandPath.setAttribute('d', curve(model, f) + 'L' + curve(model, 1 / f).slice(1).split('L').reverse().join('L') + 'Z');
      g.hi.setAttribute('d', curve(model, f)); g.lo.setAttribute('d', curve(model, 1 / f)); g.med.setAttribute('d', curve(model, 1));
    }
    data.tests.forEach(function (t, i) {
      var n = nodes[i];
      n.style.transition = animate && !reduce ? 'transform 480ms cubic-bezier(.2,.7,.2,1)' : 'none';
      n.style.transform = 'translate(' + sx(t.N).toFixed(1) + 'px,' + sy(value(t)).toFixed(1) + 'px)';
    });
    root.querySelector('[data-sp-n]').textContent = data.tests.length;
    root.querySelector('[data-sp-band]').textContent = model ? '× ' + model.band_ratio.toFixed(2) : root.dataset.noFit;
    root.querySelectorAll('[data-sp-view]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.spView === view)); });
    var label = { force: root.dataset.viewForce, one_parameter: root.dataset.viewOne, two_parameter: root.dataset.viewTwo }[view];
    svg.setAttribute('aria-label', (model ? root.dataset.label : root.dataset.labelForce).replace('%n', data.tests.length).replace('%v', label.toLowerCase()).replace('%b', model ? model.band_ratio.toFixed(1) : ''));
  }

  function showTip(i) {
    var t = data.tests[i], s = svg.getBoundingClientRect().width / W;
    var unit = view === 'force' ? ' N' : ' MPa';
    tip.textContent = (t.geometry === 'LAP' ? root.dataset.lap : root.dataset.peel) + ' · ' + (t.adhesive ? root.dataset.hybrid : root.dataset.spr) +
      ' · ' + t.t_al + '/' + t.t_steel + ' mm · N = ' + Math.round(t.N).toLocaleString('en-US') + ' · ' + Number(value(t).toPrecision(3)) + unit;
    tip.style.left = (sx(t.N) * s) + 'px'; tip.style.top = (sy(value(t)) * s) + 'px'; tip.hidden = false;
  }

  fetch(root.dataset.src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (json) {
    data = json;
    root.querySelectorAll('[data-sp-view]').forEach(function (b) { b.addEventListener('click', function () { view = b.dataset.spView; render(true); }); });
    root.querySelector('[data-sp-controls]').hidden = false;
    build();
    var pending, lastW = W;
    window.addEventListener('resize', function () {
      clearTimeout(pending);
      pending = setTimeout(function () { if (Math.round(root.querySelector('.sp-stage').clientWidth) !== lastW) { build(); lastW = W; } }, 150);
    });
    root.classList.add('is-ready');
  }).catch(function () { root.querySelector('[data-sp-error]').hidden = false; });
})();
