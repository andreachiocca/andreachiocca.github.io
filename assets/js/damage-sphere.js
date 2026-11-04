// FIG. R02: Findley damage parameter on the sphere of plane normals.
// Draws values precomputed by multifat (assets/data/figures/damage-sphere-findley.json);
// no fatigue criterion is evaluated in the browser.
(function () {
  'use strict';
  var root = document.querySelector('[data-damage-sphere]');
  if (!root) return;
  var canvas = root.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var lambdaInput = root.querySelector('[data-ds-lambda]');
  var phaseInput = root.querySelector('[data-ds-phase]');
  var lambdaOut = root.querySelector('[data-ds-lambda-out]');
  var phaseOut = root.querySelector('[data-ds-phase-out]');
  var maxOut = root.querySelector('[data-ds-max]');
  var normalOut = root.querySelector('[data-ds-normal]');
  var hoverOut = root.querySelector('[data-ds-hover]');
  var toggle = root.querySelector('[data-ds-toggle]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Sequential map on the navy panel: low damage dark, high damage bright teal-white.
  var STOPS = [[15, 47, 79], [29, 95, 134], [46, 154, 160], [130, 226, 222], [242, 251, 250]];
  var AMBER = [231, 178, 95];
  var HIGHLIGHT = 0.985; // planes within 1.5 % of the maximum are shown as critical

  var data, nT, nP, step, scale, field, target, from, tween = 1, tweenStart = 0;
  var az = 0.85, el = 0.42, spinning = !reduce, dragging = false, last = null, hover = null;
  var size = 0, dpr = 1, image = null, raf = 0, visible = true;

  function colour(u) {
    var x = Math.max(0, Math.min(1, u)) * (STOPS.length - 1), i = Math.min(STOPS.length - 2, Math.floor(x)), f = x - i;
    return [0, 1, 2].map(function (c) { return STOPS[i][c] + (STOPS[i + 1][c] - STOPS[i][c]) * f; });
  }

  function caseIndex() { return Number(lambdaInput.value) * data.phases_deg.length + Number(phaseInput.value); }

  function caseField(index) {
    var n = nT * nP, out = new Float32Array(n);
    for (var i = 0; i < n; i++) out[i] = data.values[index * n + i] / 255 * scale;
    return out;
  }

  // Camera basis from azimuth/elevation; world z points up on screen.
  function basis() {
    var ce = Math.cos(el), f = [ce * Math.cos(az), ce * Math.sin(az), Math.sin(el)];
    var r = [-Math.sin(az), Math.cos(az), 0];
    var u = [f[1] * r[2] - f[2] * r[1], f[2] * r[0] - f[0] * r[2], f[0] * r[1] - f[1] * r[0]];
    return { r: r, u: u, f: f };
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
    var w = Math.min(root.querySelector('.ds-stage').clientWidth, 460);
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    size = Math.round(w * dpr);
    canvas.width = canvas.height = size;
    canvas.style.width = canvas.style.height = w + 'px';
    image = ctx.createImageData(size, size);
  }

  function project(b, v) { return [v[0] * b.r[0] + v[1] * b.r[1] + v[2] * b.r[2], v[0] * b.u[0] + v[1] * b.u[1] + v[2] * b.u[2], v[0] * b.f[0] + v[1] * b.f[1] + v[2] * b.f[2]]; }

  function draw() {
    var b = basis(), px = image.data, R = size * 0.46, cx = size / 2, cy = size / 2;
    var caseMax = data.cases[caseIndex()].dp_max;
    for (var j = 0; j < size; j++) {
      for (var i = 0; i < size; i++) {
        var o = (j * size + i) * 4, sx = (i - cx) / R, sy = (cy - j) / R, rr = sx * sx + sy * sy;
        if (rr > 1) { px[o + 3] = 0; continue; }
        var sz = Math.sqrt(1 - rr);
        var n = [sx * b.r[0] + sy * b.u[0] + sz * b.f[0], sx * b.r[1] + sy * b.u[1] + sz * b.f[1], sx * b.r[2] + sy * b.u[2] + sz * b.f[2]];
        var v = sample(field, n), c = colour(v / scale), shade = 0.62 + 0.38 * sz;
        if (v >= HIGHLIGHT * caseMax) c = [c[0] * 0.25 + AMBER[0] * 0.75, c[1] * 0.25 + AMBER[1] * 0.75, c[2] * 0.25 + AMBER[2] * 0.75];
        px[o] = c[0] * shade; px[o + 1] = c[1] * shade; px[o + 2] = c[2] * shade;
        px[o + 3] = rr > 0.985 ? 255 * (1 - rr) / 0.015 : 255; // soft rim
      }
    }
    ctx.clearRect(0, 0, size, size);
    ctx.putImageData(image, 0, 0);

    // Global axes and the representative critical normal.
    ctx.lineWidth = 1.2 * dpr;
    ctx.font = (12 * dpr) + 'px "JetBrains Mono Variable", ui-monospace, monospace';
    [['x', [1, 0, 0]], ['y', [0, 1, 0]], ['z', [0, 0, 1]]].forEach(function (axis) {
      var p = project(b, axis[1]), front = p[2] >= 0;
      ctx.strokeStyle = front ? 'rgba(236,245,247,.85)' : 'rgba(236,245,247,.3)';
      ctx.setLineDash(front ? [] : [3 * dpr, 3 * dpr]);
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + p[0] * R * 1.08, cy - p[1] * R * 1.08); ctx.stroke();
      ctx.fillStyle = ctx.strokeStyle;
      ctx.fillText(axis[0], cx + p[0] * R * 1.14 - 4 * dpr, cy - p[1] * R * 1.14 + 4 * dpr);
    });
    ctx.setLineDash([]);
    var nStar = data.cases[caseIndex()].critical_normal, q = project(b, nStar);
    if (q[2] < 0) q = [-q[0], -q[1], -q[2]];
    ctx.strokeStyle = 'rgb(' + AMBER.join(',') + ')'; ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = 2.2 * dpr;
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + q[0] * R, cy - q[1] * R); ctx.stroke();
    ctx.beginPath(); ctx.arc(cx + q[0] * R, cy - q[1] * R, 3.5 * dpr, 0, 2 * Math.PI); ctx.fill();
    ctx.fillText('n*', cx + q[0] * R + 6 * dpr, cy - q[1] * R - 6 * dpr);
  }

  function fmt(x, d) { return (Math.round(x * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d); }

  function describe() {
    var k = caseIndex(), c = data.cases[k], n = c.critical_normal;
    var theta = Math.acos(Math.abs(n[2])) * 180 / Math.PI, phi = (Math.atan2(n[2] < 0 ? -n[1] : n[1], n[2] < 0 ? -n[0] : n[0]) * 180 / Math.PI + 360) % 360;
    lambdaOut.textContent = fmt(c.lambda, 2);
    phaseOut.textContent = c.dphi_deg + '°';
    maxOut.textContent = fmt(c.dp_max, 3);
    normalOut.textContent = 'θ = ' + fmt(theta, 0) + '°, φ = ' + fmt(phi, 0) + '°';
    canvas.setAttribute('aria-label', root.dataset.labelTemplate.replace('%l', fmt(c.lambda, 2)).replace('%p', c.dphi_deg).replace('%d', fmt(c.dp_max, 3)));
  }

  function setCase() {
    var next = caseField(caseIndex());
    describe();
    if (reduce || !field) { field = next; draw(); return; }
    from = field; target = next; tween = 0; tweenStart = performance.now();
    loop();
  }

  function loop() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function frame(now) {
      var busy = false;
      if (tween < 1) {
        tween = Math.min(1, (now - tweenStart) / 320);
        var e = 1 - Math.pow(1 - tween, 3), mixed = new Float32Array(target.length);
        for (var i = 0; i < target.length; i++) mixed[i] = from[i] + (target[i] - from[i]) * e;
        field = tween === 1 ? target : mixed; busy = true;
      }
      if (spinning && !dragging && visible) { az += 0.0035; busy = true; }
      draw(); updateHover();
      if (busy) raf = requestAnimationFrame(frame);
    });
  }

  function setSpin(on) {
    spinning = on;
    toggle.textContent = on ? toggle.dataset.pause : toggle.dataset.play;
    toggle.setAttribute('aria-pressed', String(on));
    if (on) loop();
  }

  function pointer(event) {
    var rect = canvas.getBoundingClientRect(), R = rect.width * 0.46;
    return [(event.clientX - rect.left - rect.width / 2) / R, (rect.top + rect.height / 2 - event.clientY) / R];
  }

  function updateHover() {
    if (!hover) { hoverOut.textContent = hoverOut.dataset.empty; return; }
    var rr = hover[0] * hover[0] + hover[1] * hover[1];
    if (rr > 1) { hoverOut.textContent = hoverOut.dataset.empty; return; }
    var b = basis(), sz = Math.sqrt(1 - rr);
    var n = [0, 1, 2].map(function (c) { return hover[0] * b.r[c] + hover[1] * b.u[c] + sz * b.f[c]; });
    hoverOut.textContent = 'DP/σa ≈ ' + fmt(sample(field, n), 2);
  }

  function start(json) {
    data = json; nT = data.grid.n_theta; nP = data.grid.n_phi; step = data.grid.step_deg; scale = data.value_scale_max;
    var bin = atob(data.values_uint8_base64); data.values = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) data.values[i] = bin.charCodeAt(i);
    lambdaInput.max = data.lambdas.length - 1; phaseInput.max = data.phases_deg.length - 1;
    resize(); field = caseField(caseIndex()); describe(); draw();
    root.classList.add('is-ready');
    root.querySelector('[data-ds-controls]').hidden = false;
    if (reduce) { toggle.hidden = true; spinning = false; } else setSpin(true);

    lambdaInput.addEventListener('input', setCase);
    phaseInput.addEventListener('input', setCase);
    toggle.addEventListener('click', function () { setSpin(!spinning); });
    canvas.addEventListener('pointerdown', function (e) { dragging = true; last = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); if (spinning) setSpin(false); });
    canvas.addEventListener('pointermove', function (e) {
      hover = pointer(e);
      if (dragging) { az -= (e.clientX - last[0]) * 0.01; el = Math.max(-1.45, Math.min(1.45, el + (e.clientY - last[1]) * 0.01)); last = [e.clientX, e.clientY]; draw(); }
      updateHover();
    });
    canvas.addEventListener('pointerup', function () { dragging = false; });
    canvas.addEventListener('pointerleave', function () { hover = null; updateHover(); });
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
    root.querySelector('[data-ds-error]').hidden = false;
  });
})();
