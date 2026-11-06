---
id: T-0676
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:14Z
updated: 2026-10-09T17:22:11Z
batch: [T-0448, T-0449, T-0467, T-0486, T-0487]
base: a3de9b785a8f7c9193342061d9b1769e6f90f27e
base_tree: 4c548934bc4bcb62a194948fb9bb8232c07e75a6
verified: strong
---
# Milestone: Features — Performance and cost
## Raw request
> T-0448: FEATURE: Context economy (C091, value 4/5, effort M, risk low)
>   first version: Add step-boundary compaction with a curated handoff (extend T-0098's task-boundary rule to M/L steps) and a session rotate when context slope turns bad; reuse checkpoint/resume.
>   what it is: Compact at step boundaries, rotate sessions, serve reads as deltas and share prompt-cache prefixes.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0449: FEATURE: Budgets and usage (C093, value 4/5, effort M, risk high)
>   first version: First version: when pace is over, degrade (drop optional second reads/brainstorms, keep required gates) instead of blocking, and let fm night spend expiring weekly quota on queued low-priority tasks under hard caps. Spend guard must stay conservative.
>   what it is: Forecast cost, degrade gracefully near limits, enforce latency and cost budgets and use expiring quota.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0467: FEATURE: Gate scheduling and warm starts (C092, value 3/5, effort S, risk low)
>   first version: Order gates in fm check by (recent failure rate / median runtime) from stored run times, keeping fail-fast; cancel remaining reviewer work on first blocker later.
>   what it is: Order and shard gates by failure odds, duration and return on time, cancelling reviewers on the first blocker.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0486: FEATURE: Fast hooks (C089, value 3/5, effort M, risk med)
>   first version: First version: record per-hook import time and an SLO burn counter in the ledger, and have fm doctor/friction flag regressions with the offending commit range. Skip daemon (adds a long-lived process near the guard).
>   what it is: Keep hooks fast with a resident daemon, lazy imports, fork servers and latency SLOs.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0487: FEATURE: Route work to the cheapest model (C090, value 3/5, effort M, risk med)
>   first version: Let fm run/lane pick model and effort from task type and tier using fm bench history, defaulting to current behaviour; start by logging model and pass/fail per task to feed it.
>   what it is: Route each step to the cheapest model and effort that passes and draft cheap then verify strong.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0448, T-0449, T-0467, T-0486, T-0487 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0676. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0467 GateOrder: fm check runs gates by recent failure odds per second of median runtime (from check_run history), configured order when there's no history; results still listed in configured order — verify with `python3 plugin/tests/run.py -p test_perf_cost.py -k GateOrder`
- [x] T-0486 HookSlo: each hook_ms event carries Foreman's revision; fm doctor warns when the p95 of the last 200 PreToolUse runs is over the SLO (bench_hooks' budget) and names the revision where it rose — verify with `python3 plugin/tests/run.py -p test_perf_cost.py -k HookSlo`
- [x] T-0449 DegradeOnPace: while usage runs ahead of pace but under the cap, optional work is dropped with a note (fm next offers no side work, fm ideas --deepen runs 0 rounds) and required gates still run; over the cap still blocks — verify with `python3 plugin/tests/run.py -p test_perf_cost.py -k DegradeOnPace`
- [x] T-0487 ModelLog: fm task finish logs the session's model, type, tier and verification strength; fm cost --by-model shows pass counts per model and type/tier — verify with `python3 plugin/tests/run.py -p test_perf_cost.py -k ModelLog`
- [x] T-0448 StepCompact: at a step boundary of an M/L task (a step just got evidence) with context at or over CONTEXT_NOTE_PCT, the Stop note says to checkpoint and compact there, Resume-here being the handoff — verify with `python3 plugin/tests/run.py -p test_perf_cost.py -k StepCompact`
## Non-goals
## Approach (options → choice → why)
Options per member: (a) new modules/daemons, (b) extend the existing seams each brief step names, (c) config flags. Choice: (b), smallest diffs in existing code. GateOrder: sort the gates to run by fail-rate/median-seconds from check_run history (as _slower reads it), list results in configured order. HookSlo: rev = plugin.json version, read once per hook process (module cache) only when writing hook_ms; doctor reads the events tail, SLO from bench_hooks.BUDGET_MS. DegradeOnPace: reuse fmbudget.subagent_pause() as the pace signal; drop friction pass in _next_for, side-task offers in the Stop drive, and --deepen rounds in fm ideas, each with a note; fmbudget.check unchanged (over the cap still blocks), fm check untouched. ModelLog: task_done event data gains model (statusline snapshot), type, tier, verified; fm cost --by-model groups them from the ledger. StepCompact: Stop drive note when the active M/L task's newest work event is step evidence and context >= CONTEXT_NOTE_PCT. Rejected: hook daemon (near the guard), session rotation (needs slope history), routing models now (log first).
## Risks and rollback
## Execution prompt
## Steps
1. [x] all five failing classes first (test_perf_cost.py)
2. [x] GateOrder in fm check (fmcli cmd_check, check_run history as _slower reads it)
3. [x] HookSlo: rev on hook_ms (fmhooks run), doctor check (fmdoctor)
4. [x] DegradeOnPace (fmbudget pace, fmcore/_next_for side work, fmideas deepen)
5. [x] ModelLog (task finish ledger event, fm cost --by-model)
6. [x] StepCompact (fmhooks Stop note at a step boundary)
7. [x] full suite once; CHANGELOG line for the main thread; MASTER/help lines for new flags
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md bullet (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_perf_cost.py` → ✗ exit 1 · Ran 9 tests in 3.1s (5 classes, 16 at a time; slowest: StepCompact 3s, DegradeOnPace 2s, GateOrder 1s) / FAILED (5 classes) [ran] [tree f657a8f552c6] (2026-10-09T17:13:59Z)
- (step 2) `python3 plugin/tests/run.py -p test_perf_cost.py -k GateOrder` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GateOrder 1s) / OK [ran] [tree d145a0dfff95] (2026-10-09T17:14:21Z)
- (step 3) `python3 plugin/tests/run.py -p test_perf_cost.py -k HookSlo` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: HookSlo 0s) / OK [ran] [tree 446c94e75610] (2026-10-09T17:14:56Z)
- (step 4) `python3 plugin/tests/run.py -p test_perf_cost.py -k DegradeOnPace` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: DegradeOnPace 1s) / OK [ran] [tree e12729f2c017] (2026-10-09T17:16:28Z)
- (step 5) `python3 plugin/tests/run.py -p test_perf_cost.py -k ModelLog` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: ModelLog 1s) / OK [ran] [tree ff8d0606b8a1] (2026-10-09T17:17:01Z)
- (step 6) `python3 plugin/tests/run.py -p test_perf_cost.py -k StepCompact` → exit 0 · Ran 2 tests in 4.6s (1 classes, 16 at a time; slowest: StepCompact 5s) / OK [ran] [tree 56468fddb439] (2026-10-09T17:17:24Z)
- (step 7) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.7    34.3     150  [0] / SessionEnd                  30.0    31.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 16:32 UTC; python3 plugin/tests/run.py → exit 0 · Ran 1067 tests i [ran] [tree e6fa69db3fca] (2026-10-09T17:19:00Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 17:19 UTC) [ran] [tree e6fa69db3fca] (2026-10-09T17:19:30Z)
- (step 7) `python3 plugin/tests/run.py -p test_perf_cost.py -k GateOrder` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GateOrder 0s) / OK [ran] [tree 0648ae327bf2] (2026-10-09T17:21:38Z)
- (step 7) `python3 plugin/tests/run.py -p test_perf_cost.py -k HookSlo` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: HookSlo 0s) / OK [ran] [tree 0648ae327bf2] (2026-10-09T17:21:39Z)
- (step 7) `python3 plugin/tests/run.py -p test_perf_cost.py -k DegradeOnPace` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: DegradeOnPace 1s) / OK [ran] [tree 0648ae327bf2] (2026-10-09T17:21:40Z)
- (step 7) `python3 plugin/tests/run.py -p test_perf_cost.py -k ModelLog` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ModelLog 0s) / OK [ran] [tree 0648ae327bf2] (2026-10-09T17:21:41Z)
- (step 7) `python3 plugin/tests/run.py -p test_perf_cost.py -k StepCompact` → exit 0 · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: StepCompact 2s) / OK [ran] [tree 0648ae327bf2] (2026-10-09T17:21:43Z)
- (ac 1) `python3 plugin/tests/run.py -p test_perf_cost.py -k GateOrder` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GateOrder 0s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (ac 2) `python3 plugin/tests/run.py -p test_perf_cost.py -k HookSlo` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: HookSlo 0s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (ac 3) `python3 plugin/tests/run.py -p test_perf_cost.py -k DegradeOnPace` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: DegradeOnPace 1s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (ac 4) `python3 plugin/tests/run.py -p test_perf_cost.py -k ModelLog` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ModelLog 0s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (ac 5) `python3 plugin/tests/run.py -p test_perf_cost.py -k StepCompact` → exit 0 · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: StepCompact 2s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (step 1) `python3 plugin/tests/run.py -p test_perf_cost.py` → exit 0 · Ran 9 tests in 1.9s (5 classes, 16 at a time; slowest: StepCompact 2s, DegradeOnPace 1s, GateOrder 1s) / OK [ran] [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (audit intent) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → under pace the builder also hid queued and inbox work from the drive; that's the user's requested work (they chose finishing over saving weekly usage), so only side offers wait now — test updated to assert the queue is still named [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (audit edge) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → a gate with no history runs first; SLO judged only after 20 runs; --by-model counts only tasks closed from now; unreadable usage drops nothing [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (audit operator) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → fm doctor's hook SLO reads the real events (p95 98 ms vs 150 ms now) [tree 5fc14ccb16bd] (2026-10-09T17:22:03Z)
- (audit intent) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → under pace the builder also hid queued and inbox work from the drive; that's the user's requested work (they chose finishing over saving weekly usage), so only side offers wait now — test updated to assert the queue is still named [tree 5fc14ccb16bd] (2026-10-09T17:22:11Z)
- (audit adversary) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → T-0676 adds no exec or input parsing beyond its own ledger/state files; the spend caps still refuse (check() untouched), the pace signal can only drop optional work; the guard/secrets files in the span are T-0591/T-0714/T-0722's, each closed with its own adversary lens [tree 5fc14ccb16bd] (2026-10-09T17:22:11Z)
- (audit edge) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → a gate with no history runs first; SLO judged only after 20 runs; --by-model counts only tasks closed from now; unreadable usage drops nothing [tree 5fc14ccb16bd] (2026-10-09T17:22:11Z)
- (audit operator) `main-thread review of the builder's branch (budget guard refused a reviewer subagent): hook hot path adds one plugin.json read per process after timing; Stop path imports fmbudget only where it offers side work; gate order is a stable sort with results re-listed in configured order` → fm doctor's hook SLO reads the real events (p95 98 ms vs 150 ms now) [tree 5fc14ccb16bd] (2026-10-09T17:22:11Z)
## Log
- 2026-10-09T15:40:14Z created
- 2026-10-09T17:05:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0676.builder.md
- 2026-10-09T17:09:07Z focused
- 2026-10-09T17:21:34Z merged worktree-agent-af1e2afdf10df210d (9 file(s))
- 2026-10-09T17:21:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af1e2afdf10df210d
- 2026-10-09T17:21:38Z focused
- 2026-10-09T17:22:11Z done
- 2026-10-09T17:22:11Z committed 056b373 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0519 [FEATURE M, dropped, 0 steps] Budgets and usage (C093, value 4/5, effort M, risk high)
- T-0556 [FEATURE M, dropped, 0 steps] Fast hooks (C089, value 3/5, effort M, risk med)
- T-0537 [FEATURE M, dropped, 0 steps] Gate scheduling and warm starts (C092, value 3/5, effort S, risk low)
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Lessons
- A 'degrade when over pace' rule must name what is optional: side offers and self-improvement are; the user's own queue never is.
## Files touched
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/tests/test_perf_cost.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmcli.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmhooks.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmdoctor.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmbudget.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmcore.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmideas.py
- .claude/worktrees/agent-af1e2afdf10df210d/plugin/lib/fmcost.py
- .claude/worktrees/agent-af1e2afdf10df210d/MASTER.md
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbench.py
- plugin/lib/fmbudget.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrelate.py
- plugin/lib/fmresearch.py
- plugin/lib/fmsession.py
- plugin/tests/test_builder.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_panic.py
- plugin/tests/test_perf_cost.py
- plugin/tests/test_secrets.py
- plugin/tests/test_trust.py
