# Brainstorm — lens: capability map

- **Derive gates from the repo's own CI config** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: assumption: gates are hand-written or guessed per project, and nothing in the pack shows Foreman reading `.github/workflows`, a Makefile or `tox.ini`. Those files already say what "green" means.
  Done when: on a fixture repo with a workflow file, `fm check --from-ci` lists the test and lint steps and runs them, and flags any step it can't run locally.

- **Respect monorepo workspaces** — FEATURE — value 4 — effort L — risk med — category: monorepo
  Why: assumption: the map treats the repo as one tree. pnpm, cargo, go and uv workspaces need per-package gates and per-package "affected" selection.
  Done when: in a fixture with three workspace packages, a diff touching one runs only that package and its dependents' tests, and the plan names the packages.

- **Share one build cache across lanes** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: lanes get fresh worktrees, so each rebuilds from cold. Pointing sccache, `CARGO_TARGET_DIR`, the npm/pnpm store and `UV_CACHE_DIR` at one per-project cache cuts that cost. The pack shows lane forking but no cache sharing. Assumption: the cold-build cost is large enough to matter.
  Done when: the second lane's first gate run on a fixture is measurably faster than the first lane's, and `fm doctor` reports the cache hit rate.

- **Run last-failed tests first on every runner** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: affected-test selection is covered, but ordering within the selection isn't. A fix attempt that fails should fail in seconds. Assumption: the pytest `--lf`, jest `--onlyFailures` and nextest equivalents are reachable from the runner adapters.
  Done when: after a red run, the next `fm check` executes the previously failed tests first and its time to first failure is logged.

- **Census Foreman's own background footprint** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: the pack shows watchers, monitors, a bus and a possible daemon, but only hook latency is measured. Idle CPU, RSS and open files of Foreman's own processes aren't.
  Done when: `fm doctor --footprint` prints each Foreman process with CPU, RSS and age, and fails above a configured ceiling.

- **Preflight an agent's required tools before spawning it** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: assumption: a reviewer or recon agent that needs an MCP server, LSP or browser that is down fails mid-run, after spending budget. Each agent definition should declare what it needs and be checked first.
  Done when: spawning an agent whose declared tool is unavailable is refused with the reason and a fallback agent, with no child process started.

- **Kill and salvage stalled subagents** — FIX — value 4 — effort S — risk med — category: agents
  Why: budget and turn-limit salvage exists, but a subagent that makes no tool call for N minutes is a different failure. It still holds a lane and delays the queue. Assumption: stalls without budget exhaustion occur.
  Done when: a stub agent that sleeps past the stall limit is terminated, its partial output is saved to a file, and the task gets a typed "stalled" result.

- **Show a per-agent trace timeline** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: agents have effort and turn caps, but the pack shows nothing that explains where one agent's time and tokens went. `fm agents trace ID` would show tool calls, waits and tokens per step.
  Done when: after a fixture agent run, `fm agents trace` prints an ordered timeline whose totals match the cost ledger within rounding.

- **Route changes by CODEOWNERS** — FEATURE — value 3 — effort S — risk low — category: review
  Why: assumption: team repos have a CODEOWNERS file. Foreman could flag a task touching files owned by someone else, put the owners in the close-out, and suggest reviewers on the PR.
  Done when: a fixture diff touching an owned path shows its owners at plan time and in the close-out summary.

- **Export the queue as Mermaid and Gantt** — FEATURE — value 2 — effort S — risk low — category: legibility
  Why: tasks carry `depends` and effort sizes, and `fm page` already renders HTML. A dependency graph and forecast timeline would reuse that data.
  Done when: `fm page` includes a valid Mermaid graph of the open queue, checked by a parser test.

- **Wild: reproduce a failing CI run from its URL** — FEATURE — value 4 — effort L — risk med — category: ci loop
  Why: wild. Paste a failing run URL, and a lane fetches the logs with `gh`, checks out the commit, reproduces the failure locally, and files a FIX brief with the failing command as its verify. The pack has "babysit PRs" but no repro-from-URL.
  Done when: given a fixture failing-run log, the lane produces a brief whose verify command fails on the start tree.

- **Wild: pair an optimizer agent with a regression hunter on PERF tasks** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. PERF tasks are "done" when the measurement improves, but nobody attacks the win. A second agent hunts for correctness or worst-case regressions in the optimized path, and the task closes only after both finish.
  Done when: on a fixture PERF task, the hunter must run at least one adversarial input and its result appears in the evidence.

- **Wild: attach agent traces to commits as git notes** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: wild. `git log --show-notes` would then answer "why did the agent do this" in any clone, without Foreman installed. The pack covers commit trailers but not notes, and the central store doesn't travel with the repo.
  Done when: after a task close on a fixture repo, `git notes show HEAD` contains the task id, brief summary and evidence hash, and `fm doctor` verifies they match the ledger.

- **Wild: export a time sheet from the ledger** — FEATURE — value 2 — effort S — risk low — category: reporting
  Why: wild. Freelancers and consultants need hours per task. The ledger has timestamps and attributed time. CSV and ICS export would let it fill Toggl, Harvest or a calendar.
  Done when: `fm time --csv --since 7d` outputs per-task durations that sum to the ledger's active time within 1%.
