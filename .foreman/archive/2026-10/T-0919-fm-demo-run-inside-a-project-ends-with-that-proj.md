---
id: T-0919
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:19Z
updated: 2026-10-15T19:28:30Z
base: 95bb32f4a96f85b8f3f139d61ac32ac173de5a59
base_tree: 536b188de08a6a66a793d1bb6e7a6bbef886f01d
verified: strong
---
# fm demo run inside a project ends with that project's own next step
## Raw request
> fm demo run inside a project ends with that project's own next step
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm demo in a registered project ends with its fm next line; elsewhere the fm init line — verify with `python3 plugin/tests/run.py -k DemoNext`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then fmdemo's last lines
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k DemoNext` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: DemoNext 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5510d19b2065] (2026-10-15T19:28:23Z)
- `python3 plugin/tests/run.py -k DemoNext` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: DemoNext 2s) / OK [ran] [tree 5510d19b2065] (2026-10-15T19:28:23Z)
- (ac 1) `python3 plugin/tests/run.py -k DemoNext` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: DemoNext 2s) / OK [ran] [tree 5510d19b2065] (2026-10-15T19:28:29Z)
- (step 1) `python3 plugin/tests/run.py -k Demo` → exit 0 · Ran 5 tests in 3.8s (2 classes, 16 at a time; slowest: Demo 4s, DemoNext 2s) / OK [ran] [tree 5510d19b2065] (2026-10-15T19:28:29Z)
- (audit edge) `self: inside a registered project the demo's last line names that project and its next action (fm next's first clause); elsewhere the fm init line; record.py now runs from the temp dir so the README recording stays generic` → find_project never creates here (create=False), so a repo that isn't a Foreman project stays untouched [tree 5510d19b2065] (2026-10-15T19:28:29Z)
- (audit self) `self: inside a registered project the demo's last line names that project and its next action (fm next's first clause); elsewhere the fm init line; record.py now runs from the temp dir so the README recording stays generic` → no findings [tree 5510d19b2065] (2026-10-15T19:28:29Z)
## Log
- 2026-10-15T19:25:19Z created
- 2026-10-15T19:27:28Z focused
- 2026-10-15T19:28:19Z scope: demo/record.py runs fm demo from the temp dir, so the README recording never ends on this repo's own next task
- 2026-10-15T19:28:30Z done
- 2026-10-15T19:28:30Z committed 347cdf2 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0917 [FEATURE S, done, 1 steps] Bare fm inside a project answers what now: the next action and the status line; help outside a project
- T-0896 [FEATURE S, done, 1 steps] A RESEARCH task can't close without a Decision section, and its decision lands in decision
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar finished tasks took 1–1 steps
## Files touched
- plugin/tests/test_demo.py
- plugin/lib/fmdemo.py
- demo/record.py
