---
id: T-1079
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/tests/test_perf_cost.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:45:03Z
base: 03a248c17d2830a3e19a4a3208e1a655bed1d561
base_tree: 7e8b252faa048fa3cfcc5289b475927cd9871eec
verified: strong
---
# Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm
## Raw request
> PERF: Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm cost and the digest (wild C23)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm cost` and `fm digest` flag spend that nothing in Foreman accounts for. That means sessions with no ledger events at all, such as a stray `claude -p` or subagent, and turns more than 30 minutes from any ledger event of their session. A line like "Unexplained spend: 34% (≈ 410k) in 2 session(s)" appears when it is at least 20% and 100k tokens. The existing "(no task)" bucket (fmcost.py:188) is nearly empty, because `_task_at` carries the last task forever (fmcost.py:143). It cannot flag this.
## Assumptions (confidence)
## Acceptance criteria
- [x] Spend from a session with no ledger events, or beyond the gap, appears as an unexplained line with its share; fully explained spend shows none — verify with `python3 plugin/tests/run.py test_perf_cost`
- [x] The digest shows the same line — verify with `python3 plugin/tests/run.py test_perf_cost test_economics`
## Non-goals
## Approach (options → choice → why)
(a) widen the "(no task)" bucket; (b) a separate attribution pass by session and time gap; (c) read the transcripts for prompts. Choose (b). In `cmd_cost` (fmcost.py:180-188), build `{session: sorted event times}` from `c.ledger_tail(p, 20000)` using the events' `session_id`. Add `unexplained(msgs, events, gap=1800)` returning the weighted tokens, the share and the sessions. Add the result to the data as `unexplained`, add a text line after "By task", and add the same line to `cmd_digest` (fmcost.py:379). Put thresholds in constants (`UNEXPLAINED_MIN_PCT`, `UNEXPLAINED_MIN_TOKENS`). Sessions that are unexplained but under the thresholds produce no line.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fake transcripts (follow the existing fixtures in test_perf_cost.py) with one session that has ledger events, one without, and a turn after a long gap. Assert the JSON `unexplained` share, the "Unexplained spend" text in `fm cost` and `fm digest`, and no line when the share is small.
2. [x] Implement `unexplained()` and wire both commands.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_cost` → ✗ exit 1 · Ran 12 tests in 2.5s (6 classes, 16 at a time; slowest: StepCompact 2s, DegradeOnPace 2s, GateOrder 1s) / FAILED (1 classes) [ran] [tree 904bfa4a2910] (2026-10-16T05:27:43Z)
- (step 2) `python3 plugin/tests/run.py test_perf_cost test_economics` → exit 0 · Ran 14 tests in 2.5s (8 classes, 16 at a time; slowest: StepCompact 2s, DegradeOnPace 2s, UnexplainedSpend 1s) / OK [ran] [tree 811fa43888e3] (2026-10-16T05:28:08Z)
- (step 2) `python3 plugin/tests/run.py test_perf_cost test_economics` → exit 0 · Ran 16 tests in 2.7s (8 classes, 16 at a time; slowest: StepCompact 3s, DegradeOnPace 2s, UnexplainedSpend 1s) / OK [ran] [tree 0a2a0ee382cc] (2026-10-16T05:36:35Z)
- (ac 1) `python3 plugin/tests/run.py test_perf_cost` → exit 0 · Ran 14 tests in 5.3s (6 classes, 16 at a time; slowest: StepCompact 5s, DegradeOnPace 4s, UnexplainedSpend 2s) / OK [ran] [tree 83a270fd5d30] (2026-10-16T05:45:00Z)
- (ac 2) `python3 plugin/tests/run.py test_perf_cost test_economics` → exit 0 · Ran 16 tests in 5.3s (8 classes, 16 at a time; slowest: StepCompact 5s, DegradeOnPace 4s, UnexplainedSpend 2s) / OK [ran] [tree 83a270fd5d30] (2026-10-16T05:45:00Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost test_economics` → exit 0 · Ran 16 tests in 5.3s (8 classes, 16 at a time; slowest: StepCompact 5s, DegradeOnPace 4s, UnexplainedSpend 2s) / OK [ran] [tree 83a270fd5d30] (2026-10-16T05:45:00Z)
- (audit self) `review: one fm-reviewer pass (combined); 4 findings fixed by the builder test-first (archived months via c.ledger_events, unparseable ts skipped, wording names the top session, single call)` → no findings [tree 83a270fd5d30] (2026-10-16T05:45:00Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:42Z set scope=['plugin/lib/fmcost.py', 'plugin/tests/test_perf_cost.py']
- 2026-10-16T04:22:42Z set tier=S
- 2026-10-16T05:26:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1079.builder.md
- 2026-10-16T05:26:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1079.builder.md
- 2026-10-16T05:26:55Z focused
- 2026-10-16T05:43:59Z merged worktree-agent-ab4e0426b3db0c2b9 (2 file(s))
- 2026-10-16T05:43:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab4e0426b3db0c2b9
- 2026-10-16T05:43:59Z focused
- 2026-10-16T05:44:00Z scope: CHANGELOG.md — release note
- 2026-10-16T05:45:02Z done
- 2026-10-16T05:45:03Z committed fbbede8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcost.py, plugin/tests/test_perf_cost.py; re-ground the plan against them before editing
## Measurements
fm cost on the real state (21k live ledger lines + archive): unexplained_spend 0.21 s of 6.8 s total (cProfile); the rest is pre-existing transcript scan and _task_at (4.1 s, captured separately). Before → after: the detection adds ≈0.2 s.
## Lessons
- Window reports read every ledger month (c.ledger_events), never a fixed tail
## Plan gaps
- failed first: step 1 Failing tests: fake transcripts (follow the existing fixtures in test_perf_cost.py) with one sessio…
## Files touched
- plugin/tests/test_perf_cost.py
- plugin/lib/fmcost.py
- CHANGELOG.md
