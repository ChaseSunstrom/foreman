---
id: T-1281
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T17:04:36Z
updated: 2026-10-20T17:05:23Z
base: a127187de1a750c9b16139739ab70bbf8bbc4491
base_tree: 7632e55833714cbc12db8443d52024367a447b1c
plan0_at: 2026-10-20T17:04:37Z
plan0_scope: []
verified: strong
---
# CI red again on Linux 3.12: the context-tax replay counts the 'rules aren't wired' note that only an un-set-up HOME gets
## Raw request
> CI red again on Linux 3.12: the context-tax replay counts the 'rules aren't wired' note that only an un-set-up HOME gets
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the context-tax replay measures a set-up install whatever HOME the suite runs under — verify with `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: the replay under an empty HOME
2. [x] Give the replay a home with Foreman's rules wired
## Resume here
## Docs impact
none: a test-only fix
## Verification evidence
- (step 1) `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax` → ✗ exit 1 · Ran 1 test in 3.424s / FAILED (failures=1) [ran] [tree 7632e5583371] (2026-10-20T17:04:41Z)
- `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax` → exit 0 · Ran 1 test in 3.761s / OK (start tree + this task's tests) [ran] [tree 218dc1d43dc7] (2026-10-20T17:04:57Z)
- `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax` → exit 0 · Ran 1 test in 3.336s / OK [ran] [tree 218dc1d43dc7] (2026-10-20T17:04:57Z)
- (step 2) `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax` → exit 0 · Ran 1 test in 2.371s / OK [ran] [tree 218dc1d43dc7] (2026-10-20T17:05:14Z)
- (ac 1) `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax` → exit 0 · Ran 1 test in 1.578s / OK [ran] [tree 218dc1d43dc7] (2026-10-20T17:05:20Z)
- `cd plugin/tests && env -i PATH=/usr/bin:/bin HOME=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/emptyhome python3 -m unittest test_context_tax && python3 -m unittest test_context_tax` → exit 0 · Ran 1 test in 1.635s / OK [ran] [tree 218dc1d43dc7] (2026-10-20T17:05:20Z)
- (audit intent) `self: reproduced CI's 1360/1348 bytes with an empty HOME, found the one-time setup note, made the replay's HOME a set-up one` → the ratchet measures Foreman's steady-state injection, not a first-run setup note, so it is the same on any machine [tree 218dc1d43dc7] (2026-10-20T17:05:20Z)
- (audit edge) `self: reproduced CI's 1360/1348 bytes with an empty HOME, found the one-time setup note, made the replay's HOME a set-up one` → HOME is restored after the test; the setup note itself still shows on an un-set-up machine, untouched [tree 218dc1d43dc7] (2026-10-20T17:05:20Z)
- (audit self) `self: reproduced CI's 1360/1348 bytes with an empty HOME, found the one-time setup note, made the replay's HOME a set-up one` → no findings [tree 218dc1d43dc7] (2026-10-20T17:05:20Z)
## Log
- 2026-10-20T17:04:36Z created
- 2026-10-20T17:04:37Z focused
- 2026-10-20T17:05:22Z done
- 2026-10-20T17:05:23Z committed cd7da43f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1258 [PERFORMANCE M, done, 2 steps] A context-tax ratchet: a replayed hook session's injected bytes per event stay under a bud — lesson: Measure a tax by kind before c…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- similar past tasks were M: consider --tier M
## Why not caught
the suite ran here with my own HOME, where Foreman's rules are wired; CI's runner has a bare HOME
## Lessons
- A test that measures hook output must pin HOME: SessionStart adds a setup note on a machine where Foreman isn't wired
## Plan gaps
- failed first: step 1 Red: the replay under an empty HOME
## Files touched
- plugin/tests/test_context_tax.py
