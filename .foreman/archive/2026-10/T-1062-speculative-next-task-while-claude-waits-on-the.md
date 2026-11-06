---
id: T-1062
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdraft.py, plugin/lib/fmnight.py, plugin/lib/fmcli.py, plugin/tests/test_draft.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:13:07Z
base: 021843ebfc182a65166c19f3ed6bd2e69e7982b6
base_tree: b291f55e09a1ad07d610299f3b27ce8b4e2b6b9a
plan0_at: 2026-10-16T08:45:12Z
plan0_scope: [plugin/lib/fmdraft.py, plugin/lib/fmnight.py, plugin/lib/fmcli.py, plugin/tests/test_draft.py]
verified: strong
---
# Speculative next task: while Claude waits on the user or a long job, the top queued S task
## Raw request
> FEATURE: Speculative next task: while Claude waits on the user or a long job, the top queued S task is drafted in a throwaway worktree so it is ready to review; discarded if the queue changes (wild C3)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Use waiting time: fm draft has a headless claude draft the top queued S task in a throwaway worktree branch draft/T-x, ready to review. A draft is discarded when the queue changes, and fm night can run it.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a fake `claude` on PATH, `fm draft` creates `draft/T-x`; changing the queue top and running `fm draft --status` removes it — verify with `python3 plugin/tests/run.py test_draft`
- [x] `fm night --dry-run` lists a "draft T-x" job when an S task is ready — verify with `python3 plugin/tests/run.py test_draft test_night`
## Non-goals
## Approach (options → choice → why)
fmdraft.py: a fingerprint (queue top id plus its brief hash) saved in draft.json. fm draft --status sweeps stale drafts. The drafting uses fm run's headless invocation, with no merge ever. Options considered: draft in the main tree (unsafe), or draft every queued task (cost).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: use the fake-claude pattern from `test_night.py:30`; assert the branch exists, `draft.json` has the fingerprint, a stale sweep removes both, and no S task gives "nothing to draft".
2. [x] Implement `fmdraft.py` and the parser entry.
3. [x] Add the night job.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_draft` → ✗ exit 1 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Draft 1s) / FAILED (1 classes) [ran] [tree fb0925279ed7] (2026-10-16T08:45:38Z)
- (step 2) `python3 plugin/tests/run.py test_draft test_night` → exit 0 · Ran 22 tests in 6.9s (9 classes, 16 at a time; slowest: Night 7s, NightGuards 4s, Draft 2s) / OK [ran] [tree e15728a61b3b] (2026-10-16T08:48:01Z)
- (step 3) `python3 plugin/tests/run.py test_draft test_night` → exit 0 · Ran 22 tests in 12.4s (9 classes, 16 at a time; slowest: Night 12s, NightGuards 9s, Draft 4s) / OK [ran] [tree e15728a61b3b] (2026-10-16T08:48:15Z)
- (step 3) `python3 plugin/tests/run.py test_draft test_night test_help` → exit 0 · Ran 26 tests in 9.8s (11 classes, 16 at a time; slowest: Night 10s, NightGuards 7s, Draft 4s) / OK [ran] [tree b4ff6a6c501f] (2026-10-16T09:07:08Z)
- (step 1) `python3 plugin/tests/run.py test_draft test_night test_help test_serve` → exit 0 · Ran 52 tests in 12.2s (15 classes, 16 at a time; slowest: Run 12s, Night 3s, Serve 3s) / OK [ran] [tree aae01f382318] (2026-10-16T09:12:18Z)
- (ac 1) `python3 plugin/tests/run.py test_draft` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Draft 1s) / OK [ran] [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (ac 2) `python3 plugin/tests/run.py test_draft test_night` → exit 0 · Ran 22 tests in 3.2s (9 classes, 16 at a time; slowest: Night 3s, NightGuards 2s, Draft 1s) / OK [ran] [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (audit intent) `self review: the draft reuses fmserve._claude_cmd (same sandbox and model flags as fm run) after the re-merge; it got no permission mode, so a headless draft couldn't edit → acceptEdits (decided and recorded: edits only its own throwaway worktree, never merged; shell still asks, denied headless; guard runs); stale sweep by queue-top id and brief hash` → waiting time drafts the next S task for review [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (audit adversary) `self review: the draft reuses fmserve._claude_cmd (same sandbox and model flags as fm run) after the re-merge; it got no permission mode, so a headless draft couldn't edit → acceptEdits (decided and recorded: edits only its own throwaway worktree, never merged; shell still asks, denied headless; guard runs); stale sweep by queue-top id and brief hash` → never merged; edits confined to its worktree by acceptEdits' own scope; guard active [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (audit edge) `self review: the draft reuses fmserve._claude_cmd (same sandbox and model flags as fm run) after the re-merge; it got no permission mode, so a headless draft couldn't edit → acceptEdits (decided and recorded: edits only its own throwaway worktree, never merged; shell still asks, denied headless; guard runs); stale sweep by queue-top id and brief hash` → no S task, an unchanged queue keeps the draft, a changed brief sweeps it [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (audit operator) `self review: the draft reuses fmserve._claude_cmd (same sandbox and model flags as fm run) after the re-merge; it got no permission mode, so a headless draft couldn't edit → acceptEdits (decided and recorded: edits only its own throwaway worktree, never merged; shell still asks, denied headless; guard runs); stale sweep by queue-top id and brief hash` → draft/T-x branch, draft.json, a night job line [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
- (audit maintainer) `self review: the draft reuses fmserve._claude_cmd (same sandbox and model flags as fm run) after the re-merge; it got no permission mode, so a headless draft couldn't edit → acceptEdits (decided and recorded: edits only its own throwaway worktree, never merged; shell still asks, denied headless; guard runs); stale sweep by queue-top id and brief hash` → one claude-command builder shared with fm run [tree c8c7e04a2bbb] (2026-10-16T09:12:23Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:11Z set scope=['plugin/lib/fmdraft.py', 'plugin/lib/fmnight.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_draft.py']
- 2026-10-16T05:02:12Z set tier=M
- 2026-10-16T08:45:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1062.builder.md
- 2026-10-16T08:45:12Z focused
- 2026-10-16T09:04:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4fb107a8ffd970a4 (branch worktree-agent-a4fb107a8ffd970a4 kept: not merged)
- 2026-10-16T09:05:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1062.builder.md
- 2026-10-16T09:05:42Z focused
- 2026-10-16T09:11:15Z merged worktree-agent-a4bd54a60eca45667 (4 file(s))
- 2026-10-16T09:11:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4bd54a60eca45667
- 2026-10-16T09:11:20Z focused
- 2026-10-16T09:12:18Z scope: CHANGELOG.md, MASTER.md — docs; plugin/lib/fmdraft.py, plugin/tests/test_draft.py — acceptEdits for the headless draft
- 2026-10-16T09:13:06Z done
- 2026-10-16T09:13:07Z committed b5973bf (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmdraft.py, plugin/lib/fmnight.py, plugin/tests/test_draft.py; re-ground the plan against them before editing
## Lessons
- A headless session needs an explicit permission mode for the one thing it must do, or it silently does nothing
## Plan gaps
- failed first: step 1 Failing tests: use the fake-claude pattern from `test_night.py:30`; assert the branch exists, `draf…
## Files touched
- plugin/tests/test_draft.py
- plugin/lib/fmdraft.py
- plugin/lib/fmcli.py
- plugin/lib/fmnight.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcost.py
- plugin/lib/fmevolve.py
- plugin/lib/fmtrials.py
- plugin/tests/test_trials.py
