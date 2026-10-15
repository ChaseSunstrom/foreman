---
name: aspnet-core
title: ASP.NET Core
area: dotnet
tags: [dotnet, csharp, web, api, mvc, middleware, kestrel]
detect: [dep:Microsoft.AspNetCore.App, dep:Microsoft.AspNetCore.Mvc.Testing, file:*.csproj, file:*.sln]
related: [minimal-apis, ef-core, xunit, signalr, dotnet-cli, nuget]
---
ASP.NET Core web apps and APIs: host builder, DI, middleware pipeline, controllers, options, integration tests.

## Verify
- `dotnet build -warnaserror`: compiles with nullable and analyzer warnings as errors.
- `dotnet test`: unit and in-process integration tests.
- `dotnet format --verify-no-changes`: formatting matches .editorconfig.
- `dotnet list package --vulnerable`: no known-vulnerable packages.

## Test first
Use `WebApplicationFactory<Program>` from `Microsoft.AspNetCore.Mvc.Testing` in a test project. Add `public partial class Program { }` to the web project if top-level statements hide it.
```csharp
public class ItemsTests(WebApplicationFactory<Program> factory)
    : IClassFixture<WebApplicationFactory<Program>>
{
    [Fact]
    public async Task Post_blank_name_returns_400()
    {
        var client = factory.CreateClient();
        var r = await client.PostAsJsonAsync("/items", new { name = "" });
        Assert.Equal(HttpStatusCode.BadRequest, r.StatusCode);
    }
}
```
Swap services with `WithWebHostBuilder(b => b.ConfigureTestServices(...))`.

## Do
- Register services by lifetime: scoped for per-request and DbContext, singleton only for thread-safe state, transient for cheap stateless.
- Bind config with `AddOptions<T>().BindConfiguration("Section").ValidateDataAnnotations().ValidateOnStart()`.
- Order middleware deliberately: exception handler, HTTPS redirection, routing, CORS, authentication, authorization, endpoints.
- Use `[ApiController]` for automatic 400 on model-state errors, and return `ProblemDetails` via `AddProblemDetails()`.
- Take `CancellationToken` in actions and pass it to every awaited call.
- Use `IHttpClientFactory` (typed clients) for outbound HTTP.
- Keep secrets in user-secrets or environment variables, not appsettings.json.

## Avoid
- `new HttpClient()` per request: socket exhaustion. Use `IHttpClientFactory`.
- `.Result` or `.Wait()` on tasks: thread-pool starvation and deadlocks. Make the call chain async.
- Injecting a scoped service into a singleton: captive dependency, caught only with scope validation in Development. Inject `IServiceScopeFactory` and create a scope.
- `app.UseAuthorization()` before `UseRouting()` or `UseAuthentication()`: policies silently never apply. Fix the order.
- Binding request bodies straight to EF entities: over-posting. Use request DTOs.
- `UseDeveloperExceptionPage` outside Development: leaks stack traces. Gate it by environment.
- `AllowAnyOrigin()` with `AllowCredentials()`: rejected by the framework and an unreviewed policy. List origins.

## Review
- [ ] Every endpoint has an explicit authorization stance (`[Authorize]`, `[AllowAnonymous]` or a fallback policy).
- [ ] No sync-over-async, and cancellation tokens flow through.
- [ ] DTOs in, DTOs out; no entities on the wire.
- [ ] Options are validated on start; no secrets in committed config.
- [ ] Integration test covers one failure path per endpoint.
