---
name: rive
title: Rive
area: web
tags: [rive, animation, state-machine, canvas, interactive]
detect: [dep:@rive-app/canvas, dep:@rive-app/react-canvas, dep:@rive-app/webgl, dep:rive-react]
related: [animation, svg-canvas, accessibility, web-performance]
---
Rive: runtime for `.riv` interactive vector animations driven by state machines and inputs.

## Verify
- `npx tsc --noEmit`: state machine and input names are strings, so also run the test below.
- `npx eslint .`: lint, including effect cleanup.
- `npx playwright test --grep rive`: the canvas renders (non-blank pixels) and a click changes state.
- `du -h public/*.riv`: asset sizes stay in budget (aim under 200 KB each).

## Test first
Load the file and assert the state machine and input names exist, so a renamed input fails CI.
```ts
import { Rive } from "@rive-app/canvas";

test("button.riv exposes the expected inputs", async () => {
  const r = new Rive({ src: "/button.riv", stateMachines: "Main", canvas: document.createElement("canvas") });
  await new Promise<void>(res => (r.on as any)("load", res));
  const names = r.stateMachineInputs("Main").map(i => i.name);
  expect(names).toEqual(expect.arrayContaining(["hover", "pressed"]));
  r.cleanup();
});
```

## Do
- Prefer `@rive-app/canvas` (or `canvas-lite` when no Rive text or layout is needed); use `@rive-app/webgl` only when needed.
- Drive behavior through state machine inputs (`input.value = true`, `input.fire()`), not by playing named animations.
- Pass `autoplay`, `stateMachines`, and `layout: new Layout({ fit: Fit.Contain })`; size the canvas by CSS and call `resizeDrawingSurfaceToCanvas()` on resize.
- Call `rive.cleanup()` on unmount; in React use `useRive` and let the hook own the lifecycle.
- Preload the `.riv` and the wasm, and self-host the wasm if the CDN is not allowed by your CSP.
- Pause when off-screen (`IntersectionObserver` then `rive.pause()`), and skip autoplay for reduced motion.
- Give the canvas `role="img"` and an `aria-label`, or hide it as decorative.

## Avoid
- Recreating the `Rive` instance on every render: a leak and a flash. Memoize.
- Running many canvas instances at once: each holds a render loop. Share one artboard or pause hidden ones.
- Hard-coding input names scattered through code: centralize them next to the test.
- Large unoptimized embedded images: export with compressed assets.
- Relying on the default wasm CDN in production without a CSP check.

## Review
- [ ] Instance is created once and cleaned up.
- [ ] Input names are asserted by a test.
- [ ] Off-screen and reduced-motion cases pause or skip.
- [ ] Canvas has an accessible name or is hidden.
- [ ] File and wasm sizes are within budget.
