---
name: xcuitest
title: XCUITest
area: testing
tags: [testing, ios, swift, ui, xcode, e2e, mobile]
detect: [file:*UITests.swift, file:*UITests/*.swift, ext:.xcuitest]
related: [appium, detox, e2e-strategy, flaky-tests, accessibility-testing]
---
XCUITest: Apple's native UI testing framework, driving the app by accessibility identifiers with expectation-based waits.

## Verify
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: the UI tests run on a named simulator.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:AppUITests/LoginTests`: one test class runs.
- `xcrun simctl list devices available`: the destination name exists.
- `xcodebuild test -scheme App -destination '...' -resultBundlePath out.xcresult`: a result bundle with screenshots and logs for failures.

## Test first
```swift
final class LoginTests: XCTestCase {
    override func setUp() {
        continueAfterFailure = false
        let app = XCUIApplication()
        app.launchArguments = ["-uitesting"]
        app.launch()
    }

    func testWrongPasswordShowsError() {
        let app = XCUIApplication()
        app.textFields["email"].tap()
        app.textFields["email"].typeText("a@b.co")
        app.secureTextFields["password"].tap()
        app.secureTextFields["password"].typeText("wrong")
        app.buttons["login"].tap()
        XCTAssertTrue(app.staticTexts["login-error"].waitForExistence(timeout: 5))
    }
}
```

## Do
- Set `accessibilityIdentifier` in the app on every element tests touch and query by it.
- Wait with `waitForExistence(timeout:)` or `XCTNSPredicateExpectation`; never `sleep`.
- Launch with `launchArguments` / `launchEnvironment` to switch the app to a stubbed backend and fixed data.
- Set `continueAfterFailure = false` so the first failure stops the test.
- Use page-object structs per screen to hold queries.
- Reset state per test (terminate and relaunch, or a launch argument that wipes the store).
- Use `XCTContext.runActivity` to group steps and attach screenshots on failure.
- Test on at least one small and one large device size in CI.

## Avoid
- `sleep(3)` between steps: slow and still flaky. Use `waitForExistence`.
- Querying by label text or index (`buttons.element(boundBy: 2)`): breaks on copy or layout changes. Use identifiers.
- Live network calls: flaky and slow. Inject a stub through launch arguments.
- Tests that depend on the previous test's login: reset state in `setUp`.
- Using UI tests for logic: slow. Move logic to unit tests and keep UI tests for flows.
- Running on a dirty simulator: stale keychain and permissions. Erase it (`xcrun simctl erase`) in CI.

## Review
- [ ] All queried elements have accessibility identifiers.
- [ ] No `sleep`; waits have timeouts.
- [ ] The backend is stubbed through launch configuration.
- [ ] State is reset per test; failure screenshots are attached.
- [ ] CI pins a simulator name and OS.
