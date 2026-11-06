# Brainstorm — lens: what the user would notice and love

- **Show a "closed because" receipt in the user's own words** — FEATURE — value 5 — effort S — risk low — category: trust/UX
  Why: the user's verbatim asks (e.g. "diff tour", "veto") are scattered across briefs; assumption: they want to see each of their sentences matched to the evidence that satisfied it, not Foreman's paraphrase. Complements the existing request-to-criterion trace by rendering it at close.
  Done when: finishing a task prints each quoted user clause beside its verifying run ID, and a clause with no run is flagged.

- **Add an `fm undo ID` with verified rollback** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: the user was denied an `rm` and has crash history (zero-byte git objects); a one-command revert of a whole task builds confidence to let the drive run. Assumption: tasks are commits or lane-scoped enough to invert.
  Done when: after `fm undo T-X`, the tree matches the pre-task commit and the task's criteria's verify commands are shown to fail again.

- **Make `fm next` answer "why this, not that"** — FEATURE — value 4 — effort S — risk low — category: explainability
  Why: queue ordering and hint-quieting are opaque; the user steers constantly ("steered: demote hints that never help"). Assumption: a one-line reason per rank reduces steering effort.
  Done when: `fm next --why` prints, for the top item and the runner-up, the rule that ranked one above the other.

- **Open each session with a "since you left" card** — FEATURE — value 5 — effort S — risk low — category: continuity
  Why: drive ends turns to wait on background work 18 times and crashes happen; a returning user needs a 5-line recap (finished, blocked, spent, needs-you). Deliberately merges the earlier morning-report, since-you-left and `fm since` ideas into one.
  Done when: a new session after finished tasks shows one card listing done/blocked/spend/decisions-needed in ≤10 lines, and nothing when no change.

- **Run the user's one-line grade of a pass into the shortlist** — FEATURE — value 4 — effort M — risk low — category: taste learning
  Why: three passes of many ideas, with the user dropping or steering several; the "taste" signal exists but is unused. Assumption: a thumbs up/down per shipped item is cheap for them to give.
  Done when: `fm grade T-ID good|meh|bad "why"` is stored and the next brainstorm's context pack lists graded outcomes by category.

- **Cap guard false-positive pain with an inline "teach this" prompt** — FIX — value 4 — effort M — risk med — category: guard UX
  Why: three known false positives hit (`git stash list`, python heredoc, read-only state reads). The user denied one action already, so friction is felt; the guard must stay precise, not weaker.
  Done when: a blocked-but-benign command offers `fm guard teach`, which records a replay case that must pass the precision corpus before any rule changes.

- **Wild: Add a "pane weather" and celebration for clean first-time closes** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the UI already has many cards; a single glanceable mood (calm, stormy from flakes and blocks, sunny after streaks) is what people screenshot. Assumption: low-cost derived view model in fmwatch.
  Done when: the pane shows one weather word with its top cause, and a first-time close triggers a visible one-frame flourish that can be turned off.

- **Wild: Ghost brief for the likely next request** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the user's requests chain predictably (feature → "do multiple passes" → "improve yourself"). A child drafts the probable next brief from recent steers, shown as a dim card the user accepts or discards.
  Done when: after a close, the pane shows a ghost brief; accepting it with one key creates the real task, discarding it logs a miss that adjusts future ghosts.

- **Wild: "What did you almost do?" replay** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: guard blocks, vetoes, and recalled lessons that silently changed a course are invisible, yet they are exactly what builds trust. Assumption: the ledger already holds blocks and notes to render.
  Done when: `fm almost` lists, for the last turn or task, each blocked command, fired veto, and ignored alternative, with timestamps.

- **Wild: Generate a one-page HTML "proof postcard" per task** — FEATURE — value 4 — effort M — risk low — category: sharing
  Why: the user hands off work via PRs and AGENTS.md; a self-contained page merging the diff tour, red→green runs, audit lenses and cost is what they would show others. Merges the HTML diff tour and the proof pack ideas.
  Done when: `fm proof ID --html` writes one file under a size cap with no external fetches and with secrets scrubbed.

- **Show a per-task cost and time bill before and after** — FEATURE — value 4 — effort S — risk low — category: cost transparency
  Why: the user cares that subagents "don't eat up a crap ton of tokens" without losing capability; an estimate at accept and an actual at close, with overrun noted, shows it. Merges the earlier ask-before-spend and bill ideas.
  Done when: task accept prints an estimated range, and close prints actual versus estimate per stage.
