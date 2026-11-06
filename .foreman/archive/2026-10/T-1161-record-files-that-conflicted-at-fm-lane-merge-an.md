---
id: T-1161
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:29:15Z
base: feeb84a4558ed993fa0d2e61628ad50eef4f825d
base_tree: 38802f16c0de7264132748152072879fc1500960
plan0_at: 2026-10-16T11:14:09Z
plan0_scope: []
verified: strong
---
# Record files that conflicted at `fm lane merge` and warn in `fm lane brief` when a new lan
## Raw request
> FEATURE: Record files that conflicted at `fm lane merge` and warn in `fm lane brief` when a new lane's scope includes a file that conflicted twice or more.
> DONE-WHEN: a test merges two conflicting lanes twice on one file and the next `fm lane brief` for a task scoped to that file prints the warning, and a task on another file prints none
## Interpretation
Files that keep conflicting when lanes merge are a scheduling hazard: record which files conflicted at each fm lane merge, and when a new lane's scope names a file that conflicted twice or more in the last 30 days, fm lane brief warns (merge this lane first or keep edits to that file small) and fm lane brief's JSON carries it.
## Assumptions (confidence)
## Acceptance criteria
- [x] after two recorded conflicts on one file, fm lane brief for a task scoped to that file prints the warning with the count; a task on another file prints none — verify with `python3 plugin/tests/run.py test_conflict_history`
## Non-goals
## Approach (options → choice → why)
Options: (a) a lane_conflict ledger event with the file list written where _conflict_brief runs (fmlanes.py ~638), counted per file over 30 days by the brief writer; (b) a separate conflicts.json store; (c) derive from git merge history. Choice: (a); why: the ledger is the event store and is already read by other reports; no new state file.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_conflict_history.py): two conflicting merges on one file then a brief warns; other file none; events older than 30 days ignored
2. [x] lane_conflict event at merge conflict; the warning in fm lane brief
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_conflict_history` → ✗ exit 1 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: ConflictHistory 1s) / FAILED (1 classes) [ran] [tree debb2ae4eb3a] (2026-10-16T11:14:41Z)
- (step 2) `python3 plugin/tests/run.py test_conflict_history` → exit 0 · Ran 2 tests in 3.5s (1 classes, 16 at a time; slowest: ConflictHistory 3s) / OK [ran] [tree 77c3518cba87] (2026-10-16T11:15:02Z)
- (step 2) `python3 plugin/tests/run.py test_conflict_history` → ✗ exit 1 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: ConflictHistory 2s) / FAILED (1 classes) [ran] [tree d41589f96254] (2026-10-16T11:21:49Z)
- (step 2) `python3 plugin/tests/run.py test_conflict_history` → exit 0 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: ConflictHistory 2s) / OK [ran] [tree c4f552686e9d] (2026-10-16T11:22:09Z)
- (ac 1) `python3 plugin/tests/run.py test_conflict_history test_lanes` → exit 0 · Ran 33 tests in 10.5s (6 classes, 16 at a time; slowest: Lanes 10s, ConflictHistory 2s, BoardLanes 1s) / OK [ran] [tree a9837e485ac4] (2026-10-16T11:27:41Z)
- (ac 1) `python3 plugin/tests/run.py test_conflict_history` → exit 0 · Ran 3 tests in 3.8s (1 classes, 16 at a time; slowest: ConflictHistory 4s) / OK [ran] [tree 0e423d80da78] (2026-10-16T11:27:55Z)
- (audit intent) `reviewer: one fm-reviewer pass found events counted not lanes (a retry or the task's own conflicts made a file hot), the event logged before merge --abort, and quoted non-ASCII paths; builder fixed all three (distinct tasks, own task skipped, log after abort reusing the one file list, -z)` → a lane that will collide with a hot file is told before it starts [tree 0e423d80da78] (2026-10-16T11:27:55Z)
- (audit adversary) `reviewer: one fm-reviewer pass found events counted not lanes (a retry or the task's own conflicts made a file hot), the event logged before merge --abort, and quoted non-ASCII paths; builder fixed all three (distinct tasks, own task skipped, log after abort reusing the one file list, -z)` → file names come from git and are redacted by log_event, capped at 50 [tree 0e423d80da78] (2026-10-16T11:27:55Z)
- (audit edge) `reviewer: one fm-reviewer pass found events counted not lanes (a retry or the task's own conflicts made a file hot), the event logged before merge --abort, and quoted non-ASCII paths; builder fixed all three (distinct tasks, own task skipped, log after abort reusing the one file list, -z)` → one lane twice = no warning; events older than 30 days ignored; directory scopes match via glob_match [tree 0e423d80da78] (2026-10-16T11:27:55Z)
- (audit operator) `reviewer: one fm-reviewer pass found events counted not lanes (a retry or the task's own conflicts made a file hot), the event logged before merge --abort, and quoted non-ASCII paths; builder fixed all three (distinct tasks, own task skipped, log after abort reusing the one file list, -z)` → one warning line per hot file with counts [tree 0e423d80da78] (2026-10-16T11:27:55Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found events counted not lanes (a retry or the task's own conflicts made a file hot), the event logged before merge --abort, and quoted non-ASCII paths; builder fixed all three (distinct tasks, own task skipped, log after abort reusing the one file list, -z)` → _conflict_brief takes the file list; git runs once [tree 0e423d80da78] (2026-10-16T11:27:55Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:14:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1161.builder.md
- 2026-10-16T11:14:09Z focused
- 2026-10-16T11:27:26Z merged worktree-agent-aa99a453ef3c30c26 (2 file(s))
- 2026-10-16T11:27:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa99a453ef3c30c26
- 2026-10-16T11:27:30Z focused
- 2026-10-16T11:27:51Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T11:29:13Z done
- 2026-10-16T11:29:15Z committed 611d33d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- research brainstorm-20261016-round2: Format per cluster: ideas, grounding (code or fm command), Status (queued / done / partial / new / false), Score (value 1-5, effort …
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Lessons
- count distinct actors, not events, when an event can repeat for one actor
## Plan gaps
- failed first: step 1 Failing tests (test_conflict_history.py): two conflicting merges on one file then a brief warns; ot…
## Files touched
- plugin/tests/test_conflict_history.py
- plugin/lib/fmlanes.py
- MASTER.md
- CHANGELOG.md
