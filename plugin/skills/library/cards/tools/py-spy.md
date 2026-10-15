---
name: py-spy
title: py-spy
area: tools
tags: [python, py-spy, profiling, sampling, flamegraph, production]
detect: [dep:py-spy]
related: [flamegraphs, pdb, perf, memory-leaks]
---
py-spy: a sampling profiler for Python processes that attaches without code changes or restarts.

## Verify
- `py-spy dump --pid PID`: current stack of every thread, for hangs and stuck workers.
- `py-spy top --pid PID`: live view of hot functions.
- `py-spy record -o profile.svg -- python script.py`: runs the script and writes a flame graph.
- `py-spy record --pid PID --duration 30 -o profile.svg`: samples a running process for 30 seconds.

## Test first
Practice check: reproduce the slowness with a pinned input and keep the profile as evidence.
```sh
py-spy record -r 100 -f speedscope -o before.json -- python bench.py
# change code, re-run into after.json, compare the hot frames and a timing assertion
```
Add a timing or call-count test for the fixed hot path so it cannot regress.

## Do
- Attach with `--pid`; it needs ptrace permission, so use `sudo` or set `kernel.yama.ptrace_scope` appropriately; in Docker add the `SYS_PTRACE` capability.
- Use `--native` to include C extension frames, so time in NumPy or other native code is visible.
- Use `--idle` to include sleeping threads when hunting waits, and `--gil` to show only the thread holding the GIL.
- Use `-f speedscope` or `-f raw` for output formats; the default is SVG.
- Use `--subprocesses` to follow worker processes (gunicorn, multiprocessing).
- Use `py-spy dump --locals` to see variables of stuck frames.
- Profile real workloads: sample for tens of seconds under production-like load.
- Pick rate with `--rate` (default 100 samples per second); raise it for short runs.

## Avoid
- Profiling in a tiny, unrealistic run: sampling noise dominates. Use representative input.
- Forgetting that wall-clock sampling by default shows idle time too if `--idle` is used: choose based on CPU versus waiting questions.
- Running as an unprivileged user and being denied: "Permission denied" is ptrace policy, not a py-spy bug.
- Assuming it measures memory or allocations: it samples CPU stacks only. Use `tracemalloc` or memray for memory.
- Optimizing a function because it is visible in one flame graph: confirm with a second run and a benchmark.
- Using cProfile in production: high overhead and requires code changes. py-spy attaches externally.
- Committing profile SVG or JSON files.

## Review
- [ ] Profile taken under realistic load, with native frames when extensions matter.
- [ ] The hot frame identified is the one changed.
- [ ] A before and after measurement shows improvement.
- [ ] No profiles committed.
