// The tests fail if phase lag, tensor symmetry, projection, or static fallback drift.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const script = path.join(__dirname, '../assets/js/stress-visual.js');
const exists = fs.existsSync(script);
test('the shared scientific model exists', () => assert.ok(exists, 'Missing tensor-driven stress-visual.js'));
if (exists) {
  const m = require(script);
  const close = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${a} != ${b}`);
  const vectorClose = (a, b) => a.forEach((x, i) => close(x, b[i]));
  test('quarter-cycle checkpoints have a 90 degree lead and a 0.6 common-scale amplitude', () => {
    [[0,0,.6],[.25,1,0],[.5,0,-.6],[.75,-1,0],[1,0,.6]].forEach(([c,s,t]) => {
      close(m.state(c * 2 * Math.PI).sigma, s); close(m.state(c * 2 * Math.PI).tau, t);
    });
  });
  test('the prescribed tensor stays symmetric and y faces stay traction free', () => {
    for (let i=0;i<=360;i++) {
      const p=i*Math.PI/180, {tensor, sigma, tau}=m.state(p);
      assert.deepEqual(tensor, [[0,0,tau],[0,0,0],[tau,0,sigma]]);
      vectorClose(m.traction(p,[0,0,1]),[tau,0,sigma]);
      vectorClose(m.traction(p,[1,0,0]),[0,0,tau]);
      vectorClose(m.traction(p,[0,1,0]),[0,0,0]);
    }
  });
  test('opposite faces balance force and moment over the entire cycle', () => {
    const normals=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
    for(let i=0;i<64;i++){
      const p=i*2*Math.PI/64, force=[0,0,0], moment=[0,0,0];
      for(const n of normals){
        const t=m.traction(p,n), r=n.map(x=>x/2);
        t.forEach((v,k)=>force[k]+=v);
        [r[1]*t[2]-r[2]*t[1],r[2]*t[0]-r[0]*t[2],r[0]*t[1]-r[1]*t[0]].forEach((v,k)=>moment[k]+=v);
      }
      vectorClose(force,[0,0,0]); vectorClose(moment,[0,0,0]);
    }
  });
  test('all cube axes use the same equal-length isometric projection', () => {
    const [x,y,z]=[[1,0,0],[0,1,0],[0,0,1]].map(m.project);
    assert.ok(x[0]>0 && x[1]>0 && y[0]<0 && y[1]>0 && z[0]===0 && z[1]<0);
    [x,y,z].forEach(v=>close(Math.hypot(...v),1));
    close(x[0]*y[0]+x[1]*y[1],-.5);
    close(y[0]*z[0]+y[1]*z[1],-.5);
    close(z[0]*x[0]+z[1]*x[1],-.5);
  });
  test('arrow displacement follows traction, reverses correctly, and vanishes at zero', () => {
    for(const p of [0,.2,Math.PI/2,Math.PI,3*Math.PI/2,5.7]){
      for(const component of m.components){
        const a=m.arrow(p,component), t=m.traction(p,component.normal);
        const expected=m.project(component.direction.map(v=>v*t[component.index]*m.arrowScale));
        vectorClose(a.tip.map((v,i)=>v-a.tail[i]),expected);
        assert.equal(a.visible,Math.abs(t[component.index])>1e-8);
      }
    }
  });
  test('both moving wave endpoints use exactly the same instant as the arrows', () => {
    for(const p of [0,Math.PI/4,Math.PI/2,Math.PI,3*Math.PI/2,6.28]){
      for(const key of ['sigma','tau']){
        const points=m.wavePoints(p,key);
        vectorClose(points[points.length-1],m.marker(p,key));
        close(points[0][1],points[points.length-1][1]);
        close(m.marker(p,key)[1],m.plot.zero-m.plot.amplitude*m.state(p)[key]);
      }
    }
  });
  test('non-finite input is rejected rather than emitting invalid SVG coordinates', () => {
    for(const p of [NaN,Infinity,-Infinity]) assert.throws(()=>m.state(p),/finite/);
  });
  test('the no-JavaScript SVG agrees with the model at 45 degrees', () => {
    const template=fs.readFileSync(path.join(__dirname,'../_includes/home_visual.html'),'utf8');
    for(const c of m.components){
      const d=template.match(new RegExp(`id="stress-${c.id}"[^>]* d="([^"]+)"`));
      assert.ok(d, `Static arrow ${c.id} is missing`);
      assert.equal(d[1],m.arrow(m.initialPhase,c).path);
    }
    for(const key of ['sigma','tau']){
      const d=template.match(new RegExp(`id="stress-wave-${key}"[^>]* points="([^"]+)"`));
      assert.equal(d?.[1],m.pointsString(m.wavePoints(m.initialPhase,key)));
    }
    for(const axis of ['x','y','z']){
      const d=template.match(new RegExp(`data-face="${axis}"[^>]* d="([^"]+)"`));
      assert.equal(d?.[1],m.facePath(axis));
    }
  });
}
