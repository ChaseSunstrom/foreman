---
name: xunit
title: xUnit
area: dotnet
tags: [dotnet, csharp, testing, xunit, tdd, unit-tests]
detect: [dep:xunit, dep:xunit.v3, dep:xunit.runner.visualstudio, dep:Microsoft.NET.Test.Sdk]
related: [nunit, aspnet-core, dotnet-cli, ef-core]
---
xUnit.net tests: facts, theories, per-test instances, class and collection fixtures.

## Verify
- `dotnet test`: runs every test project in the solution.
- `dotnet test --filter "FullyQualifiedName~OrderTests"`: one class while iterating.
- `dotnet test --filter "DisplayName~blank"`: by display name substring.
- `dotnet test --collect:"XPlat Code Coverage"`: coverage via the coverlet collector, when the package is referenced.

## Test first
A test project references `Microsoft.NET.Test.Sdk`, `xunit` and `xunit.runner.visualstudio`, and the project under test. Name tests for behavior.
```csharp
public class PriceTests
{
    [Theory]
    [InlineData(0, 0)]
    [InlineData(100, 90)]
    public void Discount_applies_ten_percent(int price, int expected)
        => Assert.Equal(expected, Pricing.Discount(price));

    [Fact]
    public void Negative_price_throws()
        => Assert.Throws<ArgumentOutOfRangeException>(() => Pricing.Discount(-1));
}
```

## Do
- Rely on a new class instance per test: use the constructor for setup and `IDisposable` / `IAsyncLifetime` for teardown.
- Share expensive setup with `IClassFixture<T>` (one class) or `[Collection]` plus `ICollectionFixture<T>` (many classes).
- Use `[Theory]` with `[InlineData]`, `[MemberData]` or `[ClassData]` for table cases.
- Use `Assert.Throws<T>` / `Assert.ThrowsAsync<T>` and assert the exception, not just that something threw.
- Return `Task` from async tests and await everything.
- Inject `ITestOutputHelper` for diagnostics instead of `Console.WriteLine`.
- Fake time and IO behind interfaces (`TimeProvider` exists in the BCL).

## Avoid
- `async void` tests: failures are lost or crash the runner. Return `Task`.
- Shared static mutable state: xUnit runs classes in different collections in parallel, so tests become flaky. Use fixtures or one `[Collection]`.
- Expecting `[SetUp]` / `[TearDown]`: those are NUnit. Use constructor and `Dispose`.
- `Assert.True(a == b)`: poor failure message. Use `Assert.Equal(expected, actual)` (expected first).
- `Assert.Throws` around an async lambda: use `ThrowsAsync` and await it.
- Disabling a test with `Skip` and no reason or ticket: say why, and record it.
- `Task.Delay` to wait for effects: flaky. Await a signal or poll with a timeout.

## Review
- [ ] Each new behavior has a test that failed before the change.
- [ ] No sleeps, no shared mutable statics, no order dependence.
- [ ] Theories cover boundaries (empty, zero, null, max).
- [ ] Fixtures dispose their resources.
- [ ] Assertions use expected-then-actual and check specific values.
