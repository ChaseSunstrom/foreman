---
id: T-1067
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_hunks.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T08:12:24Z
base: 7b38361e52f49fb7f4951c3903c60fcca1df2e8e
base_tree: acc2d51590eecaa65b5f81dbce0c83afc4780bd4
plan0_at: 2026-10-16T07:52:28Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_hunks.py]
verified: strong
---
# Diff ablation at close: for a task's change, revert each hunk in a scratch worktree and ru
## Raw request
> FEATURE: Diff ablation at close: for a task's change, revert each hunk in a scratch worktree and run the linked tests; a hunk whose revert no test notices is reported as untested (wild C11)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
At close, each hunk of the task's change is reverted in a scratch worktree and the linked tests are run; hunks no test notices are reported as untested (wild C11). Already built: `fm task prove ID --hunks --run CMD` does exactly this (`fmcli.py:1173-1236`, `task_prove_hunks`, tests in `test_hunks.py`). What's missing is the link at close: `--run` is manual, and nothing picks the linked tests or triggers it from `fm task finish`.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm task finish ID --ablate` reports "N/M hunks proven" and names an untested hunk — verify with `python3 plugin/tests/run.py test_hunks`
## Non-goals
## Approach (options → choice → why)
(a) new `--ablate` flag on `fm task finish` that builds the command from `affected(p)` (`fmcli.py:3485`) and calls `task_prove_hunks`; (b) a close warning telling the user to run prove --hunks; (c) always run it. Choose (a): it reuses both pieces, is opt-in (slow), and `affected` gives the linked tests (`fmmap.tests_for`).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: reuse `test_hunks._Case`'s repo and add a test that finish with `--ablate` and no `--run` still names the untested hunk, using the linked test command. Another test: no linked tests gives a one-line "no linked tests" and does not fail the close.
2. [x] In `task_finish` (`fmcli.py:805`), when `args.ablate`, set `args.run` from `affected(p)` (stop with UsageError if `cmd` is None), `args.hunks=True`, `max=20`, and call `task_prove_hunks`; print its summary into the finish output. Add the flag to the `finish` parser.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 8 tests in 1.9s (4 classes, 16 at a time; slowest: Hunks 2s, Ablate 1s, Evidence 1s) / OK [ran] [tree 7cf8852ed40e] (2026-10-16T07:55:06Z)
- (step 2) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 8 tests in 2.3s (4 classes, 16 at a time; slowest: Hunks 2s, Ablate 1s, Evidence 1s) / OK [ran] [tree 7cf8852ed40e] (2026-10-16T07:55:08Z)
- (step 2) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 12 tests in 7.6s (4 classes, 16 at a time; slowest: Ablate 7s, Hunks 5s, Evidence 3s) / OK [ran] [tree 662f4e05a473] (2026-10-16T08:02:19Z)
- (step 2) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 13 tests in 6.3s (4 classes, 16 at a time; slowest: Ablate 6s, Hunks 2s, Evidence 1s) / OK [ran] [tree c034b9e060a2] (2026-10-16T08:03:47Z)
- (step 1) `python3 plugin/tests/run.py test_hunks test_cli` → exit 0 · Ran 113 tests in 21.0s (32 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, Ablate 7s) / OK [ran] [tree e55c1bb9da7f] (2026-10-16T08:11:27Z)
- (ac 1) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 13 tests in 5.6s (4 classes, 16 at a time; slowest: Ablate 6s, Hunks 2s, Evidence 1s) / OK [ran] [tree b36127c8b345] (2026-10-16T08:11:44Z)
- (audit intent) `fm-reviewer (intent, adversary, edge): --ablate could fail the close (affected() and prove_hunks raise) → runs after the checks, any error prints 'ablation skipped'; no total bound → 600 s deadline, per-run timeout capped at the remainder; --json broken → folded into the finish JSON; a permanent inconclusive evidence line → none recorded. Ablation runs in a detached scratch worktree with finally cleanup; the stored command goes through guard_stored` → names hunks no linked test notices [tree b36127c8b345] (2026-10-16T08:11:44Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge): --ablate could fail the close (affected() and prove_hunks raise) → runs after the checks, any error prints 'ablation skipped'; no total bound → 600 s deadline, per-run timeout capped at the remainder; --json broken → folded into the finish JSON; a permanent inconclusive evidence line → none recorded. Ablation runs in a detached scratch worktree with finally cleanup; the stored command goes through guard_stored` → the real tree is never touched (detached commit-tree worktree); the command is guard-checked [tree b36127c8b345] (2026-10-16T08:11:44Z)
- (audit edge) `fm-reviewer (intent, adversary, edge): --ablate could fail the close (affected() and prove_hunks raise) → runs after the checks, any error prints 'ablation skipped'; no total bound → 600 s deadline, per-run timeout capped at the remainder; --json broken → folded into the finish JSON; a permanent inconclusive evidence line → none recorded. Ablation runs in a detached scratch worktree with finally cleanup; the stored command goes through guard_stored` → no template, red baseline, budget exhausted, slow hunk cut at the deadline [tree b36127c8b345] (2026-10-16T08:11:44Z)
- (audit operator) `fm-reviewer (intent, adversary, edge): --ablate could fail the close (affected() and prove_hunks raise) → runs after the checks, any error prints 'ablation skipped'; no total bound → 600 s deadline, per-run timeout capped at the remainder; --json broken → folded into the finish JSON; a permanent inconclusive evidence line → none recorded. Ablation runs in a detached scratch worktree with finally cleanup; the stored command goes through guard_stored` → one summary line, or 'ablation skipped: why' [tree b36127c8b345] (2026-10-16T08:11:44Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge): --ablate could fail the close (affected() and prove_hunks raise) → runs after the checks, any error prints 'ablation skipped'; no total bound → 600 s deadline, per-run timeout capped at the remainder; --json broken → folded into the finish JSON; a permanent inconclusive evidence line → none recorded. Ablation runs in a detached scratch worktree with finally cleanup; the stored command goes through guard_stored` → _ablate wraps task_prove_hunks with quiet and deadline [tree b36127c8b345] (2026-10-16T08:11:44Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:53Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_hunks.py']
- 2026-10-16T04:22:53Z set tier=M
- 2026-10-16T07:52:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1067.builder.md
- 2026-10-16T07:52:27Z focused
- 2026-10-16T08:11:01Z merged worktree-agent-a6d905d7c67c4c042 (2 file(s))
- 2026-10-16T08:11:04Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6d905d7c67c4c042
- 2026-10-16T08:11:05Z focused
- 2026-10-16T08:11:38Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T08:12:23Z done
- 2026-10-16T08:12:24Z committed f6cdaaf (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/tests/test_hunks.py; re-ground the plan against them before editing
## Lessons
- An informational step at close runs after the real checks, inside one try, under one deadline
## Files touched
- plugin/tests/test_hunks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
