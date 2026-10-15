---
name: espresso
title: Espresso
area: jvm
tags: [android, testing, ui, instrumented, idling, flaky, matchers]
detect: [dep:espresso-core, dep:espresso-intents, dep:espresso-contrib, dep:espresso-idling-resource, dep:androidx.test.ext]
related: [android, jetpack-compose, hilt, android-navigation, android-workmanager, junit5]
---
Espresso for Android View UI tests: synchronized interactions, idling resources instead of sleeps, stable matchers, and a clean device state.

## Verify
- `./gradlew connectedDebugAndroidTest`: instrumented tests pass on a connected device or emulator.
- `./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.acme.LoginTest`: one class.
- `adb shell settings get global window_animation_scale`: animations are `0.0` (disable transition, window and animator scales for stability).
- `./gradlew lintDebug`: catches missing content descriptions the tests rely on.

## Test first
Tests live in `src/androidTest/java`. Arrange state, act through the UI, assert visible outcome.
```kotlin
@RunWith(AndroidJUnit4::class)
class LoginTest {
    @get:Rule val rule = ActivityScenarioRule(LoginActivity::class.java)

    @Test fun wrongPasswordShowsError() {
        onView(withId(R.id.email)).perform(typeText("a@x.com"), closeSoftKeyboard())
        onView(withId(R.id.password)).perform(typeText("bad"), closeSoftKeyboard())
        onView(withId(R.id.login)).perform(click())
        onView(withText(R.string.login_failed)).check(matches(isDisplayed()))
    }
}
```

## Do
- Use `ActivityScenarioRule` or `ActivityScenario.launch`; `FragmentScenario` (`launchFragmentInContainer`) for fragments.
- Register async work with `IdlingRegistry.getInstance().register(...)` (`CountingIdlingResource`, or the OkHttp idling resource), and unregister in `@After`.
- Prefer stable matchers: `withId`, `withText(R.string...)`, `withContentDescription`; combine with `allOf`, `isDescendantOfA`.
- Replace network and database with fakes through Hilt test modules (`@TestInstallIn`) or a `MockWebServer`.
- Scroll first for lists: `RecyclerViewActions.actionOnItemAtPosition` from `espresso-contrib`; `onData` for adapter views.
- Use Espresso-Intents (`Intents.init()`, `intended(hasComponent(...))`, `intending(...).respondWith(...)`) to stub external activities.
- Run with the Android Test Orchestrator (`testOptions.execution = "ANDROIDX_TEST_ORCHESTRATOR"`) and `clearPackageData` for isolation.
- Use `ViewAction` extensions for repeated interactions.

## Avoid
- `Thread.sleep` to wait for UI: flaky and slow. Use idling resources or `waitUntil`-style polling in the rule.
- Leaving device animations on: random failures. Disable the three scales in CI.
- Tests that depend on order or previous app state: use the orchestrator and `clearPackageData`.
- Matching on text that is localized or dynamic: break across locales. Use resource ids or `R.string`.
- Real network and real accounts: flaky and insecure. Fake the backend.
- Idling resource leaks (registered, never unregistered): later tests hang. Unregister in `@After`.
- Using Espresso on Compose screens: use `createAndroidComposeRule` and Compose test APIs.

## Review
- [ ] No sleeps; async work is exposed through idling resources.
- [ ] Matchers use ids or string resources.
- [ ] Backend is faked and tests are order independent.
- [ ] Animations disabled, orchestrator and `clearPackageData` configured in CI.
- [ ] Every UI test asserts a visible outcome.
