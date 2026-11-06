# Brainstorm — lens: blind spots

**Missed asks, by class (the question each should have triggered):**
- T-2525 (late start point applies only to open tasks): "Which features hold for one task state only?"
- T-2532 (non-tool hook import failure): "Which event types does each fallback cover?"
- T-2533/2535 (per-call notes, commit blame in the ratchet): "Which gauges omit a source or a cause?"
- T-2534/2536 (guard-only arm, ablation): "Which feature has never been measured against its own absence?"
- T-2542 (timers known alive): "Which installed thing has no proof of life?"
- T-2505 (sealed prediction): "What did nobody ask?"

Applied to Exhaustive thinking, the 58 empty cells are where those classes hide.

- **Run every thinking gate across every task state** — FIX — value 5 — effort M — risk low — category: reliability
  Why: T-2525 shows a premise tested in one state only; plan, readings and race checks likely have the same hole (assumption: untested for captured, deferred, blocked, self-filed).
  Done when: a test matrix runs each deliberation gate against all task states and fails on any state with no assertion.

- **Add a degradation ledger for deliberation children** — FIX — value 4 — effort M — risk low — category: observability
  Why: T-2532 was a silent fallback; a dead readings/race child likely yields a quiet empty result (assumption).
  Done when: killing a child mid-run leaves a named event in `fm doctor` and the finish receipt.

- **Ablate each deliberation step against its absence** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-2534/2536 built this for hooks; readings, race and blast radius have no off arm.
  Done when: the duel's ablate output lists a cleanup candidate or a kept verdict per deliberation step.

- **Show proof of life for every deliberation job** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: T-2542 covered timers only; unattended races and brainstorm children have none.
  Done when: `fm doctor` WARNs on a deliberation job with no completed run within three intervals.

- **Annotate each gauge with what it omits** — FIX — value 3 — effort S — risk low — category: honesty
  Why: T-2533/2535 found gauges missing sources; depth, confidence and blast radius gauges unchecked.
  Done when: each deliberation gauge prints an "inflated/deflated by" line, tested.

- **Give every coverage cell a probe and the state it ran in** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the standing rule says a cell counts only when grounded; probes make that checkable.
  Done when: `fm genesis sweep` rejects a cell lacking a runnable probe or a recorded n/a.

- **Seal a prediction of the next three thinking-related asks** — FEATURE — value 3 — effort S — risk low — category: blind spots
  Why: T-2505 asked for it generally; none yet targets thinking.
  Done when: a dated sealed file exists and is scored against the user's next three steers.

- **Reconcile the plan with the baton and ledger after a kill** — FIX — value 4 — effort M — risk med — category: recovery
  Why: the pack lists "baton, ledger and repo disagree after a kill" as a recurring class (assumption: plan files lack it).
  Done when: killing a session between plan and race resumes with one reconciled state, tested.

- **Fail when a deliberation child answers with a different model than requested** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: unattended routers can silently substitute (assumption).
  Done when: a model mismatch aborts the stage with a named error.

- **Ask "is this built?" at capture time** — FEATURE — value 4 — effort S — risk low — category: dedupe
  Why: the Missions 3 and 4 lesson: most items were already built.
  Done when: `fm capture` prints the nearest existing verb or grep hit before filing.

- **Wild: Hold a silent-failure day** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: wild; kill one deliberation component per hour in a scratch copy and record who noticed.
  Done when: a report lists each kill and its first detector.

- **Wild: Let a blind child write the ask the user will send next** — FEATURE — value 3 — effort S — risk low — category: prediction
  Why: wild; the child reads only the changelog, and its guess is scored later.
  Done when: its guess and the real next ask are diffed in a ledger.

- **Wild: Print "what I would have told you if you'd asked" at session start** — FEATURE — value 3 — effort M — risk med — category: delight
  Why: wild; drawn from the dropped-as-built list, so the user stops re-asking built things.
  Done when: session start shows up to three such lines, each citing a ledger row.

Next question: Which of the 58 cells are really one capability counted under several stages, and what is the smallest probe set that covers them?
Next question: Which deliberation outputs does no session path read, so that a failure in them would never be seen?
