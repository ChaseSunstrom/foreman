---
name: react-memo
title: React memoization
area: web
tags: [react, memo, usememo, usecallback, performance, compiler]
detect: [dep:babel-plugin-react-compiler, dep:eslint-plugin-react-compiler, dep:react-compiler-runtime]
related: [react, react-context, zustand]
---
React memoization: measure first, then use memo, useMemo and useCallback only where equality actually saves renders.

## Verify
- `npx eslint .`: the `react-hooks/exhaustive-deps` rule catches stale closures in memoized code.
- `npx tsc --noEmit`: types.
- `npx vitest run`: behavior tests; a render-count assertion for the hot component.
- `npm run build`: production build for profiling with the React DevTools Profiler.

## Test first
Make the performance claim a failing test with a render counter.
```tsx
import { render } from "@testing-library/react";
import { vi } from "vitest";
import { Row } from "./Row";

test("Row does not re-render when parent state changes", () => {
  const onRender = vi.fn();
  const { rerender } = render(<Row item={{ id: 1 }} onRender={onRender} />);
  rerender(<Row item={{ id: 1 }} onRender={onRender} />);
  expect(onRender).toHaveBeenCalledTimes(1);
});
```

## Do
- Profile first (DevTools Profiler, "why did this render"); memoize only a measured hot path.
- Wrap a pure child in `React.memo` only when its parent re-renders often and the child's render is costly.
- Give memoized children stable props: `useMemo` for objects and arrays, `useCallback` for functions.
- Use `useMemo` for genuinely expensive derivations (large sorts, filters over thousands of rows), not for cheap math.
- Move state down or lift content up (pass `children`) before reaching for memo: it removes the re-render without equality checks.
- Use a stable `key` and virtualize long lists.
- If the React Compiler is enabled, delete manual memo you added only for speed and rely on its lint rules.

## Avoid
- `memo` on a component that receives inline objects or functions: props change every render, so memo does nothing. Stabilize props or drop it.
- `useCallback` on every handler "just in case": it adds cost and noise. Use it when the function is a memoized child's prop or an effect dependency.
- Wrong or missing dependency arrays: stale values. Follow the lint rule, do not silence it.
- `useMemo` as a semantic guarantee: React may discard the cache. Do not rely on it for correctness.
- Custom `memo` comparators that skip props: they hide updates. Compare all props that matter.
- Mutating state objects then memoizing: reference equality never sees the change. Create new objects.

## Review
- [ ] Each memo has a profile or render-count proof behind it.
- [ ] Dependency arrays are complete and lint-clean.
- [ ] Props passed to memoized children are referentially stable.
- [ ] State placement was tried before memoization.
- [ ] No memo wraps cheap leaf components for no measured gain.
