---
name: uikit
title: UIKit
area: mobile
tags: [swift, ios, uikit, ui, auto-layout, apple]
detect: [file:*.storyboard, file:*.xib, file:AppDelegate.swift, file:SceneDelegate.swift, file:*.xcodeproj]
related: [swiftui, swift-concurrency, xctest, xcodebuild, core-data]
---
UIKit apps: view controllers, Auto Layout, diffable data sources, scenes and the main-thread rule.

## Verify
- `xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build`: compiles (substitute your scheme and an installed simulator).
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: unit and UI tests.
- `xcrun simctl list devices available`: valid destination names.
- `swiftlint`: style, if configured.

## Test first
Instantiate the view controller, call `loadViewIfNeeded()`, and assert on outlets and state.
```swift
@MainActor
final class LoginViewControllerTests: XCTestCase {
    func testSubmitDisabledWhenEmailBlank() {
        let vc = LoginViewController(viewModel: .init())
        vc.loadViewIfNeeded()
        vc.emailField.text = ""
        vc.emailField.sendActions(for: .editingChanged)
        XCTAssertFalse(vc.submitButton.isEnabled)
    }
}
```

## Do
- Build layout with Auto Layout anchors or `NSLayoutConstraint.activate([...])`; set `translatesAutoresizingMaskIntoConstraints = false` on views you constrain in code.
- Drive lists with `UICollectionViewDiffableDataSource` and compositional layout; use `UIContentConfiguration` for cells.
- Keep view controllers thin: logic in a view model or presenter that is testable.
- Update UI only on the main actor (`@MainActor` on controllers and view models).
- Use scene-based lifecycle (`SceneDelegate`, `UIWindowScene`) for window setup.
- Capture `[weak self]` in closures stored by long-lived objects; unsubscribe observers.
- Support Dynamic Type (`UIFontMetrics`, `adjustsFontForContentSizeCategory`) and Dark Mode (semantic colors).

## Avoid
- `UITableView` reloadData for every change: flicker and lost selection. Use diffable snapshots.
- Mixing frames with constraints on the same view: layout conflicts in the console. Pick one.
- UI calls from background callbacks: crashes or silent glitches. Hop to `@MainActor`.
- Retain cycles from closures held by a view controller (`self.handler = { self.x }`): `deinit` never runs. Use `[weak self]`.
- Force-unwrapping outlets before `viewDidLoad`: they are nil. Touch them after `loadViewIfNeeded()`.
- Hardcoded sizes and colors: break on other devices and in Dark Mode. Use safe-area anchors and semantic colors.
- Massive view controllers owning networking: untestable. Inject services.

## Review
- [ ] No Auto Layout conflict warnings when running.
- [ ] Closures that outlive the screen use `[weak self]`; `deinit` runs when popped.
- [ ] All UI mutations happen on the main actor.
- [ ] Lists use diffable data sources and handle empty and error states.
- [ ] Dynamic Type and Dark Mode were checked.
