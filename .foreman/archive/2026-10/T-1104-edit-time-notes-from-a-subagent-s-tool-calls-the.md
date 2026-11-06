---
id: T-1104
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_batch_edit.py]
depends_on: []
source: self
created: 2026-10-16T05:02:25Z
updated: 2026-10-16T05:13:07Z
base: e3bf490447e45680f35ff1fe1f0e637ef3c7d3df
base_tree: b18c6d283660ca1cd67a30ef7e6f41d8e951a187
verified: strong
---
# Edit-time notes from a subagent's tool calls (the batch and thrash hints for a builder's f
## Raw request
> Edit-time notes from a subagent's tool calls (the batch and thrash hints for a builder's files) land in the main session's context, costing tokens and misleading it: key those notes to the agent (the hook payload's agent id) and keep them out of the main thread
## Interpretation
Edit-time hints raised by a subagent's own edits (the batch hint on a builder's 3rd edit of a file) show up in the main session's context: noise and tokens for the thread that didn't make the edit. The batch hint skips calls that carry an agent_id; the thrash note stays (it is rare and a stuck builder is worth knowing about).
## Assumptions (confidence)
## Acceptance criteria
- [x] a subagent's 3rd edit of a file gets no batch hint; the main thread's still does — verify with `python3 plugin/tests/run.py test_batch_edit`
## Non-goals
## Approach (options → choice → why)
Options: (a) route notes to the agent only (Claude Code decides delivery, not Foreman); (b) skip the batch hint for subagent calls (agent_id in the payload); (c) drop both hints for agents. Choice (b): the batch hint is the frequent one and the builder contract already tells builders about fm edit --file.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then skip the batch hint when the payload has an agent_id
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_batch_edit.Hint` → ✗ exit 1 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Hint 1s) / FAILED (1 classes) [ran] [tree 019ca02ea53e] (2026-10-16T05:12:16Z)
- (step 1) `python3 plugin/tests/run.py test_batch_edit test_speed` → exit 0 · Ran 31 tests in 17.1s (5 classes, 16 at a time; slowest: BatchEdit 17s, Speed 3s, Sub 2s) / OK [ran] [tree b271e2894557] (2026-10-16T05:12:39Z)
- (ac 1) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 22 tests in 19.1s (4 classes, 16 at a time; slowest: BatchEdit 19s, Sub 6s, Hint 3s) / OK [ran] [tree b271e2894557] (2026-10-16T05:12:59Z)
- (audit edge) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green` → a main-thread edit still gets the hint once; a subagent's never [tree b271e2894557] (2026-10-16T05:12:59Z)
- (audit operator) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green` → fewer stray notes in the main session while builders work [tree b271e2894557] (2026-10-16T05:12:59Z)
- (audit self) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green` → no findings [tree b271e2894557] (2026-10-16T05:12:59Z)
- `python3 plugin/tests/run.py test_batch_edit.Hint` → exit 0 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: Hint 1s) / OK [ran] [tree b271e2894557] (2026-10-16T05:13:05Z)
- (audit edge) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green on test_batch_edit.Hint` → a main-thread edit still gets the hint once; a subagent's never [tree b271e2894557] (2026-10-16T05:13:05Z)
- (audit operator) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green on test_batch_edit.Hint` → fewer stray notes in the main session while builders work [tree b271e2894557] (2026-10-16T05:13:05Z)
- (audit self) `self: one condition in the batch-hint branch; the thrash note unchanged; red then green on test_batch_edit.Hint` → no findings [tree b271e2894557] (2026-10-16T05:13:05Z)
## Log
- 2026-10-16T05:02:25Z created
- 2026-10-16T05:12:05Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_batch_edit.py']
- 2026-10-16T05:12:06Z focused
- 2026-10-16T05:13:06Z done
- 2026-10-16T05:13:07Z committed fe7d349 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: plugin/tests/test_hooks.py
## Plan gaps
- failed first: step 1 Failing test, then skip the batch hint when the payload has an agent_id
## Files touched
- plugin/tests/test_batch_edit.py
- plugin/lib/fmhooks.py
