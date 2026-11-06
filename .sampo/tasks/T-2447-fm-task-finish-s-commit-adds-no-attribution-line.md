---
id: T-2447
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T04:08:29Z
updated: 2026-11-01T04:23:28Z
base: 126d4ec84291d24b9152cbd6889f936c64d6d861
base_tree: 162c45a04115a02eb1e6c44d58fe8c40323d5000
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-01T04:08:30Z
plan0_scope: []
verified: strong
---
# fm task finish's commit adds no attribution line: drop T-2443's Claude-Session trailer
## Raw request
> fm task finish's commit adds no attribution line: drop T-2443's Claude-Session trailer
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finish commit made with CLAUDE_CODE_BRIDGE_SESSION_ID set carries no Claude-Session line — verify with `python3 plugin/tests/run.py test_bookkeeping -k session_trailer`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] flip the test, then drop the trailer code
## Resume here
<!-- auto -->
- 2026-11-01T04:09:09Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_bookkeeping.py
- touched since last checkpoint: plugin/tests/test_bookkeeping.py, plugin/lib/fmcli.py
## Docs impact
none: removes T-2443's commit trailer; no doc named it
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / FAILED (1 classes: test_bookkeeping.SessionTrailer) [ran] [tree ab20a567699b] (2026-11-01T04:08:40Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: SessionTrailer 2s) / OK [ran] [tree a6f47af45d90] (2026-11-01T04:08:49Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: SessionTrailer 2s) / OK [ran] [tree a6f47af45d90] (2026-11-01T04:08:52Z)
- `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → ✗ exit 1 · Ran 1 tests in 2.7s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / FAILED (1 classes: test_bookkeeping.SessionTrailer) (start tree + this task's tests) [ran] [tree a6f47af45d90] (2026-11-01T04:08:57Z)
- `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / OK [ran] [tree a6f47af45d90] (2026-11-01T04:08:57Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / OK [ran] [tree 327f1951f40c] (2026-11-01T04:16:49Z)
- (audit intent) `self-review; the flipped test was red with the trailer code in place and green with it removed; full fm check green` → commits carry no attribution line now (the session's instruction replaced the earlier one); fm task finish no longer reads CLAUDE_CODE_BRIDGE_SESSION_ID [tree 327f1951f40c] (2026-11-01T04:16:49Z)
- (audit edge) `self-review; the flipped test was red with the trailer code in place and green with it removed; full fm check green` → a commit message that itself contains a trailer the user typed is left as written; helpers still drop the bridge id so tests stay hermetic [tree 327f1951f40c] (2026-11-01T04:16:49Z)
- (audit self) `self-review; the flipped test was red with the trailer code in place and green with it removed; full fm check green` → no findings [tree 327f1951f40c] (2026-11-01T04:16:49Z)
## Log
- 2026-11-01T04:08:29Z created
- 2026-11-01T04:08:29Z focused
- 2026-11-01T04:08:30Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-01T04:08:57Z scope: plugin/tests/test_bookkeeping.py's SessionTrailer flipped to pin no trailer
- 2026-11-01T04:09:21Z paused: focus moved to T-2446
- 2026-11-01T04:16:45Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-01T04:16:45Z focused
- 2026-11-01T04:17:25Z done
- 2026-11-01T04:17:28Z committed ad0b9576 (2 files)
- 2026-11-01T04:17:35Z guard authorization added: publish
- 2026-11-01T04:23:28Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2443 [FIX S, done, 1 steps] fm task finish's commit carries Claude-Session from CLAUDE_CODE_BRIDGE_SESSION_ID — lesson: fm task finish's commits skipped the session tr…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
## Why not caught
T-2443 followed the instruction in force then; the instruction changed
## Lessons
- Attribution lines follow the session's current instruction, which can change mid-run: never bake them into a verb
## Plan gaps
- failed first: step 1 flip the test, then drop the trailer code
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
