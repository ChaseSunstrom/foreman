---
name: gradle-version-catalogs
title: Gradle version catalogs
area: jvm
tags: [gradle, dependencies, toml, versions, bom, plugins, multi-module]
detect: [file:gradle/libs.versions.toml, file:libs.versions.toml]
related: [gradle, maven, detekt, ktlint, kotlin-multiplatform, android]
---
Gradle version catalogs: all dependency, plugin and version declarations in `gradle/libs.versions.toml`, consumed as type-safe `libs.*` accessors.

## Verify
- `./gradlew help`: the catalog parses and the build configures.
- `./gradlew dependencies --configuration runtimeClasspath`: resolved versions match the catalog.
- `./gradlew :app:dependencyInsight --dependency okhttp --configuration runtimeClasspath`: why a version won.
- `grep -rnE "implementation\(\"[^\"]+:[^\"]+:[^\"]+\"\)" --include=*.kts .`: hardcoded coordinates left outside the catalog.

## Test first
The failing check is a build script that references a missing alias: configuration fails.
```kotlin
// app/build.gradle.kts
dependencies { implementation(libs.okhttp) }
```
```
$ ./gradlew help
Unresolved reference: okhttp
```
Add the entry to the catalog, rerun `./gradlew help`, then `dependencies` to confirm the resolved version.

## Do
- Layout of `gradle/libs.versions.toml`: `[versions]`, `[libraries]`, `[bundles]`, `[plugins]` tables.
- Declare libraries as `okhttp = { module = "com.squareup.okhttp3:okhttp", version.ref = "okhttp" }`; share one `version.ref` across related artifacts.
- Declare plugins in `[plugins]` and apply with `alias(libs.plugins.kotlin.jvm)`; in the root `plugins {}` use `apply false`.
- Use `[bundles]` for always-together groups (for example test libs).
- Import BOMs with `implementation(platform(libs.spring.bom))` and omit versions for managed libraries.
- Use rich versions in the catalog (`version = { strictly = "[1.0, 2.0[", prefer = "1.5" }`) only for real constraints.
- Name aliases with dashes or underscores (`kotlinx-coroutines-core` becomes `libs.kotlinx.coroutines.core`); keep names consistent.
- Put build-logic and convention plugins in `build-logic` (included build) so modules share config; reuse the catalog there via `versionCatalogs`.
- Settings-level `dependencyResolutionManagement { repositories { ... } }` with `repositoriesMode`.

## Avoid
- Inline `"group:name:1.2.3"` strings in modules: version drift. Move to the catalog.
- Alias names that collide at a prefix (`ktor` and `ktor-client`): Gradle forbids it. Use `ktor-core`, `ktor-client-core` or reshape.
- Duplicating a version string across libraries: use `version.ref`.
- Hand-editing and forgetting the catalog name: the default is `libs`; extra catalogs need `versionCatalogs { create("x") { from(files(...)) } }` in settings.
- Using the catalog accessor in `buildSrc` or `settings.gradle` plugin blocks where it is not available: read it via `extensions.getByType<VersionCatalogsExtension>()`.
- Relying on dynamic versions (`+`, `latest.release`): non-reproducible builds. Pin and enable dependency locking if needed.

## Review
- [ ] No hardcoded coordinates or versions in module scripts.
- [ ] Shared versions use `version.ref`; BOMs are used where available.
- [ ] Plugins are aliased, not versioned in each module.
- [ ] Alias naming is consistent and collision free.
- [ ] Dependency changes show up in `dependencies` output as intended.
