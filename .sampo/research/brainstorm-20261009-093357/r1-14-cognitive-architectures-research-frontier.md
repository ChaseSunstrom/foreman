# Brainstorm — lens: cognitive architectures (research frontier)

- **Keep a typed working-memory scratchpad per task** — FEATURE — value 5 — effort M — risk low — category: cognition
  Why: Today's thinking lives in briefs and prose, and `/compact` loses reasoning. Assumption: nothing structured holds open questions, current belief, and next-probe between steps. Add `fm task think` with slots (goal, belief, open questions, rejected paths, next probe) that resume and the handoff inject.
  Done when: after a forced compact, the resumed session's first message cites the stored belief and the next probe, and a test asserts the slots round-trip.

- **Run a deliberate–act–reflect loop with a step-level prediction** — FEATURE — value 5 — effort M — risk low — category: reasoning
  Why: execute.md has per-step discipline but no stated expectations to compare against. Before each step, record "I expect X"; after it, record the delta. Surprises (already an idea elsewhere as a log) here trigger replanning, not just logging.
  Done when: a step whose recorded expectation mismatches the result is flagged and the plan gets a revision entry.

- **Replan on evidence, with a plan-revision history** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: Plans are written at intake, and "3 failed attempts → block" is the only adaptive response. Assumption: plans don't get versioned. Treat the plan as a revisable hypothesis: each revision records the trigger, what changed and why, and drift from the original brief is checked.
  Done when: `fm task plan --revise` stores a diff against the previous plan with its trigger, and `fm task show` lists the revisions.

- **Search over approaches with a value function** — FEATURE — value 4 — effort L — risk med — category: search
  Why: Briefs list 3+ approaches for M/L but choose by judgment. Score each approach on cheap probes (spike results, recall of similar solved tasks, gate partial scores), expand the most promising, and prune the rest, with the pruning recorded.
  Done when: an L task's brief shows per-approach probe results and a stated reason for the chosen branch, produced by a command rather than prose.

- **Calibrate confidence against outcomes** — FEATURE — value 4 — effort M — risk low — category: metacognition
  Why: Briefs already carry assumptions with confidence, but nothing scores them. Compare stated confidence to what happened at done and produce a per-task-type calibration curve that sets the thresholds for when to ask, spike, or proceed.
  Done when: `fm calibrate` prints a reliability table from finished briefs, and intake escalates an assumption once its bucket's hit rate falls below a threshold.

- **Add a Socratic problem-framing pass before decomposition** — FEATURE — value 4 — effort S — risk low — category: understanding
  Why: The user's own words are terse; intake classifies and expands but doesn't test the framing. Assumption: no step asks "what would make this request the wrong problem?". Generate 2–3 rival framings (symptom vs cause, narrow vs general) and pick one explicitly, noting the others in the brief.
  Done when: the brief for a terse request contains a "rival framings" section with a chosen one and a reason.

- **Build a causal model of the project from outcomes** — FEATURE — value 4 — effort L — risk med — category: world-model
  Why: The map and the lessons are flat lists. Keep a graph of "touching A broke B" and "this test guards that module", learned from ledger co-failures, so planning can predict blast radius and seed which gates to run first.
  Done when: a new plan on a file lists the likely-affected modules and tests from the graph, and a replay over past tasks shows predictions beat a co-change baseline.

- **Give each agent type a reasoning strategy, not only a role** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: Agents differ in tools and scope but think the same way. Assign strategies: debugger does hypothesis elimination, reviewer does adversarial counterexample search, recon does breadth-then-depth, planner does backward chaining from acceptance criteria. Bench which strategy wins by task type.
  Done when: each agent definition names its strategy and a bench run reports the pass rate per strategy per task type.

- **Distil episodic memory into reusable schemas** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: fm recall is BM25 over raw briefs and lessons. Cluster solved tasks into abstract schemas ("timeout under slow network → look at retry and backoff, then a fake clock test") and offer the matching schema at intake, tracking whether it helped.
  Done when: intake on a task resembling a previous cluster shows the schema, and its later accept or reject updates its score.

- **Wild: Hold an inner council with persistent personas that argue the plan** — FEATURE — value 3 — effort M — risk med — category: deliberation
  Why: wild. Skeptic, Maintainer, Minimalist and User-advocate are small cheap voices whose positions persist across tasks, and they learn from which of their objections proved right. The plan must answer each objection or record why it was dismissed.
  Done when: an L plan carries the objections with their dispositions, and a persona's hit rate appears in `fm council`.

- **Wild: Let Foreman reason in a dream-time counterfactual simulator** — FEATURE — value 3 — effort L — risk high — category: simulation
  Why: wild. Before a risky step, simulate the outcome on a copy of the repo, run the gates, and use the result as the value estimate for choosing among steps; it's the model-based planning that cognitive-architecture work points to.
  Done when: a risky step is previewed in a scratch worktree and the preview verdict agrees with the real result on a replayed set above a stated rate.

- **Wild: Keep a self-model that predicts Foreman's own failure modes** — FEATURE — value 3 — effort M — risk med — category: metacognition
  Why: wild. A small learned profile ("I overestimate S tasks touching hooks, I skip edge cases in parsers") built from friction and rework, shown at plan time as a pre-emptive checklist and tested against held-out tasks.
  Done when: the profile's predicted weak spots overlap actual rework causes on held-out finished tasks at a measured rate.

- **Wild: Make thinking itself a replayable, forkable artifact** — FEATURE — value 3 — effort L — risk med — category: introspection
  Why: wild. Store each decision point as node (options, evidence, choice) so the user can fork the reasoning at any node, change one belief, and see the plan that follows, which turns "why did you do that" into a first-class edit.
  Done when: `fm think fork <node> --belief ...` yields a revised plan alongside the original, with the differing steps highlighted.
