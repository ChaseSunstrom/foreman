---
id: T-1085
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmrollback.py, plugin/lib/fmguard.py, plugin/tests/test_tidy.py, plugin/tests/test_guard.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T07:05:13Z
base: 017c0b7c2c35b0fc8ccb8cb76863fbb45a30ca03
base_tree: 7e8060c5b0abba00c5c6b69176235414aac88edf
verified: strong
---
# State rollback on upgrade: fm keeps a snapshot of state before a Foreman upgrade and fm ro
## Raw request
> FEATURE: State rollback on upgrade: fm keeps a snapshot of state before a Foreman upgrade and fm rollback restores it (catalogue C6)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
When Foreman's version changes, `fm` snapshots the state first; `fm rollback` lists snapshots and restores the chosen one (the latest by default). Already present: `_backup_state` writes per-project tarballs on `tidy --apply` (fmtidy.py:203, BACKUP_PARTS), and the upgrade is detected via `seen-version` in `_whats_new_note` (fmhooks.py:381-408). There is no restore, and no snapshot at upgrade.
## Assumptions (confidence)
## Acceptance criteria
- [x] After a simulated upgrade, `fm rollback --yes` restores a deleted brief. — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
(a) reuse the tidy backups, (b) a new snapshot at upgrade, (c) git for state. Choice is (b), reusing the BACKUP_PARTS logic. In `_whats_new_note`, when `old` exists and differs from `rev`, call `fmtidy.snapshot_upgrade(old)`. It tars each project's BACKUP_PARTS into `state/snapshots/<old>-<ts>.tar.gz`, keeping the last 3. Add `cmd_rollback` in fmtidy.py with `fm rollback [--list] [--to NAME] --yes`. It refuses without `--yes`, makes a safety tar first, then extracts.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: write `seen-version=0.1`, run the SessionStart hook (the version differs), assert a snapshot file exists. Delete a brief, run `fm rollback` (it refuses, exit nonzero, says "--yes"), then `fm rollback --yes` brings the brief back. `fm rollback --list` names the snapshot.
2. [x] Implement `snapshot_upgrade` and `cmd_rollback`; register the parser entry near `tidy` (fmcli.py:4669); call the snapshot from fmhooks.py.
## Resume here
## Docs impact
MASTER.md Rollback; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 27 tests in 2.8s (12 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 2s, Apply 2s) / FAILED (1 classes) [ran] [tree b0c21478abcb] (2026-10-16T06:47:55Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_board_hooks` → ✗ exit 1 · Ran 34 tests in 7.1s (14 classes, 16 at a time; slowest: StalePlans 7s, Apply 6s, DeferredTriage 5s) / FAILED (1 classes) [ran] [tree 2a7ec8c4c034] (2026-10-16T06:48:17Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_board_hooks` → exit 0 · Ran 34 tests in 3.0s (14 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 3s, Apply 3s) / OK [ran] [tree fb63ca676559] (2026-10-16T06:48:25Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_guard test_board_hooks` → exit 0 · Ran 148 tests in 6.6s (61 classes, 16 at a time; slowest: GuardAgainstBash 6s, StalePlans 3s, Apply 3s) / OK [ran] [tree 15a0bf52151e] (2026-10-16T06:59:16Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_guard test_help` → exit 0 · Ran 146 tests in 6.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 6s, StalePlans 4s, Apply 3s) / OK [ran] [tree c6b024f27ef1] (2026-10-16T07:03:24Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 31 tests in 2.9s (12 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 3s, Apply 2s) / OK [ran] [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (step 1) `python3 plugin/tests/run.py test_tidy test_guard test_help test_board_hooks` → exit 0 · Ran 153 tests in 7.1s (63 classes, 16 at a time; slowest: GuardAgainstBash 7s, StalePlans 4s, Apply 3s) / OK [ran] [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (audit intent) `review: one fm-reviewer pass (adversary first); 2 HIGH (agent-runnable consent resurrection, ledger chain break) and 4 more fixed test-first; an automated security review's flag-abbreviation finding fixed in both layers (prefix match in the guard, allow_abbrev=False)` → an upgrade that damages state can be undone with one command [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (audit adversary) `review: one fm-reviewer pass (adversary first); 2 HIGH (agent-runnable consent resurrection, ledger chain break) and 4 more fixed test-first; an automated security review's flag-abbreviation finding fixed in both layers (prefix match in the guard, allow_abbrev=False)` → the agent can't run it (user-only, every flag spelling); extraction is filter='data' into a temp dir with a manifest check; consent and the ledger are never rolled back [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (audit edge) `review: one fm-reviewer pass (adversary first); 2 HIGH (agent-runnable consent resurrection, ledger chain break) and 4 more fixed test-first; an automated security review's flag-abbreviation finding fixed in both layers (prefix match in the guard, allow_abbrev=False)` → a killed snapshot leaves a .part that is cleaned and retried; tasks archived since aren't duplicated; pre-rollback copies can't become the default target [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (audit operator) `review: one fm-reviewer pass (adversary first); 2 HIGH (agent-runnable consent resurrection, ledger chain break) and 4 more fixed test-first; an automated security review's flag-abbreviation finding fixed in both layers (prefix match in the guard, allow_abbrev=False)` → snapshot runs detached, off the 5 s hook path; fm rollback --list [--json] names the snapshots [tree 347cabb507f6] (2026-10-16T07:04:08Z)
- (audit maintainer) `review: one fm-reviewer pass (adversary first); 2 HIGH (agent-runnable consent resurrection, ledger chain break) and 4 more fixed test-first; an automated security review's flag-abbreviation finding fixed in both layers (prefix match in the guard, allow_abbrev=False)` → own module fmrollback; USER_ONLY_FM is the one table for user-only fm commands [tree 347cabb507f6] (2026-10-16T07:04:08Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:48Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T04:22:48Z set tier=M
- 2026-10-16T06:47:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1085.builder.md
- 2026-10-16T06:47:24Z focused
- 2026-10-16T06:59:09Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmrollback.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_tidy.py', 'plugin/tests/test_guard.py']
- 2026-10-16T07:03:43Z merged worktree-agent-a1fcbe38af7beb383 (6 file(s))
- 2026-10-16T07:03:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1fcbe38af7beb383
- 2026-10-16T07:03:45Z focused
- 2026-10-16T07:03:57Z scope: CHANGELOG.md, MASTER.md — docs for rollback; plugin/lib/fmrollback.py, fmguard.py, test_guard.py came with the merge (logged by the builder)
- 2026-10-16T07:05:11Z done
- 2026-10-16T07:05:13Z committed f4af16c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py, plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmrollback.py, plugin/lib/fmtidy.py, plugin/tests/test_guard.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Lessons
- A restore must not restore permission: re-apply the live consent after putting old state back
## Plan gaps
- failed first: step 1 Failing tests: write `seen-version=0.1`, run the SessionStart hook (the version differs), assert a …
- failed first: step 2 Implement `snapshot_upgrade` and `cmd_rollback`; register the parser entry near `tidy` (fmcli.py:46…
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmhooks.py
- plugin/lib/fmtidy.py
- plugin/lib/fmcli.py
- plugin/lib/fmrollback.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- CHANGELOG.md
- MASTER.md
