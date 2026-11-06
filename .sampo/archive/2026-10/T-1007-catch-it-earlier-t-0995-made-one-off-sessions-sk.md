---
id: T-1007
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T01:07:10Z
updated: 2026-10-16T01:11:56Z
base: 07c967e5d5d7898a60d4d30181374d532aa7e872
base_tree: 3c7c1f723dec828853260408b6dce92ac05d7f1f
verified: strong
---
# A one-off session leaves the project's briefs untouched through every hook
## Raw request
> T-1004 (A one-off session records no evidence on another session's task) wasn't caught before it shipped: T-0995 made one-off sessions skip the drive and the fleet but no test ran a one-off session's Bash through PostToolUse
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a FOREMAN_ONEOFF=1 session's SessionStart, UserPromptSubmit, PreToolUse/PostToolUse (Bash, Edit) and Stop leave every brief byte-identical — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] sweep test over the hooks with a focused task; fix whatever writes
2. [x] docs: none (test only) unless a fix lands
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k one_off_session_leaves` → ✗ exit 1 · Ran 154 tests in 31.6s (20 classes, 16 at a time; slowest: Stop 32s, PreToolUse 16s, Approvals 12s) / FAILED (1 classes) [ran] [tree 906deba07014] (2026-10-16T01:08:51Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_bookkeeping` → exit 0 · Ran 166 tests in 32.3s (28 classes, 16 at a time; slowest: Stop 32s, PreToolUse 17s, SessionStart 13s) / OK [ran] [tree 9715b6de4db1] (2026-10-16T01:09:35Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 154 tests in 31.9s (20 classes, 16 at a time; slowest: Stop 32s, PreToolUse 16s, Approvals 13s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9715b6de4db1] (2026-10-16T01:10:45Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 154 tests in 31.6s (20 classes, 16 at a time; slowest: Stop 32s, PreToolUse 16s, Approvals 13s) / OK [ran] [tree 9715b6de4db1] (2026-10-16T01:10:45Z)
- (step 2) `grep -q 'T-1007' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 0e45846bd835] (2026-10-16T01:10:45Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 154 tests in 31.5s (20 classes, 16 at a time; slowest: Stop 31s, PreToolUse 16s, SessionStart 13s) / OK [ran] [tree 0e45846bd835] (2026-10-16T01:11:17Z)
- (audit edge) `self` → one-off edits still logged (task=None) so tidy/blame keep them; scope notes and thrash notes skip for one-offs (no task); Bash-touch attribution skipped [tree 0e45846bd835] (2026-10-16T01:11:22Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 154 tests in 31.5s (20 classes, 16 at a time; slowest: Stop 31s, PreToolUse 16s, Approvals 13s) / OK [ran] [tree 0e45846bd835] (2026-10-16T01:11:54Z)
- (audit edge) `sweep test over SessionStart, UserPromptSubmit, Pre/PostToolUse (Bash, Write), Stop under FOREMAN_ONEOFF=1; red→green proved` → working-session attribution unchanged (bookkeeping suite green) [tree 0e45846bd835] (2026-10-16T01:11:54Z)
- (audit self) `sweep test over SessionStart, UserPromptSubmit, Pre/PostToolUse (Bash, Write), Stop under FOREMAN_ONEOFF=1; red→green proved` → no findings [tree 0e45846bd835] (2026-10-16T01:11:54Z)
## Log
- 2026-10-16T01:07:10Z created
- 2026-10-16T01:07:26Z planned from capture
- 2026-10-16T01:07:26Z focused
- 2026-10-16T01:09:41Z set type=FIX
- 2026-10-16T01:11:55Z done
- 2026-10-16T01:11:56Z committed 75d559b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0997 [FEATURE S, dropped, 0 steps] Catch it earlier: T-0705's fixture had one Python test and steps that were all code steps;
- T-0996 [FEATURE S, dropped, 0 steps] Catch it earlier: the harness had only been used with local commands (/fm) or single promp
- T-1006 [FEATURE S, dropped, 0 steps] Catch it earlier: T-1001's test seeded by-pid records for the killed session, so it never
- decision 2026-10-14: Stop the recursive improvement loop after round 3's probe: 46 new ideas, 1 grounded build (already shipped as T-0836), so it's dry by the <3 rule
## Why not caught
no sweep test ran a one-off session through every hook; added one
## Plan gaps
- failed first: step 1 sweep test over the hooks with a focused task; fix whatever writes
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
