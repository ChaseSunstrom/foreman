---
name: floating-ui
title: Floating UI
area: web
tags: [floating-ui, popover, tooltip, positioning, dropdown, middleware]
detect: [dep:@floating-ui/dom, dep:@floating-ui/react, dep:@floating-ui/react-dom, dep:@floating-ui/vue]
related: [react, accessibility, radix-ui, testing-library]
---
Floating UI: positioning engine for tooltips, popovers and dropdowns, with middleware and interaction hooks for React.

## Verify
- `npx tsc --noEmit`: middleware and placement types.
- `npx eslint .`: lint.
- `npx vitest run`: open and close behavior by role.
- `npx playwright test --grep popover`: real layout: flip near edges, stay in the viewport, scroll with the page.

## Test first
jsdom has no layout, so test behavior in unit tests and positions in a real browser.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { HelpTip } from "./HelpTip";

test("tooltip opens on focus and closes on Escape", async () => {
  render(<HelpTip label="Billing info" />);
  await userEvent.tab();
  expect(await screen.findByRole("tooltip")).toHaveTextContent("Billing info");
  await userEvent.keyboard("{Escape}");
  expect(screen.queryByRole("tooltip")).toBeNull();
});
```

## Do
- In React use `useFloating({ open, onOpenChange, placement, middleware: [offset(8), flip(), shift({ padding: 8 })], whileElementsMounted: autoUpdate })`.
- Compose interactions: `useHover`, `useFocus`, `useClick`, `useDismiss`, `useRole`, then `useInteractions([...])` and spread the prop getters.
- Render overlays in `<FloatingPortal>` and use `FloatingFocusManager` for dialogs and menus.
- Add `arrow()` before others when using an arrow, and `size()` to cap the height of long lists.
- Use `strategy: "fixed"` when the reference sits in a transformed or scrolling container.
- Use `autoUpdate` only while open (via `whileElementsMounted`) and clean up on close.
- Use `useRole({ role: "tooltip" })` or `"dialog"`, `"menu"`, `"listbox"` so aria attributes are right.

## Avoid
- Positioning once without `autoUpdate`: it drifts on scroll or resize.
- Calling `computePosition` per frame yourself.
- Hover-only triggers: add focus and touch support.
- Skipping `useDismiss`: no Escape or outside-click close.
- Putting overlays inside `overflow: hidden` ancestors without a portal.

## Review
- [ ] Middleware order is deliberate (offset, flip, shift, arrow).
- [ ] `autoUpdate` runs only while mounted and open.
- [ ] Overlays are portaled and dismissible by keyboard.
- [ ] Roles and aria attributes come from `useRole`.
- [ ] Positions are verified in a real browser.
