---
id: T-2819
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-03T17:03:35Z
updated: 2026-11-03T20:10:12Z
trigger: baseline
trigger_key: af53b81407c950c0
baseline: true
done_in: T-2822
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_demo.DemoNext.test_inside_a_project_the_demo_ends_with_its_next_step, test_docs.Fences.test_fm_new_lists_copies_and_never_overwrites, test_drill.Drill.test_every_kind_at_once_still_passes, test_exam.LanesKind.test_kind_lanes_the_drill_recovers_every_stop_by_its_cause_with_the_stub_s_work_kept. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-11-03T17:03:35Z created
- 2026-11-03T18:45:53Z same four tests as T-2822's root cause (sandbox env builders drop FOREMAN_HOST, so load gates fire in demo/drill/exam/fm new); closes when T-2822 merges
- 2026-11-03T20:10:12Z done in T-2822: same root cause, fixed by T-2822: sandboxes now skip the host load gate; the full suite at --load 30 and the ship's Python 3.12 run both passed
## Follow-ups captured
