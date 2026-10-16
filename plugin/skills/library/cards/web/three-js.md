---
name: three-js
title: Three.js
area: web
tags: [threejs, webgl, 3d, graphics, typescript, rendering]
detect: [dep:three, dep:@react-three/fiber, dep:troika-three-text]
related: [react, playwright, vitest]
---
Three.js scenes: a renderer, scene, camera and an animation loop, with explicit GPU resource disposal.

## Verify
- `npx tsc --noEmit`: with `@types/three` matching the installed `three` version.
- `npx vitest run`: pure math and scene-graph logic (no WebGL needed).
- `npm run build`: bundle; confirms imports resolve (`three/addons/...`).
- `npx playwright test`: a real browser smoke test that the canvas renders and no console errors occur.

## Test first
Unit-test logic that does not need a GPU (math, layout, scene construction); smoke-test rendering in a browser.
```ts
import { test, expect } from "vitest";
import * as THREE from "three";
import { buildScene } from "./scene";

test("scene has one light and the mesh at origin", () => {
  const scene = buildScene();
  expect(scene.getObjectByProperty("isLight", true)).toBeDefined();
  expect(scene.getObjectByName("hero")!.position.equals(new THREE.Vector3())).toBe(true);
});
```

## Do
- Drive rendering with `renderer.setAnimationLoop(fn)`; use `THREE.Clock` or the delta from the timestamp for frame-rate independent motion.
- Handle resize: update `camera.aspect`, call `camera.updateProjectionMatrix()`, `renderer.setSize(w, h)`.
- Cap pixel ratio: `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- Dispose what you create: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, and `renderer.dispose()` on teardown.
- Reuse geometries and materials; use `InstancedMesh` for many copies.
- Import add-ons from `three/addons/...` (or `three/examples/jsm/...` on older versions).
- Set `texture.colorSpace = THREE.SRGBColorSpace` on color textures and keep the renderer output in sRGB.
- With React, use `@react-three/fiber` and mutate objects in `useFrame` rather than through state.

## Avoid
- Creating geometry, materials or vectors every frame: GC stalls and GPU leaks. Allocate once and reuse.
- Forgetting to dispose on route change or unmount: VRAM grows until the context is lost. Traverse the scene and dispose.
- `requestAnimationFrame` loops with no cancel on teardown: ghost renders. Use `setAnimationLoop(null)` or cancel the id.
- Deprecated pre-r152 color settings (`renderer.outputEncoding`, `texture.encoding`, `sRGBEncoding`): wrong colors on current versions. Use `outputColorSpace` and `colorSpace`.
- Moving the camera or objects via React state per frame in R3F: re-renders at 60 fps. Mutate refs in `useFrame`.
- Huge uncompressed textures: memory and load time. Compress (KTX2) and downsize.
- `Geometry` (removed): use `BufferGeometry`.

## Review
- [ ] Resize and pixel-ratio handling exist.
- [ ] Every created geometry, material, texture and renderer is disposed on teardown.
- [ ] No allocations inside the frame loop.
- [ ] Color space settings are correct for textures and output.
- [ ] A browser smoke test confirms the canvas renders without console errors.
