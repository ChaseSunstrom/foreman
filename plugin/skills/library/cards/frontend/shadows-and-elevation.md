---
name: shadows-and-elevation
title: Shadows and Elevation
area: frontend
tags: [css, box-shadow, elevation, depth, design-tokens, dark-mode]
detect: []
related: [design-systems, dark-mode, css-custom-properties, frosted-glass, web-performance]
---
A small elevation scale of layered, low-alpha shadows from one light source, with dark-mode and forced-colors care.

## Verify
- `grep -rn "box-shadow" src | grep -v "var(--"`: ad hoc shadows that should be tokens.
- `npx playwright test --grep elevation`: asserts computed shadows on card and modal match tokens.
- Devtools Rendering panel: paint flashing while animating shows if shadows repaint.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('modal sits higher than cards', async ({ page }) => {
  await page.goto('/');
  const sh = (s: string) => page.locator(s).evaluate(e => getComputedStyle(e).boxShadow);
  expect(await sh('.modal')).not.toBe(await sh('.card'));
  expect(await sh('.card')).not.toBe('none');
});
```

## Do
- Define 4-5 levels as tokens: `--shadow-1` for resting cards through `--shadow-5` for modals.
- Layer two to three shadows per level: a tight contact shadow (y 1px, blur 2px, alpha 0.1) plus wider ambient (y 8px, blur 24px, alpha 0.08). Double offset and blur as each level rises.
- One light source: all shadows fall in the same direction (y positive, x near 0).
- Tint with the surface hue, e.g. `oklch(30% 0.03 260 / 0.15)`, not pure black.
- Dark mode: shadows vanish on dark surfaces; raise elevation by lightening the surface (about +4-8% lightness per level) and keep a faint border.
- Animate elevation by cross-fading the opacity of a pseudo-element holding the larger shadow; this avoids repainting.
- `filter: drop-shadow()` for non-rectangular shapes and transparent PNG or SVG; `box-shadow` follows the box.
- In forced-colors mode shadows disappear; keep an outline or border for separation.

## Avoid
- Heavy black shadows (alpha above 0.3): looks dated and dirty.
- A new shadow value per component.
- Animating `box-shadow` itself on many elements; every frame repaints.
- Elevation as the only separation signal.
- Large blur (above 60 px) on many elements; GPU cost climbs.

## Review
- [ ] All shadows come from the scale; light direction is consistent.
- [ ] Dark mode raises surfaces rather than darkening shadows.
- [ ] Forced-colors users see borders or outlines for separation.
- [ ] Elevation transitions use opacity, not shadow interpolation.
