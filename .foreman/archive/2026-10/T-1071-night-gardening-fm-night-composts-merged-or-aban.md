---
id: T-1071
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/lib/fmtidy.py, plugin/lib/fmlanes.py, plugin/tests/test_night.py, plugin/tests/test_recall.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T08:10:50Z
base: 0bb60d76f36b7a1cb04a1f6ef36ba4788fa654a4
base_tree: fa310a7b95d05591fe4a0efe76090cba7d912a45
plan0_at: 2026-10-16T07:52:29Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_night.py, plugin/tests/test_recall.py]
verified: strong
---
# Night gardening: fm night composts merged or abandoned worktrees and branches and consolid
## Raw request
> FEATURE: Night gardening: fm night composts merged or abandoned worktrees and branches and consolidates the week's lessons into fewer, stronger ones (wild C14)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm night` gains two free jobs: "compost" and "consolidate". Compost removes worktrees and branches left by closed tasks (merged, or dropped, since an abandoned lane is also a closed task). Consolidate merges near-duplicate lessons into fewer, stronger ones and writes the result as a captured task or research note, with the user deciding. Already covered by existing code: - Dream (the day's failures as tripwire candidates): fmnight.py:53. - Cold files and standing orders: fmnight.py:54, fmnight.py:135. - Merged-lane cleanup: `fmlanes.stale` (fmlanes.py:380), which `fm tidy --apply` runs. It never discards unmerged work. - Lesson retirement: `fm recall --lessons --retire` (fmrecall.py:548).
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm night --dry-run` lists compost and consolidate; `fm recall --lessons --consolidate` groups two near-identical lessons and names their ids — verify with `python3 plugin/tests/run.py test_night test_recall`
## Non-goals
## Approach (options → choice → why)
(a) A new gardener module. (b) Night calls `tidy --apply` for compost, and a new `recall --lessons --consolidate` for the merge proposal. (c) Only add the NAMES entries. Choose (b). It adds `("compost", ["tidy", "--apply"], 0.0)` and `("consolidate", ["recall", "--lessons", "--consolidate"], 0.0)` to `jobs()` (fmnight.py:48) and to NAMES (fmnight.py:24). `consolidate(p)` in fmrecall.py clusters live lessons by token Jaccard ≥ 0.6, and prints proposed merged text and the ids to retire. It never retires anything itself; with `--capture` it files a task.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: dry-run output contains "compost" and "consolidate". Two done tasks with near-identical Lessons give a group of 2 ids, and an unrelated lesson stays out. `--only compost` is accepted.
2. [x] Implement `consolidate` and the `--consolidate` flag in fmrecall.py and fmcli.py.
3. [x] Add the two jobs in fmnight.py.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night test_recall` → ✗ exit 1 · Ran 35 tests in 14.4s (15 classes, 16 at a time; slowest: Recall 14s, OtherProjects 5s, RedGreen 3s) / FAILED (2 classes) [ran] [tree 990ca14bfcc5] (2026-10-16T07:53:04Z)
- (step 2) `python3 plugin/tests/run.py test_night test_recall` → exit 0 · Ran 35 tests in 14.0s (15 classes, 16 at a time; slowest: Recall 14s, OtherProjects 5s, RedGreen 3s) / OK [ran] [tree 5ef07e00a5a4] (2026-10-16T07:53:50Z)
- (step 3) `python3 plugin/tests/run.py test_night test_recall` → exit 0 · Ran 35 tests in 14.7s (15 classes, 16 at a time; slowest: Recall 15s, OtherProjects 6s, RedGreen 3s) / OK [ran] [tree 5ef07e00a5a4] (2026-10-16T07:54:05Z)
- (step 1) `python3 plugin/tests/run.py test_night test_recall` → ✗ exit 1 · Ran 38 tests in 15.0s (15 classes, 16 at a time; slowest: Recall 15s, OtherProjects 6s, Consolidate 4s) / FAILED (2 classes) [ran] [tree c47139d6f1c3] (2026-10-16T08:00:29Z)
- (step 3) `python3 plugin/tests/run.py test_night test_recall` → exit 0 · Ran 38 tests in 27.0s (15 classes, 16 at a time; slowest: Recall 27s, OtherProjects 13s, Consolidate 8s) / OK [ran] [tree d02dc5b528cd] (2026-10-16T08:02:51Z)
- (step 1) `python3 plugin/tests/run.py test_night test_recall test_tidy test_lanes` → exit 0 · Ran 96 tests in 33.2s (31 classes, 16 at a time; slowest: Recall 33s, Lanes 25s, OtherProjects 15s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:09:46Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_recall` → exit 0 · Ran 38 tests in 15.4s (15 classes, 16 at a time; slowest: Recall 15s, OtherProjects 7s, Consolidate 4s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:10:03Z)
- (audit intent) `fm-reviewer (intent, adversary, edge): night compost ran all of tidy --apply (reopened blocked tasks, rewrote MEMORY.md, removed fixes, rolled the ledger) → tidy --lanes-only; an unmerged branch lost its lane_branch → kept; the night proposal was thrown away → --capture and a logged group count; --capture filed a new task each night → one open task; negated lessons grouped → same negation words required, keep <id> printed. All fixed on the builder's branch` → unattended gardening touches only closed lanes and proposes, never retires [tree acc2d51590ee] (2026-10-16T08:10:03Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge): night compost ran all of tidy --apply (reopened blocked tasks, rewrote MEMORY.md, removed fixes, rolled the ledger) → tidy --lanes-only; an unmerged branch lost its lane_branch → kept; the night proposal was thrown away → --capture and a logged group count; --capture filed a new task each night → one open task; negated lessons grouped → same negation words required, keep <id> printed. All fixed on the builder's branch` → no unattended write to MEMORY.md, fixes, ledger or blocked tasks (lanes-only path) [tree acc2d51590ee] (2026-10-16T08:10:03Z)
- (audit edge) `fm-reviewer (intent, adversary, edge): night compost ran all of tidy --apply (reopened blocked tasks, rewrote MEMORY.md, removed fixes, rolled the ledger) → tidy --lanes-only; an unmerged branch lost its lane_branch → kept; the night proposal was thrown away → --capture and a logged group count; --capture filed a new task each night → one open task; negated lessons grouped → same negation words required, keep <id> printed. All fixed on the builder's branch` → no lessons, a negated pair, a second capture, an unmerged branch [tree acc2d51590ee] (2026-10-16T08:10:03Z)
- (audit operator) `fm-reviewer (intent, adversary, edge): night compost ran all of tidy --apply (reopened blocked tasks, rewrote MEMORY.md, removed fixes, rolled the ledger) → tidy --lanes-only; an unmerged branch lost its lane_branch → kept; the night proposal was thrown away → --capture and a logged group count; --capture filed a new task each night → one open task; negated lessons grouped → same negation words required, keep <id> printed. All fixed on the builder's branch` → lessons_consolidate event with the group count; the night tail shows it [tree acc2d51590ee] (2026-10-16T08:10:03Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge): night compost ran all of tidy --apply (reopened blocked tasks, rewrote MEMORY.md, removed fixes, rolled the ledger) → tidy --lanes-only; an unmerged branch lost its lane_branch → kept; the night proposal was thrown away → --capture and a logged group count; --capture filed a new task each night → one open task; negated lessons grouped → same negation words required, keep <id> printed. All fixed on the builder's branch` → lanes-only reuses fmlanes.stale [tree acc2d51590ee] (2026-10-16T08:10:03Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:23:02Z set scope=['plugin/lib/fmnight.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_night.py', 'plugin/tests/test_recall.py']
- 2026-10-16T04:23:02Z set tier=M
- 2026-10-16T07:52:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1071.builder.md
- 2026-10-16T07:52:29Z focused
- 2026-10-16T08:01:37Z set scope=['plugin/lib/fmnight.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmtidy.py', 'plugin/lib/fmlanes.py', 'plugin/tests/test_night.py', 'plugin/tests/test_recall.py']
- 2026-10-16T08:04:01Z merged worktree-agent-af79438ba224b234e (7 file(s))
- 2026-10-16T08:04:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af79438ba224b234e
- 2026-10-16T08:09:12Z focused
- 2026-10-16T08:09:47Z scope: CHANGELOG.md and MASTER.md lines were committed with T-1047's close
- 2026-10-16T08:10:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_night.py, plugin/tests/test_recall.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmnight.py, plugin/lib/fmrecall.py, plugin/lib/fmtidy.py, plugin/tests/test_night.py, plugin/tests/test_recall.py; re-ground the plan against them before editing
## Lessons
- An unattended job runs the narrowest verb that does its job, never the broad one a person runs
## Plan gaps
- failed first: step 1 Failing tests: dry-run output contains "compost" and "consolidate". Two done tasks with near-identi…
## Files touched
- plugin/tests/test_recall.py
- plugin/tests/test_night.py
- plugin/lib/fmcli.py
- plugin/lib/fmnight.py
- plugin/lib/fmrecall.py
- plugin/lib/fmtidy.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
