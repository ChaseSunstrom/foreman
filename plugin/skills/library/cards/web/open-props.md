---
name: open-props
title: Open Props
area: web
tags: [open-props, css-variables, design-tokens, custom-properties, postcss]
detect: [dep:open-props, dep:postcss-jit-props]
related: [css-custom-properties, css-layout, accessibility, web-performance]
---
Open Props: a set of CSS custom properties (sizes, colors, easings, shadows) you compose with plain CSS.

## Verify
- `npx stylelint "**/*.css"`: lint, with `csstools/value-no-unknown-custom-properties` to catch unknown `--var` names.
- `npx postcss src/main.css -o /tmp/out.css`: confirms JIT props are injected.
- `grep -c "^\s*--" /tmp/out.css`: counts emitted custom properties (should be small with JIT).
- `npx playwright test --grep theme`: light and dark themes render with enough contrast.

## Test first
Assert the build includes only the props you use.
```ts
import postcss from "postcss";
import jit from "postcss-jit-props";
import OpenProps from "open-props";

test("JIT emits only used props", async () => {
  const out = await postcss([jit(OpenProps)]).process(
    `.a { padding: var(--size-3); }`, { from: undefined });
  expect(out.css).toContain("--size-3");
  expect(out.css).not.toContain("--size-10");
});
```

## Do
- Prefer `postcss-jit-props` with `OpenProps` so only the used variables ship; otherwise import specific files (`open-props/sizes.min.css`) not the whole bundle.
- Import normalize and theme files as needed (`open-props/normalize.min.css`, `open-props/buttons.min.css`).
- Reference tokens with `var(--size-4)`, `var(--gray-7)`, `var(--ease-3)`, `var(--shadow-2)`.
- Wrap overrides in `@layer` so your rules win predictably.
- Build themes by reassigning semantic variables under `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`, and set `color-scheme`.
- Use the `--ease-*` and `--animation-*` tokens, and set them to `none` under `prefers-reduced-motion`.
- Define project aliases (`--surface-1: var(--gray-0)`) so components never name raw palette steps.

## Avoid
- Importing `open-props/style` in full when you use a dozen tokens: about 15 KB of unused variables.
- Misspelled names: the variable silently resolves to nothing. Lint them.
- Hard-coding pixel values next to tokens.
- Components that reference palette steps directly: dark mode requires editing each one.
- Relying on `@custom-media` without the PostCSS plugin to process it.

## Review
- [ ] Only needed tokens ship (JIT or per-file imports).
- [ ] Unknown custom properties fail lint.
- [ ] Dark theme uses semantic aliases.
- [ ] Motion tokens respect reduced motion.
- [ ] Overrides live in a cascade layer.
