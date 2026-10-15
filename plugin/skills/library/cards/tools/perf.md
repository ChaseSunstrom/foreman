---
name: perf
title: Linux perf
area: tools
tags: [perf, profiling, cpu, linux, sampling, performance]
detect: [file:perf.data]
related: [flamegraphs, py-spy, rr, memory-leaks]
---
Linux `perf`: CPU sampling and hardware counters to find where time goes before optimizing.

## Verify
- `perf stat -r 5 ./prog ARGS`: cycles, instructions, branches and wall time over five runs, with variance.
- `perf record -F 99 -g -- ./prog ARGS`: samples at 99 Hz with call graphs into `perf.data`.
- `perf report --stdio | head -40`: the top symbols by overhead.
- `perf top -p PID`: live hot functions of a running process.

## Test first
Write the benchmark first and record a baseline; the failing check is a budget.
```sh
perf stat -x, -e task-clock -r 5 ./bench 2> before.csv
# after the change
perf stat -x, -e task-clock -r 5 ./bench 2> after.csv
# assert after is lower by the target margin and variance is small
```
Pin the benchmark input so runs compare.

## Do
- Build with symbols and frame pointers: `-g -fno-omit-frame-pointer`; for Rust set `debug = true` in the release profile.
- For stripped or frame-pointer-free code use `--call-graph dwarf` (bigger files) or `--call-graph lbr` where supported.
- Run the workload for several seconds under realistic input and warm caches.
- Compare with `perf diff perf.data.old perf.data`.
- Annotate hot code with `perf annotate SYMBOL`.
- Generate flamegraphs from `perf script` output (see flamegraphs).
- Check IPC (instructions per cycle) and cache and branch misses in `perf stat` to tell memory-bound from compute-bound.
- Allow profiling for non-root with `kernel.perf_event_paranoid` and `kernel.kptr_restrict` set appropriately.

## Avoid
- Optimizing from intuition: profile first, change one thing, re-measure.
- Profiling a debug (`-O0`) build: the hot spots differ from release. Profile the optimized build with symbols.
- Missing symbols or broken stacks: no frame pointers or stripped binaries. Rebuild with them or use dwarf unwinding.
- Single noisy runs: CPU frequency, other load and cache state. Use `-r`, pin CPUs (`taskset`), and fix the governor.
- Sampling too fast (`-F` thousands) in production: overhead and huge files. Use 99 or a similar low rate.
- Reading `perf.data` from another host or after rebuilding the binary: symbols mismatch. Keep the matching binary.
- Leaving `perf.data` files in the repo.

## Review
- [ ] A baseline measurement exists with variance.
- [ ] The hot path was identified by a profile, not a guess.
- [ ] The change was re-measured on the same input and shows the gain.
- [ ] No `perf.data` or profile artifacts are committed.
