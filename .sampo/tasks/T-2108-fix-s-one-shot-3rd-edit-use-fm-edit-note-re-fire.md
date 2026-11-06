---
id: T-2108
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T06:31:05Z
updated: 2026-10-30T11:23:52Z
base: 3f9afb6f15c3bc10e1b5352c1fcdb93f256e8fbb
base_tree: 1de8206e4eb257087e9e8b6572b59fcdd8231f8e
plan0_at: 2026-10-30T11:22:43Z
plan0_scope: []
verified: strong
---
# FIX S: one-shot '3rd edit, use fm edit' note re-fires after every compaction:…
## Raw request
> FIX S: one-shot '3rd edit, use fm edit' note re-fires after every compaction: fmhooks.py:1474 _first_time(sid,'batch-'+key) is cleared by session_start (fmhooks.py:331); use a keep. key plus a one-line second form like _gate_pipe_note (fmhooks.py:2145); check thrash/card/gen markers too
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after the full note once, a later file's or a compacted session's 3rd-edit note is one line — verify with `python3 plugin/tests/run.py test_hooks.BatchNoteOnce`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] keep.batch decides full vs one-line form
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.BatchNoteOnce` → red as expected (exit 1) · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: BatchNoteOnce 0s) / FAILED (1 classes) [ran] [tree 43dbc8cc46ca] (2026-10-30T11:22:44Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.BatchNoteOnce test_speed test_batch_edit` → exit 0 · Ran 37 tests in 7.8s (6 classes, 16 at a time; slowest: BatchEdit 8s, Speed 2s, Sub 2s) / OK [ran] [tree 4707139cabf3] (2026-10-30T11:23:01Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.BatchNoteOnce` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: BatchNoteOnce 1s) / OK [ran] [tree d2de22394a2e] (2026-10-30T11:23:15Z)
- (audit edge) `self: read the diff; the per-file batch- marker still gates once per file per context, keep.batch survives session_start's sweep (sid.keep. prefix), no session id still means no note` → a compacted session's next file gets the one-line form; another session still hears it in full (test) [tree d2de22394a2e] (2026-10-30T11:23:15Z)
- (audit self) `self: read the diff; the per-file batch- marker still gates once per file per context, keep.batch survives session_start's sweep (sid.keep. prefix), no session id still means no note` → no findings [tree d2de22394a2e] (2026-10-30T11:23:15Z)
## Log
- 2026-10-30T06:31:05Z created
- 2026-10-30T06:31:09Z set type=FIX, tier=S
- 2026-10-30T11:22:42Z planned: it has criteria and steps
- 2026-10-30T11:22:42Z focused
- 2026-10-30T11:23:13Z checked: thrash (situational, counts since the last check) and card (its text is gone after a compaction) re-arm on purpose; gen is one short line per file, kept re-arming
- 2026-10-30T11:23:51Z done
- 2026-10-30T11:23:52Z committed b74a315e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1889 [FIX S, done, 3 steps] The fm check is piped note is given in full once per session — lesson: Record red and green with the same test command (or use fm task prov…
- T-1104 [FIX S, done, 1 steps] Edit-time notes from a subagent's tool calls (the batch and thrash hints for a builder's f
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: Genesis select: gen N's bar is gen N-1's exam line even when gen N-1's text was reverted
- similar finished tasks took 1–5 steps
- start here (files T-1889 touched): plugin/tests/test_hooks.py, CHANGELOG.md, plugin/lib/fmhooks.py
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
