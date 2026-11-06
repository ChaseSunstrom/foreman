---
id: T-0349
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T03:47:19Z
updated: 2026-10-06T03:48:12Z
base: 1513cfb5beb2b3990e8270c69f6449511aabf512
base_tree: ce7c72491bb298c4cd7c7d1d0d3cc77e786daf95
verified: strong
---
# fm digest says when it lists only the latest finished tasks
## Raw request
> fm digest says 249 tasks done in the last 7 days but lists 8: the count likely uses a brief's last-touched time (tidy/archive/regen) instead of when it closed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with more than 8 finished tasks the digest labels its list as the latest 8 — verify with `python3 plugin/tests/run.py -k test_unattended`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + label
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_unattended` → ✗ exit 1 · Ran 9 tests in 2.9s (2 classes, 16 at a time; slowest: Unattended 3s, RunModels 0s) / FAILED (1 classes) [ran] [tree d81e23c7a00b] (2026-10-06T03:47:58Z)
- (step 1) `python3 plugin/tests/run.py -k test_unattended` → exit 0 · Ran 9 tests in 2.9s (2 classes, 16 at a time; slowest: Unattended 3s, RunModels 0s) / OK [ran] [tree 4848aa4d9c28] (2026-10-06T03:48:09Z)
- (ac 1) `python3 plugin/tests/run.py -k test_unattended` → exit 0 · Ran 9 tests in 2.9s (2 classes, 16 at a time; slowest: Unattended 3s, RunModels 0s) / OK [ran] [tree 4848aa4d9c28] (2026-10-06T03:48:12Z)
- (audit self) `self-review: the count was right (about 250 tasks really closed this week); the list showed only the newest 8 without saying so; now labelled` → no findings [tree 4848aa4d9c28] (2026-10-06T03:48:12Z)
## Log
- 2026-10-06T03:47:19Z created
- 2026-10-06T03:47:43Z planned from capture
- 2026-10-06T03:47:43Z focused
- 2026-10-06T03:47:52Z criterion 1 verify: `python3 plugin/tests/run.py -k test_cost` → `python3 plugin/tests/run.py -k test_unattended`
- 2026-10-06T03:48:12Z done
- 2026-10-06T03:48:12Z committed d1fdbc0 (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0004 [FEATURE M, done, 4 steps] Phase 6: fm tidy and fm doctor
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- T-0117 [FEATURE S, done, 2 steps] While-you-were-away row: what drive finished since the user's last message
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar finished tasks took 2–4 steps
- start here (files T-0117 touched): CHANGELOG.md, README.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts
## Files touched
- plugin/tests/test_unattended.py
- plugin/lib/fmcost.py
