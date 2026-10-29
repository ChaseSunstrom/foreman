---
name: image-direction
title: Image Direction
area: ux
tags: [ux, photography, imagery, crop, art-direction, alt-text]
detect: []
related: [art-direction, image-optimization, brand-identity, layout-shift, hero-sections, accessibility]
---
Photos chosen and cropped by rule: subject, light and color treatment fixed, focal point kept at every breakpoint.

## Verify
- `identify -format "%f %wx%h\n" public/img/*.jpg`: sizes at least 2x the largest display size.
- `grep -rnE "<img(?![^>]*alt=)" -P src`: images with no `alt`.
- `grep -rLE "width=|height=|aspect-ratio" src --include=*.tsx`: check images lacking intrinsic size.
- `npx playwright test --grep images`: no broken images, no layout shift.

## Test first
Every image has alt, dimensions and a non-empty source.
```ts
import { test, expect } from '@playwright/test';

test('images have alt, size and load', async ({ page }) => {
  await page.goto('/');
  const bad = await page.$$eval('img', imgs => imgs.filter(i =>
    !i.hasAttribute('alt') || !i.getAttribute('width') || !i.getAttribute('height') ||
    !i.complete || i.naturalWidth === 0).map(i => i.src));
  expect(bad).toEqual([]);
});
```

## Do
- Write a shot list: subject, setting, light (natural, soft), color grade, and what to avoid; give every image a purpose.
- Prefer real people, product and places over generic stock; if stock, grade it to match.
- Fix aspect ratios (16:9 hero, 4:3 card, 1:1 avatar) and use `object-fit: cover` with `object-position` on the focal point.
- Use `<picture>` with different crops per breakpoint when the subject would be lost (art direction).
- Leave quiet area (about a third) for overlay text; check contrast of text over the image, 4.5:1, using a scrim `linear-gradient(rgb(0 0 0 / .5), transparent)` if needed.
- Alt text states what matters in context, in under about 125 characters; decorative images use `alt=""`.
- Serve AVIF/WebP with `srcset` and `sizes`; reserve space with `width`/`height`.

## Avoid
- Text baked into photos.
- Auto-cropping that cuts faces or products at narrow widths.
- Photos on a blank "visual" job where the page needs information.
- Lossy re-compression chains and upscaled low-res files.

## Review
- [ ] Style rules (light, grade, subject) are written and images match.
- [ ] Focal point survives at 375 and 1280 px.
- [ ] Every image has an alt decision, dimensions and responsive sources.
- [ ] Text over images passes 4.5:1.
