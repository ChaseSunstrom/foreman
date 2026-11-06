# Brainstorm — lens: user value

- **Promote proven capture triggers to armed rules** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: `fm triggers` already groups captures by trigger with a precision figure, but nothing turns a trigger with high precision into a scheduled or event rule. Assumption: precision is stored per trigger with a sample count.
  Done when: a trigger above a set precision and sample count produces one install-card draft that cites its own hit list, and one yes arms it.

- **Log a one-line "checked, nothing found" per night** — FEATURE — value 4 — effort S — risk low — category: assurance
  Why: the night tick logs only when something happens, so a quiet night and a dead tick look the same to the user.
  Done when: after a tick with no work, `fm night status` shows "checked CI, issues, deferred dates at 03:10: 0 actions", and a skipped tick shows a gap.

- **Stage outbound drafts (issue comments, PR descriptions) behind one yes** — FEATURE — value 4 — effort M — risk med — category: outward actions
  Why: the CI and issue watchers will want to reply on GitHub. Anything posted is outward-facing and may be cached or indexed, so it needs a reviewable queue.
  Done when: a watcher lane writes `drafts/issue-123.md`, nothing is posted, and `fm yes` posts it only after the user approves that draft.

- **Add a cross-project morning card** — FEATURE — value 4 — effort M — risk low — category: digest
  Why: state is kept per project (`state/projects/foreman-4a056f`), but a user with several repos has to open each one to see what ran. Assumption: the user has more than one repo under Foreman.
  Done when: one card lists, per project, the lanes that ran, the lanes that failed, and the yeses waiting, sorted by minutes unlocked.

- **Let stack cards carry suggested triggers** — FEATURE — value 3 — effort M — risk low — category: triggers
  Why: the project has python, tailwind and cc-plugin-release cards, and they already know the repo's gates. A new repo should get "pytest on push, lockfile advisory weekly" from the card, not from the user.
  Done when: in a repo detected as python, `fm triggers suggest` lists at least two card-sourced recipes, each with exact unit text and an install yes.

- **Suspend a trigger when the user reverts what it made** — FEATURE — value 5 — effort S — risk low — category: feedback
  Why: assumption: a reverted self-started commit is the clearest unforgeable "no" the user gives, and acting on it needs no survey. The standing steers also want outcome signals Foreman didn't author.
  Done when: reverting a commit stamped with a trigger id suspends that trigger and files one capture asking "re-arm?".

- **Review the deferred backlog weekly as one batch yes** — FEATURE — value 3 — effort M — risk low — category: backlog
  Why: about 30 open tasks are marked "Later from T-07xx" or deferred, and the user can't realistically read them all. Assumption: the user would rather answer once a week than never.
  Done when: a weekly lane produces one sheet marking each deferred item keep, drop or revive with a reason, and a single yes applies all of the marks.

- **Draft the CHANGELOG entry when a task lands on main** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: recent commits are one-line T-numbers, and CHANGELOG and MASTER docs are written by hand. The drafts also stay local until the user approves them.
  Done when: after a merge, a branch holds a draft CHANGELOG line quoting the task and its ask, and the draft passes the docs-drift check.

- **Measure time to the first self-started result the user kept** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: the user installed the timers, but nothing shows when self-triggering first paid off. Assumption: nobody tracks this today.
  Done when: `fm doctor` prints "first kept self-start: 2d after install", or "none yet" with the likely reason.

- **Run a nightly `fm doctor` that files its own fix tasks** — FEATURE — value 3 — effort M — risk med — category: self-health
  Why: assumption: the doctor runs only when someone remembers it, so red rows can sit unseen. The fix tasks must stay out of the guard and hooks.
  Done when: a red doctor row creates exactly one deduplicated task, and a green re-run closes it.

- **Wild: Add a dead-man switch for the user** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: wild. Triggers keep spending while the user is gone. If nobody has run `fm` for N days, the switch parks every trigger and leaves one note.
  Done when: after the silent window, all triggers show "parked: no user activity", and the next `fm` command offers a one-word resume.

- **Wild: Print each trigger's story with `fm triggers story`** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A paragraph per trigger ("installed Tuesday, fired 9 times, 7 kept, once reverted") makes a table of rows readable enough to forward.
  Done when: the command prints one plain paragraph per trigger, and its numbers match the fire log.

- **Wild: Add an end-of-day wrap that seals state and queues tomorrow's first task** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: wild. When the user goes idle at their usual stop time, Foreman commits nothing, writes the baton, and puts the one task most likely to be wanted first in the morning card. Assumption: the user's idle pattern is learnable from timestamps.
  Done when: after an idle trigger, the baton file is sealed and the next session's first line names tomorrow's task.

- **Wild: Fire a shell "again" from a typed correction** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: wild. When the user types the same fix twice in a week, Foreman offers to make it a trigger or a hook instead of a third repeat.
  Done when: on the third matching command, a one-line offer appears with a dry-run preview, and declining it records the refusal.

Next question: which of the 59 empty cells would a user actually notice if they stayed empty, judged by what the user's own sessions touch, not by Foreman's probes?
Next question: what does the user do in the first five minutes after reading a morning card, and does any trigger shorten that path?
