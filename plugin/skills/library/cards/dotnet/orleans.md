---
name: orleans
title: Orleans
area: dotnet
tags: [dotnet, csharp, actors, grains, distributed, virtual-actors]
detect: [dep:Microsoft.Orleans.Server, dep:Microsoft.Orleans.Sdk, dep:Microsoft.Orleans.Client, dep:Microsoft.Orleans.TestingHost]
related: [dotnet-aspire, aspnet-core, xunit, masstransit]
---
Orleans: virtual-actor grains with single-threaded state, tested in a real in-process silo cluster.

## Verify
- `dotnet build -warnaserror`: grain interfaces and generated serializers compile.
- `dotnet test --filter "FullyQualifiedName~Grain"`: tests against a `TestCluster` pass.
- `grep -rn "\[GenerateSerializer\]" --include=*.cs .`: lists the types that cross grain boundaries, which should include every state and argument type.

## Test first
Use `Microsoft.Orleans.TestingHost` and call grains through the cluster client.
```csharp
public class ClusterFixture : IDisposable
{
    public TestCluster Cluster { get; } = new TestClusterBuilder().Build();
    public ClusterFixture() => Cluster.Deploy();
    public void Dispose() => Cluster.StopAllSilos();
}

public class CounterTests(ClusterFixture f) : IClassFixture<ClusterFixture>
{
    [Fact]
    public async Task Increment_persists_across_calls()
    {
        var g = f.Cluster.GrainFactory.GetGrain<ICounterGrain>("a");
        await g.Increment();
        Assert.Equal(2, await g.Increment());
    }
}
```

## Do
- Host with `builder.UseOrleans(silo => silo.UseLocalhostClustering())` in development, and a real membership provider in production.
- Design one grain per entity with a stable key (`GetGrain<IUserGrain>(userId)`), and keep the interface small and async.
- Mark all state and message types `[GenerateSerializer]` with `[Id(n)]` on members, and never reuse or renumber ids.
- Persist with `IPersistentState<T>` through `[PersistentState("name", "store")]`, and call `WriteStateAsync` explicitly after changes that must survive.
- Use reminders (`RegisterOrUpdateReminder`) for durable schedules and timers for in-memory ticks only.
- Use `[Reentrant]` or `[AlwaysInterleave]` only on grains that are proven safe against interleaving.
- Add `IGrainCallFilter` for logging and auth, and set grain collection age for memory.

## Avoid
- Blocking calls (`.Result`, `.Wait()`, `Thread.Sleep`) inside a grain: they stall its turn and can deadlock the scheduler. Use `await`.
- Awaiting non-grain tasks that schedule on other threads, then touching grain state: use grain-scheduled continuations (plain `await`) only.
- Huge grains such as a single global grain: it is a bottleneck. Shard by key.
- Missing serializer attributes or reused `[Id]` numbers: silent state corruption across upgrades. Keep ids append-only.
- Unbounded call chains between grains in a loop: they deadlock on cycles. Break cycles with one-way calls or reentrancy.
- Assuming a grain stays in memory: it deactivates when idle. Persist state and recreate timers in `OnActivateAsync`.

## Review
- [ ] Every cross-grain type has `[GenerateSerializer]` and stable `[Id]` values.
- [ ] State writes are explicit, and failures are handled.
- [ ] No sync-over-async calls inside grains.
- [ ] Reminders back any schedule that must survive deactivation.
- [ ] Tests run on `TestCluster`, including a deactivation and reactivation case.
