# Brainstorm — lens: bold bets

- **Turn `fm decide` records into machine-checked invariants**: FEATURE, value 4, effort M, risk low
  Why: decisions, lessons and constraints such as "no network in hooks" and "stdlib only" are prose that gets re-read and can be forgotten. Assumption: a decision can usually be expressed as a path glob plus a regex or a command.
  Done when: `fm decide --enforce 'plugin/hooks/**' --forbid 'urllib|socket'` makes `fm check` fail on a seeded violation and pass once it is removed.

- **Add `fm peek` as a budgeted search-then-read macro**: PERFORMANCE, value 4, effort M, risk low
  Why: `fm where`, `fm outline` and Read are separate calls, so exploration costs a grep→outline→read turn chain, and `fm cost` already breaks tokens down by tool. Assumption: those chains dominate exploration tokens.
  Done when: `fm peek "symbol or regex" --max-tokens 800` returns ranked hits with the enclosing function bodies in one call, and a replayed exploration task uses fewer turns than the baseline.

- **Delegate mechanical edits to a cheap model under a patch contract**: PERFORMANCE, value 4, effort L, risk med
  Why: `fm run --models` picks a model by tier, but inside a session every rename, docs sweep or boilerplate step runs at full price. Assumption: a `claude -p` Haiku child can return a unified diff for a step's scope globs.
  Done when: a step tagged `mechanical` is executed by a child that touches only its scope, the diff applies cleanly, the step's verify command passes, and `fm cost` shows the lower spend.

- **Run disjoint-scope queued tasks in parallel worktrees**: PERFORMANCE, value 3, effort L, risk high
  Why: `fm run` batches by scope overlap but still executes serially, and scope globs already exist to prove disjointness. Assumption: git worktrees are available.
  Done when: two tasks with non-overlapping scopes finish in less wall-clock time than back-to-back, merge without conflict, and a full `fm check` passes on the merged tree.

- **Learn the affected-test map from history**: FEATURE, value 3, effort M, risk low
  Why: `--affected` relies on static test↔source links, which miss tests that fail through indirect coupling. Failures and their `Files touched` are already recorded per task. Assumption: enough history exists to be predictive.
  Done when: a fixture shows a test that historically failed alongside file X is added to `--affected` for X, with the reason printed, and the reconcile step finds fewer misses.

- **Add `fm why FILE:LINE` for line-level provenance**: FEATURE, value 3, effort M, risk low
  Why: tripwires work per file, but Claude edits lines without knowing which task, criterion or decision produced them. `git blame` plus each brief's Files touched can supply this.
  Done when: `fm why path:42` prints the originating task, its acceptance criterion and any linked decision, and it is shown automatically before an edit to a line covered by a lesson.

- **Confirm L-task intent in three plain sentences before executing**: FEATURE, value 3, effort S, risk low
  Why: L tasks are the costliest to get wrong, and the user only answers yes/no. Assumption: misread intent is a common cause of L-task rework.
  Done when: `fm focus` on an L brief records a pending yes/no restatement, execution edits are guarded until it is answered, and a "no" reopens expansion.
