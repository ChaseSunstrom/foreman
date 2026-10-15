---
name: dotnet-aspire
title: .NET Aspire
area: dotnet
tags: [dotnet, aspire, orchestration, service-defaults, telemetry, apphost]
detect: [dep:Aspire.Hosting.AppHost, dep:Aspire.Hosting.Testing, dep:Microsoft.Extensions.ServiceDiscovery, file:*.AppHost.csproj, file:*.ServiceDefaults.csproj]
related: [aspnet-core, serilog, polly, orleans, xunit]
---
.NET Aspire: an AppHost that models services and resources in code, plus ServiceDefaults for telemetry, health and discovery, tested through the real host.

## Verify
- `dotnet build -warnaserror`: AppHost and every referenced project compile.
- `dotnet test --filter "FullyQualifiedName~Integration"`: tests booting the AppHost with `Aspire.Hosting.Testing` pass (needs a container runtime for container resources).
- `dotnet run --project *.AppHost`: starts the app model and the dashboard, where each resource should reach Running.
- `grep -rn "AddServiceDefaults" --include=Program.cs .`: every service calls the defaults.

## Test first
Boot the whole app model and hit a health endpoint.
```csharp
[Fact]
public async Task Api_is_healthy_with_database()
{
    var builder = await DistributedApplicationTestingBuilder
        .CreateAsync<Projects.Shop_AppHost>();
    await using var app = await builder.BuildAsync();
    await app.StartAsync();

    await app.ResourceNotifications
        .WaitForResourceHealthyAsync("api").WaitAsync(TimeSpan.FromMinutes(2));
    var http = app.CreateHttpClient("api");
    Assert.Equal(HttpStatusCode.OK, (await http.GetAsync("/health")).StatusCode);
}
```

## Do
- Declare resources in the AppHost: `var db = builder.AddPostgres("pg").AddDatabase("shop");` and reference them with `.WithReference(db)`.
- Order startup with `.WaitFor(db)` so services do not race their dependencies.
- Call `builder.AddServiceDefaults()` and `app.MapDefaultEndpoints()` in each service for OpenTelemetry, health checks, discovery and resilience.
- Consume connection strings by resource name: `builder.AddNpgsqlDbContext<AppDb>("shop")`, with a client integration package per resource.
- Resolve services by name over discovery: `new Uri("https+http://api")`.
- Keep secrets in parameters (`builder.AddParameter("key", secret: true)`) backed by user secrets locally.
- Add `.WithDataVolume()` for stateful containers that should survive restarts.
- Keep health endpoints dev-only unless protected, as the template does.

## Avoid
- Hard-coded ports and connection strings in services: they bypass the orchestration. Use references and names.
- Skipping `WaitFor`: intermittent startup failures that vanish on retry. Add the dependency order.
- Exposing `MapDefaultEndpoints` health and alive endpoints publicly without thought: restrict them in production.
- Treating the AppHost as the production deploy: it is the app model, and publishing to a target is a separate step with its own manifest or tool.
- Mocking resources in integration tests: boot the real model with the testing builder.
- Mixing Aspire package versions across the AppHost and client integrations: keep them aligned.

## Review
- [ ] Every service calls `AddServiceDefaults`, and exposes health.
- [ ] Dependencies use `WithReference` and `WaitFor`, with no literal ports.
- [ ] Secrets are parameters, not source literals.
- [ ] An integration test starts the AppHost and reaches a healthy state.
- [ ] Aspire package versions are consistent across projects.
