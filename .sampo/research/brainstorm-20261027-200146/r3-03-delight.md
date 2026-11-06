# Brainstorm — lens: delight

- **Thank the user when their override was right** — FEATURE — value 4 — effort S — risk low — category: feedback loop
  Why: assumption: the pack shows the user steering and dropping Foreman's calls often. When a user overrides a refusal or deferral and the gate later passes, Foreman credits the override once in the close note and logs it as a preference signal.
  Done when: after an override followed by a passing gate, the close note contains one credit line, and a second close in the same task does not repeat it.

- **Print one assumption the run was least sure of** — FEATURE — value 4 — effort S — risk low — category: close honesty
  Why: assumption: runs already mark their assumptions. The close shows the single weakest one in plain words, so the user knows where to look first instead of rereading everything.
  Done when: each close shows exactly one assumption line taken from the run's marked assumptions, and shows none when the run marked none.

- **Trace a line's history as a small family tree** — FEATURE — value 3 — effort M — risk low — category: lineage
  Why: assumption: closed tasks already record their touched files. `fm lineage file:line` shows which closed tasks changed that line, newest first, as a tree, so "why is this like this" gets a one-screen answer.
  Done when: `fm lineage <file:line>` lists each closed task that touched the line, newest first, in at most one screen.

- **Greet the first run of the day with yesterday's one true win** — FEATURE — value 3 — effort S — risk low — category: greeting
  Why: assumption: the Today charts and closed-task journal already hold yesterday's wins. The first `fm` command after local midnight prints one line naming the closed task and its proof, then goes quiet for the rest of the day.
  Done when: the first `fm` command after local midnight prints one line naming yesterday's closed task, and later commands that day print nothing extra.

- **Leave a bottle note for the next run that touches those files** — FEATURE — value 3 — effort M — risk low — category: continuity — wild
  Why: wild: a run writes one sentence addressed to whichever later run touches the same paths, and that run's first context line quotes it. The note is removed after one read, so it's a letter, not a log.
  Done when: a task that closes with a bottle note makes the next task touching those paths show the note in its first context line, and a test confirms the note is gone after that read.

- **Close each task with a fortune built from the journal** — FEATURE — value 3 — effort S — risk low — category: close ritual — wild
  Why: wild: a fortune cookie whose line is a true number from the run journal ("this fix passed on try 2; your median is 1"). Every number comes from a stored field, so the delight never overstates.
  Done when: a close prints one fortune line computed from journal fields, and a test asserts each number in the fortune matches its journal field.

- **Make a test garden: one plot per test file** — FEATURE — value 3 — effort M — risk low — category: test health — wild
  Why: wild: each test file is a plot that greens with passing runs and wilts after a recorded flake, and it recovers only after ten clean passes. The flake ledger already has the data.
  Done when: `fm garden` prints one plot per test file with a state from the flake ledger, and a recorded flake turns its plot to wilted until ten passes are logged.

- **Put a lost-and-found tag on backlog items gone quiet** — FEATURE — value 2 — effort S — risk low — category: backlog care
  Why: assumption: the open-work list holds many deferred and blocked items with no sense of age. Items untouched for 30 days get a "still waiting" tag, with one command to claim them or let them go.
  Done when: `fm status` lists items older than 30 days with claim and release commands, and releasing one moves it to dropped.

- **Reopen the pane where you left it** — FEATURE — value 2 — effort S — risk low — category: continuity
  Why: assumption: the Foreman pane is restarted often, and each restart loses the selected run and scroll offset. Persisting both makes the pane feel like it never closed.
  Done when: restarting the TUI restores the selected run and scroll offset within one frame.

- **Welcome the first verified fix in each new project** — FEATURE — value 2 — effort S — risk low — category: onboarding
  Why: assumption: a new project's first closed task is a real milestone and currently gets the same receipt as the hundredth. A one-time welcome line marks it, then is stored so it never repeats.
  Done when: the first closed task in a project prints a welcome line once, and a second close in that project prints none.

- **Shake the pane like a snow globe when a gate fails** — FEATURE — value 2 — effort S — risk low — category: motion — wild
  Why: wild: a failed gate gives the pane one short shake, then settles. Reduce-motion turns the shake into a still frame, so the cue survives for users who turn motion off.
  Done when: a failing gate plays one shake sequence, and with reduce-motion on it shows a single still frame instead.
