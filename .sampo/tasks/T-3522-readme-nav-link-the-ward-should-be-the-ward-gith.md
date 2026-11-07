---
id: T-3522
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:11:50Z
updated: 2026-11-06T19:18:47Z
lane: ~/.claude/foreman.lanes/T-3522
lane_branch: foreman/T-3522
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:13:30Z
plan0_scope: []
---
# README nav link #the-Ward should be #the-ward (GitHub anchors are lower case), and…
## Raw request
> FIX: README nav link #the-Ward should be #the-ward (GitHub anchors are lower case), and pages.yml still redeploys when demo/live.mp4 or demo.svg change though the landing page no longer shows the video
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] README's nav links match GitHub's lower-case anchors and pages.yml no longer triggers on demo/live.mp4 or demo.svg — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix anchors and the pages trigger, with a test for anchor case
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_docs` → exit 0 · Ran 116 tests in 128.6s (69 jobs, 16 at a time; slowest: Fences.test_a_panel_that_quits_or_hangs_never_passes 7s, Fences.test_fm_new_lists_copies_and_never_overwrites 2s, Fences.test_the_checks_catch_ [ran] [tree 304219efbb5a] [world 2f1906870a] (2026-11-06T19:18:47Z)
## Log
- 2026-11-06T19:11:50Z created
- 2026-11-06T19:12:38Z set tier=S
- 2026-11-06T19:12:39Z planned: it has criteria and steps
- 2026-11-06T19:12:42Z lane: ~/.claude/foreman.lanes/T-3522 on foreman/T-3522
- 2026-11-06T19:13:29Z focused
- 2026-11-06T19:13:30Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1035 [FEATURE M, done, 2 steps] Re-record the README demo video and refresh the README's pictures with the new UI (chat se — lesson: Record the demo after the UI work …
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- research readme-site-audit: Seven read-only auditors, one per slice; each claim checked against code and live data. Findings below are verified
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar past tasks were M: consider --tier M
