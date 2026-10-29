---
name: brand-identity
title: Brand Identity
area: ux
tags: [ux, brand, identity, voice, guidelines]
detect: []
related: [logo-design, color-palettes, type-pairing, design-tokens, art-direction, design-systems]
---
A brand identity is a short, enforceable guide: positioning, voice, logo, color, type, imagery, all tied to tokens.

## Verify
- `test -f docs/brand.md && wc -w docs/brand.md`: a guide exists and stays short (under about 1,500 words).
- `grep -rnE "#[0-9a-fA-F]{6}" src | grep -v tokens`: brand colors only come from tokens.
- `npx playwright test --grep brand`: checks logo, brand font and primary color on key pages.
- `grep -rniE "\b(leverage|synergy|world-class|cutting-edge)\b" src docs`: banned words from the voice guide.

## Test first
Assert the identity primitives are present and match the guide.
```ts
import { test, expect } from '@playwright/test';

test('brand primitives render', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('header img[alt="Acme"], header svg[aria-label="Acme"]')).toBeVisible();
  const h1 = page.locator('h1').first();
  expect(await h1.evaluate(e => getComputedStyle(e).fontFamily)).toContain('Fraunces');
  const cta = page.locator('[data-variant=primary]').first();
  expect(await cta.evaluate(e => getComputedStyle(e).backgroundColor)).toBe('rgb(59, 91, 219)');
});
```

## Do
- Start with positioning: who it is for, what it replaces, one promise in a sentence, three personality adjectives (and three it is not).
- Write voice rules with a before/after example for each: tone by context (error, success, marketing), reading level near grade 8, sentence case for UI.
- Fix the visual core: logo variants, 1 brand hue plus neutrals, 2 typefaces, an imagery rule, an icon style.
- Encode it as design tokens so code and design share one source.
- Keep a one-page quick reference on top of the longer guide; link examples of right and wrong use.
- Name an owner who approves exceptions; log exceptions.

## Avoid
- A PDF nobody can search or link; use a versioned page in the repo.
- Voice words without examples ("friendly, bold") that anyone can read any way.
- Rebranding by swapping colors without changing the voice or the structure.
- Many near-identical brand colors from different campaigns.

## Review
- [ ] The guide fits in 1,500 words and has right/wrong examples.
- [ ] Brand colors, fonts and logos come from tokens and files, not copies.
- [ ] Voice rules cover error, success and marketing copy.
- [ ] Someone owns exceptions.
