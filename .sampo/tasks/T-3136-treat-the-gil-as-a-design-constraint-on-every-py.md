---
id: T-3136
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T04:50:58Z
updated: 2026-11-05T04:50:58Z
steer_method_rate: 0.218
---
# Treat the GIL as a design constraint on every Python change in this work. For each…
## Raw request
> and make sure it isnt bottlenecked by the python GIL
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the GIL as a design constraint on every Python change in this work. For each CPU-bound path, concurrent path, or hot loop the change adds or touches, make sure threads sharing one interpreter are not what limits throughput.
- Classify each workload as CPU-bound, I/O-bound, or native-call-bound, and choose the mechanism to match:
- CPU-bound: use processes (`multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, or a subinterpreter or free-threaded build if the project's Python supports it), or move the work into native code that releases the GIL (NumPy, Cython `nogil`, Rust/C extensions).
- I/O-bound: use `asyncio` or threads.
- Do not use `threading` or `ThreadPoolExecutor` for pure-Python CPU work.
- Check the existing code and every new surface for GIL-bound patterns, including thread pools running pure-Python computation, shared-state locks serializing workers, and async handlers that block the event loop with CPU work. Fix them in place; don't just flag them.
- When processes are used, handle their costs: keep payloads small or use shared memory, avoid unpicklable arguments, reuse pool workers instead of respawning them, set the worker count from the available cores, and shut down cleanly with no orphaned workers.
- Prove it with measurement, not assumption. Add or run a benchmark that compares 1 worker against N workers on a realistic workload, and report the speedup, the core utilization, and any remaining serial section. Throughput should scale roughly with cores. If it doesn't, find the cause (GIL, lock co…
- Add tests for correctness under concurrency (no races, deterministic results, error propagation from workers, clean cancellation and shutdown). Keep the benchmark runnable and out of the normal fast test path if it is slow.
- Record in the docs or README which concurrency model is used and why, the Python version or build assumptions (for example, free-threaded 3.13+ versus the standard build), and how to tune the worker count.
- Apply this to future changes in the same code as a standing check: no new GIL-bound hot path should land without the benchmark evidence above.
- Do the work directly rather than only advising. Stay within the project's existing dependencies and interpreter unless a change is needed, and ask before anything outward or hard to reverse: installing system-wide packages or an alternate interpreter, changing the deployment environment, or adding …
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T04:50:58Z created
## Follow-ups captured
