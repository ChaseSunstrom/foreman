---
name: swift
title: Swift
area: lang
tags: [swift, swiftpm, xcode, xctest, concurrency, optionals]
detect: [ext:.swift, file:Package.swift, file:*.xcodeproj, file:*.xcworkspace]
related: [ios, swiftui]
---
Swift baseline: SwiftPM or Xcode builds, XCTest or Swift Testing, optionals and value types, structured concurrency with actors.

## Verify
- `swift build`: the SwiftPM package compiles.
- `swift test`: the package tests.
- `swift test --filter FooTests`: one suite while iterating.
- `xcodebuild -list`: lists schemes and targets for an Xcode project, to pick the scheme for `xcodebuild test`.

## Test first
XCTest under `Tests/<Target>Tests/`, class `FooTests: XCTestCase`.
```swift
import XCTest
@testable import MyLib

final class PortParserTests: XCTestCase {
    func testRejectsEmpty() {
        XCTAssertThrowsError(try parsePort(""))
    }
}
```

## Do
- Prefer `struct` and `enum` with associated values; use `class` only for identity or reference semantics.
- Unwrap with `guard let` and early return; use `??` for defaults.
- Use `async`/`await`, `Task` and `TaskGroup`; protect shared mutable state with an `actor`; mark UI types `@MainActor`.
- Model failures with `throws` and typed error enums conforming to `Error`.
- Use `Codable` for JSON, with `CodingKeys` for naming differences.
- Capture `[weak self]` in escaping closures stored by the object itself.
- Pin dependencies in Package.swift with version requirements and commit `Package.resolved` for apps.

## Avoid
- Force unwrap `!` and `try!` on runtime data: crash. Use `guard let` and `do/catch`.
- Strong reference cycles through closures or delegates: leaks. Use `weak` or `unowned` delegates and `[weak self]`.
- Updating UI from a background task: undefined behavior or warnings. Hop to `@MainActor`.
- Mixing completion handlers with async code by hand: lost errors and double resumes. Wrap with `withCheckedThrowingContinuation` and resume exactly once.
- `Task { }` fire-and-forget with no cancellation: orphaned work. Keep the handle and cancel it.
- Using `Date()` and `DispatchQueue.main.asyncAfter` for test timing: flaky. Inject a clock.
- Ignoring Sendable warnings: data races under strict concurrency. Fix the type or isolate it.

## Review
- [ ] No new `!`, `try!` or `as!` on external data.
- [ ] Closures that outlive the call do not retain `self` cyclically.
- [ ] UI mutations are on the main actor; shared state sits in an actor.
- [ ] Continuations resume exactly once.
- [ ] Tests run via `swift test` or the scheme and cover an error path.
