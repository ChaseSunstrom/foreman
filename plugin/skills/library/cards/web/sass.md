---
name: sass
title: Sass
area: web
tags: [sass, scss, css, styling, dart-sass, modules]
detect: [dep:sass, dep:sass-embedded, ext:.scss]
related: [tailwind, storybook]
---
Sass (Dart Sass) SCSS: modules with `@use`/`@forward`, mixins, functions and maps compiled to plain CSS.

## Verify
- `npx sass --no-source-map src/styles/main.scss /tmp/out.css`: compiles with no errors or deprecation warnings.
- `npx sass --load-path=node_modules src/main.scss /tmp/out.css`: bare package imports resolve.
- `npx stylelint "**/*.scss"`: lint, where configured.
- `npm run build`: the bundler's Sass pipeline.

## Test first
Test Sass functions and mixins with `sass-true` under a JS runner, or compile a fixture and assert on the CSS.
```scss
// _spacing.test.scss
@use "true" as *;
@use "spacing";

@include test("rem converts px") {
  @include assert-equal(spacing.rem(32px), 2rem);
}
```
If no harness exists, compile a small fixture with the Sass JS API and assert on the output string.

## Do
- Load files with `@use "path" as alias` and expose a public API from index files with `@forward`.
- Namespace everything: `colors.$primary`, `mixins.respond(md)`; use `as *` only for local helpers.
- Do math with `@use "sass:math"` and `math.div(a, b)`.
- Keep tokens in maps and read with `map.get($map, key)` (`@use "sass:map"`).
- Prefix private members with `-` or `_`; they are not visible outside the module.
- Limit nesting to about three levels and keep selectors flat.
- Mixins with `@content` for breakpoints; use `%placeholders` sparingly.
- Configure modules with `@use "lib" with ($var: value)`, once, at first load.
- Emit CSS custom properties for runtime theming and keep Sass for build-time logic.

## Avoid
- `@import`: deprecated, global namespace, duplicates output. Use `@use` and `@forward`.
- `/` for division (`$a / 2`): deprecated. Use `math.div`.
- `node-sass` and `LibSass`: unmaintained. Use `sass` (Dart Sass) or `sass-embedded`.
- Global built-ins (`map-get`, `darken`, `lighten`) in new code: deprecated. Use `map.get`, `color.adjust` or `color.scale`.
- Deep `&-suffix` nesting that hides final selectors: unsearchable. Write the selector out.
- `@extend` across modules and media queries: bloated, surprising CSS. Use mixins.
- Configuring a module in two places: error. Configure once at the entry point.

## Review
- [ ] Compile output has no deprecation warnings.
- [ ] All imports use `@use`/`@forward` with namespaces.
- [ ] Division goes through `math.div`.
- [ ] Nesting stays shallow and selectors remain greppable.
- [ ] Shared tokens live in one module.
