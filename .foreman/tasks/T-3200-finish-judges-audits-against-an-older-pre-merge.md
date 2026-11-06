---
id: T-3200
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T12:27:26Z
updated: 2026-11-05T12:32:29Z
base: 3ce71d323dd672c97496ae701419c845839846f7
base_tree: 338b293aa4bee870f1a1cf3ee0125701e6528807
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T12:27:28Z
plan0_scope: []
verified: strong
unproven: [red]
---
# finish judges audits against an older pre-merge audit tree even when audits on the current tree exist, so a close spanning another lane's merge refuses a fresh adversary audit
## Raw request
> finish judges audits against an older pre-merge audit tree even when audits on the current tree exist, so a close spanning another lane's merge refuses a fresh adversary audit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] audit_tree_past_merges returns the current tree when any audit was recorded on it; an older audit tree is used only when none was — verify with `python3 plugin/tests/run.py test_lanes.Lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: audits on the current tree win over an older pre-merge audit tree
2. [x] the fix in core.audit_tree_past_merges
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_an_audit_on_the_current_tree_beats_an_older_pre_merge_one` → ✗ exit 1 · Ran 1 tests in 3.8s (1 jobs, 16 at a time; slowest: Lanes 3s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 6de0f956a3c7] [world 2f1906870a] (2026-11-05T12:28:00Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_audit test_finish` → ✗ exit 1 · Ran 243 tests in 61.0s (166 jobs, 16 at a time; slowest: Lanes 48s, ExamAuthors 12s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 12s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 8e874485d633] [world 2f1906870a] (2026-11-05T12:29:14Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_audit test_finish test_core` → exit 0 · Ran 384 tests in 42.9s (264 jobs, 16 at a time; slowest: ExamAuthors 13s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 12s, ProbeProvisional.test_revert_route_restores_the_deare [ran] [tree 675d0f009062] [world 2f1906870a] (2026-11-05T12:30:45Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_an_audit_on_the_current_tree_beats_an_older_pre_merge_one` → ✗ exit 1 · Ran 1 tests in 3.3s (1 jobs, 16 at a time; slowest: Lanes 2s) / FAILED (1 classes: test_lanes.Lanes) (start tree + this task's tests) [ran] [tree d4f8487c4396] [world 2f1906870a] (2026-11-05T12:30:58Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_an_audit_on_the_current_tree_beats_an_older_pre_merge_one` → exit 0 · Ran 1 tests in 1.9s (1 jobs, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree d4f8487c4396] [world 2f1906870a] (2026-11-05T12:30:58Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_merge` → ✗ exit 1 · run.py: no test matches test_audit_merge [ran] [tree d4f8487c4396] [world 2f1906870a] (2026-11-05T12:31:10Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.Lanes` → exit 0 · Ran 50 tests in 31.4s (1 jobs, 16 at a time; slowest: Lanes 31s) / OK [ran] [tree d4f8487c4396] [world 2f1906870a] (2026-11-05T12:31:53Z)
- (audit adversary) `read every caller: audit_tree_past_merges feeds only done_blockers/audit_blockers (cli done, _adversary_gaps, _finish_gaps); it now returns the set of trees an audit may have been made on (current + each audit tree that differs only by other lanes' merged files), and audit_blockers accepts one id or that set; None stays None` → the set only grows by trees whose git diff to the working files is entirely other tasks' merged files this task never touched (unchanged rule), so an audit made before this task's own later edits still goes stale; a git diff that fails (None) adds nothing, failing closed [tree d4f8487c4396] (2026-11-05T12:31:53Z)
- (audit edge) `read every caller: audit_tree_past_merges feeds only done_blockers/audit_blockers (cli done, _adversary_gaps, _finish_gaps); it now returns the set of trees an audit may have been made on (current + each audit tree that differs only by other lanes' merged files), and audit_blockers accepts one id or that set; None stays None` → a task with no merges gets {tree}, same as before; an M task's pre-merge intent/edge audits and a post-merge adversary audit now count together (the new test); tree None keeps the old evidence-tree fallback [tree d4f8487c4396] (2026-11-05T12:31:53Z)
- (audit self) `read every caller: audit_tree_past_merges feeds only done_blockers/audit_blockers (cli done, _adversary_gaps, _finish_gaps); it now returns the set of trees an audit may have been made on (current + each audit tree that differs only by other lanes' merged files), and audit_blockers accepts one id or that set; None stays None` → no findings [tree d4f8487c4396] (2026-11-05T12:31:53Z)
## Log
- 2026-11-05T12:27:26Z created
- 2026-11-05T12:27:27Z focused
- 2026-11-05T12:27:28Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T12:31:20Z criterion 1 verify: `python3 plugin/tests/run.py test_audit_merge` → `python3 plugin/tests/run.py test_lanes.Lanes`
- 2026-11-05T12:32:27Z done
- 2026-11-05T12:32:29Z committed 579d11c9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- decision 2026-10-31: Narrow the code freeze during the long-tier runs: lanes off the session path (T-2294 builder doc, T-2156 ci-watch, T-2279 doctor, T-2296 friction di…
## Lessons
- When several snapshots can each be valid, return the set and test membership; picking the newest acceptable one silently drops the others
## Plan gaps
- failed first: step 1 failing test: audits on the current tree win over an older pre-merge audit tree
- failed first: step 2 the fix in core.audit_tree_past_merges
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
