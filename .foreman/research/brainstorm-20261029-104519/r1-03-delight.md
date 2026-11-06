# Brainstorm — lens: delight

- **Close a task with a one-screen receipt** — FEATURE — value 5 — effort M — risk low — category: close-out
  Why: the user ships constantly ("Ship T-1982 to main", T-1987, T-1992, T-1996, T-2001) and T-0795 (plain receipts, landing ladder) sits deferred. Each ship is a ritual with no payoff moment.
  Done when: `fm ship` ends by printing a ≤12-line receipt (task id, what changed in plain words, proof commands that ran with pass/fail, files touched, seconds spent) and a test checks each field is present.

- **Suggest the near-miss on every "no match" error** — FEATURE — value 4 — effort S — risk low — category: errors
  Why: the last three commits are all "did you mean" work (docs-impact path suggestions T-1995/T-2000, run.py `-k` naming, `CoreIntegrity` vs `core_integrity` case/underscore matching). The user clearly likes errors that give a way forward; the pattern is applied one error at a time.
  Done when: a shared `suggest(name, candidates)` helper backs docs-impact, run.py and an unknown `fm <subcommand>`, and a test shows `fm tsk` suggests `task`.

- **Turn the stage rail into a live progress bar with a finish flourish** — FEATURE — value 4 — effort M — risk low — category: terminal UI
  Why: T-0796 (progress bar, spinner, motion, palette) is deferred; the demo already shows a work bar and stage rail, so motion that explains state fits.
  Done when: the pane's work bar advances per proven step, and closing a task plays a brief ≤1s completion animation that is skipped when `NO_COLOR` or reduced-motion is set (test asserts both paths).

- **Make task ids clickable everywhere** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: T-0796 lists clickable ids; ids like T-1998 appear in every commit, message and block line.
  Done when: in a supporting terminal, `T-1998` in `fm` output is an OSC 8 link opening the task detail, and it prints as plain text when piped.

- **Show a "streak" line for first-time passes** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: T-0217 plans lessons with confidence that rises on first-time passes; the data exists but isn't surfaced as a small reward. Assumption: first-time-pass is recorded per task.
  Done when: `fm status` shows "7 tasks in a row passed first try" when true, and the line is absent when the streak is 0.

- **Say what the dry loop learned when it stops** — FEATURE — value 4 — effort S — risk low — category: loop
  Why: the user fixed the dry-streak counting twice (T-1991, budget-limited rounds). A stop reason like "2 dry rounds" is the moment people want a story.
  Done when: a loop that ends prints a summary of rounds, tasks closed, ideas dropped with reasons, and budget spent, with budget-limited rounds labelled separately.

- **Give `fm doctor` a mood** — FEATURE — value 3 — effort S — risk low — category: health
  Why: doctor is the first thing run in the gates and warned wrongly about in-scope core (T-1998). A one-line verdict ("all clear, 3 things worth a look") makes it quick to read.
  Done when: doctor's last line is a single verdict with a count of warnings, and the exit code is unchanged.

- **Replay a finished task as a 20-second scrubbable timeline** (wild) — FEATURE — value 4 — effort L — risk med — category: replay
  Why: the demo SVG shows the product is most persuasive in motion, and the data (edits, proofs, test fails-then-passes) is already recorded. Assumption: events carry timestamps.
  Done when: `fm replay T-1213` opens a page or terminal view stepping through plan, edits, failing proof, fix, passing proof, and `--svg` writes a shareable file.

- **Hand out an end-of-week "Foreman wrapped" card** (wild) — FEATURE — value 3 — effort M — risk low — category: share
  Why: the Today charts already exist, and people show polished stats. Assumption: history is stored per day.
  Done when: `fm wrapped` writes a single SVG with tasks closed, tests proven red-then-green, fewest-edit fix, and busiest hour, built only from local data.

- **Let the guard hook speak in a dry voice when it blocks** (wild) — FEATURE — value 3 — effort S — risk low — category: personality
  Why: the guard stops commands the user would never want in bypass mode; a block is a surprise moment. A short plain reason plus the safe alternative turns a refusal into help.
  Done when: each guard denial prints what was blocked, why, and one safe command to run instead, and a test covers every guard rule having all three.

- **Play a quiet tick when a long gate run finishes** (wild) — FEATURE — value 2 — effort S — risk low — category: sound
  Why: gates and ships take minutes (the "never two suites at once" work shows how long), and the user is often elsewhere. Assumption: off by default.
  Done when: with `sound=on` in settings, the terminal bell rings once when gates finish with pass and twice on fail, and with the setting off nothing rings.

- **Print the next move after every command** — FEATURE — value 4 — effort M — risk low — category: guidance
  Why: the user keeps filing fixes about rough edges in discovery (T-1909 "fm help task refused", no-match errors). A single "next: fm task prove" hint keeps them moving.
  Done when: task, check and ship commands end with one dim "next:" line chosen from task state, hidden with `--quiet`.

- **Show a diff-of-the-day on the pane's idle screen** — FEATURE — value 2 — effort S — risk low — category: empty state
  Why: the Foreman pane has lanes and charts but an idle pane is just empty. Assumption: the pane has an idle state.
  Done when: with no active task, the pane shows the last closed task, its proof, and the next queued item, and a snapshot test checks it.
