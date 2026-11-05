// FIG. R03: ECP master curves for sharp notches, drawn from sharCP outputs
// (assets/data/figures/sharcp-ecp-validation.json). No criterion is evaluated here.
(function () {
  'use strict';
  var root = document.querySelector('[data-sharcp-figure]');
  if (!root) return;
  var svg = root.querySelector('svg');
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Drawing units equal CSS pixels, so labels keep their size on narrow screens.
  var W = 640, H = 420, M = { l: 64, r: 18, t: 18, b: 46 };
  var Nmin = 1e3, Nmax = 3e7;
  var data, current = null, nodes = [], tip = root.querySelector('[data-sf-tip]');
  var showCal = root.querySelector('[data-sf-cal]'), showVal = root.querySelector('[data-sf-val]');

  function el(name, attrs, parent) {
    var node = document.createElementNS(NS, name);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(node);
    return node;
  }
  var lx = function (n) { return M.l + (Math.log10(n) - Math.log10(Nmin)) / (Math.log10(Nmax) - Math.log10(Nmin)) * (W - M.l - M.r); };
  var yRange = [1, 10];
  var ly = function (p) { return H - M.b - (Math.log10(p) - yRange[0]) / (yRange[1] - yRange[0]) * (H - M.t - M.b); };
  function fmt(x) { return x >= 1e4 || x < 1e-2 ? x.toExponential(1).replace('e+', 'e') : String(Number(x.toPrecision(3))); }

  var gGrid = el('g', { class: 'sf-grid' }), gBand = el('g', {}), gPts = el('g', {}), gAxes = el('g', { class: 'sf-axes' });
  var band = el('path', { class: 'sf-band' }, gBand), lo = el('path', { class: 'sf-bound' }, gBand),
      hi = el('path', { class: 'sf-bound' }, gBand), med = el('path', { class: 'sf-median' }, gBand);
  var ylabel = el('text', { class: 'sf-label', 'text-anchor': 'middle' }, gAxes);
  var xlabel = el('text', { class: 'sf-label', 'text-anchor': 'middle' }, gAxes);
  subscript(xlabel, root.dataset.xlabel);

  // 'N_f' -> N with subscript f.
  function subscript(node, text) {
    node.textContent = '';
    text.split(/(_\w)/).forEach(function (part) {
      if (part.charAt(0) === '_') el('tspan', { 'baseline-shift': 'sub', 'font-size': '75%' }, node).textContent = part.slice(1);
      else node.appendChild(document.createTextNode(part));
    });
  }

  function size() {
    var width = Math.max(300, Math.round(root.querySelector('.sf-stage').clientWidth));
    W = width; H = Math.round(width < 520 ? width * 0.86 : width * 0.62);
    M.l = width < 520 ? 52 : 64;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    ylabel.setAttribute('transform', 'translate(14 ' + ((H - M.b + M.t) / 2) + ') rotate(-90)');
    xlabel.setAttribute('x', (W + M.l - M.r) / 2); xlabel.setAttribute('y', H - 8);
  }

  function curve(A) {
    var d = '', b = current.b;
    for (var i = 0; i <= 40; i++) { var n = Math.pow(10, Math.log10(Nmin) + i / 40 * (Math.log10(Nmax) - Math.log10(Nmin))); d += (i ? 'L' : 'M') + lx(n).toFixed(1) + ' ' + ly(A * Math.pow(n, b)).toFixed(1); }
    return d;
  }

  function axes() {
    gGrid.textContent = ''; gAxes.querySelectorAll('.sf-tick').forEach(function (t) { t.remove(); });
    for (var e = 3; e <= 7; e++) {
      el('line', { x1: lx(Math.pow(10, e)), x2: lx(Math.pow(10, e)), y1: M.t, y2: H - M.b }, gGrid);
      // Decade label 10^e, with the exponent as a superscript tspan.
      var t = el('text', { class: 'sf-tick', x: lx(Math.pow(10, e)), y: H - M.b + 18, 'text-anchor': 'middle' }, gAxes);
      t.appendChild(document.createTextNode('10'));
      el('tspan', { 'baseline-shift': 'super', 'font-size': '9' }, t).textContent = e;
    }
    for (var y = Math.ceil(yRange[0]); y <= Math.floor(yRange[1]); y++) {
      el('line', { x1: M.l, x2: W - M.r, y1: ly(Math.pow(10, y)), y2: ly(Math.pow(10, y)) }, gGrid);
      el('text', { class: 'sf-tick', x: M.l - 8, y: ly(Math.pow(10, y)) + 4, 'text-anchor': 'end' }, gAxes).textContent = fmt(Math.pow(10, y));
    }
    el('rect', { x: M.l, y: M.t, width: W - M.l - M.r, height: H - M.t - M.b, class: 'sf-frame' }, gGrid);
  }

  function points(c) {
    return c.calibration.map(function (p) { return Object.assign({ set: 'cal' }, p); })
      .concat(c.validation.map(function (p) { return Object.assign({ set: 'val' }, p); }));
  }

  function select(key, animate) {
    current = data.criteria[key]; size();
    var pts = points(current), ps = pts.map(function (p) { return Math.log10(p.P); });
    var lowest = Math.log10(current.A_minus * Math.pow(Nmax, current.b)), highest = Math.log10(current.A_plus * Math.pow(Nmin, current.b));
    yRange = [Math.floor(Math.min.apply(null, ps.concat(lowest)) * 4) / 4, Math.ceil(Math.max.apply(null, ps.concat(highest)) * 4) / 4];
    axes();
    ylabel.textContent = root.dataset['ylabel' + key];
    // Closed band: upper bound left to right, then lower bound right to left.
    band.setAttribute('d', curve(current.A_plus) + 'L' + curve(current.A_minus).slice(1).split('L').reverse().join('L') + 'Z');
    lo.setAttribute('d', curve(current.A_minus)); hi.setAttribute('d', curve(current.A_plus)); med.setAttribute('d', curve(current.A));
    pts.forEach(function (p, i) {
      var node = nodes[i];
      if (!node) {
        node = nodes[i] = el(p.mode === 'MIII' ? 'rect' : 'circle', { class: 'sf-pt sf-' + p.set, tabindex: p.set === 'val' ? 0 : -1 }, gPts);
        node.addEventListener('mouseenter', function () { showTip(node); });
        node.addEventListener('focus', function () { showTip(node); });
        node.addEventListener('mouseleave', hideTip); node.addEventListener('blur', hideTip);
      }
      var x = lx(p.N), y = ly(p.P);
      node.__p = p; node.__xy = [x, y];
      if (animate && !reduce) node.style.transition = 'transform 420ms cubic-bezier(.2,.7,.2,1)'; else node.style.transition = 'none';
      node.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      if (p.mode === 'MIII') { node.setAttribute('x', -3.2); node.setAttribute('y', -3.2); node.setAttribute('width', 6.4); node.setAttribute('height', 6.4); }
      else node.setAttribute('r', p.set === 'val' ? 3.6 : 3);
    });
    root.querySelector('[data-sf-rc]').textContent = current.rc_mm.toFixed(3) + ' mm';
    root.querySelector('[data-sf-t]').textContent = current.T_ECP.toFixed(2);
    root.querySelector('[data-sf-in]').textContent = current.validation_inside_band + ' / ' + current.validation.length;
    root.querySelectorAll('[data-sf-key]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.sfKey === key)); });
    svg.setAttribute('aria-label', root.dataset.label.replace('%c', current.name).replace('%i', current.validation_inside_band).replace('%n', current.validation.length));
    toggleSets();
  }

  function currentKey() { return root.querySelector('[data-sf-key][aria-pressed="true"]').dataset.sfKey; }

  function toggleSets() {
    svg.classList.toggle('sf-hide-cal', !showCal.checked);
    svg.classList.toggle('sf-hide-val', !showVal.checked);
  }

  function showTip(node) {
    var p = node.__p, box = svg.getBoundingClientRect(), s = box.width / W;
    tip.textContent = (p.set === 'val' ? root.dataset.val : root.dataset.cal) + ' · ' + p.source + ' · ' + (p.mode === 'MIII' ? 'Mode III' : 'Mode I') + ' · N = ' + fmt(p.N);
    tip.style.left = (node.__xy[0] * s) + 'px'; tip.style.top = (node.__xy[1] * s) + 'px'; tip.hidden = false;
  }
  function hideTip() { tip.hidden = true; }

  fetch(root.dataset.src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (json) {
    data = json;
    root.querySelectorAll('[data-sf-key]').forEach(function (b) { b.addEventListener('click', function () { select(b.dataset.sfKey, true); }); });
    showCal.addEventListener('change', toggleSets); showVal.addEventListener('change', toggleSets);
    root.querySelector('[data-sf-controls]').hidden = false;
    select('FI', false);
    var pending; window.addEventListener('resize', function () { clearTimeout(pending); pending = setTimeout(function () { select(currentKey(), false); }, 150); });
    root.classList.add('is-ready');
  }).catch(function () { root.querySelector('[data-sf-error]').hidden = false; });
})();
