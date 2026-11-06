# Brainstorm — lens: simplicity

- **Collapse the calibration readers into one module** — CLEAN — value 4 — effort M — risk med — category: consolidation
  Why: T-2610 lists five separate readers of the same bet data (track, ledger, Briers, bar check, base rate), and each one needed its own "like with like" fix. Several readers of one ledger invite drift.
  Done when: one `fmcalib` API serves all five readers, `grep` finds no second parser of the bets file, and the existing calibration tests pass unchanged.

- **Swap rule: a new verb must retire one** — FEATURE — value 4 — effort S — risk low — category: lean ratchet
  Why: the lean ratchet counts verbs and static metrics, but nothing forces growth to be paid for. The standing rules only require a measurement before growth is judged. Assumption: the verb count is stable enough to gate on.
  Done when: `fm ship` fails a diff that raises the verb count unless the same diff removes a verb or a recorded `fm decide` waives it, and a test covers both paths.

- **Delete-a-module drill** — CLEAN — value 4 — effort M — risk low — category: modularity
  Why: `plugin/lib` has 131 files, and "Move Genesis out of core" and "Lite mode" (T-0794) are both deferred. Nobody knows which parts are really optional.
  Done when: a test copies the plugin, deletes each optional module directory in turn, and asserts `fm doctor` and the guard still run. Modules that fail the test are listed as hidden core.

- **Pack the 1,388 skill files into on-demand bundles** — PERFORMANCE — value 4 — effort L — risk med — category: footprint
  Why: the map shows `plugin/skills/` holds 1,388 files, about 60% of the repo, while the lean ratchet already tracks description chars as a cost.
  Done when: skills load from one index plus bundles fetched only when matched. Session-start injected chars drop with no new failures in `fm exam`, and `fm doctor` shows the file count.

- **Cap default output at ten lines** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: a long run of Foreman-written ledgers, doctor rows and receipts suggests output keeps growing. Assumption: several verbs print more than a screen by default.
  Done when: a lint test runs every read-only verb on a fixture repo, fails any whose default output exceeds 10 lines, and requires a `more: fm x --full` footer.

- **Verb death certificates** — CLEAN — value 3 — effort S — risk low — category: pruning
  Why: "hide unused verbs" is already proposed but only hides them. The reach check already knows which verbs no session path calls. Go further and propose the deletion diff.
  Done when: a verb with zero calls in 90 days and no reach path gets a filed task containing the exact removal diff. Closing it also removes its tests and doc lines, and a tombstone is left behind.

- **Knob census** — CLEAN — value 3 — effort S — risk low — category: configuration
  Why: the flags and env vars named in the pack (`FOREMAN_QUIET`, `--round-first`, `--pace off`, `--final`, `--regressing N`) come from separate steers. Presets are already proposed, but nobody has counted the knobs.
  Done when: `fm settings --census` lists every flag and env var with its default, its usage count and the task that added it. Any knob never set away from its default in 60 days is flagged for removal.

- **Run only the tests a diff can affect** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: `fm ship` is gated by the full suite across 404 test files, and every task also runs `fm check` and the finish audit. Assumption: the suite takes minutes per task.
  Done when: `fm check --fast` selects tests from the import graph plus the tests→src map, and a differential run shows it catches every failure the full suite catches on the last 50 commits. Full suite stays the gate at ship.

- **One hook dispatcher process** — PERFORMANCE — value 3 — effort M — risk high — category: hooks
  Why: `bench_hooks.py` and T-0832 (shell prefilter) show hook latency is a standing worry. Many hooks mean many interpreter starts per tool call.
  Done when: all PreToolUse and PostToolUse work runs in one process per call, median wall time on the bench drops, and the guard still blocks with the same decisions on the guard test corpus.

- **Wild: A 100-line kernel that boots everything else** — FEATURE — value 3 — effort L — risk high — category: architecture (wild)
  Why: assumption: the discipline loop (plan, prove, one task, guard) is small and the rest is accretion. A tiny kernel with typed extension points makes every other module removable, and a reader can audit it in one sitting.
  Done when: `fm` core is under 100 lines of logic, loads modules from a manifest, and `fm doctor` lists which modules are loaded.

- **Wild: Compact ledgers into signed summaries** — PERFORMANCE — value 3 — effort M — risk med — category: data size (wild)
  Why: ledgers grow forever (bets, outcomes, history, 2,624+ tasks), and open questions already say a missing record class makes readers answer wrongly. Compaction must keep what readers count.
  Done when: `fm compact` rewrites records older than 90 days into one summary row per class, with counts and Brier sums. Every reader returns identical numbers before and after, checked by a fixture test.

- **Wild: Say it in one sentence** — FEATURE — value 3 — effort M — risk low — category: legibility (wild)
  Why: the README, MASTER.md and the site all describe the product at length, and the user has asked for "plain" things repeatedly (T-0795 plain receipts). Assumption: a newcomer can't state what Foreman did in one line.
  Done when: every finished task, doctor run and ship ends with one generated sentence (under 140 characters) naming what changed and whether it was proven, and a test rejects any receipt without one.

Next question: Which Foreman modules has the user never touched or complained about in 100 sessions, and would they notice if each were gone?
Next question: What is the real per-task wall-clock and token cost of the ceremony (hooks, audits, gates), measured on a fixed fixture, so simplification is judged against numbers rather than line counts?
