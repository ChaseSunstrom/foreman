---
id: T-1352
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:42Z
updated: 2026-10-23T14:25:09Z
base: 8ebdea8b559dff6b2c7b411cf7b75d735fd64128
base_tree: 543c831803c2eeb6b84213828c63ae59438bf29d
plan0_at: 2026-10-23T14:22:36Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, README.md]
verified: strong
---
# Fm code undo and PR from a run (U19): after a close, u undoes the run (git revert of its c
## Raw request
> fm code undo and PR from a run (U19): after a close, u undoes the run (git revert of its commit, recorded in history) and p drafts the PR text via fm pr, pushing only with the publish grant
## Interpretation
After a run closes and commits, u undoes it: a git revert of the run's commit (asked once more within 2 s, like q mid-run), recorded in the run's history line (undone by <sha>); P drafts the pull request text via fm pr for the task and shows it, and pushes only when the project holds the publish grant (fm task set ID --allow publish), else it says how to grant it. p stays projects.
## Assumptions (confidence)
## Acceptance criteria
- [x] u twice within 2 s on a closed run reverts its commit and marks its history undone; P shows fm pr's draft and Enter posts it through fm pr; neither acts without a closed run — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete version: undo only a closed run with a known commit, a second press to confirm, a revert commit (history kept, nothing destroyed), the run's history file marked undone so the past-runs list says so, the PR draft from fm pr and its posting gated by the grant fm pr already enforces. Options for undo: git revert (chosen: a new commit, reversible, safe on shared history), git reset (rewrites history, loses the record), fm task reopen (state only, files stay). For the PR: fm pr ID's draft in the text view, Enter running fm pr ID --post (chosen: fm pr owns the grant check), a gh pr create here (a second path to keep in step).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: undo and the PR draft
2. [x] the u and P keys, the revert and its history mark, the draft view and post; CHANGELOG and README
## Resume here
## Docs impact
README.md (fm code tui paragraph: u and P after a close), CHANGELOG.md; the help poster lists u and P
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 231 tests in 8.1s (45 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / FAILED (1 classes) [ran] [tree 1c8241c6c35b] (2026-10-23T14:23:58Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 231 tests in 8.1s (45 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 7d53b63066bc] (2026-10-23T14:24:28Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_settings test_suite_hygiene test_docs` → exit 0 · Ran 411 tests in 9.6s (84 classes, 16 at a time; slowest: Serve 9s, Fuzz 9s, Fences 8s) / OK [ran] [tree 7d53b63066bc] (2026-10-23T14:24:39Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 231 tests in 8.1s (45 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 7d53b63066bc] (2026-10-23T14:24:48Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 231 tests in 8.3s (45 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 7d53b63066bc] (2026-10-23T14:24:57Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): undo needs a closed run whose close names its commit, a second u within 2 s (the confirm key is kept only for the same command), and reverts with a new commit; it refuses a second undo of the same commit and says why a revert failed (conflicts, a dirty tree) without touching anything; the history mark is an appended event the past-runs list reads; the PR post goes through fm pr --post, which holds the publish grant check, so the app never pushes or posts on its own` → a closed run can be taken back or turned into a PR from the screen that showed it [tree 7d53b63066bc] (2026-10-23T14:24:57Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): undo needs a closed run whose close names its commit, a second u within 2 s (the confirm key is kept only for the same command), and reverts with a new commit; it refuses a second undo of the same commit and says why a revert failed (conflicts, a dirty tree) without touching anything; the history mark is an appended event the past-runs list reads; the PR post goes through fm pr --post, which holds the publish grant check, so the app never pushes or posts on its own` → no closed run (u and P say so), a run still going (refused), a revert that conflicts (said, nothing changed), Esc out of the PR draft (the post target is cleared, so a later diff view's Enter posts nothing), a run without a commit (--no-commit: nothing to undo) [tree 7d53b63066bc] (2026-10-23T14:24:57Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): undo needs a closed run whose close names its commit, a second u within 2 s (the confirm key is kept only for the same command), and reverts with a new commit; it refuses a second undo of the same commit and says why a revert failed (conflicts, a dirty tree) without touching anything; the history mark is an appended event the past-runs list reads; the PR post goes through fm pr --post, which holds the publish grant check, so the app never pushes or posts on its own` → the commit comes from fm code's own close line, matched as 7-40 hex characters, and is passed to git as one argument; posting is fm pr's, under the publish grant [tree 7d53b63066bc] (2026-10-23T14:24:57Z)
## Log
- 2026-10-21T03:47:42Z created
- 2026-10-23T14:14:59Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'README.md']
- 2026-10-23T14:22:36Z focused
- 2026-10-23T14:25:07Z done
- 2026-10-23T14:25:09Z committed fdd2477a (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1305 [FEATURE S, done, 1 steps] Fm code tui close receipt: on close a receipt card (task, checks, files, tokens, time, com
- decision 2026-10-21: T-1393: hold only the mcpServers entries of ~/.claude.json, not the whole file
- similar finished tasks took 1–3 steps
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, README.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A destructive key wants its confirmation state cleared only by a different key, not by any key
## Plan gaps
- failed first: step 1 red tests: undo and the PR draft
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- README.md
