---
id: T-1775
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py]
depends_on: []
source: user
created: 2026-10-23T10:40:47Z
updated: 2026-10-23T10:42:18Z
base: cf757494ca5f31ef99c6f77ff1386ed50ffe407a
base_tree: a2ca3e4b9283d5f8d0db72523c2ac7b1e7907bb6
plan0_at: 2026-10-23T10:40:49Z
plan0_scope: [plugin/lib/fmcli.py]
verified: strong
---
# fm dojo shares help position 306 with another command, so test_help fails
## Raw request
> fm dojo shares help position 306 with another command, so test_help fails
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every command has its own help position — verify with `python3 plugin/tests/run.py test_help`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] move fm dojo to 307
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_help` → ✗ exit 1 · Ran 7 tests in 1.7s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / FAILED (1 classes) [ran] [tree a2ca3e4b9283] (2026-10-23T10:40:56Z)
- (step 1) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 7 tests in 1.7s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 57fbe824d6d0] (2026-10-23T10:41:05Z)
- (ac 1) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 7 tests in 1.7s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 57fbe824d6d0] (2026-10-23T10:41:08Z)
- (audit edge) `self review; test_help green` → 307 was free between 306 (fm whatsnew? the earlier site) and 310; only the order of fm help's Finding your way tier moves [tree 57fbe824d6d0] (2026-10-23T10:41:08Z)
- (audit self) `self review; test_help green` → no findings [tree 57fbe824d6d0] (2026-10-23T10:41:08Z)
## Log
- 2026-10-23T10:40:47Z created
- 2026-10-23T10:40:48Z focused
- 2026-10-23T10:41:51Z done
- 2026-10-23T10:41:55Z committed 7c72bdb7 (1 file)
- 2026-10-23T10:42:18Z includes T-1774: Baseline red: `python3 plugin/tests/run.py` fails test_help.Help.test_each_command_has_its
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1608 [FEATURE S, done, 1 steps] Dangerous-command dojo for people: a short interactive drill of commands the guard refuses
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- similar finished tasks took 1–4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
T-1608 ran test_guard_hardening, test_docs and test_cli; the help-position test lives in test_help, which only the full suite ran
## Plan gaps
- failed first: step 1 move fm dojo to 307
## Files touched
- plugin/lib/fmcli.py
