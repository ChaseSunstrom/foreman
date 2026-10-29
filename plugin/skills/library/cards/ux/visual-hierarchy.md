---
name: visual-hierarchy
title: Visual Hierarchy
area: ux
tags: [ux, visual-design, hierarchy, layout, contrast]
detect: []
related: [typography, spacing-scales, gestalt-principles, color-contrast, landing-pages]
---
One primary thing per screen, found in a 5-second look: size, weight, contrast and space rank the rest.

## Verify
- `npx playwright screenshot --viewport-size=1280,800 http://localhost:3000 /tmp/h.png`, then blur it (`convert /tmp/h.png -blur 0x8 /tmp/h-blur.png`): the primary action must still stand out.
- `grep -c "btn-primary\|variant=\"primary\"" src/pages/*`: one primary button per view.
- Squint test: ask someone to name the page's purpose after 5 seconds.

## Test first
Assert one primary action per view and a strict heading order.
```ts
import { test, expect } from '@playwright/test';

test('one primary action, h1 first', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('[data-variant=primary]:visible')).toHaveCount(1);
  const levels = await page.$$eval('h1,h2,h3,h4', els => els.map(e => +e.tagName[1]));
  expect(levels[0]).toBe(1);
  levels.forEach((l, i) => i && expect(l - levels[i - 1]).toBeLessThanOrEqual(1));
});
```

## Do
- Rank content in 3 levels: primary (one), secondary (a few), tertiary (the rest). Spend emphasis on the first only.
- Differ levels by at least 1.25x in size or 200 in font weight; a 2px difference reads as a mistake.
- Use whitespace to group and isolate: space around the primary element beats a bigger font.
- Make the primary action the highest-contrast filled element; secondary actions outlined or text-only.
- Follow reading patterns: F-shape for text pages, Z-shape for sparse pages; put the anchor top-left (LTR).
- Mute the supporting text to a lower contrast (still 4.5:1) instead of shrinking it below 14px.

## Avoid
- Two competing focal points (two filled buttons, two hero images): users stall.
- Emphasis by bold, color, size and an icon all at once: when all shout, none lead.
- Skipping heading levels to get a size: style with CSS, keep the outline.
- Low-contrast text as the only way to demote: fails accessibility.

## Review
- [ ] A person names the page's main action within 5 seconds of seeing a blurred screenshot.
- [ ] One primary button per view; secondary and tertiary styles are visibly weaker.
- [ ] Heading levels descend without gaps and match visual size order.
- [ ] Demoted text still meets 4.5:1 contrast.
