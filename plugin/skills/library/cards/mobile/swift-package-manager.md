---
name: swift-package-manager
title: Swift Package Manager
area: mobile
tags: [swift, spm, packages, dependencies, build, apple]
detect: [file:Package.swift, file:Package.resolved]
related: [xcodebuild, xctest, swift-concurrency, swiftui]
---
SwiftPM: Package.swift manifests, targets, dependencies, resolution, plugins and swift test.

## Verify
- `swift build`: all targets compile.
- `swift test`: runs every test target.
- `swift test --filter CartTests/testTotal`: one test while iterating.
- `swift package resolve`: dependencies resolve and Package.resolved is consistent.
- `swift package describe`: manifest parses; shows targets and products.

## Test first
Add a `.testTarget` that depends on the target under test, in `Tests/<Name>Tests/`.
```swift
// Package.swift
.target(name: "Cart"),
.testTarget(name: "CartTests", dependencies: ["Cart"]),

// Tests/CartTests/CartTests.swift
import XCTest
@testable import Cart

final class CartTests: XCTestCase {
    func testTotalAppliesDiscount() {
        XCTAssertEqual(Cart.total(prices: [100], discount: 0.1), 90)
    }
}
```
Swift Testing (`import Testing`, `@Test`, `#expect`) also runs under `swift test` on toolchains that include it.

## Do
- Start Package.swift with `// swift-tools-version:` matching the lowest toolchain you support.
- Declare dependencies with a version requirement (`from: "1.2.0"`, or `exact:` for a pin), and list them per target with `.product(name:package:)`.
- Keep targets small and acyclic; expose only what clients need via `products`.
- Commit `Package.resolved` for applications and executables; libraries usually leave it out.
- Put resources in `resources: [.process("Assets")]` and read them via `Bundle.module`.
- Declare `platforms: [.iOS(.v16), .macOS(.v13)]` to the minimum you use.
- Use `swift package update` deliberately and review the Package.resolved diff.

## Avoid
- Branch dependencies (`branch: "main"`): non-reproducible builds, and they cannot be used by published packages. Use a tagged version.
- Tests importing a target without `@testable` when they need internals: the symbols are not visible. Use `@testable import` (debug builds only).
- Circular target dependencies: SwiftPM refuses to resolve. Extract the shared piece into a third target.
- Relying on `Bundle.main` in a package: resources live in `Bundle.module`.
- Missing `platforms` for APIs newer than the default: availability errors at build. Declare the platform floor.
- Hand-editing Package.resolved: use `swift package resolve` or `update`.
- Deleting `.build` as the first response to every error: read the diagnostic; clean only for stale-state symptoms.

## Review
- [ ] Tools version and platform floors are set on purpose.
- [ ] Dependencies use semantic version ranges or pins, not branches.
- [ ] Package.resolved is committed for apps and the diff is reviewed.
- [ ] Each target has tests and no dependency cycles.
- [ ] Public surface (products, `public` symbols) is minimal.
