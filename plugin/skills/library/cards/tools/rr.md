---
name: rr
title: rr (record and replay)
area: tools
tags: [rr, debugger, record-replay, gdb, flaky, native]
detect: []
related: [gdb-lldb, memory-leaks, perf]
---
rr records a native program run once and replays it deterministically under gdb, including reverse execution.

## Verify
- `rr record ./prog ARGS`: records the run; the trace is saved under the rr trace directory.
- `rr replay`: replays the latest trace in gdb, with the same behavior every time.
- `rr ls`: the recorded traces.
- `rr record --chaos ./prog`: randomizes scheduling to expose a race on a flaky failure.

## Test first
Make a failing command, loop it under `--chaos` until it fails, keep that trace.
```sh
for i in $(seq 1 100); do
  rr record --chaos ./prog || break
done
rr replay     # the failing recording
```
After the fix, the same loop must complete 100 runs.

## Do
- Build with `-g` and without stripping; rr works on optimized code but debugging is easier at `-O0` or `-Og`.
- In replay use `break`, `continue`, then `reverse-continue`, `reverse-next`, `reverse-step`, `reverse-finish`.
- Set a watchpoint on the corrupted value, then `reverse-continue` to find who wrote it last.
- Use `rr replay -M` to prefix output with the process and event, and `-p PID` to choose a process in a multi-process trace.
- Use `when` and `run N` / `seek` to move to an event number; `checkpoint` and `restart`.
- Share traces with `rr pack` so they are self-contained.
- Run on bare metal or a VM that exposes hardware performance counters; rr needs them.
- Set `kernel.perf_event_paranoid` to 1 or lower if recording is refused.

## Avoid
- Running in a container or VM that blocks perf counters: recording fails or is unsupported. Use bare metal or a compatible VM.
- Expecting rr on macOS or Windows: it is Linux only. Use gdb or lldb there.
- Debugging a single recorded run of a race and calling it fixed: reproduce under `--chaos` repeatedly after the fix.
- Using rr for GPU, or programs that need non-deterministic hardware access: unsupported.
- Deleting the trace before the root cause is found: keep it, `rr pack` it if you move it.
- Forgetting that replay is read-only: calls you make in gdb do not change history, and `call` results may diverge.

## Review
- [ ] The failure was captured in a trace, and the cause found by reverse execution.
- [ ] The fix is stress-tested under `--chaos` repeatedly.
- [ ] A regression test or sanitizer check was added.
- [ ] Trace files are cleaned up or archived deliberately.
