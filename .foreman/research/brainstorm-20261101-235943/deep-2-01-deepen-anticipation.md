# Brainstorm — lens: deepen: anticipation

- **Run a predictor tournament on the asked stream** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: T-2546's word-overlap matcher met no bar; the pack lists "race four predictor approaches" and "backtest on the asked stream" separately. Combine them: one harness replays the recorded asks (the "asked:" stream) against every candidate forecaster (word overlap, MASTER.md clause match, recency/frequency, a tool-less child) and scores hit@3 per candidate. Only a winner above the shuffled-history control may draft anything in a lane.
  Done when: `fm foresight tournament` prints hit@3 per predictor and the shuffled-control hit@3, and `fm foresight draft` refuses with the named bar if no predictor beats the control.

- **Gate every predicted draft on already-built, grounding and a planted-history probe** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: three listed ideas ("already built before lane", "refuse without grounding line", "planted-history probe") are one gate. T-2546 already built the covered check, and T-2547 the grounding refusal, so this wires them into the lane path rather than adding a verb.
  Done when: a predicted draft that restates a MASTER.md clause, or that has no grounding line, is refused with the reason, and a test with a planted history shows the predictor recovers the planted next ask.

- **Make foresight act: prefetch context into the lane before the ask** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: "make foresight act instead of announce" and "prefetch context instead of drafting requests". Drafting a request on a wrong guess costs a lane; reading the likely files, the stack card and the open tasks costs almost nothing. Prefetch lands in a cache that `fm next` and the plan gate read.
  Done when: after a session start, a prefetch file names the top 3 predicted areas with their files, and the first plan for a matching request cites the prefetched files, measured by counting reads the plan needed beyond them.

- **Plot the anticipation learning curve** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: "hit@3 against history length" tells whether the model of me improves or plateaus, which decides if more history is worth gathering. Assumption: about 200 asks suffice for a curve.
  Done when: `fm foresight curve` prints hit@3 at 10, 25, 50, 100 and all asks, and `fm doctor` WARNs if the last point is below the first.

- **Predict which self-filed task the user will drop** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: the pack's "dropped:" rows show Foreman-filed items dropped as built, measured away or captured by mistake (T-0034 style deferrals, the "first brief" fixtures). Score each new self-filed task against past drops, and hold likely drops in the inbox rather than offering them via `fm next`. This fits the round-first rule.
  Done when: on the recorded drop history the scorer beats the base drop rate on a held-out half, and a task it flags appears in `fm next` with "likely drop: <reason>" instead of being offered.

- **Check "already built" as the request is typed** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: T-2546 runs the check at capture time, after the user has typed the whole ask. A UserPromptSubmit hook runs it on submit, so the note arrives before the plan is written and the "sorry, already built" drops (the guard-only arm, T-0963) never reach the queue.
  Done when: submitting a prompt that restates a MASTER.md clause adds the clause and task id to the session's context before any plan, shown by a hook test.

- **Add a sealed-prediction scoreboard that survives generations** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the pack asks each generation to write a sealed prediction of the user's next three steers. Nothing shows the predictions being scored against the steers that arrive. Store each one with a date and a match rule, and score hit rates per generation.
  Done when: `fm genesis predictions` lists each sealed prediction as hit, miss or open against the later steers, and the sweep reports the hit rate.

- **Fill the 58 cells through a probe set, not 58 writings** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: the earlier question asks which cells are one capability counted under several stages. Cluster cells by the file they cite, and write one probe per cluster that fails if the cited behaviour changes. Cells that stay empty with no counterexample are the true gaps.
  Done when: the sweep prints clusters with probe counts, each filled cell links to a passing probe, and a cell whose probe fails turns red.

- **Wild: a ghost-user child writes the next ask blind** — FEATURE — value 3 — effort M — risk med — category: anticipation — wild
  Why: a tool-less child sees only the last 30 asks and steers, with no code, and writes the three likeliest next asks. The real next ask scores it. This is a signal Foreman did not author, per the standing weakness-finding rule.
  Done when: `fm foresight ghost` stores its guesses before the next ask arrives, and a later run reports the hit rate beside the heuristic predictors.

- **Wild: a shadow-user twin pre-answers every yes-card** — FEATURE — value 3 — effort L — risk high — category: anticipation — wild
  Why: assumption: the user answers many fm ask prompts and door-gate questions the same way. A twin built from past `fm decide` records proposes the answer. It never acts on it alone, and it records its answer as a costly decision when it is wrong. The "never block on the user" rule suggests that cost is low.
  Done when: on recorded decisions the twin's answer matches the user's more than 70% of the time on a held-out half, and a card shows "twin says: X" without answering.

- **Wild: replay the last 20 asks through today's forecaster in the web UI** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: a "what would I have predicted" page shows each of the last 20 asks beside the forecaster's top 3 and a hit or miss. The user can see for themselves whether the model of them is any good. Without it, forecast quality stays invisible unless they open fm.
  Done when: the web UI page lists 20 rows with hit marks, and the empty state says "not enough history" when fewer than 10 asks exist.

- **Predict machine breakage from the ledger before it happens** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: "what breaks" is in gen-0 #3, but T-2542 only reads timers. Use recurring failures in the ledger (ETXTBSY flakes, a failing import in a working copy, a dead timer) as precursors, and flag them at session start with the last matching fix.
  Done when: a planted precursor in a fixture ledger produces a Watch line naming the likely failure, and a backtest on real ledger history reports precision against the failures that followed.

Next question: Which predictor, if any, beats the shuffled-history control on the real asked stream, and is that stream large enough to tell?
Next question: Which anticipation outputs (prefetch files, drafts, sealed predictions) does no session path read, so a wrong one would never be noticed?
