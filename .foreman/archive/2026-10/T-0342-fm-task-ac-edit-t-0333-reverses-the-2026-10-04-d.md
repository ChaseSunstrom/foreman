---
id: T-0342
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T03:22:09Z
updated: 2026-10-06T03:23:33Z
base: 62505d72f1d0f254cf97770f7a6fe009caa898bc
base_tree: ab2a16632e48c2e19eb0c303a51d562fc53fd700
verified: strong
---
# fm task ac edit only before a criterion has evidence, with the change logged
## Raw request
> fm task ac edit (T-0333) reverses the 2026-10-04 decision to drop T-0305: an edit can weaken a failing criterion until it passes; allow edit only while the criterion has no evidence, and log old→new in the brief
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] editing a criterion that has evidence is refused (drop and recreate, as the T-0305 decision says) and an allowed edit logs old → new in the brief — verify with `python3 plugin/tests/run.py -k test_cli.EditCriterion`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] guard in edit_ac + log
## Resume here
## Docs impact
CHANGELOG; decisions.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cli.EditCriterion` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: EditCriterion 0s) / FAILED (1 classes) [ran] [tree c8f476d9daef] (2026-10-06T03:22:56Z)
- (step 1) `python3 plugin/tests/run.py -k test_cli.EditCriterion` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: EditCriterion 1s) / OK [ran] [tree dd7e0d1da862] (2026-10-06T03:23:18Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cli.EditCriterion` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: EditCriterion 1s) / OK [ran] [tree dd7e0d1da862] (2026-10-06T03:23:33Z)
- (step 2) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 75 tests in 14.6s (19 classes, 16 at a time; slowest: TaskLifecycle 15s, StateViews 5s, Checks 3s) / OK [ran] [tree dd7e0d1da862] (2026-10-06T03:23:33Z)
- (audit adversary) `self + adversary: edit refused once any evidence exists for the criterion (has_evidence(ac=n), the same test check_ac uses); every change logged old → new; refusal is a PolicyError (exit 2, 'refused')` → a failing criterion can't be weakened in place any more; the only path left (drop + recreate) leaves a dropped task with its reason in the history [tree dd7e0d1da862] (2026-10-06T03:23:33Z)
- (audit self) `self + adversary: edit refused once any evidence exists for the criterion (has_evidence(ac=n), the same test check_ac uses); every change logged old → new; refusal is a PolicyError (exit 2, 'refused')` → no findings [tree dd7e0d1da862] (2026-10-06T03:23:33Z)
## Log
- 2026-10-06T03:22:09Z created
- 2026-10-06T03:22:46Z planned from capture
- 2026-10-06T03:22:47Z focused
- 2026-10-06T03:23:33Z done
- 2026-10-06T03:23:33Z committed 6a160b3 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
## Lessons
- Before adding a command, grep decisions.md for it: this one had been deliberately dropped two days earlier, and the reason still applied in part.
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
