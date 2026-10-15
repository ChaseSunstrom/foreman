---
name: mediatr
title: MediatR
area: dotnet
tags: [dotnet, csharp, cqrs, mediator, handlers, pipeline]
detect: [dep:MediatR]
related: [fluentvalidation, aspnet-core, xunit, ef-core, minimal-apis]
---
MediatR: in-process requests, handlers and pipeline behaviors that keep endpoints thin and cross-cutting concerns in one place.

## Verify
- `dotnet build -warnaserror`: handlers and requests compile, with no nullable or unused warnings.
- `dotnet test --filter "FullyQualifiedName~Handler"`: handler tests pass without a web host.
- `dotnet test --filter "FullyQualifiedName~Registration"`: the DI-resolution test (below) proves every request has exactly one handler.

## Test first
xUnit project beside the app. Call the handler directly, and add one test that resolves every handler from the container.
```csharp
[Fact]
public async Task CreateOrder_rejects_empty_cart()
{
    var handler = new CreateOrderHandler(new InMemoryOrders());
    var act = () => handler.Handle(new CreateOrder(Guid.NewGuid(), []), CancellationToken.None);
    await Assert.ThrowsAsync<DomainException>(act);
}

[Fact]
public void Every_request_has_a_handler()
{
    var sp = TestHost.Services;                       // real AddMediatR registration
    Assert.NotNull(sp.GetRequiredService<IRequestHandler<CreateOrder, OrderId>>());
}
```

## Do
- Register with `services.AddMediatR(cfg => cfg.RegisterServicesFromAssemblyContaining<Program>())`. Current versions use this form, not the old `AddMediatR(typeof(...))`.
- Model commands (change state) and queries (read only) as separate records implementing `IRequest<T>`.
- Put cross-cutting code in `IPipelineBehavior<TRequest,TResponse>` (validation, logging, transaction) and set order by registration order with `cfg.AddOpenBehavior(typeof(ValidationBehavior<,>))`.
- Pass the `CancellationToken` through to every EF and HTTP call.
- Use `INotification` for fan-out side effects. Keep each handler idempotent, since one failure stops the later ones by default.
- Keep one handler per file next to its request, grouped by feature folder.

## Avoid
- Handlers calling `mediator.Send` for other handlers: hidden coupling and nested pipelines. Extract a shared service instead.
- Returning `IQueryable` or tracked EF entities from queries: they leak the context. Project to a DTO inside the handler.
- Validation inside every handler: it gets forgotten. Use a validation behavior.
- A missing `AddOpenBehavior` registration for generic behaviors: the behavior silently never runs. Assert it in a test.
- Using notifications for work that must succeed: the publisher has no retry. Use an outbox or a queue.
- `async void` or fire-and-forget `Task.Run` in handlers: exceptions vanish. Await everything.

## Review
- [ ] Every request has exactly one handler, and the registration test passes.
- [ ] Behaviors are registered in the intended order (logging, validation, transaction).
- [ ] No handler injects `IMediator` to call another request.
- [ ] Queries return DTOs, not entities, and do not mutate state.
- [ ] Cancellation tokens are forwarded to all I/O.

## Notes
- Recent major versions of MediatR require a license key for commercial use. Check the package license before upgrading.
