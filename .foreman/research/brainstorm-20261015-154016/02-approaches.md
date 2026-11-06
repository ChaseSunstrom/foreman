# Brainstorm — lens: approaches

- **Gate close on a machine-checked receipt, not an agent claim** — FEATURE — value 5 — effort M — risk med — category: enforcement
  Why: builders skip red runs and card-writers "were told to lint and didn't"; the claims gate already counts real test runs, so extending it is the cheapest path. assumption: close/done verbs are the single choke point for all lanes.
  Done when: `fm close T-x` fails with a named missing receipt (lint, red-then-green run) when the hook-recorded tool log lacks it, and passes once the receipt exists.

- **Run required checks in the hook, not the prompt** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: telling agents to lint is the failing approach. A PostToolUse hook on Write/Edit runs the per-language linter (from `fm map` gates / cards) and injects the failures back as the next-turn context. assumption: a hook can add output within the existing hook latency budget (bench_hooks.py exists).
  Done when: editing a file with a seeded lint error surfaces that error in the agent's next turn with no agent action, and bench_hooks stays within budget.

- **Make subagent output a validated artifact** — FEATURE — value 5 — effort M — risk low — category: subagents
  Why: 19 card-writers skipped lint. Have `fm lib check` run on the card file in a SubagentStop hook, and deny the stop (with the errors) until it passes. Cards already have `fm lib check`.
  Done when: a card-writer that writes an invalid card cannot finish; the stop is refused with the checker's output, and passes after a fix.

- **Add an enforcement manifest in the repo (`enforce.toml`)** — FEATURE — value 4 — effort M — risk low — category: config
  Why: rules are scattered across prompts and playbooks. A single declarative file lists rule, trigger (on-write, on-close, on-stop, on-subagent-stop), check command, and severity (inject/warn/block). Every hook reads it. assumption: current hooks hard-code their rules.
  Done when: adding a rule to the file changes hook behavior with no code edit, and `fm doctor` lists active rules.

- **Do the step in FM, not the agent (replace instructions with verbs)** — CLEAN — value 4 — effort M — risk low — category: simplification
  Why: the main thread "skips steps under load". Wherever a prompt says "then do X", make `fm` do X as a side effect of the previous verb (e.g. `fm close` runs lint, sync, and the changelog check itself).
  Done when: an audit lists each step in the playbooks, and every step that can be automated is attached to a verb with a test, shrinking the playbook prose.

- **Inject the right card at the moment of the edit** — FEATURE — value 4 — effort M — risk low — category: context
  Why: the user asked for "inject the right card at the…" and cards cost nothing standing. A PreToolUse on first edit of a file type injects the matching `fm lib suggest` card once per session.
  Done when: the first edit of a `.yml` workflow shows the github-actions card section exactly once, and the pane shows it under skill use.

- **Add an enforcement ledger and a compliance score** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: nobody can say how inconsistent agents are. Log each rule fired, passed, blocked or overridden per task and lane, and show it in `fm doctor` and the pane. This tells the user which prompts to delete. assumption: tool-call logs already exist per session.
  Done when: `fm enforce report` prints per-rule fire/block counts for the last N tasks.

- **Fail loud on skipped red runs with a mutation-style check** — SECURITY — value 3 — effort M — risk med — category: verification
  Why: builders skip red runs. Require the proof command to fail on the pre-change tree (stash or worktree) before the fix, recorded in the receipt.
  Done when: a task whose proof passes before the edit is refused as "not a reproducing test".

- **Escalate by lane: fresh subagent redoes a failed check** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: when the hook blocks a builder three times, hand it to a fresh lane with the failure text instead of looping. assumption: lane fork/restart already exists (T-0792).
  Done when: three consecutive blocks on one rule spawn a new lane carrying the failure text, and the original is retired.

- **Wild: Make the non-compliance the training data** — FEATURE — value 3 — effort L — risk med — category: evals — wild
  Why: T-0035 (`fm eval capture`) is deferred. Every blocked skip becomes a redacted eval case, so prompt changes are measured against real lapses.
  Done when: `fm eval run` replays captured skips against a candidate prompt and reports the pass rate.

- **Wild: A "load meter" that tightens enforcement as the thread gets busy** — FEATURE — value 3 — effort M — risk med — category: adaptive — wild
  Why: the main thread skips steps *under load*. Context size and parallel-lane count raise the check strictness (e.g. block on close instead of warn) when drift is likelier.
  Done when: with more than N active lanes, a warn-level rule behaves as block, shown in the pane.

- **Wild: Pane shows a live "rules you'd have broken" strip** — FEATURE — value 2 — effort S — risk low — category: UI — wild
  Why: the user cares about the pane and about visible skill use. A quiet strip shows rules auto-satisfied this session (lint ran, card injected), so enforcement feels like help, not friction.
  Done when: the pane displays a count of auto-run checks that updates live without moving the layout.

- **Wild: Trust-nothing dry-run mode that replays a session against the rules** — FEATURE — value 2 — effort M — risk low — category: simulation — wild
  Why: before turning on a new rule, replay past transcripts to see how often it would have fired, avoiding false blocks like the recent guard fixes (T-0940).
  Done when: `fm enforce try RULE` reports how many past tool calls would have been blocked.
