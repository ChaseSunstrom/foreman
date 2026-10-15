---
name: tailwind
title: Tailwind CSS
area: web
tags: [tailwind, css, utility-first, styling, design-tokens]
detect: [dep:tailwindcss, file:tailwind.config.*]
related: [sass, storybook, react, vue, svelte]
---
Tailwind CSS: utility classes generated from the source files it scans, themed through config or CSS.

## Verify
- `npx tailwindcss -i ./src/input.css -o /tmp/out.css --minify`: the build succeeds (v3 CLI; v4 uses `@tailwindcss/cli`).
- `npx prettier --check .`: with `prettier-plugin-tailwindcss` it enforces class order.
- `npm run build`: the real bundler pipeline, which is what ships.
- `npx playwright test`: visual or layout assertions at the breakpoints that matter.

## Test first
Class names are not logic; the failing check is rendered behavior: a component test that asserts a state class or a browser test at a viewport.
```ts
import { test, expect } from "@playwright/test";

test("nav collapses below md", async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 800 });
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Menu" })).toBeVisible();
});
```

## Do
- Build class strings from complete literal names so the scanner sees them; map variants to full strings (`{ primary: "bg-blue-600 text-white" }`).
- Put design tokens in the theme (`theme.extend` in v3 config, `@theme` in CSS for v4), and use them instead of arbitrary values.
- Design mobile first: unprefixed is the base, then `sm:`, `md:`, `lg:` up.
- Use `dark:` with a configured strategy and state variants (`hover:`, `focus-visible:`, `disabled:`, `group-*`, `peer-*`).
- Extract repeated markup into components, not `@apply` piles.
- Merge conditional classes with `clsx` plus `tailwind-merge` so later classes win.
- Keep visible focus styles; do not remove outlines without a replacement.
- Check the installed major version: setup differs (`@tailwind` directives in v3, `@import "tailwindcss"` in v4).

## Avoid
- Dynamic class names (`` `bg-${color}-500` ``): never generated, so no style. Use a lookup of full class strings or safelist.
- Content globs that miss files (`content` in v3): classes in them are purged. Include every template, component and JS path.
- `@apply` to recreate BEM: loses the point and hits ordering bugs. Use components.
- Conflicting utilities on one element (`p-2 p-4`): winner is stylesheet order, not attribute order. Use `tailwind-merge`.
- Arbitrary values everywhere (`w-[317px]`): token drift. Add a theme value.
- `!important` modifiers (`!p-0`) as a first resort: fix specificity or ordering.
- Copying v3 config into a v4 project, or the reverse: options silently ignored. Follow the installed version's docs.

## Review
- [ ] No dynamically assembled class fragments.
- [ ] Content paths cover every file with classes.
- [ ] Colors and spacing come from the theme, with adequate contrast in dark mode.
- [ ] Interactive elements have visible focus and hover/disabled states.
- [ ] Class order is formatted by the Prettier plugin.
