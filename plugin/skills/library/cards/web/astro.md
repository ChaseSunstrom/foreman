---
name: astro
title: Astro
area: web
tags: [astro, static-site, islands, content, ssg, typescript]
detect: [dep:astro, file:astro.config.*, ext:.astro]
related: [tailwind, playwright, vitest, svelte, react, vue]
---
Astro sites: `.astro` pages render to HTML on the server, interactive UI ships only as hydrated islands.

## Verify
- `npx astro check`: types in `.astro` files, content collections and props.
- `npx astro build`: static or SSR build; fails on bad content schema.
- `npx vitest run`: unit tests (Astro's `getViteConfig` helper for Vitest).
- `npx playwright test`: pages against `astro preview`.

## Test first
Test pure logic in Vitest; test pages against the built output with Playwright.
```ts
// tests/home.spec.ts
import { test, expect } from "@playwright/test";

test("home has a title and nav", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/My Site/);
  await expect(page.getByRole("navigation")).toBeVisible();
});
```

## Do
- Write pages and layouts in `.astro`; the frontmatter fence (`---`) runs at build or request time on the server only.
- Define content with collections in `src/content.config.ts` using Zod schemas, and read via `getCollection`/`getEntry`.
- Add `client:*` directives (`client:visible`, `client:idle`, `client:load`) only to components that need interactivity, choosing the laziest that works.
- Type props with `interface Props` and read `Astro.props`.
- Use `astro:assets` `<Image />` for optimized images.
- Set `output: "server"` plus an adapter only for on-demand routes; add `export const prerender = false` per route in hybrid setups.
- Read secrets from `import.meta.env` or `astro:env`, public ones with `PUBLIC_`.

## Avoid
- `client:load` on everything: ships the whole framework. Pick `visible` or `idle`, or no directive for static markup.
- Using `window` or `document` in `.astro` frontmatter: it runs on the server. Put it in a `<script>` tag or an island.
- Hooks or event handlers in `.astro` markup: they do nothing. Use a framework island or a `<script>`.
- Untyped content (no collection schema): bad frontmatter ships silently. Add a Zod schema.
- Server-only secrets read in a client island: undefined, or leaked if prefixed `PUBLIC_`. Read them in the server frontmatter.
- Old content collection API (`src/content/config.ts` without loaders, `entry.render()`) when the installed version uses `glob` loaders and `render(entry)`: check the installed docs.
- SSR routes without an adapter: build error. Add the adapter for the host.

## Review
- [ ] Each `client:` directive is justified and as lazy as possible.
- [ ] Content schemas validate all frontmatter.
- [ ] No browser globals run in server frontmatter.
- [ ] Images use `astro:assets` with width and height or `inferSize`.
- [ ] `astro check` and `astro build` both pass.
