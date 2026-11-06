# Brainstorm — lens: capability map

- **Land a lane as a clean commit series** — FEATURE — value 4 — effort M — risk low — category: git history
  Why: assumption: lanes currently close as one squashed diff, so a reviewer can't see the logical steps. A series of one change per commit makes bisect and revert usable.
  Done when: a closed lane with three logical changes produces three commits, and each commit passes the gate on its own.

- **Resolve merge conflicts as a proven task** — FEATURE — value 5 — effort M — risk med — category: merge
  Why: assumption: a rebase conflict stops a lane with no owner, and the queue waits on the user. The gate should decide whether the resolution is correct.
  Done when: a seeded conflict is resolved, both sides' tests pass on the result, and the lane closes with the resolution in its receipt.

- **Prune merged and abandoned lane branches and worktrees** — CLEAN — value 3 — effort S — risk low — category: housekeeping
  Why: assumption: a dead run leaves its `fm/*` branch and worktree behind, and nothing removes them. Lane worktrees are already a planned idea, so cleanup has to ship with them.
  Done when: `fm prune --dry-run` lists every `fm/*` branch and worktree it would remove, and nothing is removed until `--yes` is passed.

- **Hunk-level approval before an edit lands** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the pack shows the user rejecting part of a change (the `fm edit` block that couldn't delete text). Accepting or rejecting hunks individually, like `git add -p`, fixes that without a full redo.
  Done when: rejecting one hunk leaves the others applied, and the gate reruns on the resulting tree before the task can close.

- **Triage incoming GitHub issues with duplicate detection** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: assumption: issues arrive as free text with no dedupe, so the same bug can be queued twice. The import path already exists.
  Done when: a second issue describing a known failure is linked to the first and not queued as a new task.

- **Record gate network traffic as tapes for offline reruns** — FEATURE — value 3 — effort M — risk med — category: reproducibility
  Why: assumption: gates that fetch packages or call APIs give different verdicts on rerun. Tapes make the verdict repeatable and the CI cost lower.
  Done when: a gate rerun with network disabled reproduces the recorded verdicts, and a changed response fails the run with a diff.

- **Profile a slow gate and name the hottest function** — PERFORMANCE — value 3 — effort M — risk low — category: profiling
  Why: T-1808 showed a test class stalling for 480 s with no cause visible until its stack was dumped. A profile should name the cost before the timeout fires.
  Done when: a slow run's receipt lists its top three functions by share of CPU time, and a fixture with a planted hot loop shows it first.

- **Generate PII-free fixtures from the production schema** — FEATURE — value 3 — effort M — risk low — category: test data
  Why: assumption: tests either use hand-written data that drifts from the schema, or copied real data that shouldn't be in the repo.
  Done when: generated fixtures validate against the schema, and a scan finds no value copied from the source dataset.

- **Smoke-test installers on each OS in a VM** — FEATURE — value 3 — effort L — risk med — category: distribution
  Why: the pack records platform-specific CI breakage (T-1807 on Ubuntu 26, T-1809 on macOS). The installer is the first thing a new user hits on each platform.
  Done when: the install script passes on Ubuntu, macOS and WSL images in CI, and a failure names the platform and step.

- **Socratic review card: one "why" per hunk** — FEATURE — value 4 — effort S — risk low — category: review — wild
  Why: wild: a model asks one plain "why is this here?" question per hunk. The change closes only when each answer appears in the receipt, so unexplained edits stand out.
  Done when: a diff with one hunk left unexplained stays open, and the receipt quotes the answer for every other hunk.

- **Settle merge conflicts by asking the user three intent questions** — FEATURE — value 3 — effort M — risk med — category: merge — wild
  Why: wild: when both sides of a conflict pass their tests, the choice is about intent, not code. Three yes/no questions resolve most cases, and the proof still checks the result.
  Done when: a seeded conflict with two passing sides asks at most three questions, applies the answers, and the gate passes on the result.

- **Give each directory a passport of proof stamps** — FEATURE — value 2 — effort S — risk low — category: visualization — wild
  Why: wild: each directory collects a stamp for every verified change, with the date and task id, like a visa page. Stale or never-proven areas show as blank pages.
  Done when: `fm map` marks a directory with its latest stamp, and a directory with no proof in 90 days shows as blank.
