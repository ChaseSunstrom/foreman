# Brainstorm — lens: simplicity

- **Collect the human-only chores into one copy-paste page** — FEATURE — value 4 — effort S — risk low — category: blockers
  Why: T-0325 (`sudo pacman -S libappindicator-gtk3`), T-0418 (update foreman-ui to 0.6.1), T-0352 and T-0431 (publish, release) are blocked or deferred only because they need the user, and each sits in the queue as a task. Assumption: the user would rather clear them in one sitting than answer them one at a time.
  Done when: `fm chores` prints every blocked-on-user task with its exact command, and running one marks its task unblocked.

- **Show live work by default and count the rest** — CLEAN — value 4 — effort S — risk low — category: queue view
  Why: Open work lists about 30 tasks, and 20 or more are deferred, captured or blocked. The live ones drown.
  Done when: `fm task list` prints only planned and active tasks plus one line such as "22 later, 4 blocked (--all)", and `--all` restores the full list.

- **Cut Foreman's nouns to ten and lint for the rest** — CLEAN — value 3 — effort M — risk low — category: vocabulary
  Why: The pack uses lane, drive, band, pane, cockpit, mod, ledger, brief, board, catalogue, pack, cluster, round and more. Each is another thing the user has to learn.
  Done when: a glossary file lists at most 10 user-facing terms with a one-line definition each, and a test fails if `fm` output or MASTER.md uses a retired term.

- **Resolve any id with one verb, `fm show <anything>`** — FEATURE — value 3 — effort S — risk low — category: CLI
  Why: Task ids, brainstorm ids, clusters and research ids live in separate namespaces. Round 1 added `fm research list/show` beside `fm task show`.
  Done when: `fm show T-0818`, a brainstorm id and a cluster name each print the right record, and an unknown id suggests the nearest match.

- **Emit every hook result through one helper** — CLEAN — value 3 — effort M — risk med — category: hooks
  Why: Round 1 added `sessionTitle`, Stop-hook push asks, compact-output rewrites and monitors.json, each shaping its own hook JSON. T-0777 needed a test just to check the keys. Assumption: the shaping is currently scattered across modules.
  Done when: one `emit()` function builds all hookSpecificOutput payloads, no other module writes those keys, and a grep test enforces that.

- **Give every question one of three shapes** — CLEAN — value 3 — effort M — risk low — category: interaction
  Why: The user is asked for a yes on compact output, grants, plan approval and more, each phrased differently, and nobody has ticked the board.
  Done when: every `fm ask` is yes/no, pick-one-of-3 or free text, each with a default and a deadline, and a lint rejects any other form.

- **Fold close warnings into one verdict line** — CLEAN — value 3 — effort S — risk low — category: close-out
  Why: Tier drift, left-behind files and self-docs failures are separate warnings, and round 1 spent two tasks fixing their false positives (T-0812).
  Done when: `fm task finish` ends in either "closed clean" or "closed, 1 thing to look at: X", with the full list behind `--detail`.

- **Build tests from one shared scenario builder** — CLEAN — value 3 — effort M — risk med — category: tests
  Why: `plugin/tests/` has 154 files against 50 lib modules, plus fixture repos. Each new test re-creates its own world, which slows the suite and makes tests costly to add. Assumption: setup is duplicated.
  Done when: a `scenario()` helper builds a project, queue and ledger in one call, and at least 20 tests migrate to it with fewer total lines.

- **Hibernate idle projects to guard-only (wild)** — FEATURE — value 3 — effort M — risk med — category: hooks
  Why: Hook tax is paid on every turn in every Foreman project, even ones untouched for weeks. Assumption: such projects exist.
  Done when: after N quiet days a project loads only the guard hook, the first prompt wakes the full set, and the bench shows lower p50 in a hibernated project.

- **Run a ceremony holdout on every tenth S task (wild)** — FEATURE — value 4 — effort M — risk med — category: proof of value
  Why: The ablation ideas run on bench, not on real work. The user keeps pushing for "smarter, faster", so live evidence of what the ceremony earns would settle it.
  Done when: tasks flagged as holdout skip planning ceremony but keep the guard and done-gate, and `fm` reports first-pass rate and minutes for ceremony versus holdout.

- **Make every recursive round net-zero in surface (wild)** — CLEAN — value 4 — effort S — risk low — category: rounds
  Why: Round 1 added a monitor, a toggle, a page renderer and several doctor probes, and the user asked for "recursively improve" without a stopping rule.
  Done when: `fm` counts verbs, flags, hooks and injected bytes at round start and close, and the round refuses to close above the starting count unless the user overrides.

- **Print a "quiet because" line when Foreman says nothing (wild)** — FEATURE — value 2 — effort S — risk low — category: trust
  Why: Silent hooks and an empty band look the same as a broken Foreman, and the unverified monitor arming in round 1 is that failure mode.
  Done when: `fm quiet` prints one line naming the last hook that ran, its decision, and why nothing was surfaced.
