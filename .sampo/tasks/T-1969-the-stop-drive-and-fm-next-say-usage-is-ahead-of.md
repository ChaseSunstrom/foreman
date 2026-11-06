---
id: T-1969
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T10:56:03Z
updated: 2026-10-29T11:35:36Z
base: f9a472e356277e51d5e2ab51f2544c93104bcda6
base_tree: c96223ca53cca9cea0bd122d943e63e2b9dbe867
plan0_at: 2026-10-29T11:27:28Z
plan0_scope: []
verified: strong
---
# The Stop drive and fm next say 'Usage is ahead of pace (<why>)' when fmbudget.degrade's re
## Raw request
> The Stop drive and fm next say 'Usage is ahead of pace (<why>)' when fmbudget.degrade's reason is the spent risk budget, which isn't usage: degrade could return the whole phrase and callers drop their prefix (fmhooks ~3667, fm next, fm ideas; tests in test_perf_cost assert 'ahead of pace')
## Interpretation
fmbudget.degrade's reason can be the spent risk budget; three callers wrap any reason as 'usage ahead of pace (…)', which misnames it
## Assumptions (confidence)
## Acceptance criteria
- [x] every optional-work-dropped message names its reason without calling a spent risk budget usage pace — verify with `python3 plugin/tests/run.py test_perf_cost test_risk test_loop`
## Non-goals
## Approach (options → choice → why)
Word the three messages (Stop drive, fm next's self-improvement wait, fm ideas --deepen) as 'optional work is dropped (<reason>)'; the reasons already say what they are (weekly usage N%…, 5-hour usage, risk budget spent). Alternatives: prefix the pace reason inside degrade (still misnames 5-hour usage); a kind field (more code for wording).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: a spent risk budget's Stop drive text doesn't say usage is ahead of pace
2. [x] reword the four callers (fmhooks drive, fmcore next, fmideas, fmwatch) around the reason
## Resume here
<!-- auto -->
- 2026-10-29T11:28:26Z step 1/2: red: a spent risk budget's Stop drive text doesn't say usage is ahead of pace
- git: foreman/build; 5 uncommitted: plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmideas.py, plugin/tests/test_perf_cost.py, plugin/tests/test_risk.py
- touched since last checkpoint: plugin/tests/test_risk.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmideas.py, plugin/tests/test_perf_cost.py
## Docs impact
CHANGELOG Unreleased Fix line. MASTER unchanged: it describes the pause, not its wording.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_risk -k usage_pace` → ✗ exit 1 · Ran 9 tests in 3.9s (2 classes, 16 at a time; slowest: Risk 4s, Usage 0s) / FAILED (1 classes) [ran] [tree 5e1ea5dc6714] (2026-10-29T11:27:59Z)
- (step 2) `python3 plugin/tests/run.py test_perf_cost test_risk test_loop test_ideas test_drive_side` → exit 0 · Ran 66 tests in 9.1s (18 classes, 16 at a time; slowest: Ideas 9s, DriveSide 5s, Loop 5s) / OK [ran] [tree 51b15610526b] (2026-10-29T11:29:48Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmideas.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.3    45.5     150  [0] / SessionEnd                  34.9    37.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree db028cf60ec8] (2026-10-29T11:34:19Z)
- (ac 1) `python3 plugin/tests/run.py test_perf_cost test_risk test_loop` → exit 0 · Ran 38 tests in 4.2s (12 classes, 16 at a time; slowest: Loop 4s, Risk 4s, LoopReview 4s) / OK [ran] [tree db028cf60ec8] (2026-10-29T11:34:44Z)
- (step 1) `python3 plugin/tests/run.py test_risk -k usage_pace` → exit 0 · Ran 9 tests in 3.9s (2 classes, 16 at a time; slowest: Risk 4s, Usage 0s) / OK [ran] [tree db028cf60ec8] (2026-10-29T11:34:44Z)
- (audit intent) `self-review of the 3-line diff: every caller of fmbudget.degrade(p) now names its reason without calling it usage pace; fmbudget.check_subagent and fmwatch's alert read only the usage reason, so they keep theirs; pane hits are comments/fixtures` → the Stop drive for a spent risk budget no longer says ahead of pace (test_a_spent_budget_is_not_called_usage_pace) [tree db028cf60ec8] (2026-10-29T11:34:44Z)
- (audit edge) `self-review of the 3-line diff: every caller of fmbudget.degrade(p) now names its reason without calling it usage pace; fmbudget.check_subagent and fmwatch's alert read only the usage reason, so they keep theirs; pane hits are comments/fixtures` → usage-only readers (check_subagent, fmwatch degrade() with no project) keep 'ahead of pace' since that is their only reason [tree db028cf60ec8] (2026-10-29T11:34:44Z)
## Log
- 2026-10-29T10:56:03Z created
- 2026-10-29T11:02:23Z set type=FIX, tier=M
- 2026-10-29T11:02:24Z planned: it has criteria and steps
- 2026-10-29T11:27:28Z focused
- 2026-10-29T11:35:35Z done
- 2026-10-29T11:35:36Z committed 52af012a (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-1967 [FEATURE M, done, 3 steps] round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace — lesson: A slowdown reason from fmbu…
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- decision 2026-10-23: Usage pace: subagents paused at 75% weekly usage with 27% of the week gone; work continues in the main thread, security items first (T-1751, T-1749)…
## Why not caught
none: the wording tests mocked degrade with a usage reason only; test_a_spent_budget_is_not_called_usage_pace now covers the risk source
## Lessons
- A shared reason string (degrade) is wrapped by callers; word the wrapper around what all its sources share, not the first source's name
## Plan gaps
- failed first: step 1 red: a spent risk budget's Stop drive text doesn't say usage is ahead of pace
## Files touched
- plugin/tests/test_risk.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/tests/test_perf_cost.py
- CHANGELOG.md
