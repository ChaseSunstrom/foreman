---
name: landing-pages
title: Landing Pages
area: ux
tags: [ux, landing-page, conversion, marketing, performance]
detect: []
related: [hero-sections, calls-to-action, social-proof, web-performance, seo, visual-hierarchy]
---
One page, one goal, one primary action, fast on a mid-range phone, with the offer clear in the first screen.

## Verify
- `npx lighthouse http://localhost:3000 --preset=desktop --only-categories=performance,seo,accessibility`: scores 90+.
- `npx playwright test --grep landing`: checks one h1, one primary CTA, and the form works.
- `npx lhci autorun`: budgets for LCP under 2.5 s, CLS under 0.1, total JS under 170 KB.
- `grep -c "<h1" dist/index.html`: exactly 1.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('above the fold states the offer and one action', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  const h1 = page.locator('h1');
  await expect(h1).toHaveCount(1);
  await expect(h1).toBeInViewport();
  const cta = page.locator('a[data-cta=primary], button[data-cta=primary]').first();
  await expect(cta).toBeInViewport();
  const labels = await page.locator('[data-cta=primary]').allTextContents();
  expect(new Set(labels.map(s => s.trim())).size).toBe(1);
});
```

## Do
- Order sections: hero (promise + CTA), proof, how it works (3 steps), benefits, objections/FAQ, final CTA.
- Write the headline as the outcome for the visitor in under 12 words; the subhead says how, in under 25.
- Repeat the same primary CTA every 1-2 screens, same label and destination.
- Match the ad or link text: message match keeps trust and conversion.
- Remove global navigation or reduce to a logo and a CTA; fewer exits.
- Keep forms to the needed fields; each extra field costs conversion.
- Preload the hero image and size it; defer everything below the fold; no layout shift.
- Add `<title>`, meta description, canonical, Open Graph tags and structured data where relevant.
- Track the CTA click and form submit as events, with consent.

## Avoid
- Several competing offers or CTAs with different labels.
- Auto-playing video with sound, carousels that hide the offer, cookie walls over the hero.
- Stock-photo vagueness and jargon headlines.
- Claims without evidence.

## Review
- [ ] A new visitor can state the offer and the action after 5 seconds.
- [ ] One goal, one repeated primary CTA, consistent label.
- [ ] LCP, CLS and JS budgets are met on a throttled mobile profile.
- [ ] Message matches the traffic source; analytics events fire.
