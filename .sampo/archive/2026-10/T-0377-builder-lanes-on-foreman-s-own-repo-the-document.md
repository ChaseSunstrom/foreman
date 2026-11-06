---
id: T-0377
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_builder.py, plugin/skills/intake/references/delegate.md, CHANGELOG.md, .claude/worktrees/**]
depends_on: []
source: discovered
created: 2026-10-09T00:30:56Z
updated: 2026-10-09T00:41:25Z
base: 8734dbf478da009577bc2c9c00929bcda5af9f9e
base_tree: f66bcdceba70c58af0416945ed8a1de5b7bb1e68
verified: strong
---
# fm lane merge ID merges a reviewed builder branch on Foreman's own repo; fm lane rm treats __pycache__ as disposable
## Raw request
> Builder lanes on Foreman's own repo: the documented 'git merge --no-ff <branch>' (delegate.md step 3) is refused by the guard (core: a tree write over ~/.claude/foreman), so a builder's commit has to be re-applied by hand; let fm lane merge ID do the merge itself after the review (fm-mediated, like fm task finish --commit)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane whose only ignored files are __pycache__ is removed, and fm lane merge ID merges its branch with --no-ff — verify with `python3 plugin/tests/run.py -k test_lane_merge_and_cache_only_removal`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: lane rm ignores __pycache__; fm lane merge
## Resume here
<!-- auto -->
- 2026-10-09T00:32:48Z step 1/1: test-first: lane rm ignores __pycache__; fm lane merge
- git: foreman/build; 2 uncommitted: plugin/lib/fmlanes.py, plugin/tests/test_builder.py
## Docs impact
CHANGELOG.md; plugin/skills/intake/references/delegate.md step 3
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_lane_merge_and_cache_only_removal` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 6db7b2e5b4b6] (2026-10-09T00:40:37Z)
- (step 1) `python3 plugin/tests/run.py -k test_lane_merge_and_cache_only_removal` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 6db7b2e5b4b6] (2026-10-09T00:40:37Z)
- (audit adversary) `self + adversary: fm lane merge judges every changed file with fmguard.check as the task's own Write (its allow, standing, trust), refuses a dirty checkout, aborts a conflicted merge; fm lane rm skips only __pycache__/ and .pyc/.pyo` → a branch that touches a credentials or core file without the grant is refused (tested); deletions are judged as writes too [tree 6db7b2e5b4b6] (2026-10-09T00:40:37Z)
- (audit self) `self + adversary: fm lane merge judges every changed file with fmguard.check as the task's own Write (its allow, standing, trust), refuses a dirty checkout, aborts a conflicted merge; fm lane rm skips only __pycache__/ and .pyc/.pyo` → no findings [tree 6db7b2e5b4b6] (2026-10-09T00:40:37Z)
- `python3 plugin/tests/run.py -k test_lane_merge_and_cache_only_removal` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Contract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6db7b2e5b4b6] (2026-10-09T00:41:09Z)
- `python3 plugin/tests/run.py -k test_lane_merge_and_cache_only_removal` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 6db7b2e5b4b6] (2026-10-09T00:41:09Z)
- (audit adversary) `self + adversary: fm lane merge judges every changed file with fmguard.check as the task's own Write (its allow, standing, trust), refuses a dirty checkout, aborts a conflicted merge; fm lane rm skips only __pycache__/ and .pyc/.pyo` → a branch that touches a credentials or core file without the grant is refused (tested); deletions are judged as writes too [tree 6db7b2e5b4b6] (2026-10-09T00:41:24Z)
- (audit self) `self + adversary: fm lane merge judges every changed file with fmguard.check as the task's own Write (its allow, standing, trust), refuses a dirty checkout, aborts a conflicted merge; fm lane rm skips only __pycache__/ and .pyc/.pyo` → no findings [tree 6db7b2e5b4b6] (2026-10-09T00:41:24Z)
## Log
- 2026-10-09T00:30:56Z created
- 2026-10-09T00:31:27Z planned from capture
- 2026-10-09T00:31:27Z focused
- 2026-10-09T00:32:48Z paused: focus moved to T-0378
- 2026-10-09T00:39:20Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T00:39:20Z focused
- 2026-10-09T00:41:24Z done
- 2026-10-09T00:41:25Z committed 117cf5f (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0234 [FEATURE L, done, 4 steps] Implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash) — lesson: A contract a subagent must keep nee…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- A guard that refuses a tree-wide command needs an fm path that applies the same per-file judgement, or the documented workflow can't be followed
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- plugin/skills/intake/references/delegate.md
