---
name: nunit
title: NUnit
area: dotnet
tags: [dotnet, csharp, testing, nunit, tdd, unit-tests]
detect: [dep:NUnit, dep:NUnit3TestAdapter, dep:NUnit.Analyzers, dep:Microsoft.NET.Test.Sdk]
related: [xunit, aspnet-core, dotnet-cli, ef-core]
---
NUnit tests: fixtures, SetUp/TearDown, TestCase tables, constraint-model assertions.

## Verify
- `dotnet test`: runs all test projects via NUnit3TestAdapter.
- `dotnet test --filter "FullyQualifiedName~OrderTests"`: one fixture while iterating.
- `dotnet test --filter "TestCategory=Fast"`: tests tagged `[Category("Fast")]`.
- `dotnet build -warnaserror`: NUnit.Analyzers catches misuse of assertions at build time.

## Test first
Reference `NUnit`, `NUnit3TestAdapter` and `Microsoft.NET.Test.Sdk`. Tests go in a separate `*.Tests` project.
```csharp
[TestFixture]
public class PriceTests
{
    [TestCase(0, 0)]
    [TestCase(100, 90)]
    public void Discount_applies_ten_percent(int price, int expected)
        => Assert.That(Pricing.Discount(price), Is.EqualTo(expected));

    [Test]
    public void Negative_price_throws()
        => Assert.That(() => Pricing.Discount(-1), Throws.TypeOf<ArgumentOutOfRangeException>());
}
```

## Do
- Use the constraint model: `Assert.That(actual, Is.EqualTo(expected))`.
- Use `[SetUp]` / `[TearDown]` per test, `[OneTimeSetUp]` per fixture. Keep one-time state read-only.
- Use `[TestCase]`, `[TestCaseSource]` or `[Values]` / `[Range]` for tables.
- Use `Assert.Multiple(() => { ... })` to report several assertions in one test.
- Use `Assert.ThatAsync` or `Assert.ThrowsAsync` for async code, and return `Task` from async tests.
- Add `[Parallelizable]` only to fixtures that share no state.
- Tag slow tests with `[Category]` so they can be filtered.

## Avoid
- Classic asserts (`Assert.AreEqual`): legacy API, removed from newer NUnit majors. Use `Assert.That`.
- `async void` tests: NUnit rejects or loses failures. Return `Task`.
- Mutable fields set in `[OneTimeSetUp]` and changed by tests: order-dependent failures. Reset in `[SetUp]`.
- Argument order swapped in `Is.EqualTo`: the message reads wrong. Actual goes in `That`, expected in the constraint.
- Expecting a fresh fixture instance per test: NUnit reuses one instance per fixture by default. Use `[FixtureLifeCycle(LifeCycle.InstancePerTestCase)]` or reset state in `SetUp`.
- `[Ignore]` with no reason: add a reason string.
- Sleeping to wait for async effects: flaky. Await or use `Is.EqualTo(...).After(...)` polling sparingly.

## Review
- [ ] New behavior has a test that failed first.
- [ ] All asserts use the constraint model.
- [ ] No state leaks between tests; `[Parallelizable]` only where safe.
- [ ] Async tests return Task and await everything.
- [ ] Ignored tests carry a reason.
