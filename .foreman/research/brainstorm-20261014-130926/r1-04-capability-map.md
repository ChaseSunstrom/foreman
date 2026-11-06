# Brainstorm — lens: capability map

- **Audit what round 1 shipped but nobody is using** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the pack's known gaps are all "shipped but dormant": compact output is off, the mail monitor is unproven in live sessions, and nobody has ticked the board. Nothing detects that class automatically.
  Done when: `fm doctor --adopted` lists each task closed this round as on / armed / used, or dormant with the one command to enable it, and exits nonzero while any is dormant.

- **Record proof-of-life per Claude Code integration** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: round 1 added the monitor, sessionTitle, the push ask, agent effort and maxTurns, and baseRef, but doctor only checks the version. Version support doesn't show a feature fired. Assumption: each can leave a one-line stamp the first time it is observed working.
  Done when: `fm doctor` shows "last observed working" per integration, and an integration never seen in the last 7 days of real sessions is flagged "unproven".

- **Smoke-test a cold session end to end** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: the mail monitor starts only in new sessions, and that arming is unverified. The cheap check is a capped haiku `claude -p` session in a fixture project that gets a bus mail and a task change.
  Done when: `fm doctor --live` starts a child capped at $0.05, sends a bus mail, and asserts the mail reached the model, the title changed, and the wake skipped tmux. A failing integration fails the check.

- **Make compact output expandable, and gate enabling it on measured re-fetches** — PERFORMANCE — value 4 — effort M — risk med — category: tokens
  Why: it saves ~1.04M tokens over 30 days but stays off, because dropping the middle of an output may cost a re-run. There is no measure of that cost. Assumption: a later `fm output ID --lines a:b` or an identical re-run can count as a re-fetch.
  Done when: compacted outputs carry a one-line expand hint, `fm cost` reports the re-fetch rate, and `fm doctor` recommends enabling compaction only when the rate is below a stated threshold.

- **Salvage children that die on budget or turn limits** — FIX — value 4 — effort M — risk low — category: agents
  Why: round 1 put `--max-budget-usd`, effort and maxTurns on children and lane agents. Hitting a cap probably returns a half answer that looks complete. Assumption: the child's transcript or stream keeps its partial output.
  Done when: a child stopped by a cap is recorded as truncated with its partial text kept, and `fm research show` and the lane close-out display "truncated at $X / N turns" with a one-command narrower re-run.

- **Let the user tick the catalogue page and paste the result back** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: `fm page` is read-only and nobody has ticked the board, so a round's ideas never reach the queue. Keep it local-first, with no network channel.
  Done when: checkboxes and j/k/space keys on the page build a live `fm research tick 3,7,9` command with a copy button, and running it queues those ideas, verified by a test.

- **Offer one-yes opt-ins backed by the user's own telemetry** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: round 1 leaves features behind opt-ins (compact output, and presumably the push ask) and the user must discover and judge each one. Foreman already measures 30-day Bash chars and hook ms.
  Done when: `fm suggest` prints each off-by-default setting with its projected saving from this machine's history, and `fm suggest --apply` turns on the ones the user names.

- **Keep session titles and push bodies in sensitive repos to T-ids** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: round 1 made sensitive repos refuse outward tools, but sessionTitle now carries task titles into the session list, and push bodies carry text. Assumption: titles may sync or show in surfaces outside the terminal.
  Done when: in a repo flagged sensitive, the title is "T-0818" and the push body has no task text, and a test covers both.

- **Infer repo sensitivity and say why** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: egress refusal depends on the sensitive flag, and a repo the user forgot to mark leaks by default. Signals could be a private remote, `.env` or key files, or a LICENSE or NDA marker (assumption).
  Done when: `fm doctor` suggests the sensitive flag with its reasons and never sets it silently, and a fixture repo with a `.env` triggers the suggestion.

- **Generate FEATURES.md from the doctor manifest** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: doctor already holds each relied-on Claude Code feature with its minimum version. MASTER.md documents them by hand and can drift. Finish already refuses a close that leaves self-docs failing.
  Done when: `fm doctor --write-features` renders feature, min version, using file and fallback, and a test fails when the file is stale.

- **Log whether each push got a response** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the Stop hook asks once for a push when an ask is open or the queue drains, with no measure of whether anyone responded. Assumption: the time to the next user prompt can be read from the ledger.
  Done when: `fm cost` or doctor shows push count and median time-to-response, and a push followed by the user already present within 30 seconds is counted as noise.

- **Wild: capture from a forwarded email** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: the user mostly captures from the terminal, and a phone or inbox is the one surface that would let a thought arrive before they open Claude Code. Opt-in, local polling, nothing sent out.
  Done when: with an explicit setting, a mail to a configured mailbox appears in the inbox verbatim with its source marked "mail", and nothing is fetched while the setting is off.

- **Wild: show a round-delta arrow in the band** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: "recursively improve" has no visible score. The user repeats "smarter, faster, better" and nothing shows whether round 2 beat round 1. The bench already measures hook CPU time, and cost already measures tokens per task.
  Done when: the band or `fm status` shows hook ms, tokens per task and first-pass rate with ↑/↓ since the last round marker, read from existing measurements.

- **Wild: queue the next round automatically from what the user said "etc." about** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: the user's closing "etc. etc. etc." is an open mandate they never enumerate. Assumption: clusters with no shipped task can be listed from the catalogue.
  Done when: after a round ends, `fm round next` proposes the three largest uncovered clusters as captured tasks for a yes or no, and queues nothing without that yes.
