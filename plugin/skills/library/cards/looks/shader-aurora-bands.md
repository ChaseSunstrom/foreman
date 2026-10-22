---
name: shader-aurora-bands
title: "Shader: Aurora bands"
area: looks
tags: [shader, glsl, webgl, backdrop, night, aurora, sky, dark-theme]
detect: []
related: [look-observatory, shader-soft-caustics, shader-grain-gradient, shader-performance]
---
Curtains of light over a night sky: a crisp lower hem, folds and fine rays rising out of it, fading upward and shifting hue with height.

## Shader
Fragment only; pair it with the full-screen triangle vertex shader (`BG_VS`, which gives `vUv`) in `ui/templates/scene.html`.
```glsl
#version 300 es
precision highp float;
in vec2 vUv;
uniform vec2 uRes;
uniform float uTime, uIntensity, uHem;
uniform vec3 uSky, uLow, uHigh;
out vec4 outColor;
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
void main() {
  float t = uTime * 0.04, ax = vUv.x * uRes.x / uRes.y;
  float x = ax * 1.6 + 0.8 * noise(vec2(ax * 1.2, t));          // the curtain sways sideways
  float hem = uHem + 0.4 * (noise(vec2(x * 1.4, t + 3.0)) - 0.5);  // a ribbon that bends
  float up = vUv.y - hem;                                        // height above the hem
  float reach = mix(1.8, 5.0, noise(vec2(x * 0.9, t * 1.5 + 7.0)));  // tall in some folds, short in others
  float curtain = smoothstep(-0.015, 0.02, up) * exp(-max(up, 0.0) * reach);
  float folds = 0.35 + 0.65 * noise(vec2(x * 3.0, t * 2.0));    // bright where the sheet faces us
  float rays = 0.7 + 0.3 * noise(vec2(x * 28.0, t * 0.5));       // fine vertical striation
  float glow = curtain * folds * rays * uIntensity;
  vec3 tint = mix(uLow, uHigh, smoothstep(0.0, 0.35, up));        // hue shifts with height
  vec3 c = uSky + tint * glow;                                    // additive: light on dark
  outColor = vec4(c + (hash(gl_FragCoord.xy) - 0.5) / 255.0, 1.0);  // dark gradients band without it
}
```

## Uniforms
| Uniform | Type | Meaning |
|---|---|---|
| `uRes` | vec2 | canvas size in device px |
| `uTime` | float | seconds, wrapped on the CPU every 2,000 s (a wrap jumps the sway: do it while off screen) |
| `uIntensity` | float | 0 = plain `uSky`, 1 = full curtains |
| `uHem` | float | the hem's height in uv: 0.35-0.55; keep it under the headline, not through it |
| `uSky`, `uLow`, `uHigh` | vec3 | sRGB 0-1: a near-black `--surface`, and two accent-derived lights (`uLow` the hem, `uHigh` the top) |

## Cost
Class: low. Five value-noise lookups a pixel, no loop. Half resolution is fine; the hem stays sharp enough at 2x upscale.

## Reduced motion
Still: `uTime = 0.0`: one curtain, frozen mid-fold.

## Suits
Night themes, astronomy and travel to the north, sleep and calm apps, a launch countdown, winter campaigns.
Not for: light themes (it's light on dark or nothing), anything corporate or medical.

## Verify
- `glslangValidator -S frag aurora-bands.frag`: compiles as GLSL ES 3.00.
- Screenshot the darkest region at 1x: no visible bands in the sky gradient.

## Test first
Probe the reduced-motion pair, and a pixel below the hem (exactly `uSky`, give or take the dither) before picking the lights.

## Do
- Derive `uLow` and `uHigh` from the accent, 20-60 degrees of hue apart, so the sky belongs to the brand.

## Avoid
- The green-to-violet stock aurora: the hues come from the palette, not from a photo.

## Review
- [ ] Text sits on the sky above or below the curtains with 7:1 on `uSky`, never on the brightest fold.
- [ ] The sway is slow enough to miss at a glance (a fold crosses the frame in 20 s or more).
