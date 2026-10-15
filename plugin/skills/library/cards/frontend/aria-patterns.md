---
name: aria-patterns
title: ARIA patterns
area: frontend
tags: [a11y, aria, widgets, semantics, testing]
detect: [dep:@axe-core/playwright]
related: [keyboard-navigation, focus-management, dialogs, accessibility]
---
Use native elements first; where a custom widget is unavoidable, follow the APG roles, states and keyboard model exactly.

## Verify
- `npx playwright test`: runs role-based queries and the axe scan.
- `npx @axe-core/cli http://localhost:3000`: static rule violations (names, roles, required parents).
- `npx vitest run`: Testing Library `getByRole` specs pass.

## Test first
Query by role and name, then assert state attributes.
```ts
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Disclosure } from './Disclosure';

test('disclosure toggles aria-expanded', async () => {
  render(<Disclosure title="Details">body</Disclosure>);
  const btn = screen.getByRole('button', { name: 'Details' });
  expect(btn).toHaveAttribute('aria-expanded', 'false');
  await userEvent.click(btn);
  expect(btn).toHaveAttribute('aria-expanded', 'true');
  expect(screen.getByText('body')).toBeVisible();
});
```

## Do
- Prefer `<button>`, `<a href>`, `<details>`, `<dialog>`, `<select>`, `<input type>` before any role.
- Name every control: visible text, `aria-labelledby`, or `aria-label` as the last resort.
- Keep state attributes in sync with the DOM: `aria-expanded`, `aria-selected`, `aria-pressed`, `aria-current`, `aria-checked`.
- Link relationships: `aria-controls`, `aria-describedby` (errors, hints), `aria-activedescendant` for composite widgets.
- Implement the full keyboard model for each role (tabs: arrows, Home, End; listbox, menu likewise).
- Use `aria-live="polite"` on a region that exists before the content changes; `assertive` only for urgent errors.
- Use one `<main>`, labelled `<nav>` landmarks, and a logical heading outline.

## Avoid
- `role="button"` on a `div`: no Enter or Space, no focus. Use `<button type="button">`.
- ARIA that contradicts semantics (`<button role="link">`, `role="heading"` with no `aria-level`): drop the role.
- `aria-hidden="true"` on a focusable element or its ancestor: it becomes a ghost tab stop. Use `inert` or `hidden`.
- A live region injected together with its message: screen readers miss it. Mount it empty, then update.
- `aria-label` on a generic `div` or `span`: it is ignored without a role. Add an element that supports names.
- `role="menu"` for site navigation: use a `<nav>` with a list of links; menus are for application actions.
- Icon-only buttons with no name: add `aria-label` and mark the SVG `aria-hidden`.

## Review
- [ ] Every interactive element is native or has role, name, state and keyboard handling.
- [ ] State attributes change with the UI, verified in a test.
- [ ] No `aria-hidden` over focusable content.
- [ ] axe reports zero violations on each key screen and state (open, error).
- [ ] Error text is associated through `aria-describedby`.
