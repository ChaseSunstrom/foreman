---
name: zustand
title: Zustand
area: web
tags: [zustand, react, state, store, hooks, typescript]
detect: [dep:zustand]
related: [react, redux-toolkit, tanstack-query, testing-library]
---
Zustand: small hook-based stores; components subscribe to the slice they select.

## Verify
- `npx tsc --noEmit`: store and selector types.
- `npx vitest run`: store and component tests.
- `npx eslint . --max-warnings 0`: hook rules.

## Test first
Test the store through its API, resetting state between tests.
```ts
import { beforeEach, expect, test } from "vitest";
import { useCart } from "./cart";

beforeEach(() => useCart.setState(useCart.getInitialState(), true));

test("add increases the count", () => {
  useCart.getState().add({ id: "a", price: 3 });
  expect(useCart.getState().items).toHaveLength(1);
});
```
Auto-reset every store by mocking `zustand` with a wrapper that calls each store's initial state in `afterEach`.

## Do
- Create stores with `create<State>()((set, get) => ({...}))`; the extra `()` is needed with TypeScript.
- Select narrowly: `useCart(s => s.items.length)`.
- Select several values with `useShallow` (`zustand/react/shallow`) to avoid new-reference re-renders.
- Put actions inside the store and update with `set(state => ({...}))`.
- Compose middleware: `devtools`, `persist` (with `name`, `partialize`, `version`, `migrate`), `immer`.
- Read outside React with `useStore.getState()` and subscribe with `useStore.subscribe`.
- Use a store factory plus context when state must be per request (SSR) or per component tree.
- Keep server data in a query library; zustand holds client state.

## Avoid
- `const { a, b } = useStore()` with no selector: re-renders on any change. Select, or use `useShallow`.
- A selector that returns a new object or array (`s => ({ a: s.a })`): infinite loops or constant re-renders in recent versions. Wrap with `useShallow`.
- A module-level store on the server in Next.js and similar SSR: one shared instance across all users' requests. Create it per request.
- Mutating state directly (`state.items.push`): no update without Immer. Return new values.
- `persist` without `version`/`migrate`: old shapes in localStorage crash after a change. Add a version.
- Persisting secrets or tokens to localStorage via `persist`: readable by any script. Keep them in httpOnly cookies.
- Default import `import create from "zustand"`: removed in newer majors. Use the named `create`.

## Review
- [ ] Every `useStore` call selects, and multi-value selectors use `useShallow`.
- [ ] Stores reset between tests.
- [ ] SSR code builds stores per request.
- [ ] Persisted state is versioned, minimal and holds no secrets.
- [ ] Actions live in the store, not scattered in components.
