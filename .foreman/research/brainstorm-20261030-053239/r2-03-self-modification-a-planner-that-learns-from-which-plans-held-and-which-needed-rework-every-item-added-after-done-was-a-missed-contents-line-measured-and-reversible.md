# Brainstorm — lens: self-modification: a planner that learns from which plans held and which needed rework (every item added after done was a missed contents line), measured and reversible

- **Stamp every goal with the hash of the ruleset that planned it** — FEATURE — value 4 — effort S — risk low — category: planner provenance
  Why: assumption: the pack shows no link from a goal to the planner state that made its contents list. Without that link, "this goal needed rework" cannot be blamed on a rule version, so nothing can be learned or reverted safely.
  Done when: `fm goal show` prints the ruleset hash, and a test shows that editing the rules changes the hash only on goals planned afterward.

- **Snapshot what the planner knew, then split misses into knowable and unknowable** — FEATURE — value 5 — effort M — risk med — category: miss attribution
  Why: assumption: some post-done additions come from facts that did not exist at plan time, such as a new user ask or a changed dependency. If those teach a rule, the planner learns to pad against the future. At plan time, hash the repo tree and the user-words excerpt. Only misses whose evidence was in that snapshot may feed a rule.
  Done when: a fixture with one miss that was visible in the snapshot and one that was not produces exactly one lesson candidate.

- **Learn the rework lag window that separates a miss from scope growth** — FEATURE — value 4 — effort S — risk low — category: miss attribution
  Why: "Every item added after done is a missed line" counts a feature requested a month later as a planner fault. Fit a cutoff, for example "added within N days and touching the goal's own files", from the history. The cutoff is stored with its evidence.
  Done when: a replay over fixture goals reports a lag histogram, and an addition past the cutoff is logged as "growth", not "miss".

- **Score plan precision as well as recall** — FEATURE — value 4 — effort S — risk low — category: planner metrics
  Why: the pack only counts additions. A rule that pads every plan would raise recall while lines that were never touched or were deleted pile up. Report both, plus F1 per ruleset version, on the pane and the site.
  Done when: padding every fixture plan with 10 junk lines drops the F1 for that ruleset below the baseline.

- **Plan every goal in shadow with a challenger ruleset and grade it at finish** — FEATURE — value 5 — effort M — risk med — category: champion/challenger
  Why: scoring a plan needs no extra execution, because the final set of contents lines is known once the goal finishes. A challenger can therefore be tested on real goals at the cost of one planning call each. It is promoted only if it beats the champion's recall at equal or better precision over K goals.
  Done when: a test with a seeded challenger that always wins is promoted at exactly K goals and not before.

- **Allow learned rules only to add or reorder, never to loosen** — SECURITY — value 5 — effort S — risk low — category: self-mod guard
  Why: the capability says "NEVER lower your own guard." A rule that drops a MUST line, weakens a done-when, or merges criteria is a guard-lowering edit. Make the rule format monotone: add line, raise priority, tighten a verify command. Any other diff is refused and ledgered.
  Done when: a rule proposal that deletes a MUST is rejected with a ledger event, and one that adds a line is accepted.

- **Weight each miss by the rework it caused** — FEATURE — value 4 — effort M — risk med — category: miss attribution
  Why: assumption: a missed line that forces edits to files an earlier done task already changed (structural) costs far more than one added beside the old work (additive). Use file overlap with finished tasks and the added task's wall time as the cost. Rank lessons by cost.
  Done when: a fixture with one structural miss and one additive miss ranks the structural one first.

- **Bisect the planner across its own ruleset history** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: when the rework rate rises, the question is which promotion caused it. Replay the corpus of finished goals' original intake text under each historical version and report the first version where replay recall dropped. Offer a one-command revert to the version before it.
  Done when: a test with a planted bad rule at version 5 of 8 makes `fm planner bisect` name version 5.

- **Re-audit every learned rule by ablation when the model id changes** — FEATURE — value 3 — effort M — risk low — category: rule hygiene
  Why: assumption: many rules compensate for a model's habits, such as forgetting docs pages or surface parity. A newer model may no longer need them, and they only pad. On a model change, replay with and without each rule and demote those with no measured catch.
  Done when: a fixture where a rule has no effect under the "new" model is demoted, and one that still catches is kept.

- **Withhold each learned rule on one goal in five for causal credit** — FEATURE — value 4 — effort M — risk med — category: causal measurement
  Why: replay shows what a rule would have caught, not what it does live. Randomly withholding a rule on a small share of goals, with the withholding logged, gives a true control group. A rule whose withheld goals show no more misses is retired.
  Done when: over a seeded series of goals the withhold rate is within tolerance, and the withheld goals appear in the rule's ledger.

- **Show the finished neighbour's final list next to the new plan** — FEATURE — value 3 — effort S — risk low — category: retrieval, not rules
  Why: the clause word-overlap code already exists. Pick the most similar finished goal by word overlap and print the lines its list ended with that the new plan lacks, quoted as data. It needs no promotion machinery, so it helps from goal 2.
  Done when: planning a goal that resembles a fixture finished goal lists that goal's added-later lines as candidates, each tagged with its source goal.

- **Learn the ordering of lines, not only their presence** — FEATURE — value 4 — effort M — risk med — category: planner ordering
  Why: the Stop drive can end on DRIVE_MAX or a no-progress stop, leaving the tail of the plan unbuilt. If past additions skew to a kind of line, such as docs, surface parity or exam scenarios, put that kind earlier. A cap-stopped goal then lacks only lines that rarely matter.
  Done when: on replay, the mean position of eventually-added line kinds moves earlier, and a stopped-early fixture goal's unbuilt tail has lower miss weight than before.

- **Wild: Seal three prophecies of what the user will add after done** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: assumption: a planner that must bet on its own gaps ("docs for X will be added", "Desktop surface forgotten") is forced to look hard at its weak spots. Hash the bets into the goal. At finish, score which came true. The hit rate becomes the planner's self-doubt calibration, and true hits become lesson candidates.
  Done when: a goal that gets one of its three sealed prophecies added later shows a 1/3 score, and tampering with the sealed file fails `fm goal check`.

- **Wild: Put every proposed rule on trial against the goals it might have padded** — FEATURE — value 4 — effort M — risk med — category: rule gating
  Why: before promotion, a cold prosecutor model is shown only the rule and the lines of past finished goals, and must name a goal where the rule would have added an unneeded line. Each real counterexample, checked by the replay, counts against precision. A rule with several counterexamples is rejected.
  Done when: a rule built to over-generalise is rejected with a named counterexample goal, and a narrow rule passes.

- **Wild: Have the planner plan its own next ruleset revision as a goal** — FEATURE — value 3 — effort L — risk med — category: dogfood loop
  Why: the planner's rework is then measured on the one goal type it always has. A ruleset revision gets a contents list, done-when criteria, and a closing audit like any other goal. Its reopens count in the same metrics. A planner that cannot plan its own improvement visibly loses trust.
  Done when: one full revision runs end to end as a goal, and its rework rate appears in `fm planner report`.

Next question: when the user deletes or narrows a line the planner added, is that evidence of padding or simply a changed preference, and what in the user's words separates the two?
Next question: where do learned rules live so Claude Code, `fm code`, the Codex, Gemini and opencode shims, MCP and Desktop all read the same ruleset without any of them being able to write it?
