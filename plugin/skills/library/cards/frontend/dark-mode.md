---
name: dark-mode
title: Dark mode
area: frontend
tags: [css, theme, dark-mode, color-scheme, tokens]
detect: [dep:next-themes]
related: [css-custom-properties, color-contrast, design-systems, layout-shift]
---
Light, dark and system themes without a flash, with tokens swapped per scope and a persisted user choice.

## Verify
- `npx playwright test`: emulates `colorScheme` and reloads to catch flash and persistence bugs.
- `npx @axe-core/cli http://localhost:3000`: contrast violations in the current theme (run once per theme).
- `npx tsc --noEmit`: theme union types stay consistent.

## Test first
Emulate the OS preference and assert the first paint already matches, with no flash.
```ts
import { test, expect } from '@playwright/test';

test.use({ colorScheme: 'dark' });

test('dark system preference applies before hydration', async ({ page }) => {
  await page.goto('/');
  const theme = await page.evaluate(() => document.documentElement.dataset.theme);
  expect(theme).toBe('dark');
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg).not.toBe('rgb(255, 255, 255)');
});
```

## Do
- Declare `color-scheme: light dark` on `:root` so form controls, scrollbars and canvas follow.
- Define tokens twice: `:root` for light, `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }`, plus `:root[data-theme="dark"]`.
- Run a tiny blocking inline script in `<head>` that reads storage and sets `data-theme` before first paint.
- Store three states: `light`, `dark`, `system`. Listen to `matchMedia('(prefers-color-scheme: dark)')` changes when `system`.
- Set `<meta name="color-scheme" content="light dark">` and a themed `theme-color`.
- Dim or swap images and shadows: elevation in dark mode uses lighter surfaces, not darker shadows.
- Give the toggle an accessible state (`aria-pressed` or a labelled radio group).

## Avoid
- Reading `localStorage` in a post-hydration effect to set the theme: users see a white flash. Use the head script.
- Pure `#000` backgrounds with `#fff` text: halation and harsh contrast. Use near-black and off-white tokens.
- Inverting everything with `filter: invert(1)`: images and brand colors break. Swap tokens.
- Hardcoded colors in components or SVG `fill`: they ignore the theme. Use `currentColor` and tokens.
- Testing only light: contrast failures live in dark. Run axe in both.
- Throwing when storage is blocked: wrap reads in try/catch and fall back to system.

## Review
- [ ] No flash on hard reload in either theme (head script runs first).
- [ ] The system choice follows live OS changes.
- [ ] Every token pair meets contrast in both themes.
- [ ] Form controls and scrollbars match via `color-scheme`.
- [ ] The toggle exposes its current state to assistive tech.
