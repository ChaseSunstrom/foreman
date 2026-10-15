---
name: nuxt
title: Nuxt
area: web
tags: [nuxt, vue, ssr, typescript, nitro, fullstack]
detect: [dep:nuxt, file:nuxt.config.*]
related: [vue, pinia, playwright, tailwind, vitest]
---
Nuxt apps: file-based routing, auto-imports, `useFetch`/`useAsyncData` for SSR-safe data, Nitro server routes.

## Verify
- `npx nuxi typecheck`: generated types plus `vue-tsc` over the app.
- `npx nuxi build`: SSR and Nitro build.
- `npx vitest run`: unit tests (with `@nuxt/test-utils` for runtime-aware ones).
- `npx eslint . --max-warnings 0`: lint.

## Test first
Use `@nuxt/test-utils` with the `nuxt` Vitest environment for components needing auto-imports and composables; use `$fetch` against a test server for Nitro routes.
```ts
// server/api/hello.test.ts
import { describe, it, expect } from "vitest";
import { $fetch, setup } from "@nuxt/test-utils/e2e";

describe("api", async () => {
  await setup({});
  it("greets", async () => {
    expect(await $fetch("/api/hello?name=Ada")).toEqual({ msg: "Hello Ada" });
  });
});
```

## Do
- Fetch with `useFetch` or `useAsyncData` with a unique key so data renders on the server and is not refetched on hydration.
- Put API handlers in `server/api/*.ts` with `defineEventHandler`; validate with `getValidatedQuery` or `readValidatedBody`.
- Keep shared state in `useState("key", () => init)` or Pinia, never module-level variables.
- Read config via `useRuntimeConfig()`; secrets stay in the top level of `runtimeConfig`, public values under `runtimeConfig.public`.
- Use `definePageMeta` for layouts and middleware; use route middleware for auth redirects.
- Wrap browser-only code in `onMounted` or `<ClientOnly>`.
- Set per-page SEO with `useSeoMeta`.

## Avoid
- `$fetch` directly in `setup`: it runs twice (server then client) and flashes. Use `useFetch`.
- Module-level `ref`s or stores as shared state: leaked across requests on the server. Use `useState`.
- `window`, `document` or `localStorage` at setup time: crashes SSR. Guard with `import.meta.client` or `onMounted`.
- Secrets in `runtimeConfig.public` or `app.config`: shipped to the browser. Keep them private runtime config.
- Hydration mismatches from `Date.now()`, `Math.random()` or locale formatting in templates: compute once on the server via `useState`.
- Importing from `#imports` by hand everywhere or disabling auto-imports without reason: noise. Rely on auto-imports and types from `.nuxt`.
- Editing `.nuxt/` or `.output/`: regenerated. Change config or source.

## Review
- [ ] Data fetching uses keyed `useFetch`/`useAsyncData`, not setup-time `$fetch`.
- [ ] No request-shared mutable module state.
- [ ] Server routes validate input and check auth.
- [ ] Only intentionally public values live in `runtimeConfig.public`.
- [ ] Browser-only code is client-guarded; no hydration warnings in the console.
