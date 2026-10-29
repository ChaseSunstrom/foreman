---
name: art-direction
title: Art Direction
area: ux
tags: [ux, art-direction, visual-language, moodboard, picture-element]
detect: []
related: [brand-identity, image-direction, illustration-systems, look-lab-notebook, typography, color-palettes]
---
Art direction fixes one visual concept (mood, palette, type, imagery, motion) and applies it to every page and breakpoint.

## Verify
- `grep -rn "<picture" src | wc -l`: pages with art-directed crops use `<picture>` with `media` sources.
- `npx playwright screenshot --viewport-size=375,812 http://localhost:3000 /tmp/m.png` and again at 1440,900: compare crops side by side.
- `grep -rhoE "var\(--(color|font|space)[a-z0-9-]*\)" src | sort -u`: the concept uses only the token vocabulary.

## Test first
Different crops per breakpoint are served, not one shrunken image.
```ts
import { test, expect } from '@playwright/test';

test('hero serves a different crop on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/');
  const mobile = await page.locator('picture img').first().evaluate(i => (i as HTMLImageElement).currentSrc);
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.reload();
  const desktop = await page.locator('picture img').first().evaluate(i => (i as HTMLImageElement).currentSrc);
  expect(mobile).not.toEqual(desktop);
});
```

## Do
- Write the concept in one paragraph and three references; add a moodboard of 9-12 images; name what it is not.
- Derive constraints: 4-5 colors, 1-2 typefaces, one imagery treatment (grade, crop, framing), one motion character (snappy 150 ms or slow 400 ms), one grid habit.
- Make a style tile (one screen: type, color, a component, an image) and approve it before building pages.
- Use `<picture>` with `media` queries to give mobile a tighter crop that keeps the subject; `object-position` for small shifts.
- Keep a repeatable composition: where the subject sits, the amount of empty space, the type placement.
- Stay consistent across a campaign, then vary one element at a time.
- Record the concept in the repo (docs/art-direction.md) with tokens, so new pages inherit it.

## Avoid
- Following trends with no tie to the product's voice.
- A new look per page or per designer.
- Mood without constraints: "clean and modern" is not direction.
- Cropping by CSS alone when the subject leaves the frame.

## Review
- [ ] The concept, references and anti-references are written down.
- [ ] A style tile was approved before page work.
- [ ] Mobile and desktop crops are each composed, not scaled.
- [ ] New pages can reuse the tokens and treatment without asking.
