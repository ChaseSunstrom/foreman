# Brainstorm — lens: capability map

- **Run hooks through a warm daemon** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: hooks run on every tool call; the pack shows `bench_hooks.py`, a "waiting hook" caught by the self-change gate (T-2605), and T-0832 (shell prefilter) deferred. Assumption: Python interpreter startup is the dominant per-call cost.
  Done when: `bench_hooks.py --runs 20` shows PreToolUse p95 at least 50% lower with the daemon on, and the guard still blocks when the daemon is killed (fails closed).

- **Select tests by impact during a task, run the full suite at ship** — PERFORMANCE — value 4 — effort M — risk med — category: test speed
  Why: plugin/tests has 404 files and every `fm ship` runs the full suite (push grant rule). Assumption: a loop that reruns everything on each proof is slow.
  Done when: `fm prove` on a one-module change runs only tests that import that module, prints the count skipped, and `fm ship` still runs all.

- **Predict file overlap between queued tasks and schedule lanes around it** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: T-0792 (lanes and fleet) is deferred and Missions 5–8 already run S/M briefs in parallel lanes, merged in order. Merge conflicts are the obvious failure there.
  Done when: `fm lanes plan` takes 6 queued tasks and outputs batches with no shared predicted files, and a test with two overlapping tasks puts them in different batches.

- **Profile a session's time as a flame bar** — FEATURE — value 3 — effort M — risk low — category: performance
  Why: `fm cost` counts tokens and hook chars but nothing in the pack splits wall time into thinking, tool, test wait and hook wait. Assumption: the transcript has timestamps.
  Done when: `fm profile <session>` prints percentages by bucket that sum to 100% of wall time, and the web UI shows the same bar.

- **Speak Agent Client Protocol so editors can host `fm code`** — FEATURE — value 4 — effort L — risk med — category: devices
  Why: the surface is the terminal and a web UI; "Foreman isn't specific to Claude Code" is a standing rule. Zed and other ACP editors would otherwise need an adapter per harness. Assumption: ACP is stable enough to target.
  Done when: an ACP client starts `fm code --acp`, sends a prompt, and receives streamed tool calls plus the finish receipt.

- **Install the guard and the task-id check as git hooks** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: Foreman covers agent sessions only; a human committing in the same repo bypasses the proof discipline. Assumption: users commit by hand too.
  Done when: `fm hooks install` adds commit-msg and pre-push hooks. A commit with no task id is refused, and the hooks are removable with one command.

- **Complete `fm` in bash, zsh and fish, including task ids and verbs** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the verb count is large (open tasks reference dozens of `fm` subcommands) and ids like T-2624 are hard to type. Assumption: no completion exists.
  Done when: `fm task show T-26<TAB>` completes from the live queue in all three shells, with a test per shell.

- **Keep the injected prefix byte-stable to hit the prompt cache** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: injected chars per session are already measured by the lean ratchet; reordering volatile notes after stable rules could raise cache hits. Assumption: current injections interleave changing text early.
  Done when: two consecutive sessions on the same repo show an identical first N injected bytes, and `fm cost` reports a cache-read share that rises versus the current baseline.

- **Resolve `fm config` values with their source** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: behavior is steered by flags and env vars (`FOREMAN_QUIET`, `--round-first`, `--pace off`) with no single place that says what is in effect. This is "explain", not the earlier "three presets" idea.
  Done when: `fm config explain pace` prints the effective value and the layer that set it (default, repo, user, env, flag).

- **Wild: Make ledgers merge cleanly across machines** — FEATURE — value 4 — effort L — risk high — category: devices (wild)
  Why: assumption: the user runs Foreman on a laptop, a night box and possibly a phone; append-only ledgers with ids can merge as a CRDT or git merge driver.
  Done when: two clones append different bets and tasks offline, `fm sync` merges them with no lost or duplicated records, and every reader gives the same answer on both.

- **Wild: Hover any `T-####` in the editor to see its receipt** — FEATURE — value 3 — effort M — risk low — category: developer experience (wild)
  Why: task ids appear in commits, comments and docs ("clickable ids everywhere" is only for the terminal and web UI). A small LSP gives hover, go-to-task and a CodeLens showing proven, unproven or overridden.
  Done when: in an LSP client, hovering `T-2616` in a commit message or source comment shows its title, status and proof lines.

- **Wild: Land the best verified partial when a task runs out of time** — FEATURE — value 3 — effort M — risk med — category: agents (wild)
  Why: T-0831 (salvage partial results from capped children) is deferred, and the user said not to stop work for budget. Give each task a wall-clock budget, checkpoint at each green proof, and on expiry land only the last verified slice and file the remainder.
  Done when: a task killed at its budget leaves a commit whose proof passes plus a new queued task naming what's left.

- **Wild: Run a task's proof in a throwaway container as the arbiter** — SECURITY — value 3 — effort M — risk med — category: verification (wild)
  Why: proofs are commands the agent ran in its own environment, which may carry state the agent set up. Re-run the proof command in a clean container from the committed tree. Assumption: a container runtime is present.
  Done when: `fm prove --clean` reruns the recorded commands in a fresh checkout, and a test where the proof depends on an uncommitted file fails there.

- **Offer a single-file `fm doctor` fix-it mode that applies safe repairs** — FEATURE — value 3 — effort M — risk med — category: simplicity
  Why: doctor reports many conditions (timers, steer checks, missing parts) but the pack shows only manual remediation. Fixes would be idempotent and logged.
  Done when: `fm doctor --fix` repairs a planted stale timer and a missing steer check, prints each change, and a second run changes nothing.

Next question: Which fm verbs does the user actually run in a week, and what is the median wall time of each, so performance work targets what they feel?
Next question: What would a second human on the same repo need that a single-user ledger design can't give them (identity, locks, review of each other's overrides)?
