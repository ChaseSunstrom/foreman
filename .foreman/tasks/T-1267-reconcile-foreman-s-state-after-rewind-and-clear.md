---
id: T-1267
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/tests/test_rewind.py, plugin/tests/test_doctor.py, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:29Z
updated: 2026-10-23T13:16:57Z
base: 24748396cce25d5fa5e5a3136071a4298e288a6f
base_tree: e3f218fd208697f22ff95f31336967d241dd2f9c
plan0_at: 2026-10-23T13:10:20Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/tests/test_rewind.py, plugin/tests/test_doctor.py, CHANGELOG.md, README.md]
verified: strong
---
# Reconcile Foreman's state after /rewind and /clear; flag CLAUDE.md or memory rules that co
## Raw request
> Reconcile Foreman's state after /rewind and /clear; flag CLAUDE.md or memory rules that contradict Foreman's (brainstorm-20261020 C16)
## Interpretation
(1) A /rewind (or a revert, or a checkout) takes back files, but Foreman's ticks and proofs stay: a stale 'step 3 done' would be trusted, worst in long unattended sessions. Claude Code raises no rewind event (2.1.309 mod API and hooks), so detect it from the files: the working tree is back to one recorded before a done step's newest proof (the task's start tree, or an earlier run's tree) and isn't that proof's own tree. Such steps reopen, their proofs are marked rewound (kept, never counted) and fm next queues them again. Checked at session start, on each prompt (the tree id takes about 7 ms here) and in fm state. (2) Lines in CLAUDE.md, CLAUDE.local.md, rules or Claude Code's memory that contradict Foreman's rules (never run tests, no tests, commit every change, never commit, skip planning) cost turns unseen: fm doctor names each with file:line and a one-line resolution.
## Assumptions (confidence)
## Acceptance criteria
- [x] after two ticked steps, files taken back to before step 1 reopen both at the next session (note says so; proofs marked rewound; fm next asks for step 1 again); back to between them reopens step 2 only; later work moving on reopens nothing — verify with `python3 plugin/tests/run.py test_rewind`
- [x] fm doctor on a repo whose CLAUDE.md says never run the tests prints that file:line with Foreman's rule and a one-line resolution; Foreman's own block and other lines are left alone — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Complete version: detection without a rewind event, the reopen with the reason logged, the note where the model reads it (session start and prompt), fm state, and the doctor's conflict list over the user's and the project's instruction files and memory. Options for detection: (a) the tree match above - chosen: data Foreman already keeps (base_tree, [tree] marks), no false alarm when later work just moves on; (b) read the transcript for a rewound branch - Claude Code's private format, and a revert outside Claude isn't seen; (c) a mod event - none exists. For the reopen: untick only (fm next skips steps with evidence, so nothing re-queues) vs mark the proofs rewound like inconclusive runs (chosen). For conflicts: a small table of patterns with Foreman's rule and a fix (chosen) vs a model judging the files (paid, slow, unrepeatable).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: rewind reconcile, doctor conflicts
2. [x] rewound() and the reopen in fmcore, wired into SessionStart, UserPromptSubmit and fm state; the doctor check; CHANGELOG and README
## Resume here
## Docs impact
README.md (Never loses its place: a /rewind or revert reopens a step; Health check: fm doctor names contradicting rules), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rewind test_doctor` → ✗ exit 1 · Ran 70 tests in 3.3s (24 classes, 16 at a time; slowest: Rewind 3s, Command 2s, ViewsRepair 2s) / FAILED (2 classes) [ran] [tree fc63a0455cae] (2026-10-23T13:12:04Z)
- (step 1) `python3 plugin/tests/run.py test_rewind test_doctor` → exit 0 · Ran 70 tests in 3.9s (24 classes, 16 at a time; slowest: Rewind 4s, Command 2s, ViewsRepair 2s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:14:24Z)
- (step 2) `python3 plugin/tests/run.py test_rewind test_doctor test_hooks test_session test_session_fixes test_cli test_core` → exit 0 · Ran 489 tests in 47.7s (113 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 35s, TaskLifecycle 30s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:15:13Z)
- (ac 1) `python3 plugin/tests/run.py test_rewind` → exit 0 · Ran 4 tests in 3.6s (1 classes, 16 at a time; slowest: Rewind 3s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:15:17Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 66 tests in 2.0s (23 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, RuleConflicts 1s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:15:19Z)
- (ac 1) `python3 plugin/tests/run.py test_rewind` → exit 0 · Ran 4 tests in 3.7s (1 classes, 16 at a time; slowest: Rewind 4s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:16:01Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 66 tests in 1.9s (23 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, RuleConflicts 1s) / OK [ran] [tree ed41e87f1571] (2026-10-23T13:16:01Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): rewound() orders by the evidence section's position (append-only), not seconds, after a same-second tie hid the between-steps case; it reopens a step only when the files match a tree from before its proof, not its own, and no run since was recorded on them, so later work that moves on or undoes a step with its own proof reopens nothing (tested); the reopen keeps the proofs, marked like inconclusive runs, and fm's typed text can't carry the mark; the doctor patterns want the whole clause, so 'don't commit secrets' and 'don't run tests in parallel' pass (tested), and the real machine's files pass; UserPromptSubmit p95 stays under its 150 ms budget (102 ms in the bench)` → a stale tick after /rewind is reopened before anyone trusts it, and a CLAUDE.md or memory rule that fights Foreman's is named with a fix [tree ed41e87f1571] (2026-10-23T13:16:01Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): rewound() orders by the evidence section's position (append-only), not seconds, after a same-second tie hid the between-steps case; it reopens a step only when the files match a tree from before its proof, not its own, and no run since was recorded on them, so later work that moves on or undoes a step with its own proof reopens nothing (tested); the reopen keeps the proofs, marked like inconclusive runs, and fm's typed text can't carry the mark; the doctor patterns want the whole clause, so 'don't commit secrets' and 'don't run tests in parallel' pass (tested), and the real machine's files pass; UserPromptSubmit p95 stays under its 150 ms budget (102 ms in the bench)` → proofs in the same second, a task with no start tree (nothing checked), a step proved on its start tree (its own tree: kept), a second session (flagged once), fm state --json (no note printed), a 1 s cap on the tree in hooks; Foreman's own block, fences and lines naming fm or Foreman are skipped by the doctor [tree ed41e87f1571] (2026-10-23T13:16:01Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): rewound() orders by the evidence section's position (append-only), not seconds, after a same-second tie hid the between-steps case; it reopens a step only when the files match a tree from before its proof, not its own, and no run since was recorded on them, so later work that moves on or undoes a step with its own proof reopens nothing (tested); the reopen keeps the proofs, marked like inconclusive runs, and fm's typed text can't carry the mark; the doctor patterns want the whole clause, so 'don't commit secrets' and 'don't run tests in parallel' pass (tested), and the real machine's files pass; UserPromptSubmit p95 stays under its 150 ms budget (102 ms in the bench)` → the rewound mark only lowers trust (a forged one would only reopen a step) and typed evidence can't carry it; nothing here grants, runs or skips a check [tree ed41e87f1571] (2026-10-23T13:16:01Z)
## Log
- 2026-10-20T14:01:29Z created
- 2026-10-23T13:10:17Z set tier=M, scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_rewind.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md', 'README.md']
- 2026-10-23T13:10:20Z focused
- 2026-10-23T13:16:55Z done
- 2026-10-23T13:16:57Z committed 2f33d6a4 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Lessons
- Second-resolution timestamps can't order fast events: an append-only section's line order can
## Plan gaps
- failed first: step 1 red tests: rewind reconcile, doctor conflicts
## Files touched
- plugin/tests/test_rewind.py
- plugin/tests/test_doctor.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- README.md
