# Brainstorm — lens: delight

- **Give every run a two-word name** — FEATURE — value 4 — effort S — risk low — category: naming
  Why: runs are referred to by ids like T-1213 and T-1373 in the pack's ideas and user requests. A short memorable name (e.g. "quiet otter") next to the id makes `fm status` and the TUI easier to scan and talk about. Assumption: users recall names more easily than numbers.
  Done when: `fm status` and `fm code why` show the name beside the id, and `fm code why <name>` resolves to the same run.

- **Set the terminal tab title to the run's state** — FEATURE — value 3 — effort S — risk low — category: terminal polish
  Why: with several sessions open, the tab shows only a path. Assumption: a run's state (queued, running, needs you, closed) is readable from the same journal `fm code why` uses.
  Done when: a run that reaches "needs you" changes its tab title to include that state, and the title resets when the run closes.

- **Write commit messages in the repo's own voice** — FEATURE — value 3 — effort S — risk low — category: commits
  Why: the recent commits are terse, lowercase, and use ticket ids and "Merge T-…" forms. A generated message that matches that house style reads as if the team wrote it.
  Done when: `fm task finish` produces a commit subject that passes a test comparing it to the last 20 commit subjects for length, casing and ticket-id placement.

- **Answer a near-miss command with "did you mean", one key to accept** — FEATURE — value 4 — effort S — risk low — category: command line
  Why: the pack's user words include "fm isnt recognized as a command on my system", a first-run friction point. Assumption: a typo or unknown subcommand is a common cause of that kind of confusion.
  Done when: `fm stauts` prints "did you mean `fm status`? [Enter to run]" and exits without running anything if the key isn't pressed.

- **Ring the terminal bell only when a run needs you and you've looked away** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: the pack shows runs that wait on usage limits, gate locks and stalled cards, all of which need the user's attention without constant pinging. Assumption: idle time can be read from the terminal's focus events.
  Done when: a run that needs input rings once when the terminal is unfocused for more than 60 seconds, and never while focused.

- **Stamp a playbook's first proven pass** — FEATURE — value 2 — effort S — risk low — category: playbooks
  Why: the pack's playbook library is growing to tens of thousands of entries, so most are never seen after they're written. A small first-pass record makes each one feel like it did something the first time it worked.
  Done when: the first closed task that cites a playbook and passes its check writes a "first light" line to that playbook's entry, once, and `fm playbooks show` displays it.

- **Surface the changed assertion first in each diff** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the demo's run ends in a test that fails without the change, which is the part the reviewer cares about. Assumption: test-assertion lines are a small share of a diff, so pulling them to the top saves reading.
  Done when: `fm task prove` output lists changed assertion lines above other hunks, verified by a fixture diff that puts a test change last.

- **Name each subagent and give it a lens-true personality** — FEATURE — value 3 — effort S — risk low — category: agents — wild
  Why: the brainstorm children already carry lenses like "delight" and "approaches", so each can have a name and a one-line voice that matches its lens ("the skeptic", "the one who plays"). Delight comes from knowing who said what.
  Done when: each brainstorm child's output header shows its name and lens, and two runs with the same lens produce the same name.

- **Close each task by reading back one of your own past corrections** — FEATURE — value 3 — effort S — risk low — category: feedback loop — wild
  Why: the pack records corrections such as "dont ask me for anything either" and "step 1 is the profile". Reading one back at close, chosen to match the current task's kind, turns a pushback into a habit.
  Done when: `fm task finish` shows one correction whose tags match the task's area, and a test confirms it is skipped when no tag matches.

- **Write a Sunday letter to next Monday's you** — FEATURE — value 3 — effort S — risk low — category: continuity — wild
  Why: the queue carries open work across weeks (T-0034 through T-1331 are still deferred or blocked). A short weekly note with the open items, what's blocked, and one honest sentence about what moved makes the reset feel like a page turned rather than a cliff.
  Done when: a weekly job writes a note under `.fm/letters/` listing open items by status, and the note is shown at the top of the next `fm status` after the reset.

- **Open a `?` card in the terminal UI with the next three keys** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: the stalled card's keys (w wait, k kill, m switch runner) are only findable by reading docs. Assumption: most users learn keys by trial, so a one-key reminder card helps.
  Done when: pressing `?` in the TUI shows the keys valid for the current screen, and the list changes when the screen changes.
