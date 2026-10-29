---
name: kinetic-typography
title: Kinetic Typography
area: frontend
tags: [typography, animation, text, split-text, variable-fonts, motion]
detect: [dep:splitting, dep:split-type, dep:gsap]
related: [typography, variable-fonts, animation, accessibility, stagger-choreography]
---
Moving text that stays readable, searchable and accessible: split per word or letter, animate transform, never hide the words.

## Verify
- `npx playwright test --grep kinetic`: asserts the accessible name of the heading equals the full string.
- `npx axe-cli http://localhost:3000`: flags split text that screen readers read letter by letter.
- Devtools Rendering panel: enable layout shift regions to watch for reflow as letters move.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('split headline keeps one readable name', async ({ page }) => {
  await page.goto('/');
  const h = page.getByRole('heading', { level: 1 });
  await expect(h).toHaveAccessibleName('Make it move');
});
```

## Do
- Split with a small helper or library; wrap the whole heading with `aria-label="Make it move"` and give each span `aria-hidden="true"`.
- Animate `transform` and `opacity` per span (`display: inline-block` is required for transforms); stagger 20-40 ms per character, capped at 500 ms total.
- Prefer word-level splits for long lines; use letters only for short headlines under about 30 characters.
- Animate variable-font axes (`font-variation-settings: "wght" 400 to 800`) for emphasis; check it does not reflow neighbors, or reserve width.
- Use `text-wrap: balance` so the final layout is settled before animating; pin `line-height`.
- Use `clip-path` or `overflow: clip` masks for line reveals, with the text in normal flow.
- Under reduced motion, show the plain text with a fade or none.

## Avoid
- Splitting into spans without ARIA fixes: screen readers announce letters or break words.
- Animating before fonts load: use `document.fonts.ready` to avoid a jump.
- Per-letter animation of paragraphs: unreadable and heavy.
- Letter-spacing or font-size animation: reflows the line every frame.
- Text only in a canvas or WebGL with no DOM text: no search, selection or translation.

## Review
- [ ] Copy, select and find-in-page return the full text.
- [ ] Screen readers read the heading once, as a phrase.
- [ ] Animation starts after fonts are ready and causes no layout shift.
- [ ] Reduced-motion users see static text.
