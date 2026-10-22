---
name: shader-contour-lines
title: "Shader: Contour lines"
area: looks
tags: [shader, glsl, webgl, backdrop, topographic, map, outdoor, survey]
detect: []
related: [look-cartographer, shader-performance, shader-halftone]
---
A survey map's contours over a slowly shifting terrain: hairlines a pixel wide, every fifth one heavier, like an index contour.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uTime, uIntensity, uCount;
uniform vec3 uLine, uGround;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
float height(vec2 p, float t) {  // three octaves drifting apart: the land breathes, it doesn't scroll
  return 0.55 * noise(p + vec2(t, 0.0)) + 0.3 * noise(p * 2.1 - vec2(0.0, t * 1.3))
       + 0.15 * noise(p * 4.3 + vec2(t * 0.7, -t));
}
void main() {
  vec2 p = (vUv - 0.5) * vec2(uRes.x / uRes.y, 1.0) * 2.2;
  float h = height(p, uTime * 0.01) * uCount;            // height in contour steps
  float slope = max(length(vec2(dFdx(h), dFdy(h))), 1e-4);  // true gradient: diagonals as thin as the rest
  float px = abs(fract(h - 0.5) - 0.5) / slope;          // distance to the nearest line, in px
  float index = 1.0 - step(0.5, mod(floor(h + 0.5), 5.0)); // every fifth step
  float line = clamp(mix(0.6, 1.1, index) + 0.5 - px, 0.0, 1.0);  // 1.2 px and 2.2 px lines
  float ink = line * mix(0.55, 1.0, index) * uIntensity;
  outColor = vec4(mix(uGround, uLine, ink), 1.0);
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uTime` | float | seconds, wrapped on the CPU every 1,000 s (a wrap shifts the terrain by 10 noise cells: do it while off screen) |
| `uIntensity` | float | 0 = plain `uGround`, 1 = full-strength lines |
| `uCount` | float | contour steps across the height range: 12-24; above 30 the lines merge into a moire |
| `uLine`, `uGround` | vec3 | sRGB 0-1 from the `--border` (or `--accent`) and `--surface` tokens |

## Cost
Class: low. Three value-noise lookups and two screen-space derivatives a pixel, no loop. Render at full device resolution: the lines are 1-2 px and blur when scaled.

## Reduced motion
Still: `uTime = 0.0`: one fixed map, redrawn on resize only.

## Suits
Outdoor gear, trail and travel apps, geography and climate stories, survey and land tools, an about page for a field team.
Not for: food, fashion, anything urban and flat, a backdrop under data charts (two sets of lines compete).

## Verify
- `glslangValidator -S frag contour-lines.frag`: compiles as GLSL ES 3.00.
- Zoom a screenshot at 2x density: lines stay 1-2 device px wide on steep and flat ground alike.

## Test first
Probe two screenshots under `prefers-reduced-motion: reduce` (identical), and one with `uIntensity = 0.0` (one flat colour) first.

## Do
- Put the copy over the flattest region: move the view (the `p` offset) until a calm patch sits behind the headline.

## Avoid
- Labelled elevations or fake place names: decoration that reads as data misleads.

## Review
- [ ] Index contours (every fifth) read as heavier at arm's length.
- [ ] No moire on a phone at 3x density.
- [ ] Text over the field holds 4.5:1 against `uLine` as well as `uGround`.
