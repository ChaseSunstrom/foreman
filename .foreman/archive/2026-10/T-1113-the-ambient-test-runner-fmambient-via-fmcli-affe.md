---
id: T-1113
type: FIX
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmambient.py, plugin/tests/test_check_paths.py]
depends_on: []
source: discovered
created: 2026-10-16T05:36:58Z
updated: 2026-10-16T05:41:37Z
base: e11b9e8cef1c5d49fd0211a913eceb01447c0981
base_tree: ff493ab8c27a4f8d57415adbe77ee7beb8314a69
---
# The ambient test runner (fmambient via fmcli.affected) runs other open tasks' red-first te
## Raw request
> The ambient test runner (fmambient via fmcli.affected) runs other open tasks' red-first test files and reports them as the active task's failures; pass the same red-first skip fm check uses (T-1101)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] With another task's red-first test file in the tree, the ambient runner leaves it out and reports no failure for the active task — verify with `python3 plugin/tests/run.py test_check_paths test_ambient`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then pass fm check's skip env in fmambient.run
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 11 tests in 6.9s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 2s) / OK [ran] [tree 17b3366224bf] (2026-10-16T05:40:44Z)
- (step 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 11 tests in 6.8s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 2s) / OK [ran] [tree 7871726cf89e] (2026-10-16T05:41:07Z)
## Log
- 2026-10-16T05:36:58Z created
- 2026-10-16T05:39:02Z set scope=['plugin/lib/fmambient.py', 'plugin/tests/test_check_paths.py']
- 2026-10-16T05:40:27Z focused
- 2026-10-16T05:41:37Z probe: A refocused after B wrote its red test; the ambient run selected only test_green (last.json) — the task base is re-snapshotted at focus, so B's file is never A's change. Rules out the premise; the earlier ambient noise was builder worktree edits (fixed in T-1110)
- 2026-10-16T05:41:37Z dropped: premise false: refocus re-snapshots the base, so another task's red file never reaches the ambient run; the observed noise was subagent edits, fixed by T-1110
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- decision 2026-10-15: T-0970 dropped as a duplicate of T-0705's ambient runner; ambient tests switched on in this repo; stays opt-in by default (CPU on the user's machine…
- likely tests for the scope: plugin/tests/test_ambient.py
