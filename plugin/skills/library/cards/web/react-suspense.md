---
name: react-suspense
title: React Suspense
area: web
tags: [react, suspense, streaming, lazy, transitions, errors]
detect: []
related: [react, react-server-components, nextjs-app-router, tanstack-query]
---
React Suspense: declarative loading states for lazy code and data, streaming boundaries, transitions and error boundaries.

## Verify
- `npx tsc --noEmit`: lazy imports and props type-check.
- `npx eslint .`: hooks and import rules.
- `npx vitest run`: component tests including the pending and error states.
- `npm run build`: lazy chunks split as expected.

## Test first
Assert the fallback shows first, then the content.
```tsx
import { render, screen } from "@testing-library/react";
import { Suspense } from "react";
import { Profile } from "./Profile";

test("shows fallback then profile", async () => {
  render(<Suspense fallback={<p>loading</p>}><Profile id="1" /></Suspense>);
  expect(screen.getByText("loading")).toBeInTheDocument();
  expect(await screen.findByText("Ada")).toBeInTheDocument();
});
```

## Do
- Place a boundary around each independently loading region so fast parts are not blocked by slow ones.
- Use `React.lazy(() => import("./X"))` for route-level or heavy components; define it at module scope.
- Use a Suspense-aware source: a framework loader, a query library with suspense mode, or `use(promise)` with a promise created outside render (cached or passed as a prop).
- Pair every boundary with an error boundary (`react-error-boundary` or a class component) so rejections do not blank the page.
- Wrap slow state updates in `startTransition` or `useTransition` so existing content stays visible instead of reverting to the fallback.
- Use `useDeferredValue` for expensive derived views of fast input.
- Give fallbacks stable dimensions (skeletons) to avoid layout shift.

## Avoid
- Creating the promise inside the suspending component each render: it suspends forever. Create it outside or cache it by key.
- `React.lazy` declared inside a component body: it remounts and resets state. Move to module scope.
- One giant top-level boundary: the whole page flashes to a spinner. Nest boundaries.
- Suspense without an error boundary: a failed fetch throws past the page. Add one per boundary group.
- Fetching in `useEffect` and expecting Suspense to catch it: effects do not suspend. Use a Suspense-capable source.
- Fallbacks that fetch or render heavy content: keep them static and light.

## Review
- [ ] Each boundary has a deliberate fallback and an error boundary above it.
- [ ] Promises are cached or created outside render.
- [ ] Navigation and tab changes use transitions where old content should persist.
- [ ] Lazy components are module-scoped and the chunk split shows in the build.
- [ ] Tests cover pending, success and error.
