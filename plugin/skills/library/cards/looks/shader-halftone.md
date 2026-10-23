---
name: shader-halftone
title: "Shader: Halftone"
area: looks
tags: [shader, glsl, webgl, backdrop, print, newsprint, comic, dots]
detect: []
related: [shader-dither-fade, look-broadcast-graphics, look-shipping-manifest, shader-performance]
---
A one-ink print screen: a rotated grid of dots whose size carries the tone, here a pool of light that wanders slowly across the page.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes, uFocus;
uniform float uTime, uIntensity, uCell, uAngle, uReach;
uniform vec3 uInk, uPaper;
out vec4 outColor;
void main() {
  float s = sin(uAngle), c = cos(uAngle);
  mat2 toScreen = mat2(c, s, -s, c), toPage = mat2(c, -s, s, c);
  vec2 g = toScreen * (vUv * uRes) / uCell;          // position on the rotated screen, in cells
  vec2 cell = floor(g) + 0.5, f = g - cell;          // f: offset from the dot's centre, -0.5 to 0.5
  vec2 centre = toPage * (cell * uCell) / uRes;      // that dot's centre back in uv
  vec2 aspect = vec2(uRes.x / uRes.y, 1.0);
  vec2 focus = uFocus + 0.06 * vec2(sin(uTime * 0.21), cos(uTime * 0.17));
  float lit = 1.0 - smoothstep(0.0, uReach, length((centre - focus) * aspect));
  float tone = mix(0.12, 0.85, 1.0 - lit) * uIntensity;  // ink coverage: darker away from the light
  float r = sqrt(tone / 3.14159);                     // dot area = coverage, in cell units
  float d = length(f), aa = fwidth(d);
  float dotInk = (1.0 - smoothstep(r - aa, r + aa, d)) * step(1e-4, tone);  // no speck when r is 0
  outColor = vec4(mix(uPaper, uInk, dotInk), 1.0);
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uFocus` | vec2 | the light pool's centre in uv (0-1) |
| `uTime` | float | seconds, wrapped on the CPU every 200 pi s, about 628.3 (a multiple of both sway periods, so the wrap is seamless) |
| `uIntensity` | float | 0 = plain `uPaper`, 1 = full coverage range |
| `uCell` | float | dot pitch in device px: 6-14 (multiply a CSS value by `devicePixelRatio`) |
| `uAngle` | float | screen angle in radians: 0.2618 (15 degrees) or 0.7854 (45); never 0, which reads as a grid |
| `uReach` | float | the light pool's radius in frame heights: 0.5-1.2 |
| `uInk`, `uPaper` | vec3 | sRGB 0-1 from the `--text` (or `--accent`) and `--surface` tokens |

## Cost
Class: low. No noise, no loop: two rotations, one `fwidth`, a few multiplies a pixel. Full device resolution: the dots are the look.

## Reduced motion
Still: `uTime = 0.0`: the light pool rests at `uFocus`.

## Sketch
The sketchbook's preset (`fm scene sketchbook`): `uFocus=0.6,0.55 uIntensity=1 uCell=8 uAngle=0.2618 uReach=0.8 uInk=0.1,0.1,0.14 uPaper=0.97,0.95,0.9`

## Suits
Newsletters and news products, comics and zines, sports and match pages, packaging and merch sites, a print-heritage brand.
Not for: luxury, wellness, medical, anything behind long reading (dots under text tire the eye).

## Verify
- `glslangValidator -S frag halftone.frag`: compiles as GLSL ES 3.00.
- A screenshot at 1x and 2x: dots stay round and the same pitch in CSS px.

## Test first
Probe a pixel at `uFocus` (mostly `uPaper`) and one in a corner (mostly `uInk`), and the reduced-motion pair, before the art direction.

## Do
- Keep the coverage range off both ends (0.12-0.85): solid ink or bare paper loses the print.

## Avoid
- Four-colour CMYK rosettes: one ink, the brand's, is the look; process colour turns it into a pastiche.

## Review
- [ ] `uCell` is scaled by `devicePixelRatio`, so dots are the same size on every screen.
- [ ] The screen angle isn't 0 or 90 degrees.
