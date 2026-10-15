---
name: benchmarkdotnet
title: BenchmarkDotNet
area: dotnet
tags: [dotnet, csharp, benchmarks, performance, allocations, profiling]
detect: [dep:BenchmarkDotNet]
related: [dotnet-cli, nuget, xunit]
---
BenchmarkDotNet: measure time and allocations of small code paths in Release mode, with a baseline and a memory diagnoser.

## Verify
- `dotnet run -c Release --project Benchmarks -- --filter "*Parser*"`: runs only the matching benchmarks in Release.
- `dotnet run -c Release --project Benchmarks -- --list flat`: lists discovered benchmarks without running them.
- `dotnet build -c Release -warnaserror`: benchmarks compile with the optimizer on.
- `dotnet run -c Release --project Benchmarks -- --filter "*" --job short`: a quick smoke run for CI sanity, not for numbers.

## Test first
The failing check comes first: write a correctness test for the code being optimized, then the benchmark that proves a gain.
```csharp
[MemoryDiagnoser]
public class ParserBenchmarks
{
    private string _input = null!;
    [GlobalSetup] public void Setup() => _input = File.ReadAllText("sample.csv");

    [Benchmark(Baseline = true)]
    public int Split() => OldParser.Count(_input);

    [Benchmark]
    public int Span() => NewParser.Count(_input);
}
// Program.cs: BenchmarkRunner.Run<ParserBenchmarks>();  // and a unit test: Old == New
```

## Do
- Keep benchmarks in their own console project referencing the code under test, and always run with `-c Release` and no debugger attached.
- Add `[MemoryDiagnoser]` to see allocations per operation and GC counts.
- Mark one method `Baseline = true` so the ratio column compares alternatives.
- Do setup in `[GlobalSetup]` and `[IterationSetup]` only when needed, and parametrize inputs with `[Params(10, 1000)]`.
- Return the result from the benchmark method, or consume it with a `Blackhole`, so the JIT cannot remove the work.
- Use `BenchmarkSwitcher.FromAssembly(typeof(Program).Assembly).Run(args)` to choose benchmarks from the command line.
- Pin a runtime with `[SimpleJob(RuntimeMoniker.Net80)]` (or the installed target) when comparing runtimes.
- Compare results saved with `--exporters json` over time, and look at the distribution, not only the mean.

## Avoid
- Running in Debug or with a debugger: results are meaningless, and BenchmarkDotNet warns. Use Release.
- Unused results: dead-code elimination makes the benchmark measure nothing. Return or consume.
- Measuring I/O, the network or the database as microbenchmarks: noise swamps the signal. Benchmark pure code, and use load tests for I/O.
- Hand-rolled `Stopwatch` loops: they ignore warmup, tiering and outliers. Use the library.
- Putting construction costs inside `[Benchmark]` methods when only the operation matters: move them to setup.
- Trusting one run on a noisy machine: close other loads, and rerun to check the error and standard deviation columns.
- Shipping benchmarks in the test project run by `dotnet test`: they are slow. Keep them separate.

## Review
- [ ] Release configuration, with a baseline and the memory diagnoser enabled.
- [ ] Results are consumed, and setup is outside the measured method.
- [ ] A correctness test guards the optimized path.
- [ ] Inputs are realistic and parameterized across sizes.
- [ ] The claim of improvement cites ratio and allocation columns from the run.
