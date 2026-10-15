---
name: react
title: React
area: web
tags: [react, javascript, typescript, ui, hooks, components]
detect: [dep:react, dep:react-dom]
related: [testing-library, nextjs, react-router, redux-toolkit, zustand, tanstack-query, react-hook-form]
---
React function components with hooks: state is derived, effects are for syncing with the outside world.

## Verify
- `npx tsc --noEmit`: props and hook types compile.
- `npx eslint . --max-warnings 0`: includes `react-hooks/rules-of-hooks` and `exhaustive-deps`.
- `npx vitest run` (or `npx jest`): component tests pass.
- `npm run build`: production bundle builds with no dev-only warnings.

## Test first
Test through the DOM like a user, with Testing Library, in `*.test.tsx` beside the component.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

test("increments on click", async () => {
  render(<Counter />);
  await userEvent.click(screen.getByRole("button", { name: /add/i }));
  expect(screen.getByText("Count: 1")).toBeInTheDocument();
});
```

## Do
- Derive values during render (`const total = items.reduce(...)`) instead of copying them into state.
- Give list items a stable `key` from the data id.
- Use `useEffect` only to sync with external systems (subscriptions, timers, non-React widgets) and return a cleanup.
- Lift state to the nearest common parent; use context for truly app-wide values only.
- Update state from the previous value with the functional form: `setN(n => n + 1)`.
- Use `useRef` for DOM nodes and mutable values that must not trigger renders.
- Fetch with a data library (TanStack Query, framework loaders), not hand-rolled `useEffect` plus `useState`.
- Call `root.render` via `createRoot` from `react-dom/client`.

## Avoid
- Array index as `key` on reorderable lists: state sticks to the wrong row. Use the item id.
- `useEffect` that sets state from props or other state: an extra render and drift. Compute it in render or use `useMemo`.
- Missing or suppressed `exhaustive-deps`: stale closures. Fix the dependency or move the logic out of the effect.
- Mutating state (`arr.push`, `obj.x = 1`) then `setState`: no re-render. Copy with spread, `map` or `filter`.
- `ReactDOM.render` or `react-test-renderer` in new code: legacy. Use `createRoot` and Testing Library.
- Defining a component inside another component: it remounts every render and loses state. Hoist it.
- Fetching in an effect with no cancel: out-of-order responses win. Use an `AbortController` or a query library.
- `dangerouslySetInnerHTML` with unsanitized input: XSS. Sanitize or render as text.

## Review
- [ ] No effect exists that could be a derived value or an event handler.
- [ ] Every effect with a subscription or timer returns a cleanup.
- [ ] Lists use stable keys and no component is declared inside a render body.
- [ ] Interactive elements are real `button` or `a` elements with accessible names.
- [ ] Tests query by role or label, not by class or test-id first.
