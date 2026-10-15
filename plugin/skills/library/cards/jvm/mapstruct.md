---
name: mapstruct
title: MapStruct
area: jvm
tags: [java, kotlin, mapping, dto, annotation-processing, spring, lombok]
detect: [dep:mapstruct, dep:mapstruct-processor]
related: [lombok, spring-boot, hibernate, spring-data-jpa, jackson, assertj]
---
MapStruct compile-time bean mappers: generated, null-safe, reviewable mapping code with unmapped fields treated as errors.

## Verify
- `./gradlew compileJava`: the processor generates `*MapperImpl` and reports mapping problems as compile errors.
- `./gradlew test`: mapper tests pass.
- `find build/generated -name "*MapperImpl.java"`: implementations were generated (Maven: `target/generated-sources/annotations`).

## Test first
Plain unit test, using `Mappers.getMapper` or the Spring bean.
```java
class OrderMapperTest {
  OrderMapper mapper = Mappers.getMapper(OrderMapper.class);

  @Test void mapsCustomerNameAndTotal() {
    var dto = mapper.toDto(new Order(7L, new Customer("Ann"), 1250));
    assertEquals("Ann", dto.customerName());
    assertEquals(12.50, dto.total(), 0.001);
  }
}
```

## Do
- Declare `@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.ERROR)` so new fields on the target break the build until mapped or ignored.
- Use `@Mapping(source = "customer.name", target = "customerName")` for renames, `expression` or `qualifiedByName` for logic, and `ignore = true` with intent.
- Gradle: `implementation("org.mapstruct:mapstruct:...")` and `annotationProcessor("org.mapstruct:mapstruct-processor:...")`; Kotlin uses `kapt` or KSP (the KSP variant is separate and less complete, so verify support first).
- With Lombok, add `lombok-mapstruct-binding` to the processor path and order Lombok before MapStruct.
- Update existing objects with `@MappingTarget`; keep ids and audit fields excluded.
- Compose mappers with `uses = {OtherMapper.class}` and let MapStruct map collections and nested types.
- Set `nullValuePropertyMappingStrategy = IGNORE` for patch-style updates.
- Map to immutable targets using constructors or builders; MapStruct detects them.
- Test mappers directly and cover nulls.

## Avoid
- Default unmapped policy (`WARN`): silently null fields after a model change. Set `ERROR`.
- Mapping JPA entities to DTOs through lazy associations outside a transaction: `LazyInitializationException`. Map inside the transaction or fetch needed data.
- Cyclic mappings (parent and child referencing each other): `StackOverflowError`. Use `@Context` with `CycleAvoidingMappingContext` or map one direction.
- Hand-written `default` methods duplicating generated ones: drift. Prefer annotations and delegate.
- Processor missing from the `annotationProcessor` configuration: `*Impl` not found at runtime. Add it, and rebuild clean.
- Putting business rules into mappers: hard to test and review. Keep mappers structural.

## Review
- [ ] Unmapped target policy is `ERROR`, and every `ignore` has a reason.
- [ ] Entities are mapped within transaction boundaries.
- [ ] Update mappers never overwrite ids or audit fields.
- [ ] Null and collection cases have tests.
- [ ] Processor ordering with Lombok is correct.
