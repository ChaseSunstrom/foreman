---
name: ktlint
title: ktlint
area: jvm
tags: [kotlin, lint, format, style, editorconfig, gradle, ci]
detect: [dep:ktlint-cli, dep:ktlint-gradle]
related: [detekt, gradle, kotest, jetpack-compose, gradle-version-catalogs]
---
ktlint for Kotlin style: formatting rules configured in `.editorconfig`, enforced in CI by a check task and fixed locally by a format task.

## Verify
- `./gradlew ktlintCheck`: style violations fail the build (with the jlleitschuh Gradle plugin).
- `./gradlew ktlintFormat`: auto-fixes what rules can fix; review the diff afterward.
- `ktlint "src/**/*.kt"`: standalone CLI check over sources.
- `ktlint -F "src/**/*.kt"`: standalone CLI format.

## Test first
The check that fails first is the lint run on the offending file.
```
$ cat src/main/kotlin/Bad.kt
fun f( a:Int ):Int{ return a+1 }
$ ./gradlew ktlintCheck
> Task :ktlintMainSourceSetCheck FAILED
Bad.kt:1:7: Unexpected spacing ...
```
Add the failing sample or fix before changing rules; then format and rerun until exit 0. Custom rules get a unit test with the ktlint rule-test library.

## Do
- Put all style config in `.editorconfig` (`[*.{kt,kts}]` section): `max_line_length`, `indent_size`, and `ktlint_code_style` (`ktlint_official` is the default in recent versions).
- Disable single rules with `ktlint_standard_<rule-id> = disabled` and a comment, not by turning ktlint off.
- Pin the ktlint engine version in the plugin config so CI and IDE agree.
- Wire `ktlintCheck` into `check` so `./gradlew check` enforces it.
- Use a baseline file only when adopting on a legacy codebase, and shrink it.
- Run the format task before committing generated or large refactors, in its own commit.
- Exclude generated sources (`build/generated`) from the lint filter.
- Keep ktlint for formatting and `detekt` for code smells; do not duplicate rules.

## Avoid
- Old `disabled_rules` key: removed in recent versions. Use per-rule `ktlint_standard_*` properties.
- Fixing style by hand across the repo in a feature PR: noisy diffs. Run `ktlintFormat` separately.
- Different ktlint versions in IDE plugin, Gradle and pre-commit: flapping results. Pin one.
- `@Suppress("ktlint:...")` sprinkled widely: scope it to the smallest element and justify it.
- Mixing code styles (`intellij_idea`, `android_studio`, `ktlint_official`) between modules: inconsistent formatting. Set one root `.editorconfig`.
- Linting generated code: unfixable failures. Exclude it.

## Review
- [ ] `ktlintCheck` passes locally and runs in CI via `check`.
- [ ] `.editorconfig` holds the only style config; rule disables are commented.
- [ ] Tool version is pinned in one place.
- [ ] Formatting-only changes are separate from behavior changes.
