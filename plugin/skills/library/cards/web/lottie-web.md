---
name: lottie-web
title: Lottie (lottie-web)
area: web
tags: [lottie, bodymovin, animation, json, after-effects]
detect: [dep:lottie-web, dep:lottie-react, dep:@lottiefiles/dotlottie-web, dep:@lottiefiles/react-lottie-player]
related: [animation, svg-canvas, accessibility, web-performance]
---
Lottie: plays After Effects exports (JSON or .lottie) in the browser; cheap to author, easy to make heavy.

## Verify
- `npx tsc --noEmit`: JSON imports and player props type-check.
- `npx eslint .`: lint, including effect cleanup.
- `npx playwright test --grep lottie`: the animation mounts, plays to `complete`, and the page stays responsive.
- `du -h src/**/*.json public/**/*.lottie`: each file under budget (aim under 100 KB; prefer `.lottie`).

## Test first
Load the animation without a renderer and assert its metadata, so a bad export fails CI.
```ts
import data from "./success.json";

test("success animation is short and small", () => {
  const seconds = (data.op - data.ip) / data.fr;
  expect(seconds).toBeLessThan(3);
  expect(data.layers.length).toBeLessThan(60);
  expect(JSON.stringify(data).length).toBeLessThan(100_000);
});
```

## Do
- Use `lottie.loadAnimation({ container, renderer: "svg", loop, autoplay, path })` and keep the returned handle.
- Call `anim.destroy()` on unmount; in React wrap it in an effect with that cleanup.
- Choose the renderer on purpose: `svg` for crisp small shapes, `canvas` for many layers, avoid `html`.
- Import `lottie-web/build/player/lottie_light` when expressions and effects are not needed, to cut bundle size.
- Lazy-load the player and the JSON with dynamic import, and play only when visible (`IntersectionObserver`).
- Honor reduced motion: `goToAndStop(lastFrame, true)` instead of looping.
- Give meaningful animations an `aria-label` and `role="img"`; hide decorative ones.

## Avoid
- Importing the full player on the critical path for a small icon: use the light build or CSS.
- Loading the JSON from a third-party URL at runtime: availability and CSP risk. Self-host.
- Many simultaneous looping instances: CPU burn. Pause hidden ones.
- Skipping `destroy()`: the SVG and its rAF loop leak.
- Exports with embedded raster images or heavy masks and mattes: large and slow.
- Reading `window` at module scope in SSR.

## Review
- [ ] Animation handle is destroyed on cleanup.
- [ ] Light build or lazy loading keeps the entry bundle small.
- [ ] File size and duration are checked by a test.
- [ ] Reduced motion shows a static frame.
- [ ] Off-screen animations are paused.
