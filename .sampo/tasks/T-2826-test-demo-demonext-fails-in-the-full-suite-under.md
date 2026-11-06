---
id: T-2826
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T17:55:58Z
updated: 2026-11-03T20:10:13Z
done_in: T-2822
---
# test_demo.DemoNext fails in the full suite under close-time load (3 of 3 runs during…
## Raw request
> FIX: test_demo.DemoNext fails in the full suite under close-time load (3 of 3 runs during T-2779's close, 2026-11-03, with a designer's headless Chrome running) but passes alone and in a full run at load 22. Suspects: the test's fm('demo') budget of 30 s x busy_factor (the 1-min load lags a burst), and demo.py _run's fixed 60 s child timeout, which isn't load_scaled. The close records only a summary line, so the failure text is lost: keep the failing test's traceback in the close's evidence
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-03T17:55:58Z created
- 2026-11-03T18:45:53Z same root cause as T-2822; closes with it
- 2026-11-03T20:10:13Z done in T-2822: same root cause, fixed by T-2822: sandboxes now skip the host load gate; the full suite at --load 30 and the ship's Python 3.12 run both passed
## Follow-ups captured
