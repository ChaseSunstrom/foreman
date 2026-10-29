---
name: shader-soft-caustics
title: "Shader: Soft caustics"
area: looks
tags: [shader, glsl, webgl, backdrop, water, light, summer, hospitality]
detect: []
related: [shader-aurora-bands, shader-performance, light-and-material]
---
Light on the floor of a shallow pool, out of focus: a slow net of soft bright threads over a tinted ground, never a glossy wave.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uTime, uIntensity, uScale, uSoft;
uniform vec3 uFloor, uLight;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
void main() {
  vec2 p = (vUv - 0.5) * vec2(uRes.x / uRes.y, 1.0) * uScale;
  float t = uTime * 0.15;
  mat2 r = mat2(0.8, 0.6, -0.6, 0.8);                      // turn the layers apart: no grid shows
  float a = noise(p + vec2(t, -0.6 * t)) + 0.5 * noise(r * p * 2.0 + vec2(-0.7 * t, 0.4 * t));
  float b = noise(r * p * 1.3 + 9.0 - vec2(0.5 * t, -t)) + 0.5 * noise(p * 2.6 + vec2(0.3 * t, 0.8 * t));
  float web = 1.0 - smoothstep(0.0, uSoft, abs(a - b));   // light gathers where the two ripples agree
  float depth = 0.75 + 0.25 * vUv.y;                      // brighter toward the shallow end (top)
  vec3 c = mix(uFloor, uLight, web * 0.6 * depth * uIntensity);
  outColor = vec4(c + (hash(gl_FragCoord.xy) - 0.5) / 255.0, 1.0);  // dither: soft light bands otherwise
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uTime` | float | seconds, wrapped on the CPU every 1,000 s (a wrap jumps the net: do it while off screen) |
| `uIntensity` | float | 0 = plain `uFloor`, 1 = the full net of light |
| `uScale` | float | net cells across the frame height: 3-6 |
| `uSoft` | float | thread width in noise units: 0.06 = crisp, 0.25 = defocused; this look sits at 0.15-0.25 |
| `uFloor`, `uLight` | vec3 | sRGB 0-1 from the `--surface` (or `--sunken`) and a pale tint of `--accent` |

## Cost
Class: low. Four value-noise lookups a pixel, no loop. Render at half resolution and scale up: it's soft on purpose.

## Reduced motion
Still: `uTime = 0.0`: a fixed net of light, redrawn on resize only.

## Sketch
The sketchbook's preset (`fm scene sketchbook`): `uIntensity=1 uScale=4 uSoft=0.2 uFloor=0.1,0.3,0.4 uLight=0.75,0.95,1`

## Suits
Hotels and spas, swimwear and summer campaigns, drinks and citrus brands, a pool or marine-science page.
Not for: anything that must feel dry or exact (finance, legal, tooling), dark night themes (caustics need daylight).

## Verify
- `glslangValidator -S frag soft-caustics.frag`: compiles as GLSL ES 3.00.
- Profile a frame at half resolution on a mid phone: under 2 ms of GPU time.

## Test first
Probe the reduced-motion pair and a frame at `uIntensity = 0.0` (exactly `uFloor`, give or take the dither) before tuning `uSoft`.

## Do
- Keep the contrast between `uFloor` and `uLight` low (under 1.4:1): it's light on a floor, not a pattern.

## Avoid
- Speeding it up past `uTime * 0.15`: fast caustics read as a screensaver, slow ones as daylight.

## Review
- [ ] Threads stay soft at 2x density; no hard grid lines.
- [ ] Text over it keeps 4.5:1 against `uLight`, the brightest pixel.
