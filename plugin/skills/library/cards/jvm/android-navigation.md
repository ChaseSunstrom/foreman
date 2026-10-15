---
name: android-navigation
title: Android Navigation
area: jvm
tags: [android, kotlin, navigation, compose, fragments, deep-links, back-stack]
detect: [dep:navigation-compose, dep:navigation-fragment-ktx, dep:navigation-ui-ktx, dep:navigation-testing, dep:androidx.navigation.safeargs]
related: [android, jetpack-compose, hilt, espresso]
---
Jetpack Navigation (Compose and Fragments): one NavController, type-safe routes, hoisted navigation events, deep links and tested back stacks.

## Verify
- `./gradlew testDebugUnitTest`: navigation logic and `TestNavHostController` tests pass.
- `./gradlew connectedDebugAndroidTest`: instrumented navigation flows pass.
- `./gradlew lintDebug`: catches missing deep-link intent filters and invalid destinations.
- `adb shell am start -a android.intent.action.VIEW -d "app://item/42" <package>`: a deep link opens the right destination.

## Test first
`navigation-testing` supplies `TestNavHostController`.
```kotlin
class NavTest {
    @get:Rule val rule = createComposeRule()

    @Test fun tapItemOpensDetail() {
        lateinit var nav: TestNavHostController
        rule.setContent {
            nav = TestNavHostController(LocalContext.current).apply {
                navigatorProvider.addNavigator(ComposeNavigator())
            }
            AppNavHost(nav)
        }
        rule.onNodeWithText("Item 1").performClick()
        assertTrue(nav.currentBackStackEntry?.destination?.hasRoute<Detail>() == true)
    }
}
```

## Do
- Compose: define routes as `@Serializable` objects or data classes (type-safe navigation, Navigation 2.8+), `composable<Detail> { backStackEntry -> backStackEntry.toRoute<Detail>() }`.
- Create the `NavController` once with `rememberNavController()` at the top and pass lambdas (`onOpen: (Id) -> Unit`) to screens, not the controller.
- Pass IDs, not objects; load data in the destination's ViewModel via `SavedStateHandle`.
- Use `navigate(route) { popUpTo(Start) { inclusive = true }; launchSingleTop = true }` for login flows and bottom bars with `saveState`/`restoreState`.
- Scope shared ViewModels to a nested graph with `navController.getBackStackEntry(...)`.
- Declare `navDeepLink` and the manifest intent filter together; verify with `adb`.
- Fragments: use Safe Args (`androidx.navigation.safeargs.kotlin`) for typed arguments.

## Avoid
- Passing the `NavController` into deep composables or ViewModels: untestable, leaks. Hoist navigation callbacks.
- String routes with hand-built arguments (`"detail/$id"`) in new code: typos and encoding bugs. Use type-safe routes.
- Navigating inside composition (`navController.navigate(...)` in the body): fires on every recomposition. Navigate from events or `LaunchedEffect`.
- Serializing large objects through arguments: size and crash risks. Pass an ID.
- Calling `navigate` twice on fast taps: duplicate destinations. Use `launchSingleTop = true` or debounce.
- Not clearing the back stack after login or logout: back returns to a protected screen. Use `popUpTo` with `inclusive = true`.

## Review
- [ ] Screens receive callbacks, not `NavController`.
- [ ] Routes are typed and arguments are IDs only.
- [ ] Auth flows reset the back stack.
- [ ] Deep links work through the manifest and `navDeepLink`, and have a test or `adb` check.
- [ ] Back stack state is asserted in tests.
