---
id: T-0193
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py,plugin/tests/test_core.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T19:43:16Z
updated: 2026-10-03T19:44:26Z
base: 3985e30c6d236045bd88180bc9d59fcedb275e7f
base_tree: 8fc838ecd1e112e4a3ce2e6a2173c5105b02724f
verified: strong
---
# fm next moves past a step once it has evidence and ends at fm task finish, advising run evidence instead of typed
## Raw request
> fm next moves past a step once it has evidence and ends at fm task finish, advising run evidence instead of typed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] next advises the first step without evidence, then finish — verify with `python3 plugin/tests/run.py -k test_next_moves_past_a_step_with_evidence`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] next_action: cursor at the first step without evidence; run evidence; finish when all have it
3. [x] gates
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_next_moves_past_a_step_with_evidence` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Stages 0s) / FAILED (1 classes) [ran] [tree b17eea958ed5] (2026-10-03T19:43:16Z)
- (step 2) `python3 plugin/tests/run.py -k test_next_moves_past_a_step_with_evidence` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Stages 0s) / OK [ran] [tree 046541c542bc] (2026-10-03T19:43:26Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.2    32.3     150  [0] / SessionEnd                  27.9    31.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 065ddea3c012] (2026-10-03T19:44:20Z)
- (ac 1) `python3 plugin/tests/run.py -k test_next_moves_past_a_step_with_evidence` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Stages 0s) / OK [ran] [tree 065ddea3c012] (2026-10-03T19:44:26Z)
- (audit self) `self-review: the executing cursor is the first step with no evidence, all-evidenced → finish (whose own checks refuse a failed run); verifying names finish only when the criterion has a verify command, else the typed-evidence form; the live Next line now reads step 3/3 for this task after steps 1–2 were recorded` → no findings [tree 065ddea3c012] (2026-10-03T19:44:26Z)
## Log
- 2026-10-03T19:43:16Z created
- 2026-10-03T19:43:16Z focused
- 2026-10-03T19:44:26Z done
- 2026-10-03T19:44:26Z committed d245022 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0165 [FEATURE S, done, 3 steps] A step whose newest run failed closes when the same command passed later (the red run of red→green) — lesson: Evidence rules should fol…
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0147 [FIX S, done, 1 steps] Stop: a turn that ends on purpose for a mod reload isn't blocked by the evidence or question nudge — lesson: A gate meant to catch prematur…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Measure whether advice is followed before trusting it: the injected Next line was wrong for most of every task because it read a field only the close sets.
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
