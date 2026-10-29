---
name: view-transitions
title: View Transitions
area: frontend
tags: [css, view-transitions, navigation, motion, spa]
detect: []
related: [animation, scroll-driven-animations, accessibility, focus-management, layout-shift]
---
Animate state and page changes with document.startViewTransition and view-transition-name, falling back to an instant update.

## Verify
- `npx playwright test --grep transition`: asserts the final DOM state with and without `startViewTransition` stubbed out.
- `grep -rn "view-transition-name" src`: each name must be unique on the page at capture time.
- Devtools Animations panel: pause the pseudo-elements `::view-transition-old(*)` and `::view-transition-new(*)` to inspect them.

## Test first
The update must happen even when the API is missing; test the fallback.
```ts
import { test, expect } from '@playwright/test';

test('list reorders when startViewTransition is absent', async ({ page }) => {
  await page.addInitScript(() => { (document as any).startViewTransition = undefined; });
  await page.goto('/');
  await page.getByRole('button', { name: 'Sort' }).click();
  await expect(page.getByRole('listitem').first()).toHaveText('Apple');
});
```

## Do
- Wrap the DOM change: `const run = () => update(); document.startViewTransition ? document.startViewTransition(run) : run();`.
- Give shared elements a unique `view-transition-name` (set it per item, e.g. `style="view-transition-name: card-42"`), and clear it after.
- Cross-document: add `@view-transition { navigation: auto; }` on both pages (same origin); it is supported in Chromium and Safari 18.2+.
- Tune with `::view-transition-group(*) { animation-duration: 250ms; }`; keep total time under 400 ms.
- Respect `@media (prefers-reduced-motion: reduce)`: set the pseudo-element animation to `none`.
- Await `transition.finished` before moving focus, and move focus to the new view's heading.
- Use `view-transition-class` to style many items with one rule.

## Avoid
- Duplicate `view-transition-name` values: the transition aborts and skips.
- Running during input-heavy work: the page snapshots freeze interaction until the transition begins.
- Names on hundreds of elements: each is a captured layer, costing memory and frame time.
- Assuming support: Firefox lacked same-document support for long; always have the fallback.
- Long transitions that delay the content users came for.

## Review
- [ ] Pages work identically when the API is absent or the transition is skipped.
- [ ] Reduced-motion users see a cut or a simple fade.
- [ ] Focus and the document title update with the view; screen readers announce the change.
- [ ] No two elements share a `view-transition-name` at the same time.
