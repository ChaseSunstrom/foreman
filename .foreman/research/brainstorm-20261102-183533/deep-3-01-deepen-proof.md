# Brainstorm — lens: deepen: proof

- **Bind every Exam to a filed outcome ledger row** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the carried gap says every brief's Exam names an outcome measure and a live-state reading; today these are prose. Combine the three proof ideas into one record: measure, snapshot at filing, reading at close, deadline.
  Done when: `fm task finish` refuses a brief whose Exam lacks a measure id, a filing snapshot and a close reading, and the refusal names the missing field.

- **Snapshot-and-diff live state at filing and close** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the pack's proof category starts here; many closes (e.g. "main's tree matches the local tree", T-2690) were verified by a second ask, not a recorded diff.
  Done when: closing a task prints a before/after diff of its named readings and stores both in the receipt.

- **Add a stale verdict with a deadline to Exam readings** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: a reading taken hours before close can pass on old state. Verdicts become pass / fail / stale.
  Done when: a reading older than its deadline yields "stale" and blocks close until retaken, held by a test with a fake clock.

- **Run readings cold and warm and flag disagreement** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: the open question about recovery paths tested only by their writer. A cold reading (fresh process, different cwd/env) catches state-dependent passes.
  Done when: a planted cache-dependent reading shows "warm pass, cold fail" in `fm check`.

- **Score dissents against outcomes** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the carried gap says dissents are unscored. Record each dissent as a prediction ("this will fail by X"), then settle it from the task's survival at 14 days.
  Done when: `fm outcomes` prints a dissent hit rate, with the sample count and a floor before it shows.

- **Place a canary near each idea's claim** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: the carried gap says canaries near the idea. A canary is a one-line check that fails if the idea's premise is false, filed with the brief.
  Done when: an intake brief with no canary is flagged, and a planted false premise turns its canary red.

- **Make the proof ledger tamper-evident** — SECURITY — value 3 — effort S — risk low — category: proof
  Why: `fm verify-ledger` already chains lines; extend the chain to the new snapshot and reading records so a rewritten reading is detectable.
  Done when: editing a stored snapshot makes `fm verify-ledger` fail naming the line.

- **Report "what this Exam left out" per brief** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the mission title says Foreman states what it left out; the proof layer should list which claims in the brief have no reading.
  Done when: each brief's close receipt has a "claims without a reading" list, and it is empty only if each claim maps to one.

- **Replay a closed task's Exam a week later (wild)** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: wild; a closed proof is only true on the day. Rerunning the readings at day 7 and 14 turns "done" into "still done" and feeds the outcome scores.
  Done when: a seeded regression is caught by the day-7 replay and printed in the next morning's report.

- **Let the typed-ask filter weight proof scores (wild)** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: answers the earlier question on typed versus Foreman-filed asks; proof pass rates split by who originated the work.
  Done when: `fm outcomes` shows pass rates for typed and filed asks separately.

- **Build a proof-mutation check (wild)** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: wild; deliberately break the thing the Exam claims to guard (revert the diff in a scratch copy) and require that the reading goes red. A reading that stays green is flagged as decorative. This extends `fm task prove` from tests to Exam readings.
  Done when: a reading that passes with the change reverted is reported "does not discriminate".

- **Write a signed proof card per close (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; one page showing the measure, before and after, cold/warm, and the left-out list, which the user can read in ten seconds on the web UI.
  Done when: the web UI task page renders the card, with empty, stale and failed states.

- **Rank readings by past discrimination** — PERFORMANCE — value 3 — effort M — risk low — category: proof
  Why: assumption: some readings never fail across many closes. Keep a per-reading fail record and nudge toward the ones that have caught things.
  Done when: `fm doctor` lists readings that have never failed in N closes as low-signal.

Next question: which readings has the user actually opened or overridden, and does override frequency say a reading is noise or the user is skipping proof?
Next question: when a snapshot cannot be taken (service down, offline), should the Exam say "unmeasured" and carry forward, or block, and who decides?
