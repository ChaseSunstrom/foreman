---
name: polly
title: Polly
area: dotnet
tags: [dotnet, csharp, resilience, retry, circuit-breaker, timeout]
detect: [dep:Polly, dep:Polly.Core, dep:Microsoft.Extensions.Http.Resilience, dep:Polly.Extensions]
related: [aspnet-core, xunit, dotnet-aspire, serilog]
---
Polly v8 resilience pipelines: retry, timeout and circuit breaker composed once and attached to `HttpClient` or any async call.

## Verify
- `dotnet build -warnaserror`: pipeline code compiles on the v8 API (`ResiliencePipelineBuilder`).
- `dotnet test --filter "FullyQualifiedName~Resilience"`: tests using a fake `TimeProvider` pass quickly.
- `grep -rnE "Policy\.(Handle|Timeout)|WaitAndRetryAsync" --include=*.cs .`: finds the legacy v7 API that should be migrated.

## Test first
Inject `TimeProvider` so retries do not sleep in tests.
```csharp
[Fact]
public async Task Retries_transient_failures_then_succeeds()
{
    var calls = 0;
    var pipeline = new ResiliencePipelineBuilder()
        .AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 2, Delay = TimeSpan.Zero })
        .Build();

    var result = await pipeline.ExecuteAsync(async ct =>
    {
        if (++calls < 3) throw new HttpRequestException();
        return "ok";
    });

    Assert.Equal(3, calls);
    Assert.Equal("ok", result);
}
```

## Do
- For HTTP use `services.AddHttpClient("api").AddStandardResilienceHandler()`, then tune `Retry`, `CircuitBreaker` and `TotalRequestTimeout` through its options.
- For other calls register `services.AddResiliencePipeline("db", b => b.AddRetry(...).AddTimeout(...))` and resolve `ResiliencePipelineProvider<string>`.
- Order strategies outermost to innermost: total timeout, retry, circuit breaker, attempt timeout.
- Set `BackoffType = DelayBackoffType.Exponential` with `UseJitter = true` on retries.
- Use `ShouldHandle` to retry only transient errors (5xx, 408, `HttpRequestException`, timeouts).
- Pass `CancellationToken` into the callback, and let the pipeline's own token cancel the work.
- Retry only idempotent operations, or add an idempotency key.

## Avoid
- The v7 API (`Policy.Handle<>().WaitAndRetryAsync`, `PolicyRegistry`) in new code: use `ResiliencePipeline`.
- Retrying everything including 4xx: it hammers the server and masks bugs. Narrow `ShouldHandle`.
- Retries without jitter: synchronized clients cause retry storms.
- Retry inside a circuit breaker with the wrong nesting: failures count once per attempt. Keep the breaker inner so it sees each attempt.
- `Thread.Sleep` or `Task.Delay` loops hand-rolled alongside Polly: use the strategy.
- Building a pipeline per call: build once and reuse, since pipelines are thread safe.

## Review
- [ ] Only idempotent calls are retried, and `ShouldHandle` is explicit.
- [ ] Backoff is exponential with jitter, with a capped attempt count.
- [ ] A total timeout bounds the whole operation including retries.
- [ ] Pipelines are registered once and resolved, and nothing uses the v7 API.
- [ ] Tests prove both the retry-then-succeed path and the give-up path.
