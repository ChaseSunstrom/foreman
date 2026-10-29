---
name: unocss
title: UnoCSS
area: web
tags: [unocss, atomic-css, presets, utility-first, vite]
detect: [dep:unocss, dep:@unocss/preset-uno, dep:@unocss/vite, file:uno.config.*]
related: [tailwind, css-custom-properties, vue, web-performance]
---
UnoCSS: on-demand atomic CSS engine; behavior is defined entirely by the presets, rules and shortcuts in `uno.config`.

## Verify
- `npx unocss "src/**/*.{ts,tsx,vue,html}" -o /tmp/uno.css`: generates CSS from sources via the CLI.
- `npx tsc --noEmit`: config types with `defineConfig`.
- `npx vite build`: bundles with the plugin; check CSS size.
- `npx unocss --help`: confirms the installed CLI if the command above differs.

## Test first
Generate CSS for a class string and assert on the output.
```ts
import { createGenerator } from "unocss";
import config from "../uno.config";

test("custom shortcut expands to real rules", async () => {
  const uno = await createGenerator(config);
  const { css } = await uno.generate("btn p-4", { preflights: false });
  expect(css).toContain("padding:1rem");
  expect(css).toMatch(/\.btn/);
});
```

## Do
- Choose presets explicitly: `presetWind3()` or `presetWind4()` for Tailwind-like utilities, `presetIcons()`, `presetAttributify()` only if you want that style.
- Add the Vite plugin before framework plugins and `import "virtual:uno.css"` once in the entry.
- Define repeated patterns as `shortcuts`; add `theme` values rather than arbitrary values.
- Use `presetIcons` with `@iconify-json/*` sets; only the used icons are bundled.
- Use `safelist` or `blocklist` for classes assembled at runtime.
- Use `transformerVariantGroup` and `transformerDirectives` when you rely on `hover:(a b)` or `@apply`.
- Configure `content.pipeline.include` when classes live outside normal source globs.

## Avoid
- Building class names by concatenation (`"p-" + n`): the extractor misses them. Use full strings or `safelist`.
- Installing several overlapping presets (Uno and Wind both): duplicate and conflicting rules.
- Skipping the virtual import: no CSS ships.
- Using Attributify mode without the TypeScript types and lint support.
- Keeping unused icon collections as deps.

## Review
- [ ] Presets are explicit and not overlapping.
- [ ] Runtime classes are safelisted.
- [ ] A test generates CSS for key shortcuts.
- [ ] Output CSS size is checked after build.
- [ ] Dark mode strategy is set (class or media).
