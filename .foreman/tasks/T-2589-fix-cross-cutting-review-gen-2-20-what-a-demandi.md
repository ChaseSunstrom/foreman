---
id: T-2589
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:32Z
updated: 2026-11-02T10:07:26Z
trigger: genesis-review
trigger_key: 9959dd78d5f655a2
base: 45cecd25c5f02b197aef927cdfb3e672bc5c0d75
base_tree: 0e2fb3bd69d53f35308f0d9e07b47d4e4d8630ab
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T09:54:30Z
plan0_scope: []
verified: strong
---
# The session-start note fits one 1,500-character budget, appended mandate, goal and leads included, and friction checks it against that same constant
## Raw request
> FIX: cross-cutting review gen-2 #20 (what a demanding user would complain about first): Every session opens with a note over the project's own 1,500-character trim rule (T-2109) and the friction report has flagged it again. [SessionStart: foreman project foreman- a f — 1×, 1,985 chars]
> genesis-review 2:20
## Interpretation
Reading 1 (chosen): the note must fit the project's own trim rule; today the budget (2000) and the rule (1500) disagree and appended parts escape the budget. Reading 2: friction's rule is wrong for a once-per-session note. Rejected: the review names it as the first thing a demanding user sees.
## Assumptions (confidence)
## Acceptance criteria
- [x] SessionStart additionalContext is at most CTX_BUDGET (1500) characters with a long mandate, a goal and leads all present: session_context gets the budget left after the appended parts, which are themselves capped; fmfriction's per-injection trim line uses fmhooks.CTX_BUDGET for SessionStart — verify with `python3 plugin/tests/run.py test_hooks test_friction`
## Non-goals
## Approach (options → choice → why)
1) One budget for the whole note: compute the appended parts (mandate, goal, leads, unattended line) first, cap each, and pass session_context the remainder of CTX_BUDGET=1500; friction's trim line reads CTX_BUDGET for SessionStart. Likely outcome: every session start fits 1,500. Fails if: a part the session needs gets cut (session_context already drops lowest-priority lines first; the mandate is capped, never dropped). 2) use what exists: set friction's threshold to 2000 for SessionStart to match the old budget. Fails if: the user-facing complaint (a long opening note) stays. 3) do less: trim the Map line only. Fails if: the appended parts still push past any budget. Choice 1 (80%): the budget and the rule become one number, and the appended parts stop escaping it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a session start with a 400-char mandate, a goal and leads stays within 1500
2. [x] budget the appended parts in session_start; CTX_BUDGET 1500; friction reads it
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG (Unreleased); CTX_BUDGET's comment names the rule; no README change.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.SessionStart test_friction` → ✗ exit 1 · Ran 41 tests in 17.3s (6 classes, 16 at a time; slowest: SessionStart 17s, Friction 6s, UserPromptSubmit 1s) / FAILED (2 classes: test_hooks.SessionStart, test_friction.Friction) [ran] [tree 159a455ecdcc] [world 2f1906870a] (2026-11-02T09:55:13Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_friction test_doctor` → exit 0 · Ran 374 tests in 46.3s (71 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 28s, PreToolUse 25s) / OK [ran] [tree f9db0fae35cc] [world 2f1906870a] (2026-11-02T09:58:38Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_friction test_doctor` → exit 0 · Ran 374 tests in 45.2s (71 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 27s, PreToolUse 23s) / OK [ran] [tree f9db0fae35cc] [world 2f1906870a] (2026-11-02T09:59:23Z)
- `python3 plugin/tests/run.py test_hooks.SessionStart test_friction` → ✗ exit 1 · Ran 41 tests in 18.3s (6 classes, 16 at a time; slowest: SessionStart 17s, Friction 6s, UserPromptSubmit 1s) / FAILED (2 classes: test_hooks.SessionStart, test_friction.Friction) (start tree + this task's tests) [ran] [tree fd598e463561] [world 2f1906870a] (2026-11-02T10:05:34Z)
- `python3 plugin/tests/run.py test_hooks.SessionStart test_friction` → exit 0 · Ran 41 tests in 17.2s (6 classes, 16 at a time; slowest: SessionStart 17s, Friction 6s, UserPromptSubmit 1s) / OK [ran] [tree fd598e463561] [world 2f1906870a] (2026-11-02T10:05:34Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_friction` → exit 0 · Ran 268 tests in 44.8s (36 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree fd598e463561] [world 2f1906870a] (2026-11-02T10:06:20Z)
- (audit intent) `self-review: session_start builds the tail (unattended line, leads, goal or mandate) first and passes session_context the budget left (floor 600); CTX_BUDGET 1500 in fmhooks and fmdoctor (a test pins them equal); the repo note and compact recap stay after it and are logged as addon chars that friction subtracts; leads stay whole for the Stop hook's lead accounting` → a long queue plus a 500-char mandate fits 1500 and keeps the mandate (test); a 9000-char injection with an 8000-char addon isn't flagged (test) [tree fd598e463561] (2026-11-02T10:06:20Z)
- (audit edge) `self-review: session_start builds the tail (unattended line, leads, goal or mandate) first and passes session_context the budget left (floor 600); CTX_BUDGET 1500 in fmhooks and fmdoctor (a test pins them equal); the repo note and compact recap stay after it and are logged as addon chars that friction subtracts; leads stay whole for the Stop hook's lead accounting` → the state note's 600-char floor means a very long leads note could still pass 1500; leads appear only when nothing is queued, so the state note is short then; the headless layout branch is fitted to the same budget [tree fd598e463561] (2026-11-02T10:06:20Z)
- (audit maintainer) `self-review: session_start builds the tail (unattended line, leads, goal or mandate) first and passes session_context the budget left (floor 600); CTX_BUDGET 1500 in fmhooks and fmdoctor (a test pins them equal); the repo note and compact recap stay after it and are logged as addon chars that friction subtracts; leads stay whole for the Stop hook's lead accounting` → one constant, one place the tail is built; _ADDONS is popped by the logger so a stale count never carries to another event [tree fd598e463561] (2026-11-02T10:06:20Z)
## Log
- 2026-11-02T08:23:32Z created
- 2026-11-02T09:07:22Z planned from capture
- 2026-11-02T09:07:23Z set approved=True
- 2026-11-02T09:54:30Z focused
- 2026-11-02T09:54:30Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T09:59:24Z scope: plugin/lib/fmdoctor.py, plugin/lib/fmfriction.py and test_friction — doctor's copy of the budget and friction's subtraction of add-ons
- 2026-11-02T10:07:23Z done
- 2026-11-02T10:07:26Z committed d09e1e30 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2591 [FIX M, planned, 3 steps] CHANGELOG's Unreleased section opens with a short Highlights list of user-facing changes; the rest sits under Everything else; numbers c…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Why not caught
the budget test filled only the queue, and the budget (2000) and the friction rule (1500) lived in different modules with no test tying them
## Lessons
- A size budget and the rule that audits it must be one constant, and every part appended to the note must be counted before the budgeted part is cut
## Plan gaps
- failed first: step 1 red test: a session start with a 400-char mandate, a goal and leads stays within 1500
## Files touched
- plugin/tests/test_friction.py
- plugin/tests/test_hooks.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmfriction.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
