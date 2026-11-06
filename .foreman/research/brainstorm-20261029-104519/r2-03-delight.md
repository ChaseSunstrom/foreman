# Brainstorm — lens: delight

- **Print a one-line "held" receipt when a task closes** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the user's requests are a stream of "Ship Tn to main" and fix closes, and nothing shows the payoff at the end; assumption: close output today is plain status text.
  Done when: `fm task done` prints one line with the task id, the proof command that failed-then-passed, files touched and elapsed time, and a test asserts the line format.

- **Name the next move after every command** — FEATURE — value 4 — effort S — risk low — category: guidance
  Why: many recent fixes are dead-end refusals (docs-impact blocker, "no test matches", core-integrity warning), each patched one at a time, so a refusal that points forward is what the user keeps asking for.
  Done when: every refusal from `fm task`, `run.py` and `fm doctor` ends with a "Try:" line, and a test fails if a new refusal lacks one.

- **Suggest the near-miss on every "not found"** — FEATURE — value 4 — effort S — risk low — category: errors
  Why: T-1995 added path suggestions and the latest ask (CoreIntegrity vs core_integrity) added test-id suggestions; each reimplemented did-you-mean separately.
  Done when: one `fmsuggest.closest(name, candidates)` helper backs the docs path, test id, task id and subcommand errors, with one shared test.

- **Draw the stage rail as a progress bar with a finish flourish** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the demo shows the stage rail and steps; the rail already holds state, so it can animate between stages and settle with a brief closing mark when the task closes. Assumption: the pane can repaint at low frequency.
  Done when: advancing a task's stage animates one transition in the pane, and the animation is skipped when `NO_MOTION` or a non-tty is set.

- **Make task ids clickable everywhere** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: ids like T-1998 appear in commits, the pane and the tree, yet need typing to inspect (T-0796 already lists clickable ids).
  Done when: ids in terminal output are OSC 8 links to `fm task show`, or to the web UI task page, and plain text when the terminal lacks hyperlink support.

- **Show a first-time-pass streak** — FEATURE — value 3 — effort S — risk low — category: motivation
  Why: lessons already track first-time passes (T-0217); a quiet "7 closed without rework" line rewards the discipline Foreman exists to build. Assumption: the data is stored per task.
  Done when: the pane and the close receipt show the streak, and it resets when a task is reopened or fails a gate.

- **Let the guard hook block in a dry one-liner that names the fix** — FEATURE — value 3 — effort S — risk low — category: voice
  Why: blocks are where users feel Foreman most, and a block that says what it saw and the safe alternative reads as a collaborator, not a wall. Assumption: the block text is currently terse.
  Done when: each guard rule has a "why" and a "instead" string, and the block output shows both.

- **Say what a stopped loop learned** — FEATURE — value 3 — effort S — risk low — category: loop
  Why: the loop ends as "2 dry rounds" (T-1987 fixed the miscounting); a user then knows nothing about what was tried. 
  Done when: the loop's stop message lists rounds run, ideas kept versus dropped, and the one thing it would try next.

- **Give the pane an idle screen showing today's landed diff** — FEATURE — value 2 — effort M — risk low — category: pane
  Why: the pane idles blank between tasks, wasting the surface the user stares at; the Today charts already exist.
  Done when: with no active task the pane shows the last closed task's id, title and diffstat, and a test covers the empty case with no history.

- **Render a quiet completion tick when a long gate run ends** — FEATURE — value 2 — effort S — risk low — category: sound and notice
  Why: full gates and `fm ship` test runs are long, and the user waits on them; assumption: they look away.
  Done when: a long run (over a configurable threshold) emits a terminal bell or desktop notification on finish, off by default and settable in config.

- **Wild: Play back a closed task as a 20-second scrubbable timeline** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: tasks already record plan, edits, proof and close; a replay is the shareable thing people show others. Assumption: events are timestamped.
  Done when: `fm task replay T-n` writes a single HTML file that steps through plan, edits, failing proof and passing proof, and opens offline.

- **Wild: Give `fm doctor` a mood and a one-word verdict** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: doctor output is checked constantly; a leading verdict ("steady", "itchy: 2 warnings", "bleeding: gate red") makes it glanceable.
  Done when: doctor's first line is one of a fixed set of verdicts derived from its results, with a test per verdict.

- **Wild: Hand out a weekly "Foreman wrapped" card** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: the demo SVG shows people value a visual; a generated card with tasks closed, proofs that failed first, blocks that saved a command, and time saved is what users post. Assumption: history is queryable.
  Done when: `fm wrapped` writes a local SVG for the last 7 days from task records and sends nothing anywhere.

- **Wild: Let the demo hero rebuild itself from a real session** — FEATURE — value 2 — effort L — risk med — category: demo
  Why: demo/live.svg is recorded by hand against an older state, and the README says it is a real session; regenerating it from a recorded session keeps it from drifting.
  Done when: one command records a scripted session into demo/live.svg and demo/live.mp4, and CI flags the demo when the UI changes.
