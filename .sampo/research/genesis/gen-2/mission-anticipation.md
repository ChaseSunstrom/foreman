# Mission 6 — anticipation (gen 2, #3)

Task: T-2554 (brief 1).

Parent: gen-2/seed.md row 6 → gen-0.md #3: "Anticipation. A model of me, my projects and my machines (requests,
corrections, habits, what breaks). It predicts the next request and drafts it on spec in a lane, and flags problems
before they happen (grow `fmforesight`)." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here
unchanged.

## Capability
A model of the user built from the user's own asks only. Grounded before filing, most of #3 is built: the prediction
book scores each next-request prediction against a baseline (T-2406: 62% hit against the baseline's 56% now) and mutes
a kind that trails its baseline after 20 scored rows. The top prediction is planned ahead while it beats its baseline
(T-2407: a plan, never code). The foresight sweep flags CI red, setup changes and, since T-2542, timers that stopped
firing.
What it lacks: the user model's input isn't the user's. fmforesight._requests reads every brief whose source is
"user", and two kinds of Foreman-made briefs carry that source. First, Genesis Mission briefs: Foreman writes them, and
the session files them with fm intake --file, which records source user (T-2532, T-2542 and T-2546 all read source:
user). Second, mistaken captures: 72 of the 101 dropped user-source briefs have drop notes about a mistake, a sample
or debugging. Today's T-2548 and T-2549 are two of them. So the predictor learns Foreman's own Missions and slips as
the user's habits.

## Grounding
- Brief 1: fmforesight._requests (plugin/lib/fmforesight.py) filters on source == "user" only; fm intake --file
  records source user for Mission briefs (T-2532, T-2542, T-2546); 72 of 101 dropped user-source briefs were mistakes,
  samples or debugging (drop notes).

## Gaps this Mission targets (coverage: #3, 58 empty cells; the I cells below are planned, open until the exam closes them)
- The user's own asks, cleanly: understand × CLI, learn × CLI, learn × headless/server (the prediction book and the
  night tick read a request stream with the tower's briefs and mistaken captures left out).
- Not in this Mission (grounded as built): walk-forward scoring and muting (the prediction book), a lane plan for the
  top prediction (T-2407), an already-built nudge at capture (T-2546's backtest met no bar). They stay idea cells.

## Approaches
1. Clean the stream at its one reader. fmforesight._requests leaves out briefs that any Genesis Mission's Task line
   names (fmgenesis.TASKS already parses them) and briefs dropped with a mistake note. fm intake gains --source, and
   the Genesis step's intake line says --source genesis, so new Mission briefs are filed as the tower's. Fails if: a
   Mission brief the user later took up as their own drops out. The answer: the user's own requests are still filed by
   the user's own words through capture, which the filter never touches.
2. Relabel the old briefs' source in place. Fails if: it rewrites history in briefs other tools read, and an edit to
   1,164 files is a large, irreversible step for a filter that one reader can apply.
3. Weight user-source briefs by whether they were done. Fails if: dropped asks are real signal too (the user changed
   their mind), so weighting by outcome hides that.
4. Use what exists: TASKS (fmgenesis) names every Mission's briefs, drop notes are in the briefs, and _requests is
   the single reader the prediction book and the lane plan share. Approach 1 changes only that reader and adds one
   intake flag.
5. Do less: only the --source flag for new intakes. Fails if: the 40-plus Mission briefs and 72 mistakes already filed
   keep polluting the model.

Choice: 1 on 4 (80%). The filter is reversible and sits at one reader. The 20% doubt is whether the cleaned stream
predicts better or only differently. The backtest below decides.

## Exam
#3's exam kinds are the prediction book's own scoring and the watch kind (work started from replayed events against
a hidden key). The deciding check is a walk-forward replay of the prediction book on the scored rows Foreman already
has: hit rate and baseline gap with the old stream and with the cleaned one, on the same requests. The cleaned stream
must not score below the old one. If it does, the filter ships only for new Mission briefs (approach 5) and the
critique reports why. Zero-token arms run each generation, and the session arms run at the end-of-run exam (rule 6).

## Long-horizon goal (end of run)
Across the long-horizon goals, no Genesis Mission brief and no capture dropped as a mistake is counted as a user
request, and the prediction book's hit rate stays at or above its baseline.

## Lean
No new verb. fm intake gains --source. _requests gains two filters, applied where it already reads the briefs. Hook
p95, rules size and injected context don't grow.

## Tier share
Brief 1 is tier 3, a capability Foreman lacks: a user model fed only by the user. One of one, 100%.

## Done when
fmforesight._requests leaves out briefs named by a Mission's Task line and briefs dropped as mistakes. fm intake
--source genesis files the tower's briefs under that source, and the Genesis step's intake line says so. The
walk-forward replay is recorded with both streams' hit rates, and the cleaned one is not lower.

## Briefs (fm intake)
```
FEATURE: the user model reads the user's own asks: fmforesight._requests leaves out briefs a Genesis Mission's Task line names and briefs dropped as captured by mistake; fm intake --source genesis files the tower's briefs as its own and the Genesis step's intake line uses it; a walk-forward replay of the prediction book on both streams must not score lower with the cleaned one
```
