---
name: liquibase
title: Liquibase
area: jvm
tags: [liquibase, migrations, changelog, database, java, schema]
detect: [dep:liquibase-core, dep:liquibase-maven-plugin, file:db/changelog/*.xml, file:db/changelog/*.yaml, file:liquibase.properties]
related: [flyway, spring-boot, spring-data-jpa, jooq, testcontainers, hibernate]
---
Liquibase changelogs: changesets with ids, authors and checksums, contexts, rollback, and CI validation.

## Verify
- `liquibase validate --changelog-file=db/changelog/db.changelog-master.yaml`: the changelog parses and is consistent.
- `liquibase status --verbose`: which changesets are pending.
- `liquibase update-sql`: the SQL that would run, for review before applying.
- `./mvnw -q test`: the app migrates an empty Testcontainers database through the changelog.

## Test first
Run the whole changelog against an empty real database, and test rollback where you declared it.
```java
@Test void updatesEmptyDatabase() throws Exception {
  try (var conn = DriverManager.getConnection(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())) {
    var db = DatabaseFactory.getInstance()
        .findCorrectDatabaseImplementation(new JdbcConnection(conn));
    new Liquibase("db/changelog/db.changelog-master.yaml",
        new ClassLoaderResourceAccessor(), db).update("");
  }
}
```

## Do
- Keep a master changelog that `include`s per-feature files in order; one changeset per logical change.
- Give every changeset a unique `id` and `author`; never reuse them across files in a way that collides.
- Prefer the typed change types (`createTable`, `addColumn`) for portability, and `sql` changes for engine-specific work with `dbms`.
- Declare `rollback` for changesets that can be reversed; test `rollback` on a copy.
- Use `preConditions` (`onFail: MARK_RAN`) to adopt existing schemas safely.
- With Spring Boot, set `spring.liquibase.change-log` and `spring.jpa.hibernate.ddl-auto=validate`.
- Use `contexts` and `labels` for test-only data, never for schema differences between environments.

## Avoid
- Editing a changeset that has run: checksum failure everywhere else. Add a new changeset (or `runOnChange` only for repeatable objects like views).
- Reusing an `id` and `author` pair with different content: it is the identity of the changeset.
- `liquibase dropAll` against shared databases: removes everything. Keep it to disposable test containers.
- Letting Hibernate `ddl-auto=update` run alongside Liquibase: two sources of truth.
- Large data loads via `insert` changesets: slow. Use `loadData` with a CSV, or an external seeding step.
- A `sql` changeset without `splitStatements` or `endDelimiter` for functions or procedures: statements get split wrongly.
- Auto-generated `diff-changelog` committed unreviewed: it includes drift and noise. Prune it by hand.

## Review
- [ ] No previously applied changeset was altered.
- [ ] Every changeset has a unique id and author and a rollback where reversible.
- [ ] Changelog applies to an empty database and validates in CI.
- [ ] Engine-specific SQL is guarded with `dbms`.
- [ ] Test data is gated by a context, not mixed into schema changesets.
