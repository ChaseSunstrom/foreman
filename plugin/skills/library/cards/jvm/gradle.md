---
name: gradle
title: Gradle
area: jvm
tags: [gradle, build, kotlin-dsl, java, dependencies, ci]
detect: [file:build.gradle, file:build.gradle.kts, file:settings.gradle, file:settings.gradle.kts, file:gradlew]
related: [maven, junit5, kotlin-multiplatform, android, spring-boot]
---
Gradle builds: wrapper, Kotlin DSL, version catalogs, convention plugins, configuration cache.

## Verify
- `./gradlew build`: compile, test and assemble through the pinned wrapper.
- `./gradlew dependencies --configuration runtimeClasspath`: what actually resolves at runtime.
- `./gradlew build --configuration-cache`: tasks are cache-compatible.
- `./gradlew help --task test`: confirms the task exists before scripting it.
- `./gradlew build --scan` is optional; skip it where scans are not permitted.

## Test first
Tests live in `src/test` (and `src/integrationTest` through a separate source set or the JVM Test Suite plugin). For build logic, use a failing check on the task wiring.
```kotlin
// build.gradle.kts
testing {
    suites {
        val test by getting(JvmTestSuite::class) { useJUnitJupiter() }
    }
}
tasks.named("check") { dependsOn(tasks.named("test")) }
```
Make the first failing check `./gradlew test` with one new test that fails.

## Do
- Commit `gradlew`, `gradlew.bat` and `gradle/wrapper/`; upgrade with `./gradlew wrapper --gradle-version <v>`.
- Prefer the Kotlin DSL (`build.gradle.kts`) and declare versions in `gradle/libs.versions.toml`, referenced as `libs.foo`.
- Use `implementation` for internals and `api` only in `java-library` modules for public types.
- Share logic through convention plugins in `build-logic` or `buildSrc`, not copy-pasted blocks.
- Set `kotlin { jvmToolchain(21) }` or `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` so builds don't depend on the local JDK.
- Use lazy task registration: `tasks.register<T>("name")`.
- Enable `org.gradle.caching=true` and `org.gradle.parallel=true` in `gradle.properties`.

## Avoid
- `compile` and `testCompile` configurations: removed. Use `implementation` and `testImplementation`.
- `tasks.create` and `allprojects {}` or `subprojects {}` cross-configuration: eager and fragile. Use `register` and convention plugins.
- Dynamic versions (`1.+`, `latest.release`): non-reproducible. Pin them, or use a catalog with a lockfile.
- A system `gradle` instead of `./gradlew`: version drift.
- Reading files or environment at configuration time: breaks configuration cache. Use providers (`providers.environmentVariable`).
- Committing credentials in `gradle.properties`: use `~/.gradle/gradle.properties` or env vars.

## Review
- [ ] Wrapper committed and the distribution has a checksum if the project pins one.
- [ ] Dependencies come from the catalog with no stray dynamic versions.
- [ ] Toolchain declared; CI uses the wrapper.
- [ ] Tasks are lazy and declare inputs and outputs.
- [ ] No secrets in build files.
