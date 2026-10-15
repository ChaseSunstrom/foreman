---
name: kotest
title: Kotest
area: jvm
tags: [kotlin, testing, bdd, property-testing, assertions, coroutines]
detect: [dep:kotest-runner-junit5, dep:kotest-assertions-core, dep:kotest-property, dep:kotest-extensions-spring]
related: [mockk, kotlin-coroutines, gradle, junit5, ktlint, detekt]
---
Kotest specs, matchers and property tests on the JUnit Platform runner, with coroutine-aware tests and explicit isolation.

## Verify
- `./gradlew test`: Kotest specs run (the Gradle `test` task must use `useJUnitPlatform()`).
- `./gradlew test --tests "com.acme.OrderSpec"`: one spec class.
- `grep -rn "useJUnitPlatform" build.gradle.kts`: the platform runner is enabled, else zero tests run silently.
- `./gradlew test -i | grep -E "PASSED|FAILED|SKIPPED"`: tests are discovered, not just compiled.

## Test first
Tests live in `src/test/kotlin`, one spec per class.
```kotlin
class PriceSpec : FunSpec({
    test("discount never makes price negative") {
        checkAll(Arb.int(1..10_000), Arb.int(0..200)) { price, pct ->
            applyDiscount(price, pct) shouldBeGreaterThanOrEqual 0
        }
    }
    test("rejects negative price") {
        shouldThrow<IllegalArgumentException> { applyDiscount(-1, 10) }
    }
})
```

## Do
- Pick one spec style per project (`FunSpec`, `StringSpec`, `BehaviorSpec`, `DescribeSpec`) and stay consistent.
- Use `shouldBe`, `shouldThrow<T>`, `shouldContainExactly`; for several assertions use `assertSoftly(obj) { ... }`.
- Use `checkAll` and `forAll` with `Arb` generators for invariants, and add the failing seed as a regression test.
- Suspend functions can be called directly in test bodies; use `runTest` from kotlinx-coroutines-test for virtual time when needed.
- Share setup with `beforeTest` or `beforeSpec`, and lifecycle extensions (`install(...)`, `TestListener`) for containers.
- For Spring add `kotest-extensions-spring` and `extensions(SpringExtension)`; set `isolationMode` deliberately.
- Set timeouts via `timeout = 5.seconds` on config or project config (`AbstractProjectConfig`).
- Use `withData(...)` for table-driven cases.

## Avoid
- Forgetting `useJUnitPlatform()`: Gradle reports success with zero tests. Add it in the `test` task.
- Mutating shared state in a default `SingleInstance` spec: tests leak into each other. Use `isolationMode = IsolationMode.InstancePerTest` or reset in `beforeTest`.
- Mixing JUnit annotations (`@Test`) inside Kotest specs: not discovered. Use spec DSL, or JUnit alone.
- Mismatched `kotest-*` artifact versions: runtime linkage errors. Keep all on one version via a catalog.
- `delay` in tests for async: slow and flaky. Use `runTest`, `eventually { }`, or `continually`.
- Catching `AssertionError` broadly to check failures: use `shouldThrow<AssertionError>` narrowly.

## Review
- [ ] Platform runner enabled; test count in the report is non-zero.
- [ ] Property tests have sensible ranges and a pinned seed on failure.
- [ ] No shared mutable state across tests without an isolation decision.
- [ ] Async code is tested with virtual time or `eventually`, not sleeps.
- [ ] Soft assertions group related checks.
