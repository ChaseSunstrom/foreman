# Brainstorm — lens: planning and decomposition

- **Hoist shared prerequisites across the queue** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the captured tasks C024, C026, C033 and C075 all change fmguard (rule ids, refusals that carry a fix, harness parity, the offending segment), so each plans its own plumbing. Nothing looks across the queue for shared groundwork.
  Done when: `fm plan queue` on a fixture queue of three tasks that need the same helper proposes one foundation task ahead of them, and the three plans cite it as a dependency.

- **Sequence plans riskiest-unknown first** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: briefs list assumptions with confidence, but steps follow the natural build order. Tasks that block after 3 failed attempts have usually hit the unknown late. Order by (1 − confidence) × cost to undo, and make each low-confidence assumption a step-0 probe.
  Done when: a brief with one 30%-confidence assumption produces a plan whose first step is a probe command for it, and the plan lint fails if that probe comes after an edit step.

- **Learn the steps plans forget** — FEATURE — value 4 — effort M — risk low — category: planning, learning
  Why: the user steered that cleanup requests "never got done". At finish, diff planned steps against executed steps and tag the added ones (cleanup, docs, migration, test for the failure path). Intake then adds the most frequent missed steps as a checklist.
  Done when: after 5 finished tasks that each added a cleanup step late, `fm plan` on a new task lists "cleanup" as a step with a "forgotten in 5 of 5 recent plans" note.

- **Give every M/L plan a pivot table** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: briefs already carry 3+ approach options, but nothing says when to abandon the chosen one. Each option gets a tripwire ("if the probe in step 2 shows X, switch to option B"), so a pivot happens at the probe, not after 3 failed attempts.
  Done when: `fm task done` on an M plan is refused if the chosen approach has no tripwire, and a fired tripwire records a pivot event naming the fallback option.

- **Plan in rolling waves with versioned replans** — FEATURE — value 4 — effort M — risk med — category: planning, execution
  Why: execute.md follows a fixed step list. Detail only the next wave of steps and leave the rest coarse. Force a replan when a step overruns 2× its estimate, touches a file outside the forecast footprint, or surfaces a contradiction. Keep each plan version with the reason for the change.
  Done when: a scripted task that touches an unforecast file stops and writes plan v2 with a "why" field, and `fm task show` lists both versions.

- **Decompose along oracle availability** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: a bad verify command already got through once (`-k a or b` ran no tests). Cut tasks so every piece has a check that can fail. A piece with no feasible check either merges into its neighbour or gets "build the check" as its first step.
  Done when: plan lint rejects a step whose verify command is empty or never runs a test. It suggests a merge or an added check step, and a fixture plan passes after the fix.

- **Trace plan steps to criteria** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: briefs have steps and acceptance criteria but no mapping between them. Orphan steps are scope creep and uncovered criteria are missed work. Both are cheap to detect.
  Done when: a plan with a step serving no criterion and a criterion served by no step prints both lists, and the plan is not marked ready until each is resolved or waived with a reason.

- **Build a walking skeleton first on FEATURE L** — FEATURE — value 3 — effort S — risk low — category: decomposition
  Why: L tasks are likely planned layer by layer, so integration surprises arrive last. Step 1 becomes the thinnest end-to-end path with stubs, and it is verified before any layer is deepened.
  Done when: an L plan's step 1 has a verify command that exercises entry to output end to end, and the plan lint fails an L plan without one.

- **Ship a library of named decomposition recipes** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: assumption: plans are invented fresh each time. Recipes for expand-contract migration, strangler replacement, characterize-then-refactor, dark launch and bisect-then-fix each give a step skeleton, and intake picks one by task shape. This is seeded knowledge, distinct from the learned playbooks idea.
  Done when: intake on "rename a state field used by 3 modules" selects expand-contract and emits steps for add, dual-write, migrate, remove. A CLEAN task selects characterize-then-refactor.

- **Cut lane seams with the co-change graph** — FEATURE — value 3 — effort M — risk med — category: decomposition
  Why: `fm map` and git history exist, and lane dispatch is planned. Nothing proposes where to cut an L task. A min-cut over files that change together gives sub-tasks with the least overlap.
  Done when: for an L fixture touching two clusters, `fm plan split` proposes two sub-tasks with disjoint file sets and states the overlap count it minimised.

- **Test decomposition on a cold cheap model** — FEATURE — value 4 — effort M — risk low — category: planning, agents — wild
  Why: assumption: a step is well decomposed if a weak executor can start it correctly. Hand each step text alone to fm-scout (Haiku) and ask for the first action and the verify command. A mismatch with the plan means the step is vague or too big.
  Done when: a fixture plan with one vague step ("make auth better") is flagged, while a concrete step passes. The flag shows the scout's reply next to the intended action.

- **Write the plan to fail, then invert it** — FEATURE — value 3 — effort S — risk low — category: planning — wild
  Why: assumption: models critique their own plans weakly but are good at sabotage. A recon pass writes the plan most likely to fail on this brief, the main thread inverts each failure move into a guard step, and unanswered ones become risks.
  Done when: for an M brief, the plan has a "failure moves → counter-steps" table with at least 3 entries, and one counter-step appears in the final step list.

- **Run planning poker across agent roles** — FEATURE — value 3 — effort M — risk med — category: planning, agents — wild
  Why: assumption: independent estimates from builder, reviewer, debugger and recon views disagree where complexity hides. The spread is the signal, and it decides whether to spend a spike or an L-plan tournament.
  Done when: `fm plan poll` returns four tier and effort estimates for a brief. When they differ by more than one tier, it names the step each role disagrees on and recommends a probe.

- **Plan tasks by their ending** — FEATURE — value 3 — effort S — risk low — category: planning — wild
  Why: write the close-out card first: the commit story, the one proof line, the "not verified" list. Steps are then derived backward from what that card must truthfully say. Anything in the card with no step is a gap.
  Done when: a brief carries a draft close-out, and `fm task done` diffs the final close-out against the draft and shows the claims that were dropped or added.
