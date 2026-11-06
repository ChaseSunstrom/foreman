---
id: T-2037
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:01:20Z
updated: 2026-10-29T20:11:47Z
base: 00ec968b194ce60de6c4aa9a2b17c3440b3052bf
base_tree: 61ca3812dee90b3a44ce5e439382a456a31d933b
plan0_at: 2026-10-29T20:04:42Z
plan0_scope: []
verified: strong
---
# fm digest's survival line '24 survived, 45 lost, 1234 settling' reads as a 65% loss…
## Raw request
> CLEAN: fm digest's survival line '24 survived, 45 lost, 1234 settling' reads as a 65% loss rate: lost counts all closes (a hit can come mid-window) while survived counts only closes past 30 days; say 'of N closes, L lost (x%)' so the numbers compare
## Interpretation
survival_lines counts lost over every close (a loss can land mid-window) but survived only over closes past 30 days, so '24 survived, 45 lost' reads as a 65% loss rate when it is 45 of ~1300. Show the total and the lost share so the numbers compare.
## Assumptions (confidence)
## Acceptance criteria
- [x] The survival line gives the total and the lost share — verify with `python3 plugin/tests/run.py test_outcomes`
## Non-goals
## Approach (options → choice → why)
In fmoutcomes.survival_lines: 'Survival (30 days): of N closes, L lost (x%), S survived the window, T settling; days since…'. Update the tests that pin the old wording.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test the new wording first, then change survival_lines
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `python3 plugin/tests/run.py test_outcomes` → ✗ exit 1 · Ran 15 tests in 11.5s (9 classes, 16 at a time; slowest: Survival 10s, Reopen 2s, TrackRecord 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d83a1c454cc1] (2026-10-29T20:06:03Z)
- `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 15 tests in 10.7s (9 classes, 16 at a time; slowest: Survival 10s, Reopen 2s, TrackRecord 2s) / OK [ran] [tree d83a1c454cc1] (2026-10-29T20:06:03Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmoutcomes.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    31.3     150  [0] / SessionEnd                  26.2    28.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/forem [ran] [tree d83a1c454cc1] (2026-10-29T20:08:55Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 15 tests in 10.3s (9 classes, 16 at a time; slowest: Survival 10s, Reopen 2s, TrackRecord 2s) / OK [ran] [tree d83a1c454cc1] (2026-10-29T20:09:16Z)
- (audit intent) `self-review of the diff: one line in survival_lines; total = survived + lost + settling (unknown left out, as before); max(total,1) guards an empty set, which returns early anyway` → the line now reads 'of 1304 closes, 45 lost (3%)' instead of a 65%-looking ratio (fm digest checked live) [tree d83a1c454cc1] (2026-10-29T20:09:16Z)
- (audit edge) `self-review of the diff: one line in survival_lines; total = survived + lost + settling (unknown left out, as before); max(total,1) guards an empty set, which returns early anyway` → lost counted mid-window and survived only after it, so the share uses every close as the base [tree d83a1c454cc1] (2026-10-29T20:09:16Z)
- (audit self) `self-review of the diff: one line in survival_lines; total = survived + lost + settling (unknown left out, as before); max(total,1) guards an empty set, which returns early anyway` → no findings [tree d83a1c454cc1] (2026-10-29T20:09:16Z)
## Log
- 2026-10-29T20:01:20Z created
- 2026-10-29T20:01:35Z set type=CLEAN, tier=S
- 2026-10-29T20:01:37Z planned: it has criteria and steps
- 2026-10-29T20:04:42Z focused
- 2026-10-29T20:05:34Z set type=FIX
- 2026-10-29T20:05:34Z steer: retyped CLEAN -> FIX: it changes visible output on purpose, so a behaviour lock doesn't apply
- 2026-10-29T20:09:29Z done
- 2026-10-29T20:09:31Z committed bf08ca31 (3 files)
- 2026-10-29T20:09:36Z guard authorization added: publish
- 2026-10-29T20:11:47Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1060 [FEATURE L, done, 3 steps] Survival grading: fm outcomes grades each closed task by whether its change survived 30 da — lesson: A once-only marker kept in a rolli…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
- similar past tasks were L: consider --tier L
## Lessons
- Counts with different bases need the shared total beside them, or readers compare the wrong numbers
## Files touched
- plugin/tests/test_outcomes.py
- CHANGELOG.md
- plugin/lib/fmoutcomes.py
