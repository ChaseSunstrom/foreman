# Brainstorm — lens: simplicity

- **Fold the 13 skills into 4 task-shaped skills** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: 11 of 13 skills never used in 30 days; the 2,000-char description budget (1,957 used) is spent on rarely-triggered names. Merge status/next/resume/doctor into one "orient" skill, brainstorm/improve/directions/reflect into one "plan", capture/intake into one "intake", and library/playbooks/tidy into one "reference". Fewer, fatter descriptions each get ~500 chars.
  Done when: `fm doctor` shows ≤5 plugin skills, total description chars ≤2,000, and each description starts with "Use whenever you are about to …".

- **Rewrite descriptions as task triggers, not user words** — FIX — value 5 — effort S — risk low — category: triggering
  Why: facts say descriptions trigger on "status", "where were we", words that long autonomous runs never contain. The anthropics/skills pattern says to describe the moment, not the phrase.
  Done when: every shipped description names a Claude-side moment (e.g. "about to edit a UI file", "tests just failed twice"), and a test lints for the absence of bare user-word triggers.

- **Make the "Next:" hook line name the skill** — FIX — value 5 — effort S — risk low — category: hooks
  Why: the hooks inject the exact fm command, so Claude never loads the skill describing that step. Appending "(foreman:orient has the why)" turns the injection into a pointer instead of a bypass. Stays well under the 10 KB preview limit.
  Done when: the hook output for a fixture state includes a `foreman:` skill reference, and `fm usage` shows skill loads rising in a 20-turn e2e run.

- **Delete skills whose job a hook already does** — CLEAN — value 3 — effort S — risk low — category: skills
  Why: status and next duplicate the hook's "Next: …" line. A skill that can never win against injected context is dead weight in the budget.
  Done when: those skills are removed or made user-only (`disable-model-invocation`), and the description budget drops accordingly.

- **Make playbooks self-surfacing by path, not by one skill** — FEATURE — value 4 — effort M — risk med — category: playbooks
  Why: 65 of 82 playbooks never read; they hide behind one skill. The reads that happen are review/security, ui/scene-3d, ui/motion: topics matching the task. Have the hook add a one-line "playbook: ui/motion" when the touched files or task type match, with no skill needed.
  Done when: editing a `.css` file with an animation in a fixture session injects a single playbook pointer, and the playbook-read count appears in `fm usage`.

- **Add a skill-use report to the close-out** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the 30-day usage fact had to be gathered by hand in T-1692. A one-line "skills used / offered / ignored" at task close makes the problem visible each time.
  Done when: `fm task done` prints skill and playbook usage for that task, and a test covers the zero-use case.

- **Retire playbooks nobody reads after 90 days** — CLEAN — value 3 — effort M — risk med — category: playbooks
  Why: the token ratchet applies to playbooks, and 65 unread ones cost maintenance and budget. Archive, don't delete; `fm playbooks show` still finds them.
  Done when: `fm playbooks prune --dry-run` lists never-read playbooks older than 90 days and the archive path still resolves through `show`.

- **One-line skill smoke test per skill** — FEATURE — value 3 — effort S — risk low — category: tests
  Why: assumption: skills are untested for triggering. Each skill ships a sample situation, and a test asserts its description matches it by keyword overlap.
  Done when: `plugin/tests` has a case per skill that fails when a description is emptied.

- **Wild: Let Claude write the missing skill itself** — FEATURE — value 4 — effort L — risk med — category: skills — wild
  Why: assumption: repeated manual `fm` sequences are visible in the transcript. When the same three commands recur across tasks, Foreman drafts a project-local skill, held by the guard and shown to the user for a yes.
  Done when: a fixture with a repeated command trio yields a draft `.claude/skills/<name>/SKILL.md` that passes the description lint and is not active until approved.

- **Wild: Zero skills mode: skills as `fm help <moment>`** — CLEAN — value 3 — effort M — risk high — category: simplicity — wild
  Why: if hooks already guide the model, skills may be the wrong channel. Test shipping the guidance only as hook text and `fm` subcommands, with zero skills, against the current setup on the bench.
  Done when: a bench comparison of both configs over the same cases is published, with the held-rate difference stated.

- **Wild: A skill that appears only when it is needed** — FEATURE — value 4 — effort L — risk med — category: skills — wild
  Why: the 2,000-char budget caps the count, yet most skills are relevant only in certain states. Foreman swaps which skill descriptions are installed (a symlink in the plugin dir) as the task state changes: UI task on, design skills in; verify stage, review skills in.
  Done when: switching a fixture task from build to verify changes the listed skill set, and the total stays ≤2,000 chars.

- **Show skills in the web UI with their hit rate** — FEATURE — value 2 — effort S — risk low — category: web UI
  Why: the user asked "why are they hardly used?" and had no screen to answer it. A small table of skill, offered, loaded and last used makes the answer visible.
  Done when: the web UI skills page lists all shipped skills with load counts matching `fm usage`.
