**Verdict** — changes needed. Everything the AC lists is implemented. I did not run the tests. One HIGH issue, found by reading the code, can leave the stop half-done and unrecorded when an agent runs the new command.

## lens: adversary
- HIGH — plugin/lib/fmserve.py:188-205 — `panic_stop` kills its own caller's process group before it frees leases or writes the record. `fmsession.stop` does `os.killpg(pid, SIGTERM)` (fmsession.py:439), and the agent and its tools run in that group. `fmserve.stop` runs `systemctl disable --now`, which kills the unit's cgroup. The new rule line (foreman.md:17) tells a model to run `fm pause --now` for "stop everything now". If an fm session's agent, or a `fm serve` remote-control session, runs it, the loop at fmserve.py:111 SIGTERMs the python that is running it. No handler exists: grep finds no `signal.signal(SIGTERM)` in fmcli, fmcore or fmserve. PANIC is already written, so new starts stay blocked. But the leases are not freed, serve units after the caller are not stopped, and `stops.jsonl` is never written. — Fix: write the record first and update it at the end. Stop the caller's own group (compare `os.getpgid(0)`) and unit last. Or `signal.signal(SIGTERM, SIG_IGN)` and `os.setsid()` at the top of `panic_stop`. Add a test where the caller is a descendant of the session runner. — confidence high (code path; I did not run it)

## lens: edge
- MEDIUM — plugin/lib/fmserve.py:111-119 — one exception stops the whole sweep. `fmsession.stop` and `stop_all` (os.remove, systemctl) are unguarded. A failure in the Nth session or unit, for example a vanished file or a permission error, aborts `panic_stop` after some processes are killed. Leases stay, there is no record, and the CLI shows a traceback. — Fix: wrap each stop in try/except and collect the errors in `rec["errors"]`; write the record in a `finally`. — confidence medium
- LOW — plugin/lib/fmcli.py:3894 — `fm pause off --now` silently drops `--now` (`hard=on and args.now`). — Fix: reject the combination, or ignore it knowingly. — confidence high

## lens: intent
- LOW — plugin/lib/fmserve.py:517 and 933 — the `fm run` stop writes nothing to `stops.jsonl`; it only exits with a message and a run.log line. The CHANGELOG says "Each stop is recorded", and MASTER says "one record per stop". The code writes one record per `--now` invocation, listing only the sessions, serve steps and lease count. — Fix: append a record from the paused branches, or reword the docs. — confidence high

## lens: maintainer
- MEDIUM — plugin/tests/test_panic.py:191-215 — the serve half of the AC has no test. No unit is set up and `rec["serve"]` is never asserted, so removing `stop_all()` from `panic_stop` leaves the suite green. — Fix: stub `systemctl` plus a fake unit file and assert `rec["serve"]`. — confidence high
- LOW — plugin/tests/test_panic.py:217 — the lane-parallel branch (fmserve.py:516, `sys.exit` and lane cleanup) is untested. Only the sequential path is covered. — Fix: add a `--parallel 2` case. — confidence medium

## lens: operator
- No findings. The `_watch` wake-up changes from at most every 30 s to every 2 s, one `stat` and read of PANIC each. That cost is negligible. The always-on rules file changes by one inline clause. The pre-audit note on the guard-force-push and guard-publish evals does not apply, because this change touches neither guard.

## Acceptance criteria
- `fm pause --now` stops running fm sessions, serve units and leases and writes `stops.jsonl` — partly met. The session, lease and record paths have a test. The serve path is untested (see above). The self-kill case in the adversary lens is not handled.
- `fm run` stops its session under a hard pause — met in the sequential path (fmserve.py:564, 933) and covered by a test. The lane path is read-only verified.

## Implicit decisions
- A hard flag is stored as `"<ts> hard"` inside the PANIC file. A later plain `fm pause` downgrades it to soft.
- Only sessions with status starting or running are stopped.
- Leases are cleared for every owner, including interactive sessions' leases.
- A paused `fm run` exits non-zero via `sys.exit` or `fail`, and an empty lane is removed.

## Not checked
- The full test run, the `fm night` path, and the guard treatment of `fm pause --now` when called by a model.

**Noticed:** `set_panic` (fmcore.py:429) writes PANIC non-atomically, and `panicked(hard=True)` can read an empty file mid-write. That is benign now. Use `write_atomic` if the flag ever carries more.
