---
name: swiftdata
title: SwiftData
area: mobile
tags: [swift, swiftdata, persistence, ios, database, apple]
detect: [file:*.xcdatamodeld, file:*.xcodeproj, ext:.swift]
related: [core-data, swiftui, swift-concurrency, xctest]
---
SwiftData: `@Model` classes, `ModelContainer` and `ModelContext`, `@Query`, predicates and schema migration.

## Verify
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: tests with an in-memory container pass.
- `xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build`: `#Predicate` and `@Model` macros expand and compile.
- `xcrun simctl list devices available`: confirms the destination.

## Test first
Use an in-memory `ModelConfiguration` so tests are isolated and fast.
```swift
@MainActor
final class StoreTests: XCTestCase {
    func testDeleteRemovesTask() throws {
        let c = try ModelContainer(for: TaskItem.self,
            configurations: ModelConfiguration(isStoredInMemoryOnly: true))
        let ctx = c.mainContext
        let t = TaskItem(title: "a"); ctx.insert(t)
        ctx.delete(t); try ctx.save()
        XCTAssertEqual(try ctx.fetchCount(FetchDescriptor<TaskItem>()), 0)
    }
}
```

## Do
- Annotate persisted classes with `@Model`; use `@Attribute(.unique)` for natural keys and `@Relationship(deleteRule:inverse:)` on relationships.
- Create one `ModelContainer` at app start and attach it with `.modelContainer(for:)` on the scene or root view.
- Read in views with `@Query(filter:sort:)` and write through `@Environment(\.modelContext)`.
- Use `FetchDescriptor` with `#Predicate` for fetches outside views, and set `fetchLimit` when you can.
- Use a `ModelActor` (`@ModelActor`) for background work; do not pass model objects across actors, pass `PersistentIdentifier`s.
- Version the schema with `VersionedSchema` and a `SchemaMigrationPlan` before changing stored properties.
- Call `try context.save()` explicitly at the points that must be durable.

## Avoid
- Sharing a `ModelContext` or model instances across threads or actors: not Sendable, corrupts state. Fetch again by identifier in the other context.
- Changing a `@Model` property type or name with no migration plan: the store fails to open or loses data. Add a versioned schema and a stage.
- Complex Swift expressions in `#Predicate` (custom functions, unsupported operators): fail to compile or at runtime. Keep predicates to supported comparisons, or filter after fetching.
- Doing fetches in `body` by hand: use `@Query` so views update.
- Assuming autosave covers app termination: save explicitly for critical writes.
- Using the real on-disk store in unit tests: leaks state. Use in-memory configurations.
- Mixing `NSManagedObject` and `@Model` types without a plan: they are different stacks. Choose per store.

## Review
- [ ] Schema changes ship with a migration stage and a test that opens the old store.
- [ ] Unique and delete rules express the invariants.
- [ ] No model objects cross actor or thread boundaries.
- [ ] Views read with `@Query`; background writes use a ModelActor.
- [ ] Tests use in-memory containers.
