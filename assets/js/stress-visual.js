/* FIG. 01: normalized axial/shear Cauchy stress, not experimental data.
 * Face-first labels: tau_zx is the x traction on the +z face.
 * Matrix convention: t(n) = tensor * n (symmetric in a classical continuum).
 */
(function (factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (typeof document !== 'undefined') api.mount(document);
})(function () {
  'use strict';
  const turn = 2 * Math.PI, initialPhase = Math.PI / 4, period = 8000;
  const arrowScale = 96, edge = 147, origin = [326, 282.5];
  const plot = { left: 96, right: 552, zero: 546, amplitude: 46 };
  const components = [
    { id: 'sigma-zz', normal: [0,0,1], direction: [0,0,1], index: 2 },
    { id: 'tau-zx', normal: [0,0,1], direction: [1,0,0], index: 0 },
    { id: 'tau-xz', normal: [1,0,0], direction: [0,0,1], index: 2 }
  ];
  const clean = x => Math.abs(x) < 1e-12 ? 0 : x;
  const fmt = x => clean(x).toFixed(3);
  function state(phase) {
    if (!Number.isFinite(phase)) throw new RangeError('Phase must be finite');
    const sigma = clean(Math.sin(phase)), tau = clean(.6 * Math.cos(phase));
    return { sigma, tau, tensor: [[0,0,tau],[0,0,0],[tau,0,sigma]] };
  }
  function traction(phase, normal) {
    return state(phase).tensor.map(row => row.reduce((sum,x,i) => sum + x*normal[i], 0));
  }
  // One orthographic isometric projection for geometry, axes and traction vectors.
  // Camera sees the +x, +y and +z faces; screen y increases downward.
  function project(v) { return [Math.sqrt(3)/2*(v[0]-v[1]), .5*(v[0]+v[1])-v[2]]; }
  function point(v) { return project(v).map((x,i) => origin[i]+edge*x); }
  function facePath(axis) {
    const vertices = {
      z: [[-.5,-.5,.5],[.5,-.5,.5],[.5,.5,.5],[-.5,.5,.5]],
      x: [[.5,-.5,.5],[.5,.5,.5],[.5,.5,-.5],[.5,-.5,-.5]],
      y: [[-.5,.5,.5],[.5,.5,.5],[.5,.5,-.5],[-.5,.5,-.5]]
    };
    return vertices[axis].map((v,i) => (i?'L':'M')+point(v).map(fmt).join(' ')).join('')+'Z';
  }
  function arrow(phase, component) {
    const value = traction(phase,component.normal)[component.index];
    const tail = point(component.normal.map(x=>x*.5));
    const delta = project(component.direction.map(x=>x*value*arrowScale));
    const tip = tail.map((x,i)=>x+delta[i]), length = Math.hypot(...delta);
    const visible = Math.abs(value)>1e-8;
    if (!visible) return { value, tail, tip, visible, path: '' };
    const u=delta.map(x=>x/length), h=Math.min(8,length*.3), w=h*.5;
    const a=[tip[0]-h*u[0]-w*u[1],tip[1]-h*u[1]+w*u[0]];
    const b=[tip[0]-h*u[0]+w*u[1],tip[1]-h*u[1]-w*u[0]];
    const xy=p=>p.map(fmt).join(' ');
    return { value, tail, tip, visible, path:`M${xy(tail)}L${xy(tip)}M${xy(a)}L${xy(tip)}L${xy(b)}` };
  }
  function marker(phase,key) { return [plot.right,plot.zero-plot.amplitude*state(phase)[key]]; }
  function wavePoints(phase,key) {
    return Array.from({length:97},(_,i)=>{
      const u=i/96, value=state(phase+turn*(u-1))[key];
      return [plot.left+(plot.right-plot.left)*u,plot.zero-plot.amplitude*value];
    });
  }
  const pointsString = points => points.map(p=>p.map(fmt).join(',')).join(' ');
  function mount(doc) {
    const win=doc.defaultView;
    if (!win || !win.requestAnimationFrame) return;
    doc.querySelectorAll('[data-stress-visual]').forEach(root=>{
      if (root.dataset.stressReady) return;
      const svg=root.querySelector('svg'), controls=root.querySelector('[data-stress-controls]');
      const toggle=root.querySelector('[data-stress-toggle]'), slider=root.querySelector('[data-stress-phase]');
      const phaseLabel=root.querySelector('[data-stress-angle]');
      const arrows=components.map(c=>root.querySelector('#stress-'+c.id));
      const waves=['sigma','tau'].map(k=>root.querySelector('#stress-wave-'+k));
      const markers=['sigma','tau'].map(k=>root.querySelector('#stress-marker-'+k));
      const values=['sigma','tau'].map(k=>root.querySelector('[data-stress-value="'+k+'"]'));
      if (![svg,controls,toggle,slider,phaseLabel,...arrows,...waves,...markers,...values].every(Boolean)) return;
      const motion=win.matchMedia('(prefers-reduced-motion: reduce)');
      let phase=initialPhase, paused=motion.matches, visible=false, frameId=null;
      let start=null, startPhase=phase, lastPaint=-Infinity;
      function render(p) {
        phase=((p%turn)+turn)%turn;
        const sample=state(phase);
        components.forEach((c,i)=>{
          const a=arrow(phase,c), node=arrows[i];
          node.setAttribute('d',a.path);
          node.setAttribute('visibility',a.visible?'visible':'hidden');
          node.dataset.value=fmt(a.value);
        });
        ['sigma','tau'].forEach((key,i)=>{
          waves[i].setAttribute('points',pointsString(wavePoints(phase,key)));
          const p=marker(phase,key); markers[i].setAttribute('cx',fmt(p[0])); markers[i].setAttribute('cy',fmt(p[1]));
          values[i].textContent=(sample[key]>=0?'+':'')+fmt(sample[key]);
        });
        const degrees=phase*180/Math.PI;
        slider.value=String(degrees); phaseLabel.textContent=Math.round(degrees)+'\u00b0';
        root.dataset.phase=String(phase);
      }
      function tick(now) {
        frameId=null;
        if (paused || !visible || doc.hidden) return;
        if (start===null) { start=now; startPhase=phase; }
        if (now-lastPaint>=1000/30) { render(startPhase+(now-start)*turn/period); lastPaint=now; }
        frameId=win.requestAnimationFrame(tick);
      }
      function sync() {
        if (frameId!==null) win.cancelAnimationFrame(frameId);
        frameId=null; start=null; lastPaint=-Infinity;
        toggle.textContent=paused?toggle.dataset.play:toggle.dataset.pause;
        toggle.setAttribute('aria-label',toggle.textContent);
        root.dataset.playing=String(!paused&&visible&&!doc.hidden);
        if (!paused&&visible&&!doc.hidden) frameId=win.requestAnimationFrame(tick);
      }
      toggle.addEventListener('click',()=>{ paused=!paused; sync(); });
      slider.addEventListener('input',()=>{ paused=true; render(Number(slider.value)*Math.PI/180); sync(); });
      doc.addEventListener('visibilitychange',sync);
      motion.addEventListener('change',()=>{ if (motion.matches) paused=true; sync(); });
      if ('IntersectionObserver' in win) {
        const observer=new win.IntersectionObserver(entries=>{
          visible=entries.some(e=>e.isIntersecting); sync();
        },{threshold:0});
        observer.observe(svg);
      } else { visible=true; }
      render(initialPhase); controls.hidden=false; root.dataset.stressReady='true'; sync();
    });
  }
  return { state, traction, project, point, facePath, arrow, marker, wavePoints, pointsString,
    components, initialPhase, arrowScale, plot, mount };
});
