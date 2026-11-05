// FIG. R02.2: multiaxial fatigue criteria x materials, drawn from multifat-pipeline outputs
// (assets/data/figures/multifat-comparison.json). No criterion is evaluated in the browser.
(function () {
  'use strict';
  var root = document.querySelector('[data-multifat-comparison]');
  if (!root) return;
  var svg = root.querySelector('svg');
  var NS = 'http://www.w3.org/2000/svg';
  // Sequential map of FIG. T01; diverging map: amber (non-conservative) - navy - teal (conservative).
  var STOPS = [[15, 47, 79], [29, 95, 134], [46, 154, 160], [130, 226, 222], [242, 251, 250]];
  var DIVERGE = [[231, 178, 95], [118, 104, 92], [29, 62, 92], [56, 140, 150], [130, 226, 222]];
  var BIAS = 0.25; // colour saturates at |e_L| = 0.25 (about 28 % of the load)
  var FAMILY_KEY = { cp_methods: 'famCp', invariant_methods: 'famInvariant', integral_methods: 'famIntegral', energy_based_methods: 'famEnergy' };
  var data, lookup = {}, view = 'within', sel = [0, 0], rects = [], layout = null;

  function node(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n);
    return n;
  }
  function ramp(stops, u) {
    var x = Math.max(0, Math.min(1, u)) * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(x)), f = x - i;
    return 'rgb(' + [0, 1, 2].map(function (c) { return Math.round(stops[i][c] + (stops[i + 1][c] - stops[i][c]) * f); }).join(',') + ')';
  }
  function fill(cell) {
    if (!cell) return null;
    if (view === 'within') return cell.within10 == null ? null : ramp(STOPS, cell.within10);
    return cell.mean == null ? null : ramp(DIVERGE, 0.5 + cell.mean / (2 * BIAS));
  }
  function pct(x) { return x == null ? '–' : Math.round(x * 100) + ' %'; }
  function signed(x) { return (x >= 0 ? '+' : '−') + Math.abs(x).toFixed(3); }
  function pretty(id) { return id.replace(/_/g, ' '); }

  // Rows: methods with a family header before each group; columns: materials.
  function build() {
    var width = Math.max(300, Math.round(root.querySelector('.mc-stage').clientWidth));
    var labelW = 86, headH = 74, rowH = 15, famH = 20;
    var cellW = Math.min(78, (width - labelW - 8) / data.materials.length);
    var rows = [], y = headH, family = null;
    data.methods.forEach(function (m) {
      if (m.family !== family) { family = m.family; rows.push({ family: family, y: y }); y += famH; }
      rows.push({ method: m, y: y }); y += rowH;
    });
    layout = { width: width, labelW: labelW, headH: headH, rowH: rowH, cellW: cellW, rows: rows, height: y + 4 };
    svg.textContent = ''; rects = [];
    svg.setAttribute('viewBox', '0 0 ' + width + ' ' + layout.height);
    data.materials.forEach(function (mat, j) {
      var x = labelW + (j + 0.5) * cellW;
      node('text', { class: 'mc-col', x: x, y: headH - 8, transform: 'rotate(-45 ' + x + ' ' + (headH - 8) + ')' }).textContent = pretty(mat.id);
    });
    var i = 0;
    rows.forEach(function (row) {
      if (row.family) {
        node('text', { class: 'mc-fam', x: 0, y: row.y + 14 }).textContent = root.dataset[FAMILY_KEY[row.family]] || row.family;
        node('line', { class: 'mc-rule', x1: 0, x2: labelW + cellW * data.materials.length, y1: row.y + 18.5, y2: row.y + 18.5 });
        return;
      }
      row.index = i;
      node('text', { class: 'mc-row', x: labelW - 8, y: row.y + rowH - 4 }).textContent = row.method.id;
      rects[i] = data.materials.map(function (mat, j) {
        var cell = lookup[row.method.id + '|' + mat.id];
        var r = node('rect', { x: labelW + j * cellW + 1, y: row.y + 1, width: cellW - 2, height: rowH - 2, class: cell ? 'mc-cell' : 'mc-cell mc-missing' });
        r.addEventListener('pointerenter', function () { choose(row.index, j); });
        r.addEventListener('click', function () { choose(row.index, j); });
        return r;
      });
      i++;
    });
    layout.marker = node('rect', { class: 'mc-marker', width: cellW, height: rowH, rx: 1 });
    paint(); choose(sel[0], sel[1]);
  }

  function paint() {
    data.methods.forEach(function (m, i) {
      data.materials.forEach(function (mat, j) {
        var colour = fill(lookup[m.id + '|' + mat.id]);
        rects[i][j].style.fill = colour || '';
        rects[i][j].classList.toggle('mc-missing', !colour);
      });
    });
    var stops = view === 'within' ? STOPS : DIVERGE;
    root.querySelector('[data-mc-ramp]').style.background = 'linear-gradient(90deg,' + [0, .25, .5, .75, 1].map(function (u) { return ramp(stops, u); }).join(',') + ')';
    root.querySelector('[data-mc-ticks]').innerHTML = view === 'within' ? '<span>0</span><span>50 %</span><span>100 %</span>'
      : '<span>−' + BIAS + '</span><span>0</span><span>+' + BIAS + '</span>';
    var legend = root.querySelector('[data-mc-legend]');
    legend.innerHTML = legend.dataset[view].replace('e_L', 'e<sub>L</sub>');
    root.querySelectorAll('[data-mc-view]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.mcView === view)); });
    svg.setAttribute('aria-label', root.dataset.label.replace('%m', data.methods.length).replace('%n', data.materials.length)
      .replace('%v', (view === 'within' ? root.dataset.viewWithin : root.dataset.viewBias).toLowerCase()));
  }

  function choose(i, j) {
    sel = [Math.max(0, Math.min(data.methods.length - 1, i)), Math.max(0, Math.min(data.materials.length - 1, j))];
    var m = data.methods[sel[0]], mat = data.materials[sel[1]], cell = lookup[m.id + '|' + mat.id];
    var r = rects[sel[0]][sel[1]];
    layout.marker.setAttribute('x', Number(r.getAttribute('x')) - 1); layout.marker.setAttribute('y', Number(r.getAttribute('y')) - 1);
    var link = root.querySelector('[data-mc-method]');
    link.textContent = m.id; link.title = m.citation;
    if (m.url) link.href = m.url; else link.removeAttribute('href');
    root.querySelector('[data-mc-family]').textContent = ' · ' + (root.dataset[FAMILY_KEY[m.family]] || m.family);
    root.querySelector('[data-mc-material]').textContent = pretty(mat.id);
    root.querySelector('[data-mc-n]').textContent = cell ? cell.n : '–';
    root.querySelector('[data-mc-w10]').textContent = cell ? pct(cell.within10) : '–';
    root.querySelector('[data-mc-w20]').textContent = cell ? pct(cell.within20) : '–';
    root.querySelector('[data-mc-mean]').textContent = cell && cell.mean != null ? signed(cell.mean) + (cell.sd != null ? ' ± ' + cell.sd.toFixed(3) : '') : '–';
  }

  fetch(root.dataset.src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (json) {
    data = json;
    data.cells.forEach(function (c) { lookup[c.method + '|' + c.material] = c; });
    // Start on Findley for the material with most assessment tests, when available.
    var start = data.methods.map(function (m) { return m.id; }).indexOf('FIN');
    sel = [Math.max(0, start), 0];
    root.querySelectorAll('[data-mc-view]').forEach(function (b) { b.addEventListener('click', function () { view = b.dataset.mcView; paint(); }); });
    svg.addEventListener('keydown', function (e) {
      var move = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
      if (!move) return;
      e.preventDefault(); choose(sel[0] + move[0], sel[1] + move[1]);
    });
    root.querySelector('[data-mc-controls]').hidden = false;
    build();
    var pending, lastWidth = layout.width;
    window.addEventListener('resize', function () {
      clearTimeout(pending);
      pending = setTimeout(function () { if (Math.round(root.querySelector('.mc-stage').clientWidth) !== lastWidth) { build(); lastWidth = layout.width; } }, 150);
    });
    root.classList.add('is-ready');
  }).catch(function () { root.querySelector('[data-mc-error]').hidden = false; });
})();
