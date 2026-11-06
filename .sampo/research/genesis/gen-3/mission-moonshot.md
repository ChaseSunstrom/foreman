# Mission 8 — moonshot (gen 3): a scored market among deciders

Task: T-2687 (brief 1, the spike: M-12's kill test, which also carries the Mission's grounding and filing).

Parent: gen-3/seed.md row 8 → the Moonshot section (far-domain lens: markets and auctions; judged on novelty and value
only). gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
Borrowed mechanism: a prediction market settled by a proper scoring rule. In a market, many forecasters stake on one
outcome, and each one's weight comes from its own record of being right. Its Foreman form: before a close, several
deciders post a probability that the work survives its window, and a pooled forecast, weighted by each decider's log
score on past closes, decides whether the close stands alone or goes to an independent check. Today one decider speaks
per close, and nothing weighs it against the others by record.

## Grounding
- fmoutcomes.py:292 (T-2337, the calibration ledger): every stated confidence is a write-once bet scored on signals
  Foreman didn't author, and fmoutcomes.brier (fmoutcomes.py:624) scores it. Only one forecaster: the closing agent.
- fmoutcomes.routes (fmoutcomes.py:634): where the stated numbers score a worse Brier than the type-and-tier base rate,
  the base rate is used instead. It switches between two sources. It never pools them or adds a third.
- fmoutcomes.outcomes (fmoutcomes.py:43) labels every close: 1768 closes, 1698 held, 69 fixed later, 1 reverted. That
  gives 70 failures to settle a market on. 22 of them closed 14 or more days ago and have a commit whose subject leads
  or ends with the task's id.
- bench/moonshot/kill_m12.py, run 1 (before the spike task): held closes taken from those whose survival window had
  ended were all T-0014 to T-0198, while the failures span T-0087 to T-2542. Era leaked into the label: the base
  rate's AUC was 0.08 (inverted), and the two LLM forecasters were at chance (AUC 0.40 and 0.51). Its not-yet says
  nothing about forecasting, so the spike reruns with a label equal to the forecast's question (a fix or revert within
  14 days) and each failure paired with the held close nearest it in id.
- fmanergy.py (T-2563) and the ledger hold no refusals: the anergy store is empty (bypass mode shows no prompts), and the
  ledger has 55 approval_granted rows and no declined ask. That blocks M-13 (below), not M-12.

## Ideas (each with its prior art, how ours is better, and a novelty mark)
### M-12 · Weight deciders by a scored market on whether a close survives (the spike)
Before a close, the planner, a cold rival read and record-based models each post a probability that the work survives
its window. Log-scored payouts set each decider's weight; a pooled forecast below a bar sends the close to independent
replication or the user.
Prior art: Metaculus and Good Judgment pooling; Hanson's idea futures; ensemble stacking; Foreman's calibration ledger
(one forecaster) and routes() (a switch between two).
Better by: weights come from each decider's own record on this project's closes, settled by outcomes Foreman didn't
author, and the pool is checked out of sample before it decides anything.
Novelty: 3
### M-13 · Price the user's attention and cap unreviewed output to it
Fit the user's price for an interruption from their answers, dismissals and overrides; ask only when a question's
value beats it.
Prior art: interruption-cost models in HCI, Kanban WIP limits; Foreman's doors (T-2342) and anergy (T-2563), both
fixed rules.
Better by: the threshold is learned from the user's revealed choices and checked on held-out ones.
Novelty: 4
Kill: not-yet. The ledger records 55 approvals and no refusal, so no model can learn what the user turns down. Needs:
a record of each declined ask and dismissed question (T-2688).
### M-11 · Auction the queue by calibrated yield and Kelly-size each stake
Each queued task bids its calibrated chance of a strong close times its value over its predicted cost; a run funds
the best bids first.
Prior art: Kubernetes priority classes, Mesos DRF; Foreman's inbox ranking (T-0111), fm run --stall-usd (T-2669).
Better by: order and stake come from the user's calibrated record, backtested before it runs.
Novelty: 3
### M-09 · Settle work between strangers by escrow released on replayed proof
Work from another agent or person is paid from escrow only when its proof replays green on the buyer's machine.
Prior art: bug bounties, Gitcoin, code escrow services.
Better by: release is a rerun, not a reviewer's judgement.
Novelty: 4

## Approaches
1. Spike M-12 as its kill test: replay closed tasks with known fates, let forecasters post blind (two reading the
   work, two from the record), and score the log-weighted pool against the best single one out of sample. Fails if: the sample is too small to tell 0.02 of
   Brier apart. The answer: leave-one-out weights over all rows, and a bootstrap that reports how often the margin holds.
2. Build the market into fm task finish now. Fails if: a pool that doesn't beat its best member adds calls and cost to
   every close.
3. Use what exists: the calibration ledger already settles bets on outside signals; the spike reads fmoutcomes.outcomes
   and the git history and changes nothing.
4. Do less: route on the base rate alone, as routes() already can. Fails if: it can never use what a diff shows.

Choice: 1 on 3 (70%). The 30% doubt is the sample: 22 pairs is small, and LLM forecasters reading a diff may add
noise rather than signal. A cold rival read (fm second rival) added walk-forward weights beside leave-one-out.

## Exam
No exam kind (a moonshot is judged on novelty and value). The spike's check: on every failed close 14+ days old with a
findable commit (22), each paired with the held close nearest it in id, the log-weighted pool's Brier, with
leave-one-out weights, beats the best single forecaster's by 0.02 or more → viable; otherwise not-yet, with the
measured margin and its bootstrap interval in not-yet.md. Result: not-yet (margin -0.011, interval -0.039 to +0.016).

## Campaign (MOONSHOT.md part A)
- Advanced: M-02 kill (T-2679)
- M-12 kill (T-2687): not-yet. No forecaster beat chance (AUC 0.58 at best), and the pool scored Brier 0.286 against the best single's 0.275 on 22 failed and 22 era-matched held closes. Its blocker and two tries are in not-yet.md.
- M-13 kill: not-yet (no refusals recorded); its need is captured as T-2688.

## Long-horizon goal (end of run)
A close's verdict comes from deciders weighted by their record on this project, and each decider's weight is a number
anyone can recompute from the ledger.

## Lean
The spike is one script run against existing state (outcomes, briefs, git history); it adds no verb, no hook and no
state file. Building the market waits on a viable kill test.

## Tier share
Brief 1 is tier 4: no harness weighs its own deciders by a scored record.

## Done when
The kill test has run, its verdict and numbers are in moonshot.md under M-12 (Stage: kill, Evidence: the spike's task),
and a not-yet verdict is in not-yet.md with its blocker.

## Briefs
Filed directly as T-2687 (the spike, closed with its verdict) and T-2688 (M-13's need: refusals recorded), so no
fm intake block remains.
