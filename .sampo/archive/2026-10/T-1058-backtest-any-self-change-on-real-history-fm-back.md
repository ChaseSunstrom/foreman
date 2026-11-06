---
id: T-1058
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmbacktest.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_backtest.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:07:09Z
base: 4ead49ec3274333876aa94061c78db5c635f5bbd
base_tree: c8faace65e84ea4cb268c05d28613d966f9ba26a
plan0_at: 2026-10-16T08:45:09Z
plan0_scope: [plugin/lib/fmbacktest.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_backtest.py]
verified: strong
---
# Backtest any self-change on real history: fm backtest replays past sessions against a chan
## Raw request
> FEATURE: Backtest any self-change on real history: fm backtest replays past sessions against a changed card, known fix, rule or hint (beyond fm replay's guard-only replay) and says where it would have fired and how those sessions went (wild C6)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Before a self-change ships, show what it would have done on real history: fm backtest --rule REGEX | --fix SIG | --card NAME replays recorded session commands and failures and counts the fires. It is read-only.
## Assumptions (confidence)
## Acceptance criteria
- [x] a rule that matches 2 of 3 fixture session commands reports "would have fired 2 times in 1 session(s)" with a count of fired calls followed by errors — verify with `python3 plugin/tests/run.py test_backtest`
- [x] `fm backtest --card NAME --json` has the keys fires, sessions and errored — verify with `python3 plugin/tests/run.py test_backtest`
## Non-goals
## Approach (options → choice → why)
Reuse fmreplay's log reader (fmreplay._logs) to yield tool events; count matches per kind. --json for scripts. Options considered: replay through the real hook (slow, needs a sandbox), or sample only the last session (too thin).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fixture jsonl logs under `self.home/.claude/projects` (the layout `fmreplay._logs` reads). Assert counts for `--rule`, `--fix` and `--card`, the empty-corpus message, and that `--rule` with a bad regex gives a UsageError.
2. [x] Add `fmreplay.events()` and `fmbacktest.py`; read-only, nothing is written.
3. [x] Add the `backtest` parser entry and register the command.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_backtest` → ✗ exit 1 · Ran 4 tests in 0.9s (1 classes, 16 at a time; slowest: Backtest 0s) / FAILED (1 classes) [ran] [tree 55a0e66c3f47] (2026-10-16T08:45:34Z)
- (step 2) `python3 plugin/tests/run.py test_backtest` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Backtest 1s) / OK [ran] [tree 22b8aa8bdc6a] (2026-10-16T08:45:56Z)
- (step 3) `python3 plugin/tests/run.py test_backtest` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: Backtest 1s) / OK [ran] [tree 22b8aa8bdc6a] (2026-10-16T08:45:56Z)
- (step 1) `python3 plugin/tests/run.py test_backtest test_replay test_help` → exit 0 · Ran 16 tests in 2.9s (5 classes, 16 at a time; slowest: Replay 3s, Help 1s, PromptApprovals 1s) / OK [ran] [tree 80f5dbb85e54] (2026-10-16T09:05:49Z)
- (ac 1) `python3 plugin/tests/run.py test_backtest` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Backtest 1s) / OK [ran] [tree a05fabab4237] (2026-10-16T09:06:02Z)
- (ac 2) `python3 plugin/tests/run.py test_backtest` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Backtest 1s) / OK [ran] [tree a05fabab4237] (2026-10-16T09:06:02Z)
- (audit intent) `self review of the branch: read-only over recorded session logs through fmreplay; a bad regex or unknown card is a UsageError; the empty corpus says so; --json keys fires, sessions, errored, calls, scanned_sessions` → see a self-change's reach on real history before shipping it [tree a05fabab4237] (2026-10-16T09:06:02Z)
- (audit edge) `self review of the branch: read-only over recorded session logs through fmreplay; a bad regex or unknown card is a UsageError; the empty corpus says so; --json keys fires, sessions, errored, calls, scanned_sessions` → a card's count is a text approximation, said in the docs [tree a05fabab4237] (2026-10-16T09:06:02Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:02Z set scope=['plugin/lib/fmbacktest.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_backtest.py']
- 2026-10-16T05:02:03Z set tier=M
- 2026-10-16T08:45:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1058.builder.md
- 2026-10-16T08:45:09Z focused
- 2026-10-16T09:04:48Z merged worktree-agent-abe2fe676a3114608 (4 file(s))
- 2026-10-16T09:04:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abe2fe676a3114608
- 2026-10-16T09:05:46Z focused
- 2026-10-16T09:06:01Z scope: CHANGELOG.md, MASTER.md — docs (with T-1087's lines)
- 2026-10-16T09:07:08Z done
- 2026-10-16T09:07:09Z committed 928e636 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmreplay.py, plugin/tests/test_backtest.py; re-ground the plan against them before editing
## Lessons
- A self-change's blast radius is cheapest to measure on the history you already recorded
## Plan gaps
- failed first: step 1 Failing tests: fixture jsonl logs under `self.home/.claude/projects` (the layout `fmreplay._logs` r…
## Files touched
- plugin/tests/test_backtest.py
- plugin/lib/fmbacktest.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmci.py
- plugin/lib/fmcost.py
- plugin/lib/fmpr.py
- plugin/tests/test_pr_train.py
