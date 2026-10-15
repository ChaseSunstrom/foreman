---
name: detekt
title: detekt
area: jvm
tags: [kotlin, static-analysis, lint, complexity, sarif, gradle, ci]
detect: [dep:detekt-cli, dep:detekt-gradle-plugin, dep:detekt-formatting, file:detekt.yml, file:detekt-baseline.xml, file:config/detekt/detekt.yml]
related: [ktlint, gradle, kotest, gradle-version-catalogs, kotlin-coroutines]
---
detekt static analysis for Kotlin: a config file of rule sets, a baseline for legacy findings, and a Gradle task wired into `check`.

## Verify
- `./gradlew detekt`: analysis runs and fails on findings above the configured threshold.
- `./gradlew detektBaseline`: writes a baseline of existing findings (use once, deliberately).
- `./gradlew detektGenerateConfig`: generates the default config to start from.
- `./gradlew check`: detekt is part of the standard verification.

## Test first
The failing check is detekt on a sample that breaks a rule.
```kotlin
// src/main/kotlin/Bad.kt
fun risky() {
    try { work() } catch (e: Exception) { }   // SwallowedException / EmptyCatchBlock
}
```
```
$ ./gradlew detekt
Bad.kt:2:... [EmptyCatchBlock] ...
BUILD FAILED
```
Fix the code, rerun until green. Custom rules get a test with the detekt test utilities and `lint(...)`.

## Do
- Set `buildUponDefaultConfig = true` and keep `config/detekt/detekt.yml` as overrides only.
- Set `allRules = false` and enable extra rule sets (`detekt-formatting` wraps ktlint, `detekt-rules-libraries`) explicitly.
- Set `maxIssues: 0` in `build:` so findings fail the build; use `weights` for finer control.
- Emit reports in CI (`reports { sarif.required.set(true) }`) for code scanning.
- Enable type resolution with the `detektMain` and `detektTest` tasks for rules that need symbols (for example `UnreachableCode`, `IgnoredReturnValue`).
- Suppress at the narrowest scope with `@Suppress("RuleName")` and a reason.
- Run the baseline once on legacy code, commit it, and burn it down.
- Keep the plugin version aligned with the Kotlin compiler line it supports.

## Avoid
- Running only plain `detekt` and expecting type-resolution rules: they are skipped. Run `detektMain`/`detektTest` in CI.
- Raising thresholds (`threshold`, `maxIssues`) to make a build pass: hides debt. Fix findings or baseline them.
- Regenerating the baseline on every failure: it masks new issues. Only regenerate when intentionally accepting existing ones.
- Copying the full default config into the repo: it drifts from upgrades. Keep overrides only.
- Mismatched detekt and Kotlin versions: crashes with metadata errors. Use the version built for your Kotlin.
- Disabling a rule globally because one file trips it: suppress locally.

## Review
- [ ] `./gradlew detekt` passes with `maxIssues: 0` and runs under `check`.
- [ ] Config contains only deliberate overrides, with comments for relaxed rules.
- [ ] Baseline is committed and not growing.
- [ ] Suppressions are scoped and explained.
- [ ] Type-resolution tasks run in CI.
