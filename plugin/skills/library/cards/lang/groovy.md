---
name: groovy
title: Groovy
area: lang
tags: [groovy, gradle, spock, jenkins, jvm, codenarc]
detect: [ext:.groovy, ext:.gradle, file:Jenkinsfile, file:build.gradle, dep:spock-core]
related: [clojure]
---
Groovy code: Gradle build scripts, Spock specs, Jenkins pipelines, optional static compilation.

## Verify
- `./gradlew build`: compiles main and test sources and runs checks.
- `./gradlew test`: runs Spock and JUnit specs (reports in `build/reports/tests/test`).
- `./gradlew codenarcMain codenarcTest`: CodeNarc lint, when the `codenarc` plugin is applied.
- `groovy -e 'println GroovySystem.version'`: the runtime on PATH, when scripts run outside Gradle.

## Test first
Spock specs live in `src/test/groovy/` and end `Spec`; blocks are `given/when/then/expect/where`.
```groovy
import spock.lang.Specification
import spock.lang.Unroll

class ParserSpec extends Specification {
  @Unroll
  def "parse(#input) fails"() {
    when:
    Parser.parse(input)

    then:
    thrown(IllegalArgumentException)

    where:
    input << ["", " ", null]
  }
}
```
Mock collaborators with `Mock(Repo)` and verify with `1 * repo.save(_)`.

## Do
- Add `@CompileStatic` (or `@TypeChecked`) to non-dynamic classes so type errors surface at compile time; keep dynamic code for DSLs.
- Declare types on public method signatures and fields; use `def` only locally.
- Use Groovy's null-safe `?.` and Elvis `?:`, but validate inputs at boundaries.
- In Gradle, use the Kotlin or Groovy DSL consistently, version catalogs (`libs.versions.toml`) for dependencies, and lazy APIs (`tasks.register`).
- In Jenkins pipelines, keep logic in a shared library under `vars/` and `src/`, and test it with JenkinsPipelineUnit.
- Use `@Immutable`, `@ToString` and `@EqualsAndHashCode` AST transforms for value classes.

## Avoid
- Everything dynamic: a typo in a property or method name fails only at runtime. Use `@CompileStatic`.
- GString as a map key or in `Set` lookups: `"$a" ` is not equal to a `String` with the same text hash-wise. Call `.toString()`.
- Assuming `==` is identity: in Groovy it calls `equals`/`compareTo`. Use `.is()` for identity.
- Double-quoted strings with `$` in shell steps (`sh "rm $USER_INPUT"`): Groovy interpolates secrets and input into the command line. Use single quotes with env vars in Jenkins (`sh 'rm "$FILE"'`).
- Non-serializable objects (`Matcher`, `JsonSlurper` results) held across steps in a Jenkins CPS pipeline: `NotSerializableException`. Keep them inside `@NonCPS` methods.
- `tasks.create` and eager `task` configuration in Gradle: slows configuration and breaks configuration cache. Use `tasks.register`.
- `Eval.me` or `GroovyShell.evaluate` on untrusted text: code execution.

## Review
- [ ] Non-DSL classes are `@CompileStatic`, with typed public signatures.
- [ ] No string interpolation of untrusted values into shell commands or Eval.
- [ ] Spock specs cover failure cases through `where:` tables.
- [ ] Gradle dependencies use the catalog, and tasks are registered lazily.
- [ ] Jenkins code that uses non-serializable objects sits in `@NonCPS`.
