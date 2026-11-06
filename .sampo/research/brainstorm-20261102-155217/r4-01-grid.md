# Brainstorm — lens: grid

Surfaces: web UI (the declared surface), the `fm` CLI, hooks/session start, the foreman-ui pane, and the Genesis site. Actors: user, agent, other lanes/agents, unattended drive. Failure modes: missing, wrong, slow, unsafe, unclear.

- **Require a human-input witness for web UI approvals** — SECURITY — value 4 — effort M — risk med — category: web-ui safety
  Why: cell web UI × lane × unsafe. assumption: a lane process on the same host can reach the local web server and answer its own `fm ask`.
  Done when: a test that POSTs an approval from a lane-descendant process (no browser input event or token) is refused and the refusal is ledgered.

- **Show a stale-data badge with age on every web UI card** — FIX — value 4 — effort S — risk low — category: web-ui clarity
  Why: cell web UI × user × wrong. The pack shows many readers (cost, outcomes, clock) with different windows, and nothing says how old a number is. assumption: the UI shows no per-card age today.
  Done when: with the ledger frozen for 10 minutes, every card shows "as of HH:MM", and a test asserts the field on each card.

- **Replay the first minute after a silent fail-open on each surface** — FIX — value 5 — effort M — risk low — category: degraded-state
  Why: cell hooks × user × unclear. This is an open question left by earlier brainstorms ("what does the user see in the first minute after a silent fail-open"). It becomes a matrix with one row per surface.
  Done when: a test forces a hook import failure and asserts that CLI, pane and web UI each print a degraded line naming the cause.

- **Make anticipation cards declare which surface they were rendered on** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: cell agent × user × missing. A card computed at Stop but never injected looks the same as one that was read. assumption: the delivery path isn't recorded.
  Done when: the ledger row for each card has `delivered_to: [session|pane|web|none]` and `fm doctor` shows the share with `none`.

- **Give lanes a "blocked by policy" hand-back with the widening command** — FEATURE — value 4 — effort M — risk low — category: multi-agent
  Why: cell lane × agent × unclear. Sub-agent allowlist blocks currently look like failures, and the pack shows blocked-adapter tasks T-0335/36/37 stuck on exactly this.
  Done when: a lane denied a command returns outcome `policy_blocked` plus one `fm` command that widens it, and the planner surfaces both.

- **Time-box the unattended drive's own startup on a slow disk and cold cache** — PERFORMANCE — value 3 — effort M — risk low — category: unattended
  Why: cell unattended × drive × slow. The pack names tmpfs state (`/run/user/1000`) and a cold hook-start bench, but no cold-cache drive start.
  Done when: a bench with a dropped page cache and throttled I/O finishes drive start under a recorded bar, and exceeding it fails the test.

- **Show a "what changed since you last looked" diff in the pane header** — FEATURE — value 4 — effort M — risk low — category: pane
  Why: cell pane × user × missing. The repeated asks for morning cards and "while you were away" suggest a need nobody has built into the always-visible surface.
  Done when: reopening the pane after 8 hours shows closed/filed/stopped counts, and clicking one opens the ledger line.

- **Quarantine the site's data publish when a user-authored ask is in the diff** — SECURITY — value 3 — effort S — risk low — category: site leak
  Why: cell site × unattended × unsafe. `fm genesis live` auto-publishes to main, and the pack shows verbatim user words in the data. assumption: a leak scan runs only for secrets, not user text.
  Done when: a fixture with a verbatim ask in `site/genesis` data blocks the publish with a named reason.

- **Make `fm doctor` print one cause line per red, with the command that clears it** — FIX — value 3 — effort S — risk low — category: clarity
  Why: cell CLI × user × unclear. Earlier asks like "Print one next command on every nonzero exit" show this class recurs.
  Done when: a test iterates the doctor registry and fails any row without a `fix:` command that parses.

- **Wild: Let the web UI replay a recorded worst day against each release** — FEATURE — value 3 — effort L — risk low — category: regression
  Why: wild. Cell web UI × user × wrong across time: a stored hostile ledger (torn tails, gaps, 10× size) rendered in CI, with golden screenshots.
  Done when: CI renders the fixture and diffs snapshots, and the build fails on any uncaught exception or blank card.

- **Wild: Add a "heard nothing" lamp to the status line for each unattended path** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: wild. Cell unattended × user × missing. Silence from a healthy idle drive and silence from a dead one look identical.
  Done when: killing the timer turns the lamp amber within one interval, and a healthy idle drive stays green.

- **Wild: Have a cold child guess each surface's next click from a screenshot and score it** — FEATURE — value 2 — effort M — risk low — category: UX test
  Why: wild. Cell web UI × agent × unclear. It measures "unclear" without a human.
  Done when: a scorecard gives per-view guess accuracy, and any view below 50% files a task.

- **Stamp each lane's landed commit with lane id and model** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: cell lane × user × unclear. A merged series can't be told apart by who wrote it. assumption: only the task id is recorded.
  Done when: `git log` shows `Lane:` and `Model:` trailers on a two-lane merge fixture.

Cells left empty:
- Site × agent × slow: static pages, no latency path.
- Pane × lane × missing: covered by the Agents graph already.
- CLI × unattended × slow: covered by existing bench and stall asks.

Next question: Which of these surfaces has the user never opened in 30 days, and would they notice if it silently went stale?
Next question: When a lane and the user both answer the same `fm ask`, which answer does each reader record?
