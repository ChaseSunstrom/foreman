---
id: T-0898
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T17:06:21Z
base: 45c5d5fd1b64f1a5fa86e2c35977377ea5d297cd
base_tree: 5dfeac6e2ecb0e7a0c6879cdfa8c08be4a1a0f67
verified: strong
---
# Fm at REF|ID -- CMD runs a command as of a commit or a task's start tree in a throwaway wo
## Raw request
> FEATURE: fm at REF|ID -- CMD runs a command as of a commit or a task's start tree in a throwaway worktree
> CONTEXT: round 6 #47. fmcli._run_at exists (bisect, prove use it)
## Interpretation
fm at TARGET -- CMD runs CMD in a throwaway worktree of TARGET: a task id (its start snapshot, uncommitted work included) or any git revision, and prints the result and exits with CMD's code. 'Did this pass before the task?' without stashing or checking anything out.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm at runs a command as of a commit and as of a task's start, leaving the working tree alone — verify with `python3 plugin/tests/run.py test_snapshots`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then cmd_at over _run_at
## Resume here
## Docs impact
MASTER time travel; CHANGELOG security line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_snapshots test_help test_docs` → exit 0 · Ran 144 tests in 4.9s (56 classes, 16 at a time; slowest: GuardAgainstBash 5s, Snapshots 3s, Hook 2s) / OK [ran] [tree 2daaa7f405d6] (2026-10-15T17:04:06Z)
- `python3 plugin/tests/run.py test_guard test_snapshots` → ✗ exit 1 · Ran 109 tests in 4.9s (44 classes, 16 at a time; slowest: GuardAgainstBash 5s, Snapshots 3s, Hook 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 2daaa7f405d6] (2026-10-15T17:04:16Z)
- `python3 plugin/tests/run.py test_guard test_snapshots` → exit 0 · Ran 109 tests in 4.6s (44 classes, 16 at a time; slowest: GuardAgainstBash 4s, Snapshots 3s, Hook 2s) / OK [ran] [tree 2daaa7f405d6] (2026-10-15T17:04:16Z)
- (ac 1) `python3 plugin/tests/run.py test_snapshots` → exit 0 · Ran 8 tests in 2.6s (1 classes, 16 at a time; slowest: Snapshots 2s) / OK [ran] [tree 2daaa7f405d6] (2026-10-15T17:06:20Z)
- (audit adversary) `self review: fm at resolves a task id to its start point (task_base) or a revision to a commit, runs in _run_at's throwaway worktree, exits with the command's code; while building it the guard was found never to read fm quiet's command — both are now checked as typed` → fm quiet -- rm -rf ~ passed the guard before this (verified with fmguard.check); now quiet's and at's trailing words (after --, options skipped, or the one-string form) go through check_bash; table rows cover rm-outside and publish for both, and plain test commands stay allowed; fm replay: 0 newly allowed over 3444 commands [tree 2daaa7f405d6] (2026-10-15T17:06:20Z)
- (audit edge) `self review: fm at resolves a task id to its start point (task_base) or a revision to a commit, runs in _run_at's throwaway worktree, exits with the command's code; while building it the guard was found never to read fm quiet's command — both are now checked as typed` → an unknown ref or an unfocused task is a usage error; one word is a shell string, several are argv quoted as given (as fm quiet runs them); relative paths in fm at are judged from the session's folder (stricter than the worktree it runs in) [tree 2daaa7f405d6] (2026-10-15T17:06:20Z)
- (audit self) `self review: fm at resolves a task id to its start point (task_base) or a revision to a commit, runs in _run_at's throwaway worktree, exits with the command's code; while building it the guard was found never to read fm quiet's command — both are now checked as typed` → no findings [tree 2daaa7f405d6] (2026-10-15T17:06:20Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T17:02:24Z focused
- 2026-10-15T17:02:32Z criterion 1 verify: `python3 plugin/tests/run.py test_round_i` → `python3 plugin/tests/run.py test_snapshots`
- 2026-10-15T17:03:20Z found: the guard never read the command inside fm quiet (fm quiet -- rm -rf ~ passed); fm at had the same shape. Fixed both here: the inner command gets the checks a typed one would
- 2026-10-15T17:06:21Z done
- 2026-10-15T17:06:21Z committed b784397 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0884 [FEATURE M, done, 3 steps] Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout -- — lesson: A hook that does real work before …
- research T-0224-review-1: Verdict: changes needed [stale: plugin/hooks/hooks.json, plugin/lib/fmbench.py, plugin/lib/fmevolve.py changed since it was written]
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar past tasks were M: consider --tier M
## Files touched
- plugin/tests/test_snapshots.py
- plugin/lib/fmcli.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
