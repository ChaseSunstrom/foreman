---
name: calls-to-action
title: Calls to Action
area: ux
tags: [ux, cta, buttons, copy, conversion, touch-targets]
detect: []
related: [landing-pages, hero-sections, visual-hierarchy, color-contrast, forms, accessibility]
---
A CTA is a verb-led button that names the outcome, stands out once per view, and is easy to hit.

## Verify
- `npx playwright test --grep cta`: checks label, size, contrast and count.
- `grep -rniE ">(submit|click here|ok|go)<" src`: vague labels.
- `node scripts/contrast.mjs --pair "#ffffff" "#3b5bdb"`: your contrast script; the button text needs 4.5:1, the button edge against the page 3:1.
- Devtools device mode at 375 px: tap target at least 44x44 px.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('primary CTA is a clear, large, single action', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/pricing');
  const cta = page.locator('[data-cta=primary]');
  await expect(cta.first()).toHaveText(/^(Start|Get|Book|Try|Create|Download)\b/);
  const box = await cta.first().boundingBox();
  expect(box!.height).toBeGreaterThanOrEqual(44);
  expect(box!.width).toBeGreaterThanOrEqual(44);
  expect(await page.locator('[data-cta=primary]:visible').count()).toBeLessThanOrEqual(2);
});
```

## Do
- Label: a verb plus the outcome, 2-4 words ("Start free trial", "Get the report"); first person ("Get my plan") can lift clicks, so test it.
- Add a one-line friction reducer under it ("No card needed. Cancel anytime.").
- One filled primary per view; secondary is outlined or a text link; never two same-weight buttons.
- Size: height 44-56 px, horizontal padding 20-32 px, font 16-18 px, weight 600; radius from tokens.
- Use `<a href>` for navigation and `<button>` for actions; both need visible `:focus-visible`.
- Show states: hover, active, focus, disabled (explain why), loading with `aria-busy` and no double submit.
- Leave 16+ px of space around it so it reads as isolated.
- Test copy and placement with an A/B run sized for significance, not by taste.

## Avoid
- "Submit", "Click here", "Learn more" as the main action.
- Disabled buttons with no explanation.
- Low-contrast ghost buttons as the primary action.
- Urgency tricks (fake timers, shaming opt-out text): dark patterns that erode trust and may be illegal.

## Review
- [ ] Label names the outcome with a verb.
- [ ] Single primary per view; target at least 44x44 px; contrast passes.
- [ ] All states, including focus and loading, are designed.
- [ ] No manipulative copy.
