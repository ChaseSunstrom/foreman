# Brainstorm — lens: approaches

- **Run lenses and reviewers as native subagents** — FEATURE — value 4 — effort M — risk med — category: plugin runtime
  Why: Each brainstorm child is a separate `claude -p` process that reloads the pack and pays startup cost. Assumption: plugin-shipped subagent definitions can set their own model and tool allowlist.
  Done when: A six-lens round runs through subagents from inside the plugin, and its receipt shows per-child startup time below the `claude -p` baseline.

- **Hand budget ceilings to the host's own limits** — FEATURE — value 4 — effort S — risk low — category: cost caps
  Why: Foreman's own spend counter can drift from what the host bills. Assumption: headless Claude Code accepts turn and spend limits as flags.
  Done when: A run that hits the host's limit stops with the host's exit reason, and `fm` records that reason instead of an estimate.

- **Plan under the host's read-only mode, then switch to edit** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: Plan-before-edit is currently a prose rule. Assumption: the host has a read-only permission mode the planner can run under.
  Done when: A planning child that tries to write is refused by the host's permission system, not by the rules text.

- **Loop a failing gate back to the model in a capped Stop hook** — FEATURE — value 4 — effort M — risk high — category: proof loop
  Why: Today a failed proof waits for a human or the next queue pass. Assumption: a Stop hook can block the stop and re-prompt with the failing output.
  Done when: A seeded failing test re-enters the model until it passes, and when the retry cap trips the run closes with a receipt saying so.

- **Read one feature-flag file that both surfaces honour** — FEATURE — value 3 — effort S — risk low — category: safe rollout
  Why: Recent fixes shipped without a way to back one out short of reinstalling. Assumption: plugin and CLI can read the same project file.
  Done when: Setting one flag off disables a named feature in both the plugin and the CLI with no reinstall, and the glance line shows it as off.

- **Rehearse queued branches on a throwaway merge before running them** — FEATURE — value 3 — effort S — risk low — category: conflict prediction
  Why: Queued tasks can touch the same files and collide late. Assumption: a scratch merge is cheap for the repo sizes Foreman targets.
  Done when: Two queued tasks with overlapping hunks are flagged before either runs, and a clean pair passes the check without a warning.

- **Schedule the queue by make-style staleness** — CLEAN — value 3 — effort M — risk low — category: queue ordering
  Why: The queue reruns tasks whose inputs have not changed. Assumption: each task's input set can be hashed the way make hashes its prerequisites.
  Done when: Re-running an unchanged queue does no model calls, and touching one input re-runs only the tasks that read it.

- **Draft plans cheap, let a strong critic review only the risky steps** — PERFORMANCE — value 3 — effort M — risk med — category: plan cost
  Why: Every plan currently goes to the strongest model. Assumption: a risk tag on each step can be set by the cheap draft.
  Done when: On a bench set, plan cost drops and the critic still catches every seeded risky step.

- **Guard pushes with a server-side pre-receive check** — SECURITY — value 3 — effort M — risk med — category: push guard
  Why: The guard runs only on the local machine, so a push from another machine skips it. Assumption: the remote can run a small check on incoming refs.
  Done when: A push that contains a refused command pattern is rejected by the remote, and a clean push goes through.

- **Wild: evolve the hook scripts with a genetic search scored on the bench** — FEATURE — value 2 — effort L — risk high — category: hook tuning
  Why: Wild: hook latency has been hand-tuned against one noisy p95. Assumption: the bench is stable enough to score candidates.
  Done when: An evolved hook beats the current one on median and p95 across three bench runs, and the winning variant's diff is reviewed before it ships.

- **Wild: barbell the week into cheap bulk tasks and one costly bet** — FEATURE — value 3 — effort M — risk med — category: budget strategy
  Why: Wild: the reset window is spent on whatever is queued first. Assumption: the queue can be sorted by cost and expected value.
  Done when: A week's budget runs many low-cost tasks and exactly one high-cost task, and the receipt shows the split in dollars.

- **Wild: compile tasks like source, with gates as type checks** — RESEARCH — value 2 — effort L — risk high — category: task model
  Why: Wild: tasks already have typed fields (kind, proof, file set) that nothing checks before a run. Assumption: a task schema can be validated before the queue starts.
  Done when: A task missing its proof or file set is rejected at queue time with the missing field named, and a valid task is queued without a model call.
