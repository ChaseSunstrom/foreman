---
name: webgl
title: WebGL
area: web
tags: [webgl, webgl2, shaders, glsl, canvas, gpu]
detect: [file:*.glsl, file:*.frag, file:*.vert, dep:vite-plugin-glsl]
related: [three-js, react-three-fiber, mapbox-gl]
---
Raw WebGL and WebGL2: contexts, shader programs, buffers, textures and the state-machine mistakes that produce a black canvas.

## Verify
- `npx tsc --noEmit`: typed `WebGL2RenderingContext` usage.
- `npx playwright test`: run in a real browser (use Chromium with a software GL fallback in CI); screenshot or `readPixels` assertions.
- `npx eslint .`: lint.
- `npm run build`: shader imports resolve and bundle.

## Test first
Assert a rendered pixel with `readPixels` in a browser test, before drawing anything fancy.
```ts
import { test, expect } from "@playwright/test";

test("clears to red", async ({ page }) => {
  await page.goto("/");
  const px = await page.evaluate(() => {
    const c = document.querySelector("canvas")!;
    const gl = c.getContext("webgl2", { preserveDrawingBuffer: true })!;
    const out = new Uint8Array(4);
    gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, out);
    return Array.from(out);
  });
  expect(px).toEqual([255, 0, 0, 255]);
});
```

## Do
- Request `webgl2` first and fall back only if you must; check for `null`.
- After `compileShader` and `linkProgram` read `getShaderParameter(s, gl.COMPILE_STATUS)`, `getProgramParameter(p, gl.LINK_STATUS)` and log `getShaderInfoLog` and `getProgramInfoLog`.
- Resize with the canvas `clientWidth` and `clientHeight` times `devicePixelRatio`, set `canvas.width` and `height`, then `gl.viewport`.
- Use `requestAnimationFrame` and a time delta; stop the loop when the canvas is hidden.
- Create buffers, VAOs and textures once; update with `bufferSubData`; delete them (`deleteBuffer`, `deleteTexture`) on teardown.
- Set `precision mediump float;` (or highp where needed) in fragment shaders, and `#version 300 es` first for WebGL2.
- Handle `webglcontextlost` (call `preventDefault`) and `webglcontextrestored` by rebuilding resources.
- Flip images with `UNPACK_FLIP_Y_WEBGL` or in the shader, and set texture filtering for non-power-of-two sizes in WebGL1.

## Avoid
- Ignoring shader compile and link logs: the symptom is a black canvas with no error. Always check status.
- Setting the canvas CSS size but not its `width` and `height`: blurry output. Sync drawing buffer size.
- Creating buffers or programs every frame: leaks and stalls. Create once.
- `readPixels` without `preserveDrawingBuffer` after the frame has presented: reads zeros. Read in the same task as the draw or enable it for tests only.
- Calling `getContext` with a different type on the same canvas: returns null. Pick once.
- Uploading textures that are not power-of-two in WebGL1 with mipmaps or repeat: incomplete texture, renders black. Clamp or resize.
- Forgetting `#version 300 es` as the first line: a shader error that mentions an unexpected token.

## Review
- [ ] Compile and link errors are logged and fail loudly.
- [ ] Canvas size and viewport track the DPR on resize.
- [ ] Resources are created once and deleted on teardown.
- [ ] Context loss is handled and the loop stops when hidden.
- [ ] A browser test proves at least one rendered pixel.
