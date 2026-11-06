---
id: T-1663
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_backlog.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:59:02Z
updated: 2026-10-23T03:54:17Z
base: 6c426be0e9725c9ed85db6c06e80d408edce55d2
base_tree: 72e28a5a57344a9489db25cc00f291ab46c61798
plan0_at: 2026-10-23T03:13:48Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_backlog.py, CHANGELOG.md]
verified: strong
---
# Re-verify queue: a later commit touching a closed task's files queues that task's verify through the sentinel
## Raw request
> Re-verify queue: a later commit touching a closed task's files queues that task's verify through the sentinel
## Interpretation
Re-verify queue: when a commit touches files a closed task's scope covered, that task's verify commands are queued for a re-run through the sentinel; a failure reopens attention by capturing a FIX naming the task.
## Assumptions (confidence)
## Acceptance criteria
- [x] a commit to a closed task's file queues a re-verify entry — verify with `python3 plugin/tests/run.py test_backlog.Reverify`
## Non-goals
## Approach (options → choice → why)
Options: rerun every closed task's checks (too slow); none (regressions hide); scope-to-commit matching. Choice: scope matching with a cap per commit, through the existing sentinel queue.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a temp repo
2. [x] scope-to-commit map
3. [x] queue entry through the sentinel
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_backlog.Reverify 2>&1 | tail -8` → ✗ exit 1 · Ran 2 tests in 12.4s (1 classes, 16 at a time; slowest: Reverify 9s) / FAILED (1 classes) [ran] [tree a3d3ec167840] (2026-10-23T03:16:21Z)
- (step 1) `python3 plugin/tests/run.py test_backlog.Reverify` → ✗ exit 1 · Ran 2 tests in 9.9s (1 classes, 16 at a time; slowest: Reverify 9s) / FAILED (1 classes) [ran] [tree a3d3ec167840] (2026-10-23T03:16:53Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Reverify 2>&1 | grep -v "^$" | tail -25` → exit 0 · Ran 2 tests in 9.1s (1 classes, 16 at a time; slowest: Reverify 9s) / OK [ran] [tree 6964505c1db8] (2026-10-23T03:17:45Z)
- (step 2) `python3 plugin/tests/run.py test_backlog.Reverify` → exit 0 · Ran 2 tests in 9.5s (1 classes, 16 at a time; slowest: Reverify 8s) / OK [ran] [tree 6010c8127c70] (2026-10-23T03:19:30Z)
- (step 3) `python3 plugin/tests/run.py test_backlog.Reverify test_verify_strength test_planning test_release` → ✗ exit 1 · Ran 68 tests in 71.1s (18 classes, 16 at a time; slowest: Release 69s, VerifyStrength 54s, BoardVerbs 50s) / FAILED (1 classes) [ran] [tree 6010c8127c70] (2026-10-23T03:20:43Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Reverify` → exit 0 · Ran 2 tests in 14.1s (1 classes, 16 at a time; slowest: Reverify 13s) / OK [ran] [tree 6010c8127c70] (2026-10-23T03:21:00Z)
- (step 3) `python3 plugin/tests/run.py test_backlog.Reverify test_verify_strength test_planning test_release test_board_verbs` → exit 0 · Ran 74 tests in 32.8s (18 classes, 16 at a time; slowest: BoardVerbs 33s, VerifyStrength 29s, Release 28s) / OK [ran] [tree cb45779df5ad] (2026-10-23T03:23:44Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Reverify` → exit 0 · Ran 2 tests in 2.5s (1 classes, 16 at a time; slowest: Reverify 2s) / OK [ran] [tree ebd3e0d7bfb4] (2026-10-23T03:24:26Z)
- (step 1) `python3 plugin/tests/run.py test_backlog` → ✗ exit 1 · Ran 9 tests in 12.1s (2 classes, 16 at a time; slowest: Reverify 12s, ReverifyScan 1s) / FAILED (1 classes) [ran] [tree e98288150981] (2026-10-23T03:34:57Z)
- (step 2) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 9 tests in 37.9s (2 classes, 16 at a time; slowest: Reverify 36s, ReverifyScan 4s) / OK [ran] [tree 292800fefd17] (2026-10-23T03:38:33Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 9 tests in 48.6s (2 classes, 16 at a time; slowest: Reverify 48s, ReverifyScan 4s) / OK [ran] [tree d55c4aa6afc6] (2026-10-23T03:40:06Z)
- (step 3) `python3 plugin/tests/run.py test_backlog test_verify_strength test_planning test_board_verbs` → exit 0 · Ran 52 tests in 77.3s (15 classes, 16 at a time; slowest: BoardVerbs 76s, VerifyStrength 53s, Reverify 35s) / OK [ran] [tree d55c4aa6afc6] (2026-10-23T03:41:25Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 9 tests in 4.9s (2 classes, 16 at a time; slowest: Reverify 5s, ReverifyScan 1s) / OK [ran] [tree f18ccae55bca] (2026-10-23T03:53:16Z)
- (step 1) `python3 plugin/tests/run.py test_backlog.Reverify` → exit 0 · Ran 9 tests in 4.8s (2 classes, 16 at a time; slowest: Reverify 5s, ReverifyScan 0s) / OK [ran] [tree f18ccae55bca] (2026-10-23T03:53:21Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Reverify` → exit 0 · Ran 9 tests in 4.8s (2 classes, 16 at a time; slowest: Reverify 5s, ReverifyScan 0s) / OK [ran] [tree f18ccae55bca] (2026-10-23T03:53:27Z)
- (audit intent) `fm-reviewer full pass; all 8 findings fixed test-first: own commits read from the Foreman-Task trailer (subject as fallback); a failed git log or ancestry check doesn't move the watermark; a rewritten history (last not an ancestor) records head only; the FIX text (output tail, subject, command, sha) goes through redact, plain, fit and defang; entries for tasks no longer done are dropped; FIX titles carry a command hash; a queued rm or curl is dropped and never run; --max leaves the rest queued; 5 tasks per commit` → a later commit touching a closed task's scope re-runs that task's checks in fm sentinel and captures a FIX naming the task when one fails [tree f18ccae55bca] (2026-10-23T03:53:27Z)
- (audit adversary) `fm-reviewer full pass; all 8 findings fixed test-first: own commits read from the Foreman-Task trailer (subject as fallback); a failed git log or ancestry check doesn't move the watermark; a rewritten history (last not an ancestor) records head only; the FIX text (output tail, subject, command, sha) goes through redact, plain, fit and defang; entries for tasks no longer done are dropped; FIX titles carry a command hash; a queued rm or curl is dropped and never run; --max leaves the rest queued; 5 tasks per commit` → queued commands pass the sentinel's side-effect and guard filters before run_command (no shell of their own); reverify.json is written with json.dumps; commit subjects and outputs are cleaned before they reach a brief [tree f18ccae55bca] (2026-10-23T03:53:27Z)
- (audit edge) `fm-reviewer full pass; all 8 findings fixed test-first: own commits read from the Foreman-Task trailer (subject as fallback); a failed git log or ancestry check doesn't move the watermark; a rewritten history (last not an ancestor) records head only; the FIX text (output tail, subject, command, sha) goes through redact, plain, fit and defang; entries for tasks no longer done are dropped; FIX titles carry a command hash; a queued rm or curl is dropped and never run; --max leaves the rest queued; 5 tasks per commit` → first run records HEAD only; a history rewrite or branch switch records HEAD only; a timed-out git leaves the watermark; older than the newest 50 commits after a long gap are skipped (a ponytail ceiling) [tree f18ccae55bca] (2026-10-23T03:53:27Z)
- (audit operator) `fm-reviewer full pass; all 8 findings fixed test-first: own commits read from the Foreman-Task trailer (subject as fallback); a failed git log or ancestry check doesn't move the watermark; a rewritten history (last not an ancestor) records head only; the FIX text (output tail, subject, command, sha) goes through redact, plain, fit and defang; entries for tasks no longer done are dropped; FIX titles carry a command hash; a queued rm or curl is dropped and never run; --max leaves the rest queued; 5 tasks per commit` → the sentinel says how many queued entries the filters dropped [tree f18ccae55bca] (2026-10-23T03:53:27Z)
## Log
- 2026-10-22T20:59:02Z created
- 2026-10-22T20:59:04Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-10-22T20:59:05Z split from T-1548 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:03Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_backlog.Reverify`
- 2026-10-22T21:30:26Z criterion 1 text: a commit to a closed task's file queues a re-verify entry — verify with python3 plugin/tests/run.py test_backlog.Reverify → a commit to a closed task's file queues a re-verify entry
- 2026-10-23T03:13:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1663.builder.md
- 2026-10-23T03:13:47Z focused
- 2026-10-23T03:17:18Z scope: plugin/lib/fmreverify.py — the re-verify queue as its own module, keeping the edit to conflict-prone fmcli.py to cmd_sentinel
- 2026-10-23T03:23:11Z scope: MASTER.md — fm doctor's self-docs check needs every module named
- 2026-10-23T03:51:40Z merged worktree-agent-a3f697bd7e5e894ad (5 file(s))
- 2026-10-23T03:51:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3f697bd7e5e894ad
- 2026-10-23T03:53:03Z focused
- 2026-10-23T03:53:22Z scope: plugin/lib/fmreverify.py (new module), plugin/lib/fmcli.py (cmd_sentinel), MASTER.md, CHANGELOG.md
- 2026-10-23T03:54:17Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1548 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Backlog intelligence: cap new FEATURE captures against closed work, reje
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-03: T-0110 (one yes for several queued core tasks) closed as done in T-0119: the standing core yes covers every task; plugin and remote stay per-task by…
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_backlog.py; re-ground the plan against them before editing
## Lessons
- A watermark must not move when the scan that justifies it failed
## Plan gaps
- failed first: step 1 failing test with a temp repo
- failed first: step 3 queue entry through the sentinel
## Files touched
- plugin/tests/test_backlog.py
- plugin/lib/fmreverify.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmpage.py
- plugin/lib/fmrelease.py
- plugin/lib/graph.html
- plugin/tests/test_reliability_tools.py
- plugin/tests/test_showpieces.py
