# Brainstorm — lens: unspoken needs

**Answers to earlier questions, from this lens**
- *Which pages does a session path actually reach?* The user has said that every capability must be called by a session path (the standing reach rule). The unspoken need is that they never have to open a page. Anticipation should therefore show up in `fm next` and the SessionStart line first, and the web UI should only mirror it.
- *Which cells would stay empty under the n/a counterexample rule?* Probably the cells for non-Claude harnesses, which depend on T-0335 and T-0337, and the unattended cells. These are the true gaps.

**Ideas**

- **Quarantine test and debug captures from the user model** — FIX — value 5 — effort S — risk low — category: data hygiene
  Why: two drops read "captured by mistake: a sample line fed to fm intake while debugging T-2547's test". A model of the user built on that input predicts requests the user never made.
  Done when: a capture made under a test or debug flag, or from a fixture path, is excluded from the asked stream, and a planted junk line never appears in a forecast.

- **Backtest every predictor walk-forward before it may draft** — FEATURE — value 5 — effort M — risk low — category: foresight
  Why: the Lessons section says T-2546's word-overlap matcher "met no bar", and the user's rule is "measured, not authored". The user would otherwise find out a predictor is noise only after it drafts junk.
  Done when: `fm foresight` refuses to draft from a predictor with no recorded walk-forward hit rate against a shuffled-history control, and prints the rate.

- **Predict the user's drop before Foreman files a self-filed task** — FEATURE — value 4 — effort M — risk low — category: negative model
  Why: the dropped list shows five items, each "measured" or "built", and the queue holds 20+ deferred "Later from" bundles. The user spends attention rejecting Foreman's own filing.
  Done when: a self-filed task that matches the signature of a past drop is held, with the matching drop id named, and the held rate is reported.

- **State the likely re-scope at capture** — FEATURE — value 4 — effort M — risk med — category: premise check
  Why: three "steered" entries are re-scopes after reading code (fmdoors, the BEYOND row, `--by harness`). The user corrects the premise every time.
  Done when: `fm task new` prints one line naming the module or flag the request touches and the existing behaviour that could change it, and a replay over the 5 steered cases hits at least 2.
  Assumption: the premise line is derived by grep of MASTER.md and `fmdoors`-style modules, with no model call.

- **Give each of the 58 cells a planted-history probe** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the user's rule is that a cell counts only if it names a concrete capability grounded in a file. A probe with a known next request makes the cell testable, and it also covers the question "does a cited file still behave as claimed".
  Done when: each filled cell names a probe that fails on the parent of its feature commit, and the sweep re-runs the probes.

- **Keep a per-machine failure profile** — FEATURE — value 3 — effort M — risk low — category: machines
  Why: the pack shows machine-specific trouble: ETXTBSY (T-2543), the missing setuptools on python3 (T-2529), the children dir under `/run/user` (tmpfs), a hardened kernel, and the missing libappindicator (T-0325).
  Done when: `fm doctor` and the SessionStart line warn once when a task touches something on that machine's recorded failure list, and each warning cites the past incident.

- **Cap foresight at one line and mute it after two dismissals** — FEATURE — value 4 — effort S — risk low — category: restraint
  Why: the lean ratchet and the "pay by deletion" steers show the user refuses unearned context. Anticipation that nags is unwanted weight.
  Done when: a session shows at most three flags, a signature dismissed twice stays silent, and each shown flag's lead time is logged.

- **Resolve every prediction to hit, miss or expired, and show the abstain case** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the bets machinery exists, but a forecaster that returns an empty list is indistinguishable from one that is broken.
  Done when: a forecast output reads "abstained: evidence floor 3 not met" or "failed: <reason>" and never an empty list, and `fm outcomes` scores forecasts.

- **Check that all four non-Claude harnesses yield the same asked records** — FIX — value 3 — effort M — risk med — category: harness parity
  Why: steers say Foreman is not Claude-specific, and the open questions ask whether stage data matches. A model of the user built only from Claude transcripts misses work done under codex, gemini, opencode and `fm code`.
  Done when: a fixture transcript from each harness produces an identical asked-record schema, and the sweep goes red on a missing one.

- **Wild: run a stub-user twin built only from steers** — FEATURE — value 4 — effort L — risk med — category: steer check
  Why: the user has made 30+ steers, and a feature can violate one by its letter. The twin reads the steer list and flags a new plan that breaks one before the user sees it.
  Done when: the twin flags 3 of 3 planted violations of past steers and 0 of 10 clean plans.

- **Wild: add a ghost-user lane that attempts the predicted ask blind** — FEATURE — value 3 — effort L — risk med — category: speculative lane
  Why: the idea is to find the first question a draft cannot answer. That question is what the user would have had to ask anyway.
  Done when: for a predicted ask, the lane returns only its first blocking question and a cost line, and no code merges.

- **Wild: add a "things I'd have told you" card at task close** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the dropped-as-built entries show the user keeps finding out that things already exist. The card turns that into a closing line of at most three facts, taken from MASTER.md clauses and recent sibling tasks.
  Done when: `fm task finish` prints it, and the card is empty rather than padded when nothing matches.

- **Wild: add a time-machine replay of the forecaster** — PERFORMANCE — value 3 — effort M — risk low — category: backtest
  Why: it replays the forecaster at each past commit date over the asked stream. This is the only way to catch a fitted-to-the-past predictor without waiting for new data.
  Done when: a replay report gives the hit rate per month, and a planted fake habit is not over-learned.

Next question: Which Anticipation outputs would the user have to open a page to see, and which of those could instead ride on the existing `fm next` and SessionStart lines?
Next question: What does the forecaster do on a brand-new repo with no asked history, and does the user's first hour look different from the second?
