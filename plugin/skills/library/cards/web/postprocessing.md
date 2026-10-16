---
name: postprocessing
title: postprocessing (pmndrs)
area: web
tags: [threejs, postprocessing, webgl, effects, graphics, typescript]
detect: [dep:postprocessing]
related: [three-js, vitest, playwright]
---
The pmndrs `postprocessing` library for three.js: an EffectComposer running passes, with effects merged into few draw passes.

## Verify
- `npx tsc --noEmit`: types resolve for `postprocessing` against the installed `three`.
- `npm run build`: the bundle resolves imports from `postprocessing` and `three`.
- `npx vitest run`: pure setup logic, such as which effects are configured.
- `npx playwright test`: a real browser smoke test that the canvas renders with no console errors.

## Test first
WebGL is not available in unit tests: factor the effect list into a function and test that, then smoke-test rendering in a browser.
```ts
import { test, expect } from "vitest";
import { buildEffects } from "./effects";

test("bloom comes before vignette and both are configured", () => {
  const names = buildEffects().map((e) => e.name);
  expect(names.indexOf("BloomEffect")).toBeLessThan(names.indexOf("VignetteEffect"));
});
```

## Do
- Create the renderer with antialiasing off (`new WebGLRenderer({ antialias: false })`) since the composer renders to its own buffers; use `SMAAEffect` or the composer's multisampling for edges.
- Build the chain as `new EffectComposer(renderer)`, then `composer.addPass(new RenderPass(scene, camera))`, then `composer.addPass(new EffectPass(camera, ...effects))`.
- Put several effects in one `EffectPass` so they merge into a single shader and fewer passes.
- Call `composer.render()` in the animation loop in place of `renderer.render(scene, camera)`.
- On resize, call `composer.setSize(width, height)` as well as updating the camera.
- Dispose with `composer.dispose()` on teardown, together with the renderer, geometries and materials.
- With React Three Fiber, use `@react-three/postprocessing` rather than hand-wiring a composer.

## Avoid
- Calling `renderer.render` after the composer is set up: effects are skipped or doubled. Render through the composer only.
- Leaving renderer `antialias` on with a composer: extra cost and no benefit. Turn it off.
- One `EffectPass` per effect: more passes than needed. Merge effects into one pass where possible.
- Forgetting `composer.setSize` on resize: a stretched or blurry image. Resize both.
- Mismatched `three` and `postprocessing` versions: runtime errors or shader failures. Check the peer dependency range.
- Skipping disposal on unmount: leaked render targets and VRAM growth. Dispose the composer.

## Review
- [ ] The renderer is created with `antialias: false`.
- [ ] A `RenderPass` comes first and effects share `EffectPass` instances.
- [ ] The loop calls `composer.render()` only.
- [ ] Resize updates both the camera and `composer.setSize`.
- [ ] The composer is disposed on teardown.
- [ ] A browser smoke test confirms the canvas renders.
