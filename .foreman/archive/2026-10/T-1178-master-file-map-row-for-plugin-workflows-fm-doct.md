---
id: T-1178
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:18:55Z
updated: 2026-10-16T12:20:10Z
base: 25119f8b271d6a214572ac88fd05f02147b92a5c
base_tree: f6e9911c2918c902778ea7dd942dae7f670035d5
plan0_at: 2026-10-16T12:18:55Z
plan0_scope: []
verified: strong
---
# MASTER file map row for plugin/workflows (fm doctor fails release-check without it)
## Raw request
> MASTER file map row for plugin/workflows (fm doctor fails release-check without it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor's file map check passes and release-check's test passes — verify with `python3 plugin/tests/run.py -k test_release_check_runs_doctor_and_demo_in_a_temporary_home`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Add the row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_release_check_runs_doctor_and_demo_in_a_temporary_home` → exit 0 · Ran 1 tests in 11.0s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree fcd8e2163dc7] (2026-10-16T12:19:12Z)
- (ac 1) `python3 plugin/tests/run.py -k test_release_check_runs_doctor_and_demo_in_a_temporary_home` → exit 0 · Ran 1 tests in 9.5s (1 classes, 16 at a time; slowest: BoardVerbs 9s) / OK [ran] [tree fcd8e2163dc7] (2026-10-16T12:19:26Z)
- (audit edge) `self: fm doctor's file map check failed on the new plugin/workflows folder; one MASTER row` → the folder now has its row; doctor's check passes in release-check's temporary HOME [tree fcd8e2163dc7] (2026-10-16T12:19:26Z)
- (audit self) `self: fm doctor's file map check failed on the new plugin/workflows folder; one MASTER row` → no findings [tree fcd8e2163dc7] (2026-10-16T12:19:26Z)
- (audit edge) `self: fm doctor's file map check failed on the new plugin/workflows folder; one MASTER row` → the folder now has its row; doctor's check passes in release-check's temporary HOME [tree fcd8e2163dc7] (2026-10-16T12:19:50Z)
- (audit self) `self: fm doctor's file map check failed on the new plugin/workflows folder; one MASTER row` → no findings [tree fcd8e2163dc7] (2026-10-16T12:19:50Z)
## Log
- 2026-10-16T12:18:55Z created
- 2026-10-16T12:18:55Z focused
- 2026-10-16T12:20:09Z done
- 2026-10-16T12:20:10Z committed 7c9601da (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-0296 [FIX M, done, 3 steps] Session-review follow-ups: docs drift, doctor checks routing and scopes integrity, ignored flags refused, duel rivals m… — lesson: Never al…
- research T-0964-harness: 1) **What the harness is.** claude-code-harness is a plan, work, review loop run as skills (`/harness-plan`, `-work`, `-review`, `-sync`, `-rele…
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
## Why not caught
T-0787 ran test_workflows only; the doctor's file-map rule is checked by release-check in the full gates
## Regression test
none new: the existing test_board_verbs release-check test (fm doctor's file map rule) failed before the row (gate run of T-1173 and a rerun) and passes after; it is the regression test
## Files touched
- MASTER.md
