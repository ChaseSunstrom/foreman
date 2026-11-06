---
id: T-1715
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T01:27:53Z
updated: 2026-10-23T02:39:00Z
base: 4306a4308492dc32302d14d75477fb15454a3d16
base_tree: 4de28ddbc6046741df15b95f1d6a56a526c1daf3
plan0_at: 2026-10-23T02:30:18Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# The first-UI-edit note names foreman:ui-design (it still said /foreman:directions)
## Raw request
> The first-UI-edit note (fmhooks.py:1916) still points to /foreman:directions; point it at foreman:ui-design (which routes to directions)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the first UI edit's note names Skill foreman:ui-design — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] note wording
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k first_ui_edit` → red as expected (exit 1) · Ran 201 tests in 86.2s (24 classes, 16 at a time; slowest: Stop 86s, NoTaskGate 71s, PreToolUse 64s) / FAILED (1 classes) [ran] [tree 9ae8edc4eb4a] (2026-10-23T02:31:56Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_context_tax` → exit 0 · Ran 202 tests in 121.1s (25 classes, 16 at a time; slowest: Stop 121s, NoTaskGate 94s, PreToolUse 89s) / OK [ran] [tree a3865b575c66] (2026-10-23T02:33:58Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 201 tests in 84.7s (24 classes, 16 at a time; slowest: Stop 84s, NoTaskGate 65s, PreToolUse 59s) / OK [ran] [tree 4b4608d8fdac] (2026-10-23T02:35:31Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 201 tests in 53.4s (24 classes, 16 at a time; slowest: Stop 52s, NoTaskGate 37s, PreToolUse 30s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4b4608d8fdac] (2026-10-23T02:37:12Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 201 tests in 47.0s (24 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 34s, PreToolUse 28s) / OK [ran] [tree 4b4608d8fdac] (2026-10-23T02:37:12Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 201 tests in 52.0s (24 classes, 16 at a time; slowest: Stop 52s, NoTaskGate 36s, PreToolUse 29s) / OK [ran] [tree 4b4608d8fdac] (2026-10-23T02:38:04Z)
- (audit intent) `self-review: one note's wording; the skill-exists check now looks for ui-design; the note stays under its 300-char cap (tested); prompt budget unaffected (a PreToolUse note)` → the first UI edit points at the job skill that walks direction, tokens, motion and checks [tree 4b4608d8fdac] (2026-10-23T02:38:04Z)
- (audit edge) `self-review: one note's wording; the skill-exists check now looks for ui-design; the note stays under its 300-char cap (tested); prompt budget unaffected (a PreToolUse note)` → without the ui-design skill installed the note names only the playbook [tree 4b4608d8fdac] (2026-10-23T02:38:04Z)
- (audit self) `self-review: one note's wording; the skill-exists check now looks for ui-design; the note stays under its 300-char cap (tested); prompt budget unaffected (a PreToolUse note)` → no findings [tree 4b4608d8fdac] (2026-10-23T02:38:04Z)
## Log
- 2026-10-23T01:27:53Z created
- 2026-10-23T02:30:17Z planned from capture
- 2026-10-23T02:30:17Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-23T02:30:18Z focused
- 2026-10-23T02:38:58Z done
- 2026-10-23T02:39:00Z committed 1f2da113 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1514 [FEATURE S, done, 2 steps] Brainstorm T-1479 round 2 (cluster 19): a soft hook note asking for a design direction (DE — lesson: A nudge that fires once per task n…
- research T-0264-review-1: All three reviews are below. Only fmhooks, fmcore, fmcli, fmplugins and fmevolve were read. I did not run the tests or the PreToolUse hook. [st…
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Why not caught
T-1700 updated SKILL_FOR but the PreToolUse UI note builds its own string
## Lessons
- When a router skill lands, sweep every hook string that named the old entry point
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
