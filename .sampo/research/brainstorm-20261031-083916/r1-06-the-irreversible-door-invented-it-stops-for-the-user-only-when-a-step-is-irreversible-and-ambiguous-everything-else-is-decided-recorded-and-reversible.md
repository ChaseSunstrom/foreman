# Brainstorm — lens: the irreversible door (invented): it stops for the user only when a step is irreversible and ambiguous; everything else is decided, recorded and reversible

- **Classify every action by door type before it runs** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: Mission 5 #8 asks Foreman to "stop only when something is irreversible and ambiguous"; the pack shows the guard, grants and `fm ship` but no single table saying which verbs are one-way (push, publish, migrate, delete, send) versus reversible. Assumption: today each gate decides on its own.
  Done when: `fm door NAME` prints reversible / costly-to-reverse / irreversible for every verb, and a test fails when a new verb lacks a class.

- **Ask only when the door is one-way and two readings disagree** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: T-2269's plan gate asks for readings by tier, but nothing joins "readings differ" to "action can't be undone". Assumption: `fm ask` fires today on either condition alone.
  Done when: a fixture with two readings on a reversible step records the decision and does not call `fm ask`; the same fixture on a publish step does.

- **Record every auto-decision as a one-line, undoable receipt** — FEATURE — value 5 — effort M — risk low — category: reversibility
  Why: "Everything else it decides and records" has no stated store; the user keeps asking for plain receipts (T-0795) and the steer on `fm decide`. Assumption: decisions are scattered in task notes.
  Done when: `fm decisions` lists each decision with its confidence, the alternative not taken, and an `undo` command that works for a seeded example.

- **Snapshot before the last reversible moment** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: `fm ship` and the push grant exist, yet nothing proves a push, migration or lane merge can be walked back. T-2288's migration proof covers only one kind.
  Done when: before `fm ship`, a ref/tag and the previous main SHA are written, and `fm rollback T-N` restores them on a scratch repo in a test.

- **Downgrade an irreversible step by rehearsing it on a copy** — FEATURE — value 4 — effort L — risk med — category: safety
  Why: `fm prove --migration` already rehearses on a throwaway database; generalise it to publish, release and file deletion so that the door stays shut until the rehearsal passes. Assumption: only migrations are rehearsed today.
  Done when: a task with a delete/publish step refuses to proceed without a rehearsal record, and the record names the copy used.

- **Make the confidence statement checkable** — FIX — value 4 — effort M — risk low — category: calibration
  Why: T-2290 records predictions and scores them; the stated confidence ("low-confidence assumption needs research") is never scored. Earlier question: numbers never checked by anything but their producer.
  Done when: `fm calibration` shows stated-confidence buckets against held-up rate from closed tasks, and flags a bucket off by more than 20 points.

- **Hold a one-way action behind a timer the user can cancel** — FEATURE — value 4 — effort S — risk low — category: user control
  Why: User wants no stops, yet irreversible-and-ambiguous cases need a check. A default-with-countdown ("pushing in 10 min unless `fm hold`") gives a non-blocking path, matching steer 3 (don't stop for pace).
  Done when: an ambiguous irreversible step posts a notice, proceeds on the default after the timeout in a test with a fake clock, and aborts on `fm hold`.

- **Detect a door hidden inside a reversible-looking command** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard stops destructive commands, but a script or `make deploy` can hide a push. T-2289 shows scratch/script-cache edge cases already hit. Assumption: the guard matches command text, not effects.
  Done when: a fixture script that calls `git push` inside `run.sh` is classed irreversible by the door table via static scan, and the guard asks.

- **Stop on a reversible step that quietly becomes irreversible** — FIX — value 3 — effort M — risk med — category: judgment
  Why: a file the user hasn't committed, a local branch with the only copy, a lane worktree with unmerged work: deletion is "cleanup" until it isn't (T-2289 `fm lane rm`). Assumption: look-before-delete is per verb.
  Done when: `fm lane rm` and cleanup verbs check for unique, unpushed content and refuse naming it; tested with an unmerged lane.

- **Wild: Hold a "regret drill" nightly** — FEATURE — value 3 — effort M — risk low — category: reversibility
  Why: wild. Pick last day's auto-decisions at random, replay their `undo` on a scratch clone, and report which ones don't actually undo.
  Done when: the nightly report lists N decisions tried and the count whose undo restored the prior tree hash.

- **Wild: Let a cold child play devil's advocate on the one-way door** — FEATURE — value 3 — effort M — risk low — category: judgment
  Why: wild. Before any irreversible step, a tool-less Haiku child sees only the diff and the stated intent and writes "the strongest reason not to"; a quote-grounded objection (as T-2246) blocks, others are advisory.
  Done when: a seeded bad publish is held by a quoted objection; an ungrounded objection is logged but doesn't block.

- **Wild: Give every user steer a "door budget"** — FEATURE — value 3 — effort S — risk low — category: user control
  Why: wild. The user says "don't ask me"; record how many irreversible-and-ambiguous stops they get per week (default 2), and when exceeded, Foreman must widen its default rather than ask.
  Done when: `fm doors` shows asks used against the budget, and a test shows the third ask in a week becomes a recorded default.

- **Explain each stop as the one question and its two outcomes** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: the user's earlier ideas ask for refusals in their vocabulary; a stop should read "Doing X can't be undone. Y or Z? Default Z." Assumption: `fm ask` text is free-form today.
  Done when: every `fm ask` from a door stop has fields action, why irreversible, two options, default; a lint rejects free-form ones.

Next question: Which of Foreman's existing grants (push, publish, mandate) would still be valid after the user's situation changes, and does anything notice when a grant outlives its reason?
Next question: When the door table says "irreversible", how often is that wrong in practice (a push that was force-reverted, a delete that git recovered), and should the class be learned from outcomes?
