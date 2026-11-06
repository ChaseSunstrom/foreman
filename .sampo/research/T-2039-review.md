**Not checked:** I read about 25 cards in full and ran grep across the rest. I had no network and could not run any command, so package and flag claims come from my own knowledge. I marked each finding with a confidence. Card names do not collide between T-2039 and T-2042: the 25 and 25 are disjoint, and there is no existing `cards/ux/`. The README "29 areas" edit is correct, since `ux` is a new area.

## T-2039 (product patterns)

## lens: adversary/edge
- MEDIUM — `cards/ux/{filters-and-facets:14, empty-states:15, tooltips-and-coachmarks:13, error-messages:14, multi-step-wizards:14, destructive-actions:14, settings-pages:14, command-palette:13, undo-patterns:15, mobile-navigation:14, progressive-disclosure:13, sign-up-flows:14, navigation-patterns:14, checkout-flows:13, notification-design:15}.md` — `npx axe-core-cli` is not the axe CLI. The package is `@axe-core/cli`, which other cards already use. The `--viewport 375x667` flag in `mobile-navigation.md:14` is not an axe option. — Replace with `npx @axe-core/cli <url>`. In `mobile-navigation` drop `--viewport` and use the Playwright `iPhone 13` test plus `AxeBuilder`. — high (axe CLI name), medium (package existence)
- MEDIUM — `cards/ux/information-architecture.md:19-26` — the first test asserts `depth <= 3` on a static `sitemap.json` fixture, so it cannot fail when the site changes. — Compute depth by crawling nav links in Playwright, or drop the fixture loop. — high
- LOW — `cards/ux/permission-prompts.md:21-26` — the test is named "denial leaves the app usable" but never denies anything. — Add a context without the permission and assert the fallback UI. — high
- LOW — `cards/ux/ux-writing.md:15` — `npx alex` flags insensitive wording and does not measure reading grade. — Say "alex checks inclusive wording" and name a separate readability tool. — high
- LOW — `cards/ux/information-architecture.md:13` — `broken-link-checker` finds dead links, not orphan pages, and is unmaintained. — Reword to "dead links", or cross-check the sitemap against the nav. — medium

## T-2042 (visual design)

## lens: adversary/edge
- MEDIUM — `cards/ux/color-palettes.md:13`, `calls-to-action.md:14`, `chart-design.md:14` — Verify runs `node scripts/contrast.mjs` and `python3 scripts/cvd_check.py`, which exist in no repo. — Move them out of backticks as "write a script that…", or give runnable code. For contrast, use `AxeBuilder.withRules(['color-contrast'])`. — high
- MEDIUM — `cards/ux/color-palettes.md:18-31` — the test hard-codes four colours, so it checks the arithmetic and not the repo's tokens. — Read the pairs from the token file. — high
- MEDIUM — `cards/ux/spacing-scales.md:13` — `stylelint --rule '{…}'` is not a CLI flag, and stylelint needs a config. Also, `"0"` does not match `margin: 0 auto`. — Put the rule in a `--config` file. — high
- MEDIUM — `cards/ux/app-icons-and-favicons.md:14` — Lighthouse 12 removed the `pwa` category. — Use `jq` on the manifest plus a Playwright check instead. — medium-high
- MEDIUM — `cards/ux/chart-design.md:15` — a bare `npx axe` does not resolve to `@axe-core/cli`. — Use `npx @axe-core/cli`. — medium
- LOW — `cards/ux/design-tokens.md:26` — `v.get` crashes on W3C group-level `$type`/`$description` strings. The docstring also promises a dark-value check that does not exist. — Add `isinstance(v, dict)` handling and drop the dark-value claim from the docstring. — high
- LOW — `cards/ux/type-scales.md:37` — the step for ratio 1.25 should be 0.8, not 0.833 (that is 1/1.2). Line 31 asserts ≤80 characters while the card says 45-75. — Fix both numbers. — high
- LOW — `cards/ux/social-share-images.md:24` — `expect(url).toMatch(/^https:/)` fails against a localhost dev server. — Allow `http` on localhost. — medium

## T-2043 (motion and modern CSS)

## lens: adversary/edge
- MEDIUM — `cards/frontend/scroll-driven-animations.md:37` — it says Safari 26 is behind or flagged. Safari 26 shipped scroll-driven animations, and `anchor-positioning.md:36` already lists Safari 26 for anchor positioning. — "Chromium and Safari 26+; Firefox flagged". — medium-high
- MEDIUM — `cards/frontend/anchor-positioning.md:36,44` — "Firefox is behind". I believe Firefox 147 (Jan 2026) shipped it, so by Oct 2026 this is stale. — Say "Firefox 147+; verify on caniuse". — medium
- MEDIUM — `cards/frontend/anchor-positioning.md:13` — `--project=webkit` "confirms the fallback", but WebKit supports anchor positioning. — Stub with `@supports`, or use an older Firefox project. — medium
- MEDIUM — `cards/frontend/variable-fonts.md:12` — `npx fonttools` is wrong. fonttools is a Python tool. — `fonttools varLib.instancer --help` without `npx`. — high
- MEDIUM — `cards/frontend/oklch-color.md:13` — `npx culori --help`: I do not believe culori ships a CLI. — Use `node -e "import('culori').then(c=>…)"`. — medium
- LOW — `cards/frontend/{scroll-snap-carousels,popover-api,kinetic-typography,blend-modes,frosted-glass,progress-indicators,gradient-design}.md:13` — `npx axe-cli` is the deprecated name, and `@axe-core/cli` is used elsewhere. — Use `npx @axe-core/cli`. — medium
- LOW — `cards/frontend/haptic-feedback.md:20,27` — the test title promises "missing API does not throw" but never tests it. `buzz(10)` pushes `10`, not `[10]`. — Add the missing-API case and fix the expected value. — medium

## T-2044 (web libraries)

## lens: adversary/edge
- MEDIUM — `cards/web/floating-ui.md:37` — "Add `arrow()` before others" is wrong. Floating UI places `arrow()` after `offset`, `flip` and `shift`. — Fix the ordering sentence. — medium-high
- MEDIUM — `cards/web/daisyui.md:13,30,43` — "v4 uses `@plugin`…" mixes up daisyUI and Tailwind majors. The `@plugin "daisyui" { themes: … }` syntax is daisyUI 5 with Tailwind 4. daisyUI 4 and 3 use `require("daisyui")`. — Rewrite as "daisyUI 5 / Tailwind 4 vs daisyUI ≤4 / Tailwind 3". — high
- MEDIUM — `cards/web/gsap.md:15` — `vite build --report` is not a Vite flag, and the build output does not list GSAP plugins. — Use `grep -l ScrollTrigger dist/assets/*.js` or `vite-bundle-visualizer`. — medium-high
- LOW — `cards/web/gsap.md:27` — `globalTimeline.progress(1)` does not reliably finish tweens. — Return the timeline from `buildIntro` and call `tl.progress(1)`. — medium
- LOW — `cards/web/lenis.md:22-27` — in jsdom there is no layout, so the scroll limit is 0 and `scrollTo(400)` clamps to 0. — Move the test to Playwright. — medium
- LOW — `cards/web/auto-animate.md:17-28` — the test never exercises auto-animate, and it claims to disable the animation via the controller but does not. — Call `enable(false)` or reword. — high
- LOW — `cards/web/open-props.md:13` — `npx postcss` needs `postcss-cli`. — `npx postcss-cli`. — medium
- LOW — `cards/web/pixijs.md:22-30` and `cards/web/rive.md:22` — their test-first examples need a real WebGL or canvas context, not jsdom. — Add a "run in browser mode" note. — medium

The v8 `extract.pixels`, tweakpane v4 `exportState`, anime v4 `createScope` and `svg.createDrawable`, embla `stopOnInteraction`, the unocss CLI and the panda `codegen`/`analyze` commands all checked out. `panda --minify` is probably fine.

## Verdicts
- T-2039: merge after fixes (the axe lines).
- T-2042: merge after fixes (the scripts, stylelint, the palette test, the Lighthouse category).
- T-2043: merge after fixes (the support claims, the two nonexistent `npx` tools).
- T-2044: merge after fixes (the floating-ui order, the daisyui majors, the gsap flag).

**Noticed:** `_card_problems` cannot check that a Verify `npx` package or flag exists. A small allowlist or a "your script" lint would have caught the `axe-core-cli`, `scripts/*.mjs` and `stylelint --rule` cases. Four lanes of builders all invented the axe CLI name differently (`axe-core-cli`, `axe-cli`, `axe`), so a shared snippet would prevent that.
