---
name: anchor-positioning
title: CSS Anchor Positioning
area: frontend
tags: [css, anchor-positioning, tooltip, popover, position-try, layout]
detect: []
related: [popover-api, dialogs, focus-management, aria-patterns, css-layout]
---
Attach tooltips, menus and popovers to an anchor in CSS, with automatic flip and a script fallback for older engines.

## Verify
- `npx playwright test --grep anchor`: asserts the popover sits beside its trigger and stays inside the viewport at small sizes.
- `npx playwright test --project=webkit --grep anchor`: confirms the fallback where support is missing.
- `grep -rn "getBoundingClientRect" src | grep -i "tooltip\|menu"`: JavaScript positioning that CSS could replace.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('menu stays inside the viewport near the right edge', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 640 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Options' }).click();
  const box = (await page.getByRole('menu').boundingBox())!;
  expect(box.x).toBeGreaterThanOrEqual(0);
  expect(box.x + box.width).toBeLessThanOrEqual(360);
});
```

## Do
- Declare: `.trigger { anchor-name: --opts; } .menu { position: fixed; position-anchor: --opts; top: anchor(bottom); left: anchor(left); margin-top: 4px; }`.
- Or `position-area: bottom span-right;` for a simpler grid-based placement.
- Flip when cramped: `position-try-fallbacks: flip-block, flip-inline;` or `@position-try --alt { ... }` for custom alternatives.
- Match widths: `min-width: anchor-size(width);`.
- Combine with `popover` so the layer goes to the top layer and handles light dismiss (see popover-api); do not stack z-index.
- Support: Chromium 125+, Safari 26; Firefox is behind. Guard with `@supports (anchor-name: --a)` and fall back to Floating UI or a fixed offset.
- Give tooltips `role="tooltip"` linked by `aria-describedby`; menus follow the menu pattern.
- Use `position-visibility: anchors-visible` to hide when the anchor scrolls away.

## Avoid
- Position math in `scroll` and `resize` handlers when CSS can do it.
- Many elements sharing one `anchor-name`: the last in tree order wins unless you scope with `anchor-scope`.
- Absolute placement inside overflow-clipped parents; use the top layer.
- Relying on it as the sole path for Firefox users without a fallback.
- Tooltips on hover alone: add focus triggers.

## Review
- [ ] The overlay flips or shifts and never leaves the viewport.
- [ ] A fallback positions the overlay where support is missing.
- [ ] Trigger and overlay are linked in the accessibility tree.
- [ ] Keyboard and focus open and close the overlay, not just hover.
