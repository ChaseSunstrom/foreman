# Brainstorm — lens: deepen: lanes

- **Split shared registries into per-feature drop-in files** — CLEAN — value 5 — effort M — risk med — category: lanes
  Why: the review says nearly every second merge conflicted on the one HELP_TIERS line in fmcli.py (T-1059, T-1062 twice), each costing a re-merge builder. Detecting hot spots only warns; the fix is structural. Commands register via `plugin/lib/commands.d/<name>.py` (or a generated index), so parallel builders never touch the same line.
  Done when: two lanes that each add a new command merge back to back with zero conflicts, and `fm help` still lists both in the right tier.

- **Add a builder self-adversary pass before "done"** — FEATURE — value 5 — effort M — risk low — category: lanes
  Why: the review says reviewers found real defects in almost every builder branch (deny-bypass, false green, unbounded time, writes outside a folder). A cheap second pass that gets the diff and a checklist of those classes, and must name an attempted break, catches them before review.
  Done when: `fm lane done` refuses without an adversary note, and a seeded branch with a deny-bypass gets flagged by it in a fixture test.

- **Build a lane scheduler that fuses load, cap and hot spots** — FEATURE — value 4 — effort L — risk med — category: lanes
  Why: load throttling, fan-out gating and hot-spot detection are separate ideas that all answer "which builder may start now". `fm state --json` took over 120 s at load 30-60 with 4 builders. One scheduler uses load, the file overlap between briefs and the cost forecast, so it starts, holds or serializes lanes with a stated reason.
  Done when: with a synthetic load of 30, `fm lane next` holds the second builder and prints why, and it releases once the load drops.

- **Add `fm guard why "<cmd>"` for replay through the real hook** — FEATURE — value 5 — effort S — risk low — category: guard
  Why: the main thread twice wrote a scratch script to replay a command through the hook (T-1125, T-1141). It prints allow or deny, the matching rule and the cwd used, and lanes can run it for their own commands before they hit a wall.
  Done when: `fm guard why "cat x | sh"` prints the verdict and the rule, and matches what the live hook did for the same input in a test.

- **Lint verify commands when a task or lane is created** — FIX — value 4 — effort S — risk low — category: verification
  Why: the review says verify commands are often wrong (a nonexistent test module, `npm test` without npm) and are caught only at run time. Dry-check that the module or file exists and the tool is on PATH, using `fm map` gates.
  Done when: adding a verify naming a missing test file is rejected with a pointer to the nearest real test.

- **Make lane merges transactional, with an incremental criteria cache** — PERFORMANCE — value 4 — effort M — risk med — category: lanes
  Why: merges are sequential and each re-runs all criteria; one load-sensitive failure blocked a merge. Pre-merge ref plus one-verb abort, then re-run only the criteria whose linked files the merge changed, and retry a failure once under a load-noted flag.
  Done when: a merge touching one file runs only its mapped criteria, and `fm lane abort` restores the exact pre-merge ref.

- **Normalise builder cwd and path contract** — FIX — value 4 — effort S — risk low — category: lanes
  Why: builders cd into subdirectories and the lease paths double (`mods/foreman-ui/mods/foreman-ui/...`), and bare stdin readers hung (T-1129). Wrap each builder with a root-anchored cwd, `stdin=/dev/null`, and lease paths that resolve to the worktree root.
  Done when: a fixture builder that does `cd sub && fm lease take rel/path` records one correct, non-doubled lease path.

- **Cap lane state parsing with a brief index** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: hooks dropped from 135 to 72 ms by not parsing all 1,069 briefs (T-1140), but other commands, including `fm state`, still parse every brief. A cached index keyed by mtime serves lane and state queries.
  Done when: `fm state --json` on a 1,000-brief fixture is at least 3x faster, with identical output.

- **Give each builder a no-progress tripwire that salvages the work** — FEATURE — value 4 — effort M — risk low — category: lanes
  Why: this was in the seed list, and T-0831 (salvage from capped children) is deferred. The tripwire fires on no diff, no test run and no ledger event for N minutes, checkpoints the worktree as a WIP commit, and offers re-dispatch with the partial.
  Done when: a stalled fixture builder is stopped, its edits are saved on a WIP ref, and `fm lane resume` starts from them.

- **Run builders in a rehearsal merge against main's tip (wild)** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: assumption: conflicts are cheaper found early. Each lane's idle time runs a speculative merge with the current main plus the other open lanes, so a hot-spot conflict surfaces mid-build and the pair of builders can coordinate, not after the fact.
  Done when: two lanes editing the same line produce a conflict warning before either calls done.

- **Pit two cheap builders against one hard task and keep the winner (wild)** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: `fm lane race` with `--score` and pick shipped (T-0169 area, "Racing builders"). Wild extension: auto-race only when the cost forecast is low and the first attempt failed a gate, scored by tests and diff size, with the loser's lessons merged into the recall log.
  Done when: a failed first attempt triggers a race, and the winner's branch merges while the loser's failure reason shows in `fm lessons`.

- **Tell the user which lane is the bottleneck in the pane (wild)** — FEATURE — value 3 — effort S — risk low — category: UI
  Why: assumption: a Gantt-like lane strip makes idle waiting visible (the mission says never idle while a gate, build or review runs). Bars show build, gate, review and merge waiting, with the critical path highlighted and a one-line "waiting on X".
  Done when: the pane renders each active lane as a segmented bar with the blocking stage marked, and a screenshot shows it.

- **Score each lane's outcome into the model-routing table** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the pillar says to use the cheapest model that can. Recording per-lane pass-first-time, review defects and cost by task type and model makes the default for each class evidence-based, and it can step up after two defects.
  Done when: `fm lane plan` picks a different model for a task class after seeded outcomes show the cheap one failing it, and states why.
