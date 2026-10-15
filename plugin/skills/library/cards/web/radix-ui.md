---
name: radix-ui
title: Radix UI
area: web
tags: [radix, react, primitives, accessibility, headless, portal]
detect: [dep:radix-ui, dep:@radix-ui/react-dialog, dep:@radix-ui/react-dropdown-menu, dep:@radix-ui/react-popover]
related: [shadcn-ui, react, tailwind, testing-library]
---
Radix UI primitives: unstyled, accessible React components with compound parts, controlled state and portals.

## Verify
- `npx tsc --noEmit`: part props and `asChild` usage type-check.
- `npx eslint .`: lint, with the jsx-a11y plugin if present.
- `npx vitest run`: interaction tests through roles.
- `npx playwright test`: real-browser focus, keyboard and portal behavior jsdom cannot show.

## Test first
Use role queries and the keyboard, as users do.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ConfirmDialog } from "./ConfirmDialog";

test("Escape closes the dialog", async () => {
  render(<ConfirmDialog />);
  await userEvent.click(screen.getByRole("button", { name: /open/i }));
  expect(screen.getByRole("dialog")).toBeInTheDocument();
  await userEvent.keyboard("{Escape}");
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
});
```

## Do
- Build from the parts: `Root`, `Trigger`, `Portal`, `Overlay`, `Content`, `Title`, `Description`, `Close`.
- Always render a `Title` (and `Description` or an explicit `aria-describedby`); hide it visually if needed.
- Control state with `open` and `onOpenChange` (or `value` and `onValueChange`) when the app owns it; use `defaultOpen` otherwise.
- Use `asChild` to merge behavior onto your own element; the child must forward refs and spread props.
- Style by data attributes (`[data-state="open"]`, `[data-side]`, `[data-disabled]`) and animate with CSS using `data-state`.
- Use `forceMount` with an animation library only when you control unmounting.
- Wrap tooltips in `Tooltip.Provider` once near the root.

## Avoid
- `asChild` onto a component that does not forward `ref` or spread props: triggers silently stop working. Use `forwardRef` and spread `...props`.
- Missing `Dialog.Title`: console accessibility warning and a nameless dialog. Add the title.
- Rendering content outside a `Portal` inside overflow-hidden parents: clipped menus. Use `Portal`.
- Mixing controlled and uncontrolled props (`open` without `onOpenChange`): the component cannot close. Provide both.
- Testing portal content with `container` queries: it is mounted on `document.body`. Use `screen`.
- Z-index wars: give the portal root a known stacking context instead of `z-[9999]` everywhere.
- Mixing old per-package imports and the unified `radix-ui` package inconsistently: pick one style for the repo.

## Review
- [ ] Every overlay has a title, a way to close and returns focus to its trigger.
- [ ] Controlled components pass both the value and its change handler.
- [ ] `asChild` targets forward refs and props.
- [ ] Animations key off `data-state` and unmount correctly.
- [ ] Keyboard paths (Tab, Escape, arrows) have a test.
