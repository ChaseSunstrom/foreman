# Brainstorm — lens: context per turn

- **Gate turn type before injecting** — FEATURE — value 4 — effort S — risk low — category: per-turn context
  Why: assumption: per-turn text (48 to 76 chars) goes out even on "yes", "continue" or a one-word reply, where it can't change the next action.
  Done when: a replay of 20 recorded short-reply prompts shows zero per-turn bytes injected, while a prompt naming a task, verb or file still gets its line.

- **Steer the compactor with PreCompact instructions** — FEATURE — value 4 — effort M — risk med — category: compaction
  Why: the pack covers SessionStart dedupe and source-awareness, but nothing about what survives compaction. A guard card re-injected at every start is wasteful if the summary keeps it.
  Done when: after a forced compaction, a scratch session's summary still holds the guard clause, the open task id and the stage, and `compact`-source SessionStart emits 0 extra chars.

- **Census the tool-result channel by verb** — FIX — value 4 — effort S — risk low — category: measurement
  Why: SessionStart and per-turn text are measured, but `fm next`, `fm map` and `fm doctor` output enters context through the agent's own Bash calls. Assumption: it dwarfs the hook text.
  Done when: one command ranks verbs by bytes returned into transcripts over the last 50 sessions, with the top five listed.

- **Fail the repo on any doc over a Read-safe size** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: MASTER.md at 75,758 tokens is refused by Read, and it's the only offender found because nobody scanned the rest.
  Done when: a ship-gate test lists every tracked text file above 20k tokens and fails on any not in a recorded allowlist, with MASTER.md as the first entry to clear.

- **Replace the per-turn sentence with a ≤12-character state code** — PERFORMANCE — value 3 — effort S — risk med — category: per-turn context
  Why: 48 to 76 chars each turn is mostly prose restating state. A code like `S3·T2851·$41` with the legend given once at start carries the same facts.
  Done when: the per-turn line is ≤12 chars in the steady state, and a cold-child quiz decodes stage, task and budget correctly from three sample lines plus the legend.

- **Give subagents a role-sized injection** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: assumption: each scout, builder or designer subagent inherits the full SessionStart block (2,733 chars, twice). Long-lived subagents multiply that cost across the drive's many spawns.
  Done when: a SubagentStart hook emits ≤400 chars per role, the guard line is still present in each, and the transcript of a spawned scout shows no second copy.

- **Measure survival of injected facts across turns** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: nobody knows whether text injected at start is still in the model's working context by turn 30. If it isn't, re-injecting beats a longer first block.
  Done when: a probe asks a scratch session for the guard rule at turns 1, 10 and 30, and a table shows recall per turn per injected line.

- **Write the model's own wish-list note at session close** — FEATURE — value 3 — effort S — risk low — category: injection selection
  Why: the pack's ideas rank injected lines by outcome change but don't ask the agent what it wished it had known.
  Done when: Stop appends ≤200 chars "wished I'd known" to a local file, and the next start's card orders its lines by how often each was named.

- **Wild: Run a "first prompt, 300 characters" week** — FEATURE — value 3 — effort S — risk med — category: lean — wild
  Why: assumption: most of the 2,733 chars is never acted on. A hard 300-char start card, with everything else pulled through `fm doc <name>`, tests this directly.
  Done when: one lane runs a week of tasks on the 300-char card and `fm outcomes` shows its first-time pass rate within noise of the full card.

- **Wild: Put the context diet on a nightly receipt, bisected** — FIX — value 3 — effort M — risk low — category: measurement — wild
  Why: each added line costs a few chars and nobody sees the drift. Bisecting a growth jump against git history names the commit that added it.
  Done when: a nightly job writes total injected chars per event and, on a rise over 10%, names the commit that caused it.

- **Wild: Let the agent mute a channel for its own session** — FEATURE — value 3 — effort M — risk high — category: control — wild
  Why: the agent knows when a reminder is noise. A `fm mute <channel>` scoped to the session id lets it say so, and the mute is logged as evidence for later pruning.
  Done when: muting a non-guard channel stops its output for that session only, muting the guard channel is refused, and the log shows who muted what.

- **Hash-stamp repeated reminders instead of repeating them** — PERFORMANCE — value 3 — effort S — risk low — category: per-turn context
  Why: a reminder that hasn't changed since turn 1 can be a 6-char stamp pointing at the copy already in context. This is distinct from delta emission in that it needs no state beyond one hash.
  Done when: a 50-turn replay shows each unchanged reminder appearing once in full and thereafter only as a stamp, with total reminder bytes down at least 60%.

Next question: Does the agent actually act differently when the injected text is shorter, and which first-minute behaviours would show it before the exam does?
Next question: Which injected lines does the guard depend on to hold in bypass mode, so a cut can't silently weaken it?
