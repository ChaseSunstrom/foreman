# Brainstorm — lens: capability map

- **Make the "Next:" hook line load the skill** — FIX — value 5 — effort S — risk low — category: triggering
  Why: the UserPromptSubmit and Stop hooks inject the exact next `fm` command, so Claude never needs the skill that describes the same step (cause 1 in the pack). Have the line read "Next: `fm X` (skill foreman:Y covers this)", or inline the skill's 3-line digest.
  Done when: in a recorded session, a hook-prompted step produces a Skill tool call for the matching skill, and `fm usage` counts it.

- **Add a skill trigger eval (`fm skills eval`)** — FEATURE — value 5 — effort M — risk low — category: skill evals
  Why: 12 of 13 skills had zero uses in 30 days and nobody measures why. Compare the best skill suites: they test triggering with a corpus of task-phrased prompts and check which skill fires.
  Done when: `fm skills eval` runs ≥5 prompts per skill headless, prints a fired/missed table, and exits non-zero below a set hit rate.

- **Rewrite descriptions in task terms** — FIX — value 5 — effort S — risk low — category: descriptions
  Why: cause 2 says the descriptions trigger on user words ("status", "where were we") that autonomous runs never contain. The anthropics/skills pattern is "Use whenever you are about to …". The 2,000-char cap (T-1508) still applies.
  Done when: every description opens with a "Use when about to/after …" clause, the total stays ≤2,000 chars, and the trigger eval hit rate rises versus the old text.

- **Promote the proven playbooks to skills** — FEATURE — value 4 — effort M — risk low — category: skills catalogue
  Why: reads were review/security 14, ui/scene-3d 7, code-reviewer 5, ui/motion 4, all behind the single `playbooks` skill (cause 4). The user also asked for "way more skills" and UI/3D/motion design skills.
  Done when: those four exist as their own skills with references beside SKILL.md, and a fresh session can invoke each by name.

- **Route playbooks by phase and file type** — FEATURE — value 4 — effort M — risk med — category: hooks
  Why: 65 of 82 playbooks were never read, because only a human or the `playbooks` skill reaches them. A PreToolUse or UserPromptSubmit hook could match `.css`/`.html`/`scene.json` edits, or a security-sensitive diff, and inject that playbook's digest. The injection must stay under the ~10 KB preview limit, so it needs a size check.
  Done when: editing a `.css` file in a test session injects a digest of `ui/motion`, under 10 KB and once per task.

- **Report dead skills in `fm usage` and the web UI** — FEATURE — value 4 — effort S — risk low — category: telemetry
  Why: usage data already exists (brainstorm 2, others 0), but only as a count. A report of offered, fired and never-used skills, with a keep/merge/retire suggestion, turns it into action. The web UI is the only surface and has no skills page yet.
  Done when: a Skills page lists each skill and playbook with last-used date and 30-day count, and flags those with zero use.

- **Add a prompt-to-skill preview box in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: authors can't see why a description does or doesn't fire. A box where you type a prompt and see which skills the description-matcher would rank first gives a fast loop and pairs with the eval.
  Done when: typing "I'm about to edit the guard hook" in the box highlights the expected skill and shows its matching phrase.

- **Add `fm skill new` and `fm skill lint`** — FEATURE — value 4 — effort M — risk low — category: authoring
  Why: assumption: authoring is manual. A scaffold plus a lint checks frontmatter, the description budget, a "when" clause, the references layout and the token ratchet. This is the missing piece of a complete skill system, next to skill-creator in anthropics/skills.
  Done when: `fm skill new x` creates a valid skeleton that passes `fm skill lint`, and a deliberately bad description fails it.

- **Import third-party skills through the guard (`fm skill add <repo>`)** — FEATURE — value 3 — effort L — risk high — category: ecosystem
  Why: the constraint is that third-party skills run nothing unguarded. The anthropics/skills repo and the marketplaces are a source of coverage Foreman lacks (T-0869 defers rival imports). Import into an isolated directory, statically scan bundled scripts, and run them only through the guard.
  Done when: adding a sample skill with a script `rm -rf`-style command is refused by the scan, and a benign one installs and runs under the guard.

- **Generate a per-project skill from `fm map` (wild? no: grounded)** — FEATURE — value 3 — effort S — risk low — category: project skills
  Why: T-0365 already defers a generated section with gates, layout and conventions, and `fm map` has that data. A skill in `.claude/skills/` named for the repo and triggering on "about to run tests/build/commit" gives the model repo facts on demand.
  Done when: `fm map --skill` writes a valid skill whose body lists the repo's real gates, and `fm skill lint` passes it.

- **Draft a skill when a lesson recurs (wild)** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild. T-0217 (lesson confidence) and T-0035 (eval capture) point the same way. When the same lesson is recalled or violated ≥3 times, Foreman drafts a skill from it, with the failing case as its eval. The user reviews it in the web UI.
  Done when: seeding 3 matching lessons produces a draft skill plus an eval case, listed as pending approval and never auto-installed.

- **Measure each skill's lift with a skill duel (wild)** — PERFORMANCE — value 4 — effort L — risk med — category: bench
  Why: wild. T-1231 (beat Claude Code on the duel) and T-0866 (bench with a real corpus) both need cases. Run each skill's eval cases with and without it, and keep only skills with a measured lift on pass rate, cost or time. The rest get merged or retired.
  Done when: `fm bench skills` outputs a lift table for ≥3 skills on ≥5 cases each, with runs stored for repro.

- **Build skills as specialist subagent launchers (wild)** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: wild. The demo already shows a scout subagent. A skill such as `scout-before-edit` or `review-lane` could carry the briefing template and the read-only tool limits, so Claude launches a checked specialist in one step instead of improvising the brief.
  Done when: invoking the skill spawns a subagent with the template's brief and read-only limits, and its result is saved as a findings file.

- **Move user-only skills out of the listing budget** — CLEAN — value 2 — effort S — risk low — category: budget
  Why: assumption: `capture` and `design-extract` use `disable-model-invocation`, so they gain nothing from model-facing description text. If they count toward the 1,957 chars, converting them to slash commands frees room for the new task-phrased skills.
  Done when: the measured description total drops by their length, and `/capture` and `/design-extract` still work.
