---
name: maven
title: Maven
area: jvm
tags: [maven, build, java, pom, dependencies, ci]
detect: [file:pom.xml, file:mvnw, file:.mvn/wrapper/maven-wrapper.properties]
related: [gradle, junit5, spring-boot, quarkus, testcontainers]
---
Maven builds: wrapper, lifecycle phases, dependency management, Surefire and Failsafe, reproducible versions.

## Verify
- `./mvnw -q verify`: compile, unit tests (Surefire) and integration tests (Failsafe) through the wrapper.
- `./mvnw -q dependency:tree -Dverbose`: conflicting or duplicated versions.
- `./mvnw -q help:effective-pom`: the real configuration after inheritance and BOM imports.
- `./mvnw -q versions:display-dependency-updates`: outdated dependencies (needs the versions plugin).
- `./mvnw -q enforcer:enforce`: rules pass, when the enforcer plugin is configured.

## Test first
Unit tests: `src/test/java`, named `*Test`, run by Surefire. Integration tests: `*IT`, run by Failsafe in the `verify` phase.
```java
class PriceTest {
  @Test void negativeQuantityThrows() {
    assertThrows(IllegalArgumentException.class, () -> Price.total(10, -1));
  }
}
```
Run just that class first: `./mvnw -q test -Dtest=PriceTest`.

## Do
- Commit `mvnw` and `.mvn/`; upgrade with `./mvnw wrapper:wrapper -Dmaven=<v>`.
- Manage versions in `<dependencyManagement>` or import a BOM with `<scope>import</scope>` and `<type>pom</type>`.
- Declare properties for versions (`<java.version>`, `<maven.compiler.release>`); use `release` rather than `source` and `target`.
- Pin plugin versions in `<pluginManagement>`; unpinned plugins make builds drift.
- Give each dependency the narrowest scope (`test`, `provided`, `runtime`).
- Split multi-module builds with a parent POM of `<packaging>pom</packaging>` and run one module with `-pl module -am`.
- Set `project.build.sourceEncoding` to UTF-8.

## Avoid
- `LATEST`, `RELEASE` or version ranges: non-reproducible. Pin them.
- Integration tests named `*Test`: Surefire runs them before the container is up. Name them `*IT` for Failsafe.
- Committing `settings.xml` with credentials: use `${env.X}` and server ids.
- Skipping tests with `-DskipTests` in CI to get green: fix or quarantine the test.
- Duplicate dependency declarations that override the managed version silently: remove the explicit `<version>`.
- Copying a transitive jar into your POM to "fix" a conflict: use `<exclusions>` or dependencyManagement.
- Running with a system `mvn` when `mvnw` exists.

## Review
- [ ] Wrapper present; Java release configured through `maven.compiler.release`.
- [ ] No unpinned plugins or ranged versions.
- [ ] `dependency:tree` shows no unintended duplicates.
- [ ] Integration tests are named for Failsafe and run in `verify`.
- [ ] No credentials in POM or committed settings.
