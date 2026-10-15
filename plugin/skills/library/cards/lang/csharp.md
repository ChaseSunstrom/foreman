---
name: csharp
title: C#
area: lang
tags: [csharp, dotnet, nuget, xunit, nullable, async]
detect: [ext:.cs, file:*.csproj, file:*.sln, file:global.json, file:Directory.Build.props]
related: [fsharp, aspnet-core, xunit]
---
C# baseline: the dotnet CLI, nullable reference types on, analyzers as errors, xUnit tests, and disciplined async.

## Verify
- `dotnet build -warnaserror`: compile with warnings failing the build.
- `dotnet test`: all test projects.
- `dotnet test --filter "FullyQualifiedName~PortParser"`: a subset while iterating.
- `dotnet format --verify-no-changes`: formatting and analyzer style.
- `dotnet list package --vulnerable`: known-vulnerable NuGet packages.

## Test first
xUnit project `*.Tests.csproj` referencing the project under test; class per unit, `[Fact]` and `[Theory]`.
```csharp
using Xunit;

public class PortParserTests
{
    [Theory]
    [InlineData("")]
    [InlineData("70000")]
    public void Rejects_invalid(string raw) =>
        Assert.Throws<ArgumentException>(() => PortParser.Parse(raw));
}
```

## Do
- Enable `<Nullable>enable</Nullable>` and `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` (or via Directory.Build.props); add `<AnalysisMode>`/analyzers.
- Use records for immutable data, `required` and `init` members, and pattern matching with switch expressions.
- Make I/O `async` all the way down, take a `CancellationToken`, and name methods `...Async`.
- Use `using` declarations for `IDisposable` and `await using` for `IAsyncDisposable`.
- Use `IHttpClientFactory` (or a single shared `HttpClient`), and `ILogger<T>` with message templates.
- Use `TimeProvider` (or an injected clock) instead of `DateTime.Now` in testable code.
- Manage versions centrally (`Directory.Packages.props`) and pin the SDK in `global.json`.

## Avoid
- `.Result`, `.Wait()` and `.GetAwaiter().GetResult()` on tasks: deadlocks and thread starvation. `await` instead.
- `async void` outside event handlers: unobserved exceptions crash the process. Return `Task`.
- `new HttpClient()` per request: socket exhaustion. Use the factory.
- Interpolated strings in log calls (`$"saved {id}"`): defeats structured logging. Use `"saved {Id}", id`.
- `catch (Exception) { }` and `throw ex;`: lost failures and reset stack traces. Log, and `throw;` to rethrow.
- Building SQL by concatenation: injection. Use parameters (`SqlParameter`, EF `FromSql` interpolation).
- `DateTime.Now` for stored timestamps: local-time bugs. Use `DateTimeOffset.UtcNow`.
- Suppressing nullable warnings with `!` as a habit: runtime NRE. Handle null or fix the signature.

## Review
- [ ] No sync-over-async or `async void`.
- [ ] Nullable warnings resolved, not suppressed.
- [ ] Disposables disposed; `HttpClient` shared via factory.
- [ ] Cancellation tokens flow through async calls.
- [ ] `dotnet test` and `dotnet format --verify-no-changes` pass.
