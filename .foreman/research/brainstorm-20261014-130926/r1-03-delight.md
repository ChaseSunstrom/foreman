# Brainstorm — lens: delight

- **Preview compact output on your own worst output before asking for a yes** — FEATURE — value 4 — effort S — risk low — category: delight/tokens
  Why: compact output is built and measured (~1.04M tokens/30 days) but off until the user says yes, and a bare percentage doesn't persuade. Assumption: `state/outputs` or the 30-day transcripts still hold a real large output to use.
  Done when: `fm compact try` picks the user's largest recent Bash output and prints the before and after (chars, head, failure lines, tail) without enabling anything. A test asserts the preview matches what the PostToolUse rewrite would send.

- **Add `fm out` and put its exact command in every compact stub** — FEATURE — value 4 — effort S — risk low — category: discoverability
  Why: compact output writes the full text to `state/outputs`, but a model or user seeing a trimmed stub has no obvious next step. Assumption: no retrieval command exists yet.
  Done when: a compacted result ends with `full: fm out 7`. `fm out 7 --grep ERR` and `--tail 50` return slices of the saved file, and an unknown id says what ids exist.

- **Generate the "Round N shipped" section from the ledger** — FEATURE — value 5 — effort M — risk low — category: recursion
  Why: the user steered that "recursively improve" means finishing, reviewing, brainstorming and repeating. The round-1 summary (shipped items, deferred clusters with reasons, known gaps) was written by hand for this pack.
  Done when: `fm round summary` emits tasks closed since the last round marker with their one-line outcomes, deferred clusters with the recorded reason, and known gaps taken from tasks closed with caveats. Output is identical on a rerun.

- **Auto-tick the board from observed use** — FEATURE — value 4 — effort M — risk med — category: feedback
  Why: "nobody has ticked the board yet", so round 2 has no signal on what round 1 earned. The use is observable: the monitor delivered mail, the push fired, compact saved tokens, the title changed.
  Done when: `fm page` shows each round-1 item with a ✓ and its evidence ("mail delivered 6×") or a dim "unused in 3 sessions". Items with no signal stay unticked, never guessed.

- **Confirm the mail monitor armed, with a tiny dot and a first-delivery line** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the pack says arming in a live interactive session is unverified, and monitors start only in new sessions. A silent feature feels broken.
  Done when: the statusline or SessionStart shows `📬 armed` once the watcher heartbeat is fresh and `📬 off (restart session)` otherwise. The first delivered mail adds one line, "first mail via monitor", logged once per session.

- **Show a lit/locked feature map in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: native adoption
  Why: doctor already checks each CC feature Foreman uses against the installed version, but the output is pass/fail. A map that says what you are missing and why you'd want it turns a check into an invitation.
  Done when: `fm doctor --features` prints each feature as ✓ lit or 🔒 "unlocks at 2.1.xxx: <one-line benefit>", and its test fixes two fake versions to check both states.

- **Make sessionTitle a return card on resume** — FEATURE — value 3 — effort S — risk low — category: return
  Why: round 1 titles sessions after the active task, but `sessionTitle` also applies on resume. After a long absence the resume picker is the first thing the user sees.
  Done when: a SessionStart after more than 4 hours away sets a title like `T-0818 · 3 shipped · 1 needs you`, and a fresh session keeps the plain task title.

- **Show the longest unattended stretch in the greeting** — FEATURE — value 3 — effort S — risk low — category: pride
  Why: the mail monitor and Stop-hook push now keep runs going without the user. Liveness has no visible payoff, and the heartbeat already carries the data. Assumption: the heartbeat timestamps are persisted.
  Done when: after a run of 2 hours or more with the queue moving and no user input, the next greeting says "ran 6h12 unattended, 9 tasks closed, nothing waiting". A run with an open ask never counts as unattended.

- **Coach shorter forms from the user's own `fm` history** — FEATURE — value 2 — effort S — risk low — category: ergonomics
  Why: the surface has about 45 subcommands. Assumption: command history is available from the ledger or the shell.
  Done when: after the same long form is typed 10 or more times, `fm` prints a one-time tip with the shorter equivalent or a suggested alias, and the tip never repeats once dismissed.

- **Wild: Draw the task page like a clipboard that ticks itself** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: `fm page` produces one self-contained HTML file, so a CSS-only SVG stroke animation costs no dependency. Today it is a static table.
  Done when: opening the page draws a hand-style ✓ for each closed task, honors `prefers-reduced-motion` by rendering them instantly, and the file stays under its size cap with no external requests.

- **Wild: Have Round 3 waiting at breakfast** — FEATURE — value 4 — effort L — risk med — category: recursion (wild)
  Why: the user wants repeated rounds. Idle night time plus the generated round summary and auto-ticks could produce the next round's context pack. Assumption: it respects the per-child USD cap.
  Done when: an opt-in nightly routine writes `round-N+1-pack.md` (shipped, ticks, known gaps, don't-repropose list) within a stated budget and spawns no brainstorm children, so the user starts round 3 with one command.

- **Wild: Celebrate subtraction with a net-lines-deleted flourish** — FEATURE — value 2 — effort S — risk low — category: simplicity (wild)
  Why: the open backlog has CLEAN and slim-Foreman items, and nothing in the close-out rewards deleting. Assumption: tier-drift already counts real diff lines, so the number is available.
  Done when: closing a CLEAN task with more lines removed than added prints "−412 lines, +38. Lighter." and the line appears only when the diff is net negative.

- **Wild: Turn a round into a one-minute "what got better" strip** — FEATURE — value 3 — effort M — risk low — category: proof (wild)
  Why: round 1 claims speed and token wins (bench p50, ~1.04M tokens/30 days) that live only in prose. Assumption: `plugin/tests/bench_hooks.py` outputs can be stored per round.
  Done when: `fm page --round 1` shows before and after numbers for hook p50 and compact-output savings. A metric with no stored baseline is shown as "unmeasured", not omitted.
