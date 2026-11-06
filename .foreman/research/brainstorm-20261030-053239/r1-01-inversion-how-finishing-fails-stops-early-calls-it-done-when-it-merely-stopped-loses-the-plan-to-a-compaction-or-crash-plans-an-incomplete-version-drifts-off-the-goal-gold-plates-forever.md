# Brainstorm — lens: inversion: how finishing fails — stops early, calls it done when it merely stopped, loses the plan to a compaction or crash, plans an incomplete version, drifts off the goal, gold-plates forever

- **Write a stop-reason verdict on every session end** — FEATURE — value 5 — effort M — risk low — category: done-vs-stopped
  Why: gap map lists "done-vs-stopped verdict" as missing; Stop drive has DRIVE_MAX, no-progress stop, contract bound, usage limit, crash, and the model's own "done" but records none as a typed reason.
  Done when: after each of six forced endings (usage limit, kill -9, drive cap, no-progress, model says done, all criteria met) `fm goal status` prints a distinct typed verdict, and only the last is "finished".

- **Gate "finished" on a goal-level closing audit by a cold reader** — FEATURE — value 5 — effort M — risk med — category: completion
  Why: `fm task finish` verifies per task, but nothing checks that the set of tasks still covers the goal; the model saying "done" is the failure mode named in the brief.
  Done when: a goal whose tasks are all closed but with one contents-list item lacking a task is refused "finished" with that item named; adding the task and closing it flips the verdict.

- **Freeze the contents list as a sealed, versioned object** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: `fm mission` only prompts; no stored contents list exists, so a plan that is incomplete or drifts has nothing to be measured against. Same sealing pattern as the gen-0 charter.
  Done when: `fm goal plan` writes contents v1 with a sha256 and ledger event; editing it outside `fm goal amend` fails `fm goal check`, and each amend records a reason.

- **Rate the plan for omissions before work starts** — FEATURE — value 4 — effort M — risk med — category: plan quality
  Why: "plans an incomplete version" is the earliest failure; the Mission lessons say model boilerplate lists are weak. Grade the list against grounded sources (repo map, user words, sibling products) and against the capability × verb × surface grid from coverage.md.
  Done when: a seeded goal with a deliberately omitted surface (e.g. no MCP item) gets that gap flagged by `fm goal plan --check` before any task is created.

- **Detect drift by tracing every task back to a contents item** — FEATURE — value 4 — effort S — risk low — category: drift
  Why: sessions wander; user's steers show widening mid-run ("widened — the live rerun showed…"). An orphan task with no contents item is drift or a legit discovery and should be named either way.
  Done when: `fm goal check` lists tasks with no parent item and items with no task; creating an untraced task prints a one-line orphan note at focus.

- **Add a gold-plating stop: marginal-value cutoff per goal** — FEATURE — value 4 — effort M — risk med — category: gold-plating
  Why: the forever loop stops after 2 dry rounds, but a goal with a finite contents list has no "enough" rule; best-in-class lists grow without bound.
  Done when: items added after plan v1 must cite evidence (a failure, an exam miss, a user word), and a goal with all v1 items done and only uncited additions pending reports "finished, extras deferred".

- **Re-inject a one-screen goal card every session until finished** — FEATURE — value 5 — effort S — risk low — category: continuity
  Why: gap "goal carried across days"; PreCompact only preserves a task's Resume section, so a crash between tasks loses the goal. Must fit under the ~10 KB hook limit.
  Done when: after kill -9 and a fresh SessionStart, the injected context holds the goal, the percent done, the next item, and stays under 4 KB with bench_hooks passing.

- **Wire unmet MUST clauses into the Stop hook as blockers** — FEATURE — value 4 — effort M — risk med — category: stop hook
  Why: gap map "clauses wired to the Stop hook"; MUST lines in gen-0 (tests, docs, CHANGELOG, site, pane, every surface) are the finish definition but only nudge at focus.
  Done when: a goal with an unmet "docs" clause makes the Stop hook block "done" naming that clause, and meeting it releases the block.

- **Make a finish-checklist a derived grid, not a remembered list** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: the MUST list (tests, exam, docs, site, pane, five surfaces) was repeated by hand on every Mission; the user had to ask for satellites (T-2120..2127 as late asks).
  Done when: filing a capability creates satellite rows automatically and `fm goal status` shows a capability × surface grid with unmet cells as the remaining work.

- **Wild: Hold a pre-mortem and store its failure modes as clauses** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: assumption: a child asked "it is a month later and this goal failed; why?" yields concrete failure clauses that the Stop hook then checks. Wild.
  Done when: `fm goal plan` writes ≥3 pre-mortem clauses, each tied to a verify command, and one deliberately triggered failure is caught by its clause.

- **Wild: Dead-man heartbeat that distinguishes asleep from dead** — FEATURE — value 3 — effort M — risk low — category: crash recovery
  Why: assumption: resume currently depends on the user starting a session; a heartbeat file with a goal-level "last verified step" lets the next start say "stopped by crash at step X, not finished" with no guess. Wild.
  Done when: after kill -9 mid-task, the next `fm resume` reports crash with the last heartbeat time and the exact stage, not "done".

- **Wild: Replay a finished goal against its own plan as a time-lapse** — FEATURE — value 2 — effort M — risk low — category: observability
  Why: a goal living across days has no readable story; ledger events already hash-chain. Render plan v1, amendments, stops, and finish verdicts as a timeline on the pane and site.
  Done when: `fm goal story` prints a chronological timeline, and the site page renders the same for an exported goal.

- **Plant a "looks done" goal in the exam** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the held-out exam must grade #4 with child-authored scenarios; the key failure is premature done. Scenarios: one goal truly finished, one with a missing docs item, one stopped by usage cap, one with a crash mid-plan; arms must say finished only for the first.
  Done when: `fm exam` has G-finish kinds and the plain session arm scores worse than the Foreman arm on false "done" claims.

- **Wild: Dissenting-vote finish: two independent closers must agree** — FEATURE — value 3 — effort M — risk med — category: completion
  Why: assumption: a model grading its own finish is biased; a second tool-less child sees only the contents list and the evidence and votes. Disagreement keeps the goal open with the dissent quoted. Wild.
  Done when: with a planted missing item, the second closer votes "not finished" while the first votes "finished", and the goal stays open.

- **Cap each plan revision by evidence, and show scope growth** — FEATURE — value 3 — effort S — risk low — category: gold-plating
  Why: drift and gold-plating both show as a contents list growing silently; a number on the card makes it visible.
  Done when: the goal card shows "v3, +4 items since v1 (2 cited, 2 not)", and the count is correct after two amends.

Next question: Which of the six endings (usage limit, crash, drive cap, no-progress, model-says-done, criteria met) can Foreman actually observe from inside a hook, and which can only be inferred afterwards from the next session's state?
Next question: When a user's goal text is one vague line, what grounded sources besides the repo (their past asks, ledger, sibling products) are reliable enough to build the contents list from without model boilerplate?
