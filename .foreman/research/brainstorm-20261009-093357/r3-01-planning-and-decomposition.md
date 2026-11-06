# Brainstorm — lens: planning and decomposition

- **Derive plan steps from the breakage** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: assumption: for CLEAN and refactor work, Foreman's step lists come from reasoning, not from the repo. Intake has steps, but nothing mechanically enumerates what a change will break.
  Done when: for a rename or signature change, `fm plan --probe` applies the minimal change in a scratch worktree, runs the compiler or tests, and writes one plan step per failure cluster. A test shows the step list matches the real call sites.

- **Prune steps whose postcondition already holds** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: assumption: tasks often turn out half-done, with a flag already present or a test already written. Backward-chaining from the acceptance criteria to the facts they need, then probing the repo, would drop satisfied steps. Existing ideas add pre/postconditions but don't use them to shrink the plan.
  Done when: a brief whose first two steps are already true in the tree yields a plan without them. The plan lists each pruned step with the probe command that proved it.

- **Stage every FIX as contain, cure, inoculate** — FEATURE — value 4 — effort M — risk low — category: decomposition
  Why: the user's own wording, "FIX: login times out on slow wifi", shows mitigation and root cause are usually the same task. The 3-failed-attempts block shows what happens when they are. Splitting them gives a fast mitigation, a closable root-cause fix, and a prevention step (regression test, gate).
  Done when: a FIX plan has three separately closable stages. Closing the contain stage records evidence and leaves the task open. The task can't be done until the inoculate stage has a test, or an explicit waiver.

- **Carry the remainder of every scoped-down task** — FEATURE — value 4 — effort S — risk low — category: scope
  Why: every captured task says "first version: …", and T-0034 and T-0035 sit deferred as L tasks. When a plan cuts scope, nothing tracks what was cut.
  Done when: finishing a task whose plan has a "cut" list auto-captures one linked remainder task per cut item. Each carries a revisit trigger. `fm task show` lists the remainder lineage.

- **Preflight the plan's world before step 1** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: T-0325 (needs a package install), T-0335/T-0336 (need live codex/gemini) and T-0316 are blocked on things outside the repo. Unattended runs find that out mid-way.
  Done when: plan acceptance runs a check for each declared external need (tools, credentials, network, versions). It tags steps "world-blocked" and reorders them last. The user gets one batched ask before work starts, not a stall at step 4.

- **Rebase the plan on a mid-task steer** — FEATURE — value 3 — effort M — risk med — category: replanning
  Why: the user's steers are frequent ("budget limits shouldn't block until 75%", "build it in Tauri"). Replanning exists, but nothing maps a new instruction onto done and pending steps.
  Done when: a steer during execution produces an impact table (steps kept, invalidated, added) and a plan patch. Invalidated steps that already have recorded evidence are marked stale, not silently kept.

- **Run Monte Carlo over the step graph** — FEATURE — value 3 — effort M — risk low — category: estimation
  Why: the user asked for pace and estimates (C051). Plans carry steps but no distribution. Per-step-type actuals from the ledger could be sampled across the dependency graph.
  Done when: `fm plan` prints a P50/P90 completion time and names the step that most often sits on the critical path in the samples. A bench case shows the P90 covers at least 80% of past tasks of that tier.

- **Start the common prefix while plans compete** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: M/L planning sits idle waiting on the 3+ options and second opinions. Every candidate plan usually begins the same way (read the code, reproduce, baseline gates).
  Done when: Foreman computes the shared leading steps of the rival plans and runs them read-only while the choice is made. The chosen plan references the evidence already gathered, and no step runs twice.

- **Score plans by how much reality rewrote them** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: a plan-revision history exists, but nothing grades a plan after the fact. A deviation taxonomy (steps added, split, reordered, dropped) would show which plan features predict rewrites.
  Done when: at task finish a "plan fidelity" record is written. `fm friction` reports the top two deviation kinds per task type, e.g. "FEATURE M plans omit a docs step 60% of the time".

- **Design once, derive the cluster's tasks** — FEATURE — value 3 — effort M — risk med — category: decomposition
  Why: T-0440 to T-0455 are 16 captured M tasks from one punch list. Several are plainly siblings (C024, C031 and C033 all touch the guard). Planning each alone repeats the design and can contradict itself.
  Done when: tasks tagged as a cluster share one design brief with decisions. Each task's plan cites it, and changing a shared decision flags every dependent plan as stale.

- **Wild: Build one to throw away, then plan** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild; assumption: for L tasks with high unknowns, a 10-minute ugly draft in a discarded worktree exposes the real seams, snags and missing helpers better than reasoning. The plan is then written from what broke, not from guesses.
  Done when: for a flagged L task, a throwaway lane produces a failure and surprise list, and the worktree is deleted. The final plan's risks cite specific draft findings, and nothing from the draft reaches the branch.

- **Wild: Make the plan a skeleton of empty git commits** — FEATURE — value 3 — effort M — risk med — category: execution
  Why: wild; resume at the exact step already matters to the user. If each step were an empty commit whose message holds its pre/postcondition and verify command, the git log would be the plan, and resume would be `git log`.
  Done when: approving a plan creates N empty commits on the task branch. Each step amends its own commit with the diff and evidence, and a killed session resumes from the first still-empty commit.

- **Wild: Slice features along a storyboard** — FEATURE — value 3 — effort S — risk low — category: decomposition
  Why: wild; the user gave screen-demo-style requests ("beautiful UI with smooth animations", the screen-recording bug idea). Writing a 5-frame storyboard of what the user will see, then making each frame one vertical slice, orders steps by visible value and gives each a natural smoke check.
  Done when: a FEATURE with a UI surface gets a storyboard of at most 6 frames. Each frame maps to one plan step with a `fm smoke` assertion, and the plan refuses to proceed if a frame has no observable check.
