---
name: csharp-async
title: C# async and await
area: idioms
tags: [csharp, dotnet, async, await, tasks, cancellation]
detect: [file:*.csproj, file:*.sln]
related: [csharp, dotnet, xunit]
---
C# async: Task-returning methods all the way down, cancellation tokens everywhere, no blocking on tasks.

## Verify
- `dotnet build -warnaserror`: compiles, with warnings such as CS4014 (unawaited call) as errors.
- `dotnet test`: runs the test projects.
- `dotnet format --verify-no-changes`: formatting is clean.

## Test first
xUnit with async tests and a cancellation token.
```csharp
using Xunit;

public class FetcherTests
{
    [Fact]
    public async Task FetchAsync_throws_when_cancelled()
    {
        using var cts = new CancellationTokenSource();
        cts.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(
            () => new Fetcher().FetchAsync("x", cts.Token));
    }
}
```

## Do
- Return `Task` or `Task<T>` and suffix names with `Async`. Make test methods `async Task`.
- Take a `CancellationToken` as the last parameter and pass it to every awaited call.
- Run independent work with `Task.WhenAll`, and await the result.
- Use `await using` and `IAsyncDisposable` for async cleanup.
- Use `ConfigureAwait(false)` in library code with no UI or request context needs.
- Use `ValueTask` only for hot paths that often complete synchronously, and await it exactly once.
- Use `IAsyncEnumerable<T>` with `await foreach` for streams.
- Use `Task.Run` to push CPU-bound work off a UI thread, not to fake async I/O.

## Avoid
- `.Result`, `.Wait()` and `.GetAwaiter().GetResult()`: they can deadlock and wrap exceptions. Make the caller async.
- `async void`: exceptions crash the process and cannot be awaited. Use `async Task`, except for event handlers.
- Fire-and-forget calls with no await: failures are lost and warning CS4014 appears. Await, or store and observe the task.
- Wrapping a sync method in `Task.Run` in an ASP.NET handler: it just burns another thread. Call it directly or make it truly async.
- Awaiting in a loop for independent calls: serial. Collect tasks and `Task.WhenAll`.
- Swallowing `OperationCanceledException` as an error: treat it as normal cancellation.
- `lock` around an await: not allowed, and holding locks across awaits is a design smell. Use `SemaphoreSlim.WaitAsync`.

## Review
- [ ] No blocking waits on tasks in async paths.
- [ ] Cancellation tokens flow through every layer.
- [ ] No `async void` outside event handlers.
- [ ] Every started task is awaited or deliberately observed.
- [ ] Tests cover cancellation and a faulted task.
