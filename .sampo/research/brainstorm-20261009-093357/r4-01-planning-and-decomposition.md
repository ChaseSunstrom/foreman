# Brainstorm — lens: planning and decomposition

- **Assign every single-writer artifact to one owning step** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: T-0428 had to stop builders touching CHANGELOG.md, and T-0445/T-0446 add parallel lanes, which collide on the same kind of file. Assumption: the same hazard applies to lockfiles, migration numbers, generated files, snapshots and version bumps. At plan time, detect these artifacts and give each exactly one owner step, usually an integration step on the main thread. Lane briefs list them as forbidden.
  Done when: a test plan that has two lanes both touching a migration directory and a lockfile is rewritten so one step owns each file, and a builder brief for that plan lists both as off-limits.

- **Plan breaking changes as expand, migrate, contract** — FEATURE — value 4 — effort M — risk low — category: planning recipes
  Why: assumption: L refactors that change a signature, schema or config key are the plans most likely to leave a broken middle state, and the pack shows no recipe for them. Intake detects a breaking change and emits three phases. Expand adds the new form beside the old one. Migrate moves every caller, using a caller sweep. Contract removes the old form. Each phase must leave the gates green. This also gives the cleanup step the user complained about (cleanup requests that never got done) a named place in the plan.
  Done when: a fixture task "rename function X used in 5 files" produces a three-phase plan whose phase 3 deletes X, and the gate suite is green after each phase.

- **Plan on a critical chain with one shared buffer** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: the pack has estimates, pace and lane dispatch, but each step is estimated on its own. Instead, estimate each step at its median, mark the longest dependent chain, and hold one explicit buffer at the end. Overrunning steps draw down the buffer, and the band shows the burn. When the buffer is half spent, Foreman re-plans or cuts scope early. This replaces per-step padding, which hides risk.
  Done when: `fm task plan` on a 6-step L task prints the critical chain and buffer, and a simulated overrun on step 2 shows a reduced buffer and a replan prompt at 50%.

- **Bind steps to assumptions and invalidate only their dependents** — FEATURE — value 4 — effort M — risk med — category: replanning
  Why: `fm task assume` and re-check commands exist (C052), and replanning is currently all-or-nothing. Assumption: each step can list the assumption ids it relies on. When a re-check fails or a surprise lands, only the steps downstream of that assumption are marked stale and re-planned. Finished work whose assumptions still hold is kept.
  Done when: falsifying assumption A2 in a test plan marks exactly the steps citing A2, plus their successors, as stale, and leaves the other steps' status unchanged.

- **Sample several plans and use their disagreement as the risk map** — FEATURE — value 4 — effort M — risk low — category: plan quality
  Why: the idea pile mentions asking the user when sampled plans disagree, but not using the disagreement inside the plan. Assumption: tool-less `claude -p` children can each produce a plan independently. Steps that appear in all of them become the confident core. Steps that appear in only some are the uncertainty hotspots. Hotspots get spike steps, go earliest in the order, and get stricter verification.
  Done when: three sampled plans for one fixture task yield a core list and a divergent list, and the final plan puts a spike step before each divergent item.

- **Order plan steps by reversibility and rehearse the rollback** — FEATURE — value 4 — effort M — risk low — category: sequencing
  Why: the pack covers classifying forks as one-way or two-way doors, but not ordering the plan around them. Reversible steps run first. The plan carries an explicit point-of-no-return marker. Before that marker, a rollback step is written and dry-run once, and Foreman runs `fm ask` there if the user is attending. This matters for steps that publish, migrate data, delete or release.
  Done when: a plan containing a migration step lists it after all reversible steps, with a marker line and a rollback command whose dry-run is recorded.

- **Sequence human-dependent decisions before the unattended stretch** — FEATURE — value 4 — effort S — risk low — category: sequencing
  Why: the user runs night and drive modes and a lot of unattended work, and blocking asks cost the most when the user is away. At plan time, list the steps that need the user (decisions, credentials, taste calls), and where the plan allows it, move them first. Pre-batch them into one digest, with a default and an expiry on each. The plan then records an "unattended from step N" marker.
  Done when: a plan with two user-dependent steps scattered in the middle is emitted with both at the front, plus the marker, and the queue digest lists both.

- **Hide latency by scheduling slow steps first** — PERFORMANCE — value 3 — effort M — risk low — category: scheduling
  Why: `fm doctor` and the roundtrip e2e gate are slow gates, and T-0424 shows the friction pass already tracks slow-gate medians. Assumption: ledger durations let each plan step be tagged as CPU-bound, wait-bound (install, build, full suite) or thinking-bound. The plan starts the wait-bound ones in the background as early as their inputs allow, and gives the thinking steps the gaps.
  Done when: a fixture plan with one slow gate step is reordered so the gate starts before two independent edit steps, and total simulated wall-clock drops by the overlap.

- **Fuse small queued tasks that share a footprint** — FEATURE — value 3 — effort M — risk med — category: queue planning
  Why: the queue has many tiny related tasks (T-0437, T-0438, T-0435 all touch friction/capture), and each pays a full context load. Assumption: footprints can be forecast from `fm map` and past briefs. Foreman proposes a fused run that keeps separate briefs, criteria and commits but loads context once. It refuses to fuse when the criteria conflict.
  Done when: two queued S tasks touching the same module are offered as one run, the finished work leaves two commits and two closed briefs, and a conflicting pair is not offered.

- **Relax the task, then restore constraints one by one** — FEATURE — value 3 — effort M — risk low — category: planning recipes
  Why: assumption: L tasks fail on interacting constraints (speed, compatibility, edge cases, security), not on the happy path. Planning first drops the constraints and solves the bare problem. It then adds each constraint back as its own step with its own verify, in order of how much each one reshapes the design. Each step is green before the next constraint is added.
  Done when: a fixture brief with 3 listed constraints produces a plan with a base step and 3 restore steps, each with a verify that fails if the constraint is violated.

- **Plan from both ends and treat the gap as the unknown work** (wild) — FEATURE — value 3 — effort L — risk med — category: search planning
  Why: wild; assumption: forward steps from the repo's current state and backward steps from the acceptance criteria can be produced by separate children. Where the two chains meet, the plan is solid. The unmatched middle is labelled "unknown work" and gets a spike or a question, rather than being papered over with a vague step.
  Done when: for a fixture task, the plan output shows a forward chain, a backward chain, a matched join, and a non-empty gap section that is converted into spike steps.

- **Predict the file tree after every step and diff it live** (wild) — FEATURE — value 4 — effort L — risk med — category: execution check
  Why: wild; the pack has footprint forecasting and a step-level working set, but nothing compares expected with actual after each step. Each plan step carries a predicted `git status` (which files are added, modified or deleted). After the step, the executor diffs real against predicted, and a surprise triggers a replan check. Foreman records the surprises as data for a "plans forget these steps" learner.
  Done when: running a step that touches an unpredicted file prints a divergence line and opens a replan prompt, and a matching step prints nothing.

- **Write a plan by exquisite corpse across agent roles** (wild) — FEATURE — value 2 — effort M — risk low — category: ideation of plans
  Why: wild; assumption: plans written by one voice share its blind spots. Three children each write one step at a time, seeing only the criteria and the previous step, in the roles of builder, reviewer and maintainer. A reconciler then orders and de-duplicates the steps. Compare the result with a single-author plan through the cold-reader check, and keep whichever the check prefers.
  Done when: for three fixture tasks, the pipeline produces a merged plan and a recorded preference outcome versus the single-author plan.

- **Split any step whose commit message needs "and"** — CLEAN — value 2 — effort S — risk low — category: decomposition
  Why: assumption: step size drift is the common cause of 3-attempt blocks. Write the commit message for each step at plan time. Split any step whose message joins two actions with "and", and flag messages with no observable noun. Later, diff the real commit messages against the planned ones.
  Done when: a plan with the step "add flag and update docs" is linted into two steps, and a plan of single-action steps passes unchanged.
