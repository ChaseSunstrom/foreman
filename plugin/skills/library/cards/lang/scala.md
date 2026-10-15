---
name: scala
title: Scala
area: lang
tags: [scala, sbt, scalatest, munit, cats, scalafmt]
detect: [ext:.scala, ext:.sc, file:build.sbt, file:build.sc, file:project/build.properties]
related: [java, kotlin]
---
Scala baseline: sbt (or Mill) builds, scalafmt, MUnit or ScalaTest, immutable ADTs, Option and Either over null and exceptions.

## Verify
- `sbt compile`: compiles all modules.
- `sbt test`: all tests (`sbt "testOnly *PortParserSuite"` for one suite).
- `sbt scalafmtCheckAll`: formatting, when sbt-scalafmt is enabled.
- `sbt "scalafixAll --check"`: lint rewrites pending, when sbt-scalafix is enabled.

## Test first
MUnit (or ScalaTest) under `src/test/scala`, suite names ending `Suite` or `Spec`.
```scala
import munit.FunSuite

class PortParserSuite extends FunSuite:
  test("rejects empty input"):
    assert(PortParser.parse("").isLeft)
```
Match the project's Scala version syntax (indentation-based above is Scala 3; Scala 2 uses braces).

## Do
- Model data with `case class` and closed hierarchies (`sealed trait` or Scala 3 `enum`); match exhaustively.
- Return `Option`, `Either[E, A]` or `Try` for absence and failure; compose with `for` comprehensions.
- Keep values immutable (`val`, immutable collections); use `copy` for updates.
- Enable `-Wunused`, `-Xfatal-warnings` (or `-Werror`) and exhaustivity warnings via `scalacOptions`.
- Use `scala.concurrent.Future` with an explicit `ExecutionContext`, or an effect library (cats-effect, ZIO) consistently, not both mixed.
- Pin `sbt.version` in `project/build.properties` and `scalaVersion` in build.sbt.
- Cross-build deliberately with `crossScalaVersions` when publishing.

## Avoid
- `null` and `.get` on `Option`/`Try`/`Either`: runtime exceptions. Use `fold`, `getOrElse` or pattern matching.
- Matching on a non-sealed type or ending with `case _ =>` on your own ADT: new cases fall through silently. Seal and enumerate.
- `var` and mutable collections shared between Futures: races. Use immutable data or atomics.
- Blocking (`Await.result`, `Thread.sleep`) on the global `ExecutionContext`: starves it. Use a dedicated blocking context or `blocking {}`.
- Implicit conversions for convenience: surprising resolution. Use extension methods and explicit imports (`given`/`using` in Scala 3).
- Catching `Throwable`: swallows fatal errors. Use `NonFatal`.
- Mixing Scala 2 and Scala 3 syntax or library builds (`_2.13` vs `_3`): binary incompatibility. Use `%%` and one Scala line per module.
- Large `for` over `Future` created before the comprehension: runs concurrently by accident or not at all. Create dependent Futures inside.

## Review
- [ ] No `null`, `.get` or `Await` in production code paths.
- [ ] ADTs sealed and matches exhaustive without a catch-all.
- [ ] Fatal warnings on; scalafmt clean.
- [ ] Blocking calls isolated from the main execution context.
- [ ] Scala and sbt versions pinned and consistent across modules.
