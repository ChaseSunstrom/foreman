---
name: hibernate
title: Hibernate ORM
area: jvm
tags: [java, orm, jpa, hibernate, sql, entities]
detect: [dep:hibernate-core, dep:hibernate-entitymanager, dep:hibernate-validator, dep:quarkus-hibernate-orm]
related: [spring-data-jpa, flyway, liquibase, testcontainers, jooq]
---
Hibernate ORM entities and sessions: mappings, fetch plans, flush behavior, locking and the N+1 problem.

## Verify
- `./mvnw -q test` (or `./gradlew test`): entity and repository tests pass against the real database dialect.
- `./mvnw -q test -Dhibernate.show_sql=true`: SQL the session emits; count statements per use case.
- `./mvnw -q dependency:tree | grep -i hibernate`: one Hibernate version across modules.
- `./mvnw -q dependency:tree | grep -E "javax.persistence|jakarta.persistence"`: only the `jakarta` namespace on Hibernate 6.

## Test first
Run against the production engine (Testcontainers) and assert statement counts or loaded state.
```java
@Test void listingOrdersDoesNotLoadLinesPerRow() {
  var stats = sessionFactory.getStatistics();
  stats.clear();
  orders.findAllWithLines();
  assertEquals(1, stats.getPrepareStatementCount());
}
```
Enable with `hibernate.generate_statistics=true` in the test configuration.

## Do
- Map associations `LAZY` (`@ManyToOne(fetch = LAZY)`; ToOne defaults to EAGER); load what a use case needs with `join fetch` or an entity graph.
- Keep both sides of a bidirectional association in sync in helper methods; `mappedBy` on the inverse side.
- Add `@Version` for optimistic locking; use `LockModeType.PESSIMISTIC_WRITE` only for real contention.
- Batch writes with `hibernate.jdbc.batch_size`, and order inserts and updates.
- Use `@Enumerated(EnumType.STRING)` and `@Column(nullable = false, length = ...)` matching the migration.
- Prefer a sequence-based id (`GenerationType.SEQUENCE`) with an allocation size matching the DB sequence.
- Keep sessions short: one transaction per use case; map to DTOs before leaving it.

## Avoid
- `javax.persistence` imports on Hibernate 6: it is `jakarta.persistence`.
- `EnumType.ORDINAL` (the default): reordering the enum corrupts data. Use `STRING`.
- `hbm2ddl.auto=update` outside local dev: unsafe drift. Use migrations and `validate`.
- Lombok `@Data` on entities: generated `equals`, `hashCode` and `toString` trigger lazy loads and recursion.
- Deprecated `Criteria` (legacy Hibernate API) and `session.createSQLQuery`: use JPA `CriteriaBuilder` and `createNativeQuery`.
- Open-session-in-view as a fix for `LazyInitializationException`: fetch eagerly in the query.
- `IDENTITY` ids with large batch inserts: disables JDBC batching.

## Review
- [ ] Each read use case has a bounded statement count.
- [ ] Associations are lazy with explicit fetches.
- [ ] Schema comes from migrations that match the mapping.
- [ ] Entities do not use field-wise `equals` on mutable state or Lombok `@Data`.
- [ ] Transactions end before DTOs reach the web layer.
