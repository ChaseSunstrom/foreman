---
name: shader-grain-gradient
title: "Shader: Grain gradient"
area: looks
tags: [shader, glsl, webgl, backdrop, gradient, grain, film, brand]
detect: []
related: [shader-paper-fibre, shader-aurora-bands, shader-performance, look-night-market]
---
Three brand colours pooled like light on film: slow-orbiting soft centres under a fixed photographic grain that keeps the gradient from looking plastic.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uTime, uIntensity, uGrain;
uniform vec3 uBase, uA, uB;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
vec2 orbit(vec2 home, float speed, float phase) {  // each centre circles its home, each at its own pace
  float t = uTime * speed + phase;
  return home + 0.12 * vec2(cos(t), sin(t * 1.5));
}
void main() {
  vec2 aspect = vec2(uRes.x / uRes.y, 1.0), p = vUv * aspect;
  vec2 c0 = orbit(vec2(0.25, 0.3), 0.05, 0.0) * aspect;
  vec2 c1 = orbit(vec2(0.8, 0.7), 0.04, 2.0) * aspect;
  vec2 c2 = orbit(vec2(0.55, 0.05), 0.06, 4.0) * aspect;
  vec3 d = vec3(dot(p - c0, p - c0), dot(p - c1, p - c1), dot(p - c2, p - c2));
  vec3 w = 1.0 / (d * d + 0.004);                         // 1 / distance^4 pooling: broad pools, soft seams
  vec3 c = (uBase * w.x + uA * w.y + uB * w.z) / (w.x + w.y + w.z);
  float grain = hash(floor(gl_FragCoord.xy)) - 0.5;       // fixed per pixel: grain, not snow
  c = mix(uBase, c, uIntensity) + grain * uGrain * uIntensity;
  outColor = vec4(c + (hash(gl_FragCoord.yx) - 0.5) / 255.0, 1.0);
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uTime` | float | seconds, wrapped on the CPU every 400 pi s, about 1,256.6 (a multiple of every orbit, so the wrap is seamless) |
| `uIntensity` | float | 0 = plain `uBase`, 1 = full gradient and grain |
| `uGrain` | float | grain amplitude in 0-1 colour units: 0.03-0.07 |
| `uBase`, `uA`, `uB` | vec3 | sRGB 0-1: `--surface` plus two brand tints from the project's tokens |

## Cost
Class: low. No noise and no loop: three distances and two hashes a pixel. The gradient could render at half resolution, but the grain must be at full device resolution, so render it all at full.

## Reduced motion
Still: `uTime = 0.0`: the centres rest at their homes; the grain never moved.

## Suits
Brand and campaign heroes, music and event pages, product launches, an app's sign-in backdrop.
Not for: dense UI, data views, behind body text, print-led looks (grain plus halftone fights).

## Verify
- `glslangValidator -S frag grain-gradient.frag`: compiles as GLSL ES 3.00.
- A screenshot at 1x and 2x: grain is visible but no single pixel stands out; no banding in the flats.

## Test first
Probe the reduced-motion pair and `uIntensity = 0.0` (exactly `uBase` plus dither) before choosing the brand tints.

## Do
- Keep the three colours within 0.15 of each other in OKLCH lightness: the gradient carries hue, not contrast.

## Avoid
- The purple-to-blue default pair: pick tints from the brand's own palette.

## Review
- [ ] The grain doesn't move between frames.
- [ ] Text over the brightest centre keeps 4.5:1.
- [ ] No hard ring or seam at any centre.
