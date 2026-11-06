---
id: T-0889
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:35:16Z
base: 48b0cde0435f37bf5e7c8a953af160e31078cd55
base_tree: bd55992f8175d89dd84323ba40b132c0cf1fba7e
verified: strong
---
# Fm why FILE:LINE quotes the user's original request from the task that wrote the line
## Raw request
> FEATURE: fm why FILE:LINE quotes the user's original request from the task that wrote the line
> CONTEXT: round 5 #21. fm why lists commits, tasks and lessons (fmmap.py cmd_why); the brief's Raw request is the user's words
## Interpretation
fm why FILE[:LINE] adds, under each task it names, the user's own words from that task's Raw request (when they differ from the title), so the reason a line exists reads in the requester's terms
## Assumptions (confidence)
## Acceptance criteria
- [x] fm why shows the raw request of the task behind a line — verify with `python3 plugin/tests/run.py test_round_f`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_round_f, then cmd_why quotes Raw request
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_round_f test_map` → exit 0 · Ran 16 tests in 2.2s (4 classes, 16 at a time; slowest: RoundF 2s, Map 1s, Cold 0s) / OK [ran] [tree dd2d85b2d0ad] (2026-10-15T15:33:26Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 9 tests in 2.5s (1 classes, 16 at a time; slowest: RoundF 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree dd2d85b2d0ad] (2026-10-15T15:33:31Z)
- `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 9 tests in 2.1s (1 classes, 16 at a time; slowest: RoundF 2s) / OK [ran] [tree dd2d85b2d0ad] (2026-10-15T15:33:31Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 9 tests in 2.1s (1 classes, 16 at a time; slowest: RoundF 2s) / OK [ran] [tree dd2d85b2d0ad] (2026-10-15T15:35:15Z)
- (audit self) `self review: one quoted line per named task, only when the raw request says more than the title, capped at 240 chars; tried on a real line (fmnight.py:21 → T-0752's request)` → no findings [tree dd2d85b2d0ad] (2026-10-15T15:35:15Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:30:03Z set tier=S
- 2026-10-15T15:33:00Z focused
- 2026-10-15T15:35:16Z done
- 2026-10-15T15:35:16Z committed f53629a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/fmmap.py
