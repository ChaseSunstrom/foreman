---
name: css-custom-properties
title: CSS custom properties
area: frontend
tags: [css, variables, tokens, theming, design-system]
detect: []
related: [dark-mode, design-systems, container-queries, typography]
---
Design tokens as `--vars`: layered, scoped, with fallbacks, and typed where animation matters.

## Verify
- `npx stylelint "**/*.css"`: flags unknown properties and malformed `var()` usage.
- `npx playwright test`: reads computed values after a theme or scope change.
- `grep -rnE "#[0-9a-fA-F]{3,8}\b" src --include=*.css`: stray hex literals outside the token file.

## Test first
Assert that overriding a token on a scope root changes a descendant.
```ts
import { test, expect } from '@playwright/test';

test('button follows the scoped accent token', async ({ page }) => {
  await page.setContent(`<style>:root{--accent:rgb(0,0,255)}
    .btn{background:var(--accent)}</style>
    <div id="s" style="--accent:rgb(255,0,0)"><button class="btn">go</button></div>`);
  const bg = await page.locator('#s .btn').evaluate(e => getComputedStyle(e).backgroundColor);
  expect(bg).toBe('rgb(255, 0, 0)');
});
```

## Do
- Define primitives on `:root` (`--blue-600`), then semantic tokens that reference them (`--color-accent: var(--blue-600)`). Components use only semantic ones.
- Override tokens on a scope (`[data-theme=...]`, a component root), never by redeclaring component rules.
- Give `var()` a fallback when the token may be absent: `var(--gap, 1rem)`.
- Register tokens you animate: `@property --angle { syntax: '<angle>'; inherits: false; initial-value: 0deg; }`.
- Read and write from JS with `getComputedStyle(el).getPropertyValue('--x')` and `el.style.setProperty('--x', v)`.
- Use unitless numbers for scale tokens and multiply in `calc()` (`calc(var(--space) * 2)`).
- Prefix by role (`--color-`, `--space-`, `--radius-`) so grep finds them.

## Avoid
- Setting a variable per frame from JS for something that can be a class or `@property` animation: it recalculates style for the whole subtree. Scope the property to the smallest element.
- Using `var()` inside a media query condition: it does not work. Use a literal or `@container`.
- Unregistered custom properties in `transition`: they flip instantly because the browser cannot interpolate unknown types. Register with `@property`.
- A cyclic reference (`--a: var(--b); --b: var(--a)`): both become invalid at computed time. Keep a one-way chain.
- Hex literals in components that bypass tokens: dark mode and rebrands miss them. Reference a token.
- Invalid values fail silently as "unset" at computed time: check the Computed panel, not just the rule.

## Review
- [ ] Components reference semantic tokens only, no raw colors or magic spacing.
- [ ] Every `var()` that can be undefined has a fallback.
- [ ] Animated tokens are registered with `@property` and a valid `syntax`.
- [ ] Theme changes happen by scope override, with no duplicated component CSS.
- [ ] No token chains that loop.
