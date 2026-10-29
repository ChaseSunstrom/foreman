---
name: babylonjs
title: Babylon.js
area: web
tags: [babylonjs, 3d, webgl, webgpu, scene, engine]
detect: [dep:@babylonjs/core, dep:babylonjs, dep:@babylonjs/loaders, dep:@babylonjs/gui]
related: [three-js, webgl, game-loop, web-performance]
---
Babylon.js: full 3D engine (scene, cameras, PBR, physics, GUI) for WebGL and WebGPU, with ES-module tree-shaking.

## Verify
- `npx tsc --noEmit`: engine and scene types.
- `npx eslint .`: lint.
- `npx playwright test --grep scene`: canvas renders on a fixed camera and a screenshot matches.
- `npx vite build`: bundle size; check you did not import the umbrella `babylonjs` package.

## Test first
Use the `NullEngine` for logic tests, with no GPU.
```ts
import { NullEngine, Scene, MeshBuilder } from "@babylonjs/core";

test("crate sits on the ground plane", () => {
  const engine = new NullEngine();
  const scene = new Scene(engine);
  const crate = MeshBuilder.CreateBox("crate", { size: 1 }, scene);
  crate.position.y = 0.5;
  expect(crate.getBoundingInfo().boundingBox.minimumWorld.y).toBeCloseTo(0);
  scene.dispose();
  engine.dispose();
});
```

## Do
- Import from `@babylonjs/core/...` subpaths and side-effect modules (for example `@babylonjs/core/Loaders/sceneLoader` with `@babylonjs/loaders/glTF`); avoid the `babylonjs` UMD package.
- Create `new Engine(canvas, true)`, run `engine.runRenderLoop(() => scene.render())`, and `window.addEventListener("resize", () => engine.resize())`.
- Dispose in reverse: `scene.dispose()` then `engine.dispose()`, and remove the resize listener.
- Prefer glTF/GLB with Draco or meshopt, and `SceneLoader.ImportMeshAsync` or `LoadAssetContainerAsync`.
- Use `mesh.freezeWorldMatrix()`, instances and thin instances for repeated static geometry.
- Use `scene.onBeforeRenderObservable` for per-frame logic and delta from `engine.getDeltaTime()`.
- For physics, pick one engine (Havok) and step at a fixed rate.

## Avoid
- Importing `@babylonjs/core` root barrel everywhere in a size-sensitive app: pull specific files.
- Creating meshes or materials inside the render loop.
- Leaving observers registered after unmount.
- Running two engines on one page without need.
- Relying on `Math.random` for procedural scenes you test.

## Review
- [ ] Engine and scene are disposed in cleanup.
- [ ] Imports are subpath and tree-shakable.
- [ ] Assets are compressed glTF.
- [ ] Resize and DPR are handled.
- [ ] Per-frame code uses delta time.
