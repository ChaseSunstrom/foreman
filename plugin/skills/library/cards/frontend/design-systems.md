---
name: design-systems
title: Design Systems
area: frontend
tags: [design-tokens, components, storybook, theming, dark-mode]
detect: [dep:storybook, dep:@storybook/react, dep:@storybook/vue3, dep:style-dictionary, dep:@radix-ui/react-dialog, dep:@mui/material, dep:class-variance-authority, file:.storybook/*, file:components.json]
related: [accessibility, css-layout, animation, responsive-design]
---
A shared component library driven by design tokens, with documented variants, theming and visual regression checks.

## Verify
- `npx storybook build`: every story compiles and renders.
- `npx playwright test --project=visual`: screenshot diffs of stories across themes (set up with `toHaveScreenshot`).
- `npx tsc --noEmit`: component prop types and variant unions agree.
- `npx stylelint "src/**/*.css" --rule '{"color-no-hex":true}'`: raw hex values slipping past tokens.

## Test first
Test the component contract: variants, states, accessible name.
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

test('loading button is busy and ignores clicks', async () => {
  const onClick = vi.fn();
  render(<Button loading onClick={onClick}>Save</Button>);
  const b = screen.getByRole('button', { name: /save/i });
  expect(b).toHaveAttribute('aria-busy', 'true');
  await userEvent.click(b);
  expect(onClick).not.toHaveBeenCalled();
});
```

## Do
- Define tokens in layers: primitive (`blue-500`), semantic (`color-action`), component (`button-bg`). Components consume semantic or component tokens only.
- Expose tokens as CSS custom properties; theme by swapping variables under `[data-theme]` and `prefers-color-scheme`.
- Model variants as a closed union (`variant: 'primary' | 'ghost'`, `size`); use a variant helper such as `cva` instead of string concatenation.
- Compose from accessible primitives (Radix, React Aria, Ark) for dialogs, menus, comboboxes.
- Forward `ref`, spread remaining props, and let consumers pass `className`.
- One story per state: default, hover, focus, disabled, loading, error, long text, RTL.
- Version and changelog the package; deprecate before removing.
- Document usage rules with do and don't examples.

## Avoid
- Hardcoded hex, px or z-index in components: bypasses theming. Reference tokens.
- Boolean prop explosion (`primary`, `large`, `outline`, `danger`): impossible combinations. Use enumerated variants.
- Building your own modal, select or tooltip from divs: focus and ARIA bugs. Use a primitive.
- Dark mode by inverting colors: contrast fails. Define dark semantic values explicitly.
- Overriding component internals with deep selectors: breaks on upgrade. Expose a slot or token.
- Storybook stories that mock away the real CSS and providers: stories lie. Use the app decorator and theme.
- Copy-pasting a component per app: forks drift. Publish a package.

## Review
- [ ] No raw color or spacing values outside the token files.
- [ ] Every variant and state has a story and a visual baseline in light and dark.
- [ ] Components are keyboard operable and named by role.
- [ ] Public API is typed, minimal, and documented; breaking changes are noted.
- [ ] Theme swap needs no component edits.
