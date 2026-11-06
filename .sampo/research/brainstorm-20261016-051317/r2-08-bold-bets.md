# Brainstorm — lens: bold bets

- **Adopt the dirty tree** — FEATURE — value 4 — effort S — risk low — category: handoff
  Why: assumption: users often start by hand and then hand over. Nothing in the pack covers turning uncommitted work and shell history into a task. `fm adopt` would read the diff and recent commands, write a brief with a guessed goal and done-when, and carry on from there.
  Done when: in a fixture repo with a half-written change, `fm adopt` creates a task whose brief names the touched files and a runnable verify command, and the original diff is untouched.

- **Pin legacy behaviour before the first edit** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: many repos have no tests around the code Foreman is asked to change, so red-first has nothing to anchor on. `fm characterize <file>` would record current outputs as a golden test (stand-alone, from sample calls), and the task then edits against it.
  Done when: on an untested fixture function, the generated test passes on the base and fails after a seeded behaviour change.

- **Write the PR body from proof receipts** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the pack shows close-out and landing work (T-0795, merge train, "ship to a PR"), but no verb builds the PR description from the ledger. Each claim in the body would be a command that was actually run, with its exit code and a rerun line.
  Done when: `fm pr-body T-NNNN` prints a body where every "verified" line carries a command that, rerun in the worktree, reproduces the recorded exit code.

- **Treat a living SPEC.md as a task source** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: assumption: the user hands over goals in prose ("make it THE plugin"), and drift between stated intent and code is invisible. Foreman would diff each spec section against the code and the closed tasks. A missing or contradicted clause becomes a task, and a shipped behaviour with no clause becomes a doc task.
  Done when: removing a behaviour from a fixture repo makes `fm spec check` open exactly one task citing the clause, and a satisfied clause opens none.

- **Run the discipline on non-code work** — FEATURE — value 4 — effort L — risk med — category: scope
  Why: assumption: the stage rail and red→green proof are code-shaped. Docs, research and ops tasks need their own evidence types (sources cited, links resolve, claims traceable to a command) in the same plan, prove and close loop.
  Done when: a docs-only task closes with a link-check and citation-check receipt instead of a test run, and `fm doctor` accepts it.

- **Extract the guard as a standalone package** — SECURITY — value 3 — effort M — risk med — category: distribution
  Why: the guard is the part users cite most (the guard-why, differential and fuzz ideas all stem from it). Packaged on its own with its corpus, other plugin authors could embed it, which makes Foreman the reference implementation.
  Done when: in a clean venv, installing the package and running its check on `rm -rf /` returns deny, with no Foreman state on disk.

- **Hand out a per-engagement spend allocator across projects** — FEATURE — value 3 — effort M — risk low — category: portfolio
  Why: `fm projects --next` and fmbudget exist per project. Nothing splits one day's budget across all the user's repos by expected value, using forecast cost and the backlog's evidence rank.
  Done when: `fm portfolio --budget 20` prints a per-project split that sums to 20 and cites, for each project, the open tasks it funds.

- **Export an evidence pack for audit** — FEATURE — value 3 — effort M — risk low — category: compliance
  Why: assumption: teams that adopt AI-written code get asked who approved what and what ran. Ledger receipts already exist. A dated export lists each commit with its task, tests run, guard denials, and who approved.
  Done when: `fm evidence --since 30d` writes one file listing every commit in range with a task id and a recorded test run, and flags any commit lacking either.

- **Wild: Publish a "closed with proof" badge** — FEATURE — value 3 — effort S — risk low — category: reach — wild
  Why: assumption: a README badge showing the share of recent commits closed with a real red→green run makes the discipline visible and spreads Foreman. It is generated locally from the ledger and committed as a static SVG, so no service is involved.
  Done when: `fm badge` writes an SVG whose percentage matches a hand count of the last 50 commits in a fixture ledger.

- **Wild: Drive a desk lamp from fleet state** — FEATURE — value 2 — effort S — risk low — category: devices — wild
  Why: assumption: AFK users want to know from across the room whether builders are running, blocked, or done. A setting names a local webhook or command that receives a state word (working, needs-you, done, red). Nothing is sent unless it is configured.
  Done when: with the setting pointing at a logging script, a state change in a fixture session calls it exactly once with the new state word.

- **Wild: Land one proven fix on someone else's repo for practice** — FEATURE — value 2 — effort L — risk high — category: showcase — wild
  Why: assumption: Foreman's best advertisement is a merged, small, correct PR. `fm adopt-oss <url>` would work in a fork, pick a labelled easy issue, run the full discipline, and stop at a draft PR for the user to review. Nothing is posted without an explicit approval.
  Done when: against a local bare-repo fixture with one easy issue, it produces a branch with a failing-then-passing test and a PR body, and pushes nothing.

- **Wild: Hold a nightly league between two Foreman configs** — FEATURE — value 3 — effort L — risk med — category: self-improvement — wild
  Why: the pack has A/B holdout and replay ideas, but they are separate steps. A league would run candidate and incumbent settings on the same minted case corpus in throwaway worktrees and post a table, with the winner promoted only after the user approves.
  Done when: running it on a three-case fixture corpus writes a table of pass rate and cost for both configs and changes no setting.
