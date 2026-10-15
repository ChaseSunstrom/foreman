---
name: swift-concurrency
title: Swift Concurrency
area: mobile
tags: [swift, concurrency, async-await, actors, sendable, tasks]
detect: [file:Package.swift, file:*.xcodeproj, ext:.swift]
related: [swiftui, uikit, xctest, swift-package-manager, swiftdata]
---
Swift concurrency: async/await, structured tasks, actors, `@MainActor` and Sendable checking.

## Verify
- `swift build -Xswiftc -strict-concurrency=complete`: compiles with complete Sendable and isolation diagnostics (SwiftPM projects).
- `swift test`: async tests run.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'`: same for Xcode projects (set Strict Concurrency Checking to Complete in build settings).
- `swift build -c release`: optimized build still passes isolation checks.

## Test first
Mark async tests `async` (XCTest awaits them) and assert on the result.
```swift
func testLoadReturnsItemsAndNeverBlocks() async throws {
    let repo = Repository(client: FakeClient(items: [1, 2, 3]))
    let items = try await repo.load()
    XCTAssertEqual(items, [1, 2, 3])
}

func testCancellationStopsLoad() async {
    let task = Task { try await Repository(client: SlowClient()).load() }
    task.cancel()
    do { _ = try await task.value; XCTFail("expected cancel") }
    catch is CancellationError {} catch { XCTFail("\(error)") }
}
```

## Do
- Isolate UI-facing types with `@MainActor`; keep heavy work in plain async functions or actors.
- Protect shared mutable state with an `actor` and keep its methods short; reason about reentrancy at each `await`.
- Prefer structured concurrency: `async let` and `withTaskGroup` / `withThrowingTaskGroup`, so children cancel with the parent.
- Make values crossing isolation `Sendable`: value types, immutable final classes, or actors.
- Check cancellation in loops with `try Task.checkCancellation()` and use cancellable APIs (`Task.sleep(for:)`).
- Bridge callbacks with `withCheckedThrowingContinuation` and resume exactly once.
- Use `AsyncStream` for event sequences; call `continuation.finish()` and set `onTermination`.

## Avoid
- `Task { }` fire-and-forget inside every function: errors vanish and nothing cancels. Await it, or store and cancel the handle.
- `Task.detached` by default: drops actor context and priority. Use plain `Task` unless you need to leave the actor.
- Assuming actor state is unchanged after an `await`: reentrancy lets other calls interleave. Re-check after suspension.
- `@unchecked Sendable` to silence warnings: hides real races. Make the type properly Sendable or isolate it.
- `DispatchSemaphore` or `.wait()` to block on async work: deadlocks the cooperative pool. Make the caller async.
- Calling `continuation.resume` twice or never: crash or a hang. Use checked continuations and cover every path.
- `Task.sleep(nanoseconds:)` for timeouts in new code: use `Task.sleep(for:)` and race with a task group.

## Review
- [ ] Every shared mutable value is actor-isolated or Sendable by construction.
- [ ] Long work checks cancellation; no orphan unstructured tasks.
- [ ] No blocking calls inside async contexts.
- [ ] Continuations resume exactly once on all paths.
- [ ] Strict concurrency checking is on and warnings are clean.
