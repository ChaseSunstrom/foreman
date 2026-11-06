# Brainstorm — lens: simplicity

- **Recall related past work at focus time** — FEATURE — value 5 — effort S — risk low
  Why: decisions.md, research/ and archived briefs are never surfaced for a related request. Simplest fix is plain token overlap on title and scope, with no index.
  Done when: `fm focus` on a task whose title overlaps an archived task prints up to 3 one-line hits (id, title, lesson or decision) in ≤ 400 chars, and prints nothing when nothing overlaps.

- **Require a one-line Lesson at task done** — FEATURE — value 4 — effort S — risk low
  Why: lessons only reach memory if reflect is run by hand. `fm task done` already refuses without evidence and audits, so it can require `Lesson: <text|none>` and write it to the ledger, where recall reads it.
  Done when: `fm task done` without a lesson is refused, the lesson appears in the ledger, and `fm recall` returns it for a matching task.

- **Require red-then-green evidence for FIX tasks** — FEATURE — value 5 — effort S — risk med
  Why: Foreman can't tell a weak test from a real regression test. `fm task evidence --run` already records real exit codes, so a gate can require a failing run followed by a passing run of the same command.
  Done when: a FIX task with only a passing run for its regression criterion can't be marked done, and one with a fail-then-pass pair can.

- **Generate a small project map at SessionStart** — FEATURE — value 4 — effort M — risk low
  Why: every intake re-reads the code from scratch. `fm map` would derive test command, top-level dirs and top-5 churn files (from `git log`, stdlib only) into state/map.md, refreshed only when HEAD changes and capped at 1,500 chars.
  Done when: map.md has those three items, is not rewritten when HEAD is unchanged, and the intake skill reads it.

- **Replace the tier regex with a ledger lookup** — PERFORMANCE — value 3 — effort S — risk low
  Why: `guess_tier` is a regex plus a length check and never learns. Use the median steps, attempts and files of the closest past tasks by type and scope, and fall back to the regex when there are fewer than 3 matches.
  Done when: on a fixture ledger where similar tasks were L, the guess returns L, and with an empty ledger it returns the current result.

- **Check scope drift against the frozen diff at done** — FEATURE — value 3 — effort S — risk med
  Why: the injected "Next" line is only a hint, but `fm audit prep` already freezes the diff. Files changed outside the task's scope globs would need a recorded note before done.
  Done when: a diff touching an out-of-scope file without a note blocks done, and adding the note unblocks it.

- **Retire procedures and injections that are never used** — CLEAN — value 2 — effort S — risk low
  Why: the always-on budgets are near their limits and there are 40 playbooks. `fm repeats` already reads the ledger, so it could list procedures never loaded in N tasks as candidates to cut.
  Done when: the command lists unused playbooks from a fixture ledger, and removing one keeps the context-budget tests passing.
