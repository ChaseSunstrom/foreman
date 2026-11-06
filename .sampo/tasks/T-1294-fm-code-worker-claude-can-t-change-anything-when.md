---
id: T-1294
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:26:12Z
updated: 2026-10-20T21:50:26Z
base: 8cb307f3082fa5df9f703e6171f39fb12ad0e1f7
base_tree: 8db6721245af02a664190eff94feab3ee27a7650
plan0_at: 2026-10-20T21:37:17Z
plan0_scope: []
verified: strong
---
# fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same code
## Raw request
> fm code --worker claude can't change anything when Foreman is installed: the worker's own Claude Code session takes a Foreman lease on what it edits (calc.py::add), the judge then treats that lease as another session's and puts the edit back ('reverted calc.py: Foreman lease: calc.py::add is leased by session 26279f58 (T-0001)'), and every later worker turn is refused by the same lease; found by fm code bench --worker claude (0/2)
## Interpretation
fm code --worker claude couldn't keep any change for a user with Foreman installed. Each worker turn is a new Claude Code session; its Foreman PostToolUse hook leased the function it edited under that session; fm code's judge then runs the guard as session fm-code-<task>, which saw another session's lease and put the edit back; the next turn's session was refused the same function. Found by fm code bench --worker claude (0/2).
## Assumptions (confidence)
## Acceptance criteria
- [x] with FOREMAN_WORKER_OF set (fm code's run session), a worker session's edit leases under the run's id: the run's judge and the run's next worker session see no conflict on it, while an unrelated session still gets the lease refusal — verify with `python3 plugin/tests/run.py test_bus`
- [x] fm code gives each worker turn FOREMAN_WORKER_OF=fm-code-<task> — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] fm code bench --worker claude closes the operator seed on this machine (it scored 0/2 before) — verify with `fm code bench --worker claude --seeds operator --seed-timeout 400`
## Non-goals
## Approach (options → choice → why)
Options: (a) skip leases when the lease's task equals the caller's task — rejected: two real sessions in one project share the active task, so leases would never fire; (b) turn Foreman's hooks off inside worker sessions — rejected: the worker keeps the guard as a second line of defence; (c) chosen: fm code passes FOREMAN_WORKER_OF=fm-code-<task> to each worker turn, and fmbus takes the lease identity from it (one _me(pl) for after_edit and conflict), so the run's judge and its later turns own the lease while any other session is still refused. Leases are advisory coordination, not a security boundary, so an env-named identity is acceptable.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fmbus lease identity under FOREMAN_WORKER_OF; the worker sees the variable
2. [x] fmbus: one _me(pl) used by after_edit and conflict; fm code: the variable in the worker's env
3. [x] A real bench run with the claude CLI; CHANGELOG
## Resume here
## Docs impact
CHANGELOG, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → ✗ exit 1 · Ran 25 tests in 35.2s (2 classes, 16 at a time; slowest: Worker 35s, Lease 2s) / FAILED (2 classes) [ran] [tree 31d733bf864d] (2026-10-20T21:35:52Z)
- (step 2) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → exit 0 · Ran 25 tests in 35.2s (2 classes, 16 at a time; slowest: Worker 35s, Lease 2s) / OK [ran] [tree 8db6721245af] (2026-10-20T21:36:36Z)
- (ac 3) `fm code bench --worker claude --seeds operator --seed-timeout 400` → exit 0 · ✓  operator        18.6s  1 check run  0 refused  0 tokens / score 1/1 (1.00); last time 1.00  ·  kept in ~/.claude/foreman/state/code-bench.jsonl [ran] [tree 3b78c97047a8] (2026-10-20T21:37:47Z)
- (ac 1) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → exit 0 · Ran 25 tests in 37.6s (2 classes, 16 at a time; slowest: Worker 37s, Lease 2s) / OK [ran] [tree 3b78c97047a8] (2026-10-20T21:38:29Z)
- (ac 2) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → exit 0 · Ran 25 tests in 38.2s (2 classes, 16 at a time; slowest: Worker 38s, Lease 2s) / OK [ran] [tree 3b78c97047a8] (2026-10-20T21:39:08Z)
- (step 3) `fm code bench --worker claude --seeds operator --seed-timeout 400` → exit 0 · ✓  operator        26.7s  1 check run  0 refused  0 tokens / score 1/1 (1.00); last time 1.00  ·  kept in ~/.claude/foreman/state/code-bench.jsonl [ran] [tree 3b78c97047a8] (2026-10-20T21:39:35Z)
- `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → ✗ exit 1 · Ran 25 tests in 38.6s (2 classes, 16 at a time; slowest: Worker 38s, Lease 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 3b78c97047a8] (2026-10-20T21:40:51Z)
- `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → exit 0 · Ran 25 tests in 37.4s (2 classes, 16 at a time; slowest: Worker 37s, Lease 2s) / OK [ran] [tree 3b78c97047a8] (2026-10-20T21:40:51Z)
- (step 2) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → ✗ exit 1 · Ran 26 tests in 127.9s (2 classes, 16 at a time; slowest: Worker 128s, Lease 6s) / FAILED (1 classes) [ran] [tree 8082022d7a12] (2026-10-20T21:45:43Z)
- (step 2) `python3 plugin/tests/run.py test_bus.Lease test_code_worker.Worker` → exit 0 · Ran 26 tests in 77.1s (2 classes, 16 at a time; slowest: Worker 77s, Lease 5s) / OK [ran] [tree ef019e9cf000] (2026-10-20T21:47:14Z)
- (ac 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 16 tests in 8.2s (5 classes, 16 at a time; slowest: Watch 8s, Approvals 5s, Conductor 4s) / OK [ran] [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 24 tests in 41.9s (1 classes, 16 at a time; slowest: Worker 42s) / OK [ran] [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (ac 3) `fm code bench --worker claude --seeds operator --seed-timeout 400` → exit 0 · ✓  operator        22.2s  1 check run  0 refused  0 tokens / score 1/1 (1.00); last time 1.00  ·  kept in ~/.claude/foreman/state/code-bench.jsonl [ran] [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (audit intent) `one fm-reviewer pass (research/T-1294-review.md): approve with nits; all three applied test-first (a stray FOREMAN_WORKER_OF is ignored, the run's leases are dropped at its end, MASTER names the variable); red-to-green proved; a real fm code bench --worker claude run went from 0/2 to 1/1` → a worker turn's edits lease as fm-code-<task>, so the judge keeps them and the next turn edits the same function; the claude CLI now closes the operator seed [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (audit adversary) `one fm-reviewer pass (research/T-1294-review.md): approve with nits; all three applied test-first (a stray FOREMAN_WORKER_OF is ignored, the run's leases are dropped at its end, MASTER names the variable); red-to-green proved; a real fm code bench --worker claude run went from 0/2 to 1/1` → the value passes _sid (word chars, 80 max) and only a value starting fm-code- counts; leases are advisory, so a forged run id gains nothing an edit couldn't [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (audit edge) `one fm-reviewer pass (research/T-1294-review.md): approve with nits; all three applied test-first (a stray FOREMAN_WORKER_OF is ignored, the run's leases are dropped at its end, MASTER names the variable); red-to-green proved; a real fm code bench --worker claude run went from 0/2 to 1/1` → an unrelated session is still refused; a stray shell-rc value is ignored; the run's leases are freed in a finally, whatever way it ends [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (audit operator) `one fm-reviewer pass (research/T-1294-review.md): approve with nits; all three applied test-first (a stray FOREMAN_WORKER_OF is ignored, the run's leases are dropped at its end, MASTER names the variable); red-to-green proved; a real fm code bench --worker claude run went from 0/2 to 1/1` → fm code --worker claude works for anyone with Foreman installed, which is everyone who has fm code [tree ef019e9cf000] (2026-10-20T21:48:45Z)
- (audit maintainer) `one fm-reviewer pass (research/T-1294-review.md): approve with nits; all three applied test-first (a stray FOREMAN_WORKER_OF is ignored, the run's leases are dropped at its end, MASTER names the variable); red-to-green proved; a real fm code bench --worker claude run went from 0/2 to 1/1` → one _me(pl) used by after_edit and conflict; drop_session beside release [tree ef019e9cf000] (2026-10-20T21:48:45Z)
## Log
- 2026-10-20T21:26:12Z created
- 2026-10-20T21:34:56Z planned from capture
- 2026-10-20T21:37:17Z focused
- 2026-10-20T21:50:24Z done
- 2026-10-20T21:50:26Z committed d0662fb8 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1215 [FEATURE M, done, 3 steps] fm code bench: grade any model or worker as a Foreman worker on seeded tasks — lesson: A bench must grade what the harness can check it…
- research T-1214-review: Verdict: changes needed.** The judge works for the tested cases, but several simple moves get past it. [stale: site/pages.py changed since it was…
- T-1271 [SECURITY S, done, 2 steps] fm code --worker --verify: the worker can't change the files the user's verify names; such edits are put back and reported — lesson: P…
- decision 2026-10-20: [costly] Run fm code bench --worker claude on 2 seeds (operator, off-by-one) as T-1215's real end-to-end check
- similar finished tasks took 2–3 steps
## Why not caught
none before: the worker tests use stub CLIs without Foreman's hooks, so a worker session that takes leases was never exercised; now test_bus covers the lease identity and fm code bench --worker claude exercises the real path
## Lessons
- A harness that judges a worker with its own guard must make the worker's coordination state (leases, claims) the harness's own, or the guard defends the harness against its own worker
## Plan gaps
- failed first: step 1 Failing tests: fmbus lease identity under FOREMAN_WORKER_OF; the worker sees the variable
## Files touched
- CHANGELOG.md
- plugin/tests/test_bus.py
- plugin/tests/test_code_worker.py
- MASTER.md
- plugin/lib/fmbus.py
- plugin/lib/fmcode.py
