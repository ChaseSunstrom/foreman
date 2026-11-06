# Brainstorm — lens: blind spots

- **Tag verb use by caller, so the usage census sees only hands that count** — FIX — value 4 — effort S — risk low — category: lean
  Why: T-2654 (`fm tidy --verbs`) was dropped as "mostly built" because `fm usage --prune` exists. assumption: that census also counts Foreman's own ticks, drives and hooks calling verbs, so a verb only the tick uses never looks unused. The prune verdict is then wrong in both directions.
  Done when: a fixture run where one verb is called only by the tick lists it under "self-only", and `fm usage --prune` offers it as separate from "unused".

- **Label each brainstorm-accepted ask in the pack as slate-origin, not user-origin** — FIX — value 4 — effort S — risk low — category: intake
  Why: the pack's "asked:" lines for T-2650–2659 carry slate markers like "(c06: …; value 4, effort M, risk med)". Those are brainstorm ideas echoing back as the user's words. Lenses then "read the user's need" from text Foreman wrote.
  Done when: the pack builder prints `asked (slate c##)` versus `asked (said)`, and a fixture with both kinds shows them in separate sections.

- **Turn "dropped with a noted remainder" into a tracked S task or an expiring note** — FEATURE — value 4 — effort S — risk low — category: triage
  Why: the drops say "decide() not booking a None answer is the one real gap, noted" and "the remainder (60 days, under fm tidy) isn't…". Nothing shows where those notes go, so real gaps found during re-grounding probably vanish.
  Done when: dropping an idea with a `remainder:` field files a deferred S task or a 14-day note, and `fm next` shows how many are open.

- **Ratchet the bench threshold from passing runs** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: T-2651 made `--bench CMD --under MS` a pass/fail proof, but the user picks `MS` by hand. A threshold set loosely never fails. assumption: no baseline is stored beside it.
  Done when: after three passes, `fm task evidence --bench` stores the median and suggests a tighter `--under`, and a run slower than median+noise fails against the stored one.

- **Log whether the user ran the printed `Next:` command** — FEATURE — value 3 — effort M — risk low — category: ergonomics
  Why: T-2653 prints a `Next:` on every nonzero exit, but nothing measures whether it unblocks anyone. The pack asks which proof states the user acts on.
  Done when: `fm doctor` lists the top three error classes by "Next ignored within 5 minutes", from ledger events only.

- **Scan ledger fields for write-only data** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: `--bench` recorded medians that never decided anything (T-2651), and `task_done` was read by several readers that printed zero when it was missing (T-2648). assumption: other fields are written and read by no gate or reader.
  Done when: a static scan lists every ledger field with no reader and no gate. Each is then wired, given a threshold, or deleted, and the scan runs in `fm check`.

- **Make each drill fault list the readers it must exercise** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: the drop-one-class fault found readers that "print a zero". The list of readers per class is hand-curated. assumption: new readers added later are never drilled.
  Done when: `fm drill` greps for readers of each ledger class and fails if any is not hit by that fault's run.

- **Include the guard and installed hooks in `fm drill --restore`** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: T-2652 proves each project's record reads back from a snapshot. It does not say the guard still blocks anything on the restored home. assumption: it checks records only.
  Done when: the restore drill replays the guard's red-team corpus against the temp home and fails if any blocked command is allowed, or the hooks are missing.

- **Count tombstone hits before deleting the tombstone** — CLEAN — value 2 — effort S — risk low — category: lean
  Why: T-2653-adjacent ask c08 prints a one-line tombstone for removed flags. Tombstones then linger forever, or get deleted blind.
  Done when: each tombstone hit is logged, and `fm tidy` proposes deleting those with zero hits in 90 days.

- **Weight yield per dollar by effort and flag task splitting** — FEATURE — value 3 — effort S — risk med — category: measurement
  Why: T-2655 prints tasks closed per dollar. Splitting work into more S tasks inflates it. The user's rule is that deciders reading Foreman-written data need an outside signal.
  Done when: the receipt also shows effort-weighted yield (S=1, M=3, L=8) and a note when the median task shrinks more than 30% against the last 5 runs.

- **Wild: drop one whole day from a ledger and make windowed readers report the gap** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: the drill removes a record class. Rolling-window metrics (rates, digests) still quietly average over a missing day. wild.
  Done when: `fm drill --drop-day D` makes `fm digest` and `fm outcomes` print "gap on D", not a smooth number.

- **Wild: plant a deliberately wrong number in the receipt and see whether anything flags it** — SECURITY — value 3 — effort M — risk low — category: measurement
  Why: receipts show spend, tasks and yield, computed on one path. Nothing cross-checks them, so a wrong number would look like a good one. wild.
  Done when: a nightly mutation of one receipt field (yield ×10) is caught by a second-path recompute in 100% of 20 trials.

- **Wild: show a blind-spot index per class in the pane header** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: asks cluster by class: exits, receipts, drills, brainstorm grounding. A single "asks per week since the class was last brainstormed" number would tell the user which area is quietly leaking. wild.
  Done when: the Foreman pane lists the top three classes by index, drawn from filed T-ids tagged by class.

Next question: which of the ten asks were also asked in a different wording earlier and silently deferred, so that repeated asks measure the cost of deferral and not novelty?
Next question: which "dropped as already built" verdicts came from grepping one name rather than three phrasings, and how many of them were wrong?
