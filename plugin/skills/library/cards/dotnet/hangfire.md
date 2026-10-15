---
name: hangfire
title: Hangfire
area: dotnet
tags: [dotnet, csharp, background-jobs, scheduling, queues, dashboard]
detect: [dep:Hangfire, dep:Hangfire.Core, dep:Hangfire.AspNetCore, dep:Hangfire.SqlServer]
related: [aspnet-core, masstransit, serilog, xunit]
---
Hangfire: persistent background jobs, delayed and recurring, where job arguments are serialized and jobs must be idempotent.

## Verify
- `dotnet build -warnaserror`: job methods and expressions compile.
- `dotnet test --filter "FullyQualifiedName~Job"`: job classes tested directly, with no server.
- `grep -rnE "UseHangfireDashboard\(\)" --include=*.cs .`: a dashboard mounted with no authorization filter is a finding.

## Test first
Keep the job a plain class with injected dependencies, and test it without Hangfire. Test the enqueueing against `IBackgroundJobClient`.
```csharp
[Fact]
public async Task SendReceipt_is_idempotent()
{
    var mail = new FakeMailer();
    var job = new ReceiptJob(mail, new InMemoryOrders(sent: true));
    await job.Run(orderId: 7);
    Assert.Empty(mail.Sent);               // already sent: no duplicate
}

[Fact]
public void Checkout_enqueues_receipt()
{
    var client = new Mock<IBackgroundJobClient>();
    new Checkout(client.Object).Complete(7);
    client.Verify(c => c.Create(It.Is<Job>(j => j.Type == typeof(ReceiptJob)), It.IsAny<IState>()));
}
```

## Do
- Register with `services.AddHangfire(c => c.UseSqlServerStorage(cs))` and `services.AddHangfireServer()`.
- Enqueue with `BackgroundJob.Enqueue<ReceiptJob>(j => j.Run(orderId))`, passing ids and primitives only.
- Register recurring work with `RecurringJob.AddOrUpdate<T>("id", j => j.Run(), Cron.Daily)` using stable ids at startup.
- Make jobs idempotent, because retries (default 10 attempts) and at-least-once delivery replay them. Set `[AutomaticRetry(Attempts = n)]` deliberately.
- Protect the dashboard with `app.UseHangfireDashboard("/jobs", new DashboardOptions { Authorization = [ ... ] })` implementing `IDashboardAuthorizationFilter`.
- Separate queues with `[Queue("critical")]` and list them in `WorkerCount` and `Queues` server options.
- Accept a `CancellationToken` or `IJobCancellationToken` in long jobs.

## Avoid
- Passing entities or large objects as arguments: they are serialized as JSON and go stale. Pass ids and reload.
- Capturing `HttpContext` or request-scoped services in the lambda: they are gone when the job runs. Resolve inside the job.
- The default dashboard filter (local requests only) as protection in a deployed environment, or `Authorization = []`: use a real filter.
- Non-idempotent jobs under automatic retry: payments and emails duplicate. Use a dedupe key.
- Changing a job method signature or class name with jobs queued: deserialization fails. Add a new method and leave the old one.
- Using `Enqueue` inside a database transaction before commit: the job may run before the data exists. Enqueue after commit.

## Review
- [ ] Jobs take primitives, and are idempotent under retry.
- [ ] Dashboard authorization is explicit.
- [ ] Retry attempts and queues are set on purpose.
- [ ] Recurring job ids are stable and registered at startup.
- [ ] Jobs enqueued after the data commit.
