# Brainstorm — lens: bold bets

- **Replace hooks' "Next: fm …" with "Next: skill foreman:X" where a skill wraps the step** — FIX — value 5 — effort M — risk med — category: triggering
  Why: the hooks inject the exact fm command each turn, so Claude never loads the skill describing that step (13 of 14 skills unused in 30 days). Make the injected line name the skill, or pair command and skill in one short line.
  Done when: in a recorded session, at least 5 of the skills fire through the Skill tool with the hook line pointing at them, shown by `fm usage`.

- **Turn the skills into task-shaped, "Use whenever you are about to …" triggers** — FIX — value 5 — effort S — risk low — category: descriptions
  Why: most descriptions trigger on words like "status" and "where were we" that autonomous runs never contain. The anthropics/skills pattern is task-phrased descriptions.
  Done when: a trigger eval runs each rewritten description against 10 prompts drawn from real task transcripts, and each skill triggers on at least 8 of its 10.

- **Promote the 82 playbooks into per-job skills via a generated stub skill per playbook family** — FEATURE — value 5 — effort M — risk med — category: playbooks
  Why: playbooks hide behind one skill, and 65 of 82 were never read. Reads concentrated in review/security, ui/scene-3d, review/code-reviewer and ui/motion, so families with a clear trigger already work. Budget: one-line descriptions, generated from playbook frontmatter, and the 2,000-character cap forces grouping rather than 82 entries.
  Done when: `fm doctor` shows the family stubs fit the listing budget, and a playbook family read count rises above zero in a week of use.

- **Lift the 2,000-character description cap with a two-tier listing: a router skill plus lazy detail** — FEATURE — value 4 — effort M — risk med — category: budget
  Why: decision T-1508 kept the cap (1,957 used), which makes descriptions terse and limits skill count. One "foreman:route" skill with a compact index in its body can point at many more jobs without spending listing characters.
  Done when: the skill count rises past 13 and `fm doctor` still reports the listing under budget.

- **Add a skill-miss detector: flag turns where Claude ran the fm command a skill covers without loading the skill** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the usage fact (brainstorm 2, others 0) is a snapshot, and nothing says why a skill was skipped. Logging "skill-covered step, skill not loaded" turns the cause into data.
  Done when: `fm usage --skills` lists per skill the covered steps run versus times loaded.

- **Delete or fold skills that never earn a use after a trial window** — CLEAN — value 3 — effort S — risk low — category: pruning
  Why: 13 skills and 12 are unused. Some, like status and next, may duplicate the injected "Next:" line, so they should merge into the hook rather than ship as dead listings.
  Done when: each skill has a recorded use count, and those at zero after 30 days are merged or removed with a changelog line.

- **Write skills Claude chooses over the hook line: a "before you edit" and a "before you close" skill with scripts bundled** — FEATURE — value 4 — effort M — risk med — category: new skills
  Why: Foreman's core is plan before editing and prove before closing. Skills that bundle `fm task prove` and gate checks as scripts give Claude something the bare hook line cannot.
  Done when: both skills load in a real run, and the closing skill's script output appears in the task's evidence.

- **Ship a skill pack for the design work the user keeps asking for (3D, motion, looks)** — FEATURE — value 4 — effort M — risk low — category: design skills
  Why: the user asked earlier for "way better UI design skills with 3D, good animations, non generic", and ui/scene-3d and ui/motion are among the few playbooks actually read.
  Done when: separate skills for scene, motion and looks exist, each with a bundled reference, and each is invoked in at least one real UI task.

- **Skill auto-curation: Foreman proposes a new skill from a lesson that recurred 3 times** — FEATURE — value 4 — effort L — risk med — category: self-growth — wild
  Why: assumption: Foreman already stores lessons (T-0217 mentions confidence on lessons). Recurrence is a direct signal that a skill is missing.
  Done when: after 3 matching lessons, `fm skills propose` writes a draft SKILL.md that passes the description lint, and it is held for the user's approval.

- **Skill duel: A/B the same task with and without a skill and publish the delta** — PERFORMANCE — value 3 — effort L — risk med — category: evidence — wild
  Why: assumption: the bench and duel infrastructure (T-1231, T-0866) can be reused. Only skills with a measured win keep their listing slot.
  Done when: a report shows pass rate, cost and time per skill on at least 5 cases, and a skill with no gain is flagged.

- **Install third-party skills through the guard, with a "skill sandbox" that shows what a skill's scripts would run** — SECURITY — value 3 — effort L — risk high — category: ecosystem — wild
  Why: the constraints say third-party skills run nothing unguarded. A dry-run preview of every bundled script, checked by the guard before first use, makes a skill marketplace safe.
  Done when: a skill from an outside repo installs, its scripts are listed with the guard's verdicts, and a script that would break a rule is refused.

- **Make skills a first-class pane in foreman-ui: a "which skills fired and which should have" strip** — FEATURE — value 3 — effort M — risk low — category: UI visibility — wild
  Why: the user cares about seeing the work (the live tree and the Foreman pane in the demo), and unused skills are invisible today.
  Done when: the pane shows per-session skill loads and misses, and the strip has empty, loading and error states.

- **Add a per-project skill overlay in .claude/skills, matching the playbook overlays already shipped** — FEATURE — value 3 — effort S — risk low — category: project skills
  Why: T-1621 already loads a project's `.foreman/playbooks` overlays and the guard allows writes to `.claude/playbooks`. The same route for skills lets each repo carry its own gates and conventions.
  Done when: a skill in a project's overlay folder is listed by `fm doctor` and loads in a session there, with the guard still blocking everything else.
