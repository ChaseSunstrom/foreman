---
name: color-contrast
title: Color contrast
area: frontend
tags: [a11y, color, contrast, wcag, design-tokens]
detect: [dep:axe-core]
related: [dark-mode, css-custom-properties, typography, accessibility]
---
WCAG contrast for text, UI components and focus indicators in every theme and state.

## Verify
- `npx @axe-core/cli http://localhost:3000`: the `color-contrast` rule on rendered pages (run per theme).
- `npx playwright test`: axe scans in each state (hover, disabled, error, dark).
- `npx lhci autorun`: Lighthouse accessibility audit, if configured.

## Test first
Compute contrast from tokens so a bad palette fails before it ships.
```ts
import { expect, test } from 'vitest';

const lum = (hex: string) => {
  const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map(v => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const ratio = (a: string, b: string) => {
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
};
test('muted text on surface meets AA', () => {
  expect(ratio('#6b7280', '#ffffff')).toBeGreaterThanOrEqual(4.5);
});
```

## Do
- Hit 4.5:1 for body text, 3:1 for large text (about 24px, or 19px bold), 3:1 for UI component boundaries, icons and focus rings.
- Check against the actual background, including gradients, images (add a scrim) and overlays.
- Verify every state: hover, active, visited, disabled-with-meaning, placeholder, error, selected.
- Verify both themes; compute pairs from the token file in a unit test.
- Never rely on color alone: add an icon, text or pattern for errors, status and chart series.
- Respect `prefers-contrast: more` and `forced-colors: active` (use system colors, keep borders).
- Keep focus rings 3:1 against both the element and the page.

## Avoid
- Light gray placeholder and helper text: it is the most common failure. Darken to 4.5:1.
- Text on photos with no scrim: contrast varies by image. Add an overlay or text shadow baseline.
- Removing borders in forced-colors mode with `border: 0`: controls vanish. Use `transparent` borders.
- Trusting a design mock: measure the built tokens.
- Disabled-looking styles on active controls (opacity 0.5 on real actions): fails contrast and reads as broken.
- Passing axe and stopping: it cannot see images, gradients or hover states. Spot-check them.

## Review
- [ ] All text and UI pairs meet AA in light, dark and high-contrast.
- [ ] Status and error are not communicated by hue alone.
- [ ] Focus indicators are visible on every background.
- [ ] Contrast is checked on states, not just the default.
- [ ] Forced-colors mode keeps borders and icons visible.
