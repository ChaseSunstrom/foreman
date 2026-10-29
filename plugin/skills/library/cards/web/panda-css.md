---
name: panda-css
title: Panda CSS
area: web
tags: [panda, pandacss, css-in-js, zero-runtime, design-tokens, recipes]
detect: [dep:@pandacss/dev, dep:@pandacss/preset-panda, file:panda.config.*]
related: [css-custom-properties, vanilla-extract, tailwind, react]
---
Panda CSS: build-time CSS-in-JS; a static extractor turns `css()` calls, recipes and tokens into atomic CSS.

## Verify
- `npx panda codegen`: regenerates `styled-system/` after config changes.
- `npx panda --minify`: builds CSS; fails on config errors.
- `npx panda analyze`: lists token and recipe usage.
- `npx tsc --noEmit`: token names and recipe variants type-check.

## Test first
Test recipes as pure functions; they return class strings.
```ts
import { button } from "../styled-system/recipes";

test("button recipe maps variants to classes", () => {
  const primary = button({ visual: "solid", size: "md" });
  const ghost = button({ visual: "ghost", size: "md" });
  expect(primary).not.toBe(ghost);
  expect(button.raw({ size: "lg" })).toMatchObject({ size: "lg" });
});
```

## Do
- Define tokens and semantic tokens in `defineConfig({ theme: { extend: { tokens, semanticTokens } } })`, with conditions for dark mode.
- Set `include` globs to every file that uses styles, and `outdir: "styled-system"`; add a `prepare` script `panda codegen`.
- Write styles with `css({ ... })`, `styled`, or patterns (`stack`, `hstack`, `grid`); use recipes (`cva`, `sva`) for variants.
- Keep style values static or from finite unions; reach for `data-` attributes or CSS variables for runtime values.
- Import the generated CSS once (`@layer reset, base, tokens, recipes, utilities;` in `index.css`).
- Use `staticCss` in config for classes that can only be known at runtime.
- Check in `panda.config` but gitignore `styled-system` only if codegen runs in CI and postinstall.

## Avoid
- Dynamic strings like `css({ color: `${name}.500` })` with unknown values: the extractor cannot see them.
- Files outside `include`: the styles never ship.
- Forgetting `panda codegen` after config edits: type errors and missing classes.
- Mixing Tailwind utilities and Panda on the same elements without layers.
- Hard-coded hex values when a token exists.

## Review
- [ ] `include` covers all style-using files.
- [ ] Codegen runs in install and CI.
- [ ] Variants are recipes, not ad hoc conditionals.
- [ ] Runtime-only values use CSS variables or `staticCss`.
- [ ] Dark mode uses semantic tokens.
