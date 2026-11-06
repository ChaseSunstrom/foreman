---
id: T-0380
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_round_i.py]
depends_on: []
source: discovered
created: 2026-10-09T00:42:53Z
updated: 2026-10-09T00:47:49Z
base: 29f0c2149cd0ce03d004c68efe8d93a57f7d2c36
base_tree: 5af9996c2fbbd2a44e63b578834c77c7cabd6109
verified: strong
---
# fm task finish --commit reports the files the commit holds
## Raw request
> fm task finish --commit says 'committed <sha> (70 path(s))' when the commit changed 1 file: it counts the candidate paths, not what the commit holds; report git's own count
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a task whose touched file ended unchanged reports '1 file' for a 1-file commit — verify with `python3 plugin/tests/run.py -k test_finish_commit_counts_what_the_commit_holds`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: count from git
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_finish_commit_counts_what_the_commit_holds` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: RoundI 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 542addaa429b] (2026-10-09T00:47:48Z)
- `python3 plugin/tests/run.py -k test_finish_commit_counts_what_the_commit_holds` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: RoundI 0s) / OK [ran] [tree 542addaa429b] (2026-10-09T00:47:48Z)
- (ac 1) `python3 plugin/tests/run.py -k test_finish_commit_counts_what_the_commit_holds` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: RoundI 0s) / OK [ran] [tree 542addaa429b] (2026-10-09T00:47:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_finish_commit_counts_what_the_commit_holds` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: RoundI 0s) / OK [ran] [tree 542addaa429b] (2026-10-09T00:47:49Z)
- (audit self) `self: message only; the count comes from git show --name-only HEAD` → no findings [tree 542addaa429b] (2026-10-09T00:47:49Z)
## Log
- 2026-10-09T00:42:53Z created
- 2026-10-09T00:47:14Z planned from capture
- 2026-10-09T00:47:15Z focused
- 2026-10-09T00:47:49Z done
- 2026-10-09T00:47:49Z committed c60ba31 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0224-review-1: Verdict: changes needed [stale: plugin/hooks/hooks.json, plugin/lib/fmbench.py, plugin/lib/fmevolve.py changed since it was written]
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Lessons
- Report what happened (git's own count), not what was asked for (the candidate list)
## Files touched
- plugin/tests/test_round_i.py
- plugin/lib/fmcli.py
