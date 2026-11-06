---
id: T-0759
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: self
created: 2026-10-14T15:33:32Z
updated: 2026-10-14T19:42:10Z
explore: true
confirm: true
group: same bug feedback thread
base: 99f4dc711b810f32d1cbb18fc3d7d1879e54189d
base_tree: 94f797b544075b708e30f6f7222ff035cc77ac3d
verified: strong
---
# The step pointer follows the work: an edit that names a later step moves it, and a long run of edits on one step asks once
## Raw request
> "also I noticed that it will start working on different steps without updating the step in the UI"
> (fm second session: "also I noticed that it will start working on different steps without updating the step in the UI" — a step-progress UI sync bug; no open item covers it and later messages do not confirm it was fixed.)
## Interpretation
The user saw Claude work on later steps while the band still showed an earlier one: steps move only on fm task step / evidence (fmcore track_step). The PreToolUse hook already adds edit-time notes (fmhooks.py:878). It moves the current step forward when an edited file's name appears in exactly one later step and not the current one, and after 8 edits on a step with no evidence it says once which step is current and how to move it.
## Assumptions (confidence)
## Acceptance criteria
- [x] an Edit of a file named only in step 3 moves the current step from 1 to 3 and says so; 8 edits with no evidence on a step add one note naming fm task step ID current N — verify with `python3 plugin/tests/run.py test_hooks.PreToolUse`
## Non-goals
## Approach (options → choice → why)
Options: mirror steps into the native task list (TaskCreate isn't available in every session); block edits that look like a later step (false blocks); infer and nudge in the existing PreToolUse note. Chose infer + one nudge: no block, no new hook.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] _step_note in the PreToolUse notes
## Resume here
## Docs impact
none: hook note wording is self-describing
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.PreToolUse` → ✗ exit 1 · Ran 22 tests in 15.7s (1 classes, 16 at a time; slowest: PreToolUse 15s) / FAILED (1 classes) [ran] [tree dfbfa6939708] (2026-10-14T19:34:50Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.PreToolUse` → ✗ exit 1 · Ran 22 tests in 12.4s (1 classes, 16 at a time; slowest: PreToolUse 12s) / FAILED (1 classes) [ran] [tree bc51721a50f9] (2026-10-14T19:35:13Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 22 tests in 12.7s (1 classes, 16 at a time; slowest: PreToolUse 13s) / OK [ran] [tree 184f3fd301aa] (2026-10-14T19:35:43Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 23 tests in 12.8s (1 classes, 16 at a time; slowest: PreToolUse 13s) / OK [ran] [tree aa97f7e4c98e] (2026-10-14T19:39:38Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 23 tests in 12.7s (1 classes, 16 at a time; slowest: PreToolUse 13s) / OK [ran] [tree aa97f7e4c98e] (2026-10-14T19:39:51Z)
- `python3 plugin/tests/run.py test_hooks.PreToolUse` → ✗ exit 1 · Ran 23 tests in 12.7s (1 classes, 16 at a time; slowest: PreToolUse 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree aa97f7e4c98e] (2026-10-14T19:40:16Z)
- `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 23 tests in 12.7s (1 classes, 16 at a time; slowest: PreToolUse 13s) / OK [ran] [tree aa97f7e4c98e] (2026-10-14T19:40:16Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.4    38.2     150  [0] / SessionEnd                  30.9    32.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree aa97f7e4c98e] (2026-10-14T19:41:49Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 23 tests in 12.8s (1 classes, 16 at a time; slowest: PreToolUse 13s) / OK [ran] [tree aa97f7e4c98e] (2026-10-14T19:42:09Z)
- (audit intent) `main thread reviewed the builder's 49-line diff and fixed four things: file names match on word edges (a.py no longer matches data.py; src/billing.py still names billing.py), the move takes the quick hook lock and a busy lock skips only the move, step text in the note is bounded, one long line wrapped; background security review's three flags checked: moving the pointer marks nothing done and finish still needs evidence for every step, so it grants nothing` → the user saw work on later steps while the band showed an earlier one; an edit to a file named only in a later step now moves the pointer and says so, and the 8th evidence-less edit on a step says once how to move it [tree aa97f7e4c98e] (2026-10-14T19:42:09Z)
- (audit edge) `main thread reviewed the builder's 49-line diff and fixed four things: file names match on word edges (a.py no longer matches data.py; src/billing.py still names billing.py), the move takes the quick hook lock and a busy lock skips only the move, step text in the note is bounded, one long line wrapped; background security review's three flags checked: moving the pointer marks nothing done and finish still needs evidence for every step, so it grants nothing` → a name in two open steps moves nothing; backwards moves never happen; the 8-edit count reads the last 400 ledger events, so a flood of other events can undercount (no harm, just no nudge) [tree aa97f7e4c98e] (2026-10-14T19:42:09Z)
- (audit self) `main thread reviewed the builder's 49-line diff and fixed four things: file names match on word edges (a.py no longer matches data.py; src/billing.py still names billing.py), the move takes the quick hook lock and a busy lock skips only the move, step text in the note is bounded, one long line wrapped; background security review's three flags checked: moving the pointer marks nothing done and finish still needs evidence for every step, so it grants nothing` → no findings [tree aa97f7e4c98e] (2026-10-14T19:42:09Z)
## Log
- 2026-10-14T15:33:32Z created
- 2026-10-14T16:03:45Z planned from capture
- 2026-10-14T16:09:32Z set approved=True
- 2026-10-14T16:09:34Z set approved=True
- 2026-10-14T16:21:17Z set approved=True
- 2026-10-14T16:21:17Z approved: the user said 'i approve the plan' (2026-10-14) for the round-1 slate, whose recorded decision names T-0759
- 2026-10-14T18:45:43Z blocked: needs the user's own yes: a child session mined this request from another session's transcript (confirm category), asked at the end of the run
- 2026-10-14T19:33:29Z user approved confirm in Claude Code's permission prompt
- 2026-10-14T19:33:43Z set status=planned
- 2026-10-14T19:34:06Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_hooks.PreToolUse.test_step_pointer_follows_the_edits` → `python3 plugin/tests/run.py test_hooks.PreToolUse`
- 2026-10-14T19:34:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0759.builder.md
- 2026-10-14T19:34:11Z focused
- 2026-10-14T19:37:30Z merged worktree-agent-ab8a0f4ba73d24cab (2 file(s))
- 2026-10-14T19:37:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab8a0f4ba73d24cab
- 2026-10-14T19:37:30Z focused
- 2026-10-14T19:42:10Z done
- 2026-10-14T19:42:10Z committed 3ea18f4 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
- start here (files T-0781 touched): plugin/tests/test_hooks.py, plugin/lib/fmhooks.py
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-14): plugin/lib/fmhooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Why not caught
none: a UX report from the user (mined from another session), not a regression
## Lessons
- A name match against free text needs word edges on both sides, and a path separator counts as an edge
## Plan gaps
- failed first: step 1 Failing hook test
- failed first: step 2 _step_note in the PreToolUse notes
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
