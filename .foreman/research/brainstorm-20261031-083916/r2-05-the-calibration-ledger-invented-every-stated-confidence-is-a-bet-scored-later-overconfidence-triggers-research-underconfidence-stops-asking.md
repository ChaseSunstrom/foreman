# Brainstorm — lens: the calibration ledger (invented): every stated confidence is a bet scored later; overconfidence triggers research, underconfidence stops asking

Earlier questions my lens can answer: confidence numbers Foreman states are the clearest case of a figure checked only by the code that wrote it, and a model is on both sides wherever it writes a confidence and a model-judged check then grades it. Both are addressed in ideas 1 and 4.

- **Pre-register every bet through a hook the model can't write** — SECURITY — value 5 — effort M — risk med — category: integrity
  Why: assumption: ledger ideas exist, but a confidence typed into a task file can be edited after the outcome. Hook-stamped entries (hash, time, claimant, resolver) make the score un-gameable.
  Done when: editing a recorded confidence in the task file leaves the ledger's hash unchanged, and `fm doctor` reports the mismatch.

- **Make every bet name its resolver at the moment it's placed** — FEATURE — value 5 — effort S — risk low — category: scoring
  Why: assumption: unscorable confidences ("probably fine") silently inflate a ledger. Each entry needs a command, event or date that resolves it. Otherwise it's a "dangling bet", counted by `fm doctor`.
  Done when: a plan with a confidence and no resolver is refused, and doctor prints the dangling count.

- **Show the recalibrated number beside the stated one** — FEATURE — value 5 — effort M — risk med — category: calibration
  Why: assumption: Foreman says "90%" but past 90%s held 70% of the time. Fit bins per claimant and tier (shrunk toward a global prior until n≥20) and print "said 90, history says 70".
  Done when: after 20 scored bets, a task's plan shows both numbers, and a synthetic ledger of always-wrong 90s yields ≤75.

- **Gate the plan on the ledger's miss-heat of the touched paths** — FEATURE — value 4 — effort M — risk low — category: research trigger
  Why: Mission 5's blast radius already lists co-change neighbours. Combine that with past high-confidence misses in those same paths, so research fires where Foreman has been confidently wrong before, not on a keyword.
  Done when: a task in a path with 2+ prior confident misses can't focus without a research note, and a clean path isn't blocked.

- **Retire a question class using a Wilson lower bound** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: assumption: the user's most tiring cost is repeated asks. Log each `fm ask` with the answer and whether it matched Foreman's default. When the lower bound of agreement passes 0.9 with no reversals, decide and file a one-line undo receipt. A reversal reopens the class.
  Done when: after 8 matching answers the ninth same-class ask becomes a receipt, and a reversal restores asking.

- **Price each stop in the user's regret minutes** — FEATURE — value 4 — effort S — risk low — category: asking
  Why: assumption: the user hates unneeded stops but wants irreversible ones. Ask only if P(wrong) × minutes-to-undo exceeds a price the user sets once (`fm mandate`-style, user-only).
  Done when: two decisions with equal confidence but undo costs of 1 and 90 minutes produce no ask and an ask respectively.

- **Resolve auto-decisions by silence and by undo** — FEATURE — value 4 — effort S — risk low — category: outcomes
  Why: assumption: Foreman has no ground truth for "decided without asking". A decision the user doesn't undo within a window scores a hit and a used undo scores a miss. This is a signal Foreman didn't author.
  Done when: using an undo receipt flips the matching ledger entry to a miss within one command.

- **Report resolution, not just Brier** — CLEAN — value 3 — effort S — risk low — category: scoring
  Why: assumption: a model that always says 70% looks calibrated while saying nothing. Print sharpness and the Brier decomposition so hedging is visible.
  Done when: a ledger of constant 0.7 bets scores "calibrated, zero resolution" in `fm doctor`.

- **File every sub-10% surprise as a root-cause capture** — FEATURE — value 4 — effort S — risk low — category: learning
  Why: the signal-to-fix loop (Mission 8) needs 3+ recurrences. A single event Foreman gave under 10% is itself evidence of a wrong assumption, and the first occurrence should ask why.
  Done when: a failure after a stated 95% creates exactly one capture quoting the assumption.

- **Earn autonomy through a floating ask threshold** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: assumption: one fixed gate for every project is wrong. The ask and race thresholds move with rolling calibration, tighten after misses and relax after streaks, within user-set bounds, with every shift logged.
  Done when: a synthetic run of 10 misses raises the threshold, and the bound caps it.

- **Wild: Run a calibration quiz against the user** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; assumption: the user would enjoy a ground truth Foreman doesn't author. `fm bet` has the user and Foreman each guess "will this test pass first try?", then scores both. It also feeds the user-twin idea with real data.
  Done when: after 10 bets, the report shows the user's Brier beside Foreman's.

- **Wild: Shade the diff by calibrated chance each hunk is right** — FEATURE — value 3 — effort L — risk med — category: UI
  Why: wild; assumption: the web UI has a diff view. Per-hunk gutter tint from the recalibrated odds, so review time goes to the pale parts.
  Done when: a hunk touching a high-miss path renders visibly different from a low-risk one, and a screen reader gets the number.

- **Wild: Publish a weather forecast, scored in public** — FEATURE — value 3 — effort S — risk low — category: site
  Why: wild; assumption: the site already refreshes stats daily (T-2326). Add "today: 80% of tasks pass first try" with yesterday's forecast and result beside it.
  Done when: the site shows a forecast and last day's actual, and the forecast is stamped before the day's tasks.

- **Wild: Send a cold child to take the other side of each big bet** — FEATURE — value 3 — effort M — risk med — category: adversary
  Why: wild; assumption: a Haiku child with no plan context states its own odds for the claim. Only a gap above 0.3 triggers research, so the cost stays bounded.
  Done when: a seeded wrong claim shows a gap and fires research, and a trivial one doesn't.

Next question: which stated confidences does the user override without comment (accepting a plan unread, or rerunning a check), and does that silence mean trust or fatigue?
Next question: what outcome sources exist that neither the model nor Foreman's code writes (CI results, reverts, user edits), and which of them could resolve bets without extra cost?
