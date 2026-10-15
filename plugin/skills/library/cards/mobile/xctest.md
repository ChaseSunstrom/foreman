---
name: xctest
title: XCTest
area: mobile
tags: [swift, xctest, testing, ios, xcuitest, tdd]
detect: [file:*.xctestplan, file:*Tests.swift, file:Package.swift, file:*.xcodeproj]
related: [xcodebuild, swift-package-manager, swiftui, uikit, swift-concurrency]
---
XCTest and XCUITest: unit tests, async tests, expectations, UI tests and test plans.

## Verify
- `swift test`: runs tests for a Swift package.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: runs unit and UI tests in an Xcode project.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:AppTests/CartTests`: one class.
- `xcrun simctl list devices available`: valid destination names.

## Test first
Name tests `test<Behavior>`; write the failing one first, async when the code is async.
```swift
@testable import App
import XCTest

final class PriceTests: XCTestCase {
    func testDiscountRoundsDownToCent() {
        XCTAssertEqual(Price(cents: 999).discounted(by: 0.1).cents, 899)
    }

    func testLoadThrowsOnOffline() async {
        let repo = Repo(client: OfflineClient())
        await XCTAssertThrowsErrorAsync(try await repo.load())
    }
}
```
Define `XCTAssertThrowsErrorAsync` as a small helper, since XCTest's own autoclosure form is synchronous.

## Do
- Use `setUpWithError` / `tearDownWithError` for per-test state; the class runs a fresh instance per test method.
- Prefer `async throws` tests over expectations for async/await code.
- Use `XCTestExpectation` plus `await fulfillment(of:timeout:)` for callback and notification code.
- Mark tests of `@MainActor` code `@MainActor`.
- Inject protocols or closures for clocks, networking and storage; use fakes rather than patching.
- For UI tests, set `accessibilityIdentifier` on elements and query by it; pass `launchArguments` or `launchEnvironment` to start in a known state.
- Use `XCTUnwrap` instead of force-unwrapping in tests, and `XCTAssertEqual(_, _, accuracy:)` for floats.

## Avoid
- `wait(for:timeout:)` inside async tests: can deadlock the executor. Use `await fulfillment(of:timeout:)`.
- Sleeping (`sleep`, `Task.sleep`) to wait for effects: flaky and slow. Await the result or use expectations.
- UI tests that depend on network or a previous test's state: flaky. Stub with launch arguments and reset in `setUp`.
- Static or global singletons shared across tests: order dependence. Inject and reset.
- Querying UI by visible text only: breaks on localization. Use accessibility identifiers.
- `@testable import` in release test builds: fails unless testability is enabled. Run tests in Debug.
- Forgetting `continueAfterFailure = false` in UI tests: later steps fail confusingly. Set it in `setUp`.

## Review
- [ ] New behavior has a test that failed first for the right reason.
- [ ] No sleeps and no cross-test shared state.
- [ ] Async code is tested with `async` tests or awaited expectations.
- [ ] UI tests use identifiers and a known launch state.
- [ ] Tests run on the CI destination and in a test plan if one exists.
