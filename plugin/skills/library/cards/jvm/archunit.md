---
name: archunit
title: ArchUnit
area: jvm
tags: [java, kotlin, architecture, testing, layers, dependencies, conventions]
detect: [dep:archunit, dep:archunit-junit5, dep:archunit-junit4]
related: [junit5, spring-boot, assertj, gradle, maven]
---
ArchUnit architecture tests: layers, package cycles and naming rules written as ordinary unit tests over imported bytecode, with a frozen baseline for legacy violations.

## Verify
- `./gradlew test --tests "*ArchitectureTest"`: architecture rules only.
- `./gradlew test`: rules run with the normal suite.
- `mvn -q test -Dtest=ArchitectureTest`: Maven equivalent.
- `ls archunit_store 2>/dev/null`: a frozen violation store exists only when `FreezingArchRule` is used.

## Test first
Write the rule, watch it fail on a real violation, then fix the code.
```java
@AnalyzeClasses(packages = "com.acme", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {
  @ArchTest
  static final ArchRule domainIsIndependent =
      noClasses().that().resideInAPackage("..domain..")
          .should().dependOnClassesThat().resideInAnyPackage("..web..", "..persistence..");

  @ArchTest
  static final ArchRule noCycles =
      slices().matching("com.acme.(*)..").should().beFreeOfCycles();
}
```

## Do
- Import with `@AnalyzeClasses(packages = ..., importOptions = ...)` and `@ArchTest` fields from `archunit-junit5`; or `new ClassFileImporter().importPackages(...)`.
- Use `layeredArchitecture().consideringOnlyDependenciesInLayers()` with `layer(...).definedBy(...)` and `whereLayer(...).mayOnlyBeAccessedByLayers(...)`.
- Use `onionArchitecture()` for hexagonal layouts: `domainModels`, `domainServices`, `applicationServices`, `adapter(...)`.
- Add `.because("reason")` to every rule so failures explain the policy.
- Enforce conventions: `classes().that().areAnnotatedWith(RestController.class).should().haveSimpleNameEndingWith("Controller")`, `noClasses().should().accessClassesThat().resideInAPackage("java.util.logging..")`, `fields().that().areStatic().and().areNotFinal().should(...)`.
- Adopt on legacy code with `FreezingArchRule.freeze(rule)` and commit the store; shrink it over time.
- Keep the analyzed class set explicit and cached (`@AnalyzeClasses` caches imports within a run).
- Exclude generated code and tests with `ImportOption`.
- Share a rules class across modules via test fixtures.

## Avoid
- Package-string typos: a rule over a non-existent package passes vacuously. Fail on empty with `archRule.allowEmptyShould(false)` or `archunit.properties` `archRule.failOnEmptyShould=true`.
- Rules that depend on tests or generated classes: noise. Use `DoNotIncludeTests` and exclude generated packages.
- Freezing every rule at once with a stale store: new violations get hidden if the store is regenerated blindly. Review store diffs.
- Overly broad `..` patterns that match unrelated packages: false failures. Anchor with the base package.
- Slow tests from importing the whole classpath repeatedly: restrict `packages` and share via `@AnalyzeClasses` on one class.
- Asserting style that formatters or linters already cover: keep ArchUnit for structure.

## Review
- [ ] Every rule has `because(...)` and fails when a violating class is added.
- [ ] Rules fail on empty matches rather than passing vacuously.
- [ ] Frozen store, if any, is committed and only shrinks.
- [ ] Layer and package names match the actual structure.
- [ ] Architecture tests run in the default `test` task.
