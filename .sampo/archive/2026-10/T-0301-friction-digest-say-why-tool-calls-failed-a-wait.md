---
id: T-0301
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T10:01:27Z
updated: 2026-10-04T10:03:26Z
base: 83473c5b13e8966b8c749a08788e4f5d2f340b79
base_tree: 0843e961f626bad80e3c4e3264aa4196414ebe0a
verified: strong
---
# Friction digest: say why tool calls failed; a wait on background work isn't friction
## Raw request
> Friction digest: say why tool calls failed; a wait on background work isn't friction
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the digest groups failed calls by tool and error and shows the error; drive waits are not listed as stops — verify with `python3 plugin/tests/run.py -p test_friction.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then fix fmfriction.py
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_friction.py` → ✗ exit 1 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: Friction 2s) / FAILED (1 classes) [ran] [tree c411527450e5] (2026-10-04T10:01:41Z)
- (step 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: Friction 2s) / OK [ran] [tree 2da92bf927d0] (2026-10-04T10:01:56Z)
- (step 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: Friction 2s) / OK [ran] [tree 0f80aa34d4d5] (2026-10-04T10:02:24Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.4    31.5     150  [0] / SessionEnd                  27.6    29.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 819 tests in [ran] [tree 0f80aa34d4d5] (2026-10-04T10:03:17Z)
- (ac 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: Friction 2s) / OK [ran] [tree 65697cac5cb8] (2026-10-04T10:03:26Z)
- (audit intent) `self: red→green on test_friction (both halves failed first); the live digest now reads '7× Bash: Exit code 1 — e.g. …'; friction, hooks, night and unattended suites pass` → recon findings 4 and 5 fixed; findings 1-3 dropped with reasons (fm decide) [tree 65697cac5cb8] (2026-10-04T10:03:26Z)
- (audit edge) `self: red→green on test_friction (both halves failed first); the live digest now reads '7× Bash: Exit code 1 — e.g. …'; friction, hooks, night and unattended suites pass` → an event with no error groups under 'no error recorded'; error and target pass through c.plain and c.fit; the trend's drive-stops count drops drive_wait, so the next trend line reads lower once [tree 65697cac5cb8] (2026-10-04T10:03:26Z)
- (audit self) `self: red→green on test_friction (both halves failed first); the live digest now reads '7× Bash: Exit code 1 — e.g. …'; friction, hooks, night and unattended suites pass` → no findings [tree 65697cac5cb8] (2026-10-04T10:03:26Z)
## Log
- 2026-10-04T10:01:27Z created
- 2026-10-04T10:01:28Z focused
- 2026-10-04T10:03:26Z done
- 2026-10-04T10:03:26Z committed b194b51 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261004-recon: 1. **Answer.** Four of the five findings are in the guard and the friction digest. The guard blocks most often on a heredoc that only writes…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0187 [FEATURE M, done, 3 steps] Self-improvement scoreboard: the friction digest rechecks each earlier guard block with today's guard and shows the trend since the las…
- T-0152 [CLEAN S, done, 1 steps] drive_wait is logged once per wait, not on every Stop
- similar finished tasks took 1–3 steps
## Lessons
- A digest that groups failures by target hides the cause; group by the error and keep the target as an example
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
