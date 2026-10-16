---
name: sveltekit
title: SvelteKit
area: web
tags: [sveltekit, svelte, ssr, routing, forms, typescript]
detect: [dep:@sveltejs/kit, dep:@sveltejs/adapter-*, file:svelte.config.*]
related: [svelte, playwright, vitest, tailwind]
---
SvelteKit apps: file-based routes, `load` functions, form actions, hooks, adapters.

## Verify
- `npx svelte-kit sync && npx svelte-check`: generated route types and component types.
- `npx vitest run`: unit and component tests.
- `npm run build`: runs the adapter and prerender; catches bad `load` and prerender errors.
- `npx playwright test`: end-to-end routes and form actions.

## Test first
Test routes end to end with Playwright against the preview server; unit-test pure `load` helpers.
```ts
// tests/login.test.ts
import { expect, test } from "@playwright/test";

test("bad password shows an error", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Password").fill("wrong");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page.getByText("Invalid credentials")).toBeVisible();
});
```

## Do
- Load data in `+page.server.ts` (`load`) for private data and in `+page.ts` only for public, isomorphic data.
- Handle mutations with form actions (`export const actions`) and `use:enhance` for progressive enhancement.
- Return `fail(400, { errors })` from actions for validation errors; `redirect(303, "/")` after success.
- Authenticate in `hooks.server.ts` `handle`, put the user in `event.locals`, and type it in `app.d.ts`.
- Use the `event.fetch` passed to `load`, not global `fetch`, so cookies and relative URLs work in SSR.
- Read private env from `$env/static/private` or `$env/dynamic/private`; public from `$env/static/public` (`PUBLIC_` prefix).
- Set the right adapter in `svelte.config.js` for the deploy target.

## Avoid
- Global `fetch` in `load`: no cookie forwarding and a console warning. Use the provided `fetch`.
- Importing `$env/*/private` or `$lib/server` code from a client module: build error by design. Move the call to a server `load` or action.
- Module-level mutable state on the server (a user variable): shared across requests, a data leak. Use `locals` or `load` returns.
- Returning non-serializable data (class instances, functions) from server `load`: fails. Return plain data.
- Authorizing only in layout `load`: child `+server.ts` routes and actions still run. Check in `hooks` or each handler.
- Forms with `fetch` instead of actions: no works-without-JS, no CSRF origin check benefit. Use actions plus `enhance`.
- `export const ssr = false` as a default workaround: gives up SSR for the whole route. Fix the browser-only code with `browser` from `$app/environment` or `onMount`.

## Review
- [ ] Private data comes only from `+page.server` or `+layout.server` loads.
- [ ] Every action validates input and returns `fail` on error.
- [ ] Auth is enforced in `handle` or in every server endpoint.
- [ ] No secrets or server-only imports reach client code.
- [ ] The adapter matches the deploy target and `build` succeeds.
