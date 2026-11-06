---
id: T-2168
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T14:34:46Z
updated: 2026-10-31T00:16:45Z
base: 0fb1d31baf6955ca1da2c71ed87917dae6a3acd1
base_tree: 52e600a5373e9501cb32f6b53ebcc29380d39053
plan0_at: 2026-10-31T00:16:33Z
plan0_scope: []
verified: ok
---
# Recurring obstacle: fm: refused: t-0 criterion 0 already has evidence, so its check…
## Raw request
> Recurring obstacle: fm: refused: t-0 criterion 0 already has evidence, so its check stays as it is (an edit c… (met 3 times, no known fix): remove its cause, or teach the fix with fm fix add
## Interpretation
The refusal (fmcore edit_ac, T-0342) is a deliberate policy: a criterion with evidence can't be edited, because an edit could weaken a failing check. It recurs because sessions try the edit anyway; its message names the way out. Teach that as a known fix (fm fix add) so the recurring-obstacle detector stops reporting it as unknown, instead of loosening the policy.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm fix list names the known fix for a criterion that already has evidence (add a criterion, or --redo) — verify with `fm fix list | grep -q 'already has evidence'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm fix add the obstacle with its fix
## Resume here
## Docs impact
none: no code or user-facing behavior changed; a known fix was recorded in state
## Verification evidence
- (step 1) `fm fix list | grep -q 'already has evidence'` → exit 0 · (no output) [ran] [tree 52e600a5373e] (2026-10-31T00:16:41Z)
- (ac 1) `fm fix list | grep -q 'already has evidence'` → exit 0 · (no output) [ran] [tree 52e600a5373e] (2026-10-31T00:16:41Z)
- (ac 1) `fm fix list | grep -q 'already has evidence'` → exit 0 · (no output) [ran] [tree 52e600a5373e] (2026-10-31T00:16:43Z)
- (audit self) `self: the policy (no edits to a criterion with evidence) is unchanged; only a known fix was taught, worded as the refusal's own way out` → no findings [tree 52e600a5373e] (2026-10-31T00:16:43Z)
## Log
- 2026-10-30T14:34:46Z created
- 2026-10-31T00:16:32Z set tier=S
- 2026-10-31T00:16:32Z planned: it has criteria and steps
- 2026-10-31T00:16:32Z focused
- 2026-10-31T00:16:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1769 [FIX S, done, 1 steps] A test runner's tally became the failure signature, so red-first runs read as a recurring obstacle
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-2192-review: Verdict: changes needed.** The Stop-hook change and the exam re-ask look sound. The user's stated goal is not met, and the re-ask trigger is weak…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- similar finished tasks took 1–6 steps
## Regression test
none: no code changed; the fix lives in Foreman's state (fm fix list), and its criterion greps for it
## Lessons
- A refusal that recurs while its message already names the way out is a known fix to record, not a rule to loosen
