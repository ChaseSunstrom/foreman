---
name: headless-ui
title: Headless UI
area: web
tags: [headlessui, react, vue, accessibility, unstyled, tailwind]
detect: [dep:@headlessui/react, dep:@headlessui/vue]
related: [react, tailwind, accessibility, testing-library, radix-ui]
---
Headless UI: unstyled, accessible Dialog, Menu, Listbox, Combobox, Disclosure and Transition components from the Tailwind team.

## Verify
- `npx tsc --noEmit`: component props and render-prop types.
- `npx eslint .`: lint, including jsx-a11y.
- `npx vitest run`: interaction tests by role.
- `npx playwright test --grep a11y`: keyboard flow and focus return in a real browser.

## Test first
Drive it as a keyboard user and query by role.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ConfirmDialog } from "./ConfirmDialog";

test("dialog traps focus and returns it on Escape", async () => {
  render(<ConfirmDialog />);
  const open = screen.getByRole("button", { name: /delete/i });
  await userEvent.click(open);
  expect(await screen.findByRole("dialog")).toBeVisible();
  await userEvent.keyboard("{Escape}");
  expect(screen.queryByRole("dialog")).toBeNull();
  expect(open).toHaveFocus();
});
```

## Do
- Compose parts as documented (`Dialog`, `DialogPanel`, `DialogTitle`, `Description`); the title and description wire up `aria-labelledby` and `aria-describedby`.
- Style with state via data attributes (`data-[open]:`, `data-[focus]:`, `data-[selected]:`) or render props.
- Use `as={Fragment}` or the `as` prop to render your own element, and make sure it forwards refs.
- Use `Transition` (or `transition` prop in v2) for enter and leave, and keep a focusable element inside every `Dialog`.
- Give `Combobox` a controlled `value`, `onChange`, and a `displayValue`; debounce async filtering.
- Provide `Field`, `Label` and `Description` around inputs so labels connect.
- Add `@media (prefers-reduced-motion)` fallbacks to transition classes.

## Avoid
- A `Dialog` with no focusable child: it throws at runtime.
- Wrapping parts in extra divs that break the expected structure.
- Custom elements in `as` that do not forward refs: focus management breaks.
- Mixing v1 `show`/`Transition.Child` patterns with v2 APIs; check the installed major.
- Hand-rolling `aria-*` on top of the ones it already sets.

## Review
- [ ] Every dialog has a title and a focusable element.
- [ ] Focus returns to the trigger on close.
- [ ] Tests use roles and keyboard events.
- [ ] Custom `as` components forward refs.
- [ ] Reduced motion handled for transitions.
