---
name: qwik
title: Qwik
area: web
tags: [qwik, qwik-city, resumability, ssr, signals, typescript]
detect: [dep:@builder.io/qwik, dep:@builder.io/qwik-city]
related: [vitest, playwright, tailwind]
---
Qwik apps: resumable SSR, lazy-loaded closures marked with `$`, signals and `routeLoader$`/`routeAction$` in Qwik City.

## Verify
- `npx tsc --noEmit`: types.
- `npx eslint . --max-warnings 0`: with `eslint-plugin-qwik`, which flags serialization errors.
- `npx vitest run`: unit and component tests with `createDOM`.
- `npm run build`: client, server and type build.

## Test first
Render components with `createDOM` from `@builder.io/qwik/testing` under Vitest.
```tsx
import { createDOM } from "@builder.io/qwik/testing";
import { test, expect } from "vitest";
import { Counter } from "./counter";

test("increments", async () => {
  const { screen, render, userEvent } = await createDOM();
  await render(<Counter />);
  await userEvent("button", "click");
  expect(screen.querySelector("button")!.textContent).toContain("1");
});
```

## Do
- Define components with `component$(() => ...)` and state with `useSignal()` or `useStore()`.
- Wrap handlers and tasks in `$` forms: `onClick$={() => ...}`, `useTask$`, `useVisibleTask$`.
- Load server data with `routeLoader$` and mutate with `routeAction$` plus `zod$` validation.
- Keep captured values in closures serializable: primitives, plain objects, signals, stores.
- Use `useTask$` for isomorphic effects and `track(() => sig.value)` to subscribe.
- Use `server$` for ad hoc RPC to the server, with the same input validation as an action.
- Read secrets through `requestEvent.env`, only inside server functions.

## Avoid
- `useVisibleTask$` for data loading or general effects: it forces eager client JS and defeats resumability. Use `useTask$` or `routeLoader$`.
- Capturing non-serializable values (class instances, functions, DOM nodes) in a `$` closure: build or runtime error. Move them inside, or into `noSerialize`.
- React-style `onClick={...}` without the `$`: it will not be lazy-loaded or may fail. Use `onClick$`.
- Destructuring props or store in the component body: breaks reactivity. Read `props.x` and `store.x` where used.
- Mutating a signal outside a task or handler during render: warnings and loops. Do it in events or tasks.
- Importing server-only code in a component without `server$`/loaders: it can land in the client bundle. Isolate it.
- Trusting `routeAction$` input without `zod$`: unvalidated data. Add a validator.

## Review
- [ ] No `useVisibleTask$` where `useTask$` or a loader works.
- [ ] Every `$` closure captures only serializable values.
- [ ] Actions and `server$` calls validate input and check auth.
- [ ] Props and stores are read lazily, never destructured.
- [ ] ESLint with the Qwik plugin passes.
