<!-- Foreman's own playbook (written for Foreman, not ported). -->
# C# build errors (dotnet, MSBuild, NuGet)

Use when `dotnet build`, `dotnet test` or `dotnet restore` fails. The goal is a green build with the smallest diff
that fixes the cause. Built on the library cards `fm lib show csharp` (the baseline), `fm lib show dotnet-cli`
(MSBuild, restore, solution-wide settings) and `fm lib show nuget` (package references, central versions, audit).

## Diagnostic commands

```bash
dotnet --info | head -20                     # the SDK picked for this folder (global.json applies)
dotnet --list-sdks
dotnet restore 2>&1 | tail -20               # package problems, before any compile
dotnet build --no-restore -tl:off 2>&1 | grep -E ': (error|warning) [A-Z]+[0-9]+' | sort -u
dotnet list package --vulnerable --include-transitive
dotnet list package --outdated
```

`-tl:off` turns off the live terminal logger so the output is plain lines; `sort -u` matters because of step 2 under First error.

## First error

Lines look like `src/App/Store.cs(42,17): error CS0103: The name 'Missing' does not exist in the current context
[src/App/App.csproj]`: file, (line,column), severity, code, message, then the project that compiled it.

1. **Read the code prefix first; it names the stage.** `NU` is NuGet restore, `NETSDK` is the SDK or target
   framework, `MSB` is MSBuild (copying, file locks, project files), `CS` is the compiler, `CA`/`IDE` are
   analyzers. Fix restore and SDK errors before any `CS` error: nothing compiles against a broken restore.
   Pass: you state the code and its stage before editing.
2. **Count from the summary, not the scroll.** `dotnet build` prints each error once as it happens and again in the
   summary, so two copies of one error are one error. The true count is the `N Error(s)` line.
3. **Syntax errors hide the rest.** While a file has a parse error (`CS1002 ; expected`, `CS1513 } expected`) the
   build reports only that; the type errors appear after it is fixed. Checked here: a missing `;` gave one error;
   fixing it revealed two more.
4. **Printed order is not line order.** In the same check, a `CS0103` on line 8 printed before a `CS8602` on line 7.
   Sort by file and line, and fix the declaration others depend on first.
5. **Warnings as errors.** With `TreatWarningsAsErrors` (or `-warnaserror`) a warning code shows as `error`:
   `CS8600`–`CS8625` are nullable warnings, `CS1998`/`CS4014` async ones. Fix the code; don't drop the setting.

## Common causes

| Error | Usual cause | Fix |
|---|---|---|
| `CS0103 The name 'x' does not exist in the current context` | Typo, out-of-scope variable, missing `using static` | Fix the name or declare it in scope |
| `CS0246 The type or namespace name 'X' could not be found` / `CS0234` | Missing `using`, or the package or project reference is missing | Add the `using`; `dotnet add package X` or `dotnet add reference ../X/X.csproj` |
| `CS1061 'T' does not contain a definition for 'M'` | Wrong type, or an extension method whose namespace isn't imported | Fix the call or add the `using` for the extension's namespace |
| `CS0029` / `CS0266 Cannot implicitly convert type 'A' to 'B'` | Type mismatch | Convert explicitly (`int.Parse`, `(B)a` only where the cast is safe) |
| `CS8602 Dereference of a possibly null reference` | Nullable value used without a check | Check for null, use `?.`/`??`, or make the value non-nullable at its source |
| `CS8618 Non-nullable property 'P' must contain a non-null value when exiting constructor` | Property never set | Initialise it, mark it `required`, or make it nullable if null is a real state |
| `CS0535 'T' does not implement interface member 'I.M()'` | Missing member or signature drift | Implement it with the exact signature |
| `NU1101 Unable to find package X` | Wrong ID, or the feed is missing from nuget.config | Check the ID; add the source to nuget.config |
| `NU1605 Detected package downgrade` | A direct reference pins lower than a transitive one needs | Raise the direct reference (in Directory.Packages.props when central versions are on) |
| `NU1902`/`NU1903`/`NU1904 Package 'X' has a known … severity vulnerability` | Vulnerable version, failing under warnings-as-errors | Upgrade to a patched version; `dotnet list package --vulnerable` names it |
| `NETSDK1045 The current .NET SDK does not support targeting .NET N` | SDK older than the `TargetFramework` | Install that SDK, or fix a `global.json` that pins an older one |
| `MSB3027`/`MSB3021 Could not copy … being used by another process` | The app or a test host still running | Stop the process (`dotnet build-server shutdown` for compiler servers), rebuild |

## Verify

```bash
dotnet build -warnaserror && dotnet test --no-build && dotnet format --verify-no-changes
```

Pass: exit 0, the build summary reads `0 Error(s)`, and `dotnet format` reports nothing to change. Run it on the
solution file when there is one, so every project builds.

## Rules

- No new `#pragma warning disable`, `<NoWarn>`, `<Nullable>disable</Nullable>` or
  `<TreatWarningsAsErrors>false</TreatWarningsAsErrors>` in the diff to make an error go away.
- No `!` (null-forgiving) added without a comment naming why the value can't be null there.
- Package versions change in one place: `Directory.Packages.props` when central package management is on.
- Rebuild after each fix and read the new output.

## Stop conditions

Stop and report when the same error survives three fixes, when the fix needs a new SDK or target framework the
project hasn't agreed to, or when nullable errors need an API's contract changed.

## Report

```text
[FIXED] src/App/Store.cs(42,17)  CS8602 Dereference of a possibly null reference
Fix: early return when FindUser returns null
Build: dotnet build 0 Error(s) | dotnet test passed | files: src/App/Store.cs
```
