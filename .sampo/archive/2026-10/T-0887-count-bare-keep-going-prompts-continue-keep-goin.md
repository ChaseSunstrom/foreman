---
id: T-0887
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:48:57Z
base: 8e02e1f27d1ad86f48a49629afb6d8272c3cadc8
base_tree: 2c25c6f6618ee1c64efbfc229f98f1ef1c8bb359
verified: strong
---
# Count bare keep-going prompts (continue, keep going, go on) as stalls, paired with the pre
## Raw request
> FEATURE: Count bare keep-going prompts (continue, keep going, go on) as stalls, paired with the previous Stop reason, in fm friction and the digest
> CONTEXT: round 5 #43. UserPromptSubmit logs corrections (_CORRECTION); a bare continue says Claude stopped too early
## Interpretation
A prompt that is only 'continue', 'keep going', 'go on', 'carry on', 'proceed', 'go ahead', 'resume' or 'don't stop' means Claude stopped before the user wanted: log it as a stall event with the session's last drive outcome (drive, drive_wait, drive_drained… or none), and fm friction lists the count and what preceded them so a pass can fix the stop
## Assumptions (confidence)
## Acceptance criteria
- [x] a bare keep-going prompt is a stall with its preceding stop, listed by fm friction; a longer prompt isn't — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_friction, then the hook regex + stall event and the friction section
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction test_hooks` → exit 0 · Ran 160 tests in 26.8s (22 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree fbbd69a9c97a] (2026-10-15T15:46:36Z)
- `python3 plugin/tests/run.py test_friction` → ✗ exit 1 · Ran 12 tests in 4.9s (2 classes, 16 at a time; slowest: Friction 5s, Mining 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fbbd69a9c97a] (2026-10-15T15:46:46Z)
- `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 12 tests in 4.6s (2 classes, 16 at a time; slowest: Friction 5s, Mining 0s) / OK [ran] [tree fbbd69a9c97a] (2026-10-15T15:46:46Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 12 tests in 4.7s (2 classes, 16 at a time; slowest: Friction 5s, Mining 0s) / OK [ran] [tree fbbd69a9c97a] (2026-10-15T15:48:56Z)
- (audit self) `self review: one anchored regex (a bare continue/keep going/go on/carry on/proceed/go ahead/resume/keep at it/don't stop, optional please); logged as a stall with the session's last drive event; friction groups them by what preceded; a correction match wins (elif)` → no findings [tree fbbd69a9c97a] (2026-10-15T15:48:56Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:30:03Z set tier=S
- 2026-10-15T15:45:13Z focused
- 2026-10-15T15:48:57Z done
- 2026-10-15T15:48:57Z committed 65e7f96 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- T-0117 [FEATURE S, done, 2 steps] While-you-were-away row: what drive finished since the user's last message
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
- similar finished tasks took 2–5 steps
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmhooks.py
- plugin/lib/fmfriction.py
