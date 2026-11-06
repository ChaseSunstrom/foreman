---
id: T-1059
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/lib/fmevolve.py, plugin/lib/fmcost.py, plugin/tests/test_trials.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:10:57Z
base: 928e6360ea28fadd0341acf05fc88ba309033ad5
base_tree: a05fabab42370607db51c68b8472cac2c578e2d3
plan0_at: 2026-10-16T08:45:11Z
plan0_scope: [plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/lib/fmevolve.py, plugin/lib/fmcost.py, plugin/tests/test_trials.py]
verified: strong
---
# Every self-change is a pre-registered trial: fm evolve and rule/fix/card changes record th
## Raw request
> FEATURE: Every self-change is a pre-registered trial: fm evolve and rule/fix/card changes record the metric they should move and by how much; after N days fm digest grades them and a change that didn't move it is proposed for revert (wild C7)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Each self-change (fm rule add, fm evolve, fix or card change) can pre-register the metric it should move and by when (--moves corrections --by 30). The digest grades due trials on before and after ledger rates: moved, or no movement with a revert proposal.
## Assumptions (confidence)
## Acceptance criteria
- [x] a trial registered 10 days ago with fixture ledger events (corrections 5/day before, 5/day after) grades "no movement: propose revert"; a halved rate grades "moved" — verify with `python3 plugin/tests/run.py test_trials`
- [x] `fm rule add X --moves corrections --by 30` writes a trial and `fm digest` prints it — verify with `python3 plugin/tests/run.py test_trials`
## Non-goals
## Approach (options → choice → why)
fmtrials.py stores trials in state, then rates per day from ledger events in equal windows before and after. A trial is graded only when due, and a missing --moves records nothing. Options considered: automatic reverts (too risky unattended), or a separate dashboard (the digest is where the user looks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: use `c.log_event` with backdated ts; check grade verdicts, an ungraded trial before N days ("pending, N days left"), and a rule add without `--moves` records none.
2. [x] Write `fmtrials.py` and wire it into `cmd_rule`, `cmd_evolve` and `cmd_digest`.
3. [x] Add the `trial` parser entry.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_trials` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.5s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 557d26be8df5] (2026-10-16T08:45:38Z)
- (step 2) `python3 plugin/tests/run.py test_trials` → exit 0 · Ran 4 tests in 1.6s (1 classes, 16 at a time; slowest: Trials 1s) / OK [ran] [tree 7e92831dc58a] (2026-10-16T08:46:06Z)
- (step 3) `python3 plugin/bin/fm trial` → exit 0 · No trials: fm rule add X --moves corrections --by 30 [ran] [tree 7e92831dc58a] (2026-10-16T08:46:06Z)
- (step 2) `python3 plugin/tests/run.py test_trials test_help test_cli` → exit 0 · Ran 110 tests in 26.3s (31 classes, 16 at a time; slowest: TaskLifecycle 26s, StateViews 13s, AuditPrep 12s) / OK [ran] [tree bd72e2635866] (2026-10-16T09:07:25Z)
- (step 1) `python3 plugin/tests/run.py test_trials test_help test_cli test_evolve` → exit 0 · Ran 119 tests in 34.2s (34 classes, 16 at a time; slowest: TaskLifecycle 34s, Evolve 18s, StateViews 14s) / OK [ran] [tree 82ffcd01fb34] (2026-10-16T09:09:08Z)
- (ac 1) `python3 plugin/tests/run.py test_trials` → exit 0 · Ran 6 tests in 2.1s (1 classes, 16 at a time; slowest: Trials 2s) / OK [ran] [tree b291f55e09a1] (2026-10-16T09:09:20Z)
- (ac 2) `python3 plugin/tests/run.py test_trials` → exit 0 · Ran 6 tests in 2.1s (1 classes, 16 at a time; slowest: Trials 2s) / OK [ran] [tree b291f55e09a1] (2026-10-16T09:09:20Z)
- (audit intent) `self review of the branch: trials only record (never revert unattended); my spot-check found --by 0 divided by zero inside fm digest and a malformed trials.json crashed it → --by ≥ 1 refused, bad records skipped, both tested on the re-merge branch` → a self-change says what it should move and is graded on it [tree b291f55e09a1] (2026-10-16T09:09:20Z)
- (audit edge) `self review of the branch: trials only record (never revert unattended); my spot-check found --by 0 divided by zero inside fm digest and a malformed trials.json crashed it → --by ≥ 1 refused, bad records skipped, both tested on the re-merge branch` → --by 0, malformed records, a zero baseline grades as no movement [tree b291f55e09a1] (2026-10-16T09:09:20Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:07Z set scope=['plugin/lib/fmtrials.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmevolve.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_trials.py']
- 2026-10-16T05:02:08Z set tier=M
- 2026-10-16T08:45:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1059.builder.md
- 2026-10-16T08:45:11Z focused
- 2026-10-16T09:04:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac0de1422029a5189 (branch worktree-agent-ac0de1422029a5189 kept: not merged)
- 2026-10-16T09:05:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1059.builder.md
- 2026-10-16T09:05:37Z focused
- 2026-10-16T09:08:18Z merged worktree-agent-a093616a345c29fbc (5 file(s))
- 2026-10-16T09:08:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a093616a345c29fbc
- 2026-10-16T09:08:33Z focused
- 2026-10-16T09:09:17Z scope: CHANGELOG.md, MASTER.md — docs; plugin/lib/fmcost.py — the digest's trial lines
- 2026-10-16T09:10:56Z done
- 2026-10-16T09:10:57Z committed 021843e (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_evolve.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmevolve.py, plugin/lib/fmtrials.py, plugin/tests/test_trials.py; re-ground the plan against them before editing
## Lessons
- A report that runs every day must survive any record it reads
## Plan gaps
- failed first: step 1 Failing tests: use `c.log_event` with backdated ts; check grade verdicts, an ungraded trial before …
## Files touched
- plugin/tests/test_trials.py
- plugin/lib/fmtrials.py
- plugin/lib/fmcli.py
- plugin/lib/fmevolve.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md
