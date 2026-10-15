---
name: dotnet-cli
title: dotnet CLI
area: dotnet
tags: [dotnet, csharp, cli, build, msbuild, sdk, tooling]
detect: [file:*.csproj, file:*.sln, file:*.slnx, file:global.json, file:Directory.Build.props, ext:.cs]
related: [nuget, xunit, nunit, aspnet-core, ef-core]
---
The dotnet CLI and MSBuild: restore, build, test, format, publish, local tools and solution-wide settings.

## Verify
- `dotnet build -warnaserror --no-incremental`: a clean, full compile with warnings as errors.
- `dotnet test --no-build`: tests against the build just verified.
- `dotnet format --verify-no-changes`: whitespace, style and analyzer fixes are applied.
- `dotnet --list-sdks`: the SDK that `global.json` pins is installed.
- `dotnet tool restore`: local tools from `.config/dotnet-tools.json` install.

## Test first
Add a test project and reference the project under test. A failing test is a red `dotnet test`.
```
dotnet new xunit -o tests/App.Tests
dotnet add tests/App.Tests reference src/App
dotnet sln add tests/App.Tests
dotnet test tests/App.Tests --filter "FullyQualifiedName~Slugify"
```
Write the test, see it fail for the right reason (assert failure, not a compile error stub you forgot), then implement.

## Do
- Pin the SDK in `global.json` with `rollForward` set deliberately.
- Put shared settings in `Directory.Build.props`: `Nullable` enabled, `TreatWarningsAsErrors`, `LangVersion`, analyzers.
- Use central package versions via `Directory.Packages.props` (`ManagePackageVersionsCentrally`).
- Pass `-c Release` for publish and benchmarks; `dotnet publish` for deployable output.
- Use `dotnet watch` (or `dotnet watch test`) while iterating.
- Install tools locally (`dotnet new tool-manifest`, `dotnet tool install dotnet-ef`) so versions are shared with the repo.
- Use `--no-restore` / `--no-build` in CI steps after a first restore and build.

## Avoid
- Global tool installs for repo tooling: versions drift between machines. Use a local manifest.
- `dotnet add package` without checking the target: it lands in the nearest csproj, and with central management it should go in `Directory.Packages.props`.
- Running `dotnet test` in Debug and shipping Release: Release-only differences (optimizations, `#if DEBUG`) go untested. Run CI in Release.
- Disabling nullable warnings project-wide to get green: fix the flow or annotate.
- Editing `obj/` or `bin/` or committing them: ignore both.
- Mixed SDK-style and floating `*` package versions: nondeterministic builds. Pin exact versions, and enable lock files (`RestorePackagesWithLockFile`) if reproducibility matters.
- `dotnet run` for a project with several launch profiles without `--launch-profile`: it may pick an unexpected one.

## Review
- [ ] `global.json`, props files and package versions are checked in and consistent.
- [ ] Warnings are errors in CI; no blanket `NoWarn`.
- [ ] Test project is in the solution and runs in `dotnet test` at the root.
- [ ] Release configuration builds and passes tests.
- [ ] Tools are in the local manifest.
