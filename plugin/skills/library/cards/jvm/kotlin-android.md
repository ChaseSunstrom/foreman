---
name: kotlin-android
title: Kotlin Android plugin
area: jvm
tags: [kotlin, android, gradle, plugin, build, jvm-target]
detect: [dep:org.jetbrains.kotlin.android]
related: [android, gradle, kotlin, kotlin-coroutines, jetpack-compose]
---
The `org.jetbrains.kotlin.android` Gradle plugin compiles Kotlin in Android modules; its version must match the Android Gradle Plugin and the Kotlin toolchain.

## Verify
- `./gradlew :app:assembleDebug`: the Android module compiles Kotlin with the plugin applied.
- `./gradlew testDebugUnitTest`: Kotlin unit tests compile and run on the JVM.
- `./gradlew :app:dependencies --configuration debugRuntimeClasspath | grep kotlin-stdlib`: one stdlib version resolves.
- `grep -rn "org.jetbrains.kotlin.android" --include=*.kts --include=*.gradle --include=*.toml .`: the plugin is declared once, in the root or the module that uses it.

## Test first
Test the Kotlin code the module compiles, through the unit test task.
```kotlin
// app/src/test/java/com/example/PriceTest.kt
import org.junit.Assert.assertEquals
import org.junit.Test

class PriceTest {
    @Test
    fun totalAppliesDiscount() {
        assertEquals(90, Price.total(quantity = 1, unitCents = 100, discountPercent = 10))
    }
}
```

## Do
- Declare the plugin once with `apply false` in the root build file, and apply it in each Android module that has Kotlin.
- Keep the Kotlin plugin version in the version catalog (`gradle/libs.versions.toml`) with the AGP version it was tested with.
- Set the JVM target in one place for the module, and keep it the same as the Java toolchain.
- Run `./gradlew testDebugUnitTest` after changing the plugin version.

## Avoid
- Two Kotlin plugin versions in the build: the compile uses one and the IDE another. Pin one in the catalog.
- Mixing a Kotlin plugin version that the AGP in use does not support: the sync or the build fails. Check the compatibility table of both.
- Declaring the plugin in every subproject with a version: the versions drift apart. Use `apply false` at the root.
- Setting different JVM targets for Java and Kotlin in one module: the build fails with a mismatch error.
- Editing generated sources under `build/`: the next build overwrites them.
- Upgrading the plugin in the same change as a feature: a failing build then has two causes. Upgrade alone, test, then merge.

## Review
- [ ] One plugin version, pinned in the version catalog.
- [ ] Root applies it with `apply false`; modules apply it by id.
- [ ] Java and Kotlin JVM targets match.
- [ ] `testDebugUnitTest` and `assembleDebug` pass after any version change.
- [ ] No generated code under `build/` is edited.
