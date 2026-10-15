---
name: jooq
title: jOOQ
area: jvm
tags: [java, kotlin, sql, jooq, codegen, database]
detect: [dep:jooq, dep:jooq-codegen, dep:jooq-meta, dep:spring-boot-starter-jooq, dep:jooq-kotlin]
related: [flyway, liquibase, testcontainers, spring-boot, hibernate]
---
jOOQ: type-safe SQL DSL with code generated from the real schema, plus its execution and transaction APIs.

## Verify
- `./mvnw -q generate-sources` (or `./gradlew generateJooq`): codegen runs against the migrated schema and the sources compile.
- `./mvnw -q verify` (or `./gradlew check`): tests pass against the real database engine.
- `git diff --stat -- '**/jooq/**'`: generated code changes appear only when migrations change (commit or regenerate consistently).
- `./mvnw -q dependency:tree | grep -i jooq`: one jOOQ version across runtime and codegen.

## Test first
Run queries against a real database from Testcontainers with migrations applied.
```java
@Test void findsActiveUsersByEmailDomain() {
  dsl.insertInto(USERS).columns(USERS.EMAIL, USERS.ACTIVE)
     .values("a@x.com", true).values("b@y.com", true).execute();

  var found = repo.activeByDomain("x.com");

  assertEquals(List.of("a@x.com"), found);
}
```

## Do
- Generate code from a migrated database (Flyway or Liquibase first, then codegen) so the DSL matches the schema.
- Set the dialect explicitly: `DSL.using(connection, SQLDialect.POSTGRES)` or through configuration.
- Use bind values by default (`USERS.ID.eq(id)`); that is parameterized for you.
- Use `dsl.transactionResult(cfg -> ...)` (or Spring's `@Transactional` with the jOOQ `TransactionAwareDataSourceProxy`) for atomic work.
- Fetch into records, POJOs or Kotlin data classes with `fetchInto` or `into(...)` and map at the repository boundary.
- Use `multiset` and `row` for nested results rather than N+1 queries.
- Build dynamic filters from `Condition` values combined with `DSL.noCondition().and(...)`.

## Avoid
- Plain SQL strings with concatenated input (`DSL.condition("name = '" + x + "'")`): SQL injection. Use `DSL.condition("name = {0}", x)` or typed fields.
- Hand-editing generated sources: overwritten on regeneration. Change the schema or generator config.
- Running codegen against a developer's live database: nondeterministic. Use the container or DDL-based codegen.
- Using `Connection` from a different transaction manager than the one jOOQ uses: partial commits. Share one `DataSource`.
- `fetch()` of a huge result set into memory: use `fetchLazy()` or `fetchStream()` inside a transaction and close the cursor.
- Ignoring that `fetchOne()` throws on multiple rows: use `fetchOptional()` or add a limit and a unique constraint.
- Mixing jOOQ's SQLDialect with the wrong JDBC driver.

## Review
- [ ] Generated code matches the current migrations.
- [ ] Queries bind values; no concatenated SQL.
- [ ] Transactions wrap multi-statement writes.
- [ ] Large reads stream or paginate.
- [ ] Tests run against the same engine as production.
