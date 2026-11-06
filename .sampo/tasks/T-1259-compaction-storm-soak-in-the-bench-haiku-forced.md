---
id: T-1259
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:25Z
updated: 2026-10-23T12:40:15Z
base: 5a69ae52f18e1d10c4e9508f40a6b5cb69ef805e
base_tree: e306a547951967c8b52edd446330cbc5eea95b7e
plan0_at: 2026-10-23T12:37:37Z
plan0_scope: [plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
verified: strong
---
# Compaction-storm soak in the bench (Haiku, forced compaction every few turns) and a measur
## Raw request
> Compaction-storm soak in the bench (Haiku, forced compaction every few turns) and a measured sweep of the compaction window (brainstorm-20261020 C4)
## Interpretation
fm bench soak gains --compact-at TOKENS (a compaction storm: each soak session compacts once its context nears TOKENS, so every few turns when small, with each case's compactions counted, as T-1242's duels do) and --sweep W1,W2,… (the soak once per window, a summary row each: passes, repeats, compactions, cost). The paid measured sweep on Haiku runs later, when usage allows (decision recorded).
## Assumptions (confidence)
## Acceptance criteria
- [x] soak --compact-at sets the window and counts compactions per case; --sweep runs once per window with a summary row; bad windows refused — verify with `python3 plugin/tests/run.py test_bench_family`
## Non-goals
## Approach (options → choice → why)
Options: (1) reuse T-1242's CLAUDE_CODE_AUTO_COMPACT_WINDOW and _compactions in soak_case, a loop over windows in the soak command (chosen: one mechanism for duels and soaks); (2) a separate storm command (rejected: soak already is the long-conversation bench); (3) force /compact by sending it as a user turn (rejected: the window variable is how Claude Code compacts on its own, which is what a long session meets).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the storm and the sweep, test first
## Resume here
## Docs impact
CHANGELOG line; fm bench soak -h documents both flags. The bench page's showcase text is unchanged until a measured sweep exists.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench_family.SoakStorm` → ✗ exit 1 · Ran 1 tests in 3.7s (1 classes, 16 at a time; slowest: SoakStorm 3s) / FAILED (1 classes) [ran] [tree 327581d45244] (2026-10-23T12:37:49Z)
- (step 1) `python3 plugin/tests/run.py test_bench_family test_bench test_cli` → exit 0 · Ran 164 tests in 40.1s (49 classes, 16 at a time; slowest: Bench 40s, TaskLifecycle 30s, Judged 23s) / OK [ran] [tree f80f9864c7a8] (2026-10-23T12:39:02Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 16 tests in 15.0s (7 classes, 16 at a time; slowest: Judged 15s, Duel 9s, Marathon 8s) / OK [ran] [tree f80f9864c7a8] (2026-10-23T12:39:18Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 16 tests in 14.9s (7 classes, 16 at a time; slowest: Judged 15s, Duel 9s, Marathon 8s) / OK [ran] [tree f80f9864c7a8] (2026-10-23T12:39:33Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): soak reuses T-1242's window variable and compaction count, so a soak storm is measured the way duels are; the sweep is a loop of the same soak, each window its own results file; the budget check multiplies by the windows` → a soak can force compaction every few turns and count it, and a sweep shows across windows where compaction starts to cost repeats [tree f80f9864c7a8] (2026-10-23T12:39:33Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): soak reuses T-1242's window variable and compaction count, so a soak storm is measured the way duels are; the sweep is a loop of the same soak, each window its own results file; the budget check multiplies by the windows` → a window under 1000 tokens, more than 6, words or --compact-at with --sweep are refused before anything runs; a case that errors before a session id counts 0 compactions; the kept session is removed after counting, as in duels [tree f80f9864c7a8] (2026-10-23T12:39:33Z)
## Log
- 2026-10-20T14:01:25Z created
- 2026-10-23T12:37:32Z set tier=M, scope=['plugin/lib/fmbench.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_bench_family.py', 'CHANGELOG.md']
- 2026-10-23T12:37:36Z focused
- 2026-10-23T12:40:13Z done
- 2026-10-23T12:40:15Z committed 48fe899f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-23: T-1259: build the compaction storm and the window sweep, tested with the bench's fakes; the measured sweep (real Haiku sessions) waits until weekly …
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmb…
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py; re-ground the plan against them before editing
## Lessons
- Build the paid experiment's harness against fakes now; run the paid sweep when the budget allows, from one command
## Plan gaps
- failed first: step 1 the storm and the sweep, test first
## Files touched
- CHANGELOG.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/tests/test_bench_family.py
