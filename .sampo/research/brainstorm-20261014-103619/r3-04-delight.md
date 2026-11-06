# Brainstorm — lens: delight

- **Drive the spinner from the current step** — FEATURE — value 3 — effort S — risk low — category: terminal polish
  Why: assumption: Claude Code's spinner verbs and tips are settable per session, and Foreman writes settings today. The user's complaints about steps not updating (T-0759) and idling (T-0758) are about visible state. The spinner is the one line they always look at.
  Done when: while step 3 of T-0754 runs, the spinner reads "Verifying T-0754 · 3/5" and not a generic verb. Tips cycle one-line lessons Foreman has recorded, and the spinner reverts when the queue is empty.

- **Show step progress in the terminal's own progress bar** — FEATURE — value 3 — effort S — risk low — category: terminal polish
  Why: assumption: the terminal supports the OSC 9;4 progress sequence. The band and pane only help when the Foreman UI is open. A native tab or taskbar bar shows progress from another window and works in plain terminals.
  Done when: a 5-step plan at step 3 draws 60% in a supporting terminal. The bar turns to the error state on a red gate and clears on done, and unsupported terminals receive nothing.

- **Make every T-id and file:line a clickable link** — FEATURE — value 3 — effort S — risk low — category: terminal polish
  Why: the user's own words are full of T-ids, and the close-outs name files. `fm` output and hook messages currently print them as plain text. OSC 8 links would jump to the editor, or to the task page if a cockpit exists.
  Done when: in a supporting terminal, `fm task show` prints T-0754 and `foo.py:42` as links that open the right target. With `NO_COLOR`, or when not on a tty, the output is byte-identical to today.

- **Ship a one-chord keymap for Foreman actions** — FEATURE — value 3 — effort S — risk low — category: ergonomics
  Why: assumption: Claude Code reads a user keybindings file. Pause, capture-this-thought and what's-next are the actions the user repeats, and each costs a typed command. The installer already wires `~/.claude`.
  Done when: after install, a documented chord inserts "capture:" into the prompt box, a second pauses or resumes the drive, and `fm doctor` reports the bindings active or conflicting.

- **Give each role a colour and use it everywhere** — FEATURE — value 2 — effort S — risk low — category: visual identity
  Why: the six subagents and the lanes show up in the native agent UI, the band, the pane and transcripts as plain names. Agent frontmatter can carry a colour. One palette per role would let the user read a busy fleet at a glance.
  Done when: `scout`, `recon`, `reviewer`, `debugger`, `reproducer` and `builder` each declare a colour in frontmatter, and the band and pane use the same hues. A test fails if the two palettes drift.

- **Mark each step start so the rewind picker reads like the plan** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: assumption: the rewind picker lists conversation turns, so a Foreman-written step marker would label a restore point. The user asked about reverting whole operations (T-0757). Native rewind is the cheapest way to get a per-step undo.
  Done when: after a 4-step task the rewind list shows "step 2: wire the guard" and similar entries. Rewinding to one, then `fm resume`, resumes at that step with the pointer corrected.

- **Hold a queue-zero moment when the queue empties** — FEATURE — value 3 — effort S — risk low — category: ritual
  Why: the user keeps asking that Foreman never sit idle, but it should also be unmistakable when there is truly nothing left. Today that probably looks the same as a stall. A distinct end state tells the user it is safe to walk away.
  Done when: emptying the queue prints one line (counts shipped, deferred and blocked, plus the best next suggestion), the band shows a calm "clear" state, and it fires once per emptying, not per turn.

- **Offer one gear lever for model, effort, fast mode and rigor** — FEATURE — value 4 — effort M — risk med — category: control
  Why: the user said "smarter, faster, better" and asked whether Foreman can spawn lower-model agents (T-0755). These are separate knobs today. One word per task, such as `@gear 2`, could set Agent model, effort, fast mode and review depth together.
  Done when: "@gear 1" on a brief makes its lanes spawn on haiku at low effort with no reviewer fan-out, and "@gear 5" does the opposite. `fm task show` prints the gear and the knobs it set.

- **Wild: Run a Foreman Radio ticker pane** — FEATURE — value 2 — effort M — risk low — category: ambient
  Why: assumption: Monitor can stream a background command. A second tmux pane would tail the ledger as timestamped one-liners ("14:02 scout found 3 callers", "14:05 gate green"). It would feel like a ship's log, and it needs no cockpit page.
  Done when: `fm radio` renders new ledger events within 2 seconds, collapses repeats, is read-only, and exits cleanly with the session.

- **Wild: Pre-fill the user's likely next message as ghost text** — FEATURE — value 4 — effort L — risk med — category: prediction
  Why: assumption: Claude Code can show a suggested next prompt that Tab accepts, and the host may not let a plugin set it. Foreman already tracks what the user usually asks next (FIX, then Release) and could offer "Release 1.2.28 …" after a green close-out. This is a prediction made visible and costs one keystroke to accept.
  Done when: after a task closes, a plausible next message appears as accept-by-Tab text. Replay over past inbox history shows it matches at a rate that is reported, and with the feature off nothing appears.

- **Wild: Keep one live-updating push notification on the phone** — FEATURE — value 4 — effort M — risk med — category: mobile
  Why: assumption: a repeated PushNotification with the same tag can replace the previous one. The user wants to leave Foreman running without a stream of pings. A single lock-screen card reading "T-0754 · step 3/5 · 2 queued" that edits itself would show state with zero noise.
  Done when: over one task the phone shows one notification whose text updates per step, and a blocking ask raises it with sound. If replace-by-tag is unsupported, the idea degrades to no notification and says so in `fm doctor`.

- **Wild: Open each session with a "previously on…" recap** — FEATURE — value 3 — effort S — risk low — category: ritual
  Why: the greeting ideas so far are one-liners. A three-line TV-style recap ("Previously: the guard learned about pipes; the check track record was fixed; 1.2.27 shipped. Today: T-0758") would orient the user after a long gap. The data already sits in the ledger.
  Done when: SessionStart prints at most 3 lines built only from ledger events, each citing a T-id. It adds under 50 ms to the hook latency bench, and a session with no new events prints nothing.
