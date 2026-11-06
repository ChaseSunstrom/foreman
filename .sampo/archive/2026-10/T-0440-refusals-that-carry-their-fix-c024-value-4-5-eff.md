---
id: T-0440
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:39:54Z
base: d226d7e96e60bb5f81317de504d5b948e1087556
base_tree: 617130e57a1bfa4daabf720ecb33a0db214e60f0
verified: strong
---
# Every refusal names its fix; a third identical refusal escalates
## Raw request
> SECURITY: Refusals that carry their fix (C024, value 4/5, effort M, risk low)
>   first version: Audit refusal messages so each names the allowed form (fixture test that every block reason has an 'instead/use' clause), and add a repeated-refusal counter in the hook that escalates to fm ask or task block after 3 identical blocks. Never rewrites and runs commands itself.
>   what it is: Every guard refusal says what is allowed instead, rewrites the command, and stops loops of repeated refusals.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Every guard block names an allowed form (fm ask / --allow / fm focus / fm lane / the rewrite), and the same block three times in a row in one session stops inviting a retry: it says to ask (fm ask) or block the task. Only text and a counter are added; the deny decision never changes, so nothing loosens.
## Assumptions (confidence)
## Acceptance criteria
- [x] every category's refusal names an allowed form — verify with `python3 plugin/tests/run.py -k test_every_refusal_names_its_fix`
- [x] the third identical refusal escalates and a different one resets the count — verify with `python3 plugin/tests/run.py -k test_third_identical_refusal_escalates`
## Non-goals
## Approach (options → choice → why)
(B, chosen) audit _message/_hint so each category names a fix + a per-session repeat counter in _pre_tool_use. (A) audit only: retries continue. (C, rejected) auto-rewrite commands: could loosen the guard.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: both tests
2. [x] fix-clause for categories that lack one (confine: fm lane …)
3. [x] repeat counter + escalation text in _pre_tool_use; guard suites unchanged
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_every_refusal_names_its_fix -k test_third_identical_refusal_escalates` → ✗ exit 1 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: PreToolUse 1s) / FAILED (1 classes) [ran] [tree f600fc797afc] (2026-10-09T14:38:55Z)
- (step 3) `python3 plugin/tests/run.py -k test_every_refusal_names_its_fix -k test_third_identical_refusal_escalates` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: PreToolUse 1s) / OK [ran] [tree ae68c56d9881] (2026-10-09T14:39:18Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_refusal_names_its_fix` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 85b48d75992e] (2026-10-09T14:39:53Z)
- (ac 1) `python3 plugin/tests/run.py -k test_every_refusal_names_its_fix` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 85b48d75992e] (2026-10-09T14:39:54Z)
- (ac 2) `python3 plugin/tests/run.py -k test_third_identical_refusal_escalates` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: PreToolUse 1s) / OK [ran] [tree 85b48d75992e] (2026-10-09T14:39:54Z)
- (audit adversary) `self: escalation is text only, appended to the same deny; streak read from this session's events (blocks and tool calls), reset by any other call or a different block; every category's message already names a fix (pinned by a test, so step 2 needed no change); hooks + guard suites OK` → no decision changes: the deny stays; the streak can't be gamed into allowing anything [tree 85b48d75992e] (2026-10-09T14:39:54Z)
- (audit edge) `self: escalation is text only, appended to the same deny; streak read from this session's events (blocks and tool calls), reset by any other call or a different block; every category's message already names a fix (pinned by a test, so step 2 needed no change); hooks + guard suites OK` → parallel tool calls could interleave events; a miscount only shifts when the hint appears [tree 85b48d75992e] (2026-10-09T14:39:54Z)
- (audit intent) `self: escalation is text only, appended to the same deny; streak read from this session's events (blocks and tool calls), reset by any other call or a different block; every category's message already names a fix (pinned by a test, so step 2 needed no change); hooks + guard suites OK` → the third retry of the same refused command now points to fm ask or fm task block, as the grounding asked [tree 85b48d75992e] (2026-10-09T14:39:54Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:38:29Z planned from capture
- 2026-10-09T14:38:30Z focused
- 2026-10-09T14:39:54Z done
- 2026-10-09T14:39:54Z committed 4a5388c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0510 [SECURITY M, dropped, 0 steps] Refusals that carry their fix (C024, value 4/5, effort M, risk low)
- T-0442 [SECURITY M, planned, 2 steps] Guard parity across harnesses: same decision on codex, gemini and opencode
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
## Lessons
- A retry loop is a signal: the third identical refusal should change what the refusal says.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
