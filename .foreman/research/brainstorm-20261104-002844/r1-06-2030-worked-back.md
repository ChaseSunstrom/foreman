# Brainstorm — lens: 2030 worked back

- **Resolve state from the main repo inside lane worktrees** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the pack says evidence and lease commands fail inside the builder worktree the harness puts the agent in. In 2030 every run is in a worktree, so this is the first thing to fix.
  Done when: `fm evidence` and `fm lease` run from inside a `fm lane` worktree, exit 0, and write to the main repo's state dir (checked via `git rev-parse --git-common-dir`).

- **Compile a goal into done-predicates, and compute done from them** — FEATURE — value 5 — effort L — risk med — category: goal
  Why: the long tier has 0/6 true done and 6 false dones, unchanged since gen 2. Assumption: the false dones come from the agent asserting done in prose. Each vague goal becomes a `goal.md` of falsifiable clauses, each bound to a command. Close is refused while any clause is red or unmeasured.
  Done when: on the six long-tier scenarios, a task with one failing predicate cannot close, and the false-done count is 0 of 6.

- **Journal intent and result per step, and resume from the journal** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix). Today it is rebuilt from transcript and ledger inference. Instead, a write-ahead step journal records "about to do X" and "X verified". Resume reconciles it with git state and names the first unverified step.
  Done when: after SIGKILL at a random point in a goal run, `fm resume` prints the step it will redo and why, and the redone step is idempotent in a test.

- **Kill the goal run at every plan step and compare it with an uninterrupted run** — FIX — value 4 — effort M — risk low — category: resume
  Why: the planted-fault tier covers only one kill per scenario. Resume bugs sit at particular step boundaries. Run k = 1..N kills on a small scripted goal.
  Done when: for every k, the final tree and predicate results match the uninterrupted run, and a planted resume bug in step 3 is caught by the k=3 case.

- **Re-inject a 40-line goal anchor at PreCompact and SessionStart** — FEATURE — value 4 — effort S — risk low — category: compaction
  Why: goals last days and compactions are certain. The anchor holds the goal's words, predicate states, current step and the one `Next:` command. It is read from the file, not from the summary.
  Done when: after a forced compaction in the long tier, the builder's next action cites the current step id, and the anchor size stays ≤40 lines at 50 predicates.

- **Take over a dead holder's lease with proof of death** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: lease commands exist and break in worktrees. A killed session leaves a lease nobody can release. The takeover needs the pid and start time, or a missed heartbeat, and records who took it.
  Done when: killing a lease holder lets a second session take the lease after the TTL, and a live holder's lease is refused.

- **Carry evidence across a lane merge, rebased onto the landed commit** — FIX — value 4 — effort M — risk low — category: evidence
  Why: assumption: evidence recorded in a builder worktree is keyed to a branch or sha that disappears when the lane lands, so the close at the end of a multi-day goal finds none.
  Done when: evidence from a lane is still found by `fm evidence list` for the landed sha, and the stale branch sha is marked superseded.

- **Hold done as provisional for 72 hours, then re-run the predicates** — FEATURE — value 4 — effort M — risk low — category: goal
  Why: true done means it stays done. A predicate run on a schedule reopens the goal if it flips, and the false-done counter learns from the reopening.
  Done when: a planted regression after close reopens the goal within the window with the failing predicate named.

- **Converge two planners that see only the goal** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: a vague goal gets a plan that is complete only by luck. Two cold planners decompose it, the step sets are diffed, and the plan is rerun until two rounds add no new step.
  Done when: on a seeded goal with a known hidden step (migration, docs), the converged plan contains it, and a single-planner run does not.

- **Judge done from the goal's words and the final evidence only** — FEATURE — value 4 — effort S — risk low — category: goal
  Why: the false dones are claimed by the agent that did the work. A tool-less judge sees only the user's sentence and the evidence files, never the plan, and answers "what in the sentence is unproven?"
  Done when: on the six false-done scenarios the judge names the unproven clause in at least 4.

- **Write the goal as a plain file any harness can resume (GOAL.md)** — FEATURE — value 3 — effort S — risk low — category: portability
  Why: Codex, Gemini and opencode are supported surfaces and Claude may not be the next model. Resume that needs one harness's transcript can't cross.
  Done when: a Codex session started in a repo with a half-done `GOAL.md` prints the same next step as Claude Code does.

- **Wild: write the 2030 post-mortem first** — FEATURE — value 4 — effort M — risk low — category: goal
  Why: wild. At intake, a child writes "how this goal got declared done and was not" in five lines. Each failure mode must become a predicate or a stated non-goal.
  Done when: every post-mortem line maps to a predicate id or a "not covered" line in `goal.md`, and `fm goal` refuses to start with an unmapped line.

- **Wild: make the goal hand-off model-swappable** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: wild. A goal run stops mid-way and a different model family finishes it, using only `goal.md`, the journal and the evidence. This is the proof that the state lives in files rather than in the model.
  Done when: a long-tier goal started on one model and finished on another passes all its predicates, with the swap recorded.

- **Wild: race two decompositions and keep the one that gets green first** — FEATURE — value 3 — effort L — risk high — category: planning
  Why: wild. Two lanes take different step orders for the same goal under the budget cap, and the loser's lane is parked as a dissent. This is the only way to learn which decomposition is better without guessing.
  Done when: on one scenario, both lanes run to a predicate verdict, the winner lands, and the loser's branch and cost are recorded.

Next question: which of the 6 long-tier false dones were wrong about a clause that was never written down, and which were wrong about a clause that was written but not run?
Next question: when a resumed goal redoes a step, how often does the redo undo user edits made in between, and does the journal know?
