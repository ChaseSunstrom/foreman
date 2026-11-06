---
id: T-1147
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/agents/fm-builder.md, plugin/tests/test_lanes.py, plugin/tests/test_builder.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:08:44Z
updated: 2026-10-16T10:17:25Z
base: 6a87a2f8217599c250f7777f6c9eb34670412a52
base_tree: 5b1cb9774b3ddcc933a5f25b5bb7993482366da9
plan0_at: 2026-10-16T10:12:59Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/agents/fm-builder.md, plugin/tests/test_lanes.py, plugin/tests/test_builder.py, CHANGELOG.md]
verified: strong
---
# Builders self-review before they report: the builder contract adds an adversary pass (what
## Raw request
> Builders self-review before they report: the builder contract adds an adversary pass (what input breaks it, what it trusts, what is unbounded) whose findings are fixed or listed; reviewers found real defects in almost every builder branch on 2026-10-16
## Interpretation
Builders report done without an adversarial look at their own change; the reviewer then finds a real defect in almost every branch (deny bypass, false green, unbounded time, writes outside a folder). Add a self-review pass to the builder contract, so obvious ones are fixed before the main thread's review.
## Assumptions (confidence)
## Acceptance criteria
- [x] the builder brief and agent definition carry the self-review checklist and require a Self-review section in the report — verify with `python3 plugin/tests/run.py test_lanes test_builder`
## Non-goals
## Approach (options → choice → why)
Append to fmlanes.CONTRACT (and agents/fm-builder.md) a short adversary checklist the builder must answer in its report: what input breaks it, what outside text it trusts, what is unbounded (time, size, retries), what writes where, and what a second run does. Fix what it finds, or list it under 'Self-review'. Options considered: a mandatory reviewer per builder (cost already paid once by the main thread), or nothing (the status quo found defects late).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then add the checklist to CONTRACT and fm-builder.md
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 29 tests in 12.6s (4 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) [ran] [tree 1609a4c45bc1] (2026-10-16T10:13:31Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 50 tests in 12.6s (10 classes, 16 at a time; slowest: Lanes 12s, Contract 9s, Brief 5s) / OK [ran] [tree 6b91850b2a1d] (2026-10-16T10:14:09Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 50 tests in 10.7s (10 classes, 16 at a time; slowest: Lanes 11s, Contract 7s, Brief 3s) / OK [ran] [tree 48e154ef5085] (2026-10-16T10:16:20Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 50 tests in 10.5s (10 classes, 16 at a time; slowest: Lanes 10s, Contract 7s, Brief 3s) / OK [ran] [tree 5184ce6d50a1] (2026-10-16T10:16:42Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 29 tests in 10.2s (4 classes, 16 at a time; slowest: Lanes 10s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 5184ce6d50a1] (2026-10-16T10:16:42Z)
- (audit self) `self: the checklist names the defect classes reviewers found on 2026-10-16 (deny-bypass, untrusted text, unbounded time, writes outside a folder, second-run behaviour); the test checks both texts carry it; its effect shows in later reviews` → no findings [tree 5184ce6d50a1] (2026-10-16T10:16:42Z)
## Log
- 2026-10-16T10:08:44Z created
- 2026-10-16T10:09:29Z set scope=['plugin/lib/fmlanes.py', 'plugin/agents/fm-builder.md', 'plugin/tests/test_lanes.py', 'plugin/tests/test_builder.py', 'CHANGELOG.md']
- 2026-10-16T10:12:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1147.builder.md
- 2026-10-16T10:12:58Z focused
- 2026-10-16T10:15:52Z merged worktree-agent-a950001ea6262b2c4 (3 file(s))
- 2026-10-16T10:15:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a950001ea6262b2c4
- 2026-10-16T10:16:05Z focused
- 2026-10-16T10:16:21Z scope: CHANGELOG.md — release note
- 2026-10-16T10:17:24Z done
- 2026-10-16T10:17:25Z committed 8aeebcf (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- Make the agent that writes the change ask the reviewer's questions first: the reviewer then finds what's left
## Plan gaps
- failed first: step 1 Test then add the checklist to CONTRACT and fm-builder.md
## Files touched
- plugin/tests/test_lanes.py
- plugin/agents/fm-builder.md
- plugin/lib/fmlanes.py
- CHANGELOG.md
