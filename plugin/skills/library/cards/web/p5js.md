---
name: p5js
title: p5.js
area: web
tags: [p5, p5js, creative-coding, canvas, generative]
detect: [dep:p5, dep:@types/p5, dep:react-p5, dep:@p5-wrapper/react]
related: [svg-canvas, web-performance, game-loop, webgl]
---
p5.js: Processing for the web; global-mode sketches are quick, instance mode is what belongs in an app.

## Verify
- `npx tsc --noEmit`: with `@types/p5` or bundled types for 2.x.
- `npx eslint .`: lint.
- `npx playwright test --grep sketch`: the canvas exists and a seeded frame matches a screenshot.
- `npx vite build`: p5 is large (about 1 MB minified); confirm it loads lazily.

## Test first
Make sketches deterministic with seeds and test the pure logic apart from the canvas.
```ts
import { makePoints } from "./points";

test("same seed gives the same points", () => {
  const a = makePoints(42, 100);
  const b = makePoints(42, 100);
  expect(a).toEqual(b);
  expect(a).toHaveLength(100);
});
```

## Do
- Use instance mode: `new p5(p => { p.setup = ...; p.draw = ...; }, parentEl)`; never leak globals into an app.
- Seed both generators: `p.randomSeed(seed)` and `p.noiseSeed(seed)`, and show the seed in the UI or URL.
- Keep math in plain functions that take `p` or numbers, so they test without a canvas.
- Call `p.remove()` on teardown; in React do it in the effect cleanup.
- Use `p.pixelDensity(1)` for heavy sketches, `p.noLoop()` for static ones, and `p.frameRate(30)` when 60 is not needed.
- Use `createGraphics` for layers drawn once; load assets in `preload` (1.x) or with `async setup` (2.x).
- Offer a pause control and honor reduced motion by calling `noLoop()`.

## Avoid
- Global mode in a bundled app: name clashes with `random`, `scale`, `text`.
- `Math.random()` inside a sketch you want reproducible.
- Building arrays or strings in `draw()` every frame.
- Importing p5 in SSR: it needs `window`. Use a dynamic import in an effect.
- Re-creating the sketch on every render.

## Review
- [ ] Instance mode with `remove()` on cleanup.
- [ ] Randomness and noise are seeded.
- [ ] p5 is lazy-loaded and not in the SSR path.
- [ ] Logic is testable without a canvas.
- [ ] Reduced motion and frame rate are considered.
