---
name: daisyui
title: daisyUI
area: web
tags: [daisyui, tailwind, components, themes, css]
detect: [dep:daisyui]
related: [tailwind, css-custom-properties, accessibility, testing-library]
---
daisyUI: a Tailwind plugin that adds semantic component classes (`btn`, `card`, `modal`) and themes.

## Verify
- `npx tailwindcss -i src/input.css -o /tmp/out.css --minify`: builds with the plugin (v3).
- `npx vite build`: v4 uses `@plugin "daisyui"` in CSS with the Tailwind v4 Vite plugin.
- `npx playwright test --grep theme`: each configured theme renders and keeps contrast.
- `npx eslint .`: lint, including class-name plugins.

## Test first
Assert the plugin ships the classes and themes you rely on.
```ts
import { readFileSync } from "node:fs";

test("built CSS contains used components and the dark theme", () => {
  const css = readFileSync("dist/assets/index.css", "utf8");
  expect(css).toContain(".btn");
  expect(css).toMatch(/data-theme=["']?dark/);
});
```

## Do
- Check the major: v4 uses `@plugin "daisyui" { themes: light --default, dark --prefersdark; }` in CSS; v3 uses `plugins: [require("daisyui")]` and `daisyui: { themes }` in `tailwind.config`.
- Enable only the themes you ship; set `data-theme` on `<html>` and persist the choice.
- Compose daisyUI classes with Tailwind utilities (`btn btn-primary w-full`); override with utilities or theme variables.
- Use semantic colors (`bg-base-100`, `text-base-content`, `btn-primary`) so every theme works.
- Build custom themes by defining the documented color variables, then check contrast.
- Use the native elements daisyUI styles (`<dialog class="modal">`, checkbox-based swap, `details` collapse) and keep their labels and roles.
- Make sure Tailwind scans every file that holds classes.

## Avoid
- Hard-coded Tailwind colors (`bg-gray-100`) inside themed UI: they ignore the theme.
- Enabling every built-in theme: bloats CSS.
- Dynamically constructed class names the scanner cannot see (`btn-${kind}`).
- Using a modal class without a close path and focus handling.
- Relying on v3 config options in a v4 project.

## Review
- [ ] Version syntax matches the installed major.
- [ ] Only needed themes are enabled.
- [ ] UI uses semantic color classes.
- [ ] Modals and menus are keyboard-operable.
- [ ] Contrast is checked in every shipped theme.
