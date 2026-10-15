---
name: blazor
title: Blazor
area: dotnet
tags: [dotnet, csharp, blazor, razor, web, components, wasm]
detect: [dep:Microsoft.AspNetCore.Components.WebAssembly, dep:Microsoft.AspNetCore.Components.Web, dep:bunit, file:*.razor, ext:.razor]
related: [aspnet-core, signalr, xunit, dotnet-cli]
---
Blazor components: Razor syntax, render modes (Server, WebAssembly, Auto), parameters, lifecycle, forms, bUnit tests.

## Verify
- `dotnet build -warnaserror`: compiles Razor and C# with nullable warnings as errors.
- `dotnet test`: bUnit and unit tests.
- `dotnet format --verify-no-changes`: formatting.
- `dotnet publish -c Release`: a WebAssembly publish catches trimming and AOT problems.

## Test first
Use bUnit (`bunit` package) with xUnit; test projects render components in memory.
```csharp
public class CounterTests : TestContext
{
    [Fact]
    public void Click_increments_count()
    {
        var cut = RenderComponent<Counter>();
        cut.Find("button").Click();
        cut.Find("p").MarkupMatches("<p>Count: 1</p>");
    }
}
```
Register fakes with `Services.AddSingleton<...>()`; use `JSInterop.Mode = JSRuntimeMode.Loose` for JS calls.

## Do
- Declare the render mode per component or app (`@rendermode InteractiveServer`, `InteractiveWebAssembly`, `InteractiveAuto`); static SSR is the default for pages without one.
- Pass data in with `[Parameter]`, out with `EventCallback<T>`; mark route values `[SupplyParameterFromQuery]` where needed.
- Load data in `OnInitializedAsync` or `OnParametersSetAsync`; pass a `CancellationToken` and cancel in `Dispose`.
- Use `EditForm` with `DataAnnotationsValidator` and a model, and `@bind-Value` on inputs.
- Implement `IAsyncDisposable` for event subscriptions and JS object references.
- Call JS only from `OnAfterRenderAsync(firstRender)` via `IJSRuntime`.
- Call `StateHasChanged` via `InvokeAsync(StateHasChanged)` when updating from non-UI threads.

## Avoid
- Mutating a `[Parameter]` property inside the component: the parent overwrites it on rerender. Copy to a private field.
- JS interop during prerender or `OnInitialized`: no browser yet, throws. Use `OnAfterRenderAsync`.
- Injecting `DbContext` directly in Blazor Server components: the circuit-long scope makes it long-lived and not thread-safe. Use `IDbContextFactory<T>`.
- `async void` event handlers: exceptions crash the circuit. Return `Task`.
- Secrets or server-only logic in WebAssembly code: it ships to the browser. Keep it behind an API.
- Heavy work in `BuildRenderTree` or the markup expressions: runs on every render. Compute in lifecycle methods.
- Missing `@key` on lists that reorder: DOM state sticks to the wrong item.

## Review
- [ ] Render mode is explicit and matches where the component's services run.
- [ ] No server secrets reachable from WASM; auth checked on the server API.
- [ ] Subscriptions, timers and JS references are disposed.
- [ ] Forms validate and show messages; submit handlers are async Task.
- [ ] bUnit test covers the main interaction and one error state.
