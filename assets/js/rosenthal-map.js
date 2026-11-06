// FIG. R04.1: Rosenthal map of welding and metal AM, drawn from precomputed data
// (assets/data/figures/rosenthal-process-map.json). Points, isolines, the R = R_ boundary and every
// melt-pool outline come from scripts/generate_rosenthal_map.py; nothing is solved in the browser.
(function () {
  'use strict';
  var root = document.querySelector('[data-rosenthal-map]');
  if (!root) return;
  var svg = root.querySelector('.rm-stage svg'), pool = root.querySelector('[data-rm-pool]');
  var tip = root.querySelector('[data-rm-tip]');
  var NS = 'http://www.w3.org/2000/svg';
  // Family colours echo the article's Fig. 5, lightened for the navy panel.
  var COLOURS = { steel: '#ef8a7a', al: '#86d39a', ti: '#7fb2e5', ni: '#c3a6ff', cu: '#d9a36d', co: '#f0b65a' };
  var W = 640, H = 460, M = { l: 58, r: 14, t: 14, b: 46 };
  var X = [-1.6, 1.25], Y = [Math.log10(1.5), Math.log10(32)];
  var data, nodes = [], visible = [], current = 0, families = {}, processes = {};

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n);
    return n;
  }
  function sx(u) { return M.l + (Math.log10(u) - X[0]) / (X[1] - X[0]) * (W - M.l - M.r); }
  function sy(p) { return H - M.b - (Math.log10(p) - Y[0]) / (Y[1] - Y[0]) * (H - M.t - M.b); }
  function sub(node, text) {
    // 'T_m' -> T with subscript m; '~' characters are already combined in the strings.
    node.textContent = '';
    text.split(/(_\w)/).forEach(function (part) {
      if (part.charAt(0) === '_') el('tspan', { 'baseline-shift': 'sub', 'font-size': '75%' }, node).textContent = part.slice(1);
      else node.appendChild(document.createTextNode(part));
    });
  }
  function fmt(x, d) { return Number(x.toPrecision(d || 3)).toString(); }

  function size() {
    var w = Math.max(300, Math.round(root.querySelector('.rm-stage').clientWidth));
    W = w; H = Math.round(w < 520 ? w * 0.95 : w * 0.72); M.l = w < 520 ? 50 : 58;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  }

  function draw() {
    size();
    svg.textContent = ''; nodes = [];
    var clip = el('clipPath', { id: 'rm-clip' }, el('defs', {}));
    el('rect', { x: M.l, y: M.t, width: W - M.l - M.r, height: H - M.t - M.b }, clip);
    var plot = el('g', { 'clip-path': 'url(#rm-clip)' });
    // Feasible region: above the R = R_ boundary (Eq. 22), closed along the top of the frame.
    var b = data.boundary.filter(function (q) { return q[0] > 0; });
    var line = b.map(function (q, i) { return (i ? 'L' : 'M') + sx(q[0]).toFixed(1) + ' ' + sy(q[1]).toFixed(1); }).join('');
    el('path', { class: 'rm-feasible', d: 'M' + sx(Math.pow(10, X[0])) + ' ' + sy(b[0][1]) + line.replace(/^M/, 'L') + 'L' + sx(b[b.length - 1][0]) + ' ' + M.t + 'L' + sx(Math.pow(10, X[0])) + ' ' + M.t + 'Z' }, plot);
    // Aspect-ratio isolines: P~ U~ = Ry (Eq. 12), straight lines of slope -1 in log-log.
    var lastLabel = null;
    data.ar_isolines.slice().reverse().forEach(function (iso) {
      var u0 = Math.pow(10, X[0]), u1 = Math.pow(10, X[1]);
      el('line', { class: 'rm-iso', x1: sx(u0), y1: sy(iso.Ry / u0), x2: sx(u1), y2: sy(iso.Ry / u1) }, plot);
      // Label where the isoline meets the bottom of the frame, in the empty region below R = R_.
      var pBot = Math.pow(10, Y[0]) * 1.06, ux = Math.min(iso.Ry / pBot, u1 / 1.04);
      // Skip a label that would collide with the one to its right (narrow screens).
      var lx = sx(ux), ly = sy(iso.Ry / ux);
      if (lastLabel && Math.abs(lastLabel[0] - lx) < 52 && Math.abs(lastLabel[1] - ly) < 14) return;
      lastLabel = [lx, ly];
      var t = el('text', { class: 'rm-iso-label', x: sx(ux) - 4, y: sy(iso.Ry / ux) - 5, 'text-anchor': 'end' }, plot);
      t.appendChild(document.createTextNode('A'));
      el('tspan', { 'baseline-shift': 'sub', 'font-size': '75%' }, t).textContent = 'r';
      t.appendChild(document.createTextNode(' = ' + iso.Ar));
    });
    el('path', { class: 'rm-boundary', d: line }, plot);
    // Axes.
    var g = el('g', { class: 'rm-axes' });
    for (var e = -1; e <= 1; e++) {
      el('line', { class: 'rm-grid', x1: sx(Math.pow(10, e)), x2: sx(Math.pow(10, e)), y1: M.t, y2: H - M.b }, g);
      var tx = el('text', { class: 'rm-tick', x: sx(Math.pow(10, e)), y: H - M.b + 18, 'text-anchor': 'middle' }, g);
      tx.appendChild(document.createTextNode('10')); el('tspan', { 'baseline-shift': 'super', 'font-size': '9' }, tx).textContent = e;
    }
    [2, 5, 10, 20].forEach(function (p) {
      el('line', { class: 'rm-grid', x1: M.l, x2: W - M.r, y1: sy(p), y2: sy(p) }, g);
      el('text', { class: 'rm-tick', x: M.l - 8, y: sy(p) + 4, 'text-anchor': 'end' }, g).textContent = p;
    });
    el('rect', { class: 'rm-frame', x: M.l, y: M.t, width: W - M.l - M.r, height: H - M.t - M.b }, g);
    sub(el('text', { class: 'rm-label', x: (W + M.l - M.r) / 2, y: H - 8, 'text-anchor': 'middle' }, g), root.dataset.xlabel);
    sub(el('text', { class: 'rm-label', 'text-anchor': 'middle', transform: 'translate(14 ' + ((H - M.b + M.t) / 2) + ') rotate(-90)' }, g), root.dataset.ylabel);
    var bl = b[Math.round(b.length * 0.5)];
    el('text', { class: 'rm-boundary-label', x: sx(bl[0]) + 8, y: sy(bl[1]) + 4 }, plot).textContent = 'R = R\u0304';
    // Points: circles for SLM, diamonds for LMD, coloured by alloy family.
    var gp = el('g', {}, plot);
    data.points.forEach(function (p, i) {
      var x = sx(p.U_t), y = sy(p.P_t), n;
      // Marker per process: SLM circle, LMD diamond, arc welding triangle, beam welding square.
      if (p.process === 'SLM') n = el('circle', { cx: x, cy: y, r: 3.6 }, gp);
      else if (p.process === 'LMD') n = el('path', { d: 'M' + x + ' ' + (y - 4.6) + 'l4.6 4.6l-4.6 4.6l-4.6 -4.6z' }, gp);
      else if (p.process === 'AW') n = el('path', { d: 'M' + x + ' ' + (y - 4.8) + 'l4.4 7.8h-8.8z' }, gp);
      else n = el('path', { d: 'M' + (x - 3.4) + ' ' + (y - 3.4) + 'h6.8v6.8h-6.8z' }, gp);
      n.setAttribute('class', 'rm-pt');
      n.style.fill = COLOURS[p.family];
      n.addEventListener('pointerenter', function () { hover(i, x, y); });
      n.addEventListener('pointerleave', function () { tip.hidden = true; });
      n.addEventListener('click', function () { choose(i); });
      nodes[i] = n;
    });
    filter();
  }

  function hover(i, x, y) {
    var p = data.points[i], s = svg.getBoundingClientRect().width / W;
    tip.textContent = p.material + ' · ' + p.process_label + ' · ' + p.author + (p.year ? ' ' + p.year : '');
    tip.style.left = (x * s) + 'px'; tip.style.top = (y * s) + 'px'; tip.hidden = false;
  }

  function filter() {
    visible = [];
    data.points.forEach(function (p, i) {
      var on = families[p.family] && processes[p.process];
      nodes[i].classList.toggle('rm-off', !on);
      if (on) visible.push(i);
    });
    visible.sort(function (a, b) { return data.points[a].U_t - data.points[b].U_t; });
    if (visible.length && visible.indexOf(current) < 0) current = visible[Math.floor(visible.length / 2)];
    select();
  }

  function choose(i) { current = i; select(); }

  function drawPool(p) {
    pool.textContent = '';
    // Outline normalised by the half-width R; front tip to the right, as the source moves along +x.
    var pts = p.outline, x0 = pts[pts.length - 1][0], x1 = pts[0][0], len = x1 - x0;
    var scale = Math.min(250 / len, 42), cx = 140 - (x0 + x1) / 2 * scale, cy = 75;
    var top = pts.map(function (q, i) { return (i ? 'L' : 'M') + (cx + q[0] * scale).toFixed(1) + ' ' + (cy - q[1] * scale).toFixed(1); }).join('');
    var bottom = pts.slice().reverse().map(function (q) { return 'L' + (cx + q[0] * scale).toFixed(1) + ' ' + (cy + q[1] * scale).toFixed(1); }).join('');
    var nsPool = function (name, attrs) { return el(name, attrs, pool); };
    nsPool('line', { class: 'rm-pool-axis', x1: 8, x2: 272, y1: cy, y2: cy });
    nsPool('path', { class: 'rm-pool-shape', d: top + bottom + 'Z', style: 'fill:' + COLOURS[p.family] });
    // Heat source at the origin of Eq. (1) and its direction of motion.
    nsPool('circle', { class: 'rm-pool-source', cx: cx, cy: cy, r: 3 });
    nsPool('path', { class: 'rm-pool-arrow', d: 'M' + (cx + x1 * scale + 8) + ' ' + cy + 'h18m-5 -4l5 4l-5 4' });
    // Width 2R and length L markers.
    nsPool('path', { class: 'rm-pool-dim', d: 'M' + (cx + x0 * scale) + ' ' + (cy + scale + 10) + 'H' + (cx + x1 * scale) });
    var t = nsPool('text', { class: 'rm-pool-text', x: cx + (x0 + x1) / 2 * scale, y: cy + scale + 24, 'text-anchor': 'middle' });
    t.textContent = 'L = ' + fmt(p.Ar * 2, 3) + ' R';
  }

  function select() {
    root.querySelectorAll('.rm-pt.rm-sel').forEach(function (n) { n.classList.remove('rm-sel'); });
    var p = data.points[current];
    if (!p) return;
    nodes[current].classList.add('rm-sel');
    nodes[current].parentNode.appendChild(nodes[current]);
    drawPool(p);
    root.querySelector('[data-rm-material]').textContent = p.material;
    root.querySelector('[data-rm-process-out]').textContent = p.process_label;
    root.querySelector('[data-rm-up]').textContent = fmt(p.U, 3) + ' m/s · ' + fmt(p.P, 3) + ' W';
    root.querySelector('[data-rm-rbar]').textContent = fmt(p.R_bar_um, 3) + ' µm';
    root.querySelector('[data-rm-ry]').textContent = fmt(p.Ry, 3);
    root.querySelector('[data-rm-ar]').textContent = p.Ar.toFixed(2);
    var a = root.querySelector('[data-rm-source]');
    a.textContent = p.author + (p.year ? ' (' + p.year + ')' : '');
    if (p.doi) a.href = 'https://doi.org/' + p.doi; else a.removeAttribute('href');
    svg.setAttribute('aria-label', root.dataset.label.replace('%n', visible.length).replace('%m', p.material).replace('%p', p.process_label).replace('%a', p.Ar.toFixed(2)));
  }

  fetch(root.dataset.src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (json) {
    data = json;
    var prov = root.querySelector('[data-rm-provenance]');
    prov.innerHTML = prov.dataset.template.replace('%n', data.points.length);
    root.querySelectorAll('[data-rm-family]').forEach(function (b) {
      families[b.dataset.rmFamily] = true;
      b.querySelector('i').style.background = COLOURS[b.dataset.rmFamily];
      b.addEventListener('click', function () {
        var key = b.dataset.rmFamily, on = !families[key];
        // Never hide every family: the last active chip stays on.
        if (!on && Object.keys(families).filter(function (k) { return families[k]; }).length === 1) return;
        families[key] = on; b.setAttribute('aria-pressed', String(on)); filter();
      });
    });
    root.querySelectorAll('[data-rm-process]').forEach(function (b) {
      processes[b.dataset.rmProcess] = true;
      b.addEventListener('click', function () {
        var key = b.dataset.rmProcess, on = !processes[key];
        // Never hide every process: the last active chip stays on.
        if (!on && Object.keys(processes).filter(function (k) { return processes[k]; }).length === 1) return;
        processes[key] = on; b.setAttribute('aria-pressed', String(on)); filter();
      });
    });
    // Start on a laser-melted Inconel 718 point near the middle of its cloud, when available.
    var start = data.points.map(function (p, i) { return [p, i]; }).filter(function (q) { return q[0].material === 'Inconel 718' && q[0].process === 'SLM'; });
    if (start.length) { start.sort(function (a, b) { return a[0].Ry - b[0].Ry; }); current = start[Math.floor(start.length / 2)][1]; }
    svg.addEventListener('keydown', function (e) {
      var step = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1 }[e.key];
      if (!step || !visible.length) return;
      e.preventDefault();
      var k = visible.indexOf(current);
      current = visible[Math.max(0, Math.min(visible.length - 1, k + step))]; select();
    });
    root.querySelector('[data-rm-controls]').hidden = false;
    draw();
    var pending, lastW = W;
    window.addEventListener('resize', function () {
      clearTimeout(pending);
      pending = setTimeout(function () { if (Math.round(root.querySelector('.rm-stage').clientWidth) !== lastW) { draw(); lastW = W; } }, 150);
    });
    root.classList.add('is-ready');
  }).catch(function () { root.querySelector('[data-rm-error]').hidden = false; });
})();
