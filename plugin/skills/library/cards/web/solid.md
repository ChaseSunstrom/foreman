---
name: solid
title: SolidJS
area: web
tags: [solid, solidjs, signals, jsx, ui, reactivity]
detect: [dep:solid-js]
related: [vitest, testing-library, tailwind, playwright]
---
SolidJS: components run once, fine-grained signals update the DOM directly, so reactivity lives in reads inside tracking scopes.

## Verify
- `npx tsc --noEmit`: JSX types (`jsxImportSource: "solid-js"`).
- `npx eslint . --max-warnings 0`: with `eslint-plugin-solid`.
- `npx vitest run`: component tests via `@solidjs/testing-library`.
- `npm run build`: production build.

## Test first
Render with `@solidjs/testing-library`; Vitest needs `vite-plugin-solid` and a `jsdom` environment.
```tsx
import { render, screen, fireEvent } from "@solidjs/testing-library";
import { expect, test } from "vitest";
import { Counter } from "./Counter";

test("increments", async () => {
  render(() => <Counter />);
  await fireEvent.click(screen.getByRole("button"));
  expect(screen.getByText("1")).toBeInTheDocument();
});
```

## Do
- Use `createSignal` (read with `count()`), `createMemo` for derived values, `createEffect` for side effects.
- Use `<Show when={...}>`, `<For each={...}>` and `<Switch>/<Match>` for control flow.
- Keep props reactive: read `props.x` where used, or use `splitProps` and `mergeProps`.
- Use stores (`createStore`, `produce`) for nested state, and `createResource` for async data.
- Use `onCleanup` inside effects and components for teardown.
- Use `class` and `onClick`; Solid uses native DOM names, not React's.
- Wrap batched writes in `batch(() => ...)` when several signals change together.

## Avoid
- Destructuring props (`function C({ name })`): reactivity lost, value frozen. Use `props.name` or `splitProps`.
- Reading a signal outside a tracking scope (top of the component body) and expecting updates: it runs once. Read inside JSX, `createMemo` or `createEffect`.
- React idioms: `useState`, `useEffect`, dependency arrays, `key`, re-render thinking. Signals and `<For>` replace them.
- `array.map` in JSX for dynamic lists: recreates all nodes. Use `<For>`.
- Early `return` or `if` for conditional UI in a component body: runs once. Use `<Show>`.
- Passing `count` instead of `count()`: passes the getter, not the value. Call it where the value is needed.
- Mutating store objects directly: use the setter or `produce`.

## Review
- [ ] No destructured props and no top-level signal reads that should be reactive.
- [ ] Lists and conditionals use `For`, `Show`, `Switch`.
- [ ] Effects clean up with `onCleanup`.
- [ ] Async data goes through `createResource` with `Suspense` or an error boundary.
- [ ] `eslint-plugin-solid` reports nothing.
