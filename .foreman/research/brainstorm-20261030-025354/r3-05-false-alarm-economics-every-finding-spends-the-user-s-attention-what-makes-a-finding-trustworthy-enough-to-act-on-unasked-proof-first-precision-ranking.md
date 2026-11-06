# Brainstorm — lens: false-alarm economics: every finding spends the user's attention; what makes a finding trustworthy enough to act on unasked (proof first, precision, ranking)

- **Charge each finding an attention price and set a daily purse** — FEATURE — value 5 — effort M — risk low — category: attention budget
  Why: the pack's earlier ideas cap findings per day and price them in minutes, but nothing ties the two. The exam showed deterministic finders found 0/108 planted defects, so a noisy replacement could easily flood the user. Assumption: the user's attention is the scarcest resource, not tokens.
  Done when: `fm find` shows each finding with an estimated read-and-decide cost in seconds, and with a purse of 10 minutes stops surfacing once the running total passes it, queuing the rest unseen.

- **Gate surfacing on a measured precision floor per finding kind** — FEATURE — value 5 — effort M — risk med — category: precision gate
  Why: Mission 3 is graded on the exam's `none` and `bug` kinds; a finder that fires on `none` repos is pure false-alarm cost. Assumption: exam labels can be replayed to compute precision per kind.
  Done when: a kind whose exam precision is below the configured floor (default 0.7) is reported only as "suppressed: N candidates" in `fm find`, and a test with a fixture of planted-clean repos shows zero surfaced findings.

- **Print a false-alarm bill after every scan** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: the user steers on cost and noise ("Dropped" items show they reject noisy filings). Assumption: dropped or settled findings can be counted per scan.
  Done when: each scan ends with a line like "7 candidates, 2 proven, 1 shown, est. 90s of your time; last 5 scans: 3 acted on, 4 dropped", derived from the findings ledger.

- **Require a stable red on three runs before a finding may interrupt** — FIX — value 5 — effort M — risk low — category: proof
  Why: flake-shaped false positives are the cheapest way to lose trust; the pack lists "drop any finding whose repro isn't stable" only as an idea. Assumption: the repro command can be rerun cheaply.
  Done when: a finding whose repro goes red/green/red is filed as "unstable" in the ledger, never shown on the morning card, and a test with an injected flaky repro confirms it.

- **Rank by acted-on rate, not by finder confidence** — FEATURE — value 4 — effort M — risk med — category: ranking
  Why: model confidence is uncalibrated; the only outside truth the user trusts is `fm outcomes` survival and revert history. Assumption: landed fixes can be joined to 30-day survival.
  Done when: rank weights per kind are recomputed from the ledger (landed and survived over shown), and a unit test shows a kind with three reverts falls below a kind with three survivals.

- **Make a revert the loudest signal and mute a probe on it** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: a user reverting a unasked fix is the clearest "false alarm" the pack can observe; earlier ideas mention learning from reverts but not an automatic mute.
  Done when: reverting a fix commit within 7 days sets its probe to "probation" (shadow-only) and `fm find` says why, with a test covering the revert detection.

- **Show a trust line with each finding: proof, runs, reach, prior hit rate** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: acting unasked requires the user to judge in seconds; a fixed one-line form beats prose. Assumption: those four facts are all in the ledger.
  Done when: every shown finding has a single line "red 3/3 on untouched tree · 2 callers · probe bug-null: 8 of 10 landed" and a lint test fails on a finding missing any field.

- **Escalate by consequence: silent, card, or interrupt** — FEATURE — value 4 — effort M — risk med — category: interruption policy
  Why: a typo in docs and a data-loss bug should not cost the same attention. Assumption: severity can be bounded by the proof (crash, wrong data, cosmetic).
  Done when: findings route to three channels by proven severity, and only a proven crash or data-loss finding with precision above the floor can trigger a notification, verified by a routing test table.

- **Wild: Run a decoy audit that mixes known-false findings into the card** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: assumption: the user's accept/drop habits on seeded dummies measure their own false-positive tolerance, so the purse and floor can be tuned to them rather than guessed. Wild.
  Done when: a flagged `--calibrate` run inserts labelled dummies in a scratch copy, never the real queue, and reports the user's drop rate per kind.

- **Wild: Hold every finding overnight and re-prove it at dawn** — FEATURE — value 3 — effort S — risk low — category: cooling-off
  Why: assumption: repo drift, a rebase or a concurrent commit makes a night-old finding stale; a cooling-off re-proof costs pennies versus a wasted morning decision. Wild.
  Done when: the morning card only lists findings whose repro is still red on the current HEAD, and shows "N expired overnight".

- **Wild: Let a finder stake credit that it forfeits on a drop** — FEATURE — value 3 — effort M — risk low — category: reputation
  Why: assumption: a per-probe credit balance (earn on survive, lose on drop) gives a simple, explainable throttle that replaces tuned thresholds. Wild.
  Done when: a probe at zero credit can only run in shadow mode, and `fm find credits` lists balances with the events that changed them.

- **Show an "unseen but proven" counter instead of delivering low-value finds** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: the pack's "do nothing receipt" idea stops short of counting what was withheld. Assumption: users prefer knowing the pile exists to seeing it.
  Done when: the glance line shows "3 held (low value)" and `fm find held` lists them, never nagging again unless the count passes a set size.

- **Audit the ranker against survival with a monthly scorecard** — CLEAN — value 3 — effort M — risk low — category: calibration
  Why: the pack's open question asks whether exam deltas predict 30-day survival; the same question applies to rank order. Assumption: enough landed fixes exist to compute rank correlation.
  Done when: `fm find audit` prints the correlation between rank at filing and survival at 30 days, and warns when it falls below zero.

Next question: What is the user's actual tolerance, in findings per week and seconds per finding, before they stop reading the card, and how would Foreman measure it without asking?
Next question: When a finding is correct but the user doesn't care, is that a false alarm, and which signal (ignore, snooze, drop) separates "wrong" from "not now"?
