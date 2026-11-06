# Brainstorm — lens: unspoken needs

- **Make the "Next:" hook line name the skill, not just the fm command** — FIX — value 5 — effort S — risk low — category: skill triggering
  Why: Facts say the hooks inject the exact `fm …` command each turn, so Claude never loads the skill describing that step (13 of 14 skills unused in 30 days). Assumption: the hook can append "(skill: foreman:X)" within the 10 KB limit.
  Done when: a recorded session's hook output contains a skill pointer for each step, and `fm usage` shows skill loads rising in a replay of the same task.

- **Turn every injected "Next:" step into a skill-backed step** — FEATURE — value 5 — effort M — risk med — category: skills
  Why: The duplication between hook text and skill text is the root cause (cause 1). Single-source: the hook emits a one-line summary and the skill holds the detail, so the skill is the only place the how lives.
  Done when: for each hook-injected command, the fm output and the skill share one source file, and a test fails if they drift.

- **Rewrite skill descriptions around task moments, not user words** — FIX — value 4 — effort S — risk low — category: skill triggering
  Why: Cause 2: descriptions trigger on "status" and "where were we", words autonomous runs never contain. The anthropics/skills pattern is "Use whenever you are about to …". Assumption: 1,957 chars is enough if each description is rewritten rather than lengthened.
  Done when: every description starts with a "Use when about to …" clause and a trigger eval fires on at least 80% of its matching task phrasings.

- **Add a skill-trigger eval that measures firing, not just text** — FEATURE — value 5 — effort M — risk low — category: evals
  Why: `plugin/evals/` exists, and there are 21 files, but nothing in the pack shows a measure of whether a skill loads. Without it, "improve triggering" can't be proven. Assumption: a headless run can log Skill tool calls.
  Done when: `fm eval skills` prints per-skill fire rate over N scripted prompts and fails CI below a set floor.

- **Free description budget by splitting rarely needed skills into user-only commands** — CLEAN — value 4 — effort S — risk low — category: skill budget
  Why: Cause 3: the 2,000-char cap (T-1508) limits count. `capture` and `design-extract` already use `disable-model-invocation`. Moving status, tidy, resume and library the same way costs nothing when the hooks already drive them, and frees room for task-moment skills.
  Done when: the listing budget drops below 1,200 chars with no skill lost, and the freed room funds new model-invocable skills.

- **Promote the four most-read playbook families to first-class skills** — FEATURE — value 4 — effort M — risk med — category: skills
  Why: Cause 4: playbooks hide behind one skill, yet review/security, ui/scene-3d, review/code-reviewer and ui/motion are the ones actually read (30 reads). Assumption: a skill per family stays under the budget if descriptions are short.
  Done when: four new skills each load their playbooks from references, and `fm usage` attributes reads to them.

- **Show a skill-usage scorecard in the Foreman pane and `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: The user found out "hardly used" only via a one-off fact run (T-1692). They will want it standing, because they keep asking for more skills and will ask whether the new ones work.
  Done when: `fm doctor` lists each skill's 30-day loads and flags any at zero, and the pane shows the same.

- **Prune or merge skills that stay at zero after the fix** — CLEAN — value 3 — effort S — risk low — category: skill hygiene
  Why: The user asked for "more skills", but 13 of 14 are unused; adding more without a retirement rule repeats the problem. Assumption: they prefer a smaller, used set over a larger idle one.
  Done when: a rule in `fm doctor` proposes removing a skill with zero loads across 60 days, and the proposals are listed for the user.

- **Let a project overlay its own skills, guarded** — FEATURE — value 3 — effort M — risk med — category: extensibility
  Why: The playbook overlay at `.claude/playbooks` already exists (the T-1621 steers), so skills could follow the same path. The constraint says third-party skills run nothing unguarded.
  Done when: a `.claude/skills/` skill added in a repo is listed by `fm doctor`, and any script it bundles goes through the guard in a test.

- **Wild: Make Claude write a skill after repeating a manual fix twice** — FEATURE — value 4 — effort L — risk med — category: self-improving
  Why: wild. Lessons already exist (T-0217 confidence idea). Assumption: repeated command sequences are visible in the transcript. A proposed skill goes to the inbox for the user to approve, never installs itself.
  Done when: after two near-identical sequences, `fm` queues a draft SKILL.md task with the evidence attached.

- **Wild: A "skill of the day" nudge that rehearses an unused skill on a harmless task** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Unused skills never get real-use feedback, so their descriptions never get tuned. Assumption: a read-only dry run in a spare lane is cheap.
  Done when: a nightly run exercises one zero-use skill in a scratch worktree and logs whether it loaded and finished.

- **Wild: Skills that the model can read as a map, one "foreman:index" skill that routes everything** — FEATURE — value 3 — effort S — risk med — category: routing
  Why: wild. One short description (about 150 chars) covers all 13 skills and 82 playbooks, loading a table on demand. It trades discoverability for budget, so it should be measured against the eval above.
  Done when: the eval shows the index skill fires at least as often as the separate ones it replaces, in a side-by-side run.

- **Record why a skill didn't load, from the transcript** — FEATURE — value 3 — effort M — risk low — category: diagnostics
  Why: The explanation in the pack is inferred ("as far as we can see"). The user asked "why?", and a measured answer would replace the guess. Assumption: transcripts show whether a skill was listed and a matching fm command ran instead.
  Done when: `fm usage --why-not NAME` reports, for sessions where the skill's topic came up, whether a hook-injected command pre-empted it.
