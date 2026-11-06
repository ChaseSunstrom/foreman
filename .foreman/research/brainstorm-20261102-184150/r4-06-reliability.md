# Brainstorm — lens: reliability

- **Make a Mission file atomic with a sentinel footer** — FIX — value 4 — effort S — risk low — category: durability
  Why: unattended Missions write tower files that sweeps and cold reads consume; a crash mid-write leaves a truncated brief that still parses (T-2731 mended a record that lost only its newline, so partial writes are real). Assumption: Mission files are written non-atomically.
  Done when: a test kills the writer at every byte offset of a Mission file and the sweep reports "incomplete" for each truncation, never a silent pass.

- **Pin every Exam live reading to a timeout and exit class** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the carried gap says every brief's Exam names a live-state reading; a reading that hangs stalls the sweep and the tower's self-advance. The pack shows the ship gate already has timeouts that don't name the hung step.
  Done when: a planted `sleep 999` reading is killed at the cap and recorded as "timed out after Ns", and the sweep continues.

- **Make a failed-to-read Exam a third result, "could not run"** — FIX — value 5 — effort M — risk med — category: exam
  Why: asks on UNPROVEN and "could not run" recur, and an offline or service-down snapshot must not read as pass or fail. Assumption: today it collapses into one of those two.
  Done when: with the reading's command made to fail, `fm exam brief` prints "could not run: <reason>", exits with a distinct code, and the brief stays open.

- **Score dissents idempotently, from records only** — FEATURE — value 4 — effort M — risk low — category: dissent scoring
  Why: the carried gap is dissents scored against outcomes, and the sweep re-runs. A re-run that double-counts or flips a score corrupts the very signal being built.
  Done when: running the scorer twice on a planted-outcome ledger yields byte-identical output, and that fixture runs in every sweep.

- **Run the canary's positive control before every "not built" claim** — FIX — value 4 — effort S — risk low — category: grounding
  Why: a "not built" verdict from a search that can't find known things is worse than none, and the canaries are a carried gap. The pack's ideas show dropped items later found "already met" (the T-2702-era drops).
  Done when: the canary first searches for a known-present verb, and if that comes back empty the "not built" claim is refused with "canary blind".

- **Detect a Mission that ran against a stale pack** — FIX — value 3 — effort S — risk low — category: provenance
  Why: the pack's map says "as of an older HEAD", so briefs can rest on state that has moved.
  Done when: each Mission file records the HEAD and ledger epoch of its pack, and the sweep flags any whose HEAD is more than N commits behind at filing.

- **Bound the lens fan-out with a partial-result contract** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: T-0831 (salvage partial results from capped children) is deferred, and a failed lens child looks the same as a dry one, so a Mission can claim breadth it did not have.
  Done when: a Mission with one planted-dead lens prints "N of M lenses returned" and lists the dead one in its left-out receipt.

- **Write the left-out receipt first, incrementally, per cell** — FEATURE — value 4 — effort M — risk low — category: durability
  Why: if an unattended Mission dies midway, the record of what it skipped is the most valuable thing lost.
  Done when: killing a Mission at any stage leaves a receipt that lists every cell not yet covered.

- **Run Exam readings on a frozen copy and refuse any that write** — SECURITY — value 4 — effort M — risk med — category: exam safety
  Why: live-state readings run unattended and nothing in the pack shows them being checked read-only. A reading that writes to the tree it measures corrupts its own result.
  Done when: a reading that touches a file is refused at filing with the path named, and a read-only one passes.

- **Wild: Plant one known gap in the pack each generation and check the Mission finds it** — FEATURE — value 4 — effort M — risk low — category: self-test
  Why: wild. Exhaustiveness is only claimed, never measured; a seeded gap gives the recall figure for free.
  Done when: the sweep reports found or missed for the planted gap, and a miss blocks "exhaustive" in the Mission report.

- **Wild: Pull-the-plug day for the Mission pipeline** — FEATURE — value 3 — effort L — risk med — category: chaos
  Why: wild. A seeded SIGKILL at a random stage of a real Mission on a scratch repo would show which stage loses work. It extends the drill the pack already has.
  Done when: 20 seeded kills leave zero Missions that read as complete without all their briefs.

- **Wild: Refuse readings stamped in the future** — SECURITY — value 2 — effort S — risk low — category: clocks
  Why: wild. After a clock jump or a resume from suspend, a reading's timestamp can lie and make an outcome appear to have survived 14 days.
  Done when: a reading with a timestamp ahead of the sweep's clock is rejected as "clock skew" and counted as unmeasured.

- **Cap each Exam reading and log its runtime** — PERFORMANCE — value 3 — effort S — risk low — category: exam
  Why: summed reading runtimes bound the sweep's own duration, and the hook bench shows latency is already a tracked concern.
  Done when: the sweep prints the total reading time and fails a brief whose readings exceed 15 seconds.

Next question: which stage of the Mission pipeline can lose work today with no record anywhere that it did?
Next question: when a reading is "could not run" three generations in a row, who is told, and does the brief stay open forever?
