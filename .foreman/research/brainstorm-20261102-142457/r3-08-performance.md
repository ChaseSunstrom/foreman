# Brainstorm — lens: performance

Lens: performance. I took this as speed, token spend and footprint for #12, and put the extra ideas in the thin areas (ui, agents). Nothing here repeats the list above. The existing warm daemon, impacted-tests, prove cache, incremental readers and render-budget ideas are assumed as a base.

- **Dedupe repeated file reads inside a session** — FEATURE — value 4 — effort M — risk med — category: tokens
  Why: assumption: agents re-read unchanged files and re-run `fm status` many times per task, and the ideas above cap output size but never remove the repeat itself.
  Done when: a PostToolUse/PreToolUse hook answers a second Read of an unchanged file (same mtime and hash) with a one-line "unchanged since step N" note, and a bench transcript shows fewer input tokens with the proof results identical.

- **Print only the delta on repeat calls to status verbs** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: assumption: `fm status`, `fm next` and `fm doctor` are called repeatedly in one session and each time prints the whole state.
  Done when: a second `fm status` in the same session prints only what changed since the first (or "no change"), and `--full` restores the old output.

- **Send non-urgent model children through a batch tier** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: the pack shows many deferred reads: cold reads, exam scenarios, overnight dream passes and brainstorm re-grounding. None of them blocks the user, so they could take a cheaper, slower path. Assumption: a batch endpoint exists for the provider in use.
  Done when: a `--when-idle` child class submits as a batch job, its result lands in the same ledger as a live child's, and the receipt shows the cost split between live and batch.

- **Hedge straggler lanes** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: assumption: lane durations have a long tail, since the pack says tasks are "forecast" and "scored". Races exist for L framings, but nothing duplicates a lane that overruns its own forecast.
  Done when: a lane past 2× its forecast median spawns one duplicate on a different approach, the first to pass proof wins, the loser is reaped, and the receipt names the extra cost.

- **Choose reasoning effort per step, separately from model** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: T-1266 (ceremony profile per task kind and model) and "route to the cheapest model" cover model choice, not thinking budget. Assumption: the effort setting is configurable per child.
  Done when: planning, edit and cold-read children each read an effort level from a table fed by outcome data, and a replay on 30 closed tasks shows equal or better first-pass rate at lower tokens.

- **Memoize every pure verb by input tree hash** — PERFORMANCE — value 4 — effort M — risk low — category: caching
  Why: the pack names a prove cache and an incremental map, but `fm find`, doctor checks and `fm map` each have their own cache or none at all. One content-addressed memo keyed by verb, args and tree hash would cover them all.
  Done when: a second run of an unchanged `fm find` returns in under 50 ms with a "cached" mark, and touching one file invalidates only the entries that read it.

- **Reflink-clone test fixture worlds** — PERFORMANCE — value 3 — effort M — risk low — category: tests
  Why: `plugin/tests` has 414 files and a fixtures dir. Assumption: many tests rebuild a repo or state dir from scratch, and ship-gate time scales with that setup.
  Done when: a shared prebuilt fixture is cloned with `cp --reflink=auto` (or `git worktree` as the fallback) in the slowest ten test files, and the suite's wall-clock drops by a measured amount with unchanged results.

- **Run the ship gate as a dependency graph with a critical-path report** — PERFORMANCE — value 3 — effort M — risk med — category: gate
  Why: the gates are listed as separate commands: `fm doctor`, the e2e roundtrip and the hook bench. The ideas above split fast and full runs but never run the stages concurrently.
  Done when: independent gate stages run in parallel, the output names the slowest chain, and a failing stage cancels the rest early.

- **Precompile bytecode into a writable cache prefix at install** — PERFORMANCE — value 2 — effort S — risk low — category: startup
  Why: assumption: the install dir may be read-only and `__pycache__` can't be written on a hardened host, so every hook cold start recompiles `plugin/lib`.
  Done when: `install.sh` sets a prefix and warms it, and the hook bench's cold p95 improves with the install dir read-only.

- **Stream ledger changes to the web UI** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: ui is thin so far. Assumption: the web UI re-fetches whole views, which hurts at 10k tasks and the polled Today charts.
  Done when: the server sends ETags plus a ledger-offset SSE feed, a view updates from appended lines only, and idle polling traffic falls to near zero.

- **Show a live "waiting on" strip** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: the user can't tell model latency from Foreman overhead during a pause. The pack has a flame bar idea, but nothing breaks a single pause into model, tool, proof and Foreman time as it happens.
  Done when: the pane shows a live four-way split for the current step, and its overhead figure matches the hook bench within 10%.

- **Wild: let a content-addressed memo follow the user across their machines** — FEATURE — value 3 — effort L — risk med — category: caching
  Why: wild. The memo above plus a verified-sync folder means a proof run on the desktop is free on the laptop. Assumption: tree hashes are stable across hosts.
  Done when: a proof cached on host A is reused on host B for the same tree hash and tagged "from A", and a mismatched toolchain version refuses reuse.

- **Wild: pre-warm lanes from queue prediction** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. Idle CPU builds worktrees, `fm map` and the test selection for the next two tasks `fm next` is likely to offer, so the start is instant.
  Done when: starting a predicted task skips setup, the receipt shows the saved seconds, and a wrong guess is cleaned up with nothing left behind.

- **Wild: a hostile-slow host simulator** — FEATURE — value 2 — effort M — risk low — category: testing
  Why: wild. Run the hook and drive suites under cgroup CPU and IO throttles and a 5× slow disk, to find which gates, timeouts and "dead timer" detectors misfire on a weak machine.
  Done when: a nightly matrix run lists every timeout that trips under throttling and names the fix.

Next question: which of Foreman's own overheads (hooks, injected context, gates) does the user actually feel as waiting, and have they ever measured it against the time the model spends thinking?
Next question: where does a closed task's wall-clock go by phase, and is it mostly model, proof, or queue wait?
