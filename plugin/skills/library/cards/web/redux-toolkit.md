---
name: redux-toolkit
title: Redux Toolkit
area: web
tags: [redux, redux-toolkit, state, react, rtk-query, typescript]
detect: [dep:@reduxjs/toolkit]
related: [react, zustand, tanstack-query, testing-library, msw]
---
Redux Toolkit: `configureStore`, `createSlice` with Immer, `createAsyncThunk` and RTK Query for server data.

## Verify
- `npx tsc --noEmit`: `RootState`, `AppDispatch` and selector types.
- `npx vitest run`: reducer, thunk and component tests.
- `npx eslint . --max-warnings 0`: lint.

## Test first
Test reducers as pure functions; test connected components with a real store built by a helper.
```ts
import { expect, test } from "vitest";
import cart, { added } from "./cartSlice";

test("added increments the quantity of an existing line", () => {
  const before = { lines: [{ id: "a", qty: 1 }] };
  const after = cart(before, added({ id: "a" }));
  expect(after.lines[0].qty).toBe(2);
});
```
For components, make `renderWithStore(ui, { preloadedState })` that wraps `<Provider store={setupStore(preloadedState)}>`.

## Do
- Create one store with `configureStore({ reducer })`, export `type RootState = ReturnType<typeof store.getState>` and `AppDispatch`.
- Define typed hooks (`useAppDispatch`, `useAppSelector`) once with `.withTypes<...>()`.
- Write reducers with `createSlice`; mutate the draft or return a new value, never both.
- Model events, not setters: `orderPlaced`, not `setOrder`.
- Use RTK Query (`createApi`) for server state, with `providesTags`/`invalidatesTags` for cache refresh.
- Memoize derived data with `createSelector`; select the smallest slice a component needs.
- Keep state serializable; store ids and plain data.
- Create a fresh store per test through a `setupStore` factory.

## Avoid
- Hand-written `createStore`, switch reducers, action-type constants: legacy. Use `configureStore` and `createSlice`.
- Mutating state outside a slice reducer: Immer is not active there, and the serializability middleware warns. Dispatch actions.
- Mutating the draft and also returning a new object from a case reducer: throws. Do one.
- Putting server cache in slices with manual loading flags: stale, duplicated. Use RTK Query or TanStack Query.
- `useSelector(state => state.a.items.filter(...))`: new array each time, re-renders every dispatch. Use `createSelector`.
- Non-serializable values (Dates, class instances, promises) in state or actions: warnings and broken persistence. Convert to ISO strings and ids.
- A single global store module imported in tests: state leaks between tests. Use the factory.

## Review
- [ ] Slices model events and use immutable-safe updates only.
- [ ] Server data is fetched via RTK Query with tags, not hand-rolled thunks.
- [ ] Selectors are memoized and narrow.
- [ ] Typed hooks are used instead of raw `useSelector`/`useDispatch`.
- [ ] Each test builds its own store.
