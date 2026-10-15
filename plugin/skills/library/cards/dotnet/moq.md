---
name: moq
title: Moq
area: dotnet
tags: [dotnet, csharp, mocking, testing, unit-tests, verify]
detect: [dep:Moq]
related: [xunit, nunit, mediatr, bunit]
---
Moq: mock interfaces at architectural boundaries, assert on outcomes first and on interactions only where the interaction is the behavior.

## Verify
- `dotnet test`: the suite passes.
- `dotnet test --filter "FullyQualifiedName~Services"`: the unit tests for the mocked layer pass in isolation.
- `grep -rnE "MockBehavior\.Loose|Verify\(\)" --include=*.cs .`: finds blanket verification and loose mocks for review.

## Test first
Stub inputs, run the unit, assert the result, and verify only the outward effect.
```csharp
[Fact]
public async Task Charge_failure_does_not_mark_order_paid()
{
    var gateway = new Mock<IPaymentGateway>(MockBehavior.Strict);
    gateway.Setup(g => g.ChargeAsync(42, 10m, It.IsAny<CancellationToken>()))
           .ThrowsAsync(new PaymentDeclined());
    var orders = new FakeOrders(42);

    await Assert.ThrowsAsync<PaymentDeclined>(
        () => new Checkout(gateway.Object, orders).PayAsync(42, 10m));

    Assert.False(orders.Get(42).Paid);
}
```

## Do
- Mock interfaces or virtual members only, at boundaries (clock, gateway, repository), and use hand-written fakes for simple collaborators such as in-memory stores.
- Use `ReturnsAsync` and `ThrowsAsync` for `Task` members, and `SetupSequence` for call-by-call behavior.
- Use `MockBehavior.Strict` where an unexpected call should fail the test.
- Match arguments with `It.Is<T>(x => ...)` for the property that matters, not `It.IsAny` everywhere.
- Verify interactions that are the point of the code: `Verify(x => x.SendAsync(...), Times.Once)`.
- Capture arguments with `Callback<T>` when asserting on a complex object.
- Use `mock.SetupGet` or `SetupProperty` for properties, and `mock.Protected()` only with `using Moq.Protected` for protected members.
- Inject `TimeProvider` or a clock interface instead of mocking static time.

## Avoid
- Mocking types you do not own, such as `HttpClient` or `DbContext`: use `HttpMessageHandler` stubs or an in-memory or real database.
- Verifying every call (`VerifyAll` after every test): tests break on refactors. Assert behavior.
- Setups with `It.IsAny` for everything: bugs pass silently. Match the relevant arguments.
- Setting up async methods with `.Returns(value)` where a `Task` is expected: it may return null. Use `ReturnsAsync`.
- Mocking extension methods or static members: Moq cannot intercept them. Wrap them behind an interface.
- Mocks with deep chains (`Setup(x => x.A.B.C)`) that hide a design smell: introduce a smaller interface.
- Leaving the loose-mock default unexamined, so that missing setups return defaults and hide errors: choose Strict where it matters.

## Review
- [ ] Only boundaries are mocked, and not types you do not own.
- [ ] Each test asserts an outcome, with verification limited to meaningful calls.
- [ ] Async setups use `ReturnsAsync` or `ThrowsAsync`.
- [ ] Argument matchers constrain the values that matter.
- [ ] Time and randomness come through injected abstractions.
