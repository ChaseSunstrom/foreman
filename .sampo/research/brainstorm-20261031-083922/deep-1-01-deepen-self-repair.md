# Brainstorm — lens: deepen: self-repair

- **Run one incident ledger that every self-repair signal feeds** — FEATURE — value 5 — effort M — risk med — category: self-repair
  Why: the pack shows separate loops (T-2272 signal-to-fix, T-2276 trigger outcomes, T-2290 predictions, T-2281 ratchet, "Baseline red" dupes dropped as the same failure as T-2283). Dedupe by command text missed one, so the signals aren't joined.
  Done when: a failure seen via a ship scratch run, a doctor warning and a user correction in a test lands as one incident record with three sources and produces one task.

- **Normalise failure signatures before counting recurrence** — FIX — value 4 — effort S — risk low — category: self-repair
  Why: the dropped "Baseline red" task was filed twice because the interpreter's full path differed; T-2272's 3+ task threshold depends on matching signatures.
  Done when: a test feeds the same failure with different interpreter paths, tmp dirs, timestamps and line numbers and gets one signature.

- **Reopen a fix when its signature returns, and bind it to the original task** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: T-2272 skips signatures that already have a finished task, so a fix that didn't hold is invisible. Assumption: nothing watches post-close recurrence today.
  Done when: a signature recurring after its fix task closed reopens that task with the new occurrence and a "fix did not hold" mark, visible in `fm doctor`.

- **Make every self-fix prove it would have caught its own trigger** — FEATURE — value 5 — effort M — risk med — category: self-repair
  Why: `fm task prove` already shows the test fails without the change. Extend it to self-filed FIXes: the stored trigger (the log, the correction) must replay red on the old tree and green on the new one.
  Done when: closing a self-filed FIX without a replayable trigger check is refused, and one with it records both runs.

- **Quarantine a fix that needed a fix, with a churn score per area** — FEATURE — value 4 — effort M — risk low — category: self-repair
  Why: T-2283 and the Baseline-red follow-up, plus the T-2285 plan-gate patch right after the T-2269 gate, show fix-of-fix chains. Assumption: git and task links can detect them.
  Done when: a second FIX touching the same files within N tasks flags the first, and the area's churn shows in `fm doctor`.

- **Sweep sibling code when a FIX closes** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: T-2285 (flag-led options) and T-2269's L-gate premise error suggest one bug class recurs across the plan gates. Use `fm graph blast` and a structural pattern search.
  Done when: closing a FIX lists sibling sites with the same pattern, each filed as a task or marked checked.

- **Turn every "asked" line into a permanent regression probe** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: "What earlier brainstorms missed" holds eight asks the user had to make. Their behaviours are exactly what regress silently, and each is currently covered only by its own task's test.
  Done when: `fm doctor` runs one probe per user-ask task, reports ones with no executable check, and a deliberately broken behaviour fails one by name.

- **Check a self-filed task's premise before it is filed** — FIX — value 4 — effort S — risk low — category: self-repair
  Why: three of the dropped tasks were wrong premises (the fmcode L-tier task contradicted `check_plan`, the `_next_runnable` stall wasn't a stall, one duplicate). Each cost a cycle.
  Done when: a task proposing a defect must quote the file line it cites, and a test shows a filing whose cited line doesn't match is rejected.

- **Rehearse each self-change on a snapshot of real state** — FEATURE — value 4 — effort L — risk med — category: self-repair
  Why: bench and trials gate changes, but real state (ledgers, steers, lanes) is where bugs like the lane-rm `.fm-scratch/` refusal appear. Assumption: a state snapshot can be copied cheaply.
  Done when: a self-change's merge gate runs the key verbs on a copied state dir and fails on any crash or diff outside the expected set.

- **Pin a last-green rescue `fm` that can roll back the live one** — SECURITY — value 4 — effort M — risk med — category: self-repair
  Why: a self-edited `fm` that breaks itself can't repair itself. Assumption: no frozen fallback is shown in the pack.
  Done when: a test that corrupts the live `fm` shows `fm-rescue` restoring the last version that passed `fm doctor` and the round-trip e2e.

- **Wild: Replay a user correction against the old build** — FEATURE — value 4 — effort L — risk med — category: self-repair (wild)
  Why: each correction is a counterexample to Foreman's behaviour. Replay the preceding session context through the build from before the fix, to confirm it misbehaved, then through the new build to confirm it doesn't.
  Done when: a stored correction replays through two builds in a sandbox and the report shows a differing outcome.

- **Wild: Plant a canary bug weekly and time the loop** — FEATURE — value 3 — effort M — risk med — category: self-repair (wild)
  Why: nothing shows the signal-to-fix loop working end to end. Plant a harmless recurring failure in a scratch repo and measure the time to detection, task, fix and verification.
  Done when: a weekly run reports a latency per stage, and a disabled stage makes the canary alert.

- **Wild: Keep a graveyard of dropped and reverted self-changes** — FEATURE — value 4 — effort M — risk low — category: self-repair (wild)
  Why: dropped tasks carry reasons ("premise doesn't hold", "already covered by T-1208"), yet new ideas similar to them can be filed again. Consult the graveyard first.
  Done when: filing a task whose text matches a graveyard entry shows the entry and its reason, and requires an explicit override.

- **Wild: Hold a monthly autopsy that rebuilds the worst miss as an exam scenario** — FEATURE — value 4 — effort L — risk med — category: self-repair (wild)
  Why: steers require weakness-finding from signals Foreman didn't author, and exam scenarios must come from a separate tool-less child. The autopsy picks the costliest recurring miss and has that child write a held-out scenario for it.
  Done when: each month one scenario derived from a real miss is added to the held-out set, with a link to its source incident.

Next question: Which self-repairs have been reverted or re-fixed after merge, and does Foreman currently know that rate per kind of change?
Next question: When two self-repair signals disagree (a bench pass but a user correction), which one wins by rule, and does the user see the conflict?
