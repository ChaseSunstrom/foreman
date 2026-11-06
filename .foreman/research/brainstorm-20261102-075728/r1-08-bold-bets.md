# Brainstorm — lens: bold bets

- **Cut a self-contained capsule for every plan row** — FEATURE — value 5 — effort M — risk low — category: agents
  Why: the goal must survive crashes and compactions, and the pack shows cold resumes and `fm code` weak models needing re-derived context. Assumption: a row's context today is rebuilt from the whole goal file.
  Done when: a fresh session given only one row's capsule (≤2k tokens: acceptance text, probe, touched files, upstream decisions) completes that row in a test fixture without reading the goal file.

- **Build contract-first so lanes run in parallel** — FEATURE — value 5 — effort L — risk med — category: agents
  Why: Missions 5-8 already run S/M briefs in parallel lanes merged in order, but the pack shows no interface step. Assumption: lanes that collide on shared interfaces get serialized or conflict at merge.
  Done when: for a two-lane fixture goal, a contracts row (stubs plus contract tests) lands first, both lanes build against it, and merge produces zero interface conflicts and a green contract suite.

- **Run the finish oracle incrementally by dependency hash** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: oracles re-run at resume, at sweep, at ship and on "re-run each cell's probe". Assumption: a full re-run costs minutes of wall time and tokens each time.
  Done when: after touching one file, the oracle re-runs only the probes whose recorded dependency set contains it, and a forced full run gives the same verdict.

- **Lock the goal's environment at plan time and verify it on resume** — FIX — value 4 — effort M — risk low — category: reliability
  Why: tmpfs runway, per-machine quirks, a hardened kernel and host CLI drift all appear as failure sources. Assumption: nothing records toolchain versions, ports and env for a multi-day goal.
  Done when: changing a pinned tool version between sessions makes resume name the exact drift and re-prove the rows that depended on it.

- **Fence a goal's egress and credentials** — SECURITY — value 4 — effort M — risk med — category: security
  Why: the pack plans a write fence and treats issue/CI text as hostile. Assumption: no per-goal network-domain or secret scope exists, so an unattended multi-day goal runs with the session's ambient reach.
  Done when: a goal declaring `egress: [github.com]` has a `curl` to another host denied by the guard with a one-line reason, and the denial is logged.

- **Serve the goal as an MCP resource any harness can read and lease rows from** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: Codex, Gemini and opencode lack the Stop and drive hooks (T-0335, T-0337), and the standing rule says Foreman is not Claude-specific. Assumption: goal state is only reachable by `fm` verbs.
  Done when: a non-Claude client lists rows, leases one and submits evidence through MCP, and the lease blocks a second writer.

- **Generate living architecture docs from closed rows, and fail when they go stale** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: the docs thin-spot is open and the repo has 1388 skill files plus MASTER.md clauses. Assumption: finished goals leave no durable "how it fits together" artifact.
  Done when: closing a row appends its module clause to the architecture doc, and renaming a cited symbol turns a doc-staleness check red.

- **Keep a goal flight recorder with tamper-evident segments across compactions** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the plan must be carried across crashes, and the user already asks "where were we". Assumption: the journal has no segment hashing, so a torn or edited record is undetected.
  Done when: editing one past record makes `fm goal verify` name the first bad segment, and replay up to it still reconstructs state.

- **Wild: judge the finished product with the user's verbatim first sentence** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: assumption: decomposition drifts from the original wish. A blind cold child that sees only the raw goal text and the running product rates fit against it, without seeing the plan.
  Done when: on a fixture goal where a row was silently dropped, the blind judge's miss list names the dropped capability.

- **Wild: run rival builds on two harnesses and cherry-pick winning rows** — FEATURE — value 4 — effort L — risk high — category: agents
  Why: the pack proposes building twice on cheap models to diff capability lists, but none of the earlier ideas merge the results. Assumption: row-level oracles are independent enough to merge.
  Done when: two worktrees built by different harnesses are merged row by row, and the merged tree passes the full oracle with at least as many green rows as either alone.

- **Wild: generate a maintenance runway at finish** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: "done" is not "stopped", but nothing says what rots after done. Assumption: deprecations, dependency EOLs and retiring model IDs arrive within months.
  Done when: finishing a goal writes a dated runway file (EOL dates, pinned IDs, expected breakages) and a fake clock at +120 days raises the matching wake task.

- **Wild: ship a goal-in-a-bottle replay package** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: the user wants to show or hand off a multi-day goal. One redacted file carries the plan, the evidence receipts and a scrubbable timeline.
  Done when: opening the file offline on another machine replays the goal's rows and receipts with no network and no Foreman state.

- **Cap resume cost with a measured token budget per goal** — PERFORMANCE — value 3 — effort S — risk low — category: simplicity
  Why: the pack asks for "measure the cost of resuming" and has lean ratchets for static metrics. Assumption: resume cost grows with goal age.
  Done when: resume tokens for a 30-row fixture goal stay under a recorded ceiling, and the ratchet trips with the responsible commit when exceeded.

Next question: Which of these needs a user's real multi-day goal to evaluate, and what is the cheapest way to get one without Foreman authoring the data?
Next question: Where does a goal span more than one repo or more than one person, and which of the above breaks first?
