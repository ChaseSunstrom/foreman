---
name: core-data
title: Core Data
area: mobile
tags: [swift, core-data, persistence, ios, database, apple]
detect: [file:*.xcdatamodeld, file:*.xcdatamodel, file:*.xcmappingmodel]
related: [swiftdata, uikit, swiftui, swift-concurrency, xctest]
---
Core Data: NSPersistentContainer, managed object contexts, fetch requests, background writes and lightweight migration.

## Verify
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: tests with an in-memory store pass.
- `xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build`: the model and generated classes compile.
- `xcrun simctl list devices available`: confirms the destination.
- Launch argument `-com.apple.CoreData.ConcurrencyDebug 1` in the scheme: traps cross-thread access to managed objects.

## Test first
Build the stack with an in-memory store description.
```swift
func makeContainer() -> NSPersistentContainer {
    let c = NSPersistentContainer(name: "Model")
    let d = NSPersistentStoreDescription(); d.type = NSInMemoryStoreType
    c.persistentStoreDescriptions = [d]
    c.loadPersistentStores { _, e in precondition(e == nil) }
    return c
}

func testFetchReturnsOnlyOpen() throws {
    let ctx = makeContainer().viewContext
    let a = Task(context: ctx); a.title = "a"; a.done = false
    let b = Task(context: ctx); b.title = "b"; b.done = true
    try ctx.save()
    let r: NSFetchRequest<Task> = Task.fetchRequest()
    r.predicate = NSPredicate(format: "done == NO")
    XCTAssertEqual(try ctx.fetch(r).count, 1)
}
```

## Do
- Keep one `NSPersistentContainer`; use `viewContext` on the main queue for UI and `newBackgroundContext()` or `performBackgroundTask` for writes.
- Touch managed objects only inside `perform { }` / `performAndWait` of their own context, or via `async` `perform`.
- Set `viewContext.automaticallyMergesChangesFromParent = true` and a merge policy (`NSMergeByPropertyObjectTrumpMergePolicy`) deliberately.
- Pass `NSManagedObjectID`s between contexts, not objects.
- Use `NSFetchedResultsController` (UIKit) or `@FetchRequest` (SwiftUI) to drive lists; set `fetchBatchSize`.
- Add a new model version for every schema change (Editor, Add Model Version) and rely on lightweight migration (`shouldMigrateStoreAutomatically`, `shouldInferMappingModelAutomatically`).
- Index attributes used in predicates and sorts.

## Avoid
- Using a managed object on a different thread than its context: random crashes. Enable ConcurrencyDebug and use `perform`.
- Saving on the main context for bulk imports: freezes the UI. Use a background context with batches (`NSBatchInsertRequest`).
- Editing the current model version after shipping: store fails to open. Add a version.
- `loadPersistentStores` errors ignored: the app runs with no store. Handle the error (and `fatalError` only during development).
- Fetching everything then filtering in Swift: use an `NSPredicate` and `fetchLimit`.
- Stringly keys in `NSPredicate(format:)` with user input concatenated: use `%@` arguments.
- Real SQLite store in unit tests: shared state. Use an in-memory type.

## Review
- [ ] Each context is used only on its own queue; IDs cross boundaries.
- [ ] Schema changes are new model versions with a migration test.
- [ ] Bulk work is off the main queue and batched.
- [ ] Predicates are parameterized, and sorted or filtered fields are indexed.
- [ ] Store-load failure is handled.
