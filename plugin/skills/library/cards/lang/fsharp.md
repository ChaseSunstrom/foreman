---
name: fsharp
title: F#
area: lang
tags: [fsharp, dotnet, nuget, expecto, discriminated-unions, fantomas]
detect: [ext:.fs, ext:.fsx, ext:.fsproj, file:*.fsproj]
related: [csharp, aspnet-core]
---
F# baseline: dotnet CLI, compile-order-aware projects, discriminated unions and Option/Result over nulls and exceptions, Fantomas, Expecto or xUnit.

## Verify
- `dotnet build -warnaserror`: compile; incomplete matches become errors.
- `dotnet test`: test projects.
- `dotnet fantomas --check .`: formatting, when Fantomas is installed as a local tool.
- `dotnet fsi script.fsx`: a script runs in F# Interactive.

## Test first
Expecto or xUnit in a separate `.fsproj` that references the library. Add test files to the fsproj in order.
```fsharp
module PortTests

open Xunit
open Port

[<Theory>]
[<InlineData("")>]
[<InlineData("70000")>]
let ``parse rejects invalid`` (raw: string) =
    Assert.True((parse raw).IsError)
```

## Do
- List files in dependency order in the `.fsproj` `<Compile Include>` items; a file can only use files above it.
- Model domains with discriminated unions and records; make illegal states unrepresentable.
- Return `Result<'a,'e>` or `Option<'a>` for expected failures; use `Result.bind` and `Result.map` or a `result { }` builder.
- Keep functions small and pipe with `|>`; annotate public function signatures.
- Use `task { }` for .NET async interop and `async { }` for F#-native workflows; pass `CancellationToken`.
- Use `[<RequireQualifiedAccess>]` on unions whose cases collide with common names.
- Treat incomplete-pattern warnings (FS0025) as errors via `<WarnOn>`/`TreatWarningsAsErrors`.

## Avoid
- Wildcard `| _ ->` on a union you own: new cases silently fall through. List cases so the compiler flags additions.
- `null` and `Unchecked.defaultof`: NREs. Use `Option`; wrap .NET nullable returns with `Option.ofObj`.
- `mutable` and loops where `List`/`Seq`/`Array` functions fit: harder to reason about. Fold or map instead.
- Forgetting laziness: `Seq` pipelines re-evaluate on every enumeration. Materialize with `List.ofSeq` or `Seq.cache` when needed.
- Exceptions for control flow: costly and invisible in types. Use `Result`.
- `Async.RunSynchronously` inside async code: deadlocks. Compose with `let!`.
- Ambiguous `ToString()` on records and unions for logs or keys: unstable format. Use explicit formatting.
- Wrong file order in the fsproj: "not defined" errors that look like missing code. Reorder the Compile items.

## Review
- [ ] No new incomplete-match warnings or wildcard catch-alls over owned unions.
- [ ] Expected failures typed as `Result`/`Option`, not exceptions or nulls.
- [ ] fsproj compile order is correct and new files are listed.
- [ ] Public signatures annotated; formatting checked.
- [ ] Tests cover an error case.
