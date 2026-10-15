---
name: flyway
title: Flyway
area: jvm
tags: [flyway, migrations, sql, database, java, schema]
detect: [dep:flyway-core, dep:flyway-database-postgresql, dep:flyway-maven-plugin, file:db/migration/V*.sql, file:flyway.conf]
related: [liquibase, spring-boot, spring-data-jpa, jooq, testcontainers, hibernate]
---
Flyway database migrations: versioned and repeatable SQL scripts, checksums, baselines and CI validation.

## Verify
- `./mvnw -q flyway:info` (or `./gradlew flywayInfo`): applied, pending and failed migrations.
- `./mvnw -q flyway:validate` (or `./gradlew flywayValidate`): checksums on disk match what the database recorded.
- `./mvnw -q test`: the app (or a test) migrates an empty Testcontainers database to the latest version.
- `ls src/main/resources/db/migration`: versions are unique and ordered.

## Test first
Apply every migration to an empty real database and assert the result.
```java
@Test void migratesEmptyDatabaseToLatest() {
  var flyway = Flyway.configure()
      .dataSource(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())
      .load();
  var result = flyway.migrate();
  assertTrue(result.success);
  assertEquals(0, flyway.info().pending().length);
}
```
Add a data-bearing test when a migration transforms existing rows.

## Do
- Name files `V<version>__<description>.sql` (two underscores) under `db/migration`; use `R__name.sql` for repeatable views and functions.
- Treat applied migrations as immutable; fix forward with a new version.
- Keep each migration small and one concern; make destructive steps a later release (expand, migrate, contract).
- On Flyway 10 and later add the database module (`flyway-database-postgresql` and so on) next to `flyway-core`.
- With Spring Boot, set `spring.flyway.locations` and let it migrate at startup, with `spring.jpa.hibernate.ddl-auto=validate`.
- Use `baselineOnMigrate` and `baselineVersion` only to adopt an existing database once.
- Run `validate` in CI against the production-like engine.

## Avoid
- Editing an applied migration: checksum mismatch on every other environment. Add `V<next>`.
- Single underscore in the file name (`V1_init.sql`): not recognized as a versioned migration properly. Use `V1__init.sql`.
- Forgetting the database-specific module on Flyway 10: "Unsupported Database" at startup.
- `flyway clean` against shared environments: drops everything. Disable with `cleanDisabled=true` (the default in recent versions) and keep it off.
- Out-of-order versions on branches merging late: collisions. Use timestamp-style versions or coordinate, and avoid `outOfOrder` unless deliberate.
- Mixing Hibernate `ddl-auto=update` with Flyway: two sources of truth.
- Long locking DDL on large tables without a plan (`CREATE INDEX CONCURRENTLY` needs `executeInTransaction=false` on Postgres).

## Review
- [ ] No existing migration file was modified.
- [ ] Version numbers are unique and follow the naming rule.
- [ ] Migrations apply cleanly to an empty database and to a production-like snapshot.
- [ ] Destructive changes are staged across releases.
- [ ] `ddl-auto` is `validate` or `none`.
