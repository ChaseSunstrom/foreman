---
name: solid-start
title: SolidStart
area: web
tags: [solid-start, solidjs, ssr, server-functions, vinxi, routing]
detect: [dep:@solidjs/start, dep:@solidjs/router, file:app.config.ts]
related: [solid, vitest, playwright]
---
SolidStart: the SolidJS meta-framework with file routes, server functions, route data via query and action, and SSR.

## Verify
- `npx tsc --noEmit`: types for routes, queries and actions.
- `npm run build`: SSR and client builds succeed (script name per package.json).
- `npx vitest run`: component and logic tests.
- `npx playwright test`: end-to-end SSR, hydration and form flows.

## Test first
Test reactive logic with Solid's root helper, and server functions as plain async functions.
```ts
import { createRoot, createSignal, createMemo } from "solid-js";
import { vi } from "vitest";

test("memo tracks the signal", () => {
  createRoot(dispose => {
    const [n, setN] = createSignal(1);
    const double = createMemo(() => n() * 2);
    setN(4);
    expect(double()).toBe(8);
    dispose();
  });
});
```

## Do
- Place routes in `src/routes` (`index.tsx`, `[id].tsx`, `(group)/`); use `A` from the router for links.
- Load data with `query(fn, "key")` and read it with `createAsync(() => getThing(id()))` inside `Suspense`; check the installed version's router docs for exact names.
- Mutate with `action` and the `<form action={...} method="post">` pattern; revalidate affected queries with `revalidate`.
- Mark server code with `"use server"` and validate every argument: server functions are network endpoints.
- Read environment secrets only in server code; client-visible variables use the framework's public prefix (`VITE_`).
- Keep signals and props reactive: read them by calling them inside JSX, memos or effects, and destructure props with `splitProps` or access `props.x`.
- Use `<Show>`, `<For>`, `<Switch>` for control flow.
- Add `ErrorBoundary` and `Suspense` around async regions.

## Avoid
- Destructuring props (`const { name } = props`): reactivity is lost. Use `props.name` or `splitProps`.
- Reading a signal outside a tracking scope (top level of a component) and expecting updates: it runs once. Read it in JSX, `createMemo` or `createEffect`.
- Using React habits: `useState`, array `.map` in JSX for dynamic lists, `key`. Use `createSignal` and `<For>`.
- Unvalidated input in `"use server"` functions: treat as public API, check auth and parse with a schema.
- Touching `window` or `document` during SSR: guard with `isServer` from `solid-js/web` or use `onMount`.
- Secrets in `VITE_`-prefixed variables: they are bundled to the client.

## Review
- [ ] Props and signals are read reactively, with no destructured props.
- [ ] Server functions validate input and check auth.
- [ ] Async regions have Suspense and error boundaries.
- [ ] No browser-only API runs during SSR.
- [ ] Mutations revalidate the queries they affect.
