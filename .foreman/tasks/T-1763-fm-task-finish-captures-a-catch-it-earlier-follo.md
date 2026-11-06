---
id: T-1763
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T08:14:25Z
updated: 2026-10-23T08:26:58Z
base: 34c9ef5c9c8651b7ae5a4bdd3445dbca96778f0e
base_tree: e112a9e6fda0b43305c6cb21d6434a9cccc1f971
plan0_at: 2026-10-23T08:25:35Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
verified: strong
---
# fm task finish captures a 'Catch it earlier' follow-up for a why-not-caught that says the work was new ('new playbook', 'n/a'), which has nothing to catch; skip those as it skips 'none'
## Raw request
> fm task finish captures a 'Catch it earlier' follow-up for a why-not-caught that says the work was new ('new playbook', 'n/a'), which has nothing to catch; skip those as it skips 'none'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a why-not-caught starting with none, new or n/a captures no follow-up, while a real cause still does — verify with `python3 plugin/tests/run.py test_diagnosis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test then widen the skip to none, new, n/a
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_diagnosis.NewWork` → ✗ exit 1 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: NewWork 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fda259c4f80c] (2026-10-23T08:25:40Z)
- `python3 plugin/tests/run.py test_diagnosis.NewWork` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: NewWork 1s) / FAILED (1 classes) [ran] [tree fda259c4f80c] (2026-10-23T08:25:40Z)
- `python3 plugin/tests/run.py test_diagnosis` → ✗ exit 1 · Ran 12 tests in 4.2s (7 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 26ab5fe09118] (2026-10-23T08:25:54Z)
- `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 12 tests in 3.6s (7 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 1s, NewWork 1s) / OK [ran] [tree 26ab5fe09118] (2026-10-23T08:25:54Z)
- (step 1) `python3 plugin/tests/run.py test_diagnosis test_cli` → exit 0 · Ran 128 tests in 24.4s (41 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree 26ab5fe09118] (2026-10-23T08:26:25Z)
- (audit intent) `self` → pass: new and n/a whys capture nothing; a real cause still does (WhyNotCaught test) [tree c64cc0dc42ac] (2026-10-23T08:26:26Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 12 tests in 3.6s (7 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / OK [ran] [tree c64cc0dc42ac] (2026-10-23T08:26:30Z)
- (audit intent) `self: intent, edge` → no noise follow-ups for new work [tree c64cc0dc42ac] (2026-10-23T08:26:30Z)
- (audit edge) `self: intent, edge` → matched as a whole word at the start, so 'newline handling was untested' still captures; case-insensitive [tree c64cc0dc42ac] (2026-10-23T08:26:30Z)
- (audit self) `self: intent, edge` → no findings [tree c64cc0dc42ac] (2026-10-23T08:26:30Z)
## Log
- 2026-10-23T08:14:25Z created
- 2026-10-23T08:14:31Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_followups.py', 'CHANGELOG.md']
- 2026-10-23T08:14:48Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_diagnosis.py', 'CHANGELOG.md']
- 2026-10-23T08:14:48Z criterion 1 verify: `python3 plugin/tests/run.py test_cli` → `python3 plugin/tests/run.py test_diagnosis`
- 2026-10-23T08:25:34Z focused
- 2026-10-23T08:26:56Z done
- 2026-10-23T08:26:58Z committed 78c0d6f7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1009 [FEATURE S, done, 3 steps] fm task finish --why-not-caught: no follow-up when the task's own edits already added the catching test
- T-1179 [FEATURE S, done, 2 steps] Catch it earlier: T-0787 ran test_workflows only; the doctor's file-map rule is checked by
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
the skip rule was written for 'none' only; nobody wrote 'new …' until three playbook tasks did
## Lessons
- A free-text field that drives an action needs its no-op phrases listed, not just one
## Files touched
- plugin/tests/test_diagnosis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
