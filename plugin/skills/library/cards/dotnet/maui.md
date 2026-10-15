---
name: maui
title: .NET MAUI
area: dotnet
tags: [dotnet, csharp, maui, mobile, xaml, mvvm, cross-platform]
detect: [dep:Microsoft.Maui.Controls, dep:CommunityToolkit.Maui, dep:CommunityToolkit.Mvvm, file:MauiProgram.cs]
related: [xunit, nuget, dotnet-cli, xcodebuild]
---
.NET MAUI: cross-platform XAML apps for Android, iOS, macOS and Windows with MVVM, Shell navigation and handlers.

## Verify
- `dotnet build -f net8.0-android`: Android target compiles (use the project's actual TargetFramework from the csproj).
- `dotnet workload list`: required MAUI workloads are installed.
- `dotnet test`: view-model and service tests in a plain net project.
- `dotnet build -warnaserror`: nullable and XAML compiled-binding warnings fail the build.

## Test first
Keep logic in view models in a plain class library that the test project can reference without platform workloads.
```csharp
[Fact]
public async Task Load_sets_items_and_clears_busy()
{
    var vm = new ItemsViewModel(new FakeItemService(["a", "b"]));
    await vm.LoadCommand.ExecuteAsync(null);
    Assert.Equal(2, vm.Items.Count);
    Assert.False(vm.IsBusy);
}
```
`CommunityToolkit.Mvvm` generates `LoadCommand` from `[RelayCommand] Task Load()`.

## Do
- Use MVVM with `CommunityToolkit.Mvvm` (`[ObservableProperty]`, `[RelayCommand]`); keep code-behind to view-only concerns.
- Register pages, view models and services in `MauiProgram.CreateMauiApp()` and take them through constructors.
- Turn on compiled bindings: set `x:DataType` on pages and templates.
- Navigate with Shell routes (`Routing.RegisterRoute`, `Shell.Current.GoToAsync`).
- Use platform APIs through `Microsoft.Maui.*` abstractions (Preferences, SecureStorage, Connectivity, Permissions) and request permissions at runtime.
- Customize native controls with handler mappings (`Microsoft.Maui.Handlers`), not renderers.
- Use `CollectionView` with `DataTemplate` for lists, with `MainThread.BeginInvokeOnMainThread` for UI updates from other threads.

## Avoid
- Xamarin.Forms APIs and custom renderers: obsolete in MAUI. Use handlers and `Microsoft.Maui.Controls`.
- `ListView` for new lists: legacy. Use `CollectionView`.
- Blocking the UI thread with `.Result` or sync IO: freezes the app. Use async commands.
- Forgetting manifest entries: permissions and capabilities need Info.plist (iOS) and AndroidManifest changes in addition to runtime requests.
- Storing tokens in `Preferences`: plain text. Use `SecureStorage`.
- Binding without `x:DataType`: reflection bindings are slower and fail silently at runtime.
- Leaving event handlers or messenger registrations attached after page disappears: leaks. Unsubscribe in `OnDisappearing`.

## Review
- [ ] Logic lives in view models covered by tests; code-behind is thin.
- [ ] Bindings are compiled (`x:DataType` set).
- [ ] Permissions requested at runtime and declared per platform.
- [ ] Secrets use SecureStorage; no UI-thread blocking.
- [ ] Builds for every shipped target framework.
