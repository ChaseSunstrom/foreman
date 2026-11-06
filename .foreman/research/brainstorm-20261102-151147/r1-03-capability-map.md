# Brainstorm — lens: capability map

- **Resolve merge and rebase conflicts with a proof from both sides** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: assumption: conflicts are the most common reason a lane's work stalls. The pack covers merging lanes in a scratch worktree (`fm lane --plan`) but not resolving the conflicts that merge produces. Nothing there says how a resolution is shown to keep both sides' behaviour.
  Done when: on a fixture repo with a planted conflict, `fm resolve` produces a merge whose tests from both parent branches pass, and the receipt names which tests came from which side.

- **Turn review comments on the user's own PR into tasks, with replies that cite proof** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the pack covers reviewing someone else's PR and posting a proof comment, but not the return trip. After the user's PR draws "please change X", nothing files that as a task, fixes it, and answers each comment with a receipt. assumption: `gh` or the forge API is available.
  Done when: given a recorded review-comments JSON fixture, `fm review-back` files one task per actionable comment, and each task closes with a reply draft that quotes its proof id (nothing is posted without a grant).

- **Add `fm prove --api`: public API surface diff with semver verdict** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: assumption: a "no behaviour change" or "safe refactor" claim often breaks an exported symbol, and none of the pack's provers catch that. The pack has differential runs and N-1 compatibility, but no kind that compares exported symbols. It would reuse tools such as griffe, cargo-semver-checks and api-extractor, found from manifests.
  Done when: a fixture removing one public function makes `--api` report "breaking: removed foo()". The same fixture with only a private change reports "none".

- **Search every past session and ledger with local full-text search (`fm recall --grep`)** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the pack lets the user ask "did we ever check X?" of the ledger. It has no search over transcripts, steers, receipts and decisions together, and users keep re-pasting steers (e.g. "Answer a re-pasted steer with the task that already did it"). SQLite FTS5 is in Python's stdlib, so there is no new dependency.
  Done when: searching a phrase from a recorded fixture session returns that session's id and line, built from a derived index that `fm doctor` can rebuild.

- **Retire stale feature flags and dead config with a proof lane** — FEATURE — value 3 — effort M — risk med — category: simplicity
  Why: assumption: user repos accumulate flags that are always on or off. The pack covers dead Python and unused verbs, but not the user's own flag debt. The lane would detect flags whose value never varies in config history, remove the dead branch, and prove it by differential run.
  Done when: a fixture with one always-true flag gets a removal task whose proof shows the test suite passes and the flag's name appears nowhere afterwards.

- **Revert formatting churn the agent introduced outside the lines it meant to change** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: assumption: this is a common complaint about coding agents (whitespace and import-order noise inflating review). The pack splits mechanical bulk from semantic changes in big diffs, but does not remove churn at source. The step would run the repo's formatter only on touched hunks and drop whitespace-only hunks elsewhere.
  Done when: a fixture edit that also reflows an untouched function lands with the untouched function byte-identical.

- **Check dependency licences and snippet provenance on every diff** — SECURITY — value 3 — effort M — risk low — category: security
  Why: the pack inventories dependency advisories and catches hallucinated package names, but a new GPL dependency or pasted licensed code gets no check. This is a standard gate in enterprise tools. Licences come from manifests, and clone detection runs against a local corpus only.
  Done when: adding a fixture dependency under a licence the repo's allowlist rejects makes `fm check` fail with the package and licence named.

- **Generate man pages and `fm help --search` from the verb table** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: the pack already derives completions and did-you-mean from the verb table, but there is no `man fm` or keyword search over verb help. With 100+ verbs a newcomer can't find "that one verb". The same table could drive it.
  Done when: `man fm-prove` renders from generated roff and `fm help --search budget` lists the verbs whose help mentions it. A test fails if any verb lacks a man entry.

- **(wild) Record failing and flaky tests under `rr` and ship the replayable trace as evidence** — FEATURE — value 3 — effort L — risk med — category: reliability
  Why: wild. A nondeterministic failure is the hardest thing to prove fixed; the pack's only handling is flake quarantine and rates. An `rr` trace lets a later session step backwards to the cause. It is Linux and x86 only, so it needs a clean fallback.
  Done when: on a fixture race test that fails 1 time in 5, `fm prove --record` stores a trace from the first failing run and `rr replay` on it reproduces the failure deterministically.

- **(wild) Answer "how does X work here?" only with citations a checker has verified** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: wild. The pack already rejects cold-read FAILs whose quoted line doesn't exist, but the idea hasn't reached everyday answers. An `fm explain` would drop or flag any file:line claim that fails a grep. It extends the onboarding items (newcomer tour, `fm why`) with a hallucination check.
  Done when: planting one invented `file:line` into a canned answer makes the verifier mark that citation unverified and the output shows it struck through.

- **(wild) Report the energy and carbon cost of agent runs and CI re-runs** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild and playful. The pack has per-task dollar and minute receipts but nothing in other units. A rough kWh and gCO2 estimate from tokens and CPU-seconds, with clearly labelled coefficients, would give the spend receipt a line people show others. It also rewards the cache and skip-rerun ideas already listed.
  Done when: the drive receipt prints "~X Wh (estimate; coefficients in file)" and a test confirms that skipping a rerun by cache lowers the figure.

- **Apply one change across several registered repos with a rollup receipt** — FEATURE — value 3 — effort L — risk high — category: agents
  Why: assumption: the user has more than one repo. The pack lists "tick every registered repo" and "prime neighbour repos", but no change that spans repos (a library bump plus its consumers, as in Sourcegraph batch changes). Each repo runs its own gates and a push still needs a grant.
  Done when: on two fixture repos, `fm batch` branches both and runs each one's gate. The rollup shows pass or fail per repo, and a failing repo leaves the other unpushed.

- **Export closed tasks as billable time entries** — FEATURE — value 2 — effort S — risk low — category: user value
  Why: assumption: some users bill hours or report effort. The ledger already has task start and close times plus the wage meter idea, but nothing exports them in a Toggl or CSV shape. Idle gaps would be trimmed with a documented rule.
  Done when: `fm timesheet --month` writes a CSV with one row per closed task, and a fixture with a six-hour idle gap shows that gap excluded.

Next question: which of these capabilities do the user's actual repos (language mix, forge, solo or team) need, as opposed to what rival tools ship?
Next question: which blocked tasks (T-0335/36/37, T-0352) would a capability-by-capability conformance run against real third-party CLIs unblock?
