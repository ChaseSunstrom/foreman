# Brainstorm — lens: user value

- **Make hook "Next:" lines name the skill, not just the fm command** — FIX — value 5 — effort S — risk low — category: skill triggering
  Why: usage shows hooks inject "Next: fm …" so Claude never loads the skill describing that step; 11 of 13 skills never used in 30 days.
  Done when: a recorded session where a hook injects "Next: …" shows the matching `foreman:<skill>` invoked, and `fm usage` shows its count above 0.

- **Rewrite skill descriptions in task terms ("Use whenever you are about to …")** — FIX — value 5 — effort S — risk low — category: skill triggering
  Why: the pack says descriptions trigger on user words ("status", "where were we") that autonomous runs never contain; the anthropics/skills pattern is task-phrased.
  Done when: a test runs every SKILL.md description through a lint requiring a "Use when/whenever" clause with an action phrase, and all 13 pass.

- **Add `fm skills why` usage report with per-skill trigger diagnosis** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the "why unused" answer was found by hand (T-1692). Assumption: usage logs record Skill tool calls and hook injections, so the cause can be computed.
  Done when: `fm skills why` prints, for each skill, uses, the hook-injected commands that bypass it, and a suggested fix, on a fixture log.

- **Split by job: promote the most-used playbooks into their own skills** — FEATURE — value 5 — effort M — risk med — category: skill catalogue
  Why: playbooks hide behind one skill; the read ones were review/security (14), ui/scene-3d (7), code-reviewer (5), ui/motion (4), while the user asked for "way more skills" and UI design skills with 3D and animation.
  Done when: skills for security review, code review, motion and 3D scenes exist, each with SKILL.md plus references, and the description budget test still passes.

- **Stay under the 2,000-char listing budget with a tiered descriptions file** — PERFORMANCE — value 4 — effort M — risk med — category: skill budget
  Why: 1,957 of 2,000 characters are used (T-1508), which caps the count and makes descriptions terse. Assumption: the cap is Foreman's own, set for hook and listing size, not a hard Claude Code limit.
  Done when: `fm doctor` reports the listing size, and a set of at least 20 skills is listed within the budget, using short descriptions plus a router skill.

- **Let hooks load a playbook on demand when the task type matches** — FEATURE — value 4 — effort M — risk med — category: playbook use
  Why: 65 of 82 playbooks were never read, and the hooks already know the task type (FEATURE, FIX, CLEAN). Hook context over ~10 KB becomes a preview, so inject a pointer plus a 2-line digest, not the body.
  Done when: starting a UI task makes the hook output name `ui/motion` with a digest under 600 chars, and a test shows the byte cap is respected.

- **Surface a skill and playbook "unused for 30 days" report in the final run report** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: nobody noticed the low usage until the user asked; a recurring signal closes the loop.
  Done when: the end-of-run report lists the skills and playbooks never used, with the count.

- **Add a skill-use ratchet in the evals: tasks that should trigger a skill must** — FEATURE — value 4 — effort M — risk med — category: evals
  Why: playbooks are held to a token ratchet but nothing holds triggering. Assumption: plugin/evals can run headless Claude on a prompt and read the Skill tool calls.
  Done when: an eval of 10 prompts asserts the expected skill fires at least 8 times, and a CI failure shows when a description change breaks it.

- **Ship a `fm skills new` scaffold that validates a third-party or project skill under the guard** — FEATURE — value 3 — effort M — risk med — category: extensibility
  Why: the user wants more skills, and third-party skills must run nothing unguarded. A scaffold with a lint makes adding them cheap and safe.
  Done when: `fm skills new foo` creates SKILL.md with a task-phrased description and a references folder, and `fm skills check` fails on a skill whose script bypasses the guard.

- **Wild: Skill autopilot that proposes new skills from repeated fm command sequences** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild; assumption: the usage log holds command sequences. Hooks already see repeats, such as the same review steps over many tasks.
  Done when: after 5 repeats of a command sequence, `fm skills propose` writes a draft SKILL.md to a review folder, and nothing is installed without approval.

- **Wild: Skill duel in the bench, with and without each skill, to prove each earns its place** — PERFORMANCE — value 4 — effort L — risk low — category: bench
  Why: wild; the bench and duel (T-1231, T-1866) exist, and "hardly used" raises the question of whether unused skills help at all.
  Done when: the bench report shows pass rate and cost per skill on and off, and skills with no gain are flagged for removal or merging.

- **Wild: A skill gallery page, living specimens of what each skill does, in one file** — FEATURE — value 2 — effort M — risk low — category: discoverability
  Why: wild; the user already asked for a looks gallery (`fm page`) and a 3D repo city, so the same one-file, no-network pattern could show skills, triggers and usage as a map.
  Done when: `fm page skills` writes one HTML file, and it passes the existing a11y and reduced-motion checks.

- **Show skills and their last use in the foreman-ui pane** — FEATURE — value 3 — effort S — risk low — category: UI
  Why: the pane already shows lanes, agents and History; a skills strip with "last used" makes dead skills visible. Assumption: usage data is readable from the pane's data source.
  Done when: the pane lists every skill with last-used time, and an unused one is marked "never".

- **Merge or retire skills that stay unused after the description fix** — CLEAN — value 3 — effort S — risk low — category: simplification
  Why: 13 skills with 11 unused, so some may be redundant with hook-driven fm commands (status, next, resume). Pairs with the slim-Foreman item (T-0794).
  Done when: after 30 days of the fixed descriptions, any skill with zero uses is merged into another or removed, with the CHANGELOG updated.
