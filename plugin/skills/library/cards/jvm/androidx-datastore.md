---
name: androidx-datastore
title: Jetpack DataStore
area: jvm
tags: [android, kotlin, datastore, preferences, flow, storage]
detect: [dep:androidx.datastore:datastore-preferences, dep:androidx.datastore:datastore]
related: [android, kotlin-coroutines, room, jetpack-compose]
---
Jetpack DataStore: small key-value or typed settings stored asynchronously with Flow, replacing SharedPreferences.

## Verify
- `./gradlew testDebugUnitTest`: DataStore tests against a temp file run on the JVM.
- `./gradlew lintDebug`: no leftover SharedPreferences or main-thread blocking warnings.
- `./gradlew assembleDebug`: the delegate and key declarations compile.

## Test first
Build the store over a temp file with a test scope, write, then read the Flow.
```kotlin
class SettingsTest {
  @get:Rule val tmp = TemporaryFolder()

  @Test fun savesTheme() = runTest {
    val store = PreferenceDataStoreFactory.create(
      scope = backgroundScope,
      produceFile = { tmp.newFile("s.preferences_pb") },
    )
    val key = booleanPreferencesKey("dark")
    store.edit { it[key] = true }
    assertEquals(true, store.data.first()[key])
  }
}
```

## Do
- Declare one `preferencesDataStore(name = ...)` delegate per file, at top level, on `Context`.
- Wrap the store in a repository that exposes `Flow` and suspend `edit` functions.
- Define keys once as constants: `booleanPreferencesKey`, `stringPreferencesKey`.
- Use `edit { }` for read-modify-write so it runs as one atomic transaction.
- Catch `IOException` on `data` with `catch { emit(emptyPreferences()) }`.
- Use Proto DataStore with a serializer when the data has a schema.
- Inject a `DataStore<Preferences>` so tests pass a temp-file store.
- Migrate from SharedPreferences with `SharedPreferencesMigration`.

## Avoid
- Two DataStore instances on the same file: it throws at runtime. Keep a single top-level delegate.
- `runBlocking` on the main thread to read a value: blocks the UI. Collect the Flow or read in a coroutine.
- Storing large or relational data: use Room instead.
- Creating the delegate inside a class or composable: a new instance per call. Move it to top level.
- Reading a value then writing it back outside `edit`: lost updates. Do it inside `edit`.
- Using it from multiple processes: not supported. Keep one process per file.
- Forgetting `SharedPreferencesMigration`: users lose settings on upgrade.

## Review
- [ ] One DataStore instance per file, declared at top level.
- [ ] No blocking reads on the main thread.
- [ ] Updates go through `edit`.
- [ ] IO errors on `data` are handled.
- [ ] Tests use a temp file and a test scope.
