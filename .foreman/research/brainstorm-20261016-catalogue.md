# T-1029 brainstorm catalogue (2026-10-16)

Source: research/brainstorm-20261015-221834 (3 rounds + 3 deepening rounds, 6 lenses, run past the two earlier
brainstorms with --seen; ~270 distinct ideas, 215 of them near a finished task) plus research/community-wants-20261016.
Every cluster was grounded against the code by three fm-recon passes (file:line evidence in this task's log).
Score: value 1-5 · effort S/M/L · mark.

| # | Cluster (ideas in it) | Grounding | Value | Effort | Mark |
|---|---|---|---|---|---|
| C1 | Resume stopped work: one-verb resume, resume capsule per worktree, checkpoint ref, offer at SessionStart and in the pane, resume --all, salvage partial work, heartbeat silent lanes, orphan supervisor | MISSING beyond `fm resume` printing a point; lanes bind lane/lane_branch on focus | 5 | M | BUILD (T-1028, widened) |
| C2 | Known fixes maturity: seed from git history, fix ladder to rule/test, "why it fired" receipt, drift staleness, non-Bash obstacles, weekly learned report | T-1032 shipped store/learn/recall/trust/retire/escalate; seeding, ladder, non-Bash and report MISSING | 4 | M | BUILD report + seeding (with C12, C13); skip auto-drafted regression tests (L, low precision) |
| C3 | Corrections become rules: mine repeated corrections, promote to rules, check diffs against past steers | PARTIAL: corrections are logged (fmhooks 578-615) and read by friction/taste; no repeat detection or promotion | 5 | M | BUILD |
| C4 | Portability & team brain: AGENTS.md/Cursor/Gemini export, brain by git pull, team queue, signed packs, eject | PARTIAL: `fm export agents` writes AGENTS.md; no .cursor/rules, no GEMINI.md export, fixes not exported | 4 | S | BUILD exports; skip team queue and signed packs (speculative) |
| C5 | Overnight: queue work overnight with a morning receipt, rate-limit pacing, watchdog | PARTIAL: fm night runs fixed jobs only; pacing exists in fm serve | 4 | M | BUILD |
| C6 | Reliability: orphan claude -p reaping, child deadlines, torn writes, state rollback on upgrade, chaos soak, crash-loop breaker, idempotent Stop | breaker EXISTS; claude -p helpers lack process-group kill and an orphan sweep; no state rollback | 4 | S | BUILD reaper + sweep; skip rollback and soak for now |
| C7 | Performance: ledger index, card selector memo, pane wake pipe, worktree warm pool, incremental worktree list | hooks within budget (bench green); pane polls fm ui every 2 s and lists worktrees each gather | 3 | S | BUILD a measurement first (profile fm ui gather); skip the rest until it shows a cost |
| C8 | Cards by import/dep, lazy bodies, version drift | — | 5 | M | IN T-1036 / T-1037 |
| C9 | Pane: colourblind palette, layout sweep, actionable Agents nodes, idle "what I learned" screen, time scrubber | motion setting EXISTS; one palette; few fixed sizes in tests | 3 | S | BUILD layout sweep; idle learned line with C12; resume action with C1; skip palette and scrubber |
| C10 | Safety: builder OS sandbox, tainted web/MCP content, outbound ledger, dependency checks before install, output secret scan | secret scan EXISTS; injection note on web/MCP results, no taint gate; no npm/pip install check | 4 | M | BUILD dependency-install check; tainted-content gate in round 2 |
| C11 | PR/CI loop: CI-watch until green, review threads, issues→tasks, merge train, bisect | issues→tasks and bisect EXIST; no CI watch | 4 | L | ROUND 2 |
| C12 | Measuring improvement: interventions per task, minutes lost, unused features, A/B holdout, scoreboard, replay failures | minutes lost and unused features EXIST; no per-task interventions, no scoreboard | 4 | M | BUILD (one report with C2) |
| C13 | Onboarding: start ritual, "what Foreman would do" preview, first brain from git history | fm adopt builds map/gates/secrets; no git-history mining | 3 | M | BUILD with C2 seeding |
| C14 | Alerts: push when blocked, phone answers, OSC notify, speak status | push and OSC EXIST | 2 | S | SKIP (covered) |
| C15 | Cost: per-task cap, task forecast, cache-break attribution, Haiku routing | daily caps, cost by task, scout on Haiku EXIST | 3 | M | SKIP for now (no measured overspend) |
| C16 | Backlog: deferred triage, weekly decide digest, rank by evidence, sunset clauses | digest has decisions; nothing triages deferred | 3 | S | BUILD |
| C17 | Brainstorm machinery: governor, dedupe, clustered history | rounds/dry/seen EXIST | 2 | M | SKIP |

## Slate (build marks, value for effort)
1. T-1028 widened: resume stopped worktree work (capsule, SessionStart offer, pane action, resume --all, salvage) — C1, C9
2. Corrections that recur become proposed rules on their own — C3
3. Export the learned brain to Cursor and Gemini, known fixes in AGENTS.md — C4
4. Process-group reaper and startup orphan sweep for claude -p helpers — C6
5. "What Foreman learned" report: fixes new/worked/missed, rules from corrections, interventions per closed task; in fm digest and the pane's idle line — C2, C12, C9
6. fm night works unblocked queue tasks under a spend cap and leaves a morning receipt — C5
7. Seed lessons and known fixes from git history (fm adopt, and on demand) — C2, C13
8. Deferred-work triage (drop/do/ask) in fm digest and fm tidy — C16
9. Dependency-install check in the guard (new npm/pip/cargo packages: age, typosquat, registry) — C10
10. Pane layout sweep test over many sizes — C9
11. Profile fm ui gather and memoize what's slow (measure first) — C7
Round 2 (captured): CI-watch loop until green (C11); tainted web/MCP content gate (C10).
