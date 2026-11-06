---
id: T-0963
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:52Z
updated: 2026-10-15T22:43:57Z
base: 26c8ac5e1e28f0499d350e4292458bf9b773b6b0
base_tree: 3560741dc17666acadafe0ffce9ef1f08f27c787
verified: strong
---
# Postures and rivals: fm posture lite, compact shadow mode, verify commands that read state, a bare-Claude bench arm, hollow subagent returns
## Raw request
> Postures and rivals: fm posture lite, compact shadow mode, verify commands that read state, a bare-Claude bench arm, hollow subagent returns
## Interpretation
Board clusters r4-postures-lite (fm posture lite|full: a per-project meta flag; in fmhooks.run ~83 a lite project skips every non-PreToolUse event, as _quiet() does), r2-compact-output-rollout (a shadow state for fm compact-output: the hook runs compact() but only appends {cmd_family, saved_chars} to state/outputs/shadow.jsonl; status prints would-have-cut), r2-verify-command-hygiene (fmcore.lint_verify flags verify commands that read .foreman or state/tasks|briefs), r4-bench-vs-plain (fm bench duel --vs none: an arm with no plugins, stubbed claude in tests) and lanes-fleet (SubagentStop is async, so it cannot block: log a hollow_return event when an fm-builder or fm-reviewer's last message is under 80 chars, and fm next surfaces it).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm posture lite makes the hooks skip everything but the guard for this project, and fm posture full restores them — verify with `python3 plugin/tests/run.py -k BoardPosture`
- [x] fm compact-output shadow records would-be savings in shadow.jsonl and never rewrites a tool's output — verify with `python3 plugin/tests/run.py -k BoardPosture`
- [x] lint_verify flags a verify command that reads Foreman's state paths — verify with `python3 plugin/tests/run.py -k BoardPosture`
- [x] fm bench duel --vs none adds an arm that runs with no plugins — verify with `python3 plugin/tests/run.py -k BoardPosture`
- [x] A SubagentStop from fm-builder or fm-reviewer whose last message is under 80 chars logs hollow_return, and fm next names it — verify with `python3 plugin/tests/run.py -k BoardPosture`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardPosture class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
README, MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardPosture` → ✗ exit 1 · Ran 5 tests in 1.8s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / FAILED (2 classes) [ran] [tree 1e21d7e0c881] (2026-10-15T22:24:35Z)
- (step 2) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 5 tests in 2.2s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 1755cae5df7a] (2026-10-15T22:28:14Z)
- (step 3) `python3 plugin/tests/run.py test_board_verbs test_docs test_docsdrift test_board_posture` → exit 0 · Ran 43 tests in 12.3s (14 classes, 16 at a time; slowest: BoardVerbs 12s, BoardPostureBench 3s, TaskLifecycle 2s) / OK [ran] [tree 14ab127bafd7] (2026-10-15T22:30:11Z)
- (step 2) `python3 plugin/tests/run.py test_board_posture test_guard test_hooks test_bench test_bench_family test_tidy` → exit 0 · Ran 304 tests in 35.2s (82 classes, 16 at a time; slowest: Stop 35s, Bench 22s, PreToolUse 20s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:49Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (ac 4) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (ac 5) `python3 plugin/tests/run.py -k BoardPosture` → exit 0 · Ran 7 tests in 2.1s (2 classes, 16 at a time; slowest: BoardPostureBench 2s, BoardPosture 1s) / OK [ran] [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (audit intent) `security-guidance commit review (3 medium) plus one fm-reviewer pass (1 high, 2 medium, 5 low); all fixed test-first except the bare arm's PATH (reworded) and the 24 h hollow-return window (kept)` → lite posture, shadow compaction, state-reading verify lint, bench vs no plugins, hollow-return detection [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (audit adversary) `security-guidance commit review (3 medium) plus one fm-reviewer pass (1 high, 2 medium, 5 low); all fixed test-first except the bare arm's PATH (reworded) and the 24 h hollow-return window (kept)` → Claude can't lower the posture or lift a pause, flags before the word included; lite keeps the guard, TaskCompleted and fm ask grants; the bench's bare arm copies the plugin's full PreToolUse set [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (audit edge) `security-guidance commit review (3 medium) plus one fm-reviewer pass (1 high, 2 medium, 5 low); all fixed test-first except the bare arm's PATH (reworded) and the 24 h hollow-return window (kept)` → a repo's own state/tasks folder isn't flagged; shadow data survives fm tidy; a cost-only gate failure reads as 'passes more, at a cost' [tree 0677b863a348] (2026-10-15T22:43:52Z)
- (audit operator) `security-guidance commit review (3 medium) plus one fm-reviewer pass (1 high, 2 medium, 5 low); all fixed test-first except the bare arm's PATH (reworded) and the 24 h hollow-return window (kept)` → README and MASTER say lite is the user's to type [tree 0677b863a348] (2026-10-15T22:43:52Z)
## Log
- 2026-10-15T21:12:52Z created
- 2026-10-15T22:18:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0963.builder.md
- 2026-10-15T22:20:57Z focused
- 2026-10-15T22:33:50Z merged worktree-agent-ae8148ce7ae6d2da3 (9 file(s))
- 2026-10-15T22:33:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae8148ce7ae6d2da3
- 2026-10-15T22:33:51Z focused
- 2026-10-15T22:36:40Z paused: focus moved to T-0977
- 2026-10-15T22:39:28Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T22:39:28Z focused
- 2026-10-15T22:43:55Z done
- 2026-10-15T22:43:57Z committed 95a1750 (10 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 3 steps
## Lessons
- A user-only switch must match its word anywhere in the args: a flag before it is the first bypass anyone tries
## Plan gaps
- failed first: step 1 Failing tests in a BoardPosture class
## Files touched
- plugin/tests/test_board_posture.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/hooks/compact
- plugin/lib/fmsetup.py
- plugin/lib/fmcore.py
- plugin/lib/fmbench.py
- MASTER.md
- README.md
- plugin/lib/fmguard.py
- plugin/lib/fmtidy.py
- demo/live.mp4
- CHANGELOG.md
- demo/live.svg
