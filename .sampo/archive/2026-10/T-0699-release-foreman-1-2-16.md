---
id: T-0699
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:08:03Z
updated: 2026-10-09T16:09:22Z
base: b70a350a3df4b9e3e023803324f6ec7eb054f70a
base_tree: e9e7aa423571ad48e525400d154d9c57c2fc62ea
verified: ok
---
# Release Foreman 1.2.16
## Raw request
> Release Foreman 1.2.16
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check passes on the release tree — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] trim the rules under the doctor budget, resync eval cases, bump versions and CHANGELOG heading
## Resume here
## Docs impact
CHANGELOG 1.2.16 heading
## Verification evidence
- (step 1) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 999 tests in 44.0s (247 classes, 16 at a time; slowest: Stop 34s, TaskLifecycle 23s, Parallel 21s) / OK (44.0 s) / ✓ fm replay → exit 0 · skipped: nothing [ran] [tree ec51c94c64a9] (2026-10-09T16:09:04Z)
- (ac 1) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 16:09 UTC); cached (fm check --fresh reruns) [ran] [tree ec51c94c64a9] (2026-10-09T16:09:18Z)
- (audit self) `self: fm check green on the release tree (999 tests, doctor 0 fail, replay 0 newly allowed); the two gate failures were the rules file 237 chars over the doctor budget and stale eval copies of the rules, fixed by trimming wording (no rule dropped) and sync_evals` → no findings [tree ec51c94c64a9] (2026-10-09T16:09:18Z)
- (audit self) `self: fm check green on the release tree (999 tests, doctor 0 fail, replay 0 newly allowed); the two gate failures were the rules file 237 chars over the doctor budget and stale eval copies of the rules, fixed by trimming wording (no rule dropped) and sync_evals` → no findings [tree ec51c94c64a9] (2026-10-09T16:09:22Z)
## Log
- 2026-10-09T16:08:03Z created
- 2026-10-09T16:08:03Z focused
- 2026-10-09T16:09:08Z paused: focus moved to T-0672
- 2026-10-09T16:09:17Z focused
- 2026-10-09T16:09:22Z done
- 2026-10-09T16:09:22Z committed ee170fd (3 files)
## Follow-ups captured
## Behaviour lock
none: a release changes only version strings, the CHANGELOG heading and the rules wording; the full gate run on the release tree is its check
## Lessons
- a rules edit must re-run sync_evals and the doctor footprint check in the same task
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
