---
name: android-car-app
title: Android Car App Library
area: jvm
tags: [android, auto, car, templates, kotlin, testing]
detect: [dep:androidx.car.app:app, dep:androidx.car.app:app-projected, dep:androidx.car.app:app-automotive, dep:androidx.car.app:app-testing]
related: [android, kotlin-coroutines, android-navigation]
---
Android Car App Library: template-based apps for Android Auto and Android Automotive, driven by a CarAppService and Screens.

## Verify
- `./gradlew testDebugUnitTest`: Screen logic tests with the car app testing library on the JVM.
- `./gradlew lintDebug`: manifest, category and minCarApiLevel checks are clean.
- `./gradlew assembleDebug`: the app builds with the car services declared.

## Test first
Test a Screen with `TestCarContext` and assert on the template it returns.
```kotlin
@RunWith(RobolectricTestRunner::class)
class MainScreenTest {
  @Test fun showsTitle() {
    val ctx = TestCarContext.createCarContext(ApplicationProvider.getApplicationContext())
    val template = MainScreen(ctx).onGetTemplate() as PaneTemplate
    assertEquals("Hello", template.title?.toString())
  }
}
```

## Do
- Declare a `CarAppService` in the manifest with the matching category (`androidx.car.app.category.NAVIGATION`, `POI`, `IOT`).
- Return a `Session` from `onCreateSession` and the first `Screen` from `onCreateScreen`.
- Declare `androidx.car.app.minCarApiLevel` in the manifest and guard newer APIs with `carContext.carAppApiLevel`.
- Build UI only from templates, and call `invalidate()` after state changes.
- Use `ScreenManager.push` and `pop` for navigation.
- Add `app-projected` for Android Auto and `app-automotive` for built-in cars.
- Keep `onGetTemplate` fast, loading data elsewhere and showing a loading state.
- Respect the template step and item limits per category.

## Avoid
- Long or blocking work in `onGetTemplate`: the host drops the app. Load async and call `invalidate()`.
- Calling APIs above the host's API level: crashes on older hosts. Check `carAppApiLevel`.
- Custom views or Android UI: not supported. Use templates.
- Forgetting the automotive manifest entries: the app is rejected. Add the `automotive_app_desc` metadata.
- Exceeding template limits: the host throws. Page or trim the list.
- Holding a Screen or CarContext after destroy: leaks. Use lifecycle observers.

## Review
- [ ] Service category matches the app type.
- [ ] minCarApiLevel is set and newer APIs are guarded.
- [ ] No blocking work in `onGetTemplate`.
- [ ] Screens are tested with `TestCarContext`.
- [ ] Template limits are respected.
