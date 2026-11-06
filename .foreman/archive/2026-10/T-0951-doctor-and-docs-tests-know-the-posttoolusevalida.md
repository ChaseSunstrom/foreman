---
id: T-0951
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:04:50Z
updated: 2026-10-15T21:07:01Z
base: 87c9f485b09f7940a95ac0cf3586dc8a64ff9797
base_tree: 5979ebdd4f3b49036a750efeff0fa47814e1fbbd
verified: strong
---
# Doctor and docs tests know the PostToolUseValidate handler (T-0947 follow-up)
## Raw request
> Doctor and docs tests know the PostToolUseValidate handler (T-0947 follow-up)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor's hook-events check and the hooks.json docs test accept a handler named in an entry's args — verify with `python3 plugin/tests/run.py test_docs test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Count args handlers as registered; allow event+Validate args
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 66 tests in 20.9s (23 classes, 16 at a time; slowest: Command 21s, ViewsRepair 14s, TaskLifecycle 1s) / OK [ran] [tree b5a7ea781065] (2026-10-15T21:05:19Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 66 tests in 20.8s (23 classes, 16 at a time; slowest: Command 21s, ViewsRepair 14s, TaskLifecycle 1s) / OK [ran] [tree b5a7ea781065] (2026-10-15T21:05:41Z)
- `python3 plugin/tests/run.py test_docs test_doctor` → ✗ exit 1 · Ran 66 tests in 21.9s (23 classes, 16 at a time; slowest: Command 22s, ViewsRepair 15s, TaskLifecycle 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b5a7ea781065] (2026-10-15T21:06:26Z)
- `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 66 tests in 23.6s (23 classes, 16 at a time; slowest: Command 24s, ViewsRepair 14s, TaskLifecycle 1s) / OK [ran] [tree b5a7ea781065] (2026-10-15T21:06:26Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 66 tests in 27.1s (23 classes, 16 at a time; slowest: Command 27s, ViewsRepair 20s, TaskLifecycle 2s) / OK [ran] [tree b5a7ea781065] (2026-10-15T21:06:59Z)
- (audit intent) `main-thread: two-line fixes, tests prove red then green` → ok: doctor and docs tests accept an entry's own handler name [tree b5a7ea781065] (2026-10-15T21:06:59Z)
- (audit edge) `main-thread: two-line fixes, tests prove red then green` → ok: entries without args are ignored [tree b5a7ea781065] (2026-10-15T21:06:59Z)
- (audit self) `main-thread: two-line fixes, tests prove red then green` → no findings [tree b5a7ea781065] (2026-10-15T21:06:59Z)
## Log
- 2026-10-15T21:04:50Z created
- 2026-10-15T21:04:50Z focused
- 2026-10-15T21:07:00Z done
- 2026-10-15T21:07:01Z committed be49e40 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0872 [FEATURE S, done, 1 steps] Newcomer docs: INSTALL.md an agent can follow (explain defaults, ask consent, install, fm doctor), README links it and gains 'When not …
- research claude-code-features-20261014: Foreman uses: 14 hook events, 4 async hooks, 6 agents (tools/model/color only), output style, statusline.
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar finished tasks took 1–3 steps
## Why not caught
the T-0947 close ran only its affected tests; the wiring tests live in test_docs and test_doctor — fm check affected now covers lanes, and the full gates run before release
## Lessons
- When a hook entry names its own handler in args, the doctor's registration check must read args too, not only event keys.
## Files touched
- plugin/lib/fmdoctor.py
- plugin/tests/test_docs.py
