# Brainstorm — lens: simplicity

- **Start every repo in Lite and promote features on evidence** — FEATURE — value 5 — effort M — risk med — category: defaults
  Why: the user wants Foreman cheaper than Claude Code. The tax is +10–14% on small tasks and about 60% on the long session, and it comes from bookkeeping calls and hook notes. T-0794 (Lite mode) is deferred. Assumption: each note and ceremony step can be tied to the failure it prevents (guard block, post-compaction miss, unproved claim).
  Done when: a fresh repo's first session injects only the guard plus the plan and prove steps. After a ledger event (an unproved close, a post-compaction miss) the matching feature turns on, with one printed line saying why. A test shows the late-enabled feature fires only after its trigger event.

- **Raise the support floor and delete the shims below it** — CLEAN — value 4 — effort M — risk med — category: compat
  Why: Foreman was adapted to 2.1.301, and 2.1.304 adds `decider: "person"` and `e.isReadOnly`. Home-grown approval binding and process-identity code probably duplicate what is now native. Assumption: version-branch code exists in `plugin/lib`.
  Done when: one `MIN_CLAUDE_CODE` constant exists and `fm doctor` refuses older versions with the upgrade command. A grep for version branches below the floor returns nothing, and the roundtrip e2e passes on the floor version.

- **Lint one vocabulary across help, notes, site and README** — CLEAN — value 3 — effort S — risk low — category: language
  Why: the pack mixes task/brief, lane/builder/worker/agent and hint/lesson/fix/card, and each synonym costs a newcomer a concept. Assumption: the synonyms are also used in user-facing text, not only internally.
  Done when: a glossary file of at most 15 terms, each with its banned synonyms, backs a CI check. The check fails on a banned synonym in help text, injected notes, `site/` or the README, and passes on main after the rename.

- **Keep state outside the repo unless the user opts in** — FEATURE — value 4 — effort M — risk med — category: footprint
  Why: there are 1,069 briefs, and `.foreman/` has transcripts, a ledger and hints. All of it is footprint a user must understand, ignore or commit. Assumption: most users never want to review these files in git.
  Done when: by default, state for a repo lives under `$XDG_STATE_HOME/foreman/<repo-id>/` and `git status` stays clean after a full task. `fm adopt --in-repo` moves it back, and the docs name which files are meant to be shared through git.

- **Ship the plugin as one zipapp** — PERFORMANCE — value 3 — effort M — risk med — category: install
  Why: 1,560 files, 74 of them in `plugin/lib`, have to be copied and imported on every hook start. Hook cold-start is already benchmarked (`bench_hooks.py`). Assumption: zipimport with precompiled bytecode is not slower than loose files.
  Done when: `fm.pyz` runs every verb and hook. `bench_hooks.py --runs 20` shows p50 no slower than loose files, and uninstall is a single `rm` that leaves no residue.

- **Make hooks append-only and let only `fm` verbs write state** — CLEAN — value 4 — effort M — risk med — category: state
  Why: the open tickets and drops are full of lease, claim and re-entry concerns (T-1205 and others), which suggests many writers. One writer path removes a class of races and locks. Assumption: hooks currently write more than the single ledger append.
  Done when: a test runs every hook against a read-only copy of state and passes, except for ledger append. Lock acquisition in hook code paths drops to zero, confirmed by grep.

- **Cap `.foreman` with a retention policy** — CLEAN — value 3 — effort S — risk low — category: footprint
  Why: briefs, transcript copies and ledgers only grow, and the commands that scan them slow down. Assumption: nothing needs transcripts older than about 30 days.
  Done when: each state kind has a TTL and a size cap in one table. `fm doctor` prints the size per kind, an over-cap kind is pruned oldest-first with a one-line receipt, and tests show open tasks are never pruned.

- **Delete `plugin/lib` lines that no test or real session executes** — CLEAN — value 3 — effort M — risk med — category: dead code
  Why: the 226 test files and the e2e roundtrip give a coverage map, and a usage ledger exists (`fm usage`). Together they find code nothing has reached. Assumption: the unreached share is large enough to matter.
  Done when: a report lists functions with zero test coverage and zero recorded use. The first batch is deleted as one commit with the full gate suite green, and the report is re-runnable.

- **Wild: Race Foreman against its own minimal twin** — PERFORMANCE — value 4 — effort M — risk low — category: benchmark
  Why: the duel compares Foreman with plain Claude, but never with a 300-line version of the same discipline (plan, prove, guard). Whatever the twin matches at lower cost marks the rest as deletable. This differs from the existing ablation ideas because it is one purpose-built control arm rather than component-by-component removal. Assumption: a twin can be built from existing hooks.
  Done when: the Benchmarks page shows plain, the twin and full Foreman side by side on the spec suite at the same Haiku dollar cap. Every mechanism that doesn't beat the twin gets a deletion brief.

- **Wild: Trace each clause of the tagline to exactly one mechanism** — CLEAN — value 4 — effort S — risk low — category: scope
  Why: the README promises five things: plan before editing, prove with commands run, stay on one task, keep going, and guard. Any mechanism that serves none of them is scope creep. Assumption: most of the 15 skills and the long verb list map to at most one clause.
  Done when: a table in the repo maps every verb, hook and skill to a clause or to "none". CI fails on a new unmapped item, and the "none" rows each become a deletion or justification task.

- **Wild: Expire a feature per repo after 30 days with no hits** — FEATURE — value 3 — effort M — risk med — category: self-pruning
  Why: this is a per-repo version of the self-deleting features idea, built on the default-Lite promotion above. A repo with no Docker use should stop hearing Docker cards. Assumption: the usage ledger records per-feature fires.
  Done when: a feature with zero hits in a repo for 30 days turns off there, with one printed line and a one-command re-enable. The next session shows the matching drop in injected bytes.

- **Golden-file all injected and help text** — CLEAN — value 2 — effort S — risk low — category: review
  Why: wording changes to notes silently change cost (cost per turn is the open complaint) and tone. Assumption: the notes are scattered across modules rather than in one place.
  Done when: one snapshot file holds every note, refusal and help string. A change shows as a diff in review, and CI fails if the snapshot is stale.
