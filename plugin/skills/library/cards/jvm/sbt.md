---
name: sbt
title: sbt
area: jvm
tags: [scala, sbt, build, dependencies, testing, jvm]
detect: [file:build.sbt, file:project/build.properties, file:project/plugins.sbt, ext:.scala]
related: [akka-pekko, junit5, testcontainers, maven, gradle]
---
sbt builds for Scala: `build.sbt` settings, multi-project builds, cross-building, scalatest and munit tests.

## Verify
- `sbt compile test`: compile and run all tests.
- `sbt "testOnly *PriceSpec"`: one suite runs.
- `sbt dependencyTree`: resolved graph and conflicts (sbt 1.4 and later includes the plugin).
- `sbt "scalafmtCheckAll"`: formatting, when sbt-scalafmt is configured.
- `sbt +test`: the build passes on every `crossScalaVersions` entry.

## Test first
Tests live in `src/test/scala`. Add the framework dependency, then write a failing spec.
```scala
// build.sbt
libraryDependencies += "org.scalameta" %% "munit" % munitVersion % Test

// src/test/scala/PriceSuite.scala
class PriceSuite extends munit.FunSuite {
  test("negative quantity is rejected") {
    intercept[IllegalArgumentException](Price.total(10, -1))
  }
}
```
Equivalent with scalatest: `class PriceSpec extends AnyFlatSpec with Matchers`.

## Do
- Pin `sbt.version` in `project/build.properties`; declare plugins in `project/plugins.sbt`.
- Use `%%` for Scala libraries (appends the binary version) and `%` for Java ones; add `% Test` for test scope.
- Define shared settings in `ThisBuild / scalaVersion := "..."` and `lazy val commonSettings`.
- Split modules with `lazy val core = project`, `lazy val api = project.dependsOn(core)`, and an aggregate root.
- Use `sbt-scalafmt` and `scalacOptions ++= Seq("-deprecation", "-feature", "-Wunused:imports")` appropriate to the Scala version.
- Pick versions in one place (`val`s in `build.sbt` or a `Dependencies.scala` in `project/`).
- Run the sbt server or `sbt ~test` for a fast loop.

## Avoid
- `%` where `%%` is needed: resolves a missing artifact with no Scala suffix.
- The deprecated `:=` string-key syntax with `in` (`scalacOptions in Compile`): use slash syntax (`Compile / scalacOptions`).
- `Process`-based global state and mutable `var`s in build code: use settings and tasks with proper dependencies.
- Mixing Scala 2 and Scala 3 library artifacts: use `.cross(CrossVersion.for3Use2_13)` deliberately.
- Unpinned plugin versions in `plugins.sbt`: builds drift.
- `sbt assembly` with duplicated META-INF without a merge strategy: fails or ships broken jars. Set `assembly / assemblyMergeStrategy`.
- Forking-less tests that leak static state: set `Test / fork := true` where needed.

## Review
- [ ] `sbt.version` and plugin versions are pinned.
- [ ] Cross-build passes if cross-versions are declared.
- [ ] Dependencies use the correct `%`/`%%` form and scope.
- [ ] Formatting and compiler warnings are enforced in CI.
- [ ] Tests are discoverable by the chosen framework.
