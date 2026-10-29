---
name: mobile-navigation
title: Mobile Navigation
area: ux
tags: [mobile, navigation, tab-bar, thumb-zone, product-design]
detect: []
related: [navigation-patterns, responsive-design, accessibility, information-architecture]
---
On phones put the 3-5 main destinations in a bottom tab bar within thumb reach, and keep targets at least 44 px.

## Verify
- `npx playwright test --project="Mobile Safari" --grep nav`: runs on a 390 px device profile.
- `grep -rnE "height: *(2[0-9]|3[0-9])px" src/nav`: finds likely undersized tap targets.
- `npx axe-core-cli http://localhost:3000 --viewport 375x667`: target size and label rules pass.
- Real-device test: reach every tab one-handed on a large phone; check the safe-area inset on iOS.

## Test first
```ts
import { test, expect, devices } from '@playwright/test';

test.use({ ...devices['iPhone 13'] });

test('bottom tabs are reachable and at least 44px', async ({ page }) => {
  await page.goto('/');
  const tabs = page.getByRole('navigation', { name: 'Main' }).getByRole('link');
  expect(await tabs.count()).toBeLessThanOrEqual(5);
  for (const t of await tabs.all()) {
    const box = await t.boundingBox();
    expect(box!.height).toBeGreaterThanOrEqual(44);
    expect(box!.width).toBeGreaterThanOrEqual(44);
  }
});
```

## Do
- Use a bottom tab bar for 3-5 top-level destinations, each with an icon and a text label.
- Keep the current tab marked and tapping it again scrolls to top or pops to root.
- Use a hamburger or "More" tab only for secondary destinations; never for the primary ones.
- Respect safe areas: `padding-bottom: env(safe-area-inset-bottom)` and `viewport-fit=cover`.
- Give tap targets 44x44 px (iOS) or 48 dp (Material) with 8 px between them.
- Keep the back affordance visible and consistent; support the system back gesture.
- Preserve each tab's scroll and state when switching.
- Place primary actions in the lower half; keep destructive ones away from the edge.

## Avoid
- Hiding all navigation behind a hamburger: discovery drops sharply.
- More than 5 tabs; the targets shrink and labels truncate.
- Icon-only tabs with unclear meaning.
- Hover menus, and fixed bars that cover content when the keyboard opens.
- Hijacking the browser back button or swipe edge gestures.

## Review
- [ ] 5 or fewer primary tabs, labelled, with active state.
- [ ] Targets meet 44 px; spacing prevents mis-taps.
- [ ] Safe areas and the on-screen keyboard are handled.
- [ ] Tab state and scroll persist.
