# Brainstorm — lens: reliability

- **Pin every task's start point as a git ref** — FIX — value 4 — effort S — risk low — category: git state
  Why: T-0812 showed lane-merged tasks losing their start point and the close check seeing an empty diff. A raw SHA has the same weakness after a user rebase, amend, or gc. Assumption: start points are stored as bare SHAs.
  Done when: a test records a start point, rebases and amends the branch, runs `gc --prune=now`, and the close check still computes the original diff.

- **Run a git-topology matrix over every git-reading verb** — FEATURE — value 4 — effort M — risk low — category: git state
  Why: assumption: the suite mostly runs on plain clones. Linked worktrees (Claude Code's `.claude/worktrees` is one), submodules, shallow clones, sparse checkouts, empty repos, and detached HEAD or mid-rebase states each break diff, `map`, and close in different ways.
  Done when: one parametrized test builds each topology and `fm map`, `check --affected`, and `task finish` give a correct answer or a named refusal in all of them.

- **Fuzz every state writer with hostile text** — SECURITY — value 4 — effort S — risk low — category: durability
  Why: the user pastes arbitrary text (captures, quoted transcripts), and the T-id titles and CONTEXT fields store it. Lone surrogates, NUL bytes, CRLF, 1 MB lines, and non-UTF-8 filenames are untested in the pack. Assumption: writers assume clean UTF-8.
  Done when: a fuzz test feeds each writer 500 hostile strings and every one round-trips through read and render without a traceback or a corrupted neighbour record.

- **Route all hook stdout through one validating emitter** — FIX — value 5 — effort S — risk low — category: hooks
  Why: Claude Code reads hook stdout as JSON, so a stray print, a deprecation warning, or an import side effect can silently drop a gate or a sessionTitle. Round 1 added several new hook outputs (monitor, title, compact rewrite). Assumption: each hook still prints for itself.
  Done when: every hook emits via `emit(obj)`, which validates against the schema and falls back to `{}` plus a ledger note. A test injects a `print()` at import time and the hook output still parses.

- **Give `fm` typed exit codes with a retry class** — FEATURE — value 4 — effort M — risk med — category: cli contract
  Why: the drive loop, hooks, and Claude all re-run failed commands without knowing whether the failure was the user's, the environment's, transient, or a Foreman bug. The recent "✗ exit N" parsing misses show that exit semantics already trip the metrics.
  Done when: exit codes map to usage, env, transient, and bug classes. The drive retries only transient failures, and a table test covers every verb's failure paths.

- **Add idempotency keys to mutating verbs** — FEATURE — value 3 — effort M — risk low — category: cli contract
  Why: when a Bash call times out or compaction replays it, the model reruns `fm task done` or `fm task new`. Round 1 added `--redo` but duplicate creation by retry is still possible. Assumption: there is no dedupe on retried creation.
  Done when: running `fm task new "X"` twice within a minute with the same key returns the same T-id, and `done` on a closed task is a no-op that says so.

- **Test every verb under no-tty, closed-stdin, and BrokenPipe** — FIX — value 3 — effort S — risk low — category: cli contract
  Why: Foreman output is constantly piped (`| head`, hooks, headless children). BrokenPipe tracebacks and curses or colour assumptions without a tty are classic gaps, and the pack shows no coverage of them.
  Done when: a matrix runs each read verb with `TERM=dumb`, no tty, `</dev/null`, and `| head -1`, and none produces a traceback or hangs.

- **Key project identity by repo identity, not path** — FEATURE — value 3 — effort M — risk med — category: state
  Why: central records appear to key on the project path. Moving, renaming, or re-cloning a repo orphans its queue, lessons, and research. Assumption: keyed by path.
  Done when: after `mv repo repo2`, `fm` in the new location finds the same queue and `fm doctor` reports a rebind rather than an empty project.

- **Make settings strict with did-you-mean** — FIX — value 3 — effort S — risk low — category: config
  Why: Foreman has many toggles (compact output, push, bypass). A typo'd key or mis-typed value silently leaves a safety or speed feature off, which is the same shape as "off until the user says yes".
  Done when: an unknown or ill-typed setting makes `fm doctor` and session start print one line naming the key and the nearest valid one.

- **Time-box `fm map` and `check --affected` on huge repos** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: the map covered 350 files here, but monorepos have 100k. A hook or gate that times out is a hard failure, while a partial result flagged as partial is not. Assumption: there is no wall-clock cap today.
  Done when: on a synthetic 100k-file repo both commands return within the budget with `partial: true`, and a partial affected-set widens to the full suite rather than narrowing.

- **Wild: Check multi-session histories Jepsen-style** — FEATURE — value 4 — effort L — risk med — category: concurrency — wild
  Why: assumption: parallel lanes and sessions share the queue and ledger through lock-and-rename. A generator runs random interleavings from three simulated sessions and checks the queue invariants (no lost task, no duplicate id, monotonic step).
  Done when: 10,000 seeded histories, including kills mid-write, pass the checker, and a seeded bug is caught with a minimal failing history printed.

- **Wild: Torture the calendar** — FIX — value 2 — effort S — risk low — category: time — wild
  Why: `fm tidy` prunes at 7 days and task ids, titles, and budgets are date-bound. DST shifts, timezone changes, and a laptop waking days later are untested. Assumption: local and UTC time are mixed.
  Done when: tests run under a fake clock across DST transitions, a TZ change, and a 9-day suspend. Pruning and "since you left" are correct in all of them.

- **Wild: Mine Claude Code's issue tracker for hook-crash fixtures** — FEATURE — value 3 — effort M — risk low — category: hooks — wild
  Why: users of other hook-based plugins report real payload oddities (empty fields, huge tool inputs, odd encodings). Replaying them gives an environment corpus beyond the project's own recorded payloads.
  Done when: a fixtures directory of at least 30 anonymized odd payloads runs through every hook in CI, and each is either handled or deliberately refused with a reason.
