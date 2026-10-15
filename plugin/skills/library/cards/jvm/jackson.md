---
name: jackson
title: Jackson
area: jvm
tags: [java, kotlin, json, serialization, jackson, objectmapper]
detect: [dep:jackson-databind, dep:jackson-core, dep:jackson-module-kotlin, dep:jackson-datatype-jsr310, dep:jackson-dataformat-yaml]
related: [spring-boot, kotlinx-serialization, junit5, quarkus]
---
Jackson JSON: configured `ObjectMapper`, records and Kotlin support, java.time, polymorphism, safe deserialization.

## Verify
- `./mvnw -q test` (or `./gradlew test`): JSON round-trip tests pass.
- `./mvnw -q dependency:tree | grep jackson`: all `jackson-*` modules share one version (use the Jackson BOM).
- `./mvnw -q dependency:tree | grep -E "jsr310|kotlin"`: the java.time and Kotlin modules are present where used.
- `grep -rn "enableDefaultTyping\|activateDefaultTyping" src/`: no unrestricted default typing.

## Test first
Test against literal JSON, including unknown and missing fields.
```java
class ItemJsonTest {
  private final ObjectMapper mapper = JsonMapper.builder()
      .addModule(new JavaTimeModule())
      .build();

  @Test void readsIsoDateAndIgnoresNothingUnexpected() {
    var json = "{\"name\":\"a\",\"createdAt\":\"2024-01-02T03:04:05Z\",\"extra\":1}";
    assertThrows(UnrecognizedPropertyException.class,
        () -> mapper.readValue(json, Item.class));
  }
}
```

## Do
- Build one shared, thread-safe `ObjectMapper` (or the framework's bean) and reuse it.
- Register `JavaTimeModule` and disable `WRITE_DATES_AS_TIMESTAMPS` so `Instant` and `LocalDate` serialize as ISO strings.
- For Kotlin, register `jackson-module-kotlin` (`jacksonObjectMapper()`) so data classes and nullability work.
- Prefer records or immutable classes with `@JsonCreator` and `@JsonProperty` constructors.
- Decide on unknown properties deliberately: `FAIL_ON_UNKNOWN_PROPERTIES` for strict inputs, or `@JsonIgnoreProperties(ignoreUnknown = true)` for tolerant clients.
- Model polymorphism with `@JsonTypeInfo` plus `@JsonSubTypes` listing allowed subtypes.
- Use `@JsonView` or dedicated DTOs to hide fields; use `@JsonIgnore` for secrets.
- Use `JsonMapper.builder()` for configuration rather than mutating a shared mapper.

## Avoid
- `enableDefaultTyping()` or `activateDefaultTyping` with a permissive validator: remote code execution risk through gadget classes. Use explicit `@JsonSubTypes` or a restrictive `PolymorphicTypeValidator`.
- Deserializing untrusted JSON into `Object` or `Map` and then casting: unchecked, and type confusion.
- Missing `jackson-datatype-jsr310`: `InvalidDefinitionException` for `java.time` types.
- Mixed `jackson-*` versions: `NoSuchMethodError` at runtime. Use `jackson-bom`.
- Mutating `ObjectMapper` config after first use: not thread-safe. Configure once at build.
- `new ObjectMapper()` per call: slow, and ignores the framework's configured module set.
- Serializing JPA entities directly: lazy proxies and cycles. Map to DTOs.

## Review
- [ ] One configured mapper, with modules for time and Kotlin where used.
- [ ] No default typing or untrusted polymorphic deserialization.
- [ ] Date, enum and null handling are covered by tests on literal JSON.
- [ ] Secrets and internal fields are not serialized.
- [ ] Jackson artifacts come from a single BOM version.
