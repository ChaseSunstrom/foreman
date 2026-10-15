---
name: julia
title: Julia
area: lang
tags: [julia, pkg, multiple-dispatch, test, juliaformatter, performance]
detect: [ext:.jl, file:Project.toml, file:Manifest.toml, file:.JuliaFormatter.toml]
related: [python]
---
Julia packages and scripts: Pkg environments, `Test` stdlib, multiple dispatch, type-stable code, JuliaFormatter.

## Verify
- `julia --project -e 'using Pkg; Pkg.instantiate()'`: the environment resolves from `Project.toml` and `Manifest.toml`.
- `julia --project -e 'using Pkg; Pkg.test()'`: runs `test/runtests.jl` in a clean test environment.
- `julia --project -e 'using JuliaFormatter; exit(format("."; verbose=true) ? 0 : 1)'`: exit 0 means everything was already formatted.
- `julia --project -e 'using MyPkg'`: the package loads and precompiles with no warnings.

## Test first
`test/runtests.jl` includes `@testset` blocks; add test-only deps under `[extras]` and `[targets]` or `test/Project.toml`.
```julia
using Test, MyPkg

@testset "parse_amount" begin
    @test parse_amount("12.5") == 12.5
    @test_throws ArgumentError parse_amount("")
    @test isnothing(tryparse_amount("x"))
end
```

## Do
- Work in a project (`julia --project`) and never rely on the global environment; commit `Manifest.toml` for apps, not for libraries.
- Add `[compat]` bounds for every dependency and for `julia` in `Project.toml`.
- Keep functions type-stable: same input types give one return type. Check with `@code_warntype` and `@inferred` in tests.
- Annotate struct fields with concrete types (or parametric `T`), and use `const` for global constants.
- Dispatch on types instead of `if isa` chains; add methods, don't branch.
- Benchmark with BenchmarkTools (`@btime f($x)`), interpolating arguments with `$`.
- Use `@views` or `view` to avoid slice copies and pre-allocate with `similar`/`zeros`; mutate with `!` functions.

## Avoid
- Non-const globals in hot paths: they are type-unstable and slow. Use `const` or pass as arguments.
- Abstract-typed struct fields (`x::Real`, `x::Any`): boxing. Use a type parameter.
- Timing the first call: it includes compilation. Call once to warm up, then measure.
- `Pkg.add` inside scripts: mutates the environment at runtime. Declare in `Project.toml`.
- Type piracy (extending a Base method for Base types you don't own): breaks other packages. Define a wrapper type.
- Growing arrays with `push!` in a loop when the size is known: preallocate.
- Hardcoding 1-based indexing assumptions on generic arrays: use `eachindex`, `axes` or `firstindex`.

## Review
- [ ] `[compat]` is present and `Pkg.test()` passes from a fresh clone.
- [ ] Hot functions are type-stable, with no `Any` in `@code_warntype` output.
- [ ] No new global mutable state without `const` or `Ref`.
- [ ] Public functions have docstrings and are listed in `export` or `public`.
- [ ] Tests use `@test_throws` for failure paths and avoid exact float `==` (use `isapprox` or `≈`).
