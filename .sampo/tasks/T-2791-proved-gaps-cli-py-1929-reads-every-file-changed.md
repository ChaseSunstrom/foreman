---
id: T-2791
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_lanes.py, plugin/tests/test_finish_proved.py]
depends_on: []
source: self
created: 2026-11-03T05:48:54Z
updated: 2026-11-03T14:46:27Z
builder_model: sonnet
base: 5a819e659b16c906f85aa9b94499e9ba219069ba
base_tree: 43ad4698efa7e19e7f4e2b57827af96f03da03c1
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T05:49:23Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_lanes.py]
lane_stop: merged 2026-11-03T06:07:49Z
verified: strong
unproven: [meaning]
---
# A close is asked for a red→green proof only for .fmproved files the task itself changed: _proved_gaps subtracts the files other lanes' merges brought in (_theirs), as the scope and audit checks do since T-2784
## Raw request
> FIX: _proved_gaps (cli.py:1929) reads every file changed since the task's base, so a close is asked for a red→green proof for .fmproved files only another lane's merge changed (T-2758 was asked to prove rune.py, which T-2774's merge brought in); subtract _theirs(p, b, changed) as _task_files does since T-2784
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a FEATURE task focused before another task's lane merge that changed a .fmproved file closes without a proof gap for that file, and its own change to a .fmproved file still needs one — verify with `python3 plugin/tests/run.py test_lanes.Lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_lanes.Lanes next to T-2784's: .fmproved lists a file, another lane's merge changes it, the FEATURE task's finish names no proof gap; then subtract _theirs in _proved_gaps; run test_lanes
## Resume here
## Docs impact
none
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes` → exit 0 · Ran 44 tests in 112.7s (1 classes, 16 at a time; slowest: Lanes 112s) / OK [ran] [tree bd83673e2182] [world 2f1906870a] (2026-11-03T05:53:48Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_another_lanes_merge_of_a_proved_file_asks_no_proof` → ✗ exit 1 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: Lanes 1s) / FAILED (1 classes: test_lanes.Lanes) (start tree + this task's tests) [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:44:51Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_another_lanes_merge_of_a_proved_file_asks_no_proof` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:44:51Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.Lanes` → exit 0 · Ran 44 tests in 24.0s (1 classes, 16 at a time; slowest: Lanes 24s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:45:45Z)
- `python3 plugin/tests/run.py test_lanes test_finish_proved` → exit 0 · Ran 149 tests in 23.5s (14 classes, 16 at a time; slowest: Lanes 23s, LaneRecovery 22s, RaceEvidence 10s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:45:45Z)
- (audit intent) `self: read the diff; _proved_gaps subtracts _theirs; the unit helper in test_finish_proved stubs _theirs, which the full suite caught` → a close is asked for a proof only for .fmproved files it changed [tree 1b964dd8dbe8] (2026-11-03T14:45:45Z)
- (audit edge) `self: read the diff; _proved_gaps subtracts _theirs; the unit helper in test_finish_proved stubs _theirs, which the full suite caught` → a file both the merge and this task changed stays in the list (task_touches marks it ours); a bare project stub in a unit test needs _theirs stubbed [tree 1b964dd8dbe8] (2026-11-03T14:45:45Z)
- (audit adversary) `self: read the diff; _proved_gaps subtracts _theirs; the unit helper in test_finish_proved stubs _theirs, which the full suite caught` → same trust as T-2784's merged_in: a merge subject only another committer can forge [tree 1b964dd8dbe8] (2026-11-03T14:45:45Z)
- (audit self) `self: read the diff; _proved_gaps subtracts _theirs; the unit helper in test_finish_proved stubs _theirs, which the full suite caught` → no findings [tree 1b964dd8dbe8] (2026-11-03T14:45:45Z)
## Log
- 2026-11-03T05:48:54Z created
- 2026-11-03T05:49:08Z planned from capture
- 2026-11-03T05:49:08Z set approved=True
- 2026-11-03T05:49:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2791.builder.md
- 2026-11-03T05:49:22Z focused
- 2026-11-03T05:49:23Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T06:07:49Z merged worktree-agent-ac498c4ef978c0d34 (2 file(s))
- 2026-11-03T14:21:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac498c4ef978c0d34
- 2026-11-03T14:43:49Z focused
- 2026-11-03T14:43:55Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_finish_proved.py']
- 2026-11-03T14:43:55Z scope: plugin/tests/test_finish_proved.py — its unit helper passes a bare project stub that _theirs (now called by _proved_gaps) can't read; the helper stubs _theirs, as the merge path is test_lanes' to cover
- 2026-11-03T14:46:26Z done
- 2026-11-03T14:46:27Z committed b5fdc7dc (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, planned, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task'…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2768 [CLEAN M, planned, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/out…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/tests/test_lanes.py; re-ground the plan against them before editing
## Lessons
- Run the full suite before merging a change to a shared helper's callers: a unit test with a stub project broke only there
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_finish_proved.py
