# Brainstorm — lens: bold bets

- **Make the turn-start hook choose the skill, not Claude** — FEATURE — value 5 — effort M — risk med — category: routing
  Why: the "Next: …" line makes Claude run fm directly, so skills never load (13 of 14 unused). Round 1 covered renaming the line; this goes further: a deterministic router in the hook matches task state (editing, closing, reviewing, failing gate) to one skill and injects its first 10 lines inline, with a pointer to the rest.
  Done when: a replayed transcript fixture of an "about to close" turn shows the close-out skill's checklist in hook output under 10 KB, and `fm usage` counts it as a skill use.

- **Count inline-injected skill content as a use, with provenance** — FIX — value 4 — effort S — risk low — category: observability
  Why: usage shows 2 skill uses in 30 days, but hook-injected guidance does the same job invisibly. Assumption: the usage counter reads only Skill-tool calls, so it undercounts real influence.
  Done when: `fm usage` reports separate "loaded by Claude" and "injected by hook" counts per skill and playbook, and the test fixture shows both.

- **Collapse the 13 skills into a verb-shaped set of 5 with bundled scripts** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: status, resume, next and doctor are one "orient" job; improve, reflect and brainstorm are one "learn" job. Fewer entries leave listing budget (1,957 of 2,000 used) for longer "Use whenever you are about to…" descriptions.
  Done when: the listing stays under 2,000 chars, every old skill name still resolves to an alias, and the trigger eval passes for all 5.

- **Add a playbook-as-skill compiler (`fm skills gen`)** — FEATURE — value 4 — effort M — risk med — category: playbooks
  Why: 65 of 82 playbooks are never read and hide behind one skill. A generator emits a thin SKILL.md per family (review, ui, security, clean), with "when" text derived from the playbook's own front matter, marked user-only unless it fits the budget.
  Done when: running it yields skill folders that pass `fm skill lint`, and the listing budget check still passes.

- **Gate close-out on "which skill applied?"** — FEATURE — value 3 — effort S — risk med — category: discipline
  Why: Foreman already makes Claude prove work with commands; a skill step is unchecked. Assumption: a light check, which asks whether a covering skill existed and was read, would be tolerated if it is advisory.
  Done when: `fm task close` prints a one-line "skills that matched this task: X, read: yes/no" and never blocks.

- **Skill budget is dynamic per project** — PERFORMANCE — value 3 — effort M — risk med — category: listing budget
  Why: the 2,000-char cap (T-1508) is a fixed, global cost. Assumption: most projects need only 6 to 8 of the skills. `fm map` can select which descriptions to enable (design skills only where a web or 3D surface exists), so each project gets longer descriptions for fewer skills.
  Done when: a web project and a CLI-only project list different skill sets, each under budget, and `fm doctor` shows which were dropped and why.

- **Replay old transcripts to score skill triggering** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: the repo already holds real sessions (the demo, usage logs). Replaying past prompts and task states against the descriptions gives a real-world hit rate without paying for new runs.
  Done when: `fm skills eval --replay` prints per-skill precision/recall from the last 30 days and fails under a set threshold.

- **Design skill pack with bundled scene and motion scripts** — FEATURE — value 4 — effort L — risk low — category: design skills
  Why: the user repeatedly asked for 3D, motion and looks; those capabilities exist as `fm scene compile`, `fm design lint`, `fm page`, `fm motion` but are reached by commands, not by "I'm about to build a hero section". One skill per job, each wrapping those commands.
  Done when: a prompt "add a hero with a 3D scene" in an eval loads the skill and ends with a passing `fm scene compile` and `fm design lint`.

- **Wild: Skills that rewrite themselves from misses** — FEATURE — value 4 — effort L — risk high — category: self-improvement
  Why: wild. Each skill-miss (the fm command ran, the skill wasn't loaded) becomes a training example; overnight, an agent proposes a description edit, scores it with the replay eval, and opens a task only if the score rises. Assumption: the miss detector from round 1 exists.
  Done when: a seeded miss in a fixture produces a proposed description diff with before/after scores, and nothing lands without a task.

- **Wild: Skill "trial" status with auto-retirement** — CLEAN — value 3 — effort S — risk low — category: portfolio
  Why: wild. Every new skill enters a 30-day trial, then is kept, folded or deleted by its usage and measured lift; the pack ends dense by construction.
  Done when: `fm skills` lists trial/kept/retired with days remaining, and a zero-use skill past its window is flagged in `fm doctor`.

- **Wild: Skills that speak in the foreman-ui pane as a sidekick** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. When a skill would have helped, the pane shows a small card ("Review playbook fits this diff") that the person can click to inject it for the next turn. It makes skills visible and gives a human steering handle.
  Done when: the pane shows a suggested-skill card on a fixture diff, and a click records an injection.

- **Wild: Cross-project skill commons, local-only** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: wild. Skills a user's other repos proved (high lift, repeated use) get offered when a new project is initialized, through `fm home export` bundles, guard-checked, with no network.
  Done when: importing a bundle into an empty home lists its skills as "proposed", and none run until the user accepts them.

- **Write a "why skills don't fire" page in the docs and doctor** — docs — FEATURE — value 2 — effort S — risk low — category: docs
  Why: this question took a task (T-1692) to answer. Persist the four causes with live numbers so the next person doesn't repeat the investigation.
  Done when: `fm doctor --skills` prints the four causes with the current counts, and the docs page links to it.
