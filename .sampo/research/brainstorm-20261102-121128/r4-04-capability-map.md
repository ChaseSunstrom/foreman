# Brainstorm — lens: capability map

- **Mine the user's hand edits after a landing** — FEATURE — value 5 — effort M — risk low — category: learning
  Why: assumption: the strongest signal Foreman doesn't author is what the user changes by hand within a day of a task landing, and no listed idea reads it. The pack's weakness-finding steers ask for signals Foreman didn't write.
  Done when: `fm outcomes --edited` lists landed tasks whose files had non-agent commits within 24h, with the changed hunks, and a test fixture shows one such task flagged and one untouched task not.

- **Turn each fixed bug into a lint rule** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: assumption: the red-first test guards one case, while a Semgrep or ast-grep rule distilled from the fix guards the whole class. Related ideas are "sweep siblings" and the lessons confidence task T-0217, but neither emits an executable rule.
  Done when: closing a FIX task proposes a rule file that fails on the pre-fix tree and passes on the fixed one, and `fm check` runs it.

- **Add a performance proof kind** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the pack shows proof kinds for docs and tests and an internal `bench_hooks.py` p95 gate, but PERFORMANCE tasks (T-1231) have no proof type for user repos.
  Done when: `fm task prove --perf CMD` records the median of N runs before and after and fails a receipt claiming a speedup inside the noise floor.

- **Take shadow checkpoints before each edit batch** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: Cline and Claude Code have rewind, but "undo a landed task" in the pack covers only committed work. Uncommitted and untracked edits are unprotected, and T-0798 (recovery) is deferred.
  Done when: `fm rewind` restores a tree, including untracked files, to the state before the last edit batch, verified in a test that deletes a file.

- **Run proofs in remote CI as an arbiter** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: assumption: local proofs run on the same machine as the agent. The pack has a CI badge and `fm ship`, but no receipt state for "passed in CI on another OS". Cross-platform failures are likely given the Arch-only blockers (T-0325).
  Done when: `fm task prove --remote` dispatches the repo's workflow at the task commit and records the run URL and result in the receipt, with "unrun" if dispatch fails.

- **Turn an error report into a task with a repro** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: intake handles typed asks, and T-0790 covers verbatim capture. A pasted stack trace or log slice has no path to a red-first test.
  Done when: pasting a traceback into `fm capture` creates a task whose first criterion is a failing test that reproduces the named frame.

- **Add a codemod mode with a repo-wide proof** — FEATURE — value 3 — effort L — risk med — category: refactor
  Why: assumption: OpenRewrite and Renovate-style bulk changes are a standard capability in this space, and the pack has only LSP renames (T-0788) as a gap. A bulk change needs a before/after proof, not one test per file.
  Done when: `fm codemod RULE` applies a change across the repo and the receipt shows the count of sites changed, the full suite passing, and zero remaining matches of the old pattern.

- **Watch dependencies with a proof lane** — FEATURE — value 3 — effort M — risk med — category: maintenance
  Why: "gate package installs" is listed, but nothing proposes updating dependencies. Foreman's own idle budget could spend on it.
  Done when: a nightly tick opens one task per outdated dependency, bumps it in a lane, and lands it only with a passing suite and a changelog line.

- **Route bugs to the commit that introduced them** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: bisecting Foreman's own regressions is listed, but a user's bug has the same shape: a failing proof command and a range of commits.
  Done when: `fm bisect TASK` finds the first bad commit using the task's proof command and writes it to the task's notes, tested on a synthetic repo.

- **Make a team ledger with author-tagged steers** (wild) — FEATURE — value 3 — effort L — risk high — category: team
  Why: assumption: every steer and lesson is single-user. Ideas on host ids and merging ledgers cover machines, not several people with conflicting steers.
  Done when: two clones with different authors merge their steers through git, and a conflicting pair is reported by `fm doctor` instead of silently both applying.

- **Seed bugs into the user's repo as a skill drill** (wild) — FEATURE — value 3 — effort L — risk med — category: evaluation
  Why: mutating a finished task's fix tests one proof, whereas seeding new faults across a copy of the repo tests whether `fm find` and the agent catch faults in the user's own languages. This answers the steer asking for recall per language and bug type.
  Done when: `fm exam seed` plants N faults in a scratch copy, runs the agent, and prints recall per fault type and language, with the copy deleted afterwards.

- **Learn the user's review taste from reverted commits** (wild) — FEATURE — value 3 — effort M — risk med — category: learning
  Why: assumption: reverts, amends and "fix review" commits in git history encode taste that lessons miss. Mining them gives lessons with evidence that Foreman didn't author.
  Done when: `fm lessons --from-history` proposes at least 3 candidate lessons from a repo with known reverts, each citing the commit hash it came from.

- **Let a pocket CLI reply to `fm ask` over a webhook** (wild) — FEATURE — value 2 — effort M — risk med — category: surface
  Why: blocked tasks wait on the user (T-0335, T-0352), and the standing rules say to ask once via `fm ask` and keep going. A reply channel off the desk closes that loop faster.
  Done when: a pending `fm ask` posts to a configured ntfy topic and a reply of "yes" or "no" resolves it, tested against a local stub server.

Next question: which closed tasks were later edited by the user's hand, and how much of that rework would a better proof have caught?
Next question: which capabilities in this space, such as dependency upkeep, bisecting and error intake, does a user currently do outside Foreman because it has no verb for them?
