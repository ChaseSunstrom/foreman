---
name: spline
title: Spline runtime
area: web
tags: [spline, 3d, runtime, webgl, design-tool]
detect: [dep:@splinetool/runtime, dep:@splinetool/react-spline]
related: [three-js, webgl, web-performance, accessibility]
---
Spline: embeds scenes authored in the Spline editor; the scene file is the cost, so budget it like an image hero.

## Verify
- `npx tsc --noEmit`: component props and event types.
- `npx eslint .`: lint.
- `npx playwright test --grep spline`: canvas appears after lazy load and a fallback shows before it.
- `du -h public/*.splinecode`: scene size (aim under 2 MB) and `npx lighthouse` for LCP.

## Test first
Test the fallback and the load path, not the 3D output.
```tsx
import { render, screen } from "@testing-library/react";
import { Hero3D } from "./Hero3D";

test("shows a poster until the scene loads, then calls onLoad", async () => {
  const onLoad = vi.fn();
  render(<Hero3D onLoad={onLoad} />);
  expect(screen.getByRole("img", { name: /product preview/i })).toBeInTheDocument();
});
```

## Do
- Lazy-load: `const Spline = lazy(() => import("@splinetool/react-spline"))` inside `<Suspense fallback={<Poster />}>`, or `next/dynamic` with `ssr: false`.
- Show a static poster image first and swap on `onLoad`; it protects LCP.
- Host the `.splinecode` file yourself with long-cache headers rather than relying on a remote URL.
- Reach objects with `spline.findObjectByName("Cube")` from the `onLoad` argument, and drive them from events (`onSplineMouseDown`).
- Use the vanilla runtime: `new Application(canvas).load(url)` and call `app.dispose()` on cleanup.
- Keep the scene simple: fewer lights, small textures, baked shadows.
- Pause or unmount when off-screen, and use the poster for reduced motion.

## Avoid
- Loading the scene above the fold without a poster: blank hero and bad LCP.
- Importing the runtime in server code: it needs `window` and WebGL.
- Multiple Spline canvases on one page.
- Renaming scene objects in the editor without updating the names used in code.
- Hiding information inside the 3D scene only: give a text equivalent.

## Review
- [ ] Scene is lazy-loaded with a poster fallback.
- [ ] `.splinecode` is self-hosted and size-checked.
- [ ] Object names used in code are listed and checked.
- [ ] Disposed on unmount.
- [ ] Reduced motion and a text alternative exist.
