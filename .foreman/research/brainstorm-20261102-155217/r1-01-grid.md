# Brainstorm — lens: grid

Surfaces: web UI, `fm` CLI, hooks, foreman-ui pane, Genesis site, Desktop tray. Actors: user, agent, other agents or lanes, unattended run. Failure modes: missing, wrong, slow, unsafe, unclear. Every idea below is tagged with its cell.

- **Reject web actions fired from a stale tab** — SECURITY — value 4 — effort S — risk low — category: web UI
  Why: cell web UI × user × unsafe. Assumption: the web UI can mutate state (grants, ship, answers). A tab left open overnight can approve something that no longer means what it showed.
  Done when: a test renders a page, changes the ledger, posts the old action, and gets a 409 that names what changed.

- **Retype the task id to confirm irreversible web actions** — SECURITY — value 3 — effort S — risk low — category: web UI
  Why: web UI × user × unsafe. Assumption: ship and publish grants can be clicked. A click is too cheap for actions that publish.
  Done when: the grant endpoint refuses a request that lacks the typed id, and the UI test covers both paths.

- **Serve every page render from one ledger epoch** — FIX — value 3 — effort M — risk med — category: web UI
  Why: web UI × unattended × wrong. The drive appends to many ledgers while the page reads them, so a render can show a closed task beside an open queue. The pack has torn-write drills but no cross-ledger read consistency check.
  Done when: a test appends mid-render and the page's numbers all come from a single recorded offset, which is printed in the footer.

- **Require a "not checked" field in every lane hand-back** — FEATURE — value 4 — effort S — risk low — category: agents
  Why: lane × agent × unclear. Hand-backs carry a verdict, but the places the lane did not look go unrecorded. Assumption: lanes return structured text.
  Done when: a lane result missing the field is rejected at merge, and `fm lane` shows the field on the merge card.

- **Coalesce simultaneous `fm ask` questions into one card** — FEATURE — value 4 — effort M — risk low — category: user attention
  Why: lane × user × slow. Parallel lanes (Missions 5-8 run that way) can each block on the same unanswered question, so the user sees a storm of prompts. Assumption: the questions are comparable by text.
  Done when: three lanes ask near-identical questions, one prompt appears, and one answer releases all three.

- **Run `fm doctor` from inside each harness's own sandbox** — FEATURE — value 4 — effort M — risk med — category: harness parity
  Why: CLI × other agents × missing. T-0335/36/37 stay blocked because nobody has seen what Codex, Gemini and opencode can reach. A doctor run launched by the harness itself records PATH, state-dir access and delivered hook events.
  Done when: the command writes a per-harness reach table and flags "guard not enforced" for any harness that delivered no pre-tool event.

- **Show a headless-safe line for a missing Desktop tray dependency** — FIX — value 2 — effort S — risk low — category: tray
  Why: Desktop tray × user × missing. T-0325 is blocked on `libappindicator-gtk3`, and the failure is silent. Assumption: the tray launches in the background.
  Done when: the tray command exits with the exact install line and `fm doctor` lists it as optional.

- **Let hooks degrade visibly when the user can't tell they're off** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: hooks × user × unclear. Earlier ideas cover crash cards and fail-open declarations. This one covers the first minute after a silent fail-open, which is still an open question in the pack. The cell is the user noticing at all.
  Done when: the first prompt after a hook failure carries one visible line, and a test kills a hook and asserts the line appears.

- **Record the Genesis site's published commit on every page** — FIX — value 2 — effort S — risk low — category: docs
  Why: site × user × wrong. The site auto-publishes from the tower, so a visitor can't tell data from yesterday's tick from last week's.
  Done when: each page footer shows the source sha and age, and a test fails if the footer is missing.

- **Wild: Mint a grid cell from "this surprised me"** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: wild; every surface × user × unclear. A key on any pane row or web element files the surface, actor and failure class as a cell plus a red-first fixture.
  Done when: pressing the key creates a task naming the cell, and the cell appears in the atlas.

- **Wild: Open a failure atlas as the web UI's home** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild. The standing coverage rule demands every cell hold a grounded idea, an existing path, or a recorded n/a. The user currently has no view of that grid beyond `coverage.md`. A page of surfaces × actors × failures, each cell hatched, green or n/a, with its test linked, makes it visible.
  Done when: the page renders from `coverage.md` and a templated cell shows as uncounted.

- **Wild: Replay a recorded worst-day ledger through every surface on each release** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: wild. The ledger shape the user's real state reaches is the least tested case. Assumption: a frozen, redacted ledger fixture can be assembled from a bad real day (a torn tail, an orphaned lane, a pinned clock).
  Done when: CLI, web UI and pane each render the fixture without a traceback, and each prints a one-line degraded notice.

Cells left empty:
- Hooks × agent × slow: bench_hooks already holds that.
- Site × unattended × unsafe: the leak scan is already built, per the steers.
- CLI × user × wrong: the Next-line and did-you-mean ideas already cover it.
- Pane × other agents × missing: the roster and Agents graph exist.

Next question: which of these surfaces has the user actually opened in the last 30 days, so that cells for untouched surfaces can be marked n/a with evidence?
Next question: when the user and a lane both answer or edit the same item, which side do readers trust, and is that tested per surface?
