---
name: design-handoff
title: Design Handoff
area: ux
tags: [ux, handoff, figma, storybook, specs, visual-regression]
detect: [dep:@storybook/react, dep:chromatic, dep:@figma/code-connect]
related: [design-tokens, design-systems, storybook, spacing-scales, ui-polish]
---
Designers and developers share tokens, components and states, and check the build against the design automatically.

## Verify
- `npx style-dictionary build`: tokens exported from design compile with no unresolved aliases.
- `npx storybook build && npx chromatic --exit-zero-on-changes`: visual diffs per component and state.
- `npx playwright test --update-snapshots=none --grep visual`: screenshots match the approved baseline.
- `grep -rnE "#[0-9a-fA-F]{6}" src | grep -v tokens`: values that skipped the token layer.

## Test first
A screenshot test per component state against the approved baseline.
```ts
import { test, expect } from '@playwright/test';

for (const state of ['default', 'hover', 'focus', 'disabled', 'loading']) {
  test(`button ${state}`, async ({ page }) => {
    await page.goto(`/iframe.html?id=button--${state}&viewMode=story`);
    await expect(page.locator('#storybook-root')).toHaveScreenshot(`button-${state}.png`, { maxDiffPixelRatio: 0.002 });
  });
}
```

## Do
- Hand off by link and token, not by redline PDF: a Figma file with Variables mapped to design tokens and a component per code component.
- Each component spec lists: anatomy, variants, states (default, hover, focus, active, disabled, loading, error), sizes, spacing in tokens, behavior at 375 / 768 / 1280, and keyboard behavior.
- Use the same names in design and code (`Button/Primary/Large` equals `<Button variant="primary" size="lg">`).
- Include content rules: min and max text length, truncation, empty and error text, long German and short CJK strings.
- Ship each component in Storybook with controls and an a11y addon; designers approve there.
- Run visual regression in CI with fixed fonts, viewport and disabled animation; review diffs like code.
- Define done: matches design within the token scale (not pixel-for-pixel), passes axe, has all states.
- Hold a 15-minute walk-through before build and a design review on the built version.

## Avoid
- Eyeballing pixels with a ruler overlay; spacing off the scale gets copied into code.
- Screenshots as specs: states and behavior go missing.
- Design and code tokens maintained twice by hand.
- Updating baselines without reviewing the diff.

## Review
- [ ] Tokens flow from one source to both design and code.
- [ ] Each component has all states in Storybook and baseline screenshots.
- [ ] Names match across design and code.
- [ ] Content edge cases are specified and tested.
