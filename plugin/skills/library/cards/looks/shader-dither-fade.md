---
name: shader-dither-fade
title: "Shader: Dither fade"
area: looks
tags: [shader, glsl, webgl, transition, dither, pixel, retro, one-bit]
detect: []
related: [shader-halftone, shader-performance, look-lab-notebook]
---
A two-colour transition the way a one-bit screen would draw it: a 4x4 ordered dither sweeps from one colour to the other along an uneven front.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uProgress, uIntensity, uPixel;
uniform vec3 uFrom, uTo;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
float m2(vec2 a) { return mod(2.0 * a.x + 3.0 * a.y, 4.0); }  // the 2x2 Bayer index: 0 2 / 3 1
float bayer(vec2 p) {                                        // 4x4 ordered threshold, 1/32 to 31/32
  return (4.0 * m2(mod(p, 2.0)) + m2(mod(floor(p * 0.5), 2.0)) + 0.5) / 16.0;
}
void main() {
  vec2 cell = floor(gl_FragCoord.xy / uPixel);               // one dither cell = uPixel device px
  vec2 uv = (cell + 0.5) * uPixel / uRes;                    // sampled per cell, so cells stay square
  float order = mix(1.0 - uv.y, noise(uv * vec2(uRes.x / uRes.y, 1.0) * 3.0), 0.35);  // top first, unevenly
  const float S = 0.15;                                       // the dithered band's half-width
  float v = clamp((uProgress * (1.0 + 2.0 * S) - S - order) / (2.0 * S) + 0.5, 0.0, 1.0);
  float pick = step(bayer(cell), v);                         // 0 or 1: no in-between colours
  vec3 c = mix(uFrom, uTo, mix(v, pick, uIntensity));        // uIntensity 0: a plain crossfade
  outColor = vec4(c, 1.0);
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uProgress` | float | 0 = all `uFrom`, 1 = all `uTo`; driven by the transition, not by a clock |
| `uIntensity` | float | 0 = a smooth crossfade with no dither (plain `uFrom` at `uProgress` 0), 1 = pure two-colour dither |
| `uPixel` | float | dither cell size in device px: 2-4 times `devicePixelRatio`, rounded to an integer |
| `uFrom`, `uTo` | vec3 | sRGB 0-1: the outgoing and incoming surface tokens |

## Cost
Class: low. One value-noise lookup and integer-ish arithmetic a pixel, no loop. Full device resolution: the cells must land on whole pixels.

## Reduced motion
Still: `uProgress = 1.0`: the end state at once; no sweep.

## Sketch
The sketchbook's preset (`fm scene sketchbook`; sweep runs uProgress 0 to 1 and back): `uProgress=sweep uIntensity=1 uPixel=3 uFrom=0.07,0.08,0.12 uTo=0.93,0.91,0.86`

## Suits
Page and theme transitions in retro, game and developer-tool sites, a dark-mode switch with character, loading reveals in a pixel-art product.
Not for: soft, premium or editorial looks; transitions faster than `--dur-enter` (the pattern needs time to read).

## Verify
- `glslangValidator -S frag dither-fade.frag`: compiles as GLSL ES 3.00.
- At `uProgress = 0.5`, a screenshot has exactly two colours (with `uIntensity = 1.0`).

## Test first
Count colours in screenshots at `uProgress` 0, 0.5 and 1 (one, two, one) before wiring the transition.

## Do
- Run the sweep on `--dur-stage` with `--ease-move`, then hand over to the plain page.

## Avoid
- A fractional `uPixel`: cells straddle pixels and the pattern shimmers.

## Review
- [ ] At 1x and 2x the dither cells are square and evenly sized.
- [ ] Reduced motion swaps to the end state with no sweep.
