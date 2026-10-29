---
name: ark-ui
title: Ark UI
area: web
tags: [ark-ui, zag, headless, react, vue, solid, state-machines]
detect: [dep:@ark-ui/react, dep:@ark-ui/vue, dep:@ark-ui/solid, dep:@zag-js/core]
related: [react, accessibility, radix-ui, testing-library]
---
Ark UI: headless, state-machine-driven components (Zag.js) for React, Vue and Solid; Chakra v3 and Park UI build on it.

## Verify
- `npx tsc --noEmit`: part names and prop types.
- `npx eslint .`: lint.
- `npx vitest run`: role-based interaction tests.
- `npx playwright test --grep a11y`: keyboard behavior in a real browser.

## Test first
Test through roles and state attributes.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Accordion } from "@ark-ui/react/accordion";

test("accordion item expands on click", async () => {
  render(
    <Accordion.Root collapsible>
      <Accordion.Item value="a">
        <Accordion.ItemTrigger>Details</Accordion.ItemTrigger>
        <Accordion.ItemContent>Body</Accordion.ItemContent>
      </Accordion.Item>
    </Accordion.Root>,
  );
  const trigger = screen.getByRole("button", { name: "Details" });
  await userEvent.click(trigger);
  expect(trigger).toHaveAttribute("aria-expanded", "true");
});
```

## Do
- Import per component (`@ark-ui/react/accordion`) to keep bundles small.
- Compose `Root`, `Trigger`, `Content`, and use `asChild` to render your own element, keeping ref forwarding.
- Style via `data-state`, `data-part`, `data-scope` attributes; they are the stable styling hooks.
- Control state with `value` and `onValueChange` (or `open`/`onOpenChange`), or the `defaultValue` forms.
- Use `Portal` for overlays and `Presence` or `lazyMount`/`unmountOnExit` for heavy content.
- Use the hook form (`useDialog`, `useCombobox`) when you need the machine API outside the tree.
- Use `Field` and `Fieldset` so labels, helper text and errors are linked.

## Avoid
- Importing the package root in a bundle-sensitive app.
- Targeting generated class names: use data attributes.
- Re-creating collections (for Select, Combobox) each render: memoize `createListCollection`.
- Mixing controlled and uncontrolled props for the same value.
- Custom `asChild` children that drop the ref or spread props.

## Review
- [ ] Per-component imports.
- [ ] Styling keys off data attributes.
- [ ] Collections are memoized.
- [ ] Overlays are portaled and focus-trapped.
- [ ] Interaction tests use roles and keyboard.
