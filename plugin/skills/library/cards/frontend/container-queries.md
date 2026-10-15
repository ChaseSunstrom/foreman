---
name: container-queries
title: CSS container queries
area: frontend
tags: [css, container, responsive, components, layout]
detect: []
related: [responsive-design, css-layout, css-custom-properties, layout-shift]
---
Components that adapt to the width of their container with `@container`, not the viewport.

## Verify
- `npx playwright test`: resize the wrapper (not the viewport) and assert the layout switches.
- `npx stylelint "**/*.css"`: catches invalid at-rules and duplicate selectors.
- `npx tsc --noEmit`: component props that pick variants still type-check.

## Test first
Render the same card in a narrow and a wide wrapper at one viewport size.
```ts
import { test, expect } from '@playwright/test';

test('card stacks in a narrow container', async ({ page }) => {
  await page.setContent(`<style>.w{container-type:inline-size}
    .card{display:flex}@container (max-width:400px){.card{flex-direction:column}}</style>
    <div class="w" id="a" style="width:300px"><div class="card">x</div></div>
    <div class="w" id="b" style="width:700px"><div class="card">x</div></div>`);
  const dir = (id: string) => page.locator(`#${id} .card`).evaluate(e => getComputedStyle(e).flexDirection);
  expect(await dir('a')).toBe('column');
  expect(await dir('b')).toBe('row');
});
```

## Do
- Put `container-type: inline-size` on the wrapper and name it (`container-name: card`) so queries target it: `@container card (min-width: 30rem)`.
- Query the container, style its descendants. A container cannot restyle itself.
- Use `cqi` units for fluid type and spacing inside a component (`font-size: clamp(1rem, 4cqi, 1.5rem)`).
- Keep viewport media queries for page-level layout (nav, sidebars) and container queries for reusable components.
- Provide a sane default outside any `@container` rule so unsupported browsers still render a usable layout.
- Use `@supports (container-type: inline-size)` only when the fallback differs materially.

## Avoid
- `container-type: size` on a flexible-height element: it applies size containment on both axes and the box collapses to zero height. Use `inline-size`.
- Querying the element that is itself the container: the rule never matches. Add a wrapper.
- Putting `container-type` on `<body>` or a layout root "just in case": it creates a containing block for fixed and absolute descendants and a stacking context. Scope it to components.
- Hardcoding pixel breakpoints per component copied from the viewport design: use the component's real content width (`min-width` in `rem`).
- Testing only by resizing the browser window: the bug hides when the same component sits in a sidebar. Test two wrapper widths.

## Review
- [ ] Every `@container` rule has a matching `container-type` ancestor that is not the element itself.
- [ ] No `container-type: size` without a fixed height.
- [ ] Components render a usable layout with no container query applied.
- [ ] A test places the component in at least two container widths at one viewport.
- [ ] Container names are unique enough not to collide across components.
