# Brainstorm — lens: invented: the session that can read its own map

- **Split MASTER.md into a map plus anchored section files** — CLEAN — value 5 — effort M — risk low — category: docs/context
  Why: MASTER.md is 75,758 tokens, so Read refuses it. A session can't read the project's own manual. The new MASTER.md would be an index of at most 3k tokens, with one file per section and each section under 8k tokens. Verbs would be generated from the verb table so the reference part can't grow by hand.
  Done when: `Read MASTER.md` succeeds, every linked section file also reads whole, and a test fails if either limit is crossed.

- **Find who registers SessionStart twice** — FIX — value 5 — effort S — risk low — category: hooks
  Why: the pack says 2,733 characters are injected twice. Assumption: the cause is the thin `foreman` and `foreman-ui` shim plugins plus the `sampo` plugins all registering the same hooks. `fm doctor` would list each hook event with the plugin that registers it, and the install would register only one.
  Done when: a fresh install with the shims shows exactly one registration per event in `doctor`, and the SessionStart payload appears once in a recorded session.

- **Make SessionStart source-aware** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: T-2900 shows the hook already tells `startup`, `resume`, `clear` and `compact` apart. A resumed transcript already contains the earlier injection. Resume would inject a one-line pointer, while `clear` and `compact` would inject in full because they lose it.
  Done when: replaying all four sources through the hook gives full text only for startup, clear and compact, and at most 120 characters for resume.

- **Replace the injected block with a pointer to `sampo map`** — FEATURE — value 4 — effort M — risk med — category: context/introspection
  Why: the session can't see what it was told, and the injection grows by hand. Start would inject one line, and `sampo map` would print the channels with their bytes, hook milliseconds from `bench_hooks`, the guard-rule count and hash, and the state size. A session that wants more reads it.
  Done when: SessionStart injection is under 400 characters, `sampo map --json` lists every injection channel with its bytes, and a cold child using only that output answers 5 "what were you told?" questions correctly.

- **Guide any oversized Read with an outline** — FEATURE — value 4 — effort M — risk med — category: usability
  Why: Read refusing MASTER.md is the symptom, and other big files will hit it too. A PreToolUse hint, or a `sampo outline <path>` verb the refusal message names, would show headings with line ranges and token costs and suggest the ranges that match the open task's words. Whether a hook can intercept Read this way is an assumption to check first.
  Done when: reading a file over the Read limit gives an outline and an offset/limit suggestion within one tool round-trip, and the hook adds under 50 ms.

- **Check the guard is intact at every start** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the mission says "guard intact". Hash the guard rule set together with the installed hook registrations (including the shim duplicates) and compare against a hash sealed at install. Say nothing when they match and print one loud line when they don't.
  Done when: deleting a Ward hook, or editing one rule in a scratch home, makes the next SessionStart print the deviation. An unmodified install prints nothing.

- **Archive old ledger segments behind an index** — PERFORMANCE — value 4 — effort L — risk med — category: state
  Why: project state is 2.4 GB. First run `sampo state du --by-writer` to find the heavy writers (assumption: transcript copies and hook logs dominate). Then compress segments older than 14 days into archives with a sidecar index that the windowed readers consult, with a restore verb.
  Done when: state on this machine drops by at least 60%, and `fm doctor` and the ledger readers return identical output before and after, on a copy of the real state.

- **Let the session read its own context gauge** — FEATURE — value 3 — effort M — risk low — category: introspection
  Why: sessions can't see how much of their window Sampo uses. The verb would parse the session's own transcript for injected, hook-output and skill bytes, and print the Sampo share and a "compact now?" verdict. The per-turn burden of 48–76 characters would become one line in it.
  Done when: `sampo ctx` on a recorded transcript matches a hand count of injected characters within 2%.

- **Wild: Let a session mute a channel for itself** — FEATURE — value 3 — effort S — risk low — category: context
  Why: assumption: sessions often ignore some injections. `sampo mute <channel>` would silence it for the rest of the session, and the votes would be tallied across sessions. A channel muted in at least 5 of 6 sessions becomes a subtraction task, a cheap way to find waste.
  Done when: a muted channel stops appearing for that session only, and `sampo map` shows the vote counts.

- **Wild: Record a trail of every Read and leave it for the next session** — FEATURE — value 3 — effort M — risk low — category: introspection
  Why: sessions re-read the same large files. A trail file would store file, byte range and token cost per Read. When the next session reads a big file again, the hint would offer only the ranges the previous session needed. It stays local and is capped at 200 lines.
  Done when: a second session that reads a trailed file is offered the earlier ranges, and the trail never exceeds its cap.

- **Wild: Show the user the same one-line map as the status line** — DELIGHT — value 3 — effort S — risk low — category: ui
  Why: if the pointer line, the status line and the pane header come from one `sampo map --one-line` source, the user and the agent see the same facts: injected characters, hook milliseconds, guard hash, state size. A mismatch is visible at a glance.
  Done when: a test fails if the status line and the injected pointer differ for the same session.

- **Register every lean number with the command that reproduces it** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: the mission says "every claim checked on the machine". A table of the 2,733 characters, 75,758 tokens, 2.4 GB and 48–76 figures, each with a one-line shell reproducer and a ceiling, would be run by `doctor`. It would fail on drift, so the next Mission's baseline is mechanical.
  Done when: `doctor` prints each lean number with its current value, and raising any past its ceiling turns that row red.

Next question: Which of the 2.4 GB is read by any verb or hook in the last 30 days, and does anything fail if it moves to an indexed archive?
Next question: Does a session that gets only a pointer line plus `sampo map` do as well on held-out tasks as one that gets the full 2,733 characters?
