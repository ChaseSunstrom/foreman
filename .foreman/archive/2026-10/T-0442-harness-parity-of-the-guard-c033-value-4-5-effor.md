---
id: T-0442
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:42:29Z
base: 1a35601b4f9437a499710a6b6fa7fb8eec2388c9
base_tree: 37f2c08271f094656f88156bdeebfbf735d40fe4
verified: strong
---
# Guard parity across harnesses: same decision on codex, gemini and opencode
## Raw request
> SECURITY: Harness parity of the guard (C033, value 4/5, effort M, risk low)
>   first version: Generate an enforcement matrix from fmagents capability tables (which events block, which only warn) into fm doctor, and run the guard fixtures through each adapter's payload shape.
>   what it is: Enforce and test the guard identically on every harness shell form, with a PATH shim and a published enforcement matrix.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
The guard runs for Claude Code and, through fmagents adapters, for codex, gemini and opencode. Show per harness what is enforced and what is only advisory (gemini has no Stop, ask becomes deny elsewhere, unmapped tool names pass through), and prove with a test that each guard fixture gets the same deny/allow on every adapter.
## Assumptions (confidence)
## Acceptance criteria
- [x] every guard fixture gets the same decision on codex, gemini and opencode as on Claude — verify with `python3 plugin/tests/run.py -k test_guard_decision_matches_across_harnesses`
- [x] the matrix lists every agent and marks each event block or advisory — verify with `python3 plugin/tests/run.py -k test_enforcement_matrix_lists_every_agent`
## Non-goals
## Approach (options → choice → why)
(B, chosen) matrix() from fmagents' EVENTS/SHELL tables in status + doctor, and a parametrized parity test over the hook payload fixtures (reverse-mapped per agent). (A) a doc matrix only: drifts. (C, rejected) a PATH shim: too big.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: parity test
2. [x] matrix() + status/doctor + MASTER line
## Resume here
## Docs impact
CHANGELOG + MASTER (fmagents)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard_decision_matches_across_harnesses -k test_enforcement_matrix_lists_every_agent` → ✗ exit 1 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Hook 1s) / FAILED (1 classes) [ran] [tree ae6e48afa27e] (2026-10-09T14:41:44Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard_decision_matches_across_harnesses -k test_enforcement_matrix_lists_every_agent` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Hook 1s) / OK [ran] [tree 8d092894017c] (2026-10-09T14:41:58Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard_decision_matches_across_harnesses` → exit 0 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: Hook 2s) / OK [ran] [tree 8baf7c62a751] (2026-10-09T14:42:28Z)
- (ac 2) `python3 plugin/tests/run.py -k test_enforcement_matrix_lists_every_agent` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Hook 0s) / OK [ran] [tree 8baf7c62a751] (2026-10-09T14:42:28Z)
- (audit adversary) `self: parity test (6 shell + 2 write cases x 3 harnesses, each in its own payload shape) passes against the current adapters; matrix from EVENTS; MASTER line; agents + doctor suites OK` → the parity test is the guard's regression lock for the other harnesses: any adapter change that lets one through fails it [tree 8baf7c62a751] (2026-10-09T14:42:28Z)
- (audit edge) `self: parity test (6 shell + 2 write cases x 3 harnesses, each in its own payload shape) passes against the current adapters; matrix from EVENTS; MASTER line; agents + doctor suites OK` → unmapped tool names still pass through unguarded by design (not a shell or write); noted in the matrix text indirectly [tree 8baf7c62a751] (2026-10-09T14:42:28Z)
- (audit intent) `self: parity test (6 shell + 2 write cases x 3 harnesses, each in its own payload shape) passes against the current adapters; matrix from EVENTS; MASTER line; agents + doctor suites OK` → shows enforced vs advisory per harness and proves the same decision, as planned [tree 8baf7c62a751] (2026-10-09T14:42:28Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:38:30Z planned from capture
- 2026-10-09T14:41:08Z focused
- 2026-10-09T14:42:29Z done
- 2026-10-09T14:42:29Z committed e323c68 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0512 [SECURITY M, dropped, 0 steps] Harness parity of the guard (C033, value 4/5, effort M, risk low)
- T-0440 [SECURITY M, done, 3 steps] Every refusal names its fix; a third identical refusal escalates — lesson: A retry loop is a signal: the third identical refusal shoul…
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
- the similar finished task took 3 steps
- start here (files T-0440 touched): plugin/tests/test_hooks.py, plugin/lib/fmhooks.py, CHANGELOG.md
## Lessons
- A test that passes on day one is still worth writing when it locks a property no other test covers.
## Files touched
- plugin/tests/test_agents.py
- plugin/lib/fmagents.py
- MASTER.md
- CHANGELOG.md
