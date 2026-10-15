---
name: room
title: Room
area: jvm
tags: [android, kotlin, room, sqlite, database, migrations]
detect: [dep:androidx.room:room-runtime, dep:androidx.room:room-ktx, dep:androidx.room:room-compiler, dep:androidx.room:room-testing]
related: [android, kotlin-coroutines, hilt, jetpack-compose]
---
Room on Android: entities, DAOs, exported schemas, migrations, and in-memory database tests.

## Verify
- `./gradlew testDebugUnitTest`: DAO tests (Robolectric) and migration logic pass.
- `./gradlew connectedDebugAndroidTest`: `MigrationTestHelper` tests run against real SQLite on a device.
- `ls app/schemas/`: exported schema JSON exists per version (needs the `room.schemaLocation` option).
- `./gradlew assembleDebug`: the Room processor (KSP or kapt) accepted every query at compile time.

## Test first
Use an in-memory database for DAO tests; use `MigrationTestHelper` for upgrades.
```kotlin
@RunWith(AndroidJUnit4::class)
class ItemDaoTest {
  private lateinit var db: AppDatabase

  @Before fun setUp() {
    db = Room.inMemoryDatabaseBuilder(
      ApplicationProvider.getApplicationContext(), AppDatabase::class.java).build()
  }
  @After fun tearDown() = db.close()

  @Test fun insertThenRead() = runTest {
    db.itemDao().insert(Item(1, "a"))
    assertEquals("a", db.itemDao().get(1)?.name)
  }
}
```

## Do
- Use KSP (`ksp(libs.room.compiler)`) rather than kapt, and set `room.schemaLocation` so schemas are exported and committed.
- Define DAOs as interfaces; return `Flow<T>` for observable queries and mark one-shot calls `suspend`.
- Write explicit `Migration(from, to)` objects and test each with `MigrationTestHelper`; use `@AutoMigration` for simple changes.
- Index columns used in `WHERE` and joins with `@Entity(indices = [...])`; declare `@ForeignKey` with `onDelete`.
- Use `@Transaction` on DAO methods that read relations (`@Relation`) or combine writes.
- Keep one `RoomDatabase` instance, provided by DI as a singleton.
- Convert complex types with `@TypeConverter`; keep converters pure.

## Avoid
- `fallbackToDestructiveMigration()` in production: deletes user data on version bumps. Write migrations.
- `allowMainThreadQueries()`: janks the UI. Use suspend or Flow DAOs on Room's executors.
- Bumping `version` without a migration or without committing the new schema JSON.
- Returning the full entity list into UI without paging: use `PagingSource` or a limit for large tables.
- Building the database per call or per ViewModel: expensive and inconsistent. Use one singleton.
- String concatenation in `@RawQuery`: injection risk. Use bind arguments.
- Storing lists or JSON blobs in a column to dodge a relation when you must filter on them.

## Review
- [ ] Each schema version bump has a tested migration and an exported schema file.
- [ ] Queries are validated at compile time and indexed for the access paths.
- [ ] No main-thread queries.
- [ ] Database is a singleton from DI.
- [ ] Relations are loaded in `@Transaction` methods.
