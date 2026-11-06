# Brainstorm — lens: user value

- **Say what round 1 changed for you in three lines** — FEATURE — value 5 — effort S — risk low — category: legibility
  Why: the user asked for "super improve… etc. etc. etc." and round 1 shipped ~20 items, but nothing in the pack says they were told in felt terms; "nobody has ticked the board yet." Existing ideas cover receipts per task, not a per-round "what's different when I work now" note.
  Done when: closing a round writes a ≤3-line note (e.g. "sessions get titled, phone pings only when needed, big outputs trimmed once you say yes") that `fm status` prints at the next session start and then stops showing.

- **Offer compact output on the user's own worst real output** — FEATURE — value 5 — effort S — risk low — category: opt-in
  Why: compact output is built and measured (~1.04M tokens/30 days) but off until the user says yes; they have no way to feel the tradeoff. Assumption: transcripts hold a recent big Bash output.
  Done when: `fm compact preview` shows the largest Bash output from the last 7 days as before/after with char and token counts, and ends with the one command that turns it on.

- **Turn "etc. etc." into a standing budgeted mandate** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user repeatedly asks for open-ended improvement and steered that "recursively improve" means repeat rounds. Today each round needs a retype. Assumption: a spend and round cap is acceptable.
  Done when: `fm mandate "keep improving" --rounds 3 --usd 20` runs rounds back to back, stops at either cap, and leaves one summary of what shipped.

- **Auto-tick the board from what the user does next** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: "nobody has ticked the board yet"; asking for ticks is friction the user is not paying. Behaviour is evidence: using a feature, disabling it, or dropping its task.
  Done when: after a week, a feature the user toggled off shows as reverted and one used 5+ times shows as kept, without any click, visible in `fm research show`.

- **Prove the mail monitor armed, once, loudly** — FIX — value 4 — effort S — risk low — category: liveness
  Why: the pack names "arming in a live interactive session is unverified." The user cares about never idling, and a silent miss defeats it.
  Done when: a new session's first turn shows a one-line "mail monitor armed" or "not armed, using tmux fallback because X", and a test fakes both outcomes.

- **Say "nothing changed for you" when true** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: many close-outs are internal (reader fixes, warnings). The user dropped several by-design items, which suggests noise is unwelcome. Assumption: a task can be tagged user-visible or not.
  Done when: closing an internal-only task prints "no change to how you work", and the round note leaves it out.

- **Auto-write a by-design register from the user's drops** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the "dropped" list records reasoned decisions (heredoc guard, test-folder prove, delta reads), and children still re-proposed similar ideas across rounds.
  Done when: each drop's reason is saved as a short rule, and `fm ideas` rejects a candidate that matches one, naming it.

- **Replay a metric reader against real stored strings** — FIX — value 4 — effort S — risk low — category: correctness
  Why: two of the user's recent asks were readers missing '✗ exit N' because nobody tested them against writer output. Round 1 added more readers.
  Done when: one test feeds actual stored result strings from the state dir through every track-record and catch-rate reader and fails on any miss.

- **Wild: Wake to a finished Round 3 on the breakfast page** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: wild. The user's wording ("etc. etc. etc.") suggests wanting progress without babysitting. Assumption: a night run with a cap and an `fm page` morning summary is allowed.
  Done when: `fm night --rounds 1` leaves a self-contained page listing shipped, reverted and needs-you items, and pushes once only if a decision is open.

- **Wild: Preview a round as a one-minute before/after strip** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Round results are scattered across tasks; the user reads in glances.
  Done when: `fm page --round N` renders each shipped item as a small before/after card (command output, band, notification) with no network requests.

- **Wild: Let the user say "keep it like this" about a behaviour** — FEATURE — value 4 — effort M — risk med — category: stability
  Why: wild. The user has reversed and dropped things, and self-improvement could drift settled behaviour. A pin prevents later rounds from changing it.
  Done when: `fm keep "<behaviour>"` stores a pin, and a later task whose diff touches the pinned code is blocked at plan time until the user releases it.

- **Pause a round for a one-line question with a default** — FEATURE — value 3 — effort S — risk low — category: asks
  Why: round 1 left decisions pending (compact output on or off). One bundled question at round end beats several scattered asks.
  Done when: closing a round raises at most one `fm ask` with defaults for every open opt-in, and answering it applies all of them.
