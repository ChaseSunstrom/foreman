---
id: T-3389
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:34Z
updated: 2026-11-06T09:55:09Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aa1439dafb598cd7c
lane_branch: worktree-agent-aa1439dafb598cd7c
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T09:34:00Z
plan0_scope: []
builder_returned: 2026-11-06T09:55:09Z
---
# Session liveness ('seen') refreshes only on prompts, so a holder doing 15+ min of…
## Raw request
> FIX: session liveness ('seen') refreshes only on prompts, so a holder doing 15+ min of autonomous work looks dead to the second-session lane gate and the 'another session' note; refresh it from PostToolUse cheaply (T-3331 builder)
## Interpretation
Reading 1: a tool call refreshes the owning session's meta session.seen, throttled to 60 s, no lock wait. Reading 2: a new per-session heartbeat file; ruled out because readers (focus note, lane gate) read meta session.seen.
## Assumptions (confidence)
## Acceptance criteria
- [ ] PostToolUse refreshes seen after 60 s, not within — verify with `python3 -m unittest plugin.tests.test_hooks.PostToolUse`
## Non-goals
Multi-session liveness table; changing readers.
## Approach (options → choice → why)
1) in-hook unlocked read, then lock(timeout=0) write at most each 60 s; likely outcome: one cheap read per call. 2) use what exists: reuse update_meta/write_meta, but its lock waits 5 s; fails if the lock is busy under load. 3) do less: leave as is; fails if a long autonomous run looks dead. Choice 1 (80%): smallest, no reader change, no lock wait.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then _touch_seen in post_tool_use
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest plugin.tests.test_hooks.PostToolUse plugin.tests.test_hooks.BatchNoteOnce` → ✗ exit 1 (never ran: the test module test_hooks couldn't import) · Ran 2 tests in 0.000s / FAILED (errors=2) [ran] [tree 426f1e097e57] [world 2f1906870a] (2026-11-06T09:34:28Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -k PostToolUse` → exit 0 · Ran 5 tests in 4.065s / OK [ran] [tree 426f1e097e57] [world 2f1906870a] (2026-11-06T09:34:38Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.41s] [ran] [tree 426f1e097e57] [world 2f1906870a] (2026-11-06T09:43:30Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -k PostToolUse` → exit 0 · Ran 6 tests in 1.983s / OK [ran] [tree 54726a2ccf5c] [world 2f1906870a] (2026-11-06T09:48:05Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 633 tests in 151.8s (373 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 9s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 54726a2ccf5c] [world 2f1906870a] (2026-11-06T09:50:47Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 262 tests in 137.2s (222 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 7s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree ab31cc0d2ec8] [world 2f1906870a] (2026-11-06T09:54:57Z)
## Log
- 2026-11-06T06:54:34Z created
- 2026-11-06T09:33:31Z planned: it has criteria and steps
- 2026-11-06T09:33:57Z focused
- 2026-11-06T09:34:00Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3283 [FIX S, done, 2 steps] A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease take) —…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-3129 [FIX M, planned, 5 steps] Batch: The drive offers tasks to plan and clos…; Fm-builder prompt: builders keep hittin…; An unknown verb (fm models, …
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
- similar finished tasks took 2–3 steps
