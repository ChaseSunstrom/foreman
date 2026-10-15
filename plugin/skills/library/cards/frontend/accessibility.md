---
name: accessibility
title: Accessibility (WCAG)
area: frontend
tags: [a11y, wcag, aria, keyboard, screen-reader, html]
detect: [dep:@axe-core/playwright, dep:jest-axe, dep:eslint-plugin-jsx-a11y, dep:axe-core, dep:@axe-core/react]
related: [forms, css-layout, animation, design-systems, playwright]
---
Accessible UI: semantic HTML first, full keyboard operation, visible focus, names and states for assistive tech.

## Verify
- `npx lighthouse http://localhost:3000 --only-categories=accessibility --quiet --chrome-flags="--headless"`: automated score; catches only about a third of issues.
- `npx playwright test a11y`: axe scans in a real browser, per route and per state (open modal, error form).
- `npx eslint . --rule '{"jsx-a11y/alt-text":"error"}'`: static JSX checks (needs eslint-plugin-jsx-a11y).
- Manual: Tab through the page with no mouse, then run a screen reader on the main flow.

## Test first
Scan the rendered state with axe, then assert behavior axe cannot see.
```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('dialog is operable by keyboard', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Settings' }).press('Enter');
  await expect(page.getByRole('dialog', { name: 'Settings' })).toBeVisible();
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button', { name: 'Settings' })).toBeFocused();
});
```

## Do
- Use the native element: `button`, `a href`, `input`, `select`, `dialog`, `details`. Landmarks (`header`, `nav`, `main`) and one `h1` with ordered headings.
- Give every control an accessible name: visible text, `<label for>`, or `aria-label` only when no text exists.
- Keep focus visible with `:focus-visible`; never remove an outline without a replacement of 3:1 contrast.
- Move focus on route change and into dialogs, trap it while modal, return it to the trigger on close.
- Announce async updates with `aria-live="polite"` on a container present at load.
- Text contrast 4.5:1 (3:1 large text and UI borders); targets at least 24px, ideally 44px.
- Honor `prefers-reduced-motion`; never convey state by color alone.

## Avoid
- `div onClick` as a button: no keyboard or role. Use `<button type="button">`.
- ARIA roles that duplicate or contradict native semantics (`role="button"` on `<a href>`): remove ARIA, fix the element.
- `aria-hidden="true"` on focusable elements: they stay tabbable but unnamed. Use `inert` or remove from tab order.
- `tabindex` greater than 0: breaks natural order. Use 0 or -1 only.
- Placeholder as the only label: it vanishes and fails contrast. Add a real label.
- Missing `alt`: use `alt=""` for decoration, a purpose-describing text otherwise.
- Toasts that vanish in seconds: allow dismissal and persistence, use `role="status"`.

## Review
- [ ] Every interaction works with keyboard alone, in logical order.
- [ ] Focus is visible, moves sensibly, and is never lost on close or navigation.
- [ ] Names, roles, states exposed (`aria-expanded`, `aria-current`, `aria-invalid`).
- [ ] Contrast and zoom to 200% and 320px width hold without loss of content.
- [ ] Automated axe run is clean and one manual screen reader pass done.
