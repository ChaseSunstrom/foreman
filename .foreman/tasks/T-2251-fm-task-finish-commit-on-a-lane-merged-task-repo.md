---
id: T-2251
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T01:28:48Z
updated: 2026-10-31T01:55:35Z
base: 71c3ca59afed29778d0292a9c7632aab6f8af674
base_tree: 16aeb17995f03830ad5de93ac1e3801614b447fc
plan0_at: 2026-10-31T01:39:29Z
plan0_scope: []
verified: strong
---
# fm task finish counts the docs it names as the task's own files
## Raw request
> fm task finish --commit on a lane-merged task reports the merge commit as Landed and leaves the task's later uncommitted doc edits (CHANGELOG.md for T-2132) out of the commit
## Interpretation
T-2132's finish left CHANGELOG.md uncommitted and said Landed: committed <merge sha>. _theirs() treats a file only another task touched as that task's; my shell edit made no touched record, and _claimed() reads only scope globs and 'scope:' log paths, never the docs the finish names.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file the finish's --docs (or the Docs impact section) names, edited by a shell command after another task touched it, is committed with the task and Landed reports it, instead of being left uncommitted as the other task's — verify with `cd plugin/tests && python3 -m unittest -q test_execution`
## Non-goals
## Approach (options → choice → why)
Options: (1) _claimed also takes existing file paths named in --docs and the Docs impact section (chosen: the task said they're its docs); (2) record touched for shell writes (the guard can't see every write); (3) commit every dirty file (takes other tasks' work). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: task A edits CHANGELOG.md and closes; task B appends to it by a shell write (no touched record) and finishes with --docs CHANGELOG.md --commit: the commit holds it and Landed says committed
2. [x] _claimed reads existing paths named in --docs and Docs impact; _landed agrees
3. [x] docs (MASTER fmcli line, CHANGELOG)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_execution 2>&1 | tail -15` → ✗ exit 1 · Ran 16 tests in 5.682s / FAILED (errors=2) [ran] [tree 9949ab2ac8e8] (2026-10-31T01:43:57Z)
- `cd plugin/tests && python3 -m unittest -q test_execution` → ✗ exit 1 · Ran 18 tests in 12.212s / FAILED (failures=1, errors=4) (start tree + this task's tests) [ran] [tree 12e58bf74a72] (2026-10-31T01:53:52Z)
- `cd plugin/tests && python3 -m unittest -q test_execution` → exit 0 · Ran 18 tests in 10.635s / OK [ran] [tree 12e58bf74a72] (2026-10-31T01:53:52Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_execution test_ledger_chain test_settings_power` → exit 0 · Ran 85 tests in 16.114s / OK [ran] [tree 12e58bf74a72] (2026-10-31T01:54:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_execution test_ledger_chain test_settings_power` → exit 0 · Ran 85 tests in 16.064s / OK [ran] [tree 12e58bf74a72] (2026-10-31T01:54:40Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_execution test_ledger_chain test_settings_power` → exit 0 · Ran 85 tests in 15.987s / OK [ran] [tree 12e58bf74a72] (2026-10-31T01:54:56Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_execution` → exit 0 · Ran 18 tests in 6.027s / OK [ran] [tree 12e58bf74a72] (2026-10-31T01:55:02Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer: approve with nits, fixed in 82cb406c: a named doc is claimed only when every other task that touched it is closed (an open task's half-done hunks stay out), tokens split on punctuation and markdown with leading dots kept, normpath, no absolute, .. or .foreman/ paths, a 'none' docs impact claims nothing; tests for each; test_execution test_ledger_chain test_settings_power 85 green, red-to-green proven` → a doc the finish names is committed with the task and Landed agrees [tree 12e58bf74a72] (2026-10-31T01:55:02Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer: approve with nits, fixed in 82cb406c: a named doc is claimed only when every other task that touched it is closed (an open task's half-done hunks stay out), tokens split on punctuation and markdown with leading dots kept, normpath, no absolute, .. or .foreman/ paths, a 'none' docs impact claims nothing; tests for each; test_execution test_ledger_chain test_settings_power 85 green, red-to-green proven` → an open task's in-progress edit to a shared doc is never swept into this task's commit; state paths are never claimed [tree 12e58bf74a72] (2026-10-31T01:55:02Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer: approve with nits, fixed in 82cb406c: a named doc is claimed only when every other task that touched it is closed (an open task's half-done hunks stay out), tokens split on punctuation and markdown with leading dots kept, normpath, no absolute, .. or .foreman/ paths, a 'none' docs impact claims nothing; tests for each; test_execution test_ledger_chain test_settings_power 85 green, red-to-green proven` → ./CHANGELOG.md, .github/x.yml, backticks, parentheses, 'none: README.md untouched' all tested [tree 12e58bf74a72] (2026-10-31T01:55:02Z)
- (audit maintainer) `fm-reviewer intent+adversary+edge+maintainer: approve with nits, fixed in 82cb406c: a named doc is claimed only when every other task that touched it is closed (an open task's half-done hunks stay out), tokens split on punctuation and markdown with leading dots kept, normpath, no absolute, .. or .foreman/ paths, a 'none' docs impact claims nothing; tests for each; test_execution test_ledger_chain test_settings_power 85 green, red-to-green proven` → one _closed rule shared by the docs and scope: claim paths; find_brief re-read per call is a few ms, kept [tree 12e58bf74a72] (2026-10-31T01:55:02Z)
## Log
- 2026-10-31T01:28:48Z created
- 2026-10-31T01:38:47Z planned from capture
- 2026-10-31T01:38:48Z set approved=True
- 2026-10-31T01:38:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2251.builder.md
- 2026-10-31T01:39:28Z focused
- 2026-10-31T01:53:27Z merged worktree-agent-ae5dfaa2dee05602c (3 file(s))
- 2026-10-31T01:53:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae5dfaa2dee05602c
- 2026-10-31T01:53:27Z focused
- 2026-10-31T01:54:56Z scope: plugin/lib/fmcli.py (_claimed, _closed, _theirs), plugin/tests/test_execution.py, CHANGELOG.md
- 2026-10-31T01:55:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1169 [FEATURE M, done, 2 steps] At close, name files that were already dirty when the task was focused and that the task a — lesson: store lists as JSON, never in the …
- T-1122 [FIX S, done, 1 steps] Fm task finish --commit leaves out files the task changed through Bash (a python or heredo — lesson: A hook record written after the comman…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Why not caught
no test covered a finish whose doc another task touched first; the Landed test only had one task
## Lessons
- A file-ownership rule that infers from edit records needs the task's own declarations as an input, gated on the other owners being done
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
- CHANGELOG.md
