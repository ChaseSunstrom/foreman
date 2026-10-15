---
name: lombok
title: Lombok
area: jvm
tags: [java, annotations, boilerplate, annotation-processing, jpa, records]
detect: [dep:lombok, file:lombok.config]
related: [mapstruct, hibernate, spring-data-jpa, jackson, spring-boot, assertj]
---
Lombok annotation-processed boilerplate: used narrowly, configured in `lombok.config`, and kept away from JPA entities and public APIs where generated code bites.

## Verify
- `./gradlew compileJava`: the annotation processor runs and generated members resolve.
- `./gradlew test`: behavior of generated `equals`, `hashCode` and builders holds.
- `java -jar lombok.jar delombok src/main/java -d build/delombok`: inspect generated source (when the Lombok jar is available locally).
- `grep -rnE "@Data|@EqualsAndHashCode|@ToString" src/main --include=*Entity*.java`: risky annotations on entities.

## Test first
Test the behavior Lombok generates when you depend on it (equality, builder defaults).
```java
class MoneyTest {
  @Test void equalByAmountAndCurrency() {
    var a = Money.builder().amount(5).currency("EUR").build();
    var b = Money.builder().amount(5).currency("EUR").build();
    assertEquals(a, b);
    assertEquals(a.hashCode(), b.hashCode());
  }
}
@Value @Builder class Money { long amount; String currency; }
```

## Do
- Gradle needs both: `compileOnly("org.projectlombok:lombok")` and `annotationProcessor("org.projectlombok:lombok")` (same for `testCompileOnly` and `testAnnotationProcessor`). Maven uses `provided` scope plus the processor path.
- Prefer `@Value` for immutable types, `@Builder` with `@Singular` for collections, `@RequiredArgsConstructor` for constructor injection.
- Use `@Slf4j` (or the matching logger annotation) instead of hand-written loggers.
- Put project rules in `lombok.config`: `config.stopBubbling = true`, `lombok.addLombokGeneratedAnnotation = true` (so coverage tools skip generated code), `lombok.anyConstructor.addConstructorProperties = true` when Jackson needs it.
- Use `@Builder.Default` for field defaults with builders; `@With` for immutable copies.
- Use `@NonNull` for null checks that throw `NullPointerException` at the boundary.
- Prefer Java records for plain data on Java 16+; keep Lombok for builders and logging.
- Make sure MapStruct's processor comes after Lombok (add `lombok-mapstruct-binding`).

## Avoid
- `@Data` on JPA entities: generated `equals`/`hashCode`/`toString` touch lazy associations and break identity across states. Write them by hand (id-based) or use `@Getter`/`@Setter` only.
- `@ToString` and `@EqualsAndHashCode` including bidirectional relations: infinite recursion or `StackOverflowError`. Use `@ToString.Exclude` and `@EqualsAndHashCode.Exclude`.
- `@Builder` on classes with a no-args constructor requirement (JPA, Jackson): the constructor disappears. Add `@NoArgsConstructor` and `@AllArgsConstructor`, or use `@Jacksonized`.
- `@Builder` with field initializers and no `@Builder.Default`: initializers are ignored, fields come out null.
- `@SneakyThrows` and `val` everywhere: hide checked exceptions and types. Use sparingly.
- Missing `annotationProcessor` configuration on Gradle: "cannot find symbol" for generated methods.
- `@Setter` on value types: breaks immutability.

## Review
- [ ] Gradle has both compileOnly and annotationProcessor entries (main and test).
- [ ] No `@Data` or relation-including equals/toString on entities.
- [ ] Builders have defaults via `@Builder.Default` and keep required constructors.
- [ ] `lombok.config` states project policy, including generated-code annotation.
- [ ] Records are used where they replace Lombok cleanly.
