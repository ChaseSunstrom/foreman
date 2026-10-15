---
name: hydration
title: Hydration
area: frontend
tags: [ssr, hydration, react, streaming, performance]
detect: [dep:react-dom]
related: [code-splitting, error-boundaries, layout-shift, web-performance]
---
Server HTML and the first client render must match; keep browser-only values out of the initial render.

## Verify
- `npx playwright test`: fails on console errors or warnings that mention hydration.
- `npx tsc --noEmit`: types for server and client entry points.
- `npx vitest run`: component tests render under a server renderer and then hydrate.

## Test first
Fail the test on any hydration warning.
```ts
import { test, expect } from '@playwright/test';

test('no hydration mismatch on load', async ({ page }) => {
  const bad: string[] = [];
  page.on('console', m => {
    if (['error', 'warning'].includes(m.type()) && /hydrat|did not match/i.test(m.text())) bad.push(m.text());
  });
  page.on('pageerror', e => bad.push(String(e)));
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  expect(bad).toEqual([]);
});
```

## Do
- Render identical markup on server and first client pass; read `window`, `localStorage`, `Date.now()`, `Math.random()` only in effects.
- For client-only values, render a stable placeholder first, then set state in `useEffect`.
- Generate ids with `useId`, never `Math.random()`.
- Format dates and numbers with an explicit locale and time zone so server and client agree.
- Use `suppressHydrationWarning` only on a single leaf that legitimately differs (a timestamp), not on containers.
- Gate client-only widgets behind a `mounted` flag or a dynamic import with SSR disabled.
- Stream with Suspense boundaries so slow data does not block the shell; keep each boundary sized.
- Make interactive controls work before hydration where possible (real `<form>` and `<a>`).

## Avoid
- `typeof window !== 'undefined'` branches inside render: server and client output differ. Move to an effect.
- Invalid HTML nesting (`<div>` in `<p>`, `<a>` in `<a>`, `<tr>` outside `<tbody>`): the browser repairs it and the tree mismatches. Fix the markup.
- Rendering the current time or a random value in markup: mismatch every load. Fill it after mount.
- Theme or auth state read from storage during render: flash and mismatch. Use a head script and cookies on the server.
- Hydrating a huge page at once: long main-thread task. Split with lazy islands or boundaries.
- Swallowing the warning with a blanket `suppressHydrationWarning`: hides real bugs.

## Review
- [ ] Console is clean of hydration warnings on key pages.
- [ ] No browser-only API is called during render.
- [ ] Ids come from `useId`; dates and numbers carry explicit locale.
- [ ] HTML nesting is valid, checked by the browser, not just the linter.
- [ ] Forms and links work before JS loads where it matters.
