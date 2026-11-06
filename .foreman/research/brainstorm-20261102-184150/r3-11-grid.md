# Brainstorm — lens: grid

- **Subtract the base rate from every dissent score** — FEATURE — value 4 — effort S — risk low — category: scoring
  Cell: unattended run × wrong.
  Why: the carried gap scores dissents against outcomes, but if most closes survive 14 days anyway, a dissent that "was right" 60% of the time may mean nothing. Assumption: the survival rate is high and varies by task kind.
  Done when: `fm outcomes` prints each dissent score beside the survival rate of same-kind closes without a dissent, and a fixture where both are 60% shows a lift of 0.

- **Embargo security-class left-outs from the public Genesis site** — SECURITY — value 4 — effort S — risk low — category: privacy
  Cell: web UI (site) × user × unsafe.
  Why: the left-out receipt is published through `fm genesis live`, and a line like "guard bypass via X not examined" is a public disclosure. Assumption: the receipt's cell tags include a security class.
  Done when: a left-out item tagged security or privacy is absent from `site/genesis` data until its brief closes, and a test plants one and checks the published JSON.

- **Redact canary excerpts before they enter a pack or brief** — SECURITY — value 4 — effort S — risk low — category: security
  Cell: canary × agent × unsafe.
  Why: canaries quote repo, docs and ledger text beside each idea, and that text goes to cloud children and Mission pages. Assumption: the credential redactor isn't applied on that path.
  Done when: a planted fake API key in a file a canary hits appears as `[redacted]` in the pack and the brief.

- **Never execute an Exam reading at view time** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Cell: web UI × user × slow.
  Why: a Mission page that runs live-state commands on render stalls on a big ledger, and the commands race with writers. Assumption: the web UI reads briefs on request.
  Done when: rendering a Mission page with a 10k-task ledger makes no subprocess call, shows each reading's stored value and age, and takes under a set budget in a test.

- **Bar the builder's own run from closing a brief's Exam** — FIX — value 4 — effort M — risk med — category: proof integrity
  Cell: agent × wrong.
  Why: the open question is which readings a cold process can re-run. A reading taken by the agent that built the change is self-graded. Assumption: the close record doesn't say who took the reading.
  Done when: each reading records its runner (builder, finish gate, cold process, user), and `fm task finish` refuses a close whose only reading is builder-run, with a refusal test.

- **Flag a dissent that echoes pasted source text** — SECURITY — value 3 — effort M — risk low — category: injection
  Cell: other agents × unsafe.
  Why: lenses treat the pack as data, but a user-pasted document inside it can steer a child into filing a dissent that kills a good brief. Assumption: dissents quote the pack.
  Done when: a dissent sharing a long verbatim span with a `<pasted_content>` block is marked "echo" and doesn't count in the score, tested with a planted paste.

- **Show the left-out count in the pane header and status line** — FEATURE — value 3 — effort S — risk low — category: devices
  Cell: terminal pane × user × missing.
  Why: the Mission page and the site carry the receipt, but the pane, where the user actually sits, doesn't. Assumption: the pane reads `fm status --json`.
  Done when: the pane header and the status line show "N left out" from the latest Mission, and the number matches the receipt in a fixture.

- **Add a two-key dismissal for left-out items** (wild) — FEATURE — value 3 — effort M — risk low — category: integrity
  Cell: agent × unclear.
  Why: the actor that left an item out shouldn't be the one to mark it fine, or gaps get laundered. Assumption: the receipt records who left each item out.
  Done when: closing a left-out item needs a different actor type (user, cold child or a closing brief) than the one that wrote it, and a same-actor dismissal is refused.

- **Run the Exam reading on a frozen ledger copy as a drift baseline** (wild) — FEATURE — value 3 — effort M — risk med — category: measurement
  Cell: unattended run × wrong.
  Why: an outcome that moves after a close may have moved because the world changed, not because of the fix. Reading the same measure on the ledger as it stood at filing separates the two.
  Done when: a close reports "moved X, of which Y is drift", and a fixture with a change in ledger content alone shows full drift and zero lift.

- **Run a 600-character skim test on every Mission page** (wild) — FEATURE — value 3 — effort S — risk low — category: legibility
  Cell: user × unclear.
  Why: users read the top of a page, and the page has to say what was left out there. Assumption: Mission pages can run long.
  Done when: a tool-less child sees only the first 600 characters and must name the interpretation and one left-out item, and a Mission fails filing if it can't.

- **Let a Mission narrow or widen itself from how its predecessors fared** (wild) — FEATURE — value 3 — effort L — risk med — category: adaptation
  Cell: unattended run × missing.
  Why: the user keeps narrowing scope by hand (the volatile-path audit steer), and no loop learns from that. Assumption: the dropped-brief rate and the later asks landing in left-out cells are both readable.
  Done when: the next Mission's pack states its width and the two numbers that set it, and a replay on gen-3 data picks a narrower width after a high drop rate.

- **Stop a lane building a brief whose evidence lives only on the Mission page** — FIX — value 3 — effort S — risk low — category: lanes
  Cell: other agents × missing.
  Why: a lane gets the brief, not the page, so it can't see which canaries ran or what was left out. Assumption: briefs are filed as tasks without the page body.
  Done when: every filed brief carries its canary results and its cell's left-out neighbours inline, and a lane started from `fm task show` can quote both.

- **Add a cap and a timeout to every Exam live reading, logged** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Cell: unattended run × slow.
  Why: an unattended close that waits on a hung reading stalls the drive. Assumption: readings run without a limit today.
  Done when: a reading that sleeps past its cap is recorded as "could not run: timeout" with its elapsed time, and the close proceeds as unproven.

Cells left empty:
- Other agents × slow: the existing lane-pacing and hedging ideas already cover it.
- Web UI × agent × unsafe: this is the approval surface, already covered by the stale-tab and retype-to-confirm ideas.
- Unattended × unclear: dozens of earlier receipt ideas fill it, and more would only repeat them.

Next question: Which of the five failure modes has the fewest recorded user corrections in the ledgers, and does that mean it's covered or just never noticed?
Next question: Does the user ever open a Mission page at all, or do they read only the finish card, and what would that change about where the left-out receipt should live?
