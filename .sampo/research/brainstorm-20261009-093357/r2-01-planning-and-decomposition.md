# Brainstorm — lens: planning and decomposition

- **Ground every plan against the repo** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: assumption: plans name files, functions and commands from the model's memory. Nothing in the pack checks that they exist, and "resolve every symbol" applies to diffs, not plans. Plan-time lint would catch hallucinated targets before a builder lane spends tokens.
  Done when: `fm task plan` rejects a fixture plan that names a nonexistent file, symbol or `fm` subcommand, and flags steps whose verbs are unbounded ("improve", "handle", "clean up") with no file target.

- **Mark plans stale when their footprint changes** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the pack shows parallel lanes, merge trains and user hand-edits. A plan written at HEAD A is silently wrong at HEAD B. Existing replans fire on failure, not on drift. Record the files, symbol signatures and tree hashes each plan step depends on.
  Done when: after a fixture commit touches a file a queued plan depends on, `fm task show` reports "plan stale: step 3 relies on X, changed in <sha>" and offers a rebase of just the affected steps.

- **Plan in cut-line tiers** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: the user pushed back that budget and pace limits shouldn't block work, and they want queues to keep moving. Plans are currently all-or-nothing. Split M/L plans into must/should/could increments, each ending in a shippable, green state with its own done-check.
  Done when: an L fixture plan has three tiers, and stopping after tier 1 lets `fm task done` pass with tiers 2–3 auto-captured as follow-up tasks.

- **Calibrate step size from history** — FEATURE — value 3 — effort M — risk low — category: decomposition
  Why: assumption: the ledger and bench replays hold per-step diff size, retries and verify outcomes. Steps that are too coarse fail and retry, and steps that are too fine burn round trips. Learn the sweet spot per task type and flag outliers at plan time.
  Done when: `fm plan lint` prints "step 4 is ~3× the median size for FEATURE M and failed on retry in 60% of similar steps; consider splitting", backed by a computed table from the ledger.

- **Plan as a test ladder** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: acceptance criteria already carry verify commands and `fm task prove` does red→green. A ladder orders tests from degenerate to general, in the style of the transformation priority premise, so each step is "turn the next rung green". This gives built-in progress, a natural resume point after `/compact`, and an obvious place to cut a step.
  Done when: a FEATURE brief option generates an ordered rung list, and `fm task step` advances only when the current rung is red-then-green, recorded in evidence.

- **Run optimiser passes over the plan** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: assumption: plans are structured enough to hold as a small IR. Treat the passes as compiler passes: fuse tiny steps, split at verification boundaries, order reversible steps before irreversible ones, hoist independent steps into parallel lanes. Each pass is logged and can be benched or dropped.
  Done when: `fm plan opt --explain` shows the before/after plan with the pass that made each change, and `fm bench` can disable a pass and compare outcomes.

- **Decompose RESEARCH into a question tree** — FEATURE — value 3 — effort M — risk low — category: decomposition
  Why: RESEARCH tasks like T-0316 and T-0336 sit blocked, and the pack's decomposition tooling is all code-shaped. Break a research task into sub-questions with an expected answer type (fact, measurement, yes/no), a stop rule and a source standard, then fan out `fm-recon` per leaf.
  Done when: a RESEARCH task produces a tree where each leaf ends as answered with a cited source, unanswerable with a reason, or out of scope, and `done` refuses while a leaf is open.

- **Size the plan from measurements** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: plans estimate "update all callers" or "run the full suite" from guesswork. A few bounded probes (call-site count, test runtime, file length, gate duration) let a plan state that a step touches 41 sites, so it should be a sweep step or its own lane.
  Done when: an M/L brief contains a "Measured" block with probe commands and numbers, and a step that touches more than N sites is auto-flagged for a sweep or split.

- **Check declared step order against the real dependency graph** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: step order is currently asserted by the model. `fm map` already knows tests→src, and co-change data may exist. A mismatch, such as a step editing a caller before its callee, means a bad plan.
  Done when: a fixture plan with an inverted dependency gets "step 2 depends on step 4's output (fmcli imports the function you create there)" and a suggested reorder.

- **Fuzz the plan against its request (wild)** — FEATURE — value 3 — effort M — risk low — category: reasoning
  Why: wild. Mutate the request by dropping a clause, swapping a noun or reversing a constraint, and re-plan cheaply. A plan that doesn't change was ignoring that part of the request. This is a sensitivity test of whether intake used what the user said, aimed at the "silently dropped clause" failures in the user's steers.
  Done when: `fm plan sensitivity` lists the request clauses with no effect on the plan, and a fixture request with a clause the plan ignores is flagged.

- **Fold plans like origami (wild)** — FEATURE — value 3 — effort M — risk low — category: planning UX
  Why: wild. A 12-step plan overwhelms the band and the pane. Collapse it to three load-bearing steps, and unfold a step into its sub-steps only when execution reaches it or the user asks. The same plan is readable at glance depth and executable at full depth.
  Done when: the band shows at most three plan lines for any task, and expanding a step shows its sub-steps from the same brief file with no regeneration.

- **Draw the plan as a fog-of-war map (wild)** — FEATURE — value 3 — effort M — risk low — category: planning UX
  Why: wild. Render unknowns from the known-unknowns ledger as fogged regions of the plan. Probing steps clear fog, and the next steps appear only as terrain is revealed. It makes "riskiest unknown first" visible, and shows the user why planning ahead stopped.
  Done when: the web UI task view shows fogged nodes for open unknowns, and resolving an unknown clears its fog and updates the downstream steps.
