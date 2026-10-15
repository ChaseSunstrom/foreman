---
name: mui
title: MUI (Material UI)
area: web
tags: [mui, material-ui, react, theme, sx, emotion]
detect: [dep:@mui/material, dep:@mui/system, dep:@mui/icons-material, dep:@mui/x-data-grid]
related: [react, react-hook-form, testing-library]
---
MUI (Material UI): themed React components styled through the theme, the sx prop and slots, with tree-shakeable imports.

## Verify
- `npx tsc --noEmit`: theme augmentation and component props type-check.
- `npx eslint .`: lint.
- `npx vitest run`: component tests (wrap in `ThemeProvider` when the theme matters).
- `npm run build`: bundle size and import style show up in the build output.

## Test first
Render inside your theme and query by role and label.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ThemeProvider } from "@mui/material/styles";
import { theme } from "./theme";
import { LoginForm } from "./LoginForm";

test("shows an error for an empty email", async () => {
  render(<ThemeProvider theme={theme}><LoginForm /></ThemeProvider>);
  await userEvent.click(screen.getByRole("button", { name: /sign in/i }));
  expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
});
```

## Do
- Create one theme with `createTheme` and apply it with `ThemeProvider`; add `CssBaseline` once.
- Customize through `theme.components.MuiButton.styleOverrides` and `variants`, not one-off CSS in each file.
- Use `sx` for one-off styling with theme tokens (`sx={{ p: 2, color: "text.secondary" }}`) and `styled()` for reusable styled components.
- Import from the component path (`import Button from "@mui/material/Button"`) or confirm the named root import is tree-shaken in your bundler.
- Use `Grid` with the API the installed major version documents: its props changed between versions.
- Give inputs a `label` and `id`, and wire `error` and `helperText` from form state.
- Use `Box`, `Stack` and breakpoints (`xs`, `sm`, `md`) for layout instead of fixed pixels.
- In SSR, set up the Emotion cache as documented for your framework to avoid style flash.

## Avoid
- Deprecated or removed APIs from older tutorials: `makeStyles`, `withStyles` from `@mui/styles`, the old `Grid` `item` props on newer versions. Use `sx` or `styled`.
- Deep style overrides via global class selectors (`.MuiButton-root`): fragile. Use theme overrides or slots.
- Importing icons from the barrel (`@mui/icons-material`) in large apps: slow dev builds. Import from `@mui/icons-material/Add`.
- Inline `sx` objects on hot list items: new objects each render. Hoist or use `styled`.
- Missing `CssBaseline` and then fighting margins and fonts: add it.
- Controlled `TextField` with `value={undefined}` flipping to a string: React warns. Default to `""`.

## Review
- [ ] One theme, with dark mode and custom tokens defined in it.
- [ ] No legacy `@mui/styles` usage.
- [ ] Imports keep the bundle lean.
- [ ] Form fields have labels, error and helper text wired.
- [ ] SSR style handling matches the framework's documented setup.
