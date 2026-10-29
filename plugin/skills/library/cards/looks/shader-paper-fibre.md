---
name: shader-paper-fibre
title: "Shader: Paper fibre"
area: looks
tags: [shader, glsl, webgl, backdrop, paper, texture, stationery, craft]
detect: []
related: [shader-ink-diffusion, look-archive-ledger, look-sewing-pattern, shader-performance]
---
Handmade paper seen close: cloudy mottling from the pulp, short bent fibres lying every which way and a fine tooth, all in the paper's own colour.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform float uIntensity, uScale;
uniform vec3 uPaper, uFibre;
out vec4 outColor;
uint pcg(uint v) { uint s = v * 747796405u + 2891336453u; uint w = ((s >> ((s >> 28u) + 4u)) ^ s) * 277803737u;
  return (w >> 22u) ^ w; }
float hash(vec2 p) {  // integer PCG hash: exact at any pixel coordinate, where a sin() hash streaks on some GPUs
  uvec2 q = uvec2(ivec2(floor(p)) & 0xffff);
  return float(pcg(q.x + pcg(q.y))) / 4294967295.0;
}
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
float fbm(vec2 p) {
  float s = 0.0, a = 0.5;
  for (int i = 0; i < 3; i++) { s += a * noise(p); p = mat2(1.6, 1.2, -1.2, 1.6) * p; a *= 0.5; }
  return s / 0.875;
}
float fibres(vec2 p, float angle) {  // noise stretched 25:1 along one direction: thin, short strands
  vec2 d = vec2(cos(angle), sin(angle));
  vec2 q = vec2(dot(p, d), dot(p, vec2(-d.y, d.x))) * vec2(0.035, 0.85);
  return smoothstep(0.74, 0.95, noise(q));
}
void main() {
  vec2 p = gl_FragCoord.xy / uScale;                   // in CSS px: the texture never stretches with the canvas
  float mottle = fbm(p / 140.0) - 0.5;                 // cloudy pulp, about 140 px across
  vec2 w = p + 22.0 * vec2(noise(p / 45.0), noise(p / 45.0 + 9.0));  // bend the strands: pulp, not linen
  float strands = max(max(fibres(w, 0.35), fibres(w + 31.0, 2.1) * 0.8), fibres(w + 57.0, 1.2) * 0.6);
  float tooth = hash(floor(p)) - 0.5;
  vec3 c = uPaper * (1.0 + mottle * 0.06 * uIntensity);
  c = mix(c, uFibre, strands * 0.4 * uIntensity) + tooth * 0.025 * uIntensity;
  outColor = vec4(c, 1.0);
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uIntensity` | float | 0 = plain `uPaper`, 1 = full texture; 0.5-0.8 under body text |
| `uScale` | float | `devicePixelRatio`, so the texture is sized in CSS px on every screen |
| `uPaper`, `uFibre` | vec3 | sRGB 0-1: `--surface`, and a strand colour 3-6% darker or lighter on the same hue |

## Cost
Class: medium. A 3-octave fbm, a two-lookup warp and three fibre layers: eight value-noise calls and a hash a pixel. It doesn't move: render once into a texture or a CSS background image and the cost is paid once per resize.

## Reduced motion
Static: nothing moves, so the still is the only frame; draw it once and on resize.

## Sketch
The sketchbook's preset (`fm scene sketchbook`): `uIntensity=0.7 uScale=1 uPaper=0.96,0.94,0.89 uFibre=0.9,0.88,0.82`

## Suits
Stationery, publishing and letterpress, wedding and invitation sites, archives, recipe and craft blogs, a reading view that should feel like a page.
Not for: glossy tech, dark themes (fibres read as dust on black), anything that prints (the printer adds its own paper).

## Verify
- `glslangValidator -S frag paper-fibre.frag`: compiles as GLSL ES 3.00.
- Body text over it at `uIntensity = 0.8`: 4.5:1 against the darkest strand, measured on a screenshot.

## Test first
Probe `uIntensity = 0.0` (exactly `uPaper`) and a screenshot at 1x and 2x (same strand length in CSS px) before tuning.

## Do
- Bake it once to an image (`canvas.toBlob`) and set it as the page background, then free the GL context.

## Avoid
- Visible repetition: if you tile the baked image, make the tile at least 512 CSS px.

## Review
- [ ] The texture is felt, not seen, at reading distance.
- [ ] Strands are the same length on a phone and on a desktop.
