// FIG. R04: SeAn-CP candidate-plane paths on the FS_ext damage sphere.
// Draws values precomputed by seancp (assets/data/figures/seancp-paths-fs-ext.json);
// no fatigue criterion is evaluated in the browser.
(function () {
  'use strict';
  var root = document.querySelector('[data-seancp-sphere]');
  if (!root) return;
  var canvas = root.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var toggle = root.querySelector('[data-sc-toggle]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Same sequential map as FIG. R02; path colours stay distinct from its bright end.
  var STOPS = [[15, 47, 79], [29, 95, 134], [46, 154, 160], [130, 226, 222], [242, 251, 250]];
  var PATH_COLOURS = ['#e7b25f', '#f08a6c', '#c3a6ff'];

  var data, nT, nP, step, field, current = 0;
  var az = 0.95, el = 0.38, spinning = !reduce, dragging = false, last = null;
  var size = 0, dpr = 1, image = null, raf = 0, visible = true, draw0 = 0, progress = 1;

  function colour(u) {
    var x = Math.max(0, Math.min(1, u)) * (STOPS.length - 1), i = Math.min(STOPS.length - 2, Math.floor(x)), f = x - i;
    return [0, 1, 2].map(function (c) { return STOPS[i][c] + (STOPS[i + 1][c] - STOPS[i][c]) * f; });
  }

  function caseField(index) {
    var n = nT * nP, out = new Float32Array(n);
    for (var i = 0; i < n; i++) out[i] = data.values[index * n + i] / 255;
    return out;
  }

  // Camera basis from azimuth/elevation; world z points up on screen.
  function basis() {
    var ce = Math.cos(el), f = [ce * Math.cos(az), ce * Math.sin(az), Math.sin(el)];
    var r = [-Math.sin(az), Math.cos(az), 0];
    var u = [f[1] * r[2] - f[2] * r[1], f[2] * r[0] - f[0] * r[2], f[0] * r[1] - f[1] * r[0]];
    return { r: r, u: u, f: f };
  }
  function project(b, v) {
    return [v[0] * b.r[0] + v[1] * b.r[1] + v[2] * b.r[2], v[0] * b.u[0] + v[1] * b.u[1] + v[2] * b.u[2], v[0] * b.f[0] + v[1] * b.f[1] + v[2] * b.f[2]];
  }

  // Bilinear lookup on the hemisphere grid; n and -n are the same plane.
  function sample(values, n) {
    var x = n[0], y = n[1], z = n[2];
    if (z < 0) { x = -x; y = -y; z = -z; }
    var t = Math.acos(Math.min(1, z)) * 180 / Math.PI / step;
    var p = (Math.atan2(y, x) * 180 / Math.PI + 360) % 360 / step;
    var t0 = Math.min(nT - 2, Math.floor(t)), ft = Math.min(1, t - t0);
    var p0 = Math.floor(p) % nP, p1 = (p0 + 1) % nP, fp = p - Math.floor(p);
    var a = values[t0 * nP + p0], b = values[t0 * nP + p1], c = values[(t0 + 1) * nP + p0], d = values[(t0 + 1) * nP + p1];
    return (a * (1 - fp) + b * fp) * (1 - ft) + (c * (1 - fp) + d * fp) * ft;
  }

  function resize() {
    var w = Math.min(root.querySelector('.sc-stage').clientWidth, 460);
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    size = Math.round(w * dpr);
    canvas.width = canvas.height = size;
    canvas.style.width = canvas.style.height = w + 'px';
    image = ctx.createImageData(size, size);
  }

  // Front-facing point of a plane: n or -n, whichever faces the viewer.
  function front(b, n) { var p = project(b, n); return p[2] >= 0 ? p : [-p[0], -p[1], -p[2]]; }

  function draw() {
    var b = basis(), px = image.data, R = size * 0.46, cx = size / 2, cy = size / 2;
    for (var j = 0; j < size; j++) {
      for (var i = 0; i < size; i++) {
        var o = (j * size + i) * 4, sx = (i - cx) / R, sy = (cy - j) / R, rr = sx * sx + sy * sy;
        if (rr > 1) { px[o + 3] = 0; continue; }
        var sz = Math.sqrt(1 - rr);
        var n = [sx * b.r[0] + sy * b.u[0] + sz * b.f[0], sx * b.r[1] + sy * b.u[1] + sz * b.f[1], sx * b.r[2] + sy * b.u[2] + sz * b.f[2]];
        var c = colour(sample(field, n)), shade = 0.62 + 0.38 * sz;
        px[o] = c[0] * shade; px[o + 1] = c[1] * shade; px[o + 2] = c[2] * shade;
        px[o + 3] = rr > 0.985 ? 255 * (1 - rr) / 0.015 : 255;
      }
    }
    ctx.clearRect(0, 0, size, size);
    ctx.putImageData(image, 0, 0);
    ctx.lineCap = 'round';

    // Each SeAn-CP family is half a great circle of normals; its antipodes close the circle.
    // Coinciding families are one circle drawn with alternating dashes of the three colours.
    var shared = data.cases[current].paths_coincide;
    data.cases[current].paths.forEach(function (path, k) {
      var count = Math.max(2, Math.round(path.normals.length * progress));
      ctx.strokeStyle = PATH_COLOURS[k]; ctx.lineWidth = 2.4 * dpr;
      ctx.setLineDash(shared ? [8 * dpr, 16 * dpr] : []);
      ctx.lineDashOffset = shared ? -k * 8 * dpr : 0;
      [1, -1].forEach(function (sign) {
        ctx.beginPath(); var pen = false;
        for (var i = 0; i < count; i++) {
          var p = project(b, path.normals[i].map(function (v) { return v * sign; }));
          if (p[2] < 0) { pen = false; continue; }
          var x = cx + p[0] * R, y = cy - p[1] * R;
          if (pen) ctx.lineTo(x, y); else ctx.moveTo(x, y);
          pen = true;
        }
        ctx.stroke();
      });
    });

    ctx.setLineDash([]); ctx.lineDashOffset = 0;
    // Reference maximum (white ring) and SeAn-CP restricted maximum (amber dot).
    var c = data.cases[current], ref = front(b, c.reference_normal), sea = front(b, c.seancp_normal);
    ctx.lineWidth = 2 * dpr; ctx.strokeStyle = '#ffffff';
    ctx.beginPath(); ctx.arc(cx + ref[0] * R, cy - ref[1] * R, 7 * dpr, 0, 2 * Math.PI); ctx.stroke();
    ctx.fillStyle = '#e7b25f'; ctx.strokeStyle = '#0e2a49'; ctx.lineWidth = 1.5 * dpr;
    ctx.beginPath(); ctx.arc(cx + sea[0] * R, cy - sea[1] * R, 4 * dpr, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();

    ctx.font = (12 * dpr) + 'px "JetBrains Mono Variable", ui-monospace, monospace';
    [['x', [1, 0, 0]], ['y', [0, 1, 0]], ['z', [0, 0, 1]]].forEach(function (axis) {
      var p = project(b, axis[1]);
      ctx.fillStyle = p[2] >= 0 ? 'rgba(236,245,247,.9)' : 'rgba(236,245,247,.35)';
      ctx.fillText(axis[0], cx + p[0] * R * 1.08 - 4 * dpr, cy - p[1] * R * 1.08 + 4 * dpr);
    });
  }

  function fmt(x) { return x.toExponential(3).replace('e-', ' × 10⁻').replace(/⁻(\d)/, function (m, d) { return '⁻' + '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]; }); }

  function describe() {
    var c = data.cases[current];
    root.querySelector('[data-sc-ref]').textContent = fmt(c.fs_reference);
    root.querySelector('[data-sc-sea]').textContent = fmt(c.fs_seancp);
    root.querySelector('[data-sc-fam]').textContent = c.paths_coincide ? root.dataset.coincide : root.dataset.distinct;
    root.querySelector('[data-sc-err]').textContent = (c.error_percent > -0.0005 ? '0.00' : c.error_percent.toFixed(2)) + ' %';
    root.querySelectorAll('[data-sc-case]').forEach(function (btn) { btn.setAttribute('aria-pressed', String(Number(btn.dataset.scCase) === current)); });
    canvas.setAttribute('aria-label', root.dataset.labelTemplate.replace('%c', root.querySelector('[data-sc-case="' + current + '"]').textContent).replace('%e', c.error_percent.toFixed(2)));
  }

  function select(index) {
    current = index; field = caseField(index); describe();
    if (reduce) { progress = 1; draw(); return; }
    progress = 0; draw0 = performance.now(); loop();
  }

  function loop() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function frame(now) {
      var busy = false;
      if (progress < 1) { progress = Math.min(1, (now - draw0) / 700); busy = true; }
      if (spinning && !dragging && visible) { az += 0.0035; busy = true; }
      draw();
      if (busy) raf = requestAnimationFrame(frame);
    });
  }

  function setSpin(on) {
    spinning = on;
    toggle.textContent = on ? toggle.dataset.pause : toggle.dataset.play;
    toggle.setAttribute('aria-pressed', String(on));
    if (on) loop();
  }

  function start(json) {
    data = json; nT = data.grid.n_theta; nP = data.grid.n_phi; step = data.grid.step_deg;
    var bin = atob(data.values_uint8_base64); data.values = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) data.values[i] = bin.charCodeAt(i);
    resize();
    root.querySelector('[data-sc-controls]').hidden = false;
    root.querySelectorAll('[data-sc-case]').forEach(function (btn) { btn.addEventListener('click', function () { select(Number(btn.dataset.scCase)); }); });
    select(Number(root.dataset.initialCase || 0));
    root.classList.add('is-ready');
    if (reduce) { toggle.hidden = true; spinning = false; } else setSpin(true);
    toggle.addEventListener('click', function () { setSpin(!spinning); });
    canvas.addEventListener('pointerdown', function (e) { dragging = true; last = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); if (spinning) setSpin(false); });
    canvas.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      az -= (e.clientX - last[0]) * 0.01; el = Math.max(-1.45, Math.min(1.45, el + (e.clientY - last[1]) * 0.01));
      last = [e.clientX, e.clientY]; draw();
    });
    canvas.addEventListener('pointerup', function () { dragging = false; });
    canvas.addEventListener('keydown', function (e) {
      var moves = { ArrowLeft: [0.12, 0], ArrowRight: [-0.12, 0], ArrowUp: [0, -0.12], ArrowDown: [0, 0.12] }[e.key];
      if (!moves) return;
      e.preventDefault(); if (spinning) setSpin(false);
      az += moves[0]; el = Math.max(-1.45, Math.min(1.45, el + moves[1])); draw();
    });
    window.addEventListener('resize', function () { resize(); draw(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible && spinning) loop(); }).observe(canvas);
    }
  }

  fetch(root.dataset.src).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(start).catch(function () {
    root.querySelector('[data-sc-error]').hidden = false;
  });
})();
