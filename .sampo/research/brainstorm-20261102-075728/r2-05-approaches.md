# Brainstorm — lens: approaches

- **Pin verify commands at plan acceptance** — SECURITY — value 4 — effort S — risk low — category: oracle integrity
  Why: T-2606 now lets a criterion's verify command be fixed after the fact. Approach: hash each row's verify command when the user accepts the plan. A later edit, by the model or by injected goal text, needs `fm goal amend` and a yes. Trade-off: one more step when a verify really is wrong.
  Done when: editing an accepted row's verify without `amend` makes `fm goal check` print "oracle changed" and refuse to close the row (tested).

- **Run oracle probes in a network-off sandbox unless the row declares `needs:`** — SECURITY — value 3 — effort M — risk med — category: sandboxing
  Why: assumption: probe commands are model-written text run unattended on every resume, and a pasted PRD or issue could plant a `curl | sh`. A row declares `needs: net` or `needs: write:<path>`, and the plan card shows these. Trade-off: some probes need a declaration.
  Done when: a probe calling `curl` without `needs: net` fails with a named reason, and one that declares it runs.

- **Plan locally first and show cloud only row titles** — PRIVACY — value 4 — effort M — risk med — category: local-first
  Why: assumption: goals often carry unreleased product detail. A local model drafts rows from the repo and the goal. If a cloud reviewer is enabled, it sees only the goal sentence and the row titles, never repo text. Cloud review defaults to off. Trade-off: the local plan is thinner, so a public-goal corpus should compare its row count to the cloud plan's before trusting it.
  Done when: with `goal.cloud=off`, a stubbed plan run makes zero outbound model calls, as shown by the egress ledger.

- **Add `fm goal egress` with a pre-send preview** — PRIVACY — value 3 — effort S — risk low — category: egress ledger
  Why: nothing in the pack lets the user see what a planner or child call received. Each call logs model, bytes and the file paths included, and `--preview` prints the payload before it is sent. Trade-off: one more ledger to keep small.
  Done when: the last plan's payload lists its paths, and a file matched by an ignore list never appears in it (tested).

- **Seed a canary secret and assert it never leaves** — SECURITY — value 3 — effort S — risk low — category: leak test
  Why: assumption: the privacy claim has no test. A fixture repo holds a fake key plus a canary string in the goal text. The test fails if either shows up in any child payload, handoff page, tick note or log.
  Done when: the canary test passes on the current tree and goes red once a handoff writer is changed to include raw repo text.

- **Order oracle probes cheapest-first and stop at the first red** — PERFORMANCE — value 3 — effort S — risk low — category: oracle speed
  Why: assumption: a resume check that runs every probe pays for the slowest one each time. Store each probe's p50 duration and sort by it. `--all` keeps the full run. Trade-off: a fail-fast result hides other reds until the next run.
  Done when: on a 40-row fixture with one failing 1s probe and one 30s probe, `fm goal check` exits in under 2s and names the red row.

- **Shard goal state: an index plus one file per row** — PERFORMANCE — value 3 — effort M — risk med — category: goal storage
  Why: the repo already shows heavy state (2125 files) and hook p95 gating (`bench_hooks.py`). Resume would read the index and only the active wave's row files, so cost scales with the wave, not the goal. This also shrinks lane write conflicts to one row file. Trade-off: a migration, and a many-small-files layout is harder to hand-edit.
  Done when: resuming a 500-row synthetic goal reads fewer than 10 files and stays inside the existing hook p95 budget in `bench_hooks.py`.

- **Publish a JSON Schema and `fm goal lint` for the goal file** — DEVELOPER EXPERIENCE — value 3 — effort S — risk low — category: editor and pre-commit
  Why: assumption: users will hand-edit the goal file. Lint output is `file:line: message`, so editors and pre-commit hooks make errors clickable. It flags a row with no probe, an unknown dependency or a duplicate id. Trade-off: a schema to keep in sync with the writer.
  Done when: a golden goal file validates, and a file with one probe-less row reports its exact line.

- **Report the oracle as a CI status check** — DEVELOPER EXPERIENCE — value 3 — effort M — risk med — category: CI surface
  Why: tests already run on GitHub Actions per the badge. `fm goal check --ci` emits annotations and "31/42 rows proven", and fails if a closed row's probe regressed. This is the same oracle, checked off the user's machine. Trade-off: probes needing local state must be tagged `ci: skip`.
  Done when: a fixture PR that breaks a closed row's probe shows a red check naming the row.

- **Duel the oracle against the plan** — FEATURE — value 3 — effort M — risk med — category: completeness
  Why: one cheap lane writes only a finish oracle from the goal text. A second writes only the plan. Oracle claims no plan row covers are missing rows. Plan rows no oracle claim touches are unproven or surplus. Trade-off: two lane runs per goal, and the two lanes can share the same blind spots.
  Done when: on a seeded goal where one capability is withheld from the plan, the duel reports that gap by name.

- **Render the goal view for 40-column SSH** — DEVICES — value 2 — effort S — risk low — category: narrow terminals
  Why: assumption: the user checks progress from a phone terminal. `COLUMNS<=40` or `NO_COLOR` switches to ASCII, one row per line, and the next action first.
  Done when: with `COLUMNS=38`, no output line exceeds 38 characters (snapshot test).

- **Wild: import a whiteboard photo as plan rows** — FEATURE — value 2 — effort L — risk med — category: phone input
  Why: wild. A phone photo goes through a local vision model into draft rows, shown as a strike-out deck, never auto-accepted. It is the lowest-effort way to give Foreman a vague goal from a phone.
  Done when: a fixture photo of 6 sticky notes yields 6 draft rows, each tagged "from photo".

- **Wild: serve a 4-line `/goal.txt` for a desk display** — FEATURE — value 1 — effort S — risk low — category: ambient device
  Why: wild. A loopback-only endpoint, off by default, gives rows proven, the next row and a stale flag. A cheap ESP32 or e-ink tile could poll it.
  Done when: `curl localhost:PORT/goal.txt` returns 4 lines under 60 characters each, and the port is closed unless enabled.

- **Wild: serve goal rows as LSP inlay hints** — DEVELOPER EXPERIENCE — value 2 — effort L — risk med — category: editor
  Why: wild; it follows the deferred LSP work in T-0788. A function a plan row depends on shows "row 14 · unproven" inline in the editor.
  Done when: opening a file named in a row's `touches:` shows a hint with that row's id and state.

Next question: Which Foreman-written goal artifacts (verify commands, handoff pages, row text) are read back and acted on by a later session without anyone checking them, and what is the cheapest tamper test for each?
Next question: What does the user actually run in order to trust that a goal is finished, and does any current gauge answer that without an extra command?
