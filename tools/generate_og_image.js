// Render the 1200x630 Open Graph card from the built homepage FIG. 01.
// Usage: node tools/generate_og_image.js <built _site dir> [output png]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const site = process.argv[2] || '_site';
const out = process.argv[3] || 'assets/img/og-card.png';
const html = fs.readFileSync(path.join(site, 'index.html'), 'utf8');
const match = html.match(/<svg id="stress-svg"[\s\S]*?<\/svg>/);
if (!match) throw new Error('FIG. 01 (#stress-svg) not found in ' + site);
// The HTML minifier lowercases attributes; crop the outer margins of the 640x640 figure.
const svg = match[0].replace(/viewbox="0 0 640 640"/i, 'viewBox="40 95 560 535"');
if (svg === match[0]) throw new Error('Unexpected FIG. 01 viewBox');

const card = `<!doctype html><html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; }
  body { width: 1200px; height: 630px; background: #102E51; color: #ECF5F7; font-family: Inter, "Helvetica Neue", Arial, sans-serif;
         display: grid; grid-template-columns: 560px 1fr; overflow: hidden; }
  .copy { padding: 72px 0 64px 72px; display: flex; flex-direction: column; }
  .eyebrow, .foot { font: 500 20px/1.4 ui-monospace, "DejaVu Sans Mono", monospace; letter-spacing: .1em; text-transform: uppercase; color: #77D5D0; }
  h1 { font: 700 92px/1.0 ui-monospace, "DejaVu Sans Mono", monospace; letter-spacing: -.06em; margin: 36px 0 28px; }
  h1 span { display: block; font-weight: 400; }
  p { font-size: 28px; line-height: 1.4; color: #C6DCE6; }
  .foot { margin-top: auto; color: #A3CDDF; font-size: 18px; }
  .art { background: #0E2A49; border-left: 1px solid rgba(179,217,234,.2); display: grid; place-items: center; }
  .art svg { width: 590px; height: auto; }
  /* Stroke colours of FIG. 01, mirrored from _sass/_stress_visual.scss. */
  .stress-arrow { stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; fill: none; }
  .stress-normal { stroke: #82e2de; } .stress-shear { stroke: #d2e9f8; }
  .stress-wave { stroke-width: 2.5; stroke-linejoin: round; fill: none; } .stress-wave.stress-shear { stroke-dasharray: 7 4; }
  .stress-dot-sigma { fill: #82e2de; } .stress-dot-tau { fill: #d2e9f8; }
</style></head><body>
  <div class="copy">
    <div class="eyebrow">Fatigue · Structural integrity</div>
    <h1>Andrea<span>Chiocca</span></h1>
    <p>Multiaxial fatigue, critical plane methods and welded joints. University of Pisa.</p>
    <div class="foot">andreachiocca.github.io</div>
  </div>
  <div class="art">${svg}</div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.setContent(card, { waitUntil: 'load' });
  await page.screenshot({ path: out, type: 'png' });
  await browser.close();
  console.log('Wrote', out);
})();
