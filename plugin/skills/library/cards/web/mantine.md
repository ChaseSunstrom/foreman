---
name: mantine
title: Mantine
area: web
tags: [mantine, react, components, hooks, postcss, forms]
detect: [dep:@mantine/core, dep:@mantine/hooks, dep:@mantine/form]
related: [react, testing-library, accessibility, react-hook-form, nextjs-app-router]
---
Mantine: full React component library (v7+ uses CSS modules and PostCSS, no runtime CSS-in-JS) with hooks, forms and dates.

## Verify
- `npx tsc --noEmit`: component and theme types.
- `npx eslint .`: lint.
- `npx vitest run`: component tests inside `MantineProvider`.
- `npx next build` or `npx vite build`: confirms the styles import and the PostCSS preset load.

## Test first
Wrap in a provider and stub the browser APIs Mantine reads.
```tsx
import { MantineProvider } from "@mantine/core";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SignupForm } from "./SignupForm";

beforeAll(() => {
  window.matchMedia ??= (q: string) => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {} }) as any;
  global.ResizeObserver ??= class { observe() {} unobserve() {} disconnect() {} } as any;
});

test("shows a field error on empty submit", async () => {
  render(<MantineProvider><SignupForm /></MantineProvider>);
  await userEvent.click(screen.getByRole("button", { name: /sign up/i }));
  expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
});
```

## Do
- Import `@mantine/core/styles.css` once (or per-component styles with `@mantine/core/styles/Button.css`), and wrap the app in `MantineProvider`.
- Install `postcss-preset-mantine` and `postcss-simple-vars` for `rem()`, `light-dark()` and breakpoint mixins.
- Create one theme with `createTheme` (colors, primaryColor, fontFamily, components defaults) and pass it to the provider.
- In Next.js app router, add `ColorSchemeScript` in `<head>` and use `"use client"` for components that use hooks.
- Use `@mantine/form` (`useForm` with `validate`) or pair `form.getInputProps`; use `@mantine/hooks` (`useDisclosure`, `useDebouncedValue`).
- Prefer the `Styles API` (`classNames`, `styles`, `vars`) and CSS modules over inline overrides.
- Import from the specific packages and avoid barrel-heavy icons (`@tabler/icons-react` per icon).

## Avoid
- Missing styles import: components render unstyled.
- Using v6 APIs (`createStyles`, `sx`) on v7+; they were removed.
- Rendering without a provider in tests: crashes on theme access.
- Colour scheme flashes in SSR: set `defaultColorScheme` and `ColorSchemeScript`.
- Stacking `Modal` inside `Popover` without a shared portal target and z-index plan.

## Review
- [ ] Styles and PostCSS preset are installed and imported.
- [ ] One theme object; provider at the root.
- [ ] Tests wrap in a provider and stub browser APIs.
- [ ] No removed v6 APIs.
- [ ] SSR color scheme script is present.
