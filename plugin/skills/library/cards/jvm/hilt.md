---
name: hilt
title: Hilt
area: jvm
tags: [android, kotlin, hilt, dagger, di, testing]
detect: [dep:com.google.dagger:hilt-android, dep:hilt-android, dep:hilt-android-compiler, dep:dagger, dep:androidx.hilt:hilt-navigation-compose]
related: [android, jetpack-compose, room, kotlin-coroutines, junit5]
---
Hilt dependency injection on Android: entry points, modules, scopes, ViewModel injection, test replacement of modules.

## Verify
- `./gradlew assembleDebug`: the Dagger graph is validated at compile time; missing bindings fail the build.
- `./gradlew testDebugUnitTest`: unit tests of injected classes pass with plain constructors.
- `./gradlew connectedDebugAndroidTest`: instrumented tests with `HiltAndroidRule` and a replaced module run.
- `./gradlew :app:dependencies --configuration kspDebug | grep hilt`: compiler and runtime share a version.

## Test first
Unit-test classes by constructing them with fakes; use Hilt only for instrumented wiring tests.
```kotlin
@HiltAndroidTest
@UninstallModules(NetworkModule::class)
class MainActivityTest {
  @get:Rule(order = 0) val hilt = HiltAndroidRule(this)
  @get:Rule(order = 1) val compose = createAndroidComposeRule<HiltTestActivity>()

  @BindValue @JvmField val api: Api = FakeApi()

  @Before fun init() = hilt.inject()

  @Test fun showsItems() {
    compose.onNodeWithText("Item A").assertExists()
  }
}
```

## Do
- Annotate the `Application` with `@HiltAndroidApp` and entry points with `@AndroidEntryPoint`.
- Inject ViewModels with `@HiltViewModel` plus `@Inject constructor`, obtained via `hiltViewModel()` or `by viewModels()`.
- Provide third-party types in `@Module @InstallIn(SingletonComponent::class)` using `@Provides`; bind interfaces with `@Binds` on abstract modules.
- Pick scopes deliberately (`@Singleton`, `@ViewModelScoped`, `@ActivityRetainedScoped`) and leave unscoped what is cheap.
- Use qualifiers (`@Qualifier` annotations or `@Named`) to separate dispatchers or clients; inject dispatchers rather than using `Dispatchers.IO` directly.
- Use KSP (`ksp(libs.hilt.compiler)`) or kapt, matching the project; apply `com.google.dagger.hilt.android` plugin.
- Use `@AssistedInject` for ViewModels needing runtime arguments.

## Avoid
- Field injection in classes Hilt does not create: no `@AndroidEntryPoint`, `lateinit` stays uninitialized. Use an `@EntryPoint` interface.
- Injecting `Activity` context into singletons: leak. Use `@ApplicationContext`.
- Scoping everything `@Singleton`: holds memory and shared state. Scope narrowly.
- Mixing the old `@Component` Dagger setup and Hilt in one graph without a plan.
- Forgetting `hilt.inject()` or using a plain `AndroidJUnitRunner` in instrumented tests: set a custom runner that uses `HiltTestApplication`.
- Using `kotlin-kapt` for Hilt in new projects when KSP is supported: slower builds.
- Providing mutable singletons without synchronization.

## Review
- [ ] Build passes with the graph validated; no unused or duplicated bindings.
- [ ] Scopes match lifetimes; contexts are application-scoped when long-lived.
- [ ] Dispatchers are injected and replaced in tests.
- [ ] Test modules replace network and database with fakes.
- [ ] Custom test runner is configured for instrumented tests.
