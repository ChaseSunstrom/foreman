---
name: hero-sections
title: Hero Sections
area: ux
tags: [ux, hero, above-the-fold, lcp, headline, imagery]
detect: []
related: [landing-pages, calls-to-action, image-direction, visual-hierarchy, layout-shift, image-optimization]
---
A hero states the promise, shows the product, and offers one action, within the first viewport and under 2.5 s LCP.

## Verify
- `npx lighthouse http://localhost:3000 --only-categories=performance --view=false --output=json | jq '.audits["largest-contentful-paint"].displayValue'`: under 2.5 s.
- `npx playwright test --grep hero`: headline, CTA and image in the first 667 px.
- `grep -n 'loading="lazy"' src/components/Hero*`: a lazy-loaded hero image delays LCP; there should be no match.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('hero fits the first mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  const hero = page.locator('[data-hero]');
  await expect(hero.locator('h1')).toBeInViewport({ ratio: 1 });
  await expect(hero.locator('[data-cta=primary]')).toBeInViewport({ ratio: 1 });
  const img = hero.locator('img').first();
  await expect(img).not.toHaveAttribute('loading', 'lazy');
  await expect(img).toHaveAttribute('fetchpriority', 'high');
});
```

## Do
- Headline: 6-12 words, outcome-first, size from the top of the type scale (clamp 2.5-4.5rem); subhead 1-2 lines at 1.25rem.
- Show the product or a real result, not an abstract shape; use a screenshot, short loop video or a photo with a person using it.
- One primary CTA plus at most one quiet secondary link.
- Make the hero image the LCP element: `fetchpriority="high"`, no lazy, explicit `width`/`height`, AVIF/WebP, under about 150 KB on mobile.
- Use `min-height: min(90svh, 56rem)`, not `100vh`, so mobile browser bars don't clip it; leave a hint of the next section.
- Keep text contrast 4.5:1 over images with a scrim, and stay inside a 65ch headline width.
- Videos: muted, `playsinline`, a poster, paused under `prefers-reduced-motion`, with a pause control.

## Avoid
- Sliders or carousels: the first slide is the only one read.
- Headline as the company name or a slogan with no meaning.
- A giant image pushing the CTA below the fold on mobile.
- Parallax and heavy WebGL that block the main thread on first paint.

## Review
- [ ] Headline, CTA and visual are in the first viewport at 375x667 and 1280x720.
- [ ] LCP is the hero asset and is under 2.5 s on throttled mobile.
- [ ] Text contrast over imagery passes.
- [ ] Motion respects reduced-motion and can be paused.
