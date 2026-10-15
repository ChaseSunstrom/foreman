---
name: spring-data-jpa
title: Spring Data JPA
area: jvm
tags: [java, spring, jpa, repository, sql, hibernate]
detect: [dep:spring-boot-starter-data-jpa, dep:spring-data-jpa]
related: [hibernate, spring-boot, flyway, liquibase, testcontainers, junit5]
---
Spring Data JPA repositories: derived queries, `@Query`, transactions, fetch plans and the N+1 trap.

## Verify
- `./mvnw -q test` (or `./gradlew test`): `@DataJpaTest` repository tests pass.
- `./mvnw -q verify -Dspring.jpa.show-sql=true`: inspect the emitted SQL for N+1 patterns in logs.
- `./mvnw -q dependency:tree | grep -i hibernate`: one Hibernate version.
- `./mvnw -q flyway:validate` (if the plugin is configured): migrations match the entities' schema.

## Test first
`@DataJpaTest` replaces the datasource with an embedded one by default; use a Testcontainers database for real SQL behavior and add `@AutoConfigureTestDatabase(replace = NONE)`.
```java
@DataJpaTest
class ItemRepositoryTest {
  @Autowired ItemRepository repo;

  @Test void findsByOwnerIgnoringCase() {
    repo.save(new Item("A", "Bob"));
    assertThat(repo.findByOwnerIgnoreCase("bob")).hasSize(1);
  }
}
```

## Do
- Extend `JpaRepository` (or the narrower `ListCrudRepository`); name derived queries precisely or write `@Query` with named parameters.
- Return projections (interfaces or records) for read paths instead of full entities.
- Fix N+1 with `@EntityGraph` or `join fetch`; paginate with `Pageable` plus a count query.
- Mark read services `@Transactional(readOnly = true)`.
- Set `spring.jpa.open-in-view=false` explicitly and load what the response needs inside the service.
- Add `@Version` for optimistic locking on contended entities.
- Create the schema with migrations; use `ddl-auto=validate`.

## Avoid
- `FetchType.EAGER` on collections: loads everything everywhere. Keep lazy and fetch per query.
- `join fetch` on a collection with `Pageable`: Hibernate paginates in memory. Fetch ids first, then the entities.
- `@Query` built by string concatenation: SQL injection. Use `:param` binding.
- Entities as `equals`/`hashCode` on generated id only: breaks in sets before persist. Use a business key or id-null-safe pattern.
- Self-invocation of a `@Transactional` method: the proxy is bypassed. Call through another bean.
- `@Modifying` queries without `clearAutomatically`: the persistence context serves stale entities.
- `Optional.get()` on `findById`: use `orElseThrow` with a domain exception.

## Review
- [ ] Every collection access on list endpoints is covered by a fetch plan, with a query-count check.
- [ ] No entity leaks into the JSON response.
- [ ] Transaction boundaries sit on services, with `readOnly` for queries.
- [ ] Schema changes come with a migration.
- [ ] Custom queries bind parameters.
