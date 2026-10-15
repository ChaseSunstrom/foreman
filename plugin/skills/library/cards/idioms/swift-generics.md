---
name: swift-generics
title: Swift generics and protocols
area: idioms
tags: [swift, generics, protocols, associated-types, opaque-types, existentials]
detect: [file:Package.swift]
related: [swift, xctest, swift-concurrency]
---
Swift generics: constrained generics and `some` by default, `any` only for real runtime polymorphism.

## Verify
- `swift build`: the package compiles, including generic constraints.
- `swift test`: the suite passes.
- `swift build -c release`: whole-module specialization works in release, where generic code is optimized.

## Test first
XCTest, with a generic function exercised on two types.
```swift
import XCTest
@testable import Lib

final class MaxTests: XCTestCase {
    func testLargestWorksForIntAndString() {
        XCTAssertEqual(largest([3, 9, 2]), 9)
        XCTAssertEqual(largest(["b", "z", "a"]), "z")
        XCTAssertNil(largest([Int]()))
    }
}
```
Write `func largest<T: Comparable>(_ xs: [T]) -> T?` to make it pass.

## Do
- Constrain with protocols: `func f<T: Sequence>(_ s: T) where T.Element: Hashable`.
- Use `some Protocol` for parameters and return types when one concrete type is used, and `any Protocol` when types vary at runtime.
- Use associated types for protocols whose requirements mention a related type, and `where` clauses to relate them.
- Provide behavior with protocol extensions and constrained extensions (`extension Collection where Element: Numeric`).
- Use primary associated types for readable constraints: `some Collection<Int>`.
- Prefer value types (structs and enums) that conform to protocols over class hierarchies.
- Use parameter packs (`each T`) for variadic generics where the toolchain supports them.

## Avoid
- `any Protocol` everywhere: it adds dynamic dispatch and boxing, and loses type relations. Use generics or `some`.
- Protocols with `Self` or associated-type requirements used as bare existential types in old code: use generics, or `any` on current toolchains.
- Over-constraining (`T: Hashable & Codable & Sendable` with no need): it limits callers. Ask only what the body uses.
- Specialization blockers in hot paths: unspecialized generics across module boundaries are slow. Mark `@inlinable` for small public generic functions.
- Protocol extension methods not declared in the protocol: they dispatch statically, so overrides are ignored through the protocol type. Declare the requirement.
- Type erasure wrappers written by hand when `any` or `some` suffices.

## Review
- [ ] Each generic constraint is needed by the body.
- [ ] `some` and `any` are used deliberately and not interchangeably.
- [ ] Tests instantiate generics with at least two different types and an empty input.
- [ ] Public generic APIs consider `@inlinable` and `Sendable`.
- [ ] Protocol requirements are declared, not only provided in extensions.
