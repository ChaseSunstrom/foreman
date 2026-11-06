# Brainstorm — lens: user value

Lens: user value. Each idea is new against the "ideas so far" list, aimed at the thin areas (performance, security, privacy, devices, developer experience), and framed as what the person who set the goal gets.

- **Stream the first plan rows within seconds** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: assumption: a vague goal is the most impatient moment, and today the plan arrives only when decomposition finishes. "Preview without creating state" exists but doesn't speed anything up.
  Done when: for a fixture vague goal, `fm goal` prints the first must-row within a stated bound (e.g. 15s) while the rest are still being decided, and the final plan equals a non-streamed run.

- **Label a goal private and gate every outward path on it** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: the steers say `fm genesis live` publishes to the site and `fm ship` pushes to main. Nothing stops private goal text reaching a cloud lane, a brainstorm pack or a published page.
  Done when: a goal marked `private` makes a planted secret phrase in its text absent from the brainstorm pack, the site data and the handoff page, and each refusal prints the repair command.

- **Check that a row's secrets exist without ever reading them** — SECURITY — value 3 — effort S — risk low — category: security
  Why: assumption: rows often need an API key or token. The user finds out at row 9 on day 3, and any pasted value lands in the journal.
  Done when: a row with `needs: secret STRIPE_KEY` shows as a user-only item at plan time, and the check passes or fails on presence alone with the value never appearing in any state file.

- **Scrub evidence lines for secrets as they are written** — SECURITY — value 4 — effort S — risk low — category: security
  Why: the goal journal and receipts store command output as proof, and long goals pass tokens, cookies and paths through them. The redacted handoff page covers only the one export.
  Done when: a proof command that prints a planted token leaves the journal, receipt and ledger with only the masked form, and the proof still verifies.

- **Print an egress ledger on the finish card** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: assumption: a user who left a goal running for days wants "who did it talk to?". The fence idea blocks; this one reports.
  Done when: a fixture goal that fetches from two hosts lists exactly those hosts and counts on the finish card, and a goal with no network lists "none".

- **Gate each new dependency on the row that needs it** — SECURITY — value 3 — effort M — risk med — category: supply-chain
  Why: the lists have licence audits and yank watchers but nothing that ties a dependency added mid-goal to a reason. A multi-day goal is where one slips in.
  Done when: adding a package to a manifest during a goal without a named row is flagged at the next `fm check`, and the finish card lists each added dependency with its row.

- **Ratchet the latency of the goal verbs themselves** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: hooks have a bench (`bench_hooks.py`), but resume and status read the whole goal state on every session. They get slower as a goal grows and nobody would notice.
  Done when: the bench times `status`, `next` and resume on a 200-row, 3-week synthetic goal, and ship fails if p95 grows past the recorded bound.

- **Compact the goal journal into an archive, not a deletion** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: assumption: a goal that runs for weeks makes the journal and its replay grow without bound. Resume cost then rises with age.
  Done when: past a size threshold old segments move to a compressed archive, resume time on the compacted goal matches a fresh one, and a replay across the archive gives the same verdict.

- **Give goal status a plain, narrow, no-colour form** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user meets Foreman over ssh, in a phone terminal or through a screen reader. Box art and colour break there.
  Done when: with `NO_COLOR` set or at 40 columns, goal status is one fact per line with no box characters, and a snapshot test at both widths passes.

- **Pair a phone with a read-only, expiring token for the goal page** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: the web UI exists and a phone is where the user checks a long goal. Existing ideas push notifications out but never say how a phone authenticates safely.
  Done when: a QR pairing yields a token that can read goal status but gets 403 on any write verb, and it stops working after its stated expiry.

- **Add a security pass row to goals that touch auth, files or the network** — FEATURE — value 4 — effort M — risk med — category: security
  Why: assumption: a goal that builds a login or an upload ends "done" with every functional row green and nobody having attacked it. The rows are functional, and a threat-model line sits only on trust-boundary tasks.
  Done when: a fixture goal that adds an upload endpoint gets an auto-added row where a hostile-input lane tries a path-traversal payload, and the goal cannot close while that row is open.

- **Wild: take the user on an ownership tour at finish** — FEATURE — value 4 — effort M — risk low — category: developer experience (wild)
  Why: assumption: after a three-day agent build the user is an owner who has not read the code. A short ordered reading path, from entry point to riskiest file with one line each, turns "done" into "I can maintain this".
  Done when: `fm goal tour` prints at most 12 files in reading order, each with one line, every cited file exists, and the files holding the riskiest rows come first.

- **Wild: move a goal between machines as an encrypted bundle** — FEATURE — value 3 — effort M — risk med — category: privacy (wild)
  Why: assumption: the user starts on a desktop and finishes on a laptop. A passphrase-encrypted bundle of goal state works with no cloud, no shared ref and no network.
  Done when: export on machine A and import on machine B resume to the same next row and verdict, and the bundle opened with the wrong passphrase reveals none of the plan text.

- **Wild: print the goal as a one-page card with a QR for the resume baton** — FEATURE — value 2 — effort S — risk low — category: devices (wild)
  Why: assumption: some users think better on paper. A page showing the finish line, rows closed and open, the next row and the exact resume command works with no screen at all.
  Done when: `fm goal card` writes a one-page PDF or text-art sheet whose resume command, copied into a fresh terminal, lands on the same next row.

- **Wild: lock a finished goal with a short read-aloud fingerprint** — SECURITY — value 2 — effort S — risk low — category: trust (wild)
  Why: assumption: weeks later the user asks "is this still what was signed off?". A six-word fingerprint of the finish oracle and the tree they can compare in one glance answers that without a tool.
  Done when: the fingerprint printed at finish matches a re-run on the same tree and differs after any tracked-file edit.

Next question: Which goal-state files (journal, receipts, handoff page, brainstorm pack, site data) can carry a secret or private text today, and which outward path reads each one?

Next question: On the user's slowest or remote machine (ssh, phone terminal), which goal verbs break or crawl, and has that ever been measured?
