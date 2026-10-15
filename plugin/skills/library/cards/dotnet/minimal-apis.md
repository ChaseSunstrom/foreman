---
name: minimal-apis
title: ASP.NET Core Minimal APIs
area: dotnet
tags: [dotnet, csharp, api, minimal, endpoints, openapi]
detect: [dep:Microsoft.AspNetCore.OpenApi, dep:Microsoft.AspNetCore.Mvc.Testing, file:*.csproj]
related: [aspnet-core, ef-core, xunit, dotnet-cli]
---
Minimal APIs: lambda endpoints with MapGet/MapPost, route groups, endpoint filters, TypedResults.

## Verify
- `dotnet build -warnaserror`: compiles clean.
- `dotnet test`: endpoint tests through the in-process test server.
- `dotnet format --verify-no-changes`: style.
- `dotnet publish -c Release --no-restore`: publish succeeds (trimming or AOT issues surface here when enabled).

## Test first
Call the endpoint through `WebApplicationFactory<Program>`; make `Program` visible with `public partial class Program { }`.
```csharp
[Fact]
public async Task Get_missing_item_is_404()
{
    await using var app = new WebApplicationFactory<Program>();
    var r = await app.CreateClient().GetAsync("/items/999");
    Assert.Equal(HttpStatusCode.NotFound, r.StatusCode);
}
```

## Do
- Group with `app.MapGroup("/items")`, then chain `.RequireAuthorization()`, `.WithTags(...)` and filters once on the group.
- Return `TypedResults.Ok(x)` / `TypedResults.NotFound()` and declare `Results<Ok<Item>, NotFound>`, so OpenAPI metadata is inferred.
- Move handlers into static methods or classes per feature; keep Program.cs as wiring only.
- Take services as handler parameters (inferred from DI) and `CancellationToken ct` last.
- Validate with an endpoint filter (`AddEndpointFilter`) or a validation library; return `TypedResults.ValidationProblem(errors)`.
- Use `[AsParameters]` to bundle many query or route parameters into one record.
- Add `AddProblemDetails()` and `UseExceptionHandler()` for consistent errors.

## Avoid
- Returning anonymous objects or entities: no schema, over-exposure. Return named records as DTOs.
- Handlers as inline lambdas with 40 lines: untestable and unreadable. Extract methods.
- Forgetting that minimal APIs do no automatic model validation (no `[ApiController]`): add a filter, or invalid input passes straight through.
- Capturing scoped services in closures outside the handler: use parameters so DI resolves per request.
- Using `Results.Ok` with no declared return type and expecting accurate OpenAPI: use `TypedResults` plus a union return type.
- Anonymous endpoints by accident: set `FallbackPolicy` to require an authenticated user, then opt out with `.AllowAnonymous()`.

## Review
- [ ] Each endpoint declares its success and error result types.
- [ ] Authorization is applied at group level with explicit exceptions.
- [ ] Input is validated before use and failures return ProblemDetails.
- [ ] Program.cs only wires; logic is in testable methods.
- [ ] Tests cover at least one 4xx per route.
