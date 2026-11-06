# Brainstorm — lens: user value

- **Triage the slate by swipe or keypress** — FEATURE — value 4 — effort M — risk low — category: ui/devices
  Why: assumption: the user answers slates by prose ("dropped: …", "steered: …"), and the drop reasons they type are the best intake-precision signal. One card per idea, with keys y/n/later/"already built" plus a one-line reason, served in the pane and on the LAN web UI. Each answer is written straight to the drop and steer ledgers.
  Done when: a test feeds 5 keypress answers to the triage view and the ledger gains 5 typed rows (3 keep, 1 drop with reason, 1 later).

- **Show a mock of the output before asking for acceptance** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: the user's recent asks are mostly "FEATURE: print X / list Y" lines, and several were dropped as "mostly built" only after they read them. For the top three ideas, generate a 10-line fake receipt or fake `fm` output, labelled SIMULATED.
  Done when: `fm ideas --mock` prints a fixture-based sample per top-3 idea and each sample carries the SIMULATED label.

- **Rank ideas by user-minutes, not build effort** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: the pack's effort S/M/L measures build cost. Review minutes, which T-2584 style counts treat as the user's scarce resource, are never ranked. Add an estimated "minutes you'll spend" (read, decide, verify) to each idea.
  Done when: the slate sort has a `--by-attention` mode and a test shows a different order from the value/effort sort on a fixed fixture.

- **Stream ideas as each brainstorm child finishes** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: assumption: a lens fan-out is awaited to completion, so the first idea appears only when the slowest child ends. Printing early results means the user can start triage while later lenses run.
  Done when: with two fake children (1s and 5s) the first idea prints before 2s and the merged slate matches the batch result.

- **Preview exactly what a brainstorm pack sends out** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the pack embeds the user's own words, email-bearing context and file paths. A pre-send view shows byte counts per section and flags emails, tokens and absolute home paths, and `--redact` swaps them for placeholders.
  Done when: a fixture pack containing a fake email and home path shows both flagged, and `--redact` output contains neither.

- **Make the slate readable in one paste-able markdown file** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user reads slates in the terminal only. `fm slate --export` emits one markdown file with stable idea ids, so it can be read on a phone or pasted into another chat, and answers pasted back (`i-12: drop, built`) are parsed.
  Done when: a round trip of export, hand-edit and re-import yields the matching ledger rows in a test.

- **Give each idea a first-screen sentence and lint for it** — CLEAN — value 3 — effort S — risk low — category: ui
  Why: many ideas end with "Done when" checks that no user would see. Require "On Monday you'll see: …" and fail slates where it is missing or repeats another idea's phrasing.
  Done when: the lint rejects 3 planted ideas that lack the sentence or reuse it.

- **Run the next lens in idle time while the user reads** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: assumption: brainstorm runs are all-at-once and billed. Under the existing spend caps, speculatively start the lens most likely to surface new ideas (by recent lens hit rate) and hold the output until asked, discarding it after a timeout.
  Done when: the speculative run stays within the cap, and the held output is shown once on request and gone after expiry.

- **Offer a local-only brainstorm for pack sections tagged private** — SECURITY — value 3 — effort L — risk med — category: privacy
  Why: assumption: all lenses go to a remote model. Let the user mark sections (steers, ledgers) private and route only lenses that need them to a local engine, with the rest remote.
  Done when: with a private-tagged section and a fake remote, the remote receives zero bytes of that section, checked in a test.

- **(wild) Ration the user's yes votes** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: wild. Give the user only 5 "yes" tokens per slate. This forces ranking, and the unspent tokens become a measure of how thin the slate was.
  Done when: a sixth yes is refused with the list of current yeses, and the token count is stored per slate.

- **(wild) Get a desk-lamp or tray colour for slate readiness** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild. A tiny local signal (tray icon colour, an `ntfy` message to the user's own phone, or a terminal title) shows "slate ready / needs answer / quiet", so nobody has to poll the terminal.
  Done when: the state change fires a notifier mock exactly once per transition.

- **(wild) Write the user's reply before they do** — FEATURE — value 4 — effort M — risk med — category: unspoken needs
  Why: wild. A tool-less child that sees only the user's past drops and keeps drafts accept/drop/later for each idea with a reason in their style. The user edits the draft, and the diff from the real answer is the score.
  Done when: for 20 held-out past ideas the draft decision matches the real one at a reported rate, shown against a coin-flip baseline.

- **(wild) Replay the last 30 days of asks as a Monday-morning movie** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild. A 30-second terminal playback of what Foreman did, built from ledger rows and nothing generated. It is the cheapest way for the user to feel the value without reading receipts.
  Done when: `fm replay-week` prints a timed scene sequence from a fixture ledger, and every scene cites a ledger id.

Next question: which part of a slate does the user read first and which part do they skip, and does the pack's layout match that?
Next question: when the user drops an idea, is it because it was already built, too small, or unwanted, and does Foreman store which?
