# Brainstorm — lens: user value

- **Show a "since you last looked" diff on every pane open** — FEATURE — value 4 — effort M — risk low — category: return UX
  Why: the user repeatedly says things "look weird", "not everything is shown" and "duplicated"; assumption: they reopen the pane after turns away and can't tell what changed. Shows only what moved since the last time the pane was visible (steps done, gates flipped, cost delta).
  Done when: opening the pane after two finished steps renders exactly those two steps as a highlighted delta, and a second open with no change renders "no change".

- **Make mod render-fixtures come from the user's own screenshots of complaints** — FEATURE — value 4 — effort M — risk low — category: visual regression
  Why: at least 8 asks are about visual state (diff contrast, unpaneled messages, `$` not animated, duplicated dashboard). Each was fixed then re-raised in a different form. Assumption: the mod can dump the offending frame as text when the user types `/looks-wrong`.
  Done when: `/looks-wrong` writes the current frame plus row types to a fixture dir, and a test fails if any fixture row lacks a panel owner.

- **Add a single-owner rule for screen regions: every row claims one surface** — CLEAN — value 4 — effort M — risk med — category: dashboard
  Why: "dashboard is duplicated at the bottom of the chat even though there's a panel on the top right". Duplication is a structural problem, not a styling one. Each section (AC, audits, band, status) is registered to exactly one surface, and a second claim is a test failure.
  Done when: a test enumerates sections across pane, band, status line and chat, and fails when any section is drawn in two surfaces at the same time.

- **Budget-aware "quota brake" with a plain weekly-share readout** — FEATURE — value 5 — effort M — risk low — category: usage
  Why: one session burned 20% of the weekly quota; the user is "usage-sensitive" and asked for token efficiency. Existing ideas cover ledgers and forecasts, but not an automatic brake on the drive loop and parallel lanes. The brake stops launching new lanes or brainstorm rounds once the session spends over a user-set share.
  Done when: with a share of 2%, `fm run --parallel 4` refuses to start a lane past the limit and states the figure and the override command.

- **Replace the Read-heavy context fill with outline-first reads for files over N lines** — PERFORMANCE — value 4 — effort M — risk med — category: tokens
  Why: Read fills 59% of context, Bash 34%; the median first reply sits at 27k tokens. Assumption: many reads are whole files when a range would do. Nudge once per file with an outline and offset suggestion rather than denying.
  Done when: a replay over recent logs shows lower Read tokens per session, with no new blocked-read complaints in `fm friction`.

- **Pre-reload the mod between turns so the drive loop never stops for it** — FIX — value 3 — effort S — risk low — category: drive
  Why: 5 drive stops for mod reloads and 7 for background waits in the friction data; "don't stop until complete" is the user's explicit wish. Defer reloads until the next natural turn boundary and resume the drive in the same Stop hook.
  Done when: a scripted run that edits the mod mid-drive finishes the queue with zero Stop-for-reload events in the ledger.

- **Wild: Let a fresh-eyes subagent screenshot the mod in tmux and file looks-wrong tasks** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild; the user's top complaint class is visual and currently found only by them. The subagent drives a private tmux, never the user's terminal, and files tasks with the captured frame attached.
  Done when: a seeded layout bug (an unpaneled row) is filed as a queued task with its frame and no human prompt.

- **Wild: Hold a "complaint court" that sorts each user complaint into bug, taste or misunderstanding** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: wild; the same visual areas get re-raised, which suggests some of them are taste calls that were treated as bugs. Taste verdicts become theme settings and bugs become tests.
  Done when: the last 20 recorded asks each carry a verdict, and a taste verdict yields a setting rather than a code fix.

- **Wild: Offer a "make it boring" one-key mode that collapses all panels to single-line rows** — FEATURE — value 3 — effort M — risk low — category: display
  Why: wild; the user asked for panels everywhere, yet also complains of duplication and clutter. A reversible density toggle (rich, compact, one-line) lets them settle it per moment instead of per request.
  Done when: toggling cycles all three densities with no row losing its panel owner and no content dropped.

- **Wild: Print a "what Foreman did while you were away" card with cost and a one-key undo list** — FEATURE — value 4 — effort M — risk med — category: return UX
  Why: wild; drive mode and lanes run unattended, and the user cares about quota and about guard-blocked actions. One card lists commits made, files changed, cost spent and blocks hit, with each commit offering a one-yes revert.
  Done when: after a simulated unattended run of 3 tasks, the card lists all 3 commits with cost, and a revert command restores the prior tree for one of them.

- **Attach the user's wording to every self-improvement fix and re-check it after N turns** — FEATURE — value 4 — effort M — risk low — category: loop proof
  Why: the loop is "standing" and the user asked for RSI; the pack shows fixes recurring in new forms, so there's no evidence which fixes held. Each fix stores the quoted complaint and a recurrence test, and `fm friction` reports held or reopened.
  Done when: `fm friction` lists each recent fix with its complaint quote and a held/reopened state computed from later sessions.
