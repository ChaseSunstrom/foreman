# Brainstorm — lens: delight

- **Greet by project, not by banner** — FEATURE — value 4 — effort S — risk low — category: home screen
  Why: the user wants `fm code` to open like claude does, and the nixie run failed because nothing said where it was running. assumption: the cwd's Foreman state is cheap to read at launch.
  Done when: `fm code` in a project prints a first frame whose top line names the project folder, its runner, and its queue/active counts, and a test pins the line in a golden frame.

- **Show the first-call wait as a named countdown** — FEATURE — value 5 — effort M — risk low — category: silence
  Why: "it just isn't doing anything" with 66k–133k input tokens per planner call. A quiet minute with no label reads as broken. The wait could say "Claude is reading 14 plugins, usually 40s" from the runner's measured startup history.
  Done when: a fake runner that stays quiet for 30s makes Activity show a line with elapsed time, a typical-time estimate and what it is waiting on, updated at least once a second.

- **Say "done" in one sentence a person would say** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the receipt and verdict cards are pictorial, but the user's own phrasing ("show better examples", "do anything with it") suggests plain outcomes matter. assumption: one generated line from the proved criteria is enough.
  Done when: a closed run ends with one plain line like "Fixed the parser; 3 checks pass, 1 was failing before", built from the task's criteria with no model call, and a test checks it against a fixture run.

- **Offer the next request as a ghost placeholder** — FEATURE — value 3 — effort M — risk low — category: input
  Why: the input box starts empty; the deferred `what should I work on?` ideas are about the landing answer, not the typing moment. The box could hold a dim suggestion (top queued task, or the blocked one) that Tab accepts.
  Done when: with a queued task, the empty request box shows its title dimmed, Tab fills it, and Enter runs it via `--task ID`; with an empty queue it shows nothing.

- **Let a failed guard refusal teach once, then go quiet** — FEATURE — value 3 — effort S — risk low — category: microcopy
  Why: guard hints keep being lengthened (T-1298, T-1318), so the first time is wordy. Showing the full explanation only the first time per verdict kind, then a short form with `?` to expand, keeps the screen calm.
  Done when: the same refusal kind shown twice in one config home renders the long text the first time and under 60 characters the second, verified from a stored seen-set.

- **Remember a run's last words when the terminal closes** — FIX — value 4 — effort S — risk low — category: continuity
  Why: orphaned planners and quit-without-trace were the user's actual complaint. On the next launch in that folder a single line could say "Last time you closed this mid-plan (2 min in); resume or start fresh?".
  Done when: killing a run mid-plan and relaunching shows that line, `r` resumes from the journal and `n` clears it, tested with a scripted kill.

- **Give every runner a one-line "hello" on selection** — FEATURE — value 3 — effort S — risk low — category: runners
  Why: picking a runner in `m` gives no feedback that it works. A 2-second probe that prints "claude 2.1.301 · ready · ~45s startup" turns a blind choice into a confirmed one.
  Done when: choosing a runner in the picker shows a ready/failed line with version and measured startup within 5s, and a missing binary shows its install hint instead.

- **Wild: Let the home screen keep a tiny desk plant per project** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Projects you neglect wilt a little, closed tasks make it grow. It turns a fleet view into something you glance at fondly. assumption: held-rate and last-activity time are already derivable.
  Done when: each project card shows a glyph whose stage is a pure function of days since last close and proved-task count, and a golden frame shows three different stages.

- **Wild: Hum a different bell per outcome** — FEATURE — value 2 — effort S — risk low — category: sound
  Why: wild. Optional, off by default. One BEL for needs-you, two for closed-proved, none otherwise, so you can walk away from a long run and know the result by ear.
  Done when: with `bell = on`, a fake run that closes green emits exactly two BEL bytes and a blocked one emits one, and with it off, zero.

- **Wild: Print a postcard to the shell when you quit** — FEATURE — value 3 — effort S — risk low — category: farewell
  Why: wild. On exit, leave a compact 6-line text card in scrollback (tasks closed, time, cost, what's next) so the session leaves a trace after the alternate screen disappears.
  Done when: quitting the TUI after one closed task leaves a card in the normal terminal scrollback with those four facts, and `--no-card` suppresses it.

- **Rename the thing to what the user typed** — FEATURE — value 3 — effort S — risk low — category: echo
  Why: the user's words are verbatim in the intake notes; the run shows the harness's title. Showing "you asked: …" beside the title proves the words landed, and a mismatch is visible right away.
  Done when: the run header shows the verbatim request on a second line, truncated with an ellipsis, and the run log stores it unmodified.

- **Make the wait for a worker feel like a workshop, not a spinner** — FEATURE — value 3 — effort M — risk med — category: motion
  Why: long worker turns are the dull stretch where the user decides it's broken. Each streamed event from claude/codex (a file read, an edit, a test run) could tick a distinct small glyph into a row, so activity looks like work being done.
  Done when: replaying a recorded stream-json fixture adds one glyph per tool call, by kind, to the row, and a quiet stream adds none and shows the heartbeat instead.
