---
name: react-three-fiber
title: React Three Fiber
area: web
tags: [react-three-fiber, three, react, webgl, drei, canvas]
detect: [dep:@react-three/fiber, dep:@react-three/drei, dep:@react-three/test-renderer]
related: [three-js, react, webgl]
---
React Three Fiber: a React renderer for three.js with a frame loop, drei helpers and strict rules about state and allocation.

## Verify
- `npx tsc --noEmit`: JSX intrinsic elements and three types resolve.
- `npx eslint .`: lint.
- `npx vitest run`: scene-graph tests through `@react-three/test-renderer`.
- `npm run build`: bundle (three is large, so check chunking).

## Test first
Render to the test renderer and inspect the scene graph, with no GPU needed.
```tsx
import ReactThreeTestRenderer from "@react-three/test-renderer";
import { Box } from "./Box";

test("box scales up when selected", async () => {
  const r = await ReactThreeTestRenderer.create(<Box selected />);
  const mesh = r.scene.children[0];
  expect(mesh.instance.scale.x).toBe(1.5);
});
```

## Do
- Put per-frame motion in `useFrame((state, delta) => ...)` and mutate refs directly (`ref.current.rotation.y += delta`).
- Use `delta` for frame-rate independent speed.
- Keep React state for discrete events (selected, mode), not for values that change every frame.
- Share geometries and materials: define them once (`useMemo` or module scope) or use `<instancedMesh>` for many copies.
- Load assets with `useGLTF`, `useTexture` (drei) inside `<Suspense>`, and `useGLTF.preload` for known models.
- Use `frameloop="demand"` and `invalidate()` for scenes that rarely change.
- Dispose of manually created resources in an effect cleanup; R3F disposes what it created.
- Use `<Canvas dpr={[1, 2]}>` to cap pixel ratio.

## Avoid
- `setState` inside `useFrame`: re-renders at 60 fps. Mutate refs.
- Creating `new THREE.Vector3()` or materials inside `useFrame` or render: garbage and GC stalls. Reuse module-level objects.
- Using R3F hooks (`useThree`, `useFrame`) outside `<Canvas>` children: they throw. Move the component inside.
- Putting DOM elements as children of `<Canvas>`: use drei `Html` or place the DOM outside.
- Context from outside the canvas assumed to be available inside: the canvas is a separate reconciler root, so re-provide the context inside.
- Hundreds of separate meshes for identical objects: draw calls explode. Use instancing.
- Loading assets without Suspense: nothing renders or errors unclearly. Wrap in `Suspense` with a fallback.

## Review
- [ ] No React state updates per frame.
- [ ] No allocations in `useFrame`.
- [ ] Geometries, materials and textures are shared or instanced.
- [ ] Assets load under Suspense and heavy models are preloaded or lazy.
- [ ] Context is re-provided inside the Canvas where needed.
