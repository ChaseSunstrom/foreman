# Brainstorm — lens: simplicity

I read "simplicity" as removing, merging and doing less, since the pack shows a lot of surface and many repeated fixes.

- **Close out the stale "Later from" backlog** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: about 30 deferred FEATURE M items (T-0788 to T-0869) are placeholders for ideas "kept in the catalog", and each one adds noise to every planning pass.
  Done when: every deferred item carries a revisit trigger or is closed with a one-line verdict, and the open-work list is under half its current length.

- **Ship a Lite profile: plan, prove, one task, guard hook** — FEATURE — value 5 — effort M — risk med — category: onboarding
  Why: T-0794 ("Slim Foreman: Lite mode") is deferred, while the repo has 1877 files and a long list of gates. Assumption: a new user needs only four behaviours.
  Done when: `fm init --lite` installs only those four behaviours, and `fm doctor` passes with the rest absent.

- **Give test suites a single run owner** — CLEAN — value 5 — effort M — risk med — category: gates
  Why: T-1964/65/66, T-1974 and T-1984 each patched a different way two suites ran at once (ambient, ship, check, mid-gate edits). One lock with a queue would replace those separate checks.
  Done when: one function decides "may a suite start", the other call sites use it, and a test starting two triggers at once sees only one suite run.

- **Share one "did you mean" helper across fm** — CLEAN — value 3 — effort S — risk low — category: errors
  Why: T-1995, T-2000 and the run.py `-k` message each hand-roll path or test-id suggestions. Assumption: more refusals will want the same behaviour.
  Done when: fmdocs and run.py call one `suggest(name, candidates, n=3)`, and its single test replaces the duplicated cases.

- **Mark the unverified Codex, Gemini and opencode adapters experimental, or remove them** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: T-0335, T-0336 and T-0337 are blocked, never verified live, and part of T-0794's "retire adapters".
  Done when: unverified adapters are hidden from `fm help` and the docs, or deleted, and no test depends on them.

- **Check captures against done tasks before filing them** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user's dropped items include captures that were "valid items done in another task or duplicates".
  Done when: capturing a title that matches a closed task's title prints that task id instead of creating an item.

- **Freeze the foreman-ui mod** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: T-0418, T-1217 and T-0166 are all blocked or deferred chasing Claude Code's paint behaviour; freezing the mod stops the churn (T-0794 names this).
  Done when: the mod is pinned to one version, the blocked UI items are closed, and the docs say it is unmaintained.

- **Hide skills that haven't fired in 30 days** — PERFORMANCE — value 3 — effort M — risk med — category: skills
  Why: 1248 of 1877 files sit under plugin/skills. Assumption: most are unused and cost context and scan time.
  Done when: `fm skills prune --dry-run` lists unused skills and a pruned install passes the round-trip e2e.

- **Wild: add `fm do "request"` as the only command a newcomer needs** — FEATURE — value 4 — effort L — risk med — category: UX
  Why: the user's requests are plain sentences ending in "Ship T-N to main". Assumption: the plan, edit, prove and ship sequence can be inferred.
  Done when: `fm do "fix X"` runs from capture to merge on a fixture repo with no other flags.

- **Wild: a gate ledger where each new gate must retire an old one** — CLEAN — value 4 — effort M — risk low — category: governance
  Why: each recent commit adds another check or message, and no commit removes one. Assumption: the added checks have overlapping coverage.
  Done when: `fm gates` shows a per-gate catch count, and adding a gate with a lower catch rate than the weakest existing gate is refused without a retirement.

- **Wild: a weekly delete-day task that proposes the least-used code** — FEATURE — value 3 — effort L — risk med — category: maintenance
  Why: the repo only grows. Assumption: coverage and call data can show dead paths.
  Done when: a scheduled run files one CLEAN task naming a function with no callers and no test hits.

- **Wild: a one-line `fm now` that says what happens next** — FEATURE — value 3 — effort S — risk low — category: UX
  Why: the work bar, stage rail, lanes and charts all show state, but the user mostly asks "ship T-N". Assumption: they want one answer.
  Done when: `fm now` prints a single line naming the next action and its task id.

- **Batch same-file FIX captures into one task** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: T-1984/85/86 and T-1989/90/91 landed as three tasks per commit, each paying the full gate cost.
  Done when: two captures under the same @path in one intake become one task with two DONE-WHEN lines, and its gates run once.
