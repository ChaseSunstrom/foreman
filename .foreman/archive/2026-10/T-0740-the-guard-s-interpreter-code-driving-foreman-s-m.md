---
id: T-0740
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T19:50:33Z
updated: 2026-10-09T19:51:19Z
base: 576d51c4142368dd587d28ccb49d57103f3b93a9
base_tree: 0aea665b9b448e5d2031deab32b735596c6e9033
verified: strong
---
# The guard's 'interpreter code driving Foreman's modules' refusal repeated 9 times today (f
## Raw request
> The guard's 'interpreter code driving Foreman's modules' refusal repeated 9 times today (fm dream): for a heredoc that edits a Foreman source file whose text mentions its modules, the refusal should say to use the Edit/Write tools, so the second try is right
## Interpretation
fm dream's first real run: the guard's 'interpreter code driving Foreman's modules' refusal came 9 times today, almost all from edit scripts whose replacement text mentions fm modules. The refusal names the fm CLI but not the way out for a source edit: the Edit or Write tool. Saying so makes the second try the right one.
## Assumptions (confidence)
## Acceptance criteria
- [x] the driving-modules refusal names the Edit or Write tool for source edits — verify with `python3 plugin/tests/run.py -p test_pass4.py -k EditTool`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] say it in the refusal
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py -k EditTool` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: EditTool 0s) / FAILED (1 classes) [ran] [tree edce37eedd6d] (2026-10-09T19:50:53Z)
- (step 2) `python3 plugin/tests/run.py -p test_pass4.py -p test_guard.py` → exit 0 · Ran 89 tests in 1.2s (34 classes, 16 at a time; slowest: Escapes 1s, NewFiles 1s, Sinks 0s) / OK [ran] [tree 701fe2e6043e] (2026-10-09T19:50:58Z)
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py -k EditTool` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: EditTool 0s) / OK [ran] [tree 701fe2e6043e] (2026-10-09T19:50:59Z)
- (ac 1) `python3 plugin/tests/run.py -p test_pass4.py -k EditTool` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: EditTool 0s) / OK [ran] [tree 701fe2e6043e] (2026-10-09T19:51:18Z)
- (audit adversary) `self: wording only, same category and decision; guard tests and the replay (no verdict changed) pass` → the message only adds a way out that the guard still checks (Edit and Write go through the brief and scope rules); no verdict changes, fm replay shows none [tree 701fe2e6043e] (2026-10-09T19:51:18Z)
- (audit self) `self: wording only, same category and decision; guard tests and the replay (no verdict changed) pass` → no findings [tree 701fe2e6043e] (2026-10-09T19:51:18Z)
## Log
- 2026-10-09T19:50:33Z created
- 2026-10-09T19:50:49Z focused
- 2026-10-09T19:51:18Z done
- 2026-10-09T19:51:19Z committed 3d4dfcc (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0286 [FEATURE M, done, 5 steps] Self-improvement pass 4: guard heredoc precision, test lockout of the real claude, untrusted-text sinks, escapes, hunk … — lesson: A mu…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- research dream-2026-10-09: `guard core: interpreter code driving Foreman's modules (use the fm CLI)` — 9 times (T-0380, T-0390, T-0413, T-0591, T-0672, T-0679, T-0685, T…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–5 steps
## Files touched
- plugin/tests/test_pass4.py
- plugin/lib/fmguard.py
