# Brainstorm — lens: capability map

- **Pin behaviour before a CLEAN task changes it** — FEATURE — value 4 — effort M — risk low — category: correctness
  Why: assumption: the pack shows `fm task prove` (a red test first) for FIX tasks, but nothing equivalent for CLEAN refactors, which are the likeliest to change behaviour silently.
  Done when: a CLEAN task cannot close until characterization tests exist, pass on the start tree and still pass after the change.

- **Land each task as one commit per plan step, in the repo's own commit style** — FEATURE — value 4 — effort M — risk low — category: git
  Why: the step pointer and `fm task finish --commit` exist, but a task lands as one lump. Aider-style per-step commits make review and bisect cheap. Assumption: commit style can be learned from `git log`.
  Done when: finishing a 3-step task on a fixture repo yields 3 commits whose subjects match the repo's prefix convention, and `git bisect` can land on any one of them.

- **Give parallel lanes their own ports, databases and temp dirs** — FIX — value 4 — effort M — risk med — category: lanes
  Why: lanes and fleet exist, and the pack proposes a shared build cache across lanes, but nothing prevents two lanes' test suites from colliding on port 3000, a SQLite file or `/tmp/x`. Assumption: this has bitten, or will once lanes run tests concurrently.
  Done when: two lanes run the same port-binding test suite at once and both go green, with `FM_LANE_PORT_BASE` and similar variables injected.

- **Close UI tasks with before/after screenshots and an accessibility audit** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the pack proposes native browser verification and screenshot-to-test, but not the visual diff and axe-style checks that a design-led reviewer expects as evidence for web UI work.
  Done when: a UI task's evidence file holds paired screenshots plus an a11y violation count, and a new violation versus the start tree blocks close.

- **Gate public API breaks at close** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: assumption: the map already knows exported symbols (it has symbol linking). A diff of exported names, CLI flags and config keys, with a required CHANGELOG or semver note, is a standard best-in-class gate that isn't in the pack.
  Done when: removing an exported function on a fixture fails close until a changelog line or an explicit "breaking" marker is present.

- **Review a teammate's PR by running it** — FEATURE — value 4 — effort L — risk med — category: review
  Why: T-0034 (`fm audit run`) is deferred, and "ingest PR review comments" goes the other direction. CodeRabbit-style tools only read the diff; Foreman can check out the branch, run affected tests, and probe the claims in the PR description.
  Done when: `fm review <PR-url>` writes a findings file (read-only, in a throwaway lane) in which every finding cites a command output.

- **Require a profile diff as evidence on PERF tasks** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: a PERF task type exists (the user's first ask above is PERF), but nothing demands a measured before/after. Assumption: py-spy, `perf` or the language's own profiler is detectable from the map.
  Done when: closing a PERF task without a before/after profile or benchmark in its evidence is refused, with a prefilled command to produce one.

- **Check new dependencies at close** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the pack has install jails and advisory ranking, but no gate on what a diff newly adds to a manifest (licence, last release, install scripts, size).
  Done when: adding a dependency with an incompatible licence to a fixture manifest produces a close warning naming it, and the warning is silent when no manifest changed.

- **Prove migrations are reversible and dry-run them** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: the pack interlocks production commands, but schema migrations that pass tests and then can't roll back are a classic unattended-run hazard. Assumption: the project has a migration directory Foreman can detect.
  Done when: a task that adds a migration must show an up and a down run on a scratch database, or close names the missing proof.

- **Predict lane merge conflicts at plan time** — FEATURE — value 3 — effort M — risk low — category: fleet
  Why: the pack has lane base checks and fleet work, but sequencing is only done after the fact. The map plus each step's named files can flag overlapping queue items before they fork.
  Done when: two queued tasks that name the same file are serialized or flagged in `fm plan`, and independent tasks still run in parallel.

- **Export decisions as ADR files** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: Foreman records decisions centrally, but a teammate without Foreman never sees them. Plain markdown in `docs/adr/` is the form people expect and keep.
  Done when: closing a task that recorded a decision writes a numbered ADR file, and doing it again is idempotent.

- **Emit local OpenTelemetry traces for tasks, hooks and gates** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the pack proposes Perfetto and SARIF exports, but teams already run OTel collectors and Grafana or Jaeger. Local-only by default, per the privacy lens.
  Done when: with `FM_OTLP=localhost:4317`, a task produces spans for each hook and gate that a stock collector accepts, and nothing is sent when unset.

- **wild: Extend evidence beyond code with non-code verification packs** — FEATURE — value 4 — effort L — risk med — category: reach
  Why: wild; assumption: Office/PDF skills (`--docs`) hint that users already do documents and research. Checks such as link-check, citation resolution, spreadsheet recalculation and doc build would let the discipline layer cover work no code-only rival touches.
  Done when: a seeded docs task with a dead link and a bad citation cannot close until both are fixed, with the checker output recorded as evidence.

- **wild: Run spike mode, a task whose output is a finding and whose code is discarded** — FEATURE — value 3 — effort S — risk low — category: exploration
  Why: wild; RESEARCH tasks exist and worktree experiments are proposed, but there's no first-class "explore, then throw it away and keep only the written conclusion" form that stops a spike turning into unreviewed code.
  Done when: finishing a spike removes its worktree, leaves the main tree byte-identical, and stores a finding with the commands that support it.

- **wild: Watch the human's own saves and speak up with the affected red test** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; T-0214 (edit-time sentinel) and the human git-hook idea cover Claude's edits and commits, but not the user typing in their editor. A small background watcher would make Foreman worth keeping even in sessions where Claude is idle.
  Done when: saving a file with a broken linked test in an editor produces a one-line notice within 5 s, and the watcher costs near-zero CPU when idle.
