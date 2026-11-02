# Genesis gap map — generation 3 (2026-11-02)

Drawn at: 4992e2d2

Redrawn against the code at 4992e2d2 by targeted reads: gen 3's eight Missions and their tasks (T-2607 to T-2722),
their tests, their critiques, and the measurements on record (exam lines, outcomes, the gen-3 review on fable). The
gen-3 diff since gen 2's map (d2f4f18a) is 117 files, 5,482 lines added and 323 removed. Every later idea is checked
against this map: an idea that names something under **Built** is a duplicate unless it extends it. Tiers: 3
capability, 4 paradigm.

Source limit: the held-out exam on the production model still hasn't run (the user's testing-cadence steer keeps it
for the end of the run), so `fm exam scorecard` reads 0/13 and no capability below counts as passing. Gen 3's only
foreman grade is a Haiku smoke run (s32-015, 3 train scenarios), on which gen 3 closed 2 against gen 2's 3, so select
reverted it provisionally (lineage.md). Signals Foreman didn't author: that run, the long tier (l001, l002: foreman
0/6 true done in gen 3 as in gen 2), the gen-3 review (25 findings: 15 carried here as gaps, 7 dropped with grounds,
2 held for the user, 1 dismissed), and CI on main.

## The map (one row per capability; tier of its largest open gap)

| Area | Tier | Evidence | Missing |
|---|---|---|---|
| 1. Initiative | 3 | fm find ladder and leads (T-2185, T-2297); no gen-3 Mission | a held-out score for its kinds; no foreman arm on s21-013 (review #6) |
| 2. Exhaustive thinking | 3 | grid lens (T-2672); left-out counts everywhere (T-2673, T-2676); canaries near the idea (T-2674, T-2686) | dissents scored against outcomes; a canary rule met in intent, not only letter |
| 3. Anticipation | 3 | next-request guess shown and booked (T-2681); ship step under the grant (T-2682, T-2722); pile names the freeing action (T-2683) | shown-guess hit rate due 2026-11-09; path predictor past naive |
| 4. Goal to finish | 4 | long-tier failures classed by reach (T-2613); foreman 0/6 true done, 6 false dones, unchanged | a done claim that survives hidden checks (review #3); the grader moved, not the arm (review #12) |
| 5. Getting the tools it lacks | 3 | miss trigger, scaffolds, install queue (gen 2); no gen-3 Mission | a held-out score; user-only installs wait (T-2564) |
| 6. Verifying anything | 4 | docs proof skips history files (T-2616); unproven kinds on the receipt (T-2635); fm prove --steer (T-2636) | intent proof beyond an LLM lens; 421 docs claims fell by narrowing, not proof (review #19) |
| 7. Self-repair and self-improvement | 3 | restore drill (T-2652); dropped-class fault (T-2648); torn-ledger damage (T-2664) | a held-out score for recur and correction; friction up in gen 3 (review #2) |
| 8. Calibrated judgment | 3 | one window for every read (T-2610); the record where the chance is typed (T-2611); M-12 kill not-yet (T-2687) | a forecaster that beats chance on close survival; the survival headline over 8% of closes (review #11) |
| 9. Orchestration | 3 | model router, lane recovery (gen 2); Mission 7's briefs built in lanes, three reworked on live state | the user's model key; evidence and leases fail inside worktrees (review #23) |
| 10. Beyond code | 3 | incident ritual, docs/infra/data proof (gen 2); no gen-3 Mission | a held-out score for docs, beyond, package |
| 11. Self-triggering | 3 | the tick names what it can't watch (T-2607, T-2608); notify deliveries recorded (T-2684) | a week of live ticks (the user's install); a held-out score |
| 12. Staying lean and safe | 3 | burden by source (T-2667); nesting refused fast (T-2668); stall cap (T-2669) | session-start context grew (review #25); MASTER.md can't be read whole (review #10, #21) |
| 13. Genesis as a feature | 3 | moonshot campaign (T-2626, T-2679, T-2687); lineage names whose grade is whose (T-2691, T-2693) | a production confirm; a held-out production grade (review #15) |

## Cross-cutting findings
- **Built faster than proven, again.** Gen 3 added 5,482 lines while its one foreman grade moved down (s32-015: 2 of
  3 against gen 2's 3, untested-c-f2c372 reopened) and the long tier didn't move. The tower's own verdict reverted the
  generation, provisionally. The next Seed should pay for a production-model held-out grade before it adds machinery.
- **Built for data that doesn't exist.** Three gen-3 briefs were built and passed their tests, then did nothing on
  this project's state until review: the pile line found no asks or dependencies, the ship rule could never fire under
  an open tower, and a notify recorder serves a command no project sets. Mission 7's critique asks for a live-state
  reading in every Exam.
- **Kill tests work.** M-02's (viable, 3 of 3 modules rebuilt blind, reproduced) and M-12's (not-yet, no forecaster
  beats chance) both answered their question cheaply. M-12's first run was confounded by era and caught before filing.

## 1. Initiative
- Built: unchanged in gen 3 (fm find, leads, triggers; see gen-2/gap-map.md).
- Measured: no foreman arm on s21-013, the largest run (306 scenarios); review #6.
- Gaps: held-out initiative score, with a foreman arm on the big run (3).

## 2. Exhaustive thinking
- Built: the grid lens crosses surfaces, actors and failure modes (T-2672); every cut list says what it left out, in
  every module (T-2673, T-2676); a canary before any "not found" (T-2674), now required to sit near the idea, with a
  warning when one term covers most canaries (T-2686).
- Measured: Mission 7's grounding: 27 of 41 grid cells yielded a real gap; 169 of 170 "new" verdicts carried a canary,
  156 of them "def main".
- Gaps: dissents scored against outcomes (3) · canary quality on the next brainstorm (3).

## 3. Anticipation
- Built: session start names the next-request guess while it beats "same as last" over 20+ scored rows (T-2681), and
  fm outcomes --predictions reads shown guesses apart; fm next leads with the ship step under the user's push grant
  (T-2682), now under an open tower too (T-2722); the pile names the action that frees the most (T-2683).
- Measured: next-request 52% vs 39% over 23 scored; shown-guess rate due 2026-11-09; landed work waited 0.5 h median,
  7.6 h worst before this generation (re-picked commits since 2026-11-01).
- Gaps: path predictor past naive (3) · the week-later readings of Mission 7 (3).

## 4. Goal to finish
- Built: the long tier's grade classes a failed check that names something the goal never states (T-2613).
- Measured: foreman 0/6 true done, 6 false dones on l001 and l002, as in gen 2. Review #12: the relabel lowers the
  failure read without closing one more goal.
- Gaps: false done on long goals (4), the next Seed's top gap again (review #3).

## 5. Getting the tools it lacks
- Built: unchanged in gen 3.
- Gaps: unmeasured until the end-of-run exam (3).

## 6. Verifying anything
- Built: the docs kind skips history files and diffs a task's own commits (T-2616); a close lists what fm prove still
  can't prove beside its grade (T-2635); fm prove --steer finds vacuous rule checks (T-2636, the user's to run).
- Measured: docs 601 → 421 by a narrower rule, not by proof (review #19); meaning 571 is the largest class.
- Gaps: intent proof (4) · docs claims proven, not recounted (3).

## 7. Self-repair and self-improvement
- Built: fm drill --restore (T-2652) rehearses a host wipe; a dropped ledger class is reported as unmeasured
  (T-2648); a cut-short ledger line is crash damage accepted once (T-2664).
- Measured: the restore drill reads back 22 of 23 projects on the 1.2.50 snapshot, which predates volt's accepted
  damage; failed tool calls 1.1 → 1.6 per window and steers 0.1 → 0.3 (review #2).
- Gaps: friction rising (3) · recur and correction unmeasured (3).

## 8. Calibrated judgment
- Built: every windowed read holds an open task's grade back (T-2610); fm ship --chance prints the record beside a
  far-off number (T-2611).
- Measured: M-12's kill test: Haiku planner AUC 0.58, Sonnet rival 0.50, type-and-tier 0.49, file history 0.48 on 44
  era-matched closes; the pool lost by 0.011 Brier.
- Gaps: a forecaster of close survival past chance (3) · the survival headline over in-window losses (review #11, 3).

## 9. Orchestration
- Built: unchanged machinery; Mission 7's four briefs ran in builder lanes, and review reworked three of them on
  live state (T-2681's floor, T-2682's rule, T-2683's grouping).
- Measured: five fm lease and evidence failures inside worktrees (review #23).
- Gaps: builders record evidence where they work (3) · the model layer waits on the user's key (3).

## 10. Beyond code
- Built: unchanged in gen 3.
- Gaps: unmeasured until the end-of-run exam (3).

## 11. Self-triggering
- Built: the tick's blind list (T-2607) and its exam (T-2608); notify deliveries recorded and warned on (T-2684).
- Measured: no project sets a notify command; live ticks still wait on the user's install.
- Gaps: a week of live ticks (3).

## 12. Staying lean and safe
- Built: burden reads SessionStart's real context and splits it by hook (T-2667); the guard refuses more than 8
  nested `$(` at once and a latency test holds ten pathological shapes (T-2668); fm run --stall-usd (T-2669).
- Measured: 76 characters of injected context per turn (SessionStart 42.9); MASTER.md exceeds Read's limit (75,758
  tokens).
- Gaps: session-start context trimmed (3) · MASTER.md split so a session can read it (3).

## 13. Genesis as a feature
- Built: the moonshot campaign (catalogue, blind rating, climb, floor; T-2626), two kill tests with kept scripts and
  results (bench/moonshot), lineage lines and the reader's exam tail keyed by generation (T-2691, T-2693).
- Measured: 20 of 100 moonshots; 2 kill-tested (M-02 viable, M-12 not-yet); gen 3 provisionally reverted.
- Gaps: the production confirm (3) · a held-out production grade (review #15, 3).
