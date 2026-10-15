---
name: bunit
title: bUnit
area: dotnet
tags: [dotnet, blazor, components, testing, razor, unit-tests]
detect: [dep:bunit, dep:bunit.web, dep:bunit.core]
related: [blazor, xunit, nunit, moq]
---
bUnit: render Blazor components in a test context, drive them through the DOM and assert on markup, with services faked.

## Verify
- `dotnet test --filter "FullyQualifiedName~Components"`: component tests pass.
- `dotnet build -warnaserror`: `.razor` and test code compile (Razor warnings surface here).
- `dotnet test --logger "console;verbosity=normal"`: shows which render and interop tests ran.

## Test first
Inherit `TestContext` (or `BunitContext` in newer releases, so match the installed version), register services, render and assert.
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

## Do
- Add services before rendering through `Services.AddSingleton<IClock>(new FakeClock())`.
- Pass parameters with `RenderComponent<T>(p => p.Add(x => x.Title, "Hi"))`, and use `.AddCascadingValue` for cascading parameters.
- Interact through the DOM: `cut.Find("css")`, `.Click()`, `.Change("value")`, `.Submit()`.
- Wait for async renders: `cut.WaitForAssertion(() => cut.Find(".done"))` and `cut.WaitForState(...)`.
- Set JS interop to a mode: `JSInterop.Mode = JSRuntimeMode.Loose` for incidental calls, or `JSInterop.Setup<string>("getTheme").SetResult("dark")` for expected ones.
- Use `MarkupMatches` for semantic markup comparison, which ignores whitespace and attribute order.
- Use `FakeNavigationManager` through `Services.GetRequiredService<NavigationManager>()` to assert navigation URIs.
- Use `AddAuthorization()` with `SetAuthorized("user")` to test auth-gated components.

## Avoid
- `Thread.Sleep` or `Task.Delay` to wait for rendering: it is flaky and slow. Use `WaitForAssertion`.
- Asserting on `cut.Markup` with exact string equality: whitespace noise fails tests. Use `MarkupMatches` or `Find` plus text.
- Missing service registrations: tests throw an `InvalidOperationException` on inject. Register fakes in the test constructor.
- Unconfigured JS interop in strict mode: calls throw. Set up the invocation or switch to Loose where it is irrelevant.
- Testing framework internals instead of component behavior: assert user-visible output and emitted callbacks.
- Reusing one context across tests: state leaks. Let xUnit build a new test class instance per test, and dispose it.
- Mixing bUnit versions with a different test adapter: match the packages as the bUnit docs show.

## Review
- [ ] Tests act through the DOM and assert rendered output or callbacks.
- [ ] Async UI uses `WaitForAssertion`, with no sleeps.
- [ ] JS interop and auth are set up deliberately.
- [ ] External services are faked, with no real HTTP or database.
- [ ] Each component test covers a loading, an error and a success path where relevant.
