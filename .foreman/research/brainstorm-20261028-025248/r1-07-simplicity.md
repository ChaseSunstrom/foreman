# Brainstorm — lens: simplicity

- **Delete the usage-limit retry watchdog and let `fm run --wait` handle limits** — CLEAN — value 4 — effort S — risk low — category: dead code
  Why: the user steered away from the RETRY_WATCHDOG step because `fm run` already waits out USAGE_LIMIT and fails over, so the watchdog duplicates that path.
  Done when: no retry-watchdog code path remains, and a test shows a usage-limited run waiting through `fm run --wait` and then failing over.

- **Use one argument grammar for every verb, with flags declared once** — CLEAN — value 4 — effort M — risk low — category: parsing
  Why: `fm dojo` shares help position 306 with another command, and a bespoke `test_followups` parser exists for split rows, which points to duplicated parsing and hand-set positions.
  Done when: every verb's flags come from one table, `test_help` passes with no hand-assigned positions, and the followups test uses the shared parser.

- **Make `fm done` the one closing verb, with prove and finish as its steps** — FEATURE — value 4 — effort M — risk med — category: task lifecycle
  Why: closing a task takes separate prove, finish and close steps. Assumption: users close tasks through one path most of the time.
  Done when: `fm done <id>` on a task with a passing proof closes it and prints the receipt, and the old verbs still work as aliases.

- **Drop the experimental macOS job from the path that can cancel main's tests** — FIX — value 4 — effort S — risk low — category: CI
  Why: the experimental macOS job hit its 35-minute limit and cancelled main's newest tests run (T-1809), which produced a false red on main.
  Done when: a cancelled optional job no longer cancels the required tests run, and main's required check reports the tests result.

- **Replace the 10-minute detached sweep with checks on the commit that needs them** — PERFORMANCE — value 3 — effort M — risk med — category: background work
  Why: session start reads caches that a detached sweep refreshes every 10 minutes, so a background process runs even when no one is watching.
  Done when: with no session open for 30 minutes, no sweep process is running, and the next session start still shows CI status.

- **Keep one rendering model for the stage rail and band across web, pane and desk** — CLEAN — value 3 — effort M — risk low — category: duplication
  Why: the pane and the web UI each render the stage rail and band, and T-0166 notes the band and pane are tangled inside `register.tsx`.
  Done when: one module exports the rail model, both surfaces import it, and the snapshot tests for both pass.

- **Offer a two-rule mode: no edit without a failing test, no close without a passing one** — FEATURE — value 3 — effort S — risk low — category: simplicity (wild)
  Why: (wild) the whole discipline layer could reduce to two checks a new user can hold in their head, with the rest switched off.
  Done when: with the mode on, the guard refuses an edit with no prior failing test and a close with no passing proof, and `fm doctor` lists only those two checks.

- **Drop the terminal pane and let scrollback carry the state** — FEATURE — value 2 — effort M — risk high — category: interface (wild)
  Why: (wild) assumption: a returning user only needs the state printed at the end of each command, which would remove the pane and its maintenance cost.
  Done when: `fm status` alone answers the three questions a returning user asks (what ran, what needs them, what's next) in under 24 lines.

- **Make a git commit subject a queue entry** — FEATURE — value 2 — effort M — risk med — category: intake (wild)
  Why: (wild) a commit like `todo: ...` already captures intent in the repo's own history, so a second queue store would be redundant.
  Done when: `git commit --allow-empty -m "todo: <text>"` adds a queued task that appears in `fm status` with the commit as its source.
