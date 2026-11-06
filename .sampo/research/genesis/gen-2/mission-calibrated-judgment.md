# Mission 2 — calibrated judgment (gen 2, #8)

Task: T-2496, T-2497, T-2498, T-2499, T-2500 (briefs 1-5 in order).

Parent: gen-2/seed.md row 2 → gen-0.md #8: "It knows what it doesn't know: it states confidence, researches when
unsure, and stops for me only when something is irreversible and ambiguous. Everything else it decides and records."
gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
Stated numbers that mean something. Foreman already states them: plans carry Choice N (NN%), decisions carry a
confidence, races and doors run off two bars. What it lacks is feedback fast enough to correct them. The judgment ledger
(calibration.jsonl) holds 60 bets from 2026-10-31 on, 0 scored. A task bet settles only after SURVIVE_DAYS (30) with
no revert or re-fix (plugin/lib/fmoutcomes.py), so no bar can move before late November. The first rows already show
the likely error. T-2338 stated 75% on a pair whose base rate is 96%, so the stated numbers run under the record, not
over it. Nothing says so at the moment of stating.

## Gaps this Mission targets (coverage: #8, 64 cells filled; the I cells below are planned, open until the exam closes them)
- A fast outside signal: ship × CLI (fm ship states the chance the blocking CI jobs pass, and fm ci-watch settles it
  within hours).
- Feedback while stating: plan × CLI and understand × Claude Code (a Choice 20+ points from its type and tier base
  rate is named with that rate).
- Reading the record before it is scored: verify × MCP and verify × site (reliability bins), plus a 7-day interim read.
  The interim read is never scored and never moves a bar.
- Settling without a session: learn × headless/server and find × headless/server (the night tick runs the ledger's
  maintenance; the digest names the worst kind).
- Who stated it: understand × other agents (each bet carries its harness, so one harness's record reads apart).
- Not in gen 2: shrinking a poorly calibrated harness's numbers (learn × other agents), lead bets (find × Claude Code,
  wait for the model layer's lead-triage exam), Desktop's bar view (operate × Desktop). They stay idea cells.

## Approaches
1. Add outside signals that speak in hours and show the record at the moment of stating. A ship bet is settled by
   CI's blocking jobs. The plan gate names the base rate. An interim read and reliability bins sit in the existing
   --judgment output. Fails if: CI's verdict is Foreman's own tests and so not an outside signal. The answer: the
   jobs run on hosts Foreman doesn't control (macOS, other Pythons) and catch what a local run misses (T-2492's
   symlinked TMPDIR), so ship bets score as their own kind. Bars still move only on survival.
2. Shorten SURVIVE_DAYS to 7. Fails if: a revert in week three is missed and a held verdict that later breaks can't
   be unwritten, because bets are write-once.
3. Ask a model to judge each plan's percent. Fails if: a model's opinion becomes the signal. The model layer's rule
   is that models advise and proof decides, and a judged percent is still unscored.
4. Use what exists: fmoutcomes already has write-once bets, base rates per type and tier, settle() and adjust_bars().
   fmci already decides blocking red or green. The MCP calibration tool and the Judgment page already render
   --judgment's JSON. Approach 1 adds rows and readers to these, with no new store.

Choice: 1 on 4 (80%). The ship bet gives a scored number within hours, and the base-rate note acts on the first error
already visible. The 20% doubt is whether ship bets are numerous enough: about 5 ships a day here gives 20 in four
days.

## Exam
#8's exam kind is clean: a clean repo must be left alone, with no false alarms and no busywork (fmexam KINDS). This
Mission adds no exam kind. Its effect is measured by the ledger itself: the ship kind's Brier against its base rate
once 20 are scored, and the share of plans whose Choice sits within 20 points of the base rate before and after
brief 2. Zero-token arms run each generation. The session arms of the clean kind run at the end-of-run exam (rule 6).

## Long-horizon goal (end of run)
Across the long-horizon goals, the stated Brier beats the base rate's on the ship kind. The research bar has moved at
least once from survival outcomes, or the digest says why not.

## Lean
No new verb. fm ship gains --chance, fm outcomes --judgment gains --by harness, and the JSON gains fields. Hooks gain
nothing: the base-rate note rides the plan gate fm task set already runs, and the night tick's maintenance replaces no
hook work. Rules size and injected context don't grow.

## Tier share
Briefs 1-3 are tier 3, a capability Foreman lacks: scoring within hours, base-rate feedback while stating, and a read
before scores exist. Briefs 4-5 are tier 2. Three of five, 60%.

## Done when
Ship bets are written once per commit and settled by fm ci-watch. A plan 20+ points from its base rate gets one note
naming both numbers. --judgment shows interim reads and bins, and the MCP tool and the site render the bins. The night
tick settles due bets. Bets carry their harness. Each surface names what it measured, and the ledger's ship kind has a
first scored Brier, or the critique says how many ships it still needs.

## Briefs (fm intake)
```
FEATURE: ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed commit, the stated chance its blocking CI jobs pass; fm ci-watch settles it held or missed from the run
FEATURE: the plan's percent against its base rate: a Choice 20+ points from the type and tier base rate, either way, gets one note from the plan gate and fm next naming both numbers; never a refusal
FEATURE: interim calibration reads and reliability bins: a 7-day interim read per stated bucket (never scored, never moving a bar) and per-kind bins in --judgment's JSON, returned by the MCP calibration tool and drawn on the site's Judgment page
FEATURE: bets settle with no session: fm night's tick runs fmoutcomes.maintain; the nightly digest names the kind whose Brier trails its base rate most once 20 are scored
FEATURE: bets carry their harness: each bet row records which harness stated it, and fm outcomes --judgment --by harness splits buckets and Brier by it
```
