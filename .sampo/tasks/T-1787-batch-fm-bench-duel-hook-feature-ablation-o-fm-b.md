---
id: T-1787
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T14:25:39Z
updated: 2026-10-23T14:41:40Z
batch: [T-1375, T-1376]
base: fdd2477a3ff9e17b2ee30340dfef351356969068
base_tree: 7d53b63066bc92d01d465a5e83e99dd8d0833a27
plan0_at: 2026-10-23T14:27:13Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# Batch: Fm bench duel: hook-feature ablation, o…; Fm bench duel at an equal dollar cap: b…
## Raw request
> T-1375: fm bench duel: hook-feature ablation, one Foreman hook feature switched off per arm, so each feature's effect is measured (T-1260 split)
> T-1376: fm bench duel at an equal dollar cap: both arms get the same spend, so cheaper isn't confused with better (T-1260 split)
## Interpretation
T-1375: a duel can't say which of Foreman's hook features earn their cost. FOREMAN_ABLATE=a,b switches named features off for one session: each note the guard hook adds to a tool call (fix, deps, veto, scope, lessons, steps, ambient, bus, cards, test-first, design, gate-pipe) and the Stop hook's drive; never the guard. fm bench duel --ablate a,b (or all) runs full Foreman and one arm per feature with it off, and says per feature whether turning it off lost passes, changed nothing, or only saved money. T-1376: Foreman costs more per case, so a pass-for-pass duel can confuse cheaper with better; --vs none --equal-spend gives Claude with no plugins Foreman's spend on each case as fresh attempts (up to 5, stopping at a pass), labelled duel-spend-* so the benchmarks page keeps its plain duels apart.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1375: Fm bench duel: hook-feature ablation, one Foreman hook feature switched off per arm, so ea works — verify with `python3 plugin/tests/run.py test_hooks test_bench_family`
- [x] T-1376: Fm bench duel at an equal dollar cap: both arms get the same spend, so cheaper isn't confu works — verify with `python3 plugin/tests/run.py test_bench_family`
- [x] FOREMAN_ABLATE switches off the named notes and drive, never the guard; an unknown name is ignored by hooks and refused by the bench — verify with `python3 plugin/tests/run.py test_hooks`
- [x] fm bench duel --ablate runs full Foreman plus one arm per feature with a verdict each; --vs none --equal-spend retries the plain arm up to Foreman's per-case spend (5 at most, stopping at a pass) under duel-spend labels — verify with `python3 plugin/tests/run.py test_bench_family`
## Non-goals
## Approach (options → choice → why)
Complete version: one switch the hooks read (named features only, the guard outside the list), the duel arms built from it, a per-feature verdict, the equal-spend arm with attempts and spend recorded, both refused with bad input, and the page untouched by these labels. Options for the switch: one env list read by a helper (chosen: what a bench session can set, nothing persisted), per-feature env vars (a dozen names), project meta (would leak into the user's sessions). For equal spend: retries up to the spend (chosen: it is what extra money buys a plain session), a higher --max-budget-usd (a plain session stops when it thinks it's done, so a higher cap buys nothing).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1375: Fm bench duel: hook-feature ablation, one Foreman hook feature switched off per arm, so ea
2. [x] T-1376: Fm bench duel at an equal dollar cap: both arms get the same spend, so cheaper isn't confu
3. [x] red tests: the switch in the hooks, the ablation duel, the equal-spend duel
4. [x] c.ablated and the hook gates, the bench arms and CLI flags; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md; fm bench duel --help (--ablate, --equal-spend); the switch's list is fmcore.ABLATABLE
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_hooks test_bench_family` → ✗ exit 1 · Ran 223 tests in 45.4s (36 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 33s, PreToolUse 27s) / FAILED (2 classes) [ran] [tree 1642f6c24519] (2026-10-23T14:30:24Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_bench_family test_bench` → exit 0 · Ran 250 tests in 48.4s (42 classes, 16 at a time; slowest: Stop 48s, Bench 41s, NoTaskGate 36s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:34:13Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_bench_family test_bench` → exit 0 · Ran 250 tests in 48.3s (42 classes, 16 at a time; slowest: Stop 48s, Bench 41s, NoTaskGate 36s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:35:02Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_bench_family test_bench` → exit 0 · Ran 250 tests in 48.0s (42 classes, 16 at a time; slowest: Stop 48s, Bench 41s, NoTaskGate 36s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:35:51Z)
- (step 4) `python3 plugin/tests/run.py test_hooks test_bench_family test_bench` → exit 0 · Ran 250 tests in 48.6s (42 classes, 16 at a time; slowest: Stop 48s, Bench 41s, NoTaskGate 36s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:36:40Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_bench_family` → exit 0 · Ran 223 tests in 47.2s (36 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 35s, PreToolUse 28s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:37:28Z)
- (ac 2) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 20 tests in 15.7s (10 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Ablation 9s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:37:44Z)
- (ac 4) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 20 tests in 15.5s (10 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Marathon 9s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:38:00Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 203 tests in 42.6s (26 classes, 16 at a time; slowest: Stop 42s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:38:43Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_bench_family` → exit 0 · Ran 223 tests in 47.2s (36 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 35s, PreToolUse 29s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (ac 2) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 20 tests in 15.6s (10 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Ablation 9s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 203 tests in 42.2s (26 classes, 16 at a time; slowest: Stop 42s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (ac 4) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 20 tests in 15.6s (10 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Ablation 9s) / OK [ran] [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): FOREMAN_ABLATE names only the per-call notes and drive, read by one helper; the guard runs before the notes and isn't in the list, so a session with any value still refuses (tested with guard named); the bench refuses unknown names and says the guard never switches off; the equal-spend arm retries fresh worktrees until a pass or Foreman's spend, five at most, and keeps the per-try records the cost band reads; its labels (duel-spend-*) stay off the benchmarks page` → a duel can say what each hook feature is worth, and whether Foreman's extra spend beats a plain session given the same money [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): FOREMAN_ABLATE names only the per-call notes and drive, read by one helper; the guard runs before the notes and isn't in the list, so a session with any value still refuses (tested with guard named); the bench refuses unknown names and says the guard never switches off; the equal-spend arm retries fresh worktrees until a pass or Foreman's spend, five at most, and keeps the per-try records the cost band reads; its labels (duel-spend-*) stay off the benchmarks page` → ablate all (13 arms), an unknown or empty name (refused), --ablate with a rival or --vs (refused), --equal-spend without --vs none (refused), a case Foreman spent nothing on (one try), a plain try that passes first (stops) [tree 757e543d0b95] (2026-10-23T14:40:39Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): FOREMAN_ABLATE names only the per-call notes and drive, read by one helper; the guard runs before the notes and isn't in the list, so a session with any value still refuses (tested with guard named); the bench refuses unknown names and says the guard never switches off; the equal-spend arm retries fresh worktrees until a pass or Foreman's spend, five at most, and keeps the per-try records the cost band reads; its labels (duel-spend-*) stay off the benchmarks page` → the switch only quiets advisory notes and the drive; refusals, evidence gates and audits are untouched, and hooks take their environment from Claude Code, not from a Bash command the model runs [tree 757e543d0b95] (2026-10-23T14:40:39Z)
## Log
- 2026-10-23T14:25:39Z created
- 2026-10-23T14:26:56Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmbench.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_bench_family.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-23T14:27:11Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_hooks test_bench_family`
- 2026-10-23T14:27:11Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_bench_family`
- 2026-10-23T14:27:12Z focused
- 2026-10-23T14:41:38Z done
- 2026-10-23T14:41:40Z committed 87317cb7 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmb…
- T-1260 [FEATURE M, done, 2 steps] fm bench's gate shows each delta with its noise band from repeated runs, and calls a change inside it noise, not a win or a loss — less…
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- decision 2026-10-14: [costly] Turned compact output on for the user (fm compact-output on)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- Name each injected note's builder: switching features off for measurement is then a set lookup, not a code fork
## Plan gaps
- failed first: step 3 red tests: the switch in the hooks, the ablation duel, the equal-spend duel
## Files touched
- plugin/tests/test_bench_family.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
