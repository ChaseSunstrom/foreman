---
name: robolectric
title: Robolectric
area: jvm
tags: [android, robolectric, unit-tests, jvm, activity, looper]
detect: [dep:org.robolectric:robolectric]
related: [android, junit4, espresso, jetpack-compose, gradle]
---
Robolectric runs Android framework code on the JVM, so activity and view tests run in `testDebugUnitTest` without a device.

## Verify
- `./gradlew testDebugUnitTest`: Robolectric tests run on the local JVM.
- `./gradlew testDebugUnitTest --tests 'com.example.MainActivityTest'`: one class runs alone.
- `./gradlew :app:dependencies --configuration debugUnitTestRuntimeClasspath | grep robolectric`: one Robolectric version resolves.
- `grep -n "isIncludeAndroidResources" app/build.gradle*`: resources are on the unit-test classpath, so layouts inflate.

## Test first
Build the activity and read a view from its layout.
```kotlin
import android.widget.TextView
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner

@RunWith(RobolectricTestRunner::class)
class MainActivityTest {
    @Test fun showsGreetingOnCreate() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).create().get()
        val greeting = activity.findViewById<TextView>(R.id.greeting)
        assertEquals("Hello", greeting.text.toString())
    }
}
```

## Do
- Set `unitTests.isIncludeAndroidResources = true` in `testOptions` so layouts and strings load.
- Use `ApplicationProvider.getApplicationContext()` for a `Context` in a test.
- Drive the main looper with `ShadowLooper.idleMainLooper()` after posting work, instead of sleeping.
- Use `Robolectric.buildActivity(...)` and step it through `create()`, `start()`, `resume()` to test lifecycle.
- Pin the SDK level in `@Config` when the test depends on platform behavior.
- Keep the runner on JUnit 4: `RobolectricTestRunner` is a JUnit 4 runner, so JUnit 5 tests need the vintage engine or a separate task.

## Avoid
- Sleeping or polling for a background task: the test is slow and flaky. Idle the looper or inject an executor.
- Assuming a real device behavior: Robolectric uses shadows, which approximate platform code. Cover the real behavior in an instrumented test.
- Leaving `isIncludeAndroidResources` off, then wondering why `R.layout` inflates to nulls or throws.
- Downloading the Android framework jars on every CI run without a cache: it is slow and needs network access. Cache the Gradle home.
- Testing Compose UI with Robolectric alone: use the Compose test rule (see the jetpack-compose card) for those assertions.
- Sharing a static `Application` across tests: state carries over. Reset it in `@Before`.

## Review
- [ ] `testDebugUnitTest` runs the Robolectric tests with a non-zero count.
- [ ] Resources are on the unit-test classpath.
- [ ] No sleeps: the looper is idled or work is injected.
- [ ] A device-only behavior has an instrumented test as well.
- [ ] The Gradle cache for the Android framework jars is kept in CI.
