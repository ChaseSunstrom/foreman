---
id: T-0127
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-03T04:44:01Z
updated: 2026-10-03T05:19:32Z
base: fc545fe5ec6a80064857210baf6da1827bd1a40c
base_tree: 0a8f13d1a4ad7e2495b45de6bd1c3af44bbb4468
verified: strong
---
# Past-task lesson notes repeat on every edit of a shared file; skip lessons from tasks closed this session
## Raw request
> Past-task lesson notes repeat on every edit of the same file (PostToolUse context): show each once per file per session to save tokens
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] one note per file per session; none for a task closed in the same session — verify with `python3 plugin/tests/run.py -k lesson_notes_never -k says_it_once`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, fix _tripwire_note
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_memory.py -k lesson_notes_never -k says_it_once` → ✗ exit 1 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: Memory 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3f4fe869c943] (2026-10-03T05:18:21Z)
- (step 1) `python3 plugin/tests/run.py -p test_memory.py -k lesson_notes_never -k says_it_once` → ✗ exit 1 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: Memory 2s) / FAILED (1 classes) [ran] [tree 3f4fe869c943] (2026-10-03T05:18:21Z)
- (step 1) `python3 plugin/tests/run.py -p test_memory.py -k lesson_notes_never -k says_it_once` → ✗ exit 1 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: Memory 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4fb6bc32812b] (2026-10-03T05:18:38Z)
- (step 1) `python3 plugin/tests/run.py -p test_memory.py -k lesson_notes_never -k says_it_once` → exit 0 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: Memory 2s) / OK [ran] [tree 4fb6bc32812b] (2026-10-03T05:18:38Z)
- (ac 1) `python3 plugin/tests/run.py -k lesson_notes_never -k says_it_once` → exit 0 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: Memory 2s) / OK [ran] [tree 33b692d3d1ef] (2026-10-03T05:19:32Z)
- (step 1) `python3 plugin/tests/run.py -p test_memory.py` → exit 0 · Ran 8 tests in 3.5s (1 classes, 16 at a time; slowest: Memory 4s) / OK [ran] [tree 33b692d3d1ef] (2026-10-03T05:19:32Z)
- (audit self) `self: per-file key and same-session skip; ledger tail 400 per edit only after the cheap checks pass` → no findings [tree 33b692d3d1ef] (2026-10-03T05:19:32Z)
## Log
- 2026-10-03T04:44:01Z created
- 2026-10-03T05:18:00Z planned from capture
- 2026-10-03T05:18:00Z focused
- 2026-10-03T05:18:45Z scope: run.py printed OK for zero tests while exiting 1 (T-0133 follow-up, one word)
- 2026-10-03T05:19:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- playbook Context Budget (skills/playbooks/references/context/context-budget.md)
- research t0036-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:341-364` (`_pin_problem`) and `~/.claude/foreman/plugin/lib/fmguard.py…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
## Files touched
- plugin/tests/test_memory.py
- plugin/lib/fmhooks.py
- plugin/tests/run.py
