# Brainstorm — lens: reliability

- **Gate subagent spawn on a lint receipt** — FEATURE — value 5 — effort M — risk med — category: enforcement
  Why: 19 card-writer subagents were told to lint and didn't; instruction-only enforcement failed. A SubagentStop (or fm-side post-write) hook runs `fm lib check` itself and refuses completion until a passing receipt exists for each file the agent wrote.
  Done when: a test subagent writes a malformed card, tries to stop, is refused with the lint output, and stops only after the card passes `fm lib check`.

- **Refuse close after a skipped red run** — FEATURE — value 5 — effort M — risk med — category: proof gate
  Why: "builders skip red runs"; the README already refuses a close without red-then-green proof for the main thread, but builder lanes evade it. Extend the claims gate to builder lanes: a recorded failing run of the verify command (real execution, not injected reminders) must precede the first edit to the linked source files.
  Done when: a builder lane edits source with no prior recorded red run, and `fm done` fails naming "no red run recorded"; with a red run it passes.

- **Make FM run the post-step itself, not ask the agent** — FEATURE — value 5 — effort M — risk low — category: enforcement
  Why: the pattern behind all three complaints is "told to, didn't". Introduce a declarative table of mechanical steps (lint, sync, tidy, card inject) that fm executes in hooks (PostToolUse/Stop), with the agent only seeing the results.
  Done when: removing the "run lint" sentence from a card-writer prompt still yields a lint run in the hook log for every write.

- **Add an enforcement ledger with a per-rule compliance rate** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: nobody can currently say which rules agents break. Log each rule as enforced/auto-done/violated/overridden per session and show it in `fm doctor` and the web UI pane, so the rules most often skipped get promoted from advice to a hard gate.
  Done when: `fm doctor` prints a table of rules with counts from the last N sessions, and a seeded violation shows up in it.

- **Check the main thread's step list at Stop** — FEATURE — value 4 — effort M — risk med — category: drive gate
  Why: "the main thread skips steps under load". The brief already holds steps and criteria; the Stop hook should compare the steps in the brief with the evidence on record (commands run, files touched) and block with the exact unmet steps listed.
  Done when: a brief with 4 steps and evidence for 3 blocks Stop with the 4th named; adding evidence lets it stop.

- **Inject the relevant card at edit time, not at session start** — FEATURE — value 4 — effort M — risk low — category: context
  Why: the user asked for "inject the right card at the …"; cards cost zero standing tokens, and `fm lib suggest` exists. Hook PreToolUse on Edit/Write to the path, attach the card's checklist section (via `--section`) once per session per card.
  Done when: first edit to a `.github/workflows/*.yml` file shows the github-actions card section in context, and the second edit does not repeat it.

- **Quarantine subagent output that fails its checks** — FEATURE — value 4 — effort M — risk med — category: fleet
  Why: with 19 parallel writers, one bad result is easy to merge. Land a lane's output in a staging branch and run FM's own gate (lint, tests, `fm doctor`) before merge, with a pass/fail receipt per lane.
  Done when: a lane with a failing lint stays out of the merge branch, and the report lists it with the failing output.

- **Run each enforcement rule against a deliberately lazy agent** — FEATURE — value 3 — effort M — risk low — category: evals
  Why: `plugin/evals/` exists; rules need proof that they actually bite. Add scripted "lazy agent" transcripts (skips lint, skips red run, claims pass without running) and assert each gate trips.
  Done when: CI runs the lazy-agent suite and fails if any gate lets one through.

- **Fail closed when a hook crashes or times out** — FIX — value 4 — effort S — risk med — category: hook safety
  Why: assumption: an enforcement hook that errors silently turns into no enforcement, the same failure as the agent skipping the step. Hooks on gates return deny with a "gate unavailable" reason, and `fm doctor` reports the crash count.
  Done when: a forced exception in the lint gate blocks the close with a clear message instead of passing.

- **Run a reviewer's checklist as a "second pair of eyes" lane, wild** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: wild; an unattended cheap-model auditor re-derives each claim ("tests pass", "linted") from the transcript and the repo and files a contradiction as a blocking finding. This builds on the deferred T-0034 `fm audit run`.
  Done when: a seeded false "tests pass" claim gets a blocking finding from the auditor lane.

- **Show a live enforcement strip in the pane, wild** — FEATURE — value 3 — effort M — risk low — category: UI
  Why: wild; the foreman-ui pane already shows Now, Subagents and Shells. Add a reserved-height row of gate lights (lint ✓, red-run ✗, steps 3/4) so the user sees at once what FM is holding back; the pane's stable-layout work means a fixed slot fits.
  Done when: the pane shows the gate lights, and a failed red-run turns its light red without shifting the layout.

- **Replay a session to name where it went lazy, wild** — FEATURE — value 3 — effort L — risk low — category: diagnostics
  Why: wild; given a transcript, replay it against current gates and print "this gate would have stopped it at turn N". It tells the user which new rule would have caught past failures, such as the 19 unlinted cards, before they ship the rule.
  Done when: `fm replay <session>` on the card-writer run lists the 19 missing lint steps as would-have-blocked.

- **Make agent-written prompts carry enforced contracts** — CLEAN — value 3 — effort S — risk low — category: fleet
  Why: assumption: orchestrator prompts say "lint your work" in free text. Replace that with a contract block in the lane spec (`requires: lint, red-run`) that the harness enforces and that is not editable by the agent.
  Done when: a lane spec with `requires: lint` fails to dispatch if the lint gate isn't wired, and the prompt text no longer needs the instruction.
