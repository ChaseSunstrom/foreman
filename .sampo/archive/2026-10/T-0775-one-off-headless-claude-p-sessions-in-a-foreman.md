---
id: T-0775
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:01:29Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: headless child command budget and effort
base: 4aecea1df413a2029cc510b5ccb8c28445c997b7
base_tree: 9fbf7df9dd3f3f007b3ac68a2b68b13199490a6d
verified: strong
---
# One-off headless claude -p sessions answer their prompt and stop; they never drive the queue
## Raw request
> FIX!: One-off headless claude -p sessions in a Foreman project answer their prompt and stop; they never drive the queue
> CONTEXT: T-0760 catalogue, cluster headless-children. Incident 2026-10-14: an ad-hoc claude -p (haiku) got the Next/queue context and full-autonomy rules, focused T-0764 and edited plugin/lib/fmcli.py in the main checkout until its timeout. Only fm run's sessions (FOREMAN_DRIVE_TASK) are queue workers; fmhooks._headless() (fmhooks.py:1637) gates only some drive branches.
> DONE-WHEN: SessionStart/UserPromptSubmit/Stop in a headless session without FOREMAN_DRIVE_TASK inject no queue/Next drive text and never push queued work; fm run sessions unchanged.
## Interpretation
A claude -p session Foreman didn't start (no FOREMAN_DRIVE_TASK) got SessionStart's Next/queue context, claimed the project's session, was pushed by the Stop drive and evidence gate, and worked T-0764 in the main checkout. Such a session gets one short note instead (answer the prompt; don't work queued tasks unless asked), keeps the guard, and its Stop only keeps the background-work wait.
## Assumptions (confidence)
## Acceptance criteria
- [x] one-off headless SessionStart/UserPromptSubmit carry no Next/queue text and its Stop never blocks to drive; fm run (FOREMAN_DRIVE_TASK) still drives — verify with `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives`
## Non-goals
## Approach (options → choice → why)
Options: env opt-out the user must set; a one-off check in the three hooks; skip Foreman entirely for -p. Chose the check (_oneoff = sdk-cli without FOREMAN_DRIVE_TASK): fm run keeps driving, the guard keeps protecting, nothing to configure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] _oneoff() in session_start, user_prompt_submit, stop
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives` → ✗ exit 1 · Ran 1 test in 0.747s / FAILED (failures=1) [ran] [tree f795c4ddfc37] (2026-10-14T15:58:41Z)
- (step 2) `python3 plugin/tests/run.py -k test_hooks -k test_second` → exit 0 · Ran 154 tests in 25.3s (28 classes, 16 at a time; slowest: Stop 25s, PreToolUse 11s, Approvals 11s) / OK [ran] [tree 049246abcba9] (2026-10-14T15:59:27Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives` → exit 0 · Ran 1 test in 0.844s / OK [ran] [tree 049246abcba9] (2026-10-14T15:59:44Z)
- `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives` → ✗ exit 1 · Ran 1 test in 0.857s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 049246abcba9] (2026-10-14T15:59:46Z)
- `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives` → exit 0 · Ran 1 test in 0.851s / OK [ran] [tree 049246abcba9] (2026-10-14T15:59:46Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives` → exit 0 · Ran 1 test in 0.826s / OK [ran] [tree 049246abcba9] (2026-10-14T16:01:28Z)
- (audit edge) `self: diff read; _oneoff = sdk-cli without FOREMAN_DRIVE_TASK returns a one-line note from SessionStart and UserPromptSubmit before any state write, intake or background spawn; Stop keeps only the background-work wait; PreToolUse guard untouched` → fm run (FOREMAN_DRIVE_TASK) still drives (test); fm's own children use --setting-sources project,local so Foreman's hooks don't load there at all; a user's deliberate 'claude -p "work the queue"' is allowed by the note's 'unless the prompt asks' [tree 049246abcba9] (2026-10-14T16:01:28Z)
- (audit operator) `self: diff read; _oneoff = sdk-cli without FOREMAN_DRIVE_TASK returns a one-line note from SessionStart and UserPromptSubmit before any state write, intake or background spawn; Stop keeps only the background-work wait; PreToolUse guard untouched` → real claude -p in this project answered in 1 turn, 3 s, $0.004 with no ledger events [tree 049246abcba9] (2026-10-14T16:01:28Z)
- (audit self) `self: diff read; _oneoff = sdk-cli without FOREMAN_DRIVE_TASK returns a one-line note from SessionStart and UserPromptSubmit before any state write, intake or background spawn; Stop keeps only the background-work wait; PreToolUse guard untouched` → no findings [tree 049246abcba9] (2026-10-14T16:01:28Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T15:58:22Z planned from capture
- 2026-10-14T15:58:22Z focused
- 2026-10-14T15:58:32Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_hooks.Drive.test_a_oneoff_headless_session_never_drives` → `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_oneoff_headless_session_never_drives`
- 2026-10-14T15:59:47Z real path: claude -p 'What is 2+2?' (haiku) in this project answered '4' in 1 turn, 3 s, $0.004, wrote no ledger events and touched no files (the same kind of call before the fix focused T-0764 and edited fmcli.py)
- 2026-10-14T16:01:28Z done
- 2026-10-14T16:01:29Z committed cfeff71 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- a headless session Foreman didn't start must not inherit the drive: gate on who launched it (FOREMAN_DRIVE_TASK), not on headlessness alone
## Plan gaps
- failed first: step 1 Failing hook test
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
