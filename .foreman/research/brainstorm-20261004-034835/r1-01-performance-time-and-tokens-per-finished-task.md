# Brainstorm — lens: performance: time and tokens per finished task

- **Overlap the review with the next task's first step** — FEATURE — value 5 — effort M — risk med — category: latency
  Why: 31+ drive stops idle ~1–2 min each waiting on a background reviewer. Existing ideas say "park the reviewer" or "run review in background of next task"; this is the concrete scheduler: reviewer gets a frozen diff snapshot (tree hash), the drive starts the next brief's read-only steps (map, recall, plan), and findings re-enter as a step on the closed task, reopening it if needed.
  Done when: a two-task drive test with a stub reviewer sleeping 5 s shows the second task's plan step timestamped before the first reviewer's verdict, and a finding still reopens task one.

- **Cache verdicts by tree hash and command** — PERFORMANCE — value 4 — effort M — risk low — category: gates
  Why: the 704-test suite (~30 s) and `fm check` rerun on every batch; the ledger already stamps runs. Assumption: many reruns hit an unchanged tree or unchanged touched-file set. A verify run on an identical tree plus same command reuses the recorded result, marked "cached", and never for flaky-ledger commands.
  Done when: running `fm check` twice on an untouched tree executes the suite once and the second report says "cached @ tree <hash>"; touching one file invalidates it.

- **Run only the tests the diff can reach in the inner loop** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: fmmap already has impact analysis; 30 s per full run is paid many times per task. Inner steps run impacted tests; the full suite runs once at close, and the close gate refuses without it.
  Done when: editing only fmguard.py runs its impacted test modules in the step gate (fewer than the full set), and close still requires one full green run.

- **Give the reviewer a diff-scoped context packet** — PERFORMANCE — value 5 — effort M — risk low — category: tokens
  Why: ~2.0M tokens over 20 reviewer runs is about 100k per run. Assumption: most is re-reading files. Prebuild a packet: the diff, touched definitions with callers from the map, the criteria, the lens checklist, and recent escapes for those files. The reviewer starts from it and reads more only on demand.
  Done when: a bench comparison on 5 past tasks shows mean reviewer tokens down at least 30% with the same findings recalled on planted defects.

- **Tier the reviewer model by lens and diff risk** — PERFORMANCE — value 4 — effort S — risk med — category: cost
  Why: every lens appears to run at the same cost. Edge and maintainer lenses on a docs or test-only diff run on Haiku. Adversary on network or exec diffs stays on the top model. `fm bench` judges whether recall drops, and fm evolve tunes the table.
  Done when: a docs-only diff routes to the small model, an exec-path diff routes to the large one, and a bench report shows recall per tier.

- **Show time and token cost per ceremony step** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the user asked for speed "without sacrificing quality", but there is no breakdown of where a finished task's wall time goes (gate, review wait, hook latency, model turns). Assumption: ledger timestamps suffice. `fm cost --where` prints the split per task and flags the largest bucket.
  Done when: on a finished task, `fm cost --where` prints at least four buckets summing to within 5% of wall time.

- **Wild: Speculatively pre-run the likely next gate while the model edits** — PERFORMANCE — value 4 — effort L — risk med — category: speculation
  Why: assumption: idle CPU during model turns. A PostToolUse hook starts impacted tests in a detached worktree snapshot after each edit. If the tree hash matches at `fm check`, the result is instant. Wild.
  Done when: after an edit followed by a 10 s model pause, `fm check` returns from the speculative result in under 1 s, and a later edit discards it.

- **Wild: Keep a warm reviewer that learns the repo across the session** — PERFORMANCE — value 4 — effort L — risk high — category: tokens
  Why: each reviewer starts cold and pays to learn the repo again. A long-lived reviewer holds the map and past findings, takes only deltas, and is rotated when context grows or when its independence is in question (reuse risks soft verdicts). Wild.
  Done when: the third review in a session uses under half the first review's tokens, and planted-defect recall does not drop on a bench run.

- **Wild: Compile a brief into a deterministic script when the task repeats** — FEATURE — value 3 — effort L — risk med — category: automation
  Why: assumption: tasks like version bumps, doc syncs or fm export are repetitive. After the same step shape closes cleanly three times, Foreman proposes a macro that executes without model turns, with verification kept intact. Wild.
  Done when: a recorded 3-times repeated brief shape runs from the macro with zero model tokens and the same evidence.

- **Wild: Make a token-burn "speed limit" per tier that the drive enforces** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: the user wants overuse prevented, not subagents forbidden. An S task gets a soft envelope (for example 150k tokens including children). At 80% the pane warns, and past 100% the drive asks once with a default to continue. Wild.
  Done when: a stubbed S task that crosses its envelope produces exactly one prompt, and an M task with the same spend does not.

- **Skip unchanged lenses on re-review** — PERFORMANCE — value 4 — effort M — risk med — category: review
  Why: reviews find 3–8 issues per batch, so fix-and-recheck cycles are common. Assumption: the whole review reruns. Re-review only the lenses whose finding or touched definitions changed, and always rerun adversary if a sink-touching hunk changed.
  Done when: after a fix touching one function, re-review spawns only the lens that raised the finding, plus adversary if the fix touched a flagged sink, with a test asserting the lens list.
