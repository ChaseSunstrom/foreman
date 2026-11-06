---
id: T-2107
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T06:31:04Z
updated: 2026-10-30T11:21:27Z
base: 467794d6365fccce7ca09726f99b2cd00d89fbe6
base_tree: 1dd235411049dfddcad99153948ad9691378f000
plan0_at: 2026-10-30T11:20:39Z
plan0_scope: []
verified: strong
---
# FIX S: friction digest's swallowed-errors line names no file: fmfriction.py:181 prints…
## Raw request
> FIX S: friction digest's swallowed-errors line names no file: fmfriction.py:181 prints only errs[-1][-1]; also print the last 'File "' continuation line (recent_hook_errors fmdoctor.py:734 has them), fit to 160 chars
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm friction's swallowed-errors line names the latest error's file:line — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the last File line as basename:line to the latest error
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction` → red as expected (exit 1) · Ran 16 tests in 4.9s (5 classes, 16 at a time; slowest: Friction 5s, UserPromptSubmit 1s, BoardIdeas 0s) / FAILED (1 classes) [ran] [tree 91fef88ca99f] (2026-10-30T11:20:53Z)
- (step 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 16 tests in 4.9s (5 classes, 16 at a time; slowest: Friction 5s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree e6e3c09798ad] (2026-10-30T11:21:02Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 16 tests in 4.9s (5 classes, 16 at a time; slowest: Friction 5s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree 1de8206e4eb2] (2026-10-30T11:21:23Z)
- (audit edge) `self: read the diff; the innermost frame is the last File line in a Python traceback; a non-traceback entry (no File line) keeps the old '(state/logs/hooks.log)' form; the basename goes through c.plain like the message` → an entry with no File line renders '(state/logs/hooks.log)' unchanged [tree 1de8206e4eb2] (2026-10-30T11:21:23Z)
- (audit self) `self: read the diff; the innermost frame is the last File line in a Python traceback; a non-traceback entry (no File line) keeps the old '(state/logs/hooks.log)' form; the basename goes through c.plain like the message` → no findings [tree 1de8206e4eb2] (2026-10-30T11:21:23Z)
## Log
- 2026-10-30T06:31:04Z created
- 2026-10-30T06:31:09Z set type=FIX, tier=S
- 2026-10-30T11:19:05Z set tier=S
- 2026-10-30T11:19:05Z planned: it has criteria and steps
- 2026-10-30T11:20:39Z focused
- 2026-10-30T11:21:25Z done
- 2026-10-30T11:21:27Z committed 3f9afb6f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2109 [CLEAN S, done, 1 steps] CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit…
- T-0437 [FEATURE S, done, 1 steps] fm friction reports the errors hooks swallowed — lesson: An observer that swallows its own errors needs someone downstream counting the…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar finished tasks took 1–4 steps
- start here (files T-2109 touched): CHANGELOG.md, MASTER.md, plugin/lib/fmfriction.py
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
