# Brainstorm — lens: user value

- **Replay real transcripts against the descriptions** — FEATURE — value 5 — effort M — risk low — category: skill evals
  Why: the usage data shows 11 of 13 skills never fired, and a hand-written trigger eval only tests the cases we imagine. Past sessions hold the real moments, such as long autonomous runs with no "status" in them. Assumption: transcripts are readable locally and can be redacted.
  Done when: `fm skills replay --last 30d` prints, per skill, how many past turns would have matched its old and new description, and the report flags turns where a skill clearly applied but none matched.

- **Switch skills on per project from the repo map** — FEATURE — value 4 — effort M — risk med — category: listing budget
  Why: the 1,957 of 2,000 character cap is spent on all 13 skills in every repo, including `design-extract` in a CLI-only repo. The `fm map` cards (python, tailwind, cc-skills) already say what a project is. Assumption: the listing can be changed per project, for example by a `.claude/settings` allow-list or a generated overlay.
  Done when: in a Python-only fixture repo the listing carries only skills relevant to it, the freed characters go to longer task-term descriptions on the rest, and `fm doctor` shows the active set and why.

- **Preload skills into subagents and builder lanes** — FEATURE — value 4 — effort S — risk low — category: agents
  Why: hooks inject the "Next:" line in the main session, but lane builders and scouts start cold. Claude Code subagent frontmatter can list `skills:` to preload. Assumption: Foreman's agent definitions don't already do this.
  Done when: the scout and reviewer agent files declare `skills:` and a lane transcript shows the skill body in context at turn 1 with no Skill tool call.

- **Lint competing descriptions** — CLEAN — value 3 — effort S — risk low — category: skill quality
  Why: `status`, `next`, `resume` and `doctor` all trigger on similar "where are we" words, so the model may pick wrongly or skip all of them. Assumption: the overlap is real, which is unmeasured.
  Done when: `fm skills lint` reports pairs of descriptions sharing more than a threshold of trigger terms, and the shipped set passes with no pair above it.

- **Add a one-tap skill rating** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: nothing tells Foreman whether a skill that fired was useful, so rebalancing from usage only counts calls. Assumption: a user-only `/foreman:rate` skill costs no listing budget.
  Done when: `/foreman:rate up|down [note]` appends to the last-fired skill's record, and `fm usage` shows hit count and rating side by side.

- **Ship the design skills as a standalone plugin** — FEATURE — value 4 — effort M — risk low — category: distribution
  Why: the user keeps asking for 3D, motion and looks skills, and the readings concentrate in ui/scene-3d, ui/motion and review. People who want only those must install the whole discipline layer. Assumption: the playbooks can be split without breaking the token ratchet.
  Done when: a `foreman-design` plugin installs alone in a clean Claude Code profile, its skills list and load, and the main plugin still passes its tests without it.

- **Split playbooks into a card and a body** — PERFORMANCE — value 3 — effort M — risk low — category: playbooks
  Why: 65 of 82 playbooks are never read, and the ones that are cost full tokens each time. A 10-line card could be listed or hooked cheaply, with the body fetched on demand. Assumption: the ratchet can count card and body separately.
  Done when: every playbook has a generated card of 10 lines or fewer, hook injections use cards, and `fm playbooks show` still returns the full body.

- **Export skills for other CLIs** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: open work T-0335, T-0336 and T-0337 are all about Codex, Gemini and opencode, and none of them gets Foreman's skills today. Assumption: those CLIs read AGENTS.md or similar.
  Done when: `fm skills export --agents-md` writes a guarded, size-capped file from the skill descriptions and the top playbook cards, and a fixture check confirms it is under the cap.

- **Add `/foreman:why` for the last block or injection** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: recent commits (T-1606) added guard trust notes, so users clearly meet blocks they don't understand. A user-only skill costs no listing budget. Assumption: the guard decision is logged with its rule.
  Done when: after a blocked command, `/foreman:why` prints the rule, the reason and the safe alternative from the log in under 10 lines.

- **Draft a personal-preferences skill from your steers and drops (wild)** — FEATURE — value 4 — effort M — risk med — category: personalization
  Why: the pack shows consistent steers, such as keeping the poster below the h1 and facts only in shipped text, and consistent drops of CHANGELOG nits. Those are the user's style, restated every run. Assumption: steers and drops are stored with enough text to cluster.
  Done when: after 5 or more similar steers, Foreman proposes a `my-preferences` skill listing them with evidence, and nothing is written until the user accepts.

- **Recall solutions across your other projects (wild)** — FEATURE — value 4 — effort L — risk med — category: memory
  Why: assumption: lessons are per project, so a fix found in one repo is rediscovered in the next. A local-only cross-project recall skill, firing when a failure signature matches a closed task elsewhere, would repay the user directly.
  Done when: a fixture failure already solved in repo A makes a session in repo B surface that task's fix, with nothing leaving the machine.

- **Reorder the slash menu by what you probably need now (wild)** — FEATURE — value 3 — effort M — risk med — category: discovery
  Why: user-only skills like `capture` and `design-extract` are invisible until typed. The foreman-ui mod already reads session state (stage rail, open gates). Assumption: the mod can influence slash-menu order.
  Done when: with a failing gate, typing `/` shows the repair-related skill first, and a screenshot test confirms the order changes with state.
