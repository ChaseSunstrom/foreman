---
name: social-proof
title: Social Proof
area: ux
tags: [ux, testimonials, reviews, trust, logos, structured-data]
detect: []
related: [landing-pages, calls-to-action, hero-sections, seo, image-optimization, accessibility]
---
Specific, attributable evidence placed next to the decision it supports: named quotes, numbers, logos, ratings.

## Verify
- `npx playwright test --grep proof`: each testimonial has a name, role and photo or logo.
- `grep -rniE "john doe|lorem|\bTBD\b" src content`: placeholder people.
- `npx structured-data-testing-tool -u http://localhost:3000`: validates Review or AggregateRating markup.
- `identify -format "%f %wx%h\n" public/logos/*`: logos uniformly sized.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('testimonials are attributable', async ({ page }) => {
  await page.goto('/');
  const quotes = page.locator('figure.testimonial');
  expect(await quotes.count()).toBeGreaterThanOrEqual(3);
  for (const q of await quotes.all()) {
    await expect(q.locator('blockquote')).not.toBeEmpty();
    await expect(q.locator('figcaption')).toContainText(/\S+ \S+.*,/);
    await expect(q.locator('img')).toHaveAttribute('alt', /.*/);
  }
});
```

## Do
- Prefer specifics over adjectives: "Cut onboarding from 9 days to 2" beats "Great product".
- Attribute every quote with full name, role, company and a real photo; link to the source when it exists.
- Match proof type to the doubt: logos for credibility, numbers for scale, case studies for fit, reviews for risk.
- Place proof by the CTA and by the price, not only in a block at the bottom.
- Logo strip: 5-8 logos, grayscale, equal optical height (about 32 px), with permission.
- Use real counts with a date ("12,400 teams, as of Oct 2026"); round honestly.
- Mark up as `<figure><blockquote>…</blockquote><figcaption>` and add `AggregateRating` JSON-LD only for ratings that appear on the page and are real.
- Alt text for logos is the company name.
- Keep quotes under about 40 words; link to the long version.

## Avoid
- Invented or anonymous testimonials, bought reviews, fake live-visitor counters.
- Carousels that auto-advance quotes.
- Logos of companies that never agreed or only used a free tier.
- Star ratings with no volume or source.

## Review
- [ ] Every claim is true, dated, attributable, and has permission.
- [ ] Proof is near the action it supports.
- [ ] Markup is semantic; structured data matches visible content.
- [ ] Logos are uniform and carry alt text.
