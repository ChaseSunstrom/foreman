---
name: nextjs-caching
title: Next.js caching
area: web
tags: [nextjs, cache, revalidate, isr, fetch, dynamic]
detect: [file:next.config.js, file:next.config.mjs, file:next.config.ts]
related: [nextjs-app-router, react-server-components, nextjs-middleware, nextjs]
---
Next.js caching layers: fetch and data cache, full-route cache, router cache, and revalidation by path or tag.

## Verify
- `npx next build`: the route table marks static, dynamic and ISR routes, so check each page is what you intend.
- `npx next start`: serve the production build; caching does not behave like `next dev`.
- `curl -sI http://localhost:3000/PATH`: inspect `x-nextjs-cache` and `cache-control` on the running production server.
- `npx tsc --noEmit`: route segment config exports type-check.

## Test first
Cache bugs show up in production mode, so the first failing check is a script against `next start`.
```ts
// e2e/cache.spec.ts (Playwright)
import { test, expect } from "@playwright/test";

test("post list updates after create", async ({ page }) => {
  await page.goto("/posts");
  await page.getByRole("button", { name: "New" }).click();
  await page.getByLabel("Title").fill("fresh");
  await page.getByRole("button", { name: "Save" }).click();
  await page.goto("/posts");
  await expect(page.getByText("fresh")).toBeVisible();
});
```

## Do
- Decide per route: static, time-based (`export const revalidate = N`), or dynamic (`export const dynamic = "force-dynamic"`).
- Tag data (`fetch(url, { next: { tags: ["posts"] } })`) and call `revalidateTag("posts")` or `revalidatePath("/posts")` from the mutation.
- For non-fetch data (ORM, SDK) wrap the reader in `unstable_cache` with explicit keys and tags, or the caching primitive the installed version documents.
- Set `cache: "no-store"` on fetches that must be fresh per request.
- Read the release notes for the installed version: fetch defaults changed between major versions.
- Keep per-user data out of cached shared output: read cookies in a dynamic segment.

## Avoid
- Assuming `fetch` is cached (or uncached) by default: the default differs by major version. Set `cache` or `next.revalidate` explicitly.
- Testing with `next dev`: it skips most caches. Use `build` then `start`.
- Mutating data without revalidating: users see stale lists. Call `revalidatePath` or `revalidateTag` in the action.
- Caching a response that depends on cookies or auth headers: one user's data is served to others. Mark the route dynamic.
- Calling `revalidatePath` during render: it is for actions and route handlers only.
- Forgetting the client router cache: after a mutation call `router.refresh()` or revalidate on the server.

## Review
- [ ] Each data read has an explicit cache or revalidate policy.
- [ ] Every mutation revalidates the paths or tags it affects.
- [ ] No per-user data sits in a shared cached route.
- [ ] Tags are named constants, not scattered string literals.
- [ ] Behavior was checked on a production build, not dev.
