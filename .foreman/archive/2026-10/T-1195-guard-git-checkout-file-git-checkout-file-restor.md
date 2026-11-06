---
id: T-1195
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T13:28:35Z
updated: 2026-10-16T14:30:21Z
base: c7983ba2c526e6d1f670a348fd08a9e6b6a489d7
base_tree: 0e558ec12d233f8f31e17dd71db5a2bf4928b6d1
plan0_at: 2026-10-16T13:57:58Z
plan0_scope: []
verified: strong
---
# Guard: git checkout of named files is a write to those files, not the whole tree
## Raw request
> Guard: 'git checkout -- FILE' / 'git checkout FILE' restoring tracked files is refused as a tree write over the whole repo: when every argument after checkout (or after --) is an existing tracked path, judge it as writes to those files
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] git checkout -- FILE..., git checkout REV -- FILE... and git checkout FILE... (every word an existing path and no commit) are judged as writes to those files; git checkout BRANCH, checkout -b, checkout . and a word that is both a path and a commit stay whole-tree writes; the guard corpus and replay show no loosened verdict on protected files — verify with `python3 plugin/tests/run.py test_guard test_guard_cases test_replay`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing guard cases first: checkout -- a scoped file allowed in scope, checkout -- a protected file still refused, checkout main still a tree write
2. [x] In the guard's git write targets, checkout with -- or with only existing non-commit paths returns those paths
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 143 tests in 6.4s (53 classes, 16 at a time; slowest: GuardAgainstBash 6s, Replay 3s, GuardCases 3s) / OK [ran] [tree ff58003352fc] (2026-10-16T14:00:54Z)
- (step 2) `python3 plugin/bin/fm replay --cases` → exit 0 · Guard cases: 6 labelled, 0 drifted [ran] [tree ff58003352fc] (2026-10-16T14:00:54Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 177 tests in 7.6s (58 classes, 16 at a time; slowest: GuardAgainstBash 7s, GuardCases 4s, Hook 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a1b7dcca6d9e] (2026-10-16T14:28:23Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 177 tests in 7.3s (58 classes, 16 at a time; slowest: GuardAgainstBash 7s, GuardCases 4s, Hook 3s) / OK [ran] [tree a1b7dcca6d9e] (2026-10-16T14:28:23Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay test_guard_git` → exit 0 · Ran 184 tests in 21.2s (59 classes, 16 at a time; slowest: GuardAgainstBash 20s, GuardCases 7s, Hook 6s) / OK [ran] [tree a1b7dcca6d9e] (2026-10-16T14:28:51Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay test_guard_git` → exit 0 · Ran 184 tests in 13.3s (59 classes, 16 at a time; slowest: GuardAgainstBash 12s, GuardCases 7s, Hook 6s) / OK [ran] [tree a1b7dcca6d9e] (2026-10-16T14:29:05Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 184 tests in 6.8s (59 classes, 16 at a time; slowest: GuardAgainstBash 6s, GuardCases 4s, Replay 3s) / OK [ran] [tree a1b7dcca6d9e] (2026-10-16T14:29:19Z)
- `python3 plugin/tests/run.py test_guard test_guard_cases test_replay test_guard_git` → exit 0 · Ran 184 tests in 6.3s (59 classes, 16 at a time; slowest: GuardAgainstBash 6s, GuardCases 3s, Replay 3s) / OK [ran] [tree a1b7dcca6d9e] (2026-10-16T14:29:19Z)
- (audit adversary) `self review of the merged diff plus an automated security review; three bypass rounds closed: glob pathspecs, --pathspec-from-file (any --p prefix), global --icase/--glob-pathspecs and same-command GIT_ICASE/GLOB_PATHSPECS; directory pathspecs go through the tree-write check` → every way git widens a named path (globs, magic, pathspec files, icase and glob modes by flag or env) falls back to a whole-tree write; a protected file named directly is still refused; replay of 5000 real commands shows 0 newly allowed [tree a1b7dcca6d9e] (2026-10-16T14:29:19Z)
- (audit self) `self review of the merged diff plus an automated security review; three bypass rounds closed: glob pathspecs, --pathspec-from-file (any --p prefix), global --icase/--glob-pathspecs and same-command GIT_ICASE/GLOB_PATHSPECS; directory pathspecs go through the tree-write check` → no findings [tree a1b7dcca6d9e] (2026-10-16T14:29:19Z)
## Log
- 2026-10-16T13:28:35Z created
- 2026-10-16T13:57:35Z planned from capture
- 2026-10-16T13:57:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1195.builder.md
- 2026-10-16T13:57:57Z focused
- 2026-10-16T14:27:59Z merged worktree-agent-ac97fe0c1decb1990 (2 file(s))
- 2026-10-16T14:28:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac97fe0c1decb1990
- 2026-10-16T14:28:03Z focused
- 2026-10-16T14:29:06Z scope: CHANGELOG line
- 2026-10-16T14:30:19Z done
- 2026-10-16T14:30:21Z committed d5cdcd8e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- T-0377 [FIX S, done, 1 steps] fm lane merge ID merges a reviewed builder branch on Foreman's own repo; fm lane rm treats __pycache__ as disposable — lesson: A guard that…
- T-0859 [FIX S, done, 1 steps] Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 f
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–6 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
