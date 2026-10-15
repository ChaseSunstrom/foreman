---
name: exposed
title: Exposed
area: jvm
tags: [kotlin, sql, orm, dsl, dao, transactions, migrations]
detect: [dep:exposed-core, dep:exposed-dao, dep:exposed-jdbc, dep:exposed-r2dbc, dep:exposed-java-time, dep:exposed-spring-boot-starter]
related: [ktor, kotlin-coroutines, flyway, testcontainers, kotest]
---
JetBrains Exposed SQL library for Kotlin: typed tables, DSL and DAO, explicit transactions, and migrations run outside the app's table-creating shortcuts.

## Verify
- `./gradlew test`: repository tests pass against the real database engine.
- `grep -rnE "SchemaUtils\.(create|createMissingTablesAndColumns)" src/main`: schema is not auto-created in production code.
- `grep -rn "exposed-" build.gradle.kts gradle/libs.versions.toml`: all `exposed-*` modules use one version.
- `./gradlew dependencies --configuration runtimeClasspath | grep -i exposed`: no mixed 0.x and 1.x package imports.

## Test first
Real engine via Testcontainers (H2 only if production is H2). Tests in `src/test/kotlin`.
```kotlin
class UserRepoTest {
    @Test fun `email is unique`() {
        Database.connect(dataSource)
        transaction {
            SchemaUtils.create(Users)
            Users.insert { it[email] = "a@x" }
            assertFailsWith<ExposedSQLException> {
                Users.insert { it[email] = "a@x" }
            }
        }
    }
}
```

## Do
- Declare tables as `object Users : LongIdTable("users")` with column constraints (`.uniqueIndex()`, `.references(...)`, `.index()`), nullable columns via `.nullable()`.
- Wrap all access in `transaction { }` (or `newSuspendedTransaction(Dispatchers.IO)` / `suspendTransaction` in coroutine code) and return plain data, not DAO entities, out of the block.
- Use a pooled `DataSource` (HikariCP) passed to `Database.connect(ds)`, closed on shutdown.
- Manage schema with Flyway or Liquibase; keep `SchemaUtils` for tests.
- Use `batchInsert`, `upsert`, and `insertIgnore` for bulk work; add `.limit()` and `.orderBy` for pagination.
- Use `eagerLoading` (`with(...)`/`load`) for DAO relations to avoid N+1.
- Set `DatabaseConfig` and `transactionIsolation` explicitly where it matters; use `inTopLevelTransaction` carefully.
- Log SQL in tests with `addLogger(StdOutSqlLogger)`.

## Avoid
- `SchemaUtils.createMissingTablesAndColumns` in production: unreviewed DDL, no rollback. Use migrations.
- Returning entities or `ResultRow` after the transaction closes: lazy access fails. Map to DTOs inside.
- Blocking `transaction {}` on a coroutine dispatcher thread pool without IO dispatcher: stalls. Use suspended transactions on `Dispatchers.IO`.
- Building SQL by string concatenation with `exec`: injection. Use the DSL or parameterized `exec(stmt, args)`.
- Nested `transaction {}` assuming a new transaction: it joins the outer by default. Use `requiresNew = true` if separate.
- Mixing old `org.jetbrains.exposed.sql` imports with newer package layouts after an upgrade: check the migration notes for your target version.

## Review
- [ ] Every query runs inside a transaction and returns detached data.
- [ ] Schema changes are migrations, not runtime DDL.
- [ ] Unique and foreign-key constraints exist in the schema, not only in code.
- [ ] No N+1 loads on entity relations.
- [ ] Tests run on the production engine and cover constraint failures.
