<!-- Foreman's own playbook (written for Foreman, not ported). -->
# JVM build errors (Gradle, Maven, Java, Kotlin)

Use when a Gradle or Maven build of Java or Kotlin code fails: in configuration, dependency resolution or
compilation. Test failures are a different job (see `references/verify/`). The goal is a green build with the
smallest diff that fixes the cause. Built on the library cards `fm lib show java`, `fm lib show kotlin`,
`fm lib show gradle`, `fm lib show gradle-version-catalogs` and `fm lib show maven`.

## Diagnostic commands

```bash
./gradlew --version                                   # Gradle, Kotlin and the JVM Gradle runs on
./gradlew build --console=plain 2>&1 | tail -60       # plain output, no progress bar interleaving
./gradlew :app:dependencies --configuration compileClasspath
./gradlew :app:dependencyInsight --dependency jackson-databind --configuration runtimeClasspath
./mvnw -v                                             # Maven and its JDK
./mvnw -B -e compile 2>&1 | tail -60                  # batch mode: no colour codes, full error
./mvnw -B dependency:tree -Dincludes=com.fasterxml.jackson.core
```

Always the wrapper (`./gradlew`, `./mvnw`), never a system `gradle` or `mvn`: the wrapper pins the version the
project was written for.

## First error

1. **Name the phase.** Gradle's `* What went wrong:` block says which: `A problem occurred evaluating project` or
   `A problem occurred configuring project` (build script), `Could not resolve all files for configuration`
   (dependencies), `Execution failed for task ':app:compileJava'` or `':app:compileKotlin'` (compilation).
   Maven's equivalent is the `Failed to execute goal` line: the plugin in it (`maven-compiler-plugin`,
   `maven-enforcer-plugin`, `maven-surefire-plugin`) names the phase. Pass: you state the phase before editing.
2. **For compilation, read above the summary.** `Execution failed for task` only names the task; the compiler's own
   lines are higher up:
   - javac: `src/main/java/app/Store.java:42: error: cannot find symbol`, then `symbol:` and `location:` lines.
   - Maven: `[ERROR] /…/Store.java:[42,17] cannot find symbol` (line, column in brackets).
   - Kotlin: `e: file:///…/Store.kt:42:17 Unresolved reference 'save'.` (`e:` is an error, `w:` a warning).
3. **Fix the first compiler error only, then rebuild.** javac reports parse errors (`';' expected`,
   `class, interface, enum, or record expected`) before any type errors, so a file with a syntax slip hides its
   other errors; one missing brace can produce dozens of lines. javac also stops at 100 errors.
4. **Rerun a configuration failure with `--stacktrace`**, and read the deepest `Caused by:`; it names the plugin or
   script line. Use `--stacktrace` only there: compile errors don't need it.

## Common causes

| Error text | Usual cause | Fix |
|---|---|---|
| `cannot find symbol` / `Unresolved reference 'x'` | Typo, missing import, or the dependency is not on this module's classpath | Import it, or add the dependency to this module (Gradle `implementation` is not transitive to consumers; `api` is) |
| `package com.acme.x does not exist` | Dependency missing from this module's build file | Add it to the module that uses it, in the version catalog if the project has one |
| `cannot find symbol` on a getter of a Lombok or MapStruct class | Annotation processor not configured | `annotationProcessor` (Gradle) or `<annotationProcessorPaths>` (Maven) for the processor; `kapt`/`ksp` in Kotlin |
| `incompatible types: String cannot be converted to int` / Kotlin `Type mismatch` or `Argument type mismatch` | Wrong type | Convert explicitly (`Integer.parseInt`, `toInt()`); don't cast through `Object` |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver` | Kotlin nullability | Handle null (`?.`, `?:`, an early return); `!!` only with a comment saying why it can't be null |
| `Could not resolve all files for configuration ':app:compileClasspath'` + `Could not find g:a:v` | Wrong coordinates or version, missing repository, offline | Check the coordinates on the repository; add the repository; drop `--offline` |
| `error: release version 21 not supported` / `invalid target release` | JDK older than the target | Configure a toolchain (`java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }`) or `maven.compiler.release` matching an installed JDK |
| `class file has wrong version 65.0, should be 61.0` | A dependency built for Java 21 on a Java 17 compile | Raise the toolchain to the dependency's level, or use a dependency version built for yours (major 61 = 17, 65 = 21, 69 = 25) |
| `Unsupported class file major version N` during configuration | Gradle itself running on a JDK newer than it supports | Upgrade the wrapper (`./gradlew wrapper --gradle-version …`) or run Gradle on an older JDK via `JAVA_HOME` |
| `Duplicate class x found in modules a and b` | Two artifacts ship the same class | Find both with `dependencyInsight`, exclude one or align versions with a BOM/platform |
| `unmappable character for encoding` | Source read in the platform charset | Set UTF-8: `tasks.withType<JavaCompile> { options.encoding = "UTF-8" }` or `project.build.sourceEncoding` |

## Verify

```bash
./gradlew build --console=plain      # Gradle: compiles, runs tests and checks
./mvnw -B verify                     # Maven: through integration tests
```

Pass: exit 0 and the last lines say `BUILD SUCCESSFUL` (Gradle) or `BUILD SUCCESS` (Maven). A multi-module change
builds from the root, not one module.

## Rules

- The command in your evidence starts with `./gradlew` or `./mvnw`.
- No new `@SuppressWarnings`, `@Suppress`, `-Xlint:none`, `-nowarn`, `allWarningsAsErrors = false` or
  `-Dmaven.test.skip=true` in the diff to make a build pass.
- Dependency versions change in one place: the version catalog (`libs.versions.toml`) or the parent POM's
  `<dependencyManagement>`, when the project has one.
- Rebuild after each fix and read the new output; don't fix from stale lines.

## Stop conditions

Stop and report when the same error survives three fixes, when the fix needs a JDK or Gradle upgrade the project
hasn't agreed to, or when a dependency conflict can only be solved by changing a public API.

## Report

```text
[FIXED] app/src/main/kotlin/app/Store.kt:42:17  Unresolved reference 'save'
Fix: added implementation(libs.exposed.jdbc) to app/build.gradle.kts
Build: ./gradlew build BUILD SUCCESSFUL | files: app/build.gradle.kts
```
