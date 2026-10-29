---
name: popover-api
title: Popover API
area: frontend
tags: [html, popover, top-layer, popovertarget, light-dismiss, menus]
detect: []
related: [anchor-positioning, dialogs, focus-management, aria-patterns, animation]
---
Native popovers with the popover attribute: top layer, light dismiss and Escape handling without JavaScript, animated with @starting-style.

## Verify
- `npx playwright test --grep popover`: opens by click, closes with Escape and an outside click, asserts focus returns.
- `npx @axe-core/cli http://localhost:3000`: checks roles and names on the trigger and content.
- `grep -rn "z-index: *[0-9]\{3,\}" src`: stacking hacks the top layer makes unnecessary.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('popover closes on Escape and returns focus', async ({ page }) => {
  await page.goto('/');
  const trigger = page.getByRole('button', { name: 'Help' });
  await trigger.click();
  await expect(page.locator('#help')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('#help')).toBeHidden();
  await expect(trigger).toBeFocused();
});
```

## Do
- Markup: `<button popovertarget="help">Help</button> <div id="help" popover>...</div>`. Default `popover="auto"` closes on outside click and Escape, and closes other auto popovers.
- Use `popover="manual"` for toasts and persistent panels; you control closing.
- Use `popovertargetaction="show|hide|toggle"`; JS calls: `el.showPopover()`, `hidePopover()`, `togglePopover()`.
- Listen to `toggle` and `beforetoggle` events for state; `:popover-open` selects the open state.
- Animate with `@starting-style` and `transition: opacity 150ms, display 150ms allow-discrete, overlay 150ms allow-discrete;`.
- Position with anchor positioning (see anchor-positioning); `::backdrop` styles the layer behind.
- Use `popover=hint` hover tooltips only after checking support; baseline for `auto` and `manual` since 2024.
- Menus still need roles: add `role="menu"` and arrow-key handling, since popover gives focus and dismissal, not semantics.
- Use `<dialog>` instead when the content is modal and must block the page.

## Avoid
- Popovers for modal flows: no focus trap or inert background; use `dialog.showModal()`.
- Nesting auto popovers without a parent link: opening the child closes the parent unless it is a descendant or invoked from it.
- Hiding with `display: none` by hand; use the API so state stays in sync.
- Forgetting a visible close button on touch.
- Putting essential content only in a hover-triggered tip.

## Review
- [ ] Escape, outside click and the trigger all close it; focus returns to the trigger.
- [ ] Entry and exit animation respect `prefers-reduced-motion`.
- [ ] Roles and labels match the pattern (menu, tooltip, dialog).
- [ ] Browsers without support still show the content or have a fallback.
