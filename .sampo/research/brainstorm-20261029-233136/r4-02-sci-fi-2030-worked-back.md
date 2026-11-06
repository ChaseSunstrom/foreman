# Brainstorm — lens: sci-fi 2030 worked back

- **Trigger a generation from project events, not just a dry queue** — FEATURE — value 4 — effort M — risk med — category: auto-start
  Why: the pack covers only "queue runs dry" and "gap map shows big gaps" as triggers. By 2030 a harness reacts to what happens to the project. Candidate events are a CI run going red, a dependency major bump, the user reverting a commit, and a surface falling out of date. Assumption: `fm loop` or `fm scout` can read CI status and git events cheaply.
  Done when: on a fixture repo, a simulated red CI run and a revert each produce exactly one proposed, scoped Genesis generation (a proposal only, never a silent run), and a quiet repo produces none.

- **Screen rewrites on a digital twin replayed from recorded traces** — PERFORMANCE — value 4 — effort L — risk med — category: exam cost
  Why: assumption: gate and tool I/O can be recorded during exam runs. Replaying recordings against a candidate rewrite shows which scenarios could plausibly flip, so only those get a live run. This differs from cheap screening by the model, because it uses replayed execution.
  Done when: on 20 recorded scenarios, the twin screen predicts the live pass/fail flip with at least 90% agreement while running at least 5× faster. Any disagreement is logged.

- **Layer the tower by pace: charter, spec and tasks** — FEATURE — value 4 — effort M — risk low — category: structure
  Why: the pack mixes docs that change every put with the user's MUSTs. Fast layers (tasks, Missions) change freely. The middle layer (capability spec) changes only at generation close with an exam win. The slow layer (charter) changes only with the user's explicit yes. Assumption: a path-prefix rule and a hook can enforce this.
  Done when: a rewrite that edits a slow-layer file without a ratification record is rejected by `fm genesis put`, and fast-layer edits pass untouched.

- **Allocate quota across projects by marginal exam value** — FEATURE — value 4 — effort M — risk med — category: portfolio
  Why: Genesis is built per project, but the user has many projects sharing one subscription. Rank projects by (expected scenarios closed per dollar, taken from past generations) and hand out the next unit of budget to the top one. Assumption: `exam.jsonl` and cost ledgers exist per project.
  Done when: with three fixture projects and a fixed budget, `fm genesis plan` splits the budget by that ranking. A project with a flat curve gets the floor allocation and the plan says why.

- **Add a screenshot-judged scenario kind for web UI projects** — FEATURE — value 3 — effort L — risk med — category: exam
  Why: surfaces are "web UI" and there are many UI and motion asks (favicon still shows the old logo, tab icon, motion polish), but the 11 scenario kinds read as code and gate oriented. Planted visual gaps would be a missing favicon, no empty state or broken contrast. A cold tool-less judge would score the screenshots. Assumption: a headless browser is available.
  Done when: a planted missing-favicon and a planted contrast failure each fail the empty arm and pass the oracle arm, scored from screenshots alone.

- **Render the tower's output as a stacked PR series with exam receipts** — FEATURE — value 3 — effort M — risk med — category: delivery
  Why: today the work lands via `fm ship`. A reviewer on a phone would rather read one PR per closed scenario, each with its before and after result and cost. Opening PRs is outward-facing, so it needs the user's yes.
  Done when: `fm genesis pr --dry-run` prints N PR bodies, each citing its scenario id, lineage line and measured cost, and creates nothing remote without a confirmation flag.

- **Make generations preemptible when the user starts typing** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: assumption: a background tower competes with the user's live edits. A fast file-activity detector can checkpoint the in-flight step and release the worktree, then resume on idle. This is stricter than "never land over live edits", because it also frees the machine and the quota lane.
  Done when: touching a tracked file mid-generation pauses within 5 seconds with a checkpoint line in the tower journal. After 2 minutes of idle it resumes at the same step with no repeated spend.

- **Hold a winter generation where the only legal move is removal** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the pack proposes "require a deletion for every addition" per change, but nothing schedules a whole generation for pruning. The Seed bans additions. Missions propose deletions of rules, templates, lenses and docs. The exam must stay green and the injected-context size must shrink.
  Done when: a winter generation on a fixture tower shrinks injected bytes by at least 10% with the exam unchanged, and any added line fails the generation.

- **Shrink property failures into new exam scenarios** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: the pack proposes compiling each MUST into a check. A 2030 harness also fuzzes it, so a falsified MUST yields a minimal counterexample. That counterexample is minted as a permanent scenario in the held-out pool, so the exam grows from the failures it finds. Assumption: Hypothesis-style tooling is available for the project's language.
  Done when: a planted MUST violation produces a shrunk counterexample under 20 lines, filed as a scenario that fails the empty arm and passes the oracle arm.

- **Ask typed questions with a deadline and a default** — FEATURE — value 3 — effort S — risk low — category: human interface
  Why: Genesis can stall on questions the user never sees, and the pack's batching ideas stop at "ask once". A typed question carries options, a default and a deadline. At the deadline the default is taken, logged as an assumption and marked revertible. Assumption: answers can come from the terminal now, or from other surfaces later.
  Done when: an unanswered question takes its default at the deadline, the tower shows "assumed: X (you can overrule)", and a later overrule reverts the dependent step.

- **Wild: Ship the tower as a standalone `agent.py` so the project carries its own discipline** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: wild. Gen-N's spec compiles into one dependency-free script that any contributor's Claude Code, Codex or Gemini loads as its project rules and checks. The project outlives Foreman being installed (cf. the open Gemini/Codex/opencode tasks).
  Done when: on a machine without Foreman, running the script on a fixture repo enforces the same NEVERs and answers 3 of the project's gate questions identically to `fm`.

- **Wild: Export lineage as a local preference corpus for training a small project model** — FEATURE — value 3 — effort M — risk low — category: local learning
  Why: wild. Every selection already compares a winning and a losing rewrite on the same scenarios, which are labeled preference pairs. Written to a local JSONL (redacted, never uploaded), they could later tune a tiny router or reviewer on the owner's hardware.
  Done when: `fm genesis corpus` writes at least one (prompt, chosen, rejected, scenario, cost) row per decided selection, with secrets scrubbed, and a schema validator passes it.

- **Wild: Run a tower on a deliberately handicapped model to expose what is scaffolding versus real capability** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. The same tower runs on Haiku and on the largest model. Rules that raise the small model's score but do nothing for the big one are marked training wheels, and each gets a scheduled sunset review. This also shows which rules a future model will no longer need.
  Done when: for a fixture tower, `fm genesis wheels` lists each rule with its delta on the small and large model, and the training-wheel rules are tagged.

Next question: What does Genesis owe the user when its own tower is correct but the user's goal for the project changes — how does it detect a pivot, as opposed to drift?
Next question: Which parts of the tower would still make sense if Foreman were uninstalled tomorrow, and are those the parts the user values most?
