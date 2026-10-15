---
name: swift-testing
title: Swift Testing
area: mobile
tags: [swift, testing, ios, macros, unit-tests, parameterized]
detect: [file:Package.swift, file:*.xcodeproj, file:*.xctestplan]
related: [xctest, swift-package-manager, xcodebuild, swift-macros, swift-concurrency]
---
Swift Testing: the `import Testing` framework with `@Test`, `#expect` and `#require`, which coexists with XCTest in one target.

## Verify
- `swift test`: runs both Swift Testing and XCTest tests in a package.
- `swift test --filter MyModuleTests`: runs one suite or test by name.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: runs app tests on a simulator (use an installed device name).
- `swift test --parallel`: proves tests are independent when running concurrently.

## Test first
Tests live in the test target, and Swift Testing and XCTest files can share it.
```swift
import Testing
@testable import Cart

@Suite struct CartTests {
    @Test func emptyCartHasZeroTotal() {
        #expect(Cart().total == 0)
    }

    @Test(arguments: [(1, 10), (3, 30)])
    func totalScalesWithQuantity(qty: Int, expected: Int) throws {
        var cart = Cart()
        cart.add(Item(price: 10), quantity: qty)
        #expect(cart.total == expected)
    }
}
```

## Do
- Use `#expect(expr)` for soft assertions (the test continues) and `try #require(expr)` to unwrap or stop when later lines depend on it.
- Group with `@Suite` on a struct. Each test gets a fresh instance, so use `init()` for setup and `deinit` for teardown (on a class or actor).
- Parameterize with `@Test(arguments: collection)`. Zip two collections with `zip(a, b)`, because two bare collections run the Cartesian product.
- Assert errors with `#expect(throws: CartError.empty) { try cart.checkout() }` and `#expect(throws: Never.self)` for no-throw.
- Label tests: `@Test("Applies discount over 100", .tags(.pricing))` and declare tags in an extension of `Tag` with `@Tag`.
- Gate with traits: `.enabled(if:)`, `.disabled("reason")`, `.timeLimit(.minutes(1))`, `.serialized` for order-dependent suites.
- Test async code with `async` test functions, and use `confirmation("event") { confirm in ... }` for callbacks that should fire.
- Record known failures with `withKnownIssue { ... }` instead of deleting a test.

## Avoid
- Mixing `XCTAssert*` inside `@Test` functions: they do not report there. Use `#expect`.
- Using `@Test` on a method in an `XCTestCase` subclass: it is not discovered. Use a `@Suite` struct.
- UI tests and performance metrics in Swift Testing: keep `XCUIApplication` and `measure` in XCTest.
- Shared mutable state between tests: tests run in parallel by default, so use per-test instances or `.serialized`.
- Two bare argument collections when pairs were intended: the combinations multiply. Zip them.
- Conditions with side effects inside `#expect`: failures expand the expression, which confuses output. Compute first, then assert.

## Review
- [ ] Each test has one behavior, with `#require` guarding unwraps.
- [ ] Parameterized cases name inputs and expectations, with no repeated copy-paste tests.
- [ ] Order-dependent tests are `.serialized`, and nothing shares global state.
- [ ] Async callbacks use `confirmation`, with no sleeps.
- [ ] UI and performance tests remain in XCTest.
