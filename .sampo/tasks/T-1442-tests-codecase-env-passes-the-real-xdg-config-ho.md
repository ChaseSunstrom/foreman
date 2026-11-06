---
id: T-1442
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_code.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T22:37:08Z
updated: 2026-10-22T15:56:46Z
base: 5962fe079074cbba746cabbdc8dd6ebd0e08c778
base_tree: 14b0f9bc72848f619ff883a9ef3ef8554458d2a4
plan0_at: 2026-10-22T15:39:51Z
plan0_scope: [plugin/tests/test_code.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md]
verified: strong
---
# Tests keep XDG_CONFIG_HOME inside the temp HOME; fm tidy ages out reverted copies
## Raw request
> tests: CodeCase.env passes the real XDG_CONFIG_HOME through, so tests relying on the ~/.config default can look outside the temp HOME; and fm code's reverted/ copies are never pruned (fm tidy could age them out) (T-1417 builder)
## Interpretation
CodeCase.env (test_code.py:120) passes the real XDG_CONFIG_HOME through, so a test relying on the ~/.config default can read or write outside its temp HOME. fm code's judge keeps a private copy of each file it reverts under <journal dir>/reverted/ (fmcode ~1232) and nothing ever removes them.
## Assumptions (confidence)
## Acceptance criteria
- [x] CodeCase's env points every XDG dir inside the temp HOME — verify with `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home`
- [x] fm tidy lists then removes reverted copies older than 30 days and keeps newer ones and links — verify with `cd plugin/tests && python3 -m unittest test_tidy.Apply.test_old_reverted_copies_are_aged_out`
## Non-goals
## Approach (options → choice → why)
CodeCase.env sets XDG_CONFIG_HOME (and XDG_DATA_HOME/XDG_STATE_HOME/XDG_CACHE_HOME) under the temp HOME. fm tidy gains a prune of reverted/ entries older than 30 days, beside _prune_snapshots (fmtidy.py:399): dry-run lists, --apply removes; never follows links (the folder is private, 0700, but a link inside is skipped).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] XDG env in CodeCase
3. [x] reverted prune in fm tidy
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code.CodeEnv test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 2 tests in 1.983s / OK [ran] [tree 40ff20e57d5e] (2026-10-22T15:43:50Z)
- (step 2) `python3 plugin/tests/run.py test_code.CodeEnv` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: CodeEnv 1s) / OK [ran] [tree 40ff20e57d5e] (2026-10-22T15:49:02Z)
- (step 3) `python3 plugin/tests/run.py test_tidy.Apply` → exit 0 · Ran 7 tests in 11.9s (1 classes, 16 at a time; slowest: Apply 11s) / OK [ran] [tree 40ff20e57d5e] (2026-10-22T15:49:16Z)
- `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home test_tidy.Apply.test_old_reverted_copies_are_aged_out` → ✗ exit 1 · Ran 2 tests in 0.718s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 86d26d79d952] (2026-10-22T15:53:17Z)
- `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 2 tests in 0.737s / OK [ran] [tree 86d26d79d952] (2026-10-22T15:53:17Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 2 tests in 0.675s / OK [ran] [tree 86d26d79d952] (2026-10-22T15:53:18Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 2 tests in 0.719s / OK [ran] [tree 86d26d79d952] (2026-10-22T15:53:20Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 2 tests in 0.731s / OK [ran] [tree 86d26d79d952] (2026-10-22T15:53:22Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code.CodeEnv.test_xdg_dirs_stay_inside_the_temp_home` → exit 0 · Ran 1 test in 0.023s / OK [ran] [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_tidy.Apply.test_old_reverted_copies_are_aged_out` → exit 0 · Ran 1 test in 0.513s / OK [ran] [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
- (audit adversary) `builder (sonnet) test-first; red proved with fm task prove; merged; test_tidy green and the CodeEnv test green.` → the prune lstat's and unlinks plain files only inside <project state>/code/reverted; a link (file, or the folder itself) is skipped; never follows [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
- (audit edge) `builder (sonnet) test-first; red proved with fm task prove; merged; test_tidy green and the CodeEnv test green.` → a file gone between listing and unlink is ignored; a second run removes nothing [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
- (audit operator) `builder (sonnet) test-first; red proved with fm task prove; merged; test_tidy green and the CodeEnv test green.` → dry run lists old_reverted before --apply removes [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
- (audit self) `builder (sonnet) test-first; red proved with fm task prove; merged; test_tidy green and the CodeEnv test green.` → no findings [tree 62fa6fb1fff9] (2026-10-22T15:54:07Z)
## Log
- 2026-10-21T22:37:08Z created
- 2026-10-22T15:39:21Z planned from capture
- 2026-10-22T15:39:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1442.builder.md
- 2026-10-22T15:39:50Z focused
- 2026-10-22T15:53:11Z merged worktree-agent-a0227506cf6486435 (3 file(s))
- 2026-10-22T15:53:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0227506cf6486435
- 2026-10-22T15:53:13Z focused
- 2026-10-22T15:56:43Z done
- 2026-10-22T15:56:46Z committed 04565bdd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1434-1417-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** T-1438 approve. T-1434 changes needed. T-1417 change…
- research T-1294-review: Verdict: approve with nits.** The diff file holds only the CHANGELOG hunk. I reviewed the real working-tree changes in `fmbus.py`, `fmcode.py` an…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-15: Keep claude plugin install under the plugin category even with HOME=<scratch>; no exemption (T-0893 dropped)
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmtidy.py, plugin/tests/test_code.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
