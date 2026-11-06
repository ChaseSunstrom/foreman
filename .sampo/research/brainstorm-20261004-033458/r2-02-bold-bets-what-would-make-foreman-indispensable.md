# Brainstorm — lens: bold bets: what would make Foreman indispensable

- **Ship `fm adopt` for foreign repos** — FEATURE — value 5 — effort L — risk med — category: onboarding
  Why: assumption: Foreman's value is capped by how fast it becomes useful in a project it has never seen. Today it starts empty (no lessons, no map, no bench cases). Nothing in the pack covers cold-start on an existing repo.
  Done when: on a fixture repo with 50 commits and a test suite, `fm adopt` produces a repo map, a verify-command inventory (each probed to actually run), a seeded lessons file mined from reverted/fix commits, and 3 bench cases from past fixes. A test asserts all four exist.

- **Mine git history into fail-to-pass bench cases** — FEATURE — value 5 — effort M — risk low — category: bench
  Why: fmbench replays only tasks Foreman finished itself, so a new project has no corpus. Fix commits with a test change are free ground truth. The user wants evolve to be "bench-gated", and a gate is only as good as its corpus.
  Done when: `fm bench mine --since 90d` on a fixture repo emits cases only for commits where the test fails on the parent and passes on the commit; commits without that property are listed as skipped with a reason.

- **Make the brief a negotiated contract with a price tag** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the user asked for savings "to prevent over usage", not to forbid it. Per-task tier and token/time estimates drawn from the spend ledger, shown at brief time with the cheaper variant ("skip debate, reviewer on delta only: -40%"), let the user choose rather than be capped.
  Done when: `fm task new` prints an estimate with a range from the last 20 same-tier tasks and at least one named cheaper variant; the actual spend at close is stored next to the estimate; a test checks that the stored pair exists.

- **Run the reviewer as a continuous background pair on every save** — PERFORMANCE — value 5 — effort L — risk med — category: speed
  Why: friction: "~1–2 min idle per review pass, 31+ drive stops". Reviewing hunks as they settle (after each step's gate goes green), then merging verdicts at close, removes the wait. This is the review-speculation idea made concrete, with a staleness rule: a verdict is dropped if its hunk changed afterwards.
  Done when: on a 3-step task, step-level reviews are launched at step completion; at close only hunks changed since their review are re-reviewed; a measured drive-stop count on the fixture drops to 0 for the review wait.

- **Expose the verdict kernel as a GitHub Action and pre-push check** — FEATURE — value 4 — effort M — risk low — category: reach
  Why: Foreman's proof pack exists (`fm pr`) but only the user's session sees it. A CI step that fails when a PR's claimed criteria have no ledger evidence makes it useful to teammates and a second line of defence when hooks are bypassed. Nothing is published without the user's yes (the Action ships as a file in the repo).
  Done when: `fm verify-pack FILE` exits non-zero on a proof pack whose evidence hashes don't match the current tree, and zero on a fresh one; a test covers both.

- **Wild: Hold a "Foreman vs. the world" quarterly tournament** — FEATURE — value 4 — effort L — risk low — category: benchmarking
  Why: assumption: indispensable means provably better than the alternatives. `fm bench duel` exists for plugins; extend it into a standing ladder against bare Claude Code, other popular harness plugins from `fm landscape`, and Foreman's own previous releases, with a single scoreboard on the pane. (wild)
  Done when: `fm bench ladder` runs the same 5 cases on N configurations within the budget cap and writes a ranked table with cost per pass; the table is diffed against the last run.

- **Wild: Let Foreman fork itself into a sandbox and take a pass while the user sleeps** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: the user asked for "numerous multiple passes of recursive improvements"; the inbox has "night shift" and "Foreman for Foreman" ideas separately. Combine them: a budgeted run on a throwaway branch/worktree, each change benched, only what passes the evolve gate lands in a morning report, and nothing merges without the user's yes. (wild)
  Done when: `fm night --budget $3 --hours 2` on a fixture creates a worktree, runs at least one improve cycle, stops at the cap, and leaves the main branch untouched; the morning report lists each change with its bench delta.

- **Wild: Answer "what's wrong with my project" from the ledger across tasks** — FEATURE — value 4 — effort M — risk low — category: insight
  Why: escapes, surprises, flakes, repeated guard blocks and reviewer findings are all stored but read per task. Clustering them by file/module yields a hotspot map ("parser.py: 6 surprises, 3 escapes, 2 flakes") that no single task would surface. (wild)
  Done when: `fm hotspots` on a fixture ledger ranks modules by combined signal, with the counts per signal and the task IDs behind each; a test checks ordering.

- **Make hooks the portable core: ship a harness-neutral shim and MCP read tools** — FEATURE — value 4 — effort L — risk med — category: compatibility
  Why: the user wants "better compat with plugins/skills/whatever". The pack lists the MCP server as open and a neutral kernel as an idea; merge both into one item with one deliverable: the "no done without evidence" check callable over stdio.
  Done when: a stdio client calling `claim_done(task)` on a task without evidence gets a refusal with the missing criteria, and on a proven task gets an OK; a test drives it with no Claude Code present.

- **Wild: Turn every guard block into a one-line lesson the user can accept at the block** — FEATURE — value 3 — effort S — risk low — category: guard UX
  Why: friction: guard false positives cost four blocked edits earlier. Merging "teach this" with a dry-run check (`fm guard check '<cmd>'`, a pain point from this pass) means the user's yes becomes a stored precise rule and the fixture becomes a corpus entry. (wild)
  Done when: after a guard block, `fm guard allow --last` stores a narrow rule plus a replay case; the same command is then allowed, and a broader variant is still blocked, both asserted in tests.

- **Fix the pre-audit patterns flagging their own source** — FIX — value 2 — effort S — risk low — category: noise
  Why: friction: "pre-audit's security patterns match their own regex source". Cheap to fix and it erodes trust in the flag.
  Done when: running pre-audit on the file that defines the patterns yields no network-code flag, while a fixture with a real `urllib.request.urlopen` call still does.
