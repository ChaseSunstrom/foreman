---
name: pixijs
title: PixiJS
area: web
tags: [pixijs, pixi, 2d, webgl, webgpu, sprites, canvas]
detect: [dep:pixi.js, dep:@pixi/react, dep:@pixi/app]
related: [webgl, svg-canvas, game-loop, web-performance]
---
PixiJS: fast 2D renderer (WebGL or WebGPU) with a scene graph, sprites, text and filters.

## Verify
- `npx tsc --noEmit`: display object and options types (v8 uses async `app.init`).
- `npx eslint .`: lint, including effect cleanup.
- `npx playwright test --grep pixi`: canvas renders, screenshot or pixel read matches.
- `npx vite build`: bundle size; import only what you use in v8.

## Test first
Render once and assert a pixel, not frames. This needs a real WebGL context, so run it in browser mode (Vitest browser mode or Playwright), not jsdom.
```ts
import { Application, Graphics, Rectangle } from "pixi.js";

test("red square draws at the origin", async () => {
  const app = new Application();
  await app.init({ width: 64, height: 64, preference: "webgl", backgroundAlpha: 0 });
  app.stage.addChild(new Graphics().rect(0, 0, 32, 32).fill(0xff0000));
  app.render();
  const px = app.renderer.extract.pixels({ target: app.stage, frame: new Rectangle(8, 8, 1, 1) });
  expect(Array.from(px.pixels.slice(0, 3))).toEqual([255, 0, 0]);
  app.destroy(true, { children: true, texture: true });
});
```

## Do
- In v8, `await app.init({...})` before using `app.canvas`; in v7, `app.view`. Check the installed major.
- Destroy on teardown: `app.destroy(true, { children: true, texture: true })`; in React strict mode make init and destroy idempotent.
- Use `Assets.load` for textures and spritesheets; pack sprites into atlases to cut draw calls.
- Put game logic in `app.ticker.add(({ deltaTime }) => ...)`; scale movement by delta.
- Use `ParticleContainer` for thousands of simple sprites, and `cacheAsTexture` for static complex groups.
- Set `resolution: devicePixelRatio` with `autoDensity: true`, and `resizeTo` the container.
- Reduce motion for decorative scenes by pausing the ticker.

## Avoid
- Creating `Graphics` or `Text` objects every frame: allocation churn. Reuse and mutate.
- Forgetting to destroy textures: GPU memory leaks.
- Large filters over the whole stage: a fill-rate cost. Scope filters.
- Mixing v7 and v8 snippets: the API changed.
- Running the ticker in hidden tabs or off-screen.

## Review
- [ ] Init is awaited and destroy is called.
- [ ] Textures come from atlases, and counts are reasonable.
- [ ] Movement uses delta time.
- [ ] No per-frame allocations in the ticker.
- [ ] DPR and resize handled.
