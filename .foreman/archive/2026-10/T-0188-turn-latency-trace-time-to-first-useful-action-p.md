---
id: T-0188
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py,plugin/tests/test_speed.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T19:12:03Z
updated: 2026-10-03T19:28:46Z
base: d68d829f01768a414024836f20d5eb33dc3763ad
base_tree: 42a7dec63ac58e74b1f491fa9eee4559f3aec754
verified: strong
---
# fm cost says where the time went: the model's against each tool's, shell commands by what they ran
## Raw request
> Turn latency trace: time to first useful action per turn, where the wall time goes — brainstorm round 4, value 3
## Interpretation
Brainstorm round 4 (the user's 'faster'): nothing says where an agent turn's wall time goes; fm cost reads the session logs for tokens only.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm cost splits the time between the model and each tool — verify with `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went`
## Non-goals
## Approach (options → choice → why)
A: in the same pass over the logs, each stretch between consecutive entries of a session (10 min or less) goes to what ended it: a tool result to its tool (a shell command to what it ran: fm's subcommand, else the program, after cd/assignments), a reply to the model; a prompt ends waiting time, which isn't counted. fm cost prints one Time line and the JSON carries the seconds. B (rejected): time hooks and turns live from the mod — only this session, and the logs already hold every session's timestamps.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] time accounting in fmcost.scan
3. [x] gates, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (fm cost: time)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went` → ✗ exit 1 · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 42a7dec63ac5] (2026-10-03T19:26:38Z)
- (step 1) `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / FAILED (1 classes) [ran] [tree c081d8884630] (2026-10-03T19:26:49Z)
- (step 2) `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / OK [ran] [tree d890de9a2d2e] (2026-10-03T19:27:36Z)
- (step 2) `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / OK [ran] [tree 48d4f967024e] (2026-10-03T19:27:47Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.8    31.8     150  [0] / SessionEnd                  28.2    29.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 48d4f967024e] (2026-10-03T19:28:38Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cost_says_where_the_time_went` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / OK [ran] [tree 5b79702587ad] (2026-10-03T19:28:46Z)
- (audit intent) `self: the test (model 14 s, Bash 20 s as fm check, an hour away not counted) and the real week (15 h active: model 55%, shell 44%)` → the user's 'faster' now has a measure: where an agent turn's wall time goes, per tool and per shell program [tree 5b79702587ad] (2026-10-03T19:28:46Z)
- (audit edge) `self: the test (model 14 s, Bash 20 s as fm check, an hour away not counted) and the real week (15 h active: model 55%, shell 44%)` → a prompt ends time waiting on the person (not counted), parallel results split their stretch evenly, unreadable timestamps and torn lines are skipped, entries before the window are left out [tree 5b79702587ad] (2026-10-03T19:28:46Z)
## Log
- 2026-10-03T19:12:03Z created
- 2026-10-03T19:26:38Z planned from capture
- 2026-10-03T19:26:38Z focused
- 2026-10-03T19:28:46Z done
- 2026-10-03T19:28:46Z committed e9ffd6d (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
## Lessons
- Measure before speeding up: the week's shell time was mostly test and script runs, not Foreman's bookkeeping, and 4% was waiting on a permission prompt.
## Files touched
- plugin/tests/test_speed.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md
