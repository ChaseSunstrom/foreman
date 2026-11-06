# Brainstorm — lens: unspoken needs

- **Lint every DONE-WHEN at capture** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: T-1994's steer: "ac 1's -k core_integrity matched no test", so a vacuous check was accepted as an acceptance criterion. Four recent fixes (T-1994, T-1995, T-2001, batch DONE-WHEN) all concern checks that don't check what was meant.
  Done when: capturing a task whose DONE-WHEN command matches zero tests, or passes on the unchanged tree, is refused or flagged with the reason, and a test covers both cases.

- **Share one did-you-mean across all not-found errors** — FEATURE — value 4 — effort M — risk low — category: error UX
  Why: The user fixed "no test matches" (T-1996), then added path suggestions (T-1998 to T-2000), then case/underscore suggestions (T-2001), one error at a time. The next not-found (task ids, lib cards, skills, gate names) will need the same fix.
  Done when: `fm task`, `fm lib show`, `fm gates` and `run.py` give a ranked "did you mean" for a near-miss name, from one helper with one test table.

- **Add a concurrency stress harness for the hook and gate paths** — CLEAN — value 5 — effort M — risk med — category: reliability
  Why: Three separate fixes in a row for two suites running at once (T-1967, T-1974, T-1984). Each was found by dogfooding, not by a test.
  Done when: a test fires interleaved edit, ambient, check and ship events and asserts that at most one test suite process is ever live.

- **Make one scope-aware predicate that every check uses** — CLEAN — value 4 — effort M — risk med — category: consistency
  Why: The same bug keeps recurring in different places: `_theirs` dropped from `_task_files`, first_touch counting only project files, doctor warning about core the task is changing inside its own scope, "the note ignores edits outside the project". Each place re-derived "is this file mine?".
  Done when: doctor, task finish, ship and the notes call a single `in_focus_scope(path)`, and a table test of own, another task's and outside-project files passes for all four.

- **Dedupe captures against closed tasks and commits** — FIX — value 4 — effort S — risk low — category: capture noise
  Why: "Noticed:" captures were dropped 74 of 106 times, and the sampled drops were "valid items done in another task or duplicates".
  Done when: a capture whose title or paths match a closed task from the last 30 days is attached to that task as a note instead of becoming a new item, and a test shows the drop rate falling on a recorded sample.

- **Flag fix clusters on one module** — FEATURE — value 3 — effort M — risk low — category: root cause
  Why: Recent commits circle fmambient, fmdocs, run.py and the gates, with 3 or more fixes each in a short span.
  Done when: `fm doctor` or `fm risk` lists any module with at least 3 FIX tasks in 14 days and proposes one "root-cause" task for it.

- **Review the deferred backlog on a schedule** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: More than 30 "Later from T-07xx/08xx" items sit deferred, many with "needs evidence" conditions. The user never revisits them, and a stale list hides the real ones.
  Done when: `fm backlog review` marks each deferred item as promote, merge, close or keep, citing whether its unblock condition now holds, and lists the changes for a one-keystroke accept.

- **Record dismissed warnings and tune the noisy check** — FEATURE — value 4 — effort M — risk low — category: noise
  Why: The user's steers show warnings that fired wrongly (the scratchpad write, the core-integrity warning inside its own scope). Each was found by hand.
  Done when: each check keeps a fired/overridden count and `fm doctor --noise` lists checks overridden more than half the time.

- **Treat repeated steers as standing rules** — FEATURE — value 4 — effort M — risk med — category: lessons
  Why: "Make sure it doesn't sit idle" had to be cited from memory to reject a later idea. T-0217 (lesson confidence) is deferred, yet steers are the strongest signal there is.
  Done when: a steer or drop that cites a principle is stored as a lesson, and a later proposal that contradicts it shows the lesson in its brief.

- **Let "Ship Tn to main" run as one command with a receipt** (wild) — FEATURE — value 3 — effort S — risk med — category: shipping
  Why: Five "Ship T-… to main" requests in this window. Assumption: each is a manual repeat of the same sequence of steps.
  Done when: that phrase in intake runs the ship sequence (still behind the existing confirm rule) and ends with a one-screen receipt of the tests run, commit and branch.

- **Predict the user's next ask and pre-draft it** (wild) — FEATURE — value 3 — effort L — risk med — category: anticipation
  Why: The history shows strong patterns: a FIX is followed by a sibling FIX or FEATURE in the same file, and a closed batch is followed by "Ship". Assumption: patterns are stable enough to draft from.
  Done when: after a task closes, `fm next` shows up to 2 drafted tasks with their paths and DONE-WHEN, and the accept rate is logged.

- **Replay real intake history as parser fixtures** (wild) — CLEAN — value 3 — effort M — risk low — category: regression
  Why: Intake bugs (titles cut mid-word, @path-only lines dropped, "Fm batch" capitalization) were found by chance on real input.
  Done when: a corpus built from redacted past intake lines runs in the test suite and asserts titles, scopes and DONE-WHEN come out as the user wrote them.

- **Fail the build on dead-end refusals** (wild) — CLEAN — value 3 — effort M — risk low — category: error UX
  Why: "no test matches…" and "commit it through a task, or git checkout it back" both led nowhere in cases the user hit.
  Done when: a test scans every user-facing refusal string and fails if it names no next command or an allowlisted reason.

- **Dry-run a new check against recent sessions** — SECURITY — value 3 — effort L — risk med — category: false positives
  Why: Several steers are false positives from checks that were never tried on real history before shipping.
  Done when: `fm doctor --replay` runs a candidate check over the last 50 recorded sessions and reports how many times it would have fired and how many of those were overridden.
