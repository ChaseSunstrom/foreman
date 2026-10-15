---
name: masstransit
title: MassTransit
area: dotnet
tags: [dotnet, csharp, messaging, rabbitmq, consumers, sagas, outbox]
detect: [dep:MassTransit, dep:MassTransit.RabbitMQ, dep:MassTransit.Azure.ServiceBus.Core, dep:MassTransit.EntityFrameworkCore]
related: [hangfire, ef-core, aspnet-core, xunit, polly]
---
MassTransit: message-bus consumers, sagas and the transactional outbox, tested in memory through its harness.

## Verify
- `dotnet build -warnaserror`: consumers and contracts compile.
- `dotnet test --filter "FullyQualifiedName~Consumer"`: harness tests pass with no broker.
- `grep -rn "AddMassTransit" --include=*.cs .`: confirms registration sits in one place with consumers added by type.

## Test first
Use the in-memory test harness and assert consumption and publishes.
```csharp
[Fact]
public async Task Order_submitted_publishes_accepted()
{
    await using var provider = new ServiceCollection()
        .AddMassTransitTestHarness(x => x.AddConsumer<SubmitOrderConsumer>())
        .BuildServiceProvider(true);
    var harness = provider.GetRequiredService<ITestHarness>();
    await harness.Start();

    await harness.Bus.Publish(new SubmitOrder { OrderId = Guid.NewGuid() });

    Assert.True(await harness.Consumed.Any<SubmitOrder>());
    Assert.True(await harness.Published.Any<OrderAccepted>());
}
```

## Do
- Define contracts as records or interfaces in a shared assembly, and only add fields, never rename or remove.
- Register with `services.AddMassTransit(x => { x.AddConsumers(typeof(Program).Assembly); x.UsingRabbitMq((ctx, cfg) => { cfg.Host(...); cfg.ConfigureEndpoints(ctx); }); })`.
- Use `Publish` for events (many subscribers) and `Send` for commands (one endpoint).
- Enable the EF outbox so database writes and publishes commit together: `x.AddEntityFrameworkOutbox<AppDb>(o => { o.UsePostgres(); o.UseBusOutbox(); })`.
- Configure retry and redelivery in the endpoint: `cfg.UseMessageRetry(r => r.Exponential(5, ...))`. Add `UseDelayedRedelivery` for slow dependencies.
- Make consumers idempotent. Delivery is at least once.
- Carry a correlation id on every message, and use the saga `CorrelateById` for state machines.
- Inspect `_error` and `_skipped` queues in operations and decide on a replay path.

## Avoid
- Publishing inside a handler and then saving to the database without an outbox: a crash between them loses or duplicates the event. Use the bus outbox.
- Changing a message namespace or type name after deploy: the message-type URN no longer matches the consumers. Keep the original type or add a new contract.
- Long synchronous work in consumers with the default prefetch: use `PrefetchCount` and `ConcurrentMessageLimit` to match the load.
- Request/response with `GetResponse` as a general RPC: it couples availability. Use events where the caller can wait.
- Starting the bus in tests with a real broker: use the test harness.
- Swallowing exceptions in consumers: the message is acked and lost. Let it throw so retry and error queues apply.

## Review
- [ ] Contracts are additive-only, and live in a shared assembly.
- [ ] Outbox is enabled where consumers write to the database.
- [ ] Retry, redelivery and concurrency limits are explicit.
- [ ] Consumers are idempotent, and failures reach an error queue.
- [ ] Harness tests exist per consumer and saga transition.
