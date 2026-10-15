---
name: swiftui
title: SwiftUI
area: mobile
tags: [swift, ios, swiftui, ui, declarative, apple]
detect: [file:*.xcodeproj, file:Package.swift, ext:.swift]
related: [swift-concurrency, swiftdata, xctest, xcodebuild, uikit, swift-package-manager]
---
SwiftUI views: declarative state-driven UI with property wrappers, Observation, navigation and previews.

## Verify
- `xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build`: the app compiles for a simulator (use your scheme and an installed device name).
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: unit and UI tests run.
- `xcrun simctl list devices available`: confirms the destination name exists.
- `swiftlint`: style, when the repo configures it.

## Test first
Keep logic in an observable model and test it without views.
```swift
import XCTest
@testable import App

@MainActor
final class CartModelTests: XCTestCase {
    func testAddingSameItemTwiceIncrementsQuantity() {
        let cart = CartModel()
        cart.add(.init(id: "a")); cart.add(.init(id: "a"))
        XCTAssertEqual(cart.lines.first?.quantity, 2)
    }
}
```
Use `#Preview` for visual states; use XCUITest for flows.

## Do
- Pick the owner: `@State` for view-local value state, `@Binding` for a child editing parent state, `@Environment` for shared values.
- Use `@Observable` (Observation framework) classes with `@State` to own and plain properties to read, on current OS targets; use `ObservableObject` only for older deployment targets.
- Navigate with `NavigationStack` and `navigationDestination(for:)`, with the path as state.
- Keep `body` cheap and pure; extract subviews with small inputs to limit invalidation.
- Use `.task { }` for async loading (auto-cancelled on disappear) and `.task(id:)` to reload on change.
- Give `ForEach` stable `Identifiable` ids.
- Add accessibility labels and Dynamic Type support.

## Avoid
- `NavigationView`: deprecated. Use `NavigationStack` or `NavigationSplitView`.
- `@ObservedObject` for an object the view creates: it is recreated on re-render. Own it with `@StateObject` (or `@State` with `@Observable`).
- `.onAppear { Task { ... } }` for loading: not cancelled. Use `.task`.
- `ForEach(items.indices)` with mutable arrays or `id: \.self` on non-unique values: crashes and wrong animations. Use identifiable models.
- Mutating state during `body` evaluation: undefined behavior and update loops. Mutate in actions and tasks.
- `AnyView` everywhere: erases identity and hurts diffing. Use `@ViewBuilder` or generics.
- Network or disk work on the main actor in a view model: UI hitches. Await off-actor services.

## Review
- [ ] Each piece of state has one owner and the right wrapper.
- [ ] Async work uses `.task` and respects cancellation.
- [ ] Lists use stable ids; navigation state is value-based.
- [ ] Previews exist for empty, loading and error states.
- [ ] Accessibility labels and Dynamic Type checked.
