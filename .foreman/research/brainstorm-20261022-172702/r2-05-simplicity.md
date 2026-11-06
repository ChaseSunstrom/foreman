# Brainstorm — lens: simplicity

- **Generate hooks, skills and docs from one moment registry** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: the "Next:" hook text, skill descriptions and the docs all describe the same steps separately, so they drift. The pack shows hooks and skills duplicating each other (cause 1).
  Done when: one file maps moment → fm command → skill → playbook, and a test fails if a hook's Next line, a skill description or the docs table disagrees with it.

- **Make skill bodies thin pointers to `fm` output** — CLEAN — value 4 — effort M — risk low — category: skills
  Why: assumption: skill bodies repeat guidance that `fm` commands can print themselves. Guidance that lives in `fm help <moment>` is testable and carries across the plugin and `fm code`.
  Done when: every SKILL.md body is ≤15 lines and ends in one `fm` command, and a test confirms each pointed-to command exists.

- **Keep a single `skills.toml` manifest** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: the 1,957 of 2,000 chars budget (T-1508) is managed by hand. The manifest would hold each skill's description, user-only flag, a trigger example prompt and its eval case, and generate the frontmatter.
  Done when: editing the manifest regenerates every SKILL.md frontmatter, and the build fails over budget with the per-skill char cost printed.

- **Make playbooks section-addressable** — FEATURE — value 3 — effort M — risk low — category: playbooks
  Why: 65 of 82 playbooks went unread and the read ones are long. `fm playbooks show ui/motion#easing` would let a hook inject 10 lines instead of a file or nothing, which keeps the output under the ~10 KB preview limit.
  Done when: the `#section` form prints only that section, and a test shows a hook injecting a section under 1 KB.

- **Silence the "Next:" line once the model does it right** — PERFORMANCE — value 3 — effort S — risk med — category: hooks
  Why: the hook injects the exact command every turn, which both bypasses skills and costs context. Dropping it for a moment after Claude has run the command correctly twice in a session removes the noise.
  Done when: a replayed session shows the Next line absent after two correct runs and returning after a missed step, with hook bench numbers not worse.

- **Show Foreman's context rent in `fm doctor` and the pane** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: assumption: nobody knows the tokens per turn that skills, hooks and the rules file inject. The rules file is capped at 80 lines, but the total isn't visible.
  Done when: `fm doctor` prints injected tokens per turn split by source, and warns above a configurable ceiling.

- **List only the skills a project's `fm map` makes relevant** — FEATURE — value 3 — effort M — risk med — category: skills
  Why: assumption: design-extract and the UI skills are dead weight in a backend repo and spend listing budget. Map facts (layout, cards) could pick the enabled set.
  Done when: a repo without web files lists fewer skills than one with them, and `fm doctor` shows which were left out and why.

- **Merge the redundant status-type skills into one "where are we" skill** — CLEAN — value 3 — effort S — risk low — category: skills
  Why: status, next, resume and doctor all answer "where are we", and none were used in 30 days. One skill with one description frees budget and removes four chances to pick wrongly.
  Done when: one skill replaces the four, its trigger eval passes on prompts for each old job, and the description total drops.

- **Wild: Run a weekly skill ablation** — FEATURE — value 3 — effort L — risk med — category: evals
  Why: wild. Disable one skill at a time on the bench corpus and compare pass rate, cost and time. A skill whose removal changes nothing is retired by data rather than by opinion.
  Done when: `fm skills ablate` prints a per-skill delta table and flags skills with zero effect across N runs.

- **Wild: Make a skill's description its entire content** — FEATURE — value 2 — effort S — risk low — category: skills
  Why: wild. The model sees only name and description until it invokes a skill. Test whether tiny skills, where the description carries the instruction and no body exists, get loaded and followed as well.
  Done when: a bench comparison of body-less and full skills on 10 trigger prompts shows firing rate and task result side by side.

- **Wild: Replace the skill list with one self-updating line** — FEATURE — value 3 — effort M — risk high — category: hooks
  Why: wild. At session start the hook injects one line, "Today's job: X; use `fm help X`", derived from the open queue, instead of 13 descriptions. The listing budget then stops being a limit.
  Done when: a session with skills disabled still reaches each moment's guidance via that line, verified on the e2e roundtrip.

- **Wild: Print a one-screen "why unused" answer from `fm skills`** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: wild. The user had to ask why skills go unused. A five-line generated diagnosis per skill (hook shadows it, trigger words absent from runs, cut for budget) answers that without a research task.
  Done when: `fm skills` prints one cause line per skill from usage data, and the web UI shows the same text.
