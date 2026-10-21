# FIG. 01 scientific model and animation

## Prescribed history

This is an illustrative, spatially uniform Cauchy stress history at a material
point, not measured data, a solved boundary-value problem, or a fatigue-life
prediction. All displayed values are divided by the normal-stress amplitude.

- `sigma_zz / sigma_a = sin(phase)`
- `tau_zx / sigma_a = tau_xz / sigma_a = 0.6 sin(phase + pi/2)`
- All other tensor components are zero.

The normalized tensor is `[[0,0,tau],[0,0,0],[tau,0,sigma]]`. Tractions are
computed as `t(n) = tensor * n`. Labels use the face-normal index first and
the traction-direction index second. The tensor is symmetric, so complementary
shears agree in either tensor-index convention. The +y face is traction free.
The hidden negative faces have opposite traction vectors. No deformation is
implied. Grid lines and orbital curves are decorative, not additional data.

One orthographic isometric projection maps geometry and vectors alike:
`P(x,y,z) = (sqrt(3)/2 * (x-y), (x+y)/2 - z)`. Screen y increases downward.
The three projected unit axes have equal lengths and pairwise angles of 120
 degrees. The displayed cube uses edge length 147 and origin (326,282.5).

The analytical quarter-cycle checkpoints are:

| Phase | Normal / sigma_a | Shear / sigma_a |
| --- | --- | --- |
| 0 degrees | 0 | +0.6 |
| 90 degrees | +1 | 0 |
| 180 degrees | 0 | -0.6 |
| 270 degrees | -1 | 0 |

## Rendering

`assets/js/stress-visual.js` contains the shared model and renderer. A single
phase drives both scrolling waveforms, their rightmost current-time markers,
and all three stress-component arrows. Arrow displacement is linear in the
signed component; arrowheads shrink with the vector and vanish at zero.
The curves share one normalized vertical axis. Solid teal identifies the
normal component; dashed pale blue identifies shear, without relying only
on colour. Static SVG paths are checked against the model at 45 degrees.

The figure runs at most approximately 30 updates per second with an 8-second
illustrative cycle. This display period does not claim an experimental loading
frequency. A timestamp-driven clock avoids frame-rate-dependent loading.
Animation pauses off-screen or when the document is hidden. Reduced-motion
preferences start it paused. Play/Pause and a labelled phase slider support
keyboard control. No JavaScript leaves a valid 45-degree static figure and
hides inactive controls. Description and controls use shared EN/IT data files.
No runtime libraries, GIFs, videos, network APIs, or font files are introduced.

## Verification

Run `node --test tests/stress_visual.test.cjs` or the existing
`python -m unittest discover -s tests -v` command. Tests cover quarter cycles,
tensor symmetry, six-face force and moment balance, axis projection, arrow
signs/zero crossings, waveform synchronization and the checked-in fallback.
The repository's existing Jekyll, bilingual and browser CI checks also apply.

Local Chromium component tests cover English and Italian, widths 320, 375,
390, 768 and 1280 px, keyboard control, off-screen suspension, reduced-motion
and disabled-JavaScript rendering. This is component testing, not independent
verification of the deployed Cloudflare site.

## Primary references

- A. F. Bower, Applied Mechanics of Solids, 2.3 (stress and traction)
  https://solidmechanics.org/Text/Chapter2_3/Chapter2_3.php
- MDN requestAnimationFrame (timestamp-driven rendering)
  https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
- MDN Intersection Observer (visibility)
  https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
- MDN prefers-reduced-motion
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
