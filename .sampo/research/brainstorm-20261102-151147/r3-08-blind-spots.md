# Brainstorm — lens: blind spots

Most of the 2 Nov asks follow a few patterns: a number or counter that ignored a second path (T-2667, T-2657, T-2583), a stop or cap with a guessed limit (T-2668, T-2669), and an event whose effect on stored items nobody traced (T-2656). I put each question to the whole project; the ideas below are what it surfaces that the earlier lists don't cover.

- **Pair every start record with a terminal record, and list the orphans** — FEATURE — value 4 — effort M — risk low — category: ledger integrity
  Why: T-2657 counts fails and passes, but nothing in the pack says that tasks, lanes, children, provers or `fm run` write a matching end record when they die mid-way. Question: which things get a start record but no guaranteed finish?
  Done when: a test kills a lane, a prover and a child mid-run, and `fm doctor` names each as "started, never ended" with its id.

- **Rank flaky tests by lower confidence bound, not raw fail rate** — FIX — value 3 — effort S — risk low — category: statistics
  Why: T-2657 lists the three worst tests by fail rate. One fail in one run reads as 100% and outranks a test that failed 12 of 40. Question: what does a rate look like at n=1?
  Done when: a fixture with a 1-of-1 test and a 12-of-40 test ranks the 12-of-40 test first, and each line shows its n.

- **Make every stall and spend stop work when dollars read zero** — FIX — value 4 — effort S — risk med — category: unattended safety
  Why: assumption: on a subscription plan, usage is priced at $0 (this harness's own meter shows `$0/$200`). `--stall-usd N` (T-2669) would then never trip. Question: is the stop's unit nonzero in every billing mode?
  Done when: with spend forced to 0, `fm run --stall-turns N` (or tokens) still halts a run that closes nothing and names the unit in the receipt.

- **Re-run the closed task's proof when a capture near-duplicates it** — FEATURE — value 4 — effort M — risk low — category: regression catch
  Why: T-2656 wakes only deferred duplicates. A duplicate of a task closed last week is either a regression or a misunderstanding, and today it files as a fresh task. Question: what happens when the duplicate matches a closed task?
  Done when: a capture matching a closed FIX runs that task's stored red-first check. If it fails, the capture is filed as a regression linked to the closing commit. If it passes, the capture is annotated "still holds, here is the proof".

- **Print "N left out" on every truncated list, with the flag that shows them** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: the steer expansion (T-2631) had to be told to list the generations it left out. Question: where does a summary cut items without saying so?
  Done when: a lint finds any verb output that slices a list with no "showing X of Y" line, and the suite fails on one planted case.

- **Keep a limit register with boundary tests at n−1, n and n+1** — CLEAN — value 3 — effort M — risk low — category: caps
  Why: T-2668 picked 8 nested `$(`, with the other pathological inputs it timed at 50k chars, and T-2669 picks a stall threshold. Nothing lists these guessed constants together. Question: which other hard-coded limits were chosen by feel?
  Done when: one table holds every cap with its reason and its refusal text, and a generated test hits each at n−1, n and n+1.

- **Calibrate each hard cap from the user's own command history via `fm replay`** — FEATURE — value 3 — effort S — risk low — category: guard fit
  Why: `fmreplay.py` already runs session-log commands through the guard. Nobody has asked what the deepest nesting or longest line the user actually types is. That tells us whether a cap of 8 refuses real work.
  Done when: `fm replay --caps` prints the max observed value per cap and flags any cap the user's own history has touched.

- **Declare a `valid_while` predicate on every gauge and check it on host upgrade** — FEATURE — value 4 — effort M — risk med — category: measurement integrity (wild)
  Why: `fm burden` was wrong because the host delivers context on a second channel (T-2667). Each gauge should state which host behaviour it depends on and have `fm doctor` test that behaviour on the live host. Question: how will we notice when a gauge's premise stops being true?
  Done when: `fm doctor` evaluates the predicate for the burden gauge, and a fake host that moves the channel turns the row red.

- **Find derived labels stored apart from their source** — CLEAN — value 3 — effort M — risk low — category: consistency
  Why: the re-grounded T-2671 note says the receipt lists unproven kinds, but the stored grade (`verified: strong`) is counted by digests regardless. Question: which stored labels can disagree with what the record derives?
  Done when: a census recomputes each stored label (grade, status, kind) from its source and `fm doctor` lists the disagreements, with one fixture planted.

- **Make equivalent transcript encodings a test fixture for every counting gauge** — FEATURE — value 3 — effort M — risk low — category: gauge parity
  Why: `fmcost.INJECTS` missed `hook_success` stdout. Question: for every gauge, in how many encodings can the same logical event arrive?
  Done when: one fixture per event kind is written in every known encoding, and each gauge must return the same count for all of them.

- **Pre-fund each task from its forecast and stop on overdraft (wild)** — FEATURE — value 3 — effort L — risk med — category: spend control
  Why: assumption: `--stall-usd` stops a run after the spending, and a per-task allowance would stop it earlier. Question: what limits a single task's burn, rather than the whole run's?
  Done when: a task with a $1 allowance halts at $1, files the remainder as a follow-up, and the receipt shows funded versus spent.

- **Pre-answer the three likeliest follow-up asks on every finish card (wild)** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: the user's 2 Nov asks read as follow-ups to earlier receipts (stored grades, `fm doctor` rows, a "next command"). Question: what will the user ask right after this card?
  Done when: the card holds three one-line answers with commands, and a backtest over the last 30 closed tasks counts how often a real next ask matched one.

- **Name the hung step when the ship gate hits its timeout (wild)** — FIX — value 3 — effort S — risk low — category: diagnosability
  Why: T-2668 shows a guard hang cost a whole run before anyone saw where. Question: when anything times out, does the message name the culprit?
  Done when: a planted sleeping test makes the gate print its name, how long it ran and the command to re-run it alone.

Next question: for every verb that prints a number, can the user falsify it by hand with one shell command, and does the output show that command?
Next question: which Foreman-filed tasks closed without the user ever seeing what they changed, and how would the next brainstorm count those as unasked?
