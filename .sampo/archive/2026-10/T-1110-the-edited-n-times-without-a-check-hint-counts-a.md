---
id: T-1110
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_batch_edit.py]
depends_on: []
source: discovered
created: 2026-10-16T05:17:44Z
updated: 2026-10-16T05:29:41Z
base: 454002ee23a72a623862fdfe210afe9f561f151f
base_tree: 85d5e279543b307a7acf2b97bc60376ffad4c414
verified: strong
---
# The 'edited N times without a check' hint counts a subagent's edits and lands in the main
## Raw request
> The 'edited N times without a check' hint counts a subagent's edits and lands in the main thread naming the builder's task (T-1101 here); skip payloads with agent_id as T-1104 did for the batch hint
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A subagent's repeated edits raise neither the batch hint nor the thrash note; the main thread's still do — verify with `python3 plugin/tests/run.py test_batch_edit test_speed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: 7 subagent edits of one file give no note
2. [x] Skip both notes for payloads with agent_id
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_batch_edit` → ✗ exit 1 · Ran 22 tests in 9.9s (4 classes, 16 at a time; slowest: BatchEdit 10s, Sub 4s, Hint 2s) / FAILED (1 classes) [ran] [tree 6a7b924667ae] (2026-10-16T05:27:45Z)
- (step 2) `python3 plugin/tests/run.py test_batch_edit test_speed` → exit 0 · Ran 31 tests in 9.0s (5 classes, 16 at a time; slowest: BatchEdit 9s, Speed 4s, Sub 3s) / OK [ran] [tree cd50f7f942ce] (2026-10-16T05:28:01Z)
- (step 2) `python3 plugin/tests/run.py test_batch_edit test_speed test_fixes test_recall test_ambient` → exit 0 · Ran 63 tests in 14.0s (12 classes, 16 at a time; slowest: Recall 14s, BatchEdit 7s, KnownFixes 5s) / OK [ran] [tree 1f6b89c2f810] (2026-10-16T05:29:18Z)
- (ac 1) `python3 plugin/tests/run.py test_batch_edit test_speed` → exit 0 · Ran 32 tests in 6.9s (5 classes, 16 at a time; slowest: BatchEdit 7s, Speed 2s, Sub 2s) / OK [ran] [tree f5d869d3ec23] (2026-10-16T05:29:39Z)
- (step 1) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 23 tests in 6.9s (4 classes, 16 at a time; slowest: BatchEdit 7s, Sub 2s, Hint 1s) / OK [ran] [tree f5d869d3ec23] (2026-10-16T05:29:39Z)
- (audit self) `self: subagent and main-thread payloads compared for the thrash note and the failure hook; ambient after_edit gated by the same agent_id test` → no findings [tree f5d869d3ec23] (2026-10-16T05:29:39Z)
## Log
- 2026-10-16T05:17:44Z created
- 2026-10-16T05:27:13Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_hooks_batch.py']
- 2026-10-16T05:27:29Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_batch_edit.py']
- 2026-10-16T05:27:30Z focused
- 2026-10-16T05:28:30Z steer (self): the same leak exists for a subagent's failed Bash (fixes/recall/suspects notes, and its failure recorded against this thread's task) and its edits starting ambient runs whose flips land here; widening to those two call sites in fmhooks
- 2026-10-16T05:29:25Z scope: CHANGELOG.md — release note
- 2026-10-16T05:29:40Z done
- 2026-10-16T05:29:41Z committed 84f827f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1104 [FIX S, done, 1 steps] Edit-time notes from a subagent's tool calls (the batch and thrash hints for a builder's f
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 1–4 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- Hook output for a subagent's tool call reaches the parent's context: every PostToolUse note needs the agent_id gate, not just the one that was noticed
## Plan gaps
- failed first: step 1 Failing test: 7 subagent edits of one file give no note
## Files touched
- plugin/tests/test_batch_edit.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
