---
id: T-0424
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T14:00:49Z
updated: 2026-10-09T14:15:15Z
base: b58bad0007aac79a97ac9475dfb53e6bfc8d05b0
base_tree: e0ea593c021e97fd7fc60302894e7bca0324ff65
verified: strong
---
# fm friction: slow-gate signal compares real runs only
## Raw request
> FIX: fm friction's slow-gate signal compares against a median that counts reused passes (0.0 s): 'fm replay 12s vs usual 0s' (fmfriction.py:115-117); take the median over real runs only
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a gate whose reused passes are 0.0 s is compared against the median of its real runs — verify with `python3 plugin/tests/run.py -k test_slow_gate_ignores_reused_passes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the median over runs with s > 0 in fmfriction
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_slow_gate_ignores_reused_passes` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Friction 0s) / FAILED (1 classes) [ran] [tree 64e597de607d] (2026-10-09T14:12:43Z)
- (step 1) `python3 plugin/tests/run.py -k test_slow_gate_ignores_reused_passes` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Friction 0s) / OK [ran] [tree b0b8dc4939d2] (2026-10-09T14:12:48Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                51.5    79.9     150  [0] / SessionEnd                  46.3    63.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 971 tests in [ran] [tree b0b8dc4939d2] (2026-10-09T14:14:53Z)
- (ac 1) `python3 plugin/tests/run.py -k test_slow_gate_ignores_reused_passes` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Friction 0s) / OK [ran] [tree 4e8eb5df022a] (2026-10-09T14:15:14Z)
- (audit adversary) `builder branch read (one condition, matching fmcli._slower); red→green recorded by the builder; merged; criterion rerun OK` → reads the project's own ledger only; the guard files in its diff range are T-0414/T-0421/T-0422's, reviewed there [tree 4e8eb5df022a] (2026-10-09T14:15:14Z)
- (audit edge) `builder branch read (one condition, matching fmcli._slower); red→green recorded by the builder; merged; criterion rerun OK` → 'latest' is now the latest real run; a gate with only reused passes has no line [tree 4e8eb5df022a] (2026-10-09T14:15:14Z)
- (audit self) `builder branch read (one condition, matching fmcli._slower); red→green recorded by the builder; merged; criterion rerun OK` → no findings [tree 4e8eb5df022a] (2026-10-09T14:15:14Z)
## Log
- 2026-10-09T14:00:49Z created
- 2026-10-09T14:12:07Z planned from capture
- 2026-10-09T14:12:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0424.builder.md
- 2026-10-09T14:12:18Z focused
- 2026-10-09T14:15:08Z merged worktree-agent-a49949272833e0676 (2 file(s))
- 2026-10-09T14:15:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a49949272833e0676
- 2026-10-09T14:15:14Z focused
- 2026-10-09T14:15:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-20261009b: 1. **Answer.** I could ground three improvements. The biggest is that the guard-block log records the wrong part of the command. That made t…
- T-0261 [FEATURE M, done, 4 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log — lesson: Filtering a marked line out of the one accessor …
- T-0187 [FEATURE M, done, 3 steps] Self-improvement scoreboard: the friction digest rechecks each earlier guard block with today's guard and shows the trend since the las…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Lessons
- A cache hit is not a measurement: keep reused results out of timing statistics.
## Files touched
- .claude/worktrees/agent-a49949272833e0676/plugin/tests/test_friction.py
- .claude/worktrees/agent-a49949272833e0676/plugin/lib/fmfriction.py
- CHANGELOG.md
- plugin/lib/fmfriction.py
- plugin/lib/fmhooks.py
- plugin/tests/test_friction.py
- plugin/tests/test_hooks.py
