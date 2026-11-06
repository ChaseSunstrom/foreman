---
id: T-2259
type: FEATURE
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: self
created: 2026-10-31T03:42:40Z
updated: 2026-10-31T05:59:23Z
base: 85b3b64012d0ccdf216d89b61ac0544272171863
base_tree: ed73bb9d327fb79cc9e50c63229155282643bc12
plan0_at: 2026-10-31T05:54:39Z
plan0_scope: []
verified: strong
---
# Builders write scratch files with cat > /tmp/claude-… heredocs and get 'isolated in the…
## Raw request
> Builders write scratch files with cat > /tmp/claude-… heredocs and get 'isolated in the worktree' refusals (30x in the digest; fm-builder.md:34-44 forbids it in prose only): a PreToolUse nudge in a lane naming the scratchpad write and the Write tool
## Interpretation
fm-builder.md tells builders to write an fm edit batch to a file but never says where, so they pick /tmp or the main thread's scratchpad, which worktree isolation refuses (15x in the last window): the missing piece is a writable place, named.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm-builder.md names .fm-scratch/ in the worktree as where scratch files and fm edit batches go, and .gitignore ignores .fm-scratch/ — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
1) name a git-ignored scratch folder inside the worktree (.fm-scratch/) in fm-builder.md wherever it says to write a file, and ignore it in .gitignore so a builder's commit never carries it. 2) a PreToolUse deny for /tmp writes from a lane — rejected: another refusal, same count. 3) more prose about /tmp — rejected: the prose is there and doesn't work without a place to go. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_docs; fm-builder.md and .gitignore; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_docs` → ✗ exit 1 · Ran 64 tests in 18.256s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 784e4c756e8a] (2026-10-31T05:56:14Z)
- `cd plugin/tests && python3 -m unittest -q test_docs` → exit 0 · Ran 64 tests in 12.917s / OK [ran] [tree 784e4c756e8a] (2026-10-31T05:56:14Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 83 tests in 10.6s (22 classes, 16 at a time; slowest: Fences 10s, TaskLifecycle 3s, Site 2s) / OK [ran] [tree 784e4c756e8a] (2026-10-31T05:56:25Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 83 tests in 14.8s (22 classes, 16 at a time; slowest: Fences 14s, TaskLifecycle 4s, Site 3s) / OK [ran] [tree 38405beaf14b] (2026-10-31T05:56:41Z)
- (audit intent) `self: the builder contract named a batch file with no place; it now names .fm-scratch/ in the worktree, git-ignored so it never lands in a commit` → removes the cause of the 15 refusals a window (builders choosing /tmp) rather than adding another refusal (test_docs red-to-green) [tree 38405beaf14b] (2026-10-31T05:56:41Z)
- (audit edge) `self: the builder contract named a batch file with no place; it now names .fm-scratch/ in the worktree, git-ignored so it never lands in a commit` → .fm-scratch/ is ignored at the repo root, so a lane's merge never carries scratch files [tree 38405beaf14b] (2026-10-31T05:56:41Z)
- (audit self) `self: the builder contract named a batch file with no place; it now names .fm-scratch/ in the worktree, git-ignored so it never lands in a commit` → no findings [tree 38405beaf14b] (2026-10-31T05:56:41Z)
## Log
- 2026-10-31T03:42:40Z created
- 2026-10-31T05:53:58Z set priority=urgent
- 2026-10-31T05:54:36Z set tier=S
- 2026-10-31T05:54:37Z planned: it has criteria and steps
- 2026-10-31T05:54:38Z focused
- 2026-10-31T05:56:25Z scope: plugin/agents/fm-builder.md, .gitignore, plugin/tests/test_docs.py, CHANGELOG.md
- 2026-10-31T05:59:16Z done
- 2026-10-31T05:59:23Z committed e39b5cf9 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research rsi-20261009-review: 1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- An instruction to write a file must name where; left open, an isolated agent picks /tmp
## Files touched
- plugin/tests/test_docs.py
- plugin/agents/fm-builder.md
- .gitignore
- CHANGELOG.md
