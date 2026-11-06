# Brainstorm — lens: simplicity

- **Delete verbs by usage receipt, not by hunch** — CLEAN — value 4 — effort M — risk med — category: pruning
  Why: pack lists 1,158 skill files, a HELP_TIERS registry every feature edits, and "Report which features are never used" only as a report. Nothing turns that into deletion. Assumption: the ledger records verb invocations.
  Done when: `fm prune --dry-run` lists every verb with zero invocations in 60 days, each with its caller count, and a deletion task is opened for one of them.

- **Retire the "Later from T-…" tail into one dated parking file** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: ~25 deferred tasks titled "Later from T-0760/0818/0843" sit in the open queue with no trigger; the user wants to be asked nothing. Earlier ideas propose an epic or a digest, not removal from the hot queue.
  Done when: `fm state` open-work count drops by those tasks, each is one line in `.foreman/parked.md` with a revisit condition, and `fm unpark <id>` restores it.

- **Make one verb own each job: a duplicate-purpose report** — CLEAN — value 3 — effort M — risk low — category: consolidation
  Why: ideas so far repeatedly invent overlapping stores (hints, fixes, lessons, vetoes, decisions, preferences). Assumption: several of these already exist as separate files.
  Done when: `fm doctor` prints groups of verbs/stores that read or write the same kind of data and the count is lower after a merge task.

- **Give every setting a single source and a printed effective value** — FEATURE — value 3 — effort S — risk low — category: config
  Why: escape-hatch flags, `.foreman/off/` toggles, settings file and env vars are all proposed or present; users can't tell which wins. Assumption: precedence is currently implicit.
  Done when: `fm config show` lists every effective setting with its origin (default, file, env, flag).

- **Cap the default `fm` help at ten lines** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the project has a verb for nearly everything and the user keeps asking for more tools; a newcomer sees HELP_TIERS growth. Assumption: tier 1 is currently longer than ten entries.
  Done when: bare `fm help` prints ≤10 lines, a golden test fails if it grows, and `fm help --all` still lists everything.

- **Merge task states into four visible words** — CLEAN — value 3 — effort M — risk med — category: vocabulary
  Why: the queue shows deferred, blocked, open and more, plus stage rails and statuses; "Explain each blocked item with its unblock command" suggests the states already confuse. Assumption: more than four states exist in briefs.
  Done when: pane and `fm state` show only now/next/waiting/done, with the old state kept as a reason string, and old briefs load unchanged.

- **Auto-close blocked tasks whose unblock is user-only into the final report** — FEATURE — value 4 — effort S — risk low — category: queue hygiene
  Why: T-0325, T-0335, T-0336, T-0337, T-0352, T-0418 are blocked on things only the user can do; the mission says those belong in the final report, not the queue.
  Done when: the final report lists each with its exact command, and blocked tasks leave the active queue until the blocker is observed resolved.

- **Ship `fm explain-less`: show only what changed vs the last turn** — FEATURE — value 3 — effort M — risk med — category: output
  Why: "Make healthy turns add zero bytes" is proposed for hook injection but not for the verbs' own output. Assumption: verbs print full state each call.
  Done when: running `fm state` twice with no changes prints one line the second time.

- **Wild: A "one-page Foreman" mode that is the entire product on a single screen** — FEATURE — value 4 — effort L — risk med — category: lite mode
  Why: wild; T-0794 and T-0861 defer a Lite mode for lack of evidence. Build it as a measurement: plan, prove, next, nothing else.
  Done when: `FM_MODE=one` exposes exactly three verbs, and a scripted session completes a task through them.

- **Wild: Delete-first Fridays: a weekly forced deletion task** — CLEAN — value 3 — effort S — risk low — category: pruning
  Why: wild; the loop only adds. Each week the queue gets one task whose goal is net-negative lines, chosen from the least-used code.
  Done when: a task titled "Delete-first" is auto-created weekly and closes only if the diff's net line count is negative with gates green.

- **Wild: A complexity budget that blocks merges which grow the verb count** — SECURITY — value 3 — effort M — risk med — category: governance
  Why: wild; every round adds verbs (the user said "make more tools"). A ratchet paired with the usage-based pruning forces an add to be matched by a removal or an explicit waiver.
  Done when: CI fails a merge that raises the verb count without a removal or `--because` waiver recorded in the brief.

- **Collapse the three ledger readers into the one shared reader** — CLEAN — value 3 — effort S — risk low — category: consolidation
  Why: T-shipped `c.ledger_events` was added for fmoutcomes, while fm ui, recall and others rescan the ledger on their own. Assumption: some still read files directly.
  Done when: a grep-based test fails if any module outside the shared reader opens the ledger files.
