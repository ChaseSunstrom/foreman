# Brainstorm — lens: blind spots

Each ask in "What earlier brainstorms missed" falls into one of five classes, and I list the question that would have caught each:

- **Subtraction (T-2534/35/36):** what does each thing Foreman adds cost, and what does it earn?
- **Unattended liveness (T-2542):** what runs without a session, and who notices when it stops?
- **Duplicates and grounding (T-2546/47):** does this idea already exist, and where is the evidence for it?
- **Input authorship (T-2554):** which inputs to a learned model did the user not write?
- **Silent abstention (T-2566):** which deciders quietly decide nothing, or decide on a fraction of their inputs, and say nothing?

I then asked the same questions of the whole project.

- **Make every decider report its coverage** — FIX — value 5 — effort M — risk low — category: trust
  Why: T-2566 shows `genesis select` deciding nothing when only held-out lines existed. The same shape can hide in ship chance, the bar check, calibration and the `--final` exam gate.
  Done when: every verb that keeps, reverts, gates or scores prints "decided on N of M inputs" or "abstained: <reason>", and a test feeds each one partial data and sees the line.

- **Tag every record with its author and filter readers by it** — FEATURE — value 5 — effort M — risk med — category: provenance
  Why: T-2554 and the dropped items (pasted credentials, `bash-input`, quoted steers, Mission briefs) show non-user text reaching user-facing readers one patch at a time.
  Done when: each ledger row carries `author` (user, foreman, child, paste, genesis), and every reader that models the user declares which authors it accepts, with a test per reader.

- **Run a drill that deletes one ledger record class at a time** — FEATURE — value 5 — effort M — risk low — category: ledgers
  Why: it answers the left-over question about which reader gives a wrong answer, not an error, when a record class is missing. T-2542 and T-2566 were both quiet-wrongness bugs.
  Done when: `fm doctor --drill` copies the state, removes each class in turn, and lists every reader that still answers confidently, with the list empty or ticketed.

- **Lint the criteria in a task against their own examples** — FIX — value 3 — effort S — risk low — category: task quality
  Why: T-2583 stated "8+ characters" next to the 7-character example "4% lost". Nothing checks a rule against the examples written beside it.
  Done when: `fm task new` runs numeric thresholds and quoted examples through a checker and refuses a task whose example breaks its own rule.

- **Give exam items stable IDs and versions** — FIX — value 4 — effort M — risk med — category: exam integrity
  Why: the steer says a fifth BEYOND row would reassign items through `hash % len`, and the exam has no item versioning, so recorded runs would stop being comparable.
  Done when: each exam item has a permanent ID, adding a row never changes an existing item's assignment, and a test pins the old assignments.

- **Make an override record that it is not proof** — SECURITY — value 4 — effort S — risk low — category: proof
  Why: this answers the left-over question about who records that an unproven row was overridden by hand.
  Done when: finishing over an unproven row writes an `overridden` flag with a reason, the receipt shows "unproven, overridden by user", and held-rate counts exclude it.

- **Give every check a third state, "could not run", with a reason** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: UI and browser checks can't run headless, and the pack asks how the receipt avoids reading as a pass.
  Done when: a web check with no display records `unrun: no display`, and `fm task finish` treats it as not proven in the receipt and the audit.

- **Track proven labels that were later reversed** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: this is a pack question, and outcome survival is already a signal Foreman didn't author.
  Done when: reopening or reverting a task whose receipt said proven writes a reversal row, and `fm outcomes` shows the reversal rate and the share that had no run record.

- **Check each ops gauge against one signal Foreman didn't write** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: timer liveness, bet settlement and canary state are all self-reported. Examples of outside signals are the systemd journal, GitHub Actions run times, and file mtimes read by a different tool.
  Done when: `fm doctor` shows each gauge beside an outside reading and WARNs when they disagree, with a test that forges the gauge.

- **Prove a restore drill on a clean home directory** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: the host-wipe question is open, and T-0798 (blackstart and recovery) is deferred.
  Done when: `fm restore --drill` rebuilds timers, ledgers and settings into a temp HOME, and the report separates what came back from what needs a hand step.

- **Log the commands the user types by hand to check verdicts** — FEATURE — value 3 — effort S — risk med — category: user model
  Why: the pack shows `bash-input` events like `fm night --print-timer` already pass through hooks, and typed checks show what the user distrusts. It needs to be opt-in, with no reading of shell history.
  Done when: user-typed bash lines are stored as `author=user, kind=check`, and `fm doctor` lists the three most-repeated ones as candidates for built-in proof.

- **Run a fuzzer that tries to make the gauges lie** — FEATURE — wild — value 4 — effort L — risk med — category: adversarial
  Why: assumption: a cold child that deletes a ledger, stops a timer or forges a bet finds blind spots faster than brainstorms do.
  Done when: a run produces a report listing which tampering each reader missed, and each miss becomes a task.

- **Add a negative-space map of what Foreman never observes** — FEATURE — wild — value 3 — effort M — risk low — category: coverage
  Why: assumption: the coverage grid lists what exists, not what has no recorder at all, such as non-Claude harnesses (T-0336) or the human's side.
  Done when: `fm coverage --blind` prints each surface and stage with no recorded events in 30 days.

- **Sweep a whole class of siblings after every user correction** — FEATURE — wild — value 5 — effort M — risk med — category: learning
  Why: the missed asks arrived one at a time (T-2534/35/36, T-2542/46/47), and a class sweep would have caught several together.
  Done when: closing a task from a user steer files a sibling-sweep task naming candidate readers or deciders of the same shape, grounded in the code.

Next question: for each Foreman verb that learns from or acts on a ledger, which record fields does it assume are always present, and what does it do when they aren't?
Next question: which public claims in the README and site rest on an arm that only the free or Haiku exam has run, and are they labelled provisional?
