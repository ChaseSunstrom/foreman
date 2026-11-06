---
id: T-3168
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T06:50:43Z
updated: 2026-11-05T11:24:20Z
builder_model: haiku
base: 8156d1f79fa74d7bf7fd74fbc5cd239ce388628b
base_tree: 1aa4dec9a3a5be467c60358bfdbb22a47f5d1843
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T09:56:39Z
plan0_scope: []
builder_returned: 2026-11-05T10:07:05Z
lane_stop: merged 2026-11-05T11:21:28Z
verified: strong
---
# sampo lane brief refuses a task whose work is already in main (its commits found by git log --grep ID on HEAD) and says to re-run its criteria and finish it
## Raw request
> sampo lane brief briefed T-3034 for a fresh builder although its work (7e06c53f, 37db4efa) was already merged into main and only its close was pending; lane brief should refuse a task whose commits (git log --grep the id) are already in main, and say 'merged: re-run its criteria and finish it'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] lane brief on a task with a commit naming its id already reachable from HEAD refuses with 'merged: re-run its criteria and finish it' and writes no brief; a task with no such commit briefs as before — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test then the refusal
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -15` → ✗ exit 1 · Ran 163 tests in 104.3s (14 classes, 16 at a time; slowest: Lanes 101s, LaneRecovery 73s, RaceEvidence 49s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree c62fb4ffa040] [world 2f1906870a] (2026-11-05T09:58:39Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 163 tests in 120.8s (14 classes, 16 at a time; slowest: Lanes 120s, LaneRecovery 69s, RaceEvidence 42s) / OK [ran] [tree 317577d5fbea] [world 2f1906870a] (2026-11-05T10:02:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_twins test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [22.25s] [ran] [tree 317577d5fbea] [world 2f1906870a] (2026-11-05T10:04:11Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 163 tests in 65.9s (14 classes, 16 at a time; slowest: Lanes 65s, LaneRecovery 52s, RaceEvidence 27s) / OK [ran] [tree 1381ce8e24f3] [world 2f1906870a] (2026-11-05T10:05:57Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_twins test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [18.41s] [ran] [tree 1381ce8e24f3] [world 2f1906870a] (2026-11-05T10:07:00Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 163 tests in 39.2s (14 classes, 16 at a time; slowest: Lanes 39s, LaneRecovery 39s, RaceEvidence 20s) / OK [ran] [tree 08df4c345a18] [world 2f1906870a] (2026-11-05T11:22:19Z)
- `python3 plugin/tests/run.py test_lanes.Lanes` → ✗ exit 1 · Ran 49 tests in 31.0s (1 classes, 16 at a time; slowest: Lanes 29s) / FAILED (1 classes: test_lanes.Lanes) (start tree + this task's tests) [ran] [tree 08df4c345a18] [world 2f1906870a] (2026-11-05T11:23:20Z)
- `python3 plugin/tests/run.py test_lanes.Lanes` → exit 0 · Ran 49 tests in 29.2s (1 classes, 16 at a time; slowest: Lanes 29s) / OK [ran] [tree 08df4c345a18] [world 2f1906870a] (2026-11-05T11:23:20Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T11:22:19Z [ran] [tree 08df4c345a18] [world 2f1906870a] (2026-11-05T11:23:26Z)
- (audit edge) `self: read the merged lanes.py check (git log --grep on HEAD for the task's own commits: subject 'ID' as the task, not part/follow-up/revert mentions; a later revert reopens) and its test; proved red on the start tree; test_lanes 163 green` → a task whose id only appears in another task's message ('after T-x', 'part of T-x') still briefs; a merged-then-reverted task briefs again; a repo with no commits briefs as before [tree 08df4c345a18] (2026-11-05T11:23:26Z)
- (audit self) `self: read the merged lanes.py check (git log --grep on HEAD for the task's own commits: subject 'ID' as the task, not part/follow-up/revert mentions; a later revert reopens) and its test; proved red on the start tree; test_lanes 163 green` → no findings [tree 08df4c345a18] (2026-11-05T11:23:26Z)
## Log
- 2026-11-05T06:50:43Z created
- 2026-11-05T09:55:52Z planned from capture
- 2026-11-05T09:55:55Z set approved=True
- 2026-11-05T09:55:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3168.builder.md
- 2026-11-05T09:56:37Z focused
- 2026-11-05T09:56:39Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:21:28Z merged worktree-agent-aa9777d4f4c715a18 (2 file(s))
- 2026-11-05T11:21:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa9777d4f4c715a18
- 2026-11-05T11:21:31Z focused
- 2026-11-05T11:24:17Z done
- 2026-11-05T11:24:20Z committed 738524a9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-02: [outward] Release 1.2.51 finished by hand after fm release refused a fresh run (version already bumped) and its checkpoints were abandoned: pushed t…
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
