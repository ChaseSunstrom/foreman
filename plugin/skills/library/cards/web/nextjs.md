---
name: nextjs
title: Next.js
area: web
tags: [nextjs, react, ssr, app-router, server-components, typescript]
detect: [dep:next, file:next.config.*]
related: [react, testing-library, playwright, tailwind, tanstack-query, msw]
---
Next.js App Router apps: server components by default, client components opt-in, route handlers and server actions on the server.

## Verify
- `npx tsc --noEmit`: types, including route props.
- `npx next lint`: Next ESLint rules (or `npx eslint .` where lint is configured directly).
- `npx next build`: catches server/client boundary errors, bad static params and type errors.
- `npx vitest run`: unit and component tests; add `npx playwright test` for pages.

## Test first
Unit-test pure logic and client components with Vitest and Testing Library. Cover async server components and routing with Playwright against `next dev` or a build.
```ts
// e2e/home.spec.ts
import { test, expect } from "@playwright/test";

test("home lists posts", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Posts" })).toBeVisible();
});
```

## Do
- Keep components server by default; add `"use client"` only to the leaf that needs state, effects or browser APIs.
- Fetch in server components with `async`/`await`; pass plain serializable props to client components.
- Mutate with server actions (`"use server"`) and call `revalidatePath` or `revalidateTag` afterwards.
- Validate every server action and route handler input (Zod or similar) and re-check auth inside it.
- Use `next/image`, `next/link` and `next/font`.
- Read secrets from `process.env`; expose to the browser only through `NEXT_PUBLIC_` names.
- Add `loading.tsx` and `error.tsx` per route segment.
- Set caching explicitly (`fetch` options, `export const revalidate`, `dynamic`) rather than relying on defaults you have not checked.

## Avoid
- `"use client"` at the top of a layout: the whole subtree ships as client JS. Push it to leaves.
- Importing a server-only module (db, secrets) into a client component: leaks or breaks the build. Add `import "server-only"` to those modules.
- `pages/` router APIs (`getServerSideProps`, `next/router`) in an `app/` route: use async components and `next/navigation`.
- Trusting server action arguments or auth done only in middleware: actions are public POST endpoints. Check the session in the action.
- Secrets in `NEXT_PUBLIC_*`: they are inlined into the bundle. Keep them server-side.
- Reading `cookies()`, `headers()` or `searchParams` in a route you expect static: it becomes dynamic. Check the build output table.
- Passing functions or class instances from server to client components: not serializable. Pass data, or use a server action.

## Review
- [ ] Each `"use client"` file needs it, and sits as low in the tree as possible.
- [ ] Server actions and route handlers validate input and authorize the caller.
- [ ] Cache and revalidation behavior is chosen deliberately for every data fetch.
- [ ] No secrets in client bundles or `NEXT_PUBLIC_` variables.
- [ ] `next build` output shows the expected static or dynamic mode per route.

## Notes
Dynamic APIs such as `params`, `cookies()` and `headers()` are async in recent major versions; check the installed version's docs.
