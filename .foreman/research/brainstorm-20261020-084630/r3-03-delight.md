# Brainstorm — lens: delight

- **Ask the terminal for its real colours** — FIX — value 4 — effort S — risk low — category: pane
  Why: T-1217 shows Claude Code paints the docked pane #262626 and the pane doesn't match. Querying OSC 11/10/4 for the actual background and foreground, then deriving the palette, fixes that case and every other terminal theme. It falls back to the current palette when there is no reply.
  Done when: a test feeding a fake OSC 11 reply of `rgb:1e1e/1e1e/2e2e` renders pane cells whose background equals that value, and a run with no reply renders the existing palette.

- **Pin a thought that survives compaction** — FEATURE — value 5 — effort S — risk low — category: long sessions
  Why: the user keeps asking for long runs that stay on track after compactions, and T-1231 already carries the request text across them. A one-line `fm pin "use tabs, never touch vendor/"` has no such path. The pane shows it as a small pin, and the compaction note repeats it verbatim.
  Done when: after a forced compaction in the long-session harness, the pinned line appears in the post-compaction context. `fm pin --rm` removes it, and a pin older than the session is not carried over.

- **Make every number on the site a link to its raw run** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: T-1246 says the site's prose figures are hard-coded, and the user's constraint is that every claim must be measured. Hovering or tapping a figure shows its model, run count, date, Claude Code version and a link to the results file. The build fails on a bare figure.
  Done when: the site build fails on an unannotated figure in the Benchmarks prose, and a sample figure opens a popover naming its results file.

- **Copy any suggested command with one key** — FEATURE — value 4 — effort S — risk low — category: pane
  Why: the pane and refusals print many `fm ...` commands, and copying them from a docked pane is awkward. Each printed command is numbered, and pressing its digit copies it through OSC 52, which also works over SSH. Nothing is run.
  Done when: pressing `2` in the pane emits the OSC 52 sequence containing the second command's exact text, which a pty test captures.

- **Peek any id with Space** — FEATURE — value 4 — effort M — risk low — category: pane
  Why: the pane shows task ids and stages, but the user has to leave it to learn what an item is. Space on a selected row opens a floating card with the brief, criteria state and last proof, and `?` explains the highlighted widget in a sentence. This is the empty-state and accessibility help the UI lens asks for.
  Done when: a pane screenshot test with a task selected and Space pressed shows the card containing the criterion text, and Escape closes it without redraw artefacts.

- **Show how often Foreman stayed quiet** — FEATURE — value 3 — effort S — risk low — category: cost, framing
  Why: the measured Foreman premium comes from bookkeeping calls and hook notes, and the user wants cheaper. The close line reads "quiet on 83% of turns, 4 notes, 1.1k tokens". That is the positive side of the earlier tax-receipt ideas, and it makes quiet a goal.
  Done when: closing a task prints the fraction of turns with zero injected notes, computed from the ledger and matching a hand count on a fixture session.

- **Write the session as chapters** — FEATURE — value 3 — effort M — risk low — category: close-out
  Why: the user runs long unattended sessions and returns to a wall of ledger lines. At close, Foreman writes a short table of contents with a title, time span, commit and proof for each chapter, derived from tasks and compactions. Assumption: the ledger has enough boundaries to cut chapters.
  Done when: `fm session chapters` on the marathon fixture prints one chapter per compaction span, each with a commit hash that exists.

- **Suggest the first task from the repo's own evidence** — FEATURE — value 3 — effort M — risk low — category: empty state
  Why: T-0862 and T-0863 are deferred pending evidence that the first run needs help. An empty queue is the first screen, so it can offer one concrete request taken from a failing test, a TODO or a red CI badge, shown as a command to copy.
  Done when: in a fixture repo with one failing test, the empty pane names that test and offers a `fm task new` line. In a clean repo it shows nothing invented.

- **Give motion one grammar** — CLEAN — value 3 — effort S — risk low — category: motion
  Why: the pack mentions flashes, fades and criterion ticks as separate ideas. One tiny vocabulary (appear, settle, flash) in a single module, with the reduced-motion switch applied in one place, keeps them consistent.
  Done when: grep shows no direct animation timing outside that module, and with reduced motion on, a pane test records zero intermediate frames.

- **Wild: Print a boarding pass when an unattended run starts** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: wild. The queue, dollar cap, gate, ETA and kill phrase appear as a small ticket. On return it is stamped with arrived, diverted or delayed, so the receipt is something the user can screenshot and show.
  Done when: starting the drive prints the ticket with cap and queue, and the drive's finish rewrites it with a stamp that matches the ledger outcome.

- **Wild: Add voice packs for every pane and refusal string** — FEATURE — value 2 — effort M — risk low — category: personality
  Why: wild. Strings move to one catalogue, so `fm config voice plain|terse|warm` swaps the register. It doubles as the base for translation. The guard's verdict text stays identical in every pack.
  Done when: switching packs changes the greeting text, while a guard-refusal snapshot test is unchanged across all packs.

- **Wild: Open a museum of fixed bugs on the Pages site** — FEATURE — value 3 — effort M — risk low — category: site
  Why: wild. The repo holds thousands of closed tasks with red-to-green proofs. One card per bug class shows the failing test, the one-line fix and how it was caught, generated from closed briefs. That is a browsable record that Foreman catches things, alongside the benchmark numbers.
  Done when: the site build emits at least 20 cards, each linking to a real commit, and a card with no proof is omitted.
