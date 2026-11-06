# Brainstorm — lens: delight

- **Report a bad refusal with one key** — FEATURE — value 5 — effort M — risk low — category: friction
  Why: Many recent asks are one blocker that was wrong or dead-ended: the core-integrity warning on in-scope core, the docs-impact blocker with no suggested path, the `-k` that matched nothing. Each time the user types out the FIX by hand. Assumption: a refusal's context (command, task, rule id) is available when it fires.
  Done when: after any hook or gate refusal, `fm wrong` (or a single keypress in the pane) files a FIX capture that already holds the refusal text, rule id, task and triggering command, and a test shows the capture exists.

- **Greet the user with a welcome-back line** — FEATURE — value 4 — effort S — risk low — category: pane
  Why: The user queues work (`Ship Tn to main`, loops) and comes back to it. Assumption: idle gaps can be detected from the session clock. On the first prompt after 30+ minutes away, the pane or session prints one line: what landed, what is blocked on them, and the next move.
  Done when: a test that fakes a 40-minute gap sees exactly one such line, and a 5-minute gap sees none.

- **Whisper a file's history the first time it's edited** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: Fixes keep touching the same modules (`fmambient`, `fmcore`, `fmdocs`, `run.py`), and the reasons live in closed tasks and steers. When a task first edits a file, show one line, e.g. "last changed in T-1984 to stop two suites overlapping; its test is `test_ambient`". Assumption: task-to-file links are stored.
  Done when: the first edit of a file that has a closed task prints one whisper naming that task and its test, and a second edit in the same task prints nothing.

- **Flip the proof line from red to green** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: The demo's best beat is `fm task prove` showing the test fails without the change, but it reads as plain text. Render the "fails without" and "passes with" results as a two-frame red-to-green flip on that tree line. It is static under reduced motion.
  Done when: the live tree shows the flip for a proof run, and a snapshot with reduced motion set shows the final green state with both results labelled.

- **Show a ghost marker on time bars** — FEATURE — value 3 — effort M — risk low — category: live tree
  Why: The live tree already draws time bars per call and subagent. Add a faint tick at the median time for the same task kind and size, so the user sees whether a task is ahead or behind. Assumption: durations per kind are in the history.
  Done when: a running task's bar shows a marker at the historical median, and with fewer than 5 samples the marker is hidden.

- **Badge the README with the live first-time-pass rate** — FEATURE — value 3 — effort S — risk low — category: sharing
  Why: The README already carries a tests badge, and the held-rate scorecard (T-0867) is deferred because it lacks a corpus. A small static SVG generated from the project's own closed tasks needs no corpus, and users show it off.
  Done when: `fm badge` writes an SVG with the pass percentage and task count from state, and the number matches `fm` stats on a fixture.

- **Peek a task from any id in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: Ids like T-1994 appear everywhere and mean nothing until opened. Hover or focus shows a card with the title, DONE-WHEN, proof marks and files. It is keyboard reachable.
  Done when: hovering or focusing an id in the web UI shows the card within 150 ms, and Esc closes it.

- **Tint each project's accent from its name** — FEATURE — value 2 — effort S — risk low — category: pane
  Why: The pane's colours are fixed (and T-1217 shows pane colour is already a fight). A stable per-project hue on the work bar and border tells terminals apart at a glance. Assumption: the user runs several projects.
  Done when: two project names yield different accent hues, the same name always yields the same one, and the contrast ratio stays at or above 4.5:1.

- **Mark round-number milestones** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: The task counter just passed T-2000. One quiet line at T-2000 or at the 100th first-time pass ("T-2000: 1,2xx proven, 83% first try") costs almost nothing and gets screenshotted.
  Done when: closing a task whose id or pass count crosses a round number prints the line once, and a test confirms it prints only once.

- **Dim everything but the focused task's branch** — FEATURE — value 2 — effort S — risk low — category: live tree
  Why: With several tasks and subagents in the tree, it is hard to follow the one that matters. Dim the unfocused branches to 50% so the focused task's calls stand out.
  Done when: with two tasks active, only the focused task's rows render at full intensity, and `fm focus` switches which ones.

- **Wild: Let a newcomer try to fool Foreman in a playground** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: T-0862 and T-0863 (tour, start ladder) are deferred for lack of evidence. A game is more fun than a tour. `fm playground` makes a throwaway repo with a planted bug, and the player tries to close a task without a real proof, run a guarded command, or drift out of scope. Foreman refuses and explains each attempt, and a tally counts the blocks. (wild)
  Done when: a scripted attempt of each of the three kinds is refused in the throwaway repo, and the tally shows 3 blocks.

- **Wild: Ask one assumption-breaking question with `fm duck`** — FEATURE — value 3 — effort S — risk low — category: thinking
  Why: Many of the user's tasks start as a hunch ("a captured title is cut mid-word"). `fm duck "<hunch>"` answers with the single question that would most likely prove the hunch wrong, and no plan, so the user finds the false premise before capturing a task. (wild)
  Done when: given a hunch, it outputs exactly one question ending in "?", and it makes no file edits or task writes.

- **Wild: Follow the agent's reading in the web UI like a presence cursor** — FEATURE — value 3 — effort L — risk med — category: web UI
  Why: The web UI shows state but not attention. A file pane that scrolls to the lines the agent is reading or editing, with a soft highlight, makes a long autonomous round feel like pair programming. Assumption: tool-call events carry paths and line ranges. (wild)
  Done when: in a recorded session, the pane scrolls to the edited range within 1 s of each Edit event, and it stays still while "follow" is off.
