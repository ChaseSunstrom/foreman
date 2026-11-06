# Brainstorm — lens: approaches

- **Make the duel the judge of every idea** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: T-1231 (beat Claude Code on the duel), T-1266 and T-0866 are all deferred for want of a case corpus, so brainstorming never learns which ideas helped. Approach: brainstorming only proposes, and a fixed duel/bench corpus scores before and after, so an idea merges only if pass rate, cost or time improves.
  Done when: `fm bench` runs a frozen set of at least 20 cases against two Foreman versions and prints a pass/cost/time delta that a task can cite in its close.

- **Turn the user's own request stream into the bench corpus** — FEATURE — value 5 — effort M — risk low — category: evals
  Why: the "asked" lines (about 20 recent items, each with a DONE-WHEN) are ready-made cases, and T-0035 (eval capture) is deferred. Approach: reuse each shipped task's DONE-WHEN and fixture as a replayable case, redacted, instead of writing a corpus by hand.
  Done when: `fm eval capture T-1996` writes a case that fails on the parent commit and passes on the task's commit.

- **Prune the "Later from T-07xx/T-08xx" backlog instead of adding to it** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: about 25 deferred "Later from…" clusters (T-0788 to T-0869) have no evidence attached, and the user drops YAGNI items quickly. Approach: do less, with one pass that closes every deferred item lacking a failure, a user quote or a measured cost.
  Done when: the open-work list shrinks by at least half and each closed item records a one-line reason.

- **Fix failure classes, not instances: a file-ownership invariant test** — FIX — value 4 — effort M — risk med — category: correctness
  Why: recent fixes keep hitting one root cause, which is who owns which dirty file and which run is live (T-1967 and T-1984 on two suites at once, T-1968 and the `_theirs` fix on scope, T-1998 on core-integrity). Approach: a model-based or randomized test that interleaves edits, ambient runs, ships and closes across two tasks and asserts the invariants (never two suites, never another task's file counted).
  Done when: the randomized test runs 500 sequences green and fails when any of those fixes is reverted.

- **Dedupe "Noticed:" captures against done tasks and commits at capture time** — FIX — value 3 — effort S — risk low — category: intake
  Why: 74 of 106 captures were dropped, and the sample of 40 showed nearly all were valid items already done in another task, or duplicates. Approach: match the capture's path and title tokens against closed task titles and recent commit subjects, and skip a capture that matches.
  Done when: replaying the 106 historical captures drops at least 60 of the 74 previously dropped ones and keeps all 32 that were taken.

- **Add a fast lane for one-file FIX tasks with an existing test** — PERFORMANCE — value 4 — effort M — risk med — category: ceremony
  Why: most recent commits are tiny FIXes (T-1982, T-1989, T-1996), each paying the full check, gates and ship ceremony, and T-1266 (ceremony per task kind) is deferred. Approach: a profile that runs only the named test and the affected module, then a full check once at ship.
  Done when: a one-file FIX with a regression test closes in at least 40% less wall time than before, and the duel pass rate doesn't drop.

- **Make the loop stop on measured yield, not a dry-round count** — FEATURE — value 3 — effort M — risk low — category: loop
  Why: T-1987 and T-1992 patched what counts as a dry round, and T-0829 (scale lenses by `lens_rates`) is deferred. Approach: track kept ideas per dollar per round, and stop or drop lenses when the rate falls below a floor.
  Done when: a loop with a stubbed zero-yield lens drops that lens after N rounds and prints why.

- **Rank new ideas by a keep-predictor trained on asked and dropped history** — FEATURE — value 3 — effort M — risk med — category: ranking
  Why: the dropped lines carry reasons (conflicts with never-idle, YAGNI, already handled), which are labelled data. Approach: score ideas against that history and surface likely drops before any are built. Assumption: about 100 labelled drops and keeps are enough for a cheap similarity ranker.
  Done when: on a held-out slice of history the ranker puts at least 70% of dropped ideas in the bottom half.

- **List every human-only blocker in one digest** — FEATURE — value 2 — effort S — risk low — category: unblock
  Why: T-0325 (`sudo pacman -S libappindicator-gtk3`), T-0418 (update the installed foreman-ui), T-0352 and T-0336 are blocked on one-off user actions or live runs. Approach: a single `fm blocked` output with the exact command for each.
  Done when: `fm blocked` prints each blocked task with a copy-pasteable next action.

- **Mutation-test Foreman's own gates (wild)** — SECURITY — value 4 — effort L — risk med — category: self-verification
  Why: assumption: `fm gates` now names why-not-caught (T-1980), but nothing measures whether the gates catch real regressions. Approach: mutate core `plugin/lib` functions and require at least one gate or test to fail.
  Done when: a report gives a mutation score per module, with surviving mutants listed as candidate tasks.
  (wild)

- **Run a red-team agent that tries to fake a proof (wild)** — SECURITY — value 4 — effort M — risk med — category: adversarial
  Why: Foreman's promise is that Claude proves work with commands it actually ran. Approach: an unattended adversary tries to close tasks with a vacuous test, a stale result or an out-of-scope edit, and each success becomes a fix task. Assumption: `fm task prove` has holes beyond the `-k` mismatch found in T-1994.
  Done when: a nightly run reports N attempted bypasses and files a task for each success.
  (wild)

- **Replay a recorded session against each new version as a visual regression (wild)** — FEATURE — value 3 — effort L — risk med — category: regression
  Why: the demo (`demo/live.svg` and the MP4) is a real recorded session, and the foreman-ui mod (T-0166, T-1217) is fragile against Claude Code updates. Approach: replay a captured session and diff the rendered frames.
  Done when: CI fails if the replayed frames differ beyond a threshold after a Claude Code bump.
  (wild)

- **Let a "Foreman for Foreman" agent do the micro-fix queue unattended and merge on green (wild)** — FEATURE — value 3 — effort L — risk high — category: autonomy
  Why: the user's requests are mostly a steady stream of specified FIX/PERF items with DONE-WHEN lines, an already-structured work type. Approach: a worker takes only items with a DONE-WHEN verify command and a single-file scope, and lands them on a branch for review. Assumption: the user would trust branch-only landings, not main.
  Done when: five queued items land overnight as separate branches, each with its proof output attached, and none touches main.
  (wild)

- **Retire or freeze surfaces that no data shows are used** — CLEAN — value 3 — effort M — risk med — category: slimming
  Why: T-0794 (slim Foreman, retire adapters, freeze the mod) is deferred, while T-0335 to T-0337 are blocked on three other CLIs. Approach: do less, keeping a surface only if its use shows up in the logs.
  Done when: a usage report lists each adapter and surface with its call count, and anything with zero calls in 30 days has a retire task.
