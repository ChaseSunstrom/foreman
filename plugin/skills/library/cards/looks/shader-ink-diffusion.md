---
name: shader-ink-diffusion
title: "Shader: Ink diffusion"
area: looks
tags: [shader, glsl, webgl, backdrop, ink, watercolour, reveal, editorial]
detect: []
related: [shader-paper-fibre, shader-performance, look-archive-ledger, look-ceramic-studio]
---
A drop of ink spreading through wet paper: an uneven stain, pale in the middle, pigment piled dark along its edge.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uTime, uIntensity, uSpread;
uniform vec2 uOrigin;
uniform vec3 uInk, uPaper;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
float fbm(vec2 p) {
  float s = 0.0, a = 0.5;
  for (int i = 0; i < 4; i++) { s += a * noise(p); p = mat2(1.6, 1.2, -1.2, 1.6) * p + 7.0; a *= 0.5; }
  return s;
}
void main() {
  vec2 aspect = vec2(uRes.x / uRes.y, 1.0), p = (vUv - uOrigin) * aspect * 3.0;
  vec2 drift = 0.6 * vec2(cos(uTime * 0.02), sin(uTime * 0.015));       // a closed loop: the wrap is seamless
  vec2 warp = vec2(fbm(p + drift), fbm(p + 5.2 - drift.yx));            // fibres pull the ink unevenly
  float edge = uSpread - length(p + (warp - 0.5) * 1.8) / 1.5;            // > 0 inside the stain
  float w = fwidth(edge) + 0.004;
  float inside = smoothstep(-w, w, edge);
  float body = mix(0.5, 0.22, smoothstep(0.0, 0.4, edge));               // pale where it soaked in...
  float rim = exp(-max(edge, 0.0) * 22.0);                                // ...dark where it dried
  float ink = clamp((body + rim * 0.45) * inside * (0.8 + 0.4 * fbm(p * 7.0)), 0.0, 1.0);
  vec3 c = mix(uPaper, uInk, ink * uIntensity);
  outColor = vec4(c + (hash(gl_FragCoord.xy) - 0.5) / 255.0, 1.0);  // dither: no banding in the pale wash
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uTime` | float | seconds, wrapped on the CPU every 400 pi s, about 1,256.6 (a multiple of both drift periods, so the outline never jumps) |
| `uIntensity` | float | 0 = plain `uPaper`, 1 = the full stain |
| `uSpread` | float | stain radius, about half a frame height per unit (the warp moves the edge about 0.3 heights either way): 0 = a dot, 0.6 frames a headline, 1 spans the frame's height |
| `uOrigin` | vec2 | the drop's centre in uv (0-1), set behind the element it frames |
| `uInk`, `uPaper` | vec3 | sRGB 0-1 from the `--text` (or `--accent`) and `--surface` tokens |

## Cost
Class: medium. Three 4-octave fbm calls, twelve value-noise lookups a pixel. Render at half resolution and scale up: the wash is soft, only the rim needs `fwidth`, which survives the upscale.

## Reduced motion
Still: `uTime = 0.0`, `uSpread = 1.0`: draw the finished stain once, no spread and no drift; redraw only on resize.

## Suits
Editorial features, literary and art sites, tea and craft brands, a hero reveal behind one headline.
Not for: dashboards, dense UI, anything behind body text (the rim crosses it).

## Verify
- `glslangValidator -S frag ink-diffusion.frag`: compiles as GLSL ES 3.00.
- Emulate `prefers-reduced-motion: reduce`, screenshot twice a second apart: identical.

## Test first
Write the reduced-motion probe and pixel probes before tuning the warp: at `uOrigin` a pale wash (nearer `uPaper` than `uInk`), in a corner exactly `uPaper`.

## Do
- Animate `uSpread` once, 0 to 1 over 1.2-2 s on load, then let only `uTime` drift.

## Avoid
- Several drops at once: one stain is a gesture, five is a screensaver.

## Review
- [ ] The stain never sits under running text; text over it keeps 4.5:1 on its darkest pixel.
- [ ] `uIntensity = 0` renders flat `uPaper`.
- [ ] The rim is crisp at 1x and 2x density.
