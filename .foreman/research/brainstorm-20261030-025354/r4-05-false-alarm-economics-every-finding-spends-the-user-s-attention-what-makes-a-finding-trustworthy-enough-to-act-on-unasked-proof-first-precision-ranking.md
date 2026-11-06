# Brainstorm — lens: false-alarm economics: every finding spends the user's attention; what makes a finding trustworthy enough to act on unasked (proof first, precision, ranking)

Answering one earlier question through this lens: a finished project and a dry queue look the same until you measure how often the user finds the same bug first. Ideas 6 and 11 below produce that signal.

- **Subtract what the user already knows** — FEATURE — value 5 — effort M — risk low — category: marginal info
  Why: assumption: a finding is worth only what the user wouldn't learn anyway, and a red gate, a TODO/FIXME or an open issue already tells them. Nothing in the pack subtracts those.
  Done when: on a fixture with a failing gate, a FIXME and a matching issue, a finding for each is withheld with a "known: <source>" line, and an unknown bug is still shown.

- **Make drops carry a reason chip** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: the pack learns from drops and reverts but treats them as one signal. Five chips (wrong, known, obvious, not now, not mine) would each feed a different learner: probe precision, subtract-known, holdout value, defer and ownership.
  Done when: a drop with each chip changes exactly the matching ledger and no other, and a drop with no chip still works.

- **Gate surfacing on a precision lower bound** — FEATURE — value 4 — effort S — risk low — category: statistics
  Why: assumption: a probe with 2 keeps in 2 tries has 100% raw precision, so a raw-rate floor lets lucky small samples through. A Wilson or Beta lower bound, seeded from the exam's clean-twin run, stops that.
  Done when: a probe with 2 of 2 keeps stays silent, and one with 40 of 50 surfaces. A unit test pins the bound for 5 sample sizes.

- **Elicit the user's false-alarm tolerance in plain odds** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the pack has an attention price and a daily purse, but the user never states a tolerance. One question ("is 1 wrong in 4 fine, or should I miss more to be right more?") would set the surfacing threshold and put it in the receipts.
  Done when: answering "1 in 4" sets a target precision of 0.75 that the threshold step reads, and `fm find` prints the setting and how to change it.

- **Sense fatigue from dismissal speed** — FEATURE — value 3 — effort M — risk med — category: implicit signal
  Why: assumption: a card dismissed in under 2 seconds or never opened is skimmed, not judged. That is a cheaper fatigue signal than asking, and nobody in the pack reads it.
  Done when: a replayed log of 5 quick dismissals in a row halves the next shift's card cap and writes one journal line saying why.

- **Deliver findings at commit and close boundaries** — FEATURE — value 4 — effort M — risk low — category: timing
  Why: assumption: the same card costs less at a natural pause (after a commit, gate green or task close) than mid-edit. The pack varies hunting and quiet hours but not when a card arrives.
  Done when: with a run mid-edit, a ready finding stays queued, and it appears on the next close or commit event. A test checks both.

- **Render findings from verified facts only** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: model prose such as "critical" or "serious" inflates urgency and builds false-alarm distrust. A template filled with test name, expected vs observed and caller count carries no adjectives, and severity comes from a table.
  Done when: the card has no free-text field from the finder. A lint fails any template slot not backed by a recorded fact.

- **Close the loop when muted findings turn out real** — FEATURE — value 3 — effort M — risk low — category: recall regret
  Why: mutes and floors protect attention but silently cost recall. Matching the user's later fix commits against suppressed fingerprints would catch a mute that was wrong.
  Done when: a fixture where a muted fingerprint is later fixed by the user logs a "missed by mute" event and restores that probe's weight one notch.

- **Cool the neighbourhood after a drop** — FEATURE — value 3 — effort S — risk low — category: rate limit
  Why: a wrong finding in a file signals that the nearby ones are probably wrong too, because probes are correlated by path and idiom. "Mute a path" exists but is manual.
  Done when: after a drop, new findings under the same directory need a higher score for 14 days, and a test shows a high-score one still passes.

- **Withhold a random tenth of proven findings to measure obviousness** — FEATURE — value 4 — effort M — risk med — category: counterfactual value (wild)
  Why: keep/drop tells you if the finding is right, not if the user would have found it anyway. If they fix a withheld one on their own within 14 days, its kind was obvious, and rank should say so.
  Done when: 10% of eligible findings are held back and logged, and a rediscovery rate per kind appears in the scorecard. The user can opt out with one setting.

- **Run the finding rate like TCP congestion control** — FEATURE — value 3 — effort S — risk med — category: rate control (wild)
  Why: add one card per day on each keep and halve the cap on each drop. It replaces a fixed cap with a self-tuning one and recovers slowly from cry-wolf streaks.
  Done when: simulating a keep, keep, drop, drop sequence gives caps of 2, 3, 1, 1 as specified, and the cap is shown in the card header.

- **Say how many of tonight's cards are expected to be wrong** — FEATURE — value 3 — effort S — risk low — category: expectation setting (wild)
  Why: a false card hurts more when it looks guaranteed. A header like "4 shown, I expect 1 to be wrong" from the probes' lower bounds makes errors expected and lets calibration be checked later.
  Done when: the header's expected-wrong figure equals the sum of (1 − lower bound) over the cards, and the weekly scorecard compares it to actual drops.

- **Hold a silent week and compare it with the loud one** — FEATURE — value 3 — effort M — risk low — category: cost of silence (wild)
  Why: nobody has measured what no initiative costs. One week per quarter of private logging, then the top 3 it would have raised and what the user did meanwhile, answers whether the whole feature earns its attention.
  Done when: `fm find silence 7d` logs without notifying, and the end-of-week report lists proven findings and which the user fixed independently.

Next question: When a finding's fix is correct but the user's reaction is "I didn't want that touched", which ledger records it: precision, scope or taste?
Next question: Does the user's keep/drop rate differ by the surface the card arrives on (pane, web, phone), and should the cap and threshold follow the surface?
