---
id: T-0403
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:13:45Z
updated: 2026-10-09T04:16:16Z
base: 26e511c853f53b88688ab314ede8b43f0807392d
base_tree: c7eb46d24903891e167fdeb483e4130edbcb6247
verified: strong
---
# fm lane merge refuses any dirty main checkout; the main thread is mid-task while lanes finish (JARVIS: T-0280 couldn't land during T-0278) — merge when the dirty files don't overlap the branch and nothing is staged
## Raw request
> fm lane merge refuses any dirty main checkout; the main thread is mid-task while lanes finish (JARVIS: T-0280 couldn't land during T-0278) — merge when the dirty files don't overlap the branch and nothing is staged
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane merges over unrelated uncommitted edits and keeps them; an overlapping edit or a staged change is refused by name — verify with `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the overlap rule in fmlanes.merge
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Contract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d5a8e60fcd6a] (2026-10-09T04:14:31Z)
- `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Contract 1s) / FAILED (1 classes) [ran] [tree d5a8e60fcd6a] (2026-10-09T04:14:31Z)
- `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Contract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 982d0d3da3f6] (2026-10-09T04:14:51Z)
- `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 982d0d3da3f6] (2026-10-09T04:14:51Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.1    33.5     150  [0] / SessionEnd                  29.6    30.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 938 tests in [ran] [tree 518097e18b5f] (2026-10-09T04:16:14Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lane_merge_over_unrelated_uncommitted_work` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 518097e18b5f] (2026-10-09T04:16:16Z)
- (audit intent) `self: traced git's own rules (merge aborts on a dirty index; refuses edits it would overwrite); fm now refuses exactly those cases by name and lets unrelated edits through; abort stays safe without overlap` → a lane merges beside the main thread's uncommitted work, which survives (test) [tree 518097e18b5f] (2026-10-09T04:16:16Z)
- (audit edge) `self: traced git's own rules (merge aborts on a dirty index; refuses edits it would overwrite); fm now refuses exactly those cases by name and lets unrelated edits through; abort stays safe without overlap` → an edit to a file the branch changes → refused naming it; a staged change → refused; renames list both paths (-z parsing); untracked files are left to git, which refuses to overwrite them [tree 518097e18b5f] (2026-10-09T04:16:16Z)
- (audit adversary) `self: traced git's own rules (merge aborts on a dirty index; refuses edits it would overwrite); fm now refuses exactly those cases by name and lets unrelated edits through; abort stays safe without overlap` → every changed file still passes the guard as the task's write before the merge; only the dirty-tree precondition changed [tree 518097e18b5f] (2026-10-09T04:16:16Z)
- (audit self) `self: traced git's own rules (merge aborts on a dirty index; refuses edits it would overwrite); fm now refuses exactly those cases by name and lets unrelated edits through; abort stays safe without overlap` → no findings [tree 518097e18b5f] (2026-10-09T04:16:16Z)
## Log
- 2026-10-09T04:13:45Z created
- 2026-10-09T04:13:45Z focused
- 2026-10-09T04:16:16Z done
- 2026-10-09T04:16:16Z committed 7dcf1bf (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0167-review: Verdict:** changes needed. One HIGH finding (a hang) and two MEDIUM ones. I traced each finding below by reading the code. I did not run any of t…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- the similar finished task took 1 steps
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
