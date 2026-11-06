---
id: T-1890
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T01:19:05Z
updated: 2026-10-29T01:58:14Z
base: ce17e08bf99154097ec31b6c8fefda7be28c5d2f
base_tree: 8b7b96ac4254d7948c941a499baa189a821a4405
plan0_at: 2026-10-29T01:50:28Z
plan0_scope: [plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md]
verified: strong
---
# fm tidy's stale-plan check skips CHANGELOG.md in a plan's scope
## Raw request
> fm tidy's stale-plan check flags every queued plan whose scope lists CHANGELOG.md, since each finished task appends to it: 4 false re-plans this round. Skip append-only shared docs (CHANGELOG.md) there
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a plan scoped to CHANGELOG.md is not stale when only CHANGELOG.md moved; other scope files still flag — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: CHANGELOG.md newer than the plan flags nothing
2. [x] Skip CHANGELOG-named files in stale_plans
3. [x] CHANGELOG entry
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → red as expected (exit 1) · Ran 36 tests in 11.9s (13 classes, 16 at a time; slowest: DeferredTriage 11s, StalePlans 11s, DecisionSunset 10s) / FAILED (1 classes) [ran] [tree d3b09bd8ea8a] (2026-10-29T01:50:42Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 36 tests in 11.9s (13 classes, 16 at a time; slowest: StalePlans 11s, DeferredTriage 11s, DecisionSunset 9s) / OK [ran] [tree eaf966adab97] (2026-10-29T01:50:58Z)
- (step 3) `grep -c T-1890 CHANGELOG.md` → exit 0 · 1 [ran] [tree eaf966adab97] (2026-10-29T01:51:02Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmtidy.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.6    42.7     150  [0] / SessionEnd                  35.1    36.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree eaf966adab97] (2026-10-29T01:57:18Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 36 tests in 6.3s (13 classes, 16 at a time; slowest: StalePlans 6s, DeferredTriage 6s, DecisionSunset 5s) / OK [ran] [tree eaf966adab97] (2026-10-29T01:57:31Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → a queued plan scoped to CHANGELOG.md is no longer flagged for re-plan because another task appended to the changelog [tree eaf966adab97] (2026-10-29T01:57:31Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → only a file named exactly CHANGELOG.md is skipped; any other scope file that changes still flags (tested with a.py) [tree eaf966adab97] (2026-10-29T01:57:31Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → a plan whose only scope file is the changelog is never flagged; that is intended, since every closed task appends to it [tree eaf966adab97] (2026-10-29T01:57:31Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree eaf966adab97] (2026-10-29T01:57:31Z)
- `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 36 tests in 7.0s (13 classes, 16 at a time; slowest: DeferredTriage 6s, StalePlans 6s, DecisionSunset 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree eaf966adab97] (2026-10-29T01:58:04Z)
- `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 36 tests in 6.3s (13 classes, 16 at a time; slowest: DeferredTriage 6s, StalePlans 6s, DecisionSunset 5s) / OK [ran] [tree eaf966adab97] (2026-10-29T01:58:04Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → a queued plan scoped to CHANGELOG.md is no longer flagged for re-plan because another task appended to the changelog [tree eaf966adab97] (2026-10-29T01:58:05Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → only a file named exactly CHANGELOG.md is skipped; any other scope file that changes still flags (tested with a.py) [tree eaf966adab97] (2026-10-29T01:58:05Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → a plan whose only scope file is the changelog is never flagged; that is intended, since every closed task appends to it [tree eaf966adab97] (2026-10-29T01:58:05Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree eaf966adab97] (2026-10-29T01:58:05Z)
## Log
- 2026-10-29T01:19:05Z created
- 2026-10-29T01:19:23Z planned from capture
- 2026-10-29T01:50:27Z focused
- 2026-10-29T01:58:13Z done
- 2026-10-29T01:58:14Z committed fbe7d26a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- research wave1-plan-ac858e27ec64c546f: === T-1077 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- research T-1077-review: Verdict: approve with nits** (one MEDIUM to fix before merge). [stale: plugin/lib/fmtidy.py changed since it was written]
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_tidy.py
## Lessons
- A file every task touches is no signal that a plan went stale
## Files touched
- plugin/tests/test_tidy.py
- CHANGELOG.md
- plugin/lib/fmtidy.py
