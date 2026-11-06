# Brainstorm — lens: capability map

- **Gate public API breaks at close** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: the pack shows gates for tests, coverage and licences but none that diffs exported symbols. Aider and Cursor don't do it either, whereas semver checkers (cargo-semver-checks, api-extractor, griffe) do.
  Done when: a test that removes a public function in a fixture package makes `fm task finish` print "breaking: removed foo()" and block unless `--because` is given.

- **Ship migration and infra guard packs** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard covers shell commands (T-0275, `fm guard wrong`), but nothing recognises `terraform apply`, `kubectl delete`, `DROP TABLE` or `alembic downgrade` as their own classes. Assumption: users' repos include these.
  Done when: `fm guard try "kubectl delete ns prod"` is refused with a named class, and a replay corpus of 10 labelled infra commands passes.

- **Gate UI projects on visual regression** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: the pack screenshots Foreman's own pane, but a general version for the user's web app is missing. Percy, Chromatic and Playwright snapshots do this. T-0797 (native browser verification) is deferred.
  Done when: with a fixture app, a CSS change that moves a button fails the gate with a diff image path, and `fm golden approve` accepts it.

- **Add an accessibility gate for web projects** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: assumption: pane a11y ideas exist (screen-reader mode, reduced motion), but nothing checks the user's own pages. axe-core and Lighthouse are the standard.
  Done when: a fixture page with an unlabeled input yields one finding at close with its selector.

- **Run framework upgrade runbooks** — FEATURE — value 4 — effort L — risk med — category: maintenance
  Why: the pack has `fm deps --capture` (one brief per major bump) and a Renovate-style lane idea, but no multi-step migration such as React 18→19 or Django LTS. Those need codemods, changelog reading and staged gates.
  Done when: a fixture upgrade runs as an ordered task chain (codemod, fix, gate), each step is committed, and a failed step stops the chain.

- **Write tests for uncovered changed lines** — FEATURE — value 4 — effort M — risk low — category: test generation
  Why: "gate close on diff coverage" is only a gate. Codium/Qodo and Copilot generate the missing tests, and the pack lacks the follow-through.
  Done when: for a fixture diff with an untested branch, the lane adds a test that fails when the branch is mutated and passes otherwise.

- **Prove dead code before deleting it** — CLEAN — value 3 — effort M — risk low — category: cleanup
  Why: the pack deletes unused `fm` verbs, but nothing finds dead code in the user's project. Knip, vulture and ts-prune do. Assumption: the repo sweep (pillar 6) benefits.
  Done when: a fixture with one unreferenced function yields a CLEAN brief whose proof is a green suite after removal.

- **Generate a devcontainer and bootstrap script from the map** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: assumption: the gates and layout are already known from `fm map`. Codespaces and Devin's environment setup are the benchmark. The "bootstrap a fresh machine" idea covers only the brain, not the project.
  Done when: a generated `.devcontainer/` in a fixture repo builds and the listed gate passes inside it.

- **Add a plan editor to the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: Cline, Kiro and Cursor plan mode let users edit a plan before it runs. The pack has the stage rail but no pre-execution edit and approve step. Assumption: the web UI can write back to the task file.
  Done when: reordering two plan steps in the page changes the order `fm next` prints, and the edit is logged.

- **Resolve a symbol rename across the repo through LSP** — FEATURE — value 3 — effort M — risk med — category: code intelligence
  Why: T-0788 (LSP for blast radius and renames) is deferred. Cursor, Sourcegraph and IDEs all provide it. Assumption: `fm rename OLD NEW` is the smallest useful slice.
  Done when: renaming a fixture function updates all references including tests, and the gate stays green.

- **Run a time-boxed spike lane that self-discards** — FEATURE — value 3 — effort S — risk low — category: lanes (wild)
  Why: wild; assumption: exploratory work currently pollutes the queue and commits. A spike lane keeps only a findings note and deletes the worktree at the deadline.
  Done when: a spike lane past its deadline is removed, its note is saved, and it never appears in `git log`.

- **Walk through a PR in narrated reading order** — FEATURE — value 3 — effort M — risk low — category: review (wild)
  Why: wild; CodeRabbit gives summaries and Graphite stacks changes, but neither orders hunks by dependency. Assumption: `fm pr` and the web UI can host this page.
  Done when: for a 3-file fixture diff the page lists hunks callee-first, each with its proof line.

- **Turn ADRs into executable checks** — FEATURE — value 3 — effort M — risk med — category: architecture (wild)
  Why: wild; the pack mines boundaries from the import graph but doesn't read the user's written decisions. An ADR saying "no X in module Y" can become a gate.
  Done when: an ADR containing a `check:` line fails the gate when a fixture file violates it.

- **Show a live blast-radius preview before each edit** — FEATURE — value 3 — effort L — risk med — category: code intelligence (wild)
  Why: wild; combines the dependents-tests idea with LSP references. The web UI would show callers, tests and cards the edit touches before Claude saves it.
  Done when: opening a task for a fixture function lists its two callers and one test in the page within 2 seconds.
