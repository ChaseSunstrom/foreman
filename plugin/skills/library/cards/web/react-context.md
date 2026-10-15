---
name: react-context
title: React Context
area: web
tags: [react, context, state, rerender, provider, hooks]
detect: []
related: [react, react-memo, zustand, redux-toolkit]
---
React Context: pass slow-changing values through the tree, with split providers and stable values to avoid re-render storms.

## Verify
- `npx tsc --noEmit`: the context type forbids a missing provider.
- `npx eslint .`: hooks rules and exhaustive deps.
- `npx vitest run`: provider and consumer tests.
- `npx vitest run --coverage`: confirms the no-provider error branch is covered (needs a coverage provider installed).

## Test first
Test the consumer inside and outside the provider.
```tsx
import { render, screen } from "@testing-library/react";
import { ThemeProvider, useTheme } from "./theme";

function Probe() { return <p>{useTheme().mode}</p>; }

test("throws outside provider", () => {
  const spy = vi.spyOn(console, "error").mockImplementation(() => {});
  expect(() => render(<Probe />)).toThrow(/ThemeProvider/);
  spy.mockRestore();
});

test("reads value", () => {
  render(<ThemeProvider mode="dark"><Probe /></ThemeProvider>);
  expect(screen.getByText("dark")).toBeInTheDocument();
});
```

## Do
- Create the context with `createContext<T | null>(null)` and export a `useX` hook that throws when the value is null.
- Memoize the provided value with `useMemo` and callbacks with `useCallback` when the provider re-renders for other reasons.
- Split contexts by update frequency: one for state, one for dispatch or actions.
- Put the provider as low in the tree as it can go, and pass `children` through it so children do not re-render with the provider.
- Keep Context for low-frequency data (theme, locale, auth user); use a store library with selectors for hot state.
- With `useReducer`, provide `dispatch` separately because its identity is stable.
- In React 19 the context object can be rendered directly as the provider; check the installed version before using it.

## Avoid
- `value={{ a, b }}` inline: a new object every render re-renders all consumers. Memoize it.
- One giant context for everything: any field change re-renders every consumer. Split it or use a selector store.
- A default value that hides a missing provider: bugs show as silent defaults. Use null and throw.
- Storing fast-changing values (mouse position, input text) in context: use local state or a store with selectors.
- Putting the provider at the app root for state only one subtree uses: move it down.
- Relying on `React.memo` to stop context re-renders: memo does not block context updates. Split the context.

## Review
- [ ] The provided value is stable between unrelated renders.
- [ ] A missing provider throws a clear error.
- [ ] Contexts are split by change frequency and scope.
- [ ] Hot state lives in a store or local state, not context.
- [ ] Tests render consumers with and without the provider.
