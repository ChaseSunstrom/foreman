# Brainstorm — lens: capability map

Capability map for "enforce mechanically, don't trust agents". Comparable products: pre-commit, Husky/lefthook, Danger, CodeRabbit-style gates, Claude Code hooks, Cursor rules, Aider lint/test auto-loops, GitHub branch protection and required checks, OPA/Conftest policy engines.

- **Enforce a lint gate on every subagent's result** — FEATURE — value 5 — effort M — risk low — category: gates
  Why: 19 card-writer subagents were told to lint and didn't. Assumption: the lint command is known from `fm map` gates or `fm lib check`.
  Done when: a subagent that returns files without a passing lint record is rejected by a SubagentStop hook with the lint output as the reason, and a test covers it.

- **Refuse to close on a red run** — FEATURE — value 5 — effort S — risk low — category: gates
  Why: builders skip red runs. The close gate already demands red-then-green proof for tasks. Assumption: this isn't enforced for builder lanes.
  Done when: closing a lane whose last recorded test run exited nonzero fails with that run's id, and a test shows it.

- **Declare a per-task-type obligations list that FM checks** — FEATURE — value 5 — effort M — risk med — category: policy
  Why: the main thread skips steps under load, so obligations should live in a data file instead of prompts. Examples: card-writer = lint + `fm lib check`; builder = tests + diff review.
  Done when: `fm obligations show <type>` lists the checks, and a close with any unmet one is refused with a named list.

- **Run checks on write via PostToolUse** — FEATURE — value 4 — effort M — risk med — category: hooks
  Why: the user asked for "hooks that run checks on write". It overlaps T-0214 (edit-time test sentinel). The hook runs the matching linter or formatter on edited files and feeds back failures immediately.
  Done when: editing a card with a broken frontmatter prints the lint error in the next tool result, and the bench stays under the hook time budget.

- **Inject the right card at the moment of need** — FEATURE — value 4 — effort M — risk low — category: context
  Why: the user asked for this, and cards cost zero standing tokens. The hook maps a file path or command to `fm lib suggest` and injects the card once per session.
  Done when: the first edit of a `.github/workflows/*.yml` file injects the github-actions card, and a second edit doesn't.

- **Add an enforcement ledger and a compliance score** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: nobody can tell today how often agents skip steps. Record each obligation as asked, met, forced or bypassed, then show it in `fm doctor` and the web pane.
  Done when: `fm doctor` prints the per-obligation skip rate for the last N tasks, and the pane shows a compliance row.

- **Block the main thread's step-skipping with a stage rail** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: the main thread skips steps under load. The stage rail exists in the pane, so make its stage transitions machine-checked: no `verify` stage without a recorded command run.
  Done when: attempting to mark a stage done without its artefact returns a deny, and the artefacts are listed in the reason.

- **Fan out lint centrally after a subagent batch** — FEATURE — value 4 — effort S — risk low — category: gates
  Why: instead of trusting 19 agents, FM runs one lint pass over the union of changed files after the batch finishes. Assumption: the batch is tracked in the lanes registry.
  Done when: finishing a batch of N writers produces a single lint report, and failures are routed back to the owning lane.

- **Add an auto-retry loop like Aider's lint/test loop** — FEATURE — value 3 — effort M — risk med — category: loops
  Why: gate failures should be fed back to the agent automatically, capped at K tries and then escalated, instead of ending in a silent skip.
  Done when: a deliberately failing lint triggers up to 3 fix attempts and then a blocked task with the log.

- **Wild: Make a "trust ledger" that tightens or loosens enforcement per agent and model** — FEATURE — value 3 — effort L — risk med — category: adaptive
  Why: wild. The ledger above gives each model and task type a skip rate. Cheap models that comply stay on light checks, and repeat skippers get stricter gates. This ties into T-0217 (lesson confidence).
  Done when: a model with 3 recorded skips gets the stricter profile on its next task, visible in `fm obligations show`.

- **Wild: Add a canary check that catches faked compliance** — SECURITY — value 3 — effort M — risk low — category: integrity
  Why: wild. An agent can claim "linted" without running it. FM re-runs a random sample of claimed checks itself and flags mismatches, building on the claims gate that counts only real runs.
  Done when: a seeded false "lint passed" claim is detected in a test and recorded as a violation.

- **Wild: Add a dry-run replay of past sessions against new rules** — FEATURE — value 3 — effort L — risk low — category: policy
  Why: wild. Before turning on a new obligation, replay stored transcripts and show how many past tasks it would have blocked, so rules don't ship blind. Related to T-0826 (round ledger).
  Done when: `fm obligations replay <rule>` prints counts of would-block tasks over the last 30 days.

- **Show enforcement in the web UI** — FEATURE — value 3 — effort M — risk low — category: UI
  Why: the pane work is ongoing, and a "Gates" card showing pending, met and forced obligations makes enforcement visible. It must reserve its height, per the user's stable-layout steer.
  Done when: the pane shows per-task obligations with a state each, and the card doesn't shift the layout when it appears.
