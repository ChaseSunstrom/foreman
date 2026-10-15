---
name: swiftui-navigation
title: SwiftUI Navigation
area: mobile
tags: [swift, swiftui, navigation, navigationstack, routing, ios]
detect: [file:*.xcodeproj, file:Package.swift]
related: [swiftui, swift-concurrency, xctest, swift-testing, deep-links]
---
SwiftUI navigation: `NavigationStack` driven by value-based paths and state-owned routing, so screens can be restored and deep linked.

## Verify
- `xcodebuild build -scheme App -destination 'generic/platform=iOS Simulator'`: the app compiles for the simulator.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: unit and UI tests pass (use an installed device name).
- `grep -rn "NavigationView" --include=*.swift .`: finds the deprecated container, which should return nothing.

## Test first
Keep routing in an observable model, and test it without views.
```swift
import Testing
@testable import App

@MainActor
@Test func openingOrderPushesDetail() {
    let router = Router()
    router.open(.order(id: 7))
    #expect(router.path == [.order(id: 7)])
}

@MainActor
@Test func popToRootClearsPath() {
    let router = Router(path: [.order(id: 1), .receipt])
    router.popToRoot()
    #expect(router.path.isEmpty)
}
```

## Do
- Use `NavigationStack(path: $router.path)` with `.navigationDestination(for: Route.self) { ... }`, where `Route` is a `Hashable` (and `Codable` if restoring) enum.
- Push with `NavigationLink(value: Route.order(id: 7))`, or `router.path.append(...)` from code.
- Keep `path` in an `@Observable` (or `ObservableObject`) router held by the owning view, with one stack per tab.
- Use `NavigationSplitView` for sidebar/detail layouts, with selection bound to state.
- Present sheets with `.sheet(item: $router.sheet)` and an `Identifiable` enum, not several booleans.
- Register `navigationDestination` once per type, high in the stack's root, not inside lazy rows.
- Restore state by encoding the path with `NavigationPath.CodableRepresentation` (or an array of a `Codable` route) in `SceneStorage`.
- Drive tab selection from a bound state value, so deep links can switch tabs and push in one step.

## Avoid
- `NavigationView`: deprecated, and it behaves differently across versions. Use `NavigationStack` or `NavigationSplitView`.
- `NavigationLink(destination:)` with eagerly created views in lists: destinations init on every render. Use value links.
- Mutating the path off the main actor or during view body evaluation: it produces undefined behavior and warnings. Update it in handlers on the main actor.
- Several `navigationDestination` modifiers for the same type: the last one wins unpredictably. Register one.
- `navigationDestination` inside a lazy container such as `List` rows: it may not be seen. Attach it to the stack root.
- Boolean flags per screen (`isShowingX`): states conflict. Use an enum route.
- Putting the stack inside another stack: duplicate nav bars and broken back behavior.

## Review
- [ ] One `NavigationStack` per tab, with a route type that is `Hashable`.
- [ ] Destinations are registered once, at the stack root.
- [ ] Routing logic is in a testable model, and tests cover push, pop and reset.
- [ ] Deep link and restoration paths build the same `Route` values.
- [ ] No `NavigationView` or eager `NavigationLink(destination:)` remains.
