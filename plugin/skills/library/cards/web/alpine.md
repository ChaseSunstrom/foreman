---
name: alpine
title: Alpine.js
area: web
tags: [alpine, alpinejs, javascript, html, directives, progressive-enhancement]
detect: [dep:alpinejs, dep:@alpinejs/*]
related: [htmx, tailwind, playwright]
---
Alpine.js: small reactive behavior declared in HTML attributes (`x-data`, `x-bind`, `x-on`), no build step required.

## Verify
- `npx playwright test`: behavior in a real browser, the only reliable check for directives.
- `npx eslint . --max-warnings 0`: any JS you extract into `Alpine.data` components.
- `npx prettier --check "**/*.html"`: markup formatting, where configured.

## Test first
Alpine logic lives in markup, so the failing test is a browser test of the visible behavior.
```ts
import { test, expect } from "@playwright/test";

test("dropdown opens and closes on escape", async ({ page }) => {
  await page.goto("/menu.html");
  await page.getByRole("button", { name: "Menu" }).click();
  await expect(page.getByRole("menu")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("menu")).toBeHidden();
});
```
Extract logic to `Alpine.data("name", () => ({...}))` so it can be unit-tested as a plain function.

## Do
- Scope state with `x-data` on the smallest wrapper; share across components with `Alpine.store`.
- Register reusable components with `Alpine.data` inside `document.addEventListener("alpine:init", ...)`.
- Use `x-show` for toggles (keeps DOM) and `x-if` on a `<template>` to add or remove nodes.
- Give `x-for` templates a `:key`.
- Use `x-cloak` plus `[x-cloak] { display: none !important; }` to hide until initialized.
- Use `$refs`, `$dispatch`, `$nextTick` and `@click.outside` instead of manual DOM code.
- Add `aria-expanded`, `aria-controls` and focus handling to toggles and dialogs; `x-trap` needs the Focus plugin.
- Load Alpine with `defer` and a pinned version.

## Avoid
- Putting growing business logic in inline `x-data="{...}"` expressions: untestable. Move it to `Alpine.data`.
- Loading Alpine via an unpinned CDN URL (`@3.x.x` style ranges or `latest`): a surprise upgrade or compromise. Pin the exact version or vendor it.
- Missing `defer` on the script tag: Alpine initializes before the DOM exists.
- `x-html` with user content: XSS. Use `x-text`.
- `x-for` and `x-if` on elements other than `<template>`: ignored or errors. Use a template with a single root child.
- Mutating state on elements outside the `x-data` scope: the expression sees undefined. Use a store or an event.
- Expecting reactivity from replaced objects held outside Alpine: wrap with `Alpine.reactive` or use a store.

## Review
- [ ] State scope is as small as possible and logic is extracted once it grows.
- [ ] Interactive widgets are keyboard and screen-reader usable.
- [ ] Scripts load with `defer` and pinned versions.
- [ ] No `x-html` on untrusted data.
- [ ] A browser test covers each interactive behavior.
