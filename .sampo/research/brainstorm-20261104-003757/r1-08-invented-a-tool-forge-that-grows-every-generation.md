# Brainstorm — lens: invented: a tool forge that grows every generation

- **Add a tool-gap ledger that records every "missing tool" moment** — FEATURE — value 5 — effort S — risk low — category: tool forge
  Why: the dropped shellcheck item and "Missing tool" tasks are found ad hoc; nothing counts how often a session reached for something absent (failed command, "command not found", denied grant, workaround script).
  Done when: `sampo tools gaps` lists the top 10 missing tools from the last 30 days with count, first/last seen and the task that hit each, from real ledger rows.

- **Build a tool-forge pipeline: need → search → build → test → quarantine → promote** — FEATURE — value 5 — effort L — risk med — category: tool forge
  Why: the mission is "finds or builds the plugin, skill, MCP server or script it lacks, tests it, uses it". `plugin/templates/mcp-server/test_server.py` exists, so a template is there, but no staged lifecycle ties it together.
  Done when: given one gap from the ledger, one command produces a script or MCP server from the template, runs its red-first test, and leaves it in a quarantine dir; promotion needs a green test plus one real call from a session path.

- **Make "forge a tool" a small-model card kind** — FEATURE — value 5 — effort M — risk low — category: small-model cards
  Why: the steer wants thousands of cards so 27B/9B/4B models match frontier. Tool-building is a repeatable shape (spec, stub, test, fixture, wire-up) that a card grid cell (kind × stack × stage × surface) can hold as numbered steps.
  Done when: `research/cards/cards.jsonl` has at least 20 tool-building cards across 4 stacks, and Smith on qwen3.5-9B builds a passing CLI wrapper from one card in a held-out scenario.

- **Grow the forge each generation by mining closed tasks for repeated hand-built scripts** — FEATURE — value 4 — effort M — risk low — category: generation growth
  Why: the standing pattern "grown every generation"; repeated command sequences across closed tasks are already in the ledgers but nothing turns them into tools.
  Done when: each generation's seed lists the N new tools or cards forged, each tied to at least 3 source tasks, and the sweep fails if the count is zero without a recorded reason.

- **Score every forged tool by calls, saves and failures, and retire the dead ones** — FEATURE — value 4 — effort M — risk low — category: tool lifecycle
  Why: the lean-substance rule says growth without measurement waits; the tool library would otherwise become another 2.4 GB of unused state.
  Done when: `sampo tools ls` shows per-tool call count, last use and failure rate, and tools unused for two generations are listed as retire candidates in the sweep.

- **Run a tool exam arm: with the tool versus without it on the same scenarios** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the standing rule requires an exam arm against the path a not-yet item replaces (selfjev-4b, jeff, Jevlike, Von); the same applies to forged tools.
  Done when: `sampo exam` prints a tool row with pass/cost deltas on held-out scenarios, and a tool with no gain is flagged, not promoted.

- **Sandbox-test every forged tool under the Ward before first use** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: the injection and supply-chain defenses are deferred (T-0791), and the rules forbid installs; a self-built tool runs unreviewed code in bypass sessions.
  Done when: a forged tool's first run is in a scratch home with no network, its file opens and commands pass through the Ward exam, and a planted tool that tries `rm -rf` or an outbound call is refused.

- **Prefer a build over an install and record the reason** — FEATURE — value 3 — effort S — risk low — category: tool forge
  Why: the user's standing rule says no software installs, and install grants queue. A decision step "script it ourselves in under N lines" avoids waiting on a grant.
  Done when: for each gap, the forge prints a choice (existing local, build, queue grant) with a one-line reason, and the grant queue only receives items where build was judged impractical.

- **Wild: a tool bazaar where local models bid to build a tool and the Exam picks the winner** — FEATURE — value 4 — effort L — risk med — category: tournament
  Why: wild. Nightly idle hardware, several local models (27B, 9B, gpt-oss 20B); a tool spec goes to each, and the version that passes the held-out test at the lowest cost wins and records which model builds which kind best.
  Done when: one night's run produces a table of model × tool-kind with pass rates, and the winning tool is promoted only if it beats the runner-up on the held-out cases.

- **Wild: let a tool grow its own sibling when it fails** — FEATURE — value 3 — effort M — risk med — category: self-extension
  Why: wild. A forged tool that fails on an input class writes a failing case, then the forge builds a variant for that class; the pair is kept only if the combined pass rate rises.
  Done when: a seeded failure produces a new case, a variant tool, and a before/after pass rate in the tool's record.

- **Wild: a tool graveyard that teaches** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: wild. Per the "no idea killed" rule, retired and failed tools go into a searchable graveyard with their blocker, and a new gap checks it first so no one rebuilds the same dead end.
  Done when: forging a tool whose gap matches a graveyard entry prints the entry and its blocker before any build starts.

- **Detect a native replacement before building** — FEATURE — value 4 — effort S — risk low — category: reuse
  Why: the questions list asks who retires a verb when the host overlaps it; building a tool the host already has repeats that waste.
  Done when: before forging, the forge probes the host's tool list, `fm plugins find` and the stack cards, and reports a match with its name, so a duplicate is not built.

- **Publish forged tools as signed cards for other harnesses** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: the project says it is not Claude-specific; a tool that only works under one harness shrinks the lift.
  Done when: a forged tool exports as a script plus a card that runs under Codex or opencode in a scratch home, with the same test passing.

Next question: Which gaps are tools versus missing knowledge a card could fill, and does the ledger tell them apart?
Next question: What stops a forged tool from becoming the next thing the user must prune?
