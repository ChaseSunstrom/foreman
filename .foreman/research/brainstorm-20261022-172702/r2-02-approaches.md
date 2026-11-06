# Brainstorm — lens: approaches

- **Retrieve skills and playbooks in the hook, not by description** — FEATURE — value 4 — effort M — risk low — category: triggering
  Why: assumption: the 2,000-char listing budget and terse descriptions are the cap. A local TF-IDF or BM25 index over all 13 skills and 82 playbooks (names, headings, first lines) would run in UserPromptSubmit with no model call. It would inject the top match as one line, "Relevant: playbooks/ui/motion", of at most 200 chars, and stay far below the ~10 KB hook limit.
  Done when: for 20 fixture prompts, the correct skill or playbook is in the injected line at least 17 times, and the hook adds under 30 ms in `bench_hooks.py`.

- **Require a "consulted" field in the task plan** — FEATURE — value 4 — effort S — risk low — category: plan schema
  Why: the pack shows Claude follows the plan-first gate reliably, and the "Next:" line only names fm commands. If `fm task plan` takes `consulted: <skill|playbook|none, reason>` and validates the names, choosing is forced at the one moment Foreman controls.
  Done when: a plan with an unknown name is refused, `none` needs a reason, and the field shows in `fm usage` as a use.

- **Mine a real trigger corpus from past transcripts** — FEATURE — value 4 — effort M — risk low — category: eval
  Why: the earlier ideas propose a trigger eval but not where its prompts come from. The usage logs already show 65 of 82 playbooks unread, so past turns can be labelled "a skill would have fit" by a cheap Haiku pass. They would be redacted and stored as `should_fire` and `should_not_fire` cases.
  Done when: `fm skills eval --corpus real` runs at least 50 cases from the user's history, with secrets redacted, and reports a fire rate per skill.

- **Learn triggers from the user's manual invocations** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: when the user types `/foreman:x` or "use the motion playbook", that prompt-to-skill pair is the best signal for a missed trigger. Today it goes nowhere.
  Done when: a manual invocation appends the prompt to that skill's `should_fire` examples, and `fm skills why` lists these as "missed until you asked".

- **A/B two descriptions live and keep the winner** — FEATURE — value 3 — effort M — risk med — category: experiment
  Why: offline evals only approximate real firing. Foreman already logs usage per session, so a session-hash could pick description A or B per skill, with a 14-day window and a guard against shipping a worse one.
  Done when: `fm skills ab` shows fire counts per variant and promotes a winner only past a set margin, and the 2,000-char cap holds for both variants.

- **Map every workflow step to how it is reached** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: reason 1 (hooks already inject the command) suggests the real question is which steps are reached by a hook, skill, playbook or nothing, not which skills are used. A generated table makes that visible and sends gaps to tasks. It also shows the skills that are redundant by design.
  Done when: `fm skills map` prints each step with its route(s), flags steps with none, and flags skills duplicating a hook.

- **Compile mechanical playbooks into fm checks** — FEATURE — value 3 — effort M — risk med — category: do less
  Why: 65 playbooks are unread. Those that are checklists of commands ("run X, confirm Y") are better as executable `fm check <name>` steps than as prose nobody loads. That is less text to maintain and it respects the token ratchet.
  Done when: at least 5 playbooks become `fm check` entries with tests, and each source playbook is slimmed to a pointer.

- **Preload skills into specialist subagents** — FEATURE — value 3 — effort S — risk low — category: delegation
  Why: assumption: Claude Code agent definitions can name skills to preload, so delegation guarantees use without relying on trigger text. A scout or reviewer subagent would carry the review/security and ui/motion playbooks, which are the ones that do get read.
  Done when: the reviewer and ui builder agent files list their skills, and a transcript of a delegated run shows those bodies in context.

- **Export skills to the other CLIs as instruction files** — FEATURE — value 2 — effort M — risk low — category: reuse
  Why: T-0335 and T-0337 show the Codex, Gemini and opencode adapters lack the Skill tool, so they get nothing. A generated AGENTS.md or GEMINI.md section that carries the same one-liners and routes reuses the work. Plugin behaviour is unchanged.
  Done when: `fm skills export --target gemini` writes a file under 6,400 chars, and `fm code` loads it.

- **Run heavy skills in a forked context** — PERFORMANCE — value 2 — effort S — risk med — category: cost
  Why: assumption: skill frontmatter can fork a skill into its own context. The review and audit skills dump long output into the main session, which may be why Claude avoids loading them. Forking makes loading cheap.
  Done when: the review skill runs forked and the parent context grows by under 1 KB, measured in a fixture run.

- **Hold a skill court for keep, merge or kill** — FEATURE — value 3 — effort M — risk low — category: curation — wild
  Why: assumption: nobody wants to hand-delete skills. T-0034's `fm audit run` pattern would let three read-only reviewers argue for and against each skill using usage and eval evidence. A clerk would write a verdict file, and a person approves the deletions.
  Done when: `fm skills court` writes a verdict per skill with its evidence, and applies nothing without approval.

- **Show unused skills as sleepy mascots in the pane** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: a visible streak or "asleep for 12 days" state is a nudge the user will notice, and something worth showing off. It fits the afterglow and motion work already underway.
  Done when: the web UI skills strip shows one tile per skill with awake and asleep states, and reduced-motion users get a static label.

- **Rehearse an unused skill on a throwaway task** — FEATURE — value 2 — effort M — risk med — category: autonomy — wild
  Why: assumption: a skill never used in 30 days may be broken, not just unloved. An unattended lane would run it on a fixture repo and check the output. Rotting skills would surface in `fm doctor`, not in a real task.
  Done when: `fm doctor --skills` runs each skill's fixture rehearsal, in a temp folder under the guard, and fails on a skill whose script or referenced command no longer works.
