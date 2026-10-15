---
name: vanilla-extract
title: vanilla-extract
area: web
tags: [vanilla-extract, css-in-ts, zero-runtime, recipes, themes, sprinkles]
detect: [dep:@vanilla-extract/css, dep:@vanilla-extract/recipes, dep:@vanilla-extract/sprinkles, dep:@vanilla-extract/vite-plugin]
related: [tailwind, sass, react]
---
vanilla-extract: type-safe, zero-runtime CSS authored in .css.ts files, with themes, recipes and sprinkles.

## Verify
- `npx tsc --noEmit`: style objects, theme contracts and recipe variants type-check.
- `npm run build`: the bundler plugin extracts CSS at build time; errors here mean a bad `.css.ts` import.
- `npx vitest run`: logic tests; the Vite plugin must be configured for Vitest or style files mocked.
- `npx eslint .`: lint.

## Test first
Keep style tokens and recipe outputs checkable: the first failing check is the type or build error for a variant you have not defined yet.
```ts
// button.css.test.ts (needs the vanilla-extract plugin in the test config)
import { button } from "./button.css";

test("danger large returns class names", () => {
  const cls = button({ tone: "danger", size: "lg" });
  expect(typeof cls).toBe("string");
  expect(cls.split(" ").length).toBeGreaterThan(1);
});
```

## Do
- Name files `*.css.ts`; export styles from them and import into components like any module.
- Use `style({...})` for single classes, `styleVariants` for keyed sets, `globalStyle` for resets and element selectors.
- Define tokens with `createTheme(vars)` or `createThemeContract` plus `createTheme(contract, values)`; swap themes by applying the class to a root element.
- Use `recipe({ base, variants, defaultVariants, compoundVariants })` from `@vanilla-extract/recipes` and `RecipeVariants<typeof x>` for prop types.
- Use `@vanilla-extract/sprinkles` (`defineProperties`, `createSprinkles`) for atomic utility props.
- Write selectors with the `selectors` key and `&` self reference, and media or supports queries inside `@media` keys.
- Use `vars` references (`vars.color.brand`) instead of repeating literal values.
- Add the plugin for your bundler (Vite, esbuild, webpack, Next plugin) and confirm it in the config.

## Avoid
- Importing a `.css.ts` file from server or test code without the plugin: it throws about running outside a build. Configure the plugin or mock it.
- Doing runtime logic in `.css.ts` (reading props, `window`): styles are evaluated at build time. Use variants or CSS variables via `assignInlineVars`.
- Selectors targeting a class from another file by string: breaks hashing. Reference the exported class in `selectors`.
- Plain object nesting like Sass (`&:hover` as a top-level key): use `":hover": {...}` or `selectors`.
- Creating `style()` calls in a loop at runtime: they must be module-level and static.
- Skipping `defaultVariants`: components render unstyled when a variant prop is omitted.

## Review
- [ ] All style authoring lives in `*.css.ts` and the plugin is wired for build and tests.
- [ ] Tokens come from theme vars, and themes share one contract.
- [ ] Recipes declare defaults, and component props use `RecipeVariants`.
- [ ] Dynamic values flow through `assignInlineVars`, not runtime style calls.
- [ ] The production build outputs one extracted stylesheet and no runtime style engine.
