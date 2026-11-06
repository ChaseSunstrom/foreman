---
id: T-0917
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:18Z
updated: 2026-10-15T19:26:07Z
base: bc99c724ac805d6a7d534be1a343d24b7d8a5101
base_tree: 7baa257ed696e79d992611d5c7a92dab7bb98c5e
verified: strong
---
# Bare fm inside a project answers what now: the next action and the status line; help outside a project
## Raw request
> Bare fm inside a project answers what now: the next action and the status line; help outside a project
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] bare fm in a project prints Next: and the status line; outside one it prints help — verify with `python3 plugin/tests/run.py -k BareFm`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then main() picks next+status when a project resolves
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k BareFm` → ✗ exit 1 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: BareFm 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c136b2c12a99] (2026-10-15T19:26:04Z)
- `python3 plugin/tests/run.py -k BareFm` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: BareFm 0s) / OK [ran] [tree c136b2c12a99] (2026-10-15T19:26:04Z)
- (ac 1) `python3 plugin/tests/run.py -k BareFm` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: BareFm 0s) / OK [ran] [tree c136b2c12a99] (2026-10-15T19:26:06Z)
- (step 1) `python3 plugin/tests/run.py -k Help` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Help 1s) / OK [ran] [tree c136b2c12a99] (2026-10-15T19:26:06Z)
- (audit edge) `self: bare fm with no argv in a registered project prints the status line, a pointer to fm help, then fm next (its exit code); anything else, including fm -p X, parses as before; outside a project it is the help tiers` → a project that resolves only by -p still gets help on bare fm -p X (argv not empty), unchanged [tree c136b2c12a99] (2026-10-15T19:26:06Z)
- (audit self) `self: bare fm with no argv in a registered project prints the status line, a pointer to fm help, then fm next (its exit code); anything else, including fm -p X, parses as before; outside a project it is the help tiers` → no findings [tree c136b2c12a99] (2026-10-15T19:26:06Z)
## Log
- 2026-10-15T19:25:18Z created
- 2026-10-15T19:25:26Z focused
- 2026-10-15T19:26:06Z done
- 2026-10-15T19:26:07Z committed 7102c91 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
