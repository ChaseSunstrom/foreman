---
id: T-0823
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-14T18:16:44Z
updated: 2026-10-14T18:34:37Z
base: 4bdf495472e642fa090e48cf57d85992a7a16857
base_tree: 374a0776be48dd6dc51c15e04f5c763d42880196
verified: strong
---
# Fm lane brief refuses (or warns) when the task fails the same plan_gaps check fm focus app
## Raw request
> fm lane brief refuses (or warns) when the task fails the same plan_gaps check fm focus applies — a builder was launched for an under-planned task and could only stop
## Interpretation
fm focus refuses a task with plan gaps (fmcli focus → c.plan_gaps); fm lane brief didn't, so a builder was launched for T-0821 and could only stop. Apply the same check in builder_brief.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief refuses a task fm focus would refuse as under-planned, naming the gaps — verify with `python3 plugin/tests/run.py test_builder`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then the plan_gaps check in builder_brief
## Resume here
## Docs impact
none: refusal is self-describing
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 6.2s (6 classes, 16 at a time; slowest: Contract 6s, Brief 3s, Flow 1s) / OK [ran] [tree ee7c0734d9be] (2026-10-14T18:32:16Z)
- `python3 plugin/tests/run.py test_builder` → ✗ exit 1 · Ran 20 tests in 6.5s (6 classes, 16 at a time; slowest: Contract 6s, Brief 3s, Flow 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ee7c0734d9be] (2026-10-14T18:32:29Z)
- `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 6.0s (6 classes, 16 at a time; slowest: Contract 6s, Brief 3s, Flow 1s) / OK [ran] [tree ee7c0734d9be] (2026-10-14T18:32:29Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.9    46.8     150  [0] / SessionEnd                  36.5    41.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree ee7c0734d9be] (2026-10-14T18:34:23Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 6.3s (6 classes, 16 at a time; slowest: Contract 6s, Brief 3s, Flow 1s) / OK [ran] [tree ee7c0734d9be] (2026-10-14T18:34:36Z)
- (audit edge) `self: builder_brief applies the same plan_gaps check fm focus applies, before taking a builder slot` → an active/verifying task is refused earlier by the status check, so plan_gaps' active exemption in focus doesn't matter here [tree ee7c0734d9be] (2026-10-14T18:34:36Z)
- (audit self) `self: builder_brief applies the same plan_gaps check fm focus applies, before taking a builder slot` → no findings [tree ee7c0734d9be] (2026-10-14T18:34:36Z)
## Log
- 2026-10-14T18:16:44Z created
- 2026-10-14T18:31:43Z focused
- 2026-10-14T18:34:36Z done
- 2026-10-14T18:34:37Z committed 7eb3a6c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0436 [SECURITY M, done, 3 steps] fm pause: one flag stops everything Foreman runs unattended — lesson: a kill switch is one flag every launcher checks at its own entry…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Lessons
- A launcher must check every refusal its launched agent's first command can hit
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
