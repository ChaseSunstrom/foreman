# Brainstorm — lens: bold bets

- **Event-source all state with a universal `--at`** — FEATURE — value 4 — effort L — risk med — category: state
  Why: assumption: `fm doctor --as-of`, "query the guard as of a past date" and "rewind state to before a bad write" are each proposed separately. One append-only event log with derived views would give every reader time travel and make torn-write and record-class-loss drills a single test.
  Done when: `fm status --at <ledger offset>` and `fm outcomes --at <offset>` print the view as it was then, and a test replays 500 events to the same state the live readers hold.

- **Generate ledger writers, readers and validators from one schema file** — CLEAN — value 4 — effort L — risk med — category: ledgers
  Why: the missed-ask list (T-2656, T-2657, T-2667) keeps finding readers that miss a record class, such as `hook_success` stdout missed by `fmcost.INJECTS`. Generated readers would declare the classes they consume and fail the build when a new class is unclaimed.
  Done when: adding a record class to the schema without a declared consumer fails `fm check`, and `fm drill` deleting any one class makes every reader name it.

- **Type every string with its provenance** — SECURITY — value 4 — effort L — risk high — category: taint
  Why: the "taint untrusted content", "fingerprint Foreman's own output" and "fenced prompt templates" ideas each patch one edge. A `Tainted(str)` carrying user, model, repo, web and ledger labels would let every outward sink (push, publish, model child, site data) check labels at one chokepoint.
  Done when: a planted repo string reaches `fm genesis live` and `fm ship` and each refuses, naming the source label, and a test proves the label survives concatenation.

- **Make the autonomy dial a replay-previewed slider** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: the pack proposes three presets and several separate knobs (guard strictness, ceremony, spend cap, interruption cap). The user's steers show they keep tuning these by hand. A single dial whose positions are previewed against last week's ledger ("at 3 you'd have been asked 4 times, blocked 2 commands, spent $11 less") turns settings into a decision.
  Done when: `fm dial` prints per-position counts computed from the real ledgers, and a test shows the preview's counts equal the counts from actually replaying under that position.

- **Run an offline parity score for `fm code` on a local model** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: T-1207 and the privacy lens want nothing sent without a setting, but nothing measures what going local costs. The duel (T-1231) and the exam already supply scenarios, and a local-model arm would give the number.
  Done when: `fm exam local` reports tasks passed, cost and time for the local arm against the cloud arm on the same scenarios, with the gap on the scorecard.

- **Show steer violations as live editor squiggles** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the user's steers carry `[check: CMD]` (T-2636) and are enforced only at sweep time. A minimal LSP server could run the cheap ones on save and underline the line that breaks a standing rule, naming the steer.
  Done when: saving a file that violates a stored steer check in an LSP-capable editor shows one diagnostic citing the steer's date, and a stdio-level test asserts the diagnostic message.

- **Back-test brainstorm configurations against the accept and drop ledger** — FEATURE — value 4 — effort M — risk low — category: meta
  Why: the pack holds more than 2,000 ideas and many "dropped: already built" entries. Which pack shapes (digest or full list, lens set, grounding step) predict what the user later accepts has never been measured. Replaying 20 past brainstorms with pack variants and scoring against accept, drop and later-asked would give that.
  Done when: `fm ideas backtest` prints precision (accepted over proposed) per pack variant over the last N brainstorms, with an empty-pack baseline row.

- **Run local-model brainstorm lenses on idle hardware** — PERFORMANCE — value 3 — effort M — risk med — category: privacy/spend
  Why: assumption: a local engine can generate the cheap lens fan-out while the cold-read and grounding steps stay on the stronger model. The pack covers idle API quota but not the user's own idle CPU or GPU.
  Done when: a brainstorm with a local-lens flag completes with zero API tokens for the fan-out, and the ledger records which lenses ran locally.

- **Run lanes in microVMs that restore from a snapshot** — PERFORMANCE — value 3 — effort L — risk high — category: isolation
  Why: pack ideas for a warm worktree pool, a sandbox profile and an overlay of `$HOME` each get part of this. A snapshotted microVM gives fast lane start, a hard reach boundary and a clean throwaway after a hostile or runaway lane. Assumption: the user's kernel permits KVM.
  Done when: a lane starts from snapshot in under 2 s, a write outside its declared paths does not appear on the host, and a planted escape attempt is recorded in the ledger.

- **Compile friction events into capability candidates weekly** — FEATURE — value 3 — effort M — risk low — category: self-direction
  Why: `fm friction` and `fm outcomes` hold repeated pains, but each becomes a one-off task. Clustering them by cause and filing one named capability per cluster, with its evidence list, matches "build Foreman into a self-directing harness".
  Done when: `fm friction --cluster` prints clusters with counts and filing a cluster yields one inbox item citing every member's task id.

- **Wild: Turn state into a haptic grammar for phone and watch** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild. Stop, proof landed, ask pending and usage limit hit could each get a distinct vibration pattern via the phone-push path in the pack, so a user away from the screen feels state without reading it.
  Done when: each of 4 states maps to a distinct pattern in a table, and a test asserts the table has no duplicates.

- **Wild: Distil a small local model of the user's judgement overnight** — FEATURE — value 3 — effort L — risk high — category: privacy/learning
  Why: wild. Drops, steers and reverted commits are labelled preference data. A small adapter trained locally could pre-answer `fm ask` and pre-score slates, with nothing leaving the machine.
  Done when: on held-out past asks, the adapter's agree-with-user rate beats the always-defer baseline, and the training set is shown never to have left the host.

- **Wild: Ship the read model as one offline HTML file with embedded Python readers** — FEATURE — value 2 — effort L — risk med — category: devices
  Why: wild. Pyodide in a single file would let a phone open the exact `fm` readers over a copied ledger snapshot with no server and no network, which also fits the local-first constraint.
  Done when: opening the file offline in a browser renders `fm status` and `fm outcomes` from an embedded snapshot, with no network requests.

Next question: which of Foreman's readers would give a different answer if the same ledger were replayed in a different order or after a clock jump?
Next question: which user surface (phone, editor, tray or terminal) has the user actually opened in the last 30 days, and does any idea here depend on one they haven't?
