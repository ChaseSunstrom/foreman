# Brainstorm — lens: bold bets

- **Run mechanical tasks with zero model calls** — FEATURE — value 4 — effort M — risk low — category: zero-token lane
  Why: Renames, formatter passes, dependency bumps and doc-command drift are deterministic, but each still spends a model turn. The pack's top complaint is token burn. Assumption: a codemod runner covers most of these.
  Done when: a rename task closes with `fm cost` showing zero model calls and the same gate verdict as the model path.

- **Schedule the queue as one constraint problem** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: The pack shows gate-lock waits (one held over 40 minutes), deferrals tied to the usage reset, and per-task budget caps. These are being handled one at a time. Assumption: one solver over lock, budget window and deadline can replace them.
  Done when: a simulated queue with a held gate and a reset window finishes with no task waiting over 60 seconds on the lock.

- **Simulate a week of usage before changing the governor** — FEATURE — value 4 — effort M — risk low — category: usage simulation
  Why: The user has pushed on usage burn twice, and each governor change ships untested against real spend. Assumption: a recorded week of usage events is enough to replay.
  Done when: the replay reproduces the last week's deferral times within 5 minutes and flags any config that would breach the cap.

- **Let the guard learn from overrides, with the user's sign-off** — FEATURE — value 4 — effort M — risk high — category: guard learning
  Why: The guard refuses commands the user later approves. Each override is evidence of a false positive. Assumption: proposals only, never auto-allowed, because this is the security boundary.
  Done when: an override creates a proposed rule, the same command stays refused until the user accepts it, and the accepted rule is scoped to that project.

- **Serve the queue over a local socket** — FEATURE — value 3 — effort M — risk low — category: local API
  Why: Editors and scripts shell out to `fm` and parse text. The pack shows several surfaces (web UI, pane, desk card) rebuilding the same state. Assumption: a socket returning the `fm status --json` shape is a stable contract.
  Done when: `curl --unix-socket` returns the same JSON as `fm status --json` for the same journal state.

- **Plan a whole week in one model call, execute on cheaper runners** — FEATURE — value 4 — effort L — risk med — category: batch planning
  Why: The user wants all ideas done with little usage. Planning once and executing mechanical steps cheaply fits that. Assumption: a plan written once stays valid across the week's changes.
  Done when: a 10-task queue uses at most 2 planning calls, and each step's runner is recorded in its receipt.

- **Write release notes from closed-task receipts** — FEATURE — value 3 — effort S — risk low — category: release notes
  Why: Each closed task already has a receipt with its proof line. The pack lists many shipped tasks per release but no single changelog. Assumption: receipts hold the user-facing summary.
  Done when: `fm release notes <range>` lists each closed task once, with its proof line, and omits tasks with no receipt.

- **Publish a conformance suite for other agent tools** — FEATURE — value 2 — effort L — risk low — category: open standard
  Why: The pack shows Foreman's guard, proof and queue rules are already tested in isolation. Other tools could run the same checks. Assumption: some users want to adopt the rules without the full plugin.
  Done when: a clean checkout of a third-party tool passes the suite's guard and proof cases with one command.

- **Keep a wager book on Foreman's own estimates** — FEATURE — value 2 — effort S — risk low — category: estimate calibration
  Why: (wild) Foreman states an estimate for each task, the user settles the bet at close, and the book shows which estimates are reliably high or low. Assumption: a short, optional prompt at close will get answers.
  Done when: each closed task records an estimate and an outcome, and `fm wager` shows the hit rate per task kind.

- **Turn the pane's quiet moments into a one-line haiku per gate** — CLEAN — value 2 — effort S — risk low — category: delight
  Why: (wild) The pane already shows gate results as status lines. A seventeen-syllable line per result gives each pass a human note without clutter. Assumption: users enjoy small words more than charts.
  Done when: a green gate shows a haiku in the pane that stays under the pane's width, and a setting turns it off.

- **Sleep a repo with no open work to a one-line stub** — PERFORMANCE — value 2 — effort S — risk low — category: idle footprint
  Why: (wild) Idle repos still load hooks and state on every session. A stub that wakes on a file change would cut that cost to near zero. Assumption: the wake check is cheap.
  Done when: a repo with no open work costs no hook time in a session, and the first file change restores the full state.

- **Show a lighthouse beacon when main breaks** — FEATURE — value 2 — effort S — risk low — category: broken-main signal
  Why: (wild) The site and pane don't signal a broken main until someone runs the gate. A beacon on the web UI and the desk card makes the state visible from across the room. Assumption: the state is already in the journal.
  Done when: a failing main shows the beacon on the web UI, and a green run clears it within one refresh.
