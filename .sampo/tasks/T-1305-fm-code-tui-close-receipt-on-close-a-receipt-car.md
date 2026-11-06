---
id: T-1305
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, plugin/tests/fixtures/golden/demo-30.0s.txt, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T00:22:52Z
updated: 2026-10-23T09:33:16Z
base: eea3069ed6b7bb6e22b81c6c084f707e0289173e
base_tree: f9c312bd77495a72db6e43c1859b6c2ba7221254
plan0_at: 2026-10-23T09:30:10Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code tui close receipt: on close a receipt card (task, checks, files, tokens, time, com
## Raw request
> fm code tui close receipt: on close a receipt card (task, checks, files, tokens, time, commit) assembles in the Activity panel, and on quit the final frame is printed to the scrollback so the run stays readable (T-1300 brainstorm C6)
## Interpretation
On close the app adds a receipt line to Activity (task, checks passed of all, files and +/− lines, tokens, cost when known, run time, commit or 'not committed'), shown in --plain too; on quit, once the alternate screen is gone, the last frame is written to stdout as plain text (printable characters only, trailing blanks trimmed) so the run stays readable in the scrollback. One line, not a multi-row card: the Activity panel is a list of lines.
## Assumptions (confidence)
## Acceptance criteria
- [x] a closed run's log ends with its receipt line, and run_screen leaves the last frame as plain text on stdout with no escape — verify with `python3 plugin/tests/run.py test_code_tui.Receipt`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then State.receipt, the receipt entry and final_frame after the session
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui.Receipt` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Receipt 0s) / FAILED (1 classes) [ran] [tree a2c45f37c90c] (2026-10-23T09:30:17Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 207 tests in 8.1s (37 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree b2904c7e4e7d] (2026-10-23T09:33:03Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Receipt` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Receipt 0s) / OK [ran] [tree b2904c7e4e7d] (2026-10-23T09:33:04Z)
- (audit edge) `self review; test_code_tui and test_code green; the demo golden regenerated on purpose (one row: the receipt)` → no stat, no usd, no ts or no commit each drop or say their part ('not committed'); a render failure at quit writes nothing rather than crash; control characters never reach the scrollback (test) [tree b2904c7e4e7d] (2026-10-23T09:33:04Z)
- (audit self) `self review; test_code_tui and test_code green; the demo golden regenerated on purpose (one row: the receipt)` → no findings [tree b2904c7e4e7d] (2026-10-23T09:33:04Z)
## Log
- 2026-10-21T00:22:52Z created
- 2026-10-21T03:48:21Z steer (catalogue U8): the closed event carries one line 'You asked X → did Y · checks 3/3 · commit abc' and up to two suggested next requests; the close card shows them and history rows show that line
- 2026-10-23T09:23:32Z set tier=S, scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T09:30:09Z focused
- 2026-10-23T09:31:30Z set scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/fixtures/golden/demo-30.0s.txt', 'CHANGELOG.md']
- 2026-10-23T09:32:55Z scope: the demo golden shows the receipt line at 30 s; regenerated with FM_GOLDEN=regen on purpose
- 2026-10-23T09:33:14Z done
- 2026-10-23T09:33:16Z committed 7b7ac5e5 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- playbook Terminal and mod UI (fm playbooks show ui/terminal-ui)
- decision 2026-10-22: T-1508: keep the 2,000-character skill-listing budget; make room by trimming the longest Foreman skill descriptions, not by raising the cap
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 test, then State.receipt, the receipt entry and final_frame after the session
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-30.0s.txt
- CHANGELOG.md
