---
id: T-0778
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:26:32Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
base: a0e801e127a599b037db41018952b6224635ab45
base_tree: 76c083da820df091428888a631b4184e2be03dab
verified: strong
---
# Phone push when the user is needed or the queue drains: the Stop hook asks for one PushNotification, once per ask or drain
## Raw request
> FEATURE: Push to the phone only when the user is needed or a long unattended run ends
> CONTEXT: T-0760, cluster attention (27 ideas). PushNotification is a model tool (skips itself when the user is at the terminal); fm notify only serves fm run. The drive's Stop-hook text decides when the model stops.
> DONE-WHEN: the Stop hook, when the queue drains after unattended work or the next item waits on the user's yes, tells the model to send one PushNotification with a one-line lead; not more than once per drain or ask; a test pins the text and the once-only rule.
## Interpretation
Foreman notifies only through a terminal sequence (OSC 777, fmhooks.py:187, desktop only) when a turn ends waiting for an answer or on an empty queue. PushNotification (a model tool) also reaches the phone over Remote Control and skips itself when the user is at the terminal. In full autonomy, when a turn ends with the queue drained after work or with a question for the user, the Stop hook blocks once and asks for one PushNotification leading with what the user would act on, then lets the turn end.
## Assumptions (confidence)
## Acceptance criteria
- [x] in full autonomy a Stop that ends on a question or a drained queue blocks once with a PushNotification request (under 200 chars lead), and the next Stop of the chain passes; standard autonomy and one-off headless sessions never get it — verify with `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed`
## Non-goals
## Approach (options → choice → why)
Options: a line in the rules (unreliable at the end of long runs); a hook that sends the push itself (hooks can't call model tools); one Stop block per ask/drain. Chose the block: one short extra turn, deduplicated by the tool when the user is present.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] _push_nudge in stop()
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed` → ✗ exit 1 · Ran 1 test in 4.095s / FAILED (failures=1) [ran] [tree 6f57eeab9f96] (2026-10-14T16:21:50Z)
- (step 2) `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 140 tests in 62.1s (20 classes, 16 at a time; slowest: Stop 62s, PreToolUse 28s, Approvals 25s) / OK [ran] [tree 65a1e26ce2a8] (2026-10-14T16:24:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed` → exit 0 · Ran 1 test in 1.803s / OK [ran] [tree 65a1e26ce2a8] (2026-10-14T16:24:33Z)
- `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed` → ✗ exit 1 · Ran 1 test in 1.654s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 65a1e26ce2a8] (2026-10-14T16:24:37Z)
- `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed` → exit 0 · Ran 1 test in 1.887s / OK [ran] [tree 65a1e26ce2a8] (2026-10-14T16:24:37Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_push_once_when_the_user_is_needed` → exit 0 · Ran 1 test in 0.800s / OK [ran] [tree 65a1e26ce2a8] (2026-10-14T16:26:31Z)
- (audit edge) `self: diff read; the nudge runs only in full autonomy, never in a one-off headless session or inside a stop chain, and only when nothing else holds the turn; one per open-ask set (keyed by ids) or per drain hour via the session's one-shot files; the request names the ask ids and asks for one line under 200 chars` → the existing full-autonomy test now sees one push request before the plain stop (updated deliberately); the user at the terminal gets nothing from the tool itself (PushNotification skips redundant pushes) [tree 65a1e26ce2a8] (2026-10-14T16:26:31Z)
- (audit self) `self: diff read; the nudge runs only in full autonomy, never in a one-off headless session or inside a stop chain, and only when nothing else holds the turn; one per open-ask set (keyed by ids) or per drain hour via the session's one-shot files; the request names the ask ids and asks for one line under 200 chars` → no findings [tree 65a1e26ce2a8] (2026-10-14T16:26:31Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:07:00Z planned from capture
- 2026-10-14T16:21:33Z focused
- 2026-10-14T16:26:32Z done
- 2026-10-14T16:26:32Z committed b215492 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- research brainstorm-20261014: 609 ideas from 11 lenses x 4 rounds + 3 deepen rounds, in 30 capability clusters. Every idea is listed under its cluster. Marks: build (rou…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- a model tool a hook wants called is reached through one bounded Stop block, keyed so it can't loop
## Plan gaps
- failed first: step 1 Failing hook test
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
