# Brainstorm — lens: performance

- **Bound the cost of work snapshots** — PERFORMANCE — value 4 — effort S — risk low — category: git speed
  Why: round 5 snapshots uncommitted work under refs/foreman/snapshots before `reset --hard`, `clean -f` and similar. In a repo with big untracked or ignored trees (node_modules, target/, build output), each snapshot could stall the guard. Assumption: no size gate or time budget exists yet.
  Done when: a fixture repo with 2 GB of ignored files snapshots in under 1 s, and an oversized untracked set gets a one-line "skipped N MB, restore won't include it" instead of a hang.

- **Make mutation proof stop at the first kill** — PERFORMANCE — value 4 — effort M — risk low — category: gate speed
  Why: hunk mutation proof and `fm task prove` re-run tests per mutant. Assumption: they run the full affected set each time.
  Done when: each mutant runs only its linked tests, ordered by past kill rate, and stops on the first failure. On a 10-hunk fixture the proof takes under half the current wall time with identical verdicts.

- **Prove on a sparse worktree** — PERFORMANCE — value 3 — effort M — risk med — category: gate speed
  Why: `fm task prove` has to check the start tree out to show a red run. On a large repo that costs a full checkout. Assumption: it currently checks out the whole tree.
  Done when: prove materialises only the changed files plus their linked tests over a shared object store. Checkout time on a 50k-file fixture drops by 80% and the red/green verdicts match a full checkout.

- **Key the pyc cache by tree hash instead of deleting it** — PERFORMANCE — value 3 — effort S — risk low — category: gate speed
  Why: round 4 "evidence runs drop stale .pyc" fixed a correctness bug by deleting caches, so every evidence run recompiles. Assumption: this costs seconds on a large suite.
  Done when: evidence runs set `PYTHONPYCACHEPREFIX` to a directory keyed by the tree hash. A second run on an unchanged tree compiles nothing, and a stale-pyc regression test still passes.

- **Make tidy backups incremental** — PERFORMANCE — value 3 — effort S — risk low — category: storage
  Why: T-0922 keeps the newest five dated backups of each project's record, and T-0920 warns at 200 MB of state. Five full copies of a 200 MB state is 1 GB, and copying it makes `fm tidy --apply` slow.
  Done when: backups are hardlinked or delta-packed. Five backups of a 100 MB state use under 150 MB of extra disk and `tidy --apply` runs in under 2 s, and restore still round-trips.

- **Cache per-project summaries for `fm projects --next` and `fm tour --since`** — PERFORMANCE — value 3 — effort S — risk low — category: fan-out verbs
  Why: both shipped in round 5 and walk every project's state or a whole branch. Assumption: no mtime-keyed summary cache, so cost grows with project count and branch size.
  Done when: with 40 projects the second `fm projects --next` finishes under 200 ms, and a branch tour is time-boxed with a "ranked N of M files" note.

- **Give bare `fm` and `fm complete` a latency budget** — PERFORMANCE — value 4 — effort S — risk low — category: cli latency
  Why: T-0917 (bare `fm` as status) and T-0924 (tab completion with live task ids) run on every keystroke or shell prompt. Python import time is felt there far more than in hooks.
  Done when: the bench measures both. Completion stays under 60 ms from a one-line id index, bare `fm` stays under 120 ms, and CI fails when either regresses by more than 30%.

- **Nudge whole-file Writes that change under 10% of a file** — PERFORMANCE — value 3 — effort M — risk low — category: output tokens
  Why: output tokens are the slowest part of a turn. A Write that rewrites a file for a small change costs more than an Edit. Assumption: this is common but unmeasured; the transcript scan can count it.
  Done when: a PostToolUse note fires once per such Write, the bench counts how many are avoided, and a fixture that rewrites a 500-line file for 3 changed lines triggers it.

- **Shape unbounded Grep and Glob calls** — PERFORMANCE — value 3 — effort M — risk med — category: input tokens
  Why: compact output covers Bash only, while Grep with default output on a big repo floods context the same way. Assumption: the 30-day measurement T-0760 made for Bash was not repeated for Grep.
  Done when: the transcript scan reports Grep and Glob output volume, and a PreToolUse hook adds `head_limit` or `files_with_matches` to unbounded calls. Median result size falls with no rise in re-fetches.

- **Skip `fm doctor` checks whose inputs haven't changed** — PERFORMANCE — value 2 — effort M — risk low — category: diagnostics
  Why: `fm doctor` is run at install, release and on demand, and checks like install-version drift and state size rarely change. Each check gets an input fingerprint and a last-green stamp.
  Done when: a second `fm doctor` on unchanged inputs runs in under 300 ms, `--full` bypasses the stamps, and a changed input re-runs only its own check.

- **Wild: add a tmpfs hot tier for volatile state** — PERFORMANCE — value 3 — effort M — risk med — category: state IO
  Why: wild. Heartbeats, hook ring buffers, wake receipts and step-pointer nudges are rewritten constantly and need no durability. The working directory is already under /run/user. Only stage transitions and closes should reach durable disk.
  Done when: hot files live in a per-session tmpfs path, durable writes drop by more than 70% on a bench replay, and a kill -9 test loses only volatile state and still resumes at the correct step.

- **Wild: bench hooks with a cold page cache** — PERFORMANCE — value 3 — effort M — risk low — category: cold start
  Why: wild. `bench_hooks.py` runs 20 warm iterations, but the user's first prompt after boot reads 50 lib modules from disk. The real first-turn latency has never been measured. Run the bench in a container with dropped caches, or use `posix_fadvise(DONTNEED)` on the plugin tree.
  Done when: the bench reports separate cold first-hook and warm p95 numbers, and the cold number gets its own CI threshold.

- **Wild: pick the pane's motion level from measured frame lag** — PERFORMANCE — value 2 — effort S — risk low — category: ui cost
  Why: wild. The foreman-ui motion setting is manual (full 30 fps, calm 8 fps, off), but a slow SSH link or a busy host drops frames. The mod would time its own repaints and step down to calm, then off, saying so once. It would climb back up when frames are fast again.
  Done when: an injected 100 ms render delay moves the pane to calm within 3 s and shows one "motion eased: slow terminal" line. The user's explicit setting still wins.
