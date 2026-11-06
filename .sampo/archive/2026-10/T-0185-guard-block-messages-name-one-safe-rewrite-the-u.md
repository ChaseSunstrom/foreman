---
id: T-0185
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-03T19:12:03Z
updated: 2026-10-03T19:25:31Z
base: 5b97630cae2c563c0e3fe0eba438c0b3f9517887
base_tree: b90f5e23a2c9c239fd74656e74b8db60e3224e3a
verified: strong
---
# Guard block messages name one safe rewrite when the guard couldn't pin the target down
## Raw request
> Guard block messages name one safe rewrite (the unknown-target and state cases) — brainstorm round 4, value 3
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] each uncertain block names its rewrite — verify with `python3 plugin/tests/run.py -k test_an_uncertain_block_names_its_rewrite`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] hints in message()
3. [x] gates, docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_an_uncertain_block_names_its_rewrite` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Authorization 0s) / FAILED (1 classes) [ran] [tree 8fbc79f42b8d] (2026-10-03T19:24:19Z)
- (step 2) `python3 plugin/tests/run.py -k test_an_uncertain_block_names_its_rewrite` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Authorization 0s) / OK [ran] [tree 8c9acabc1268] (2026-10-03T19:24:28Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    31.8     150  [0] / SessionEnd                  28.3    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 8c9acabc1268] (2026-10-03T19:25:17Z)
- (ac 1) `python3 plugin/tests/run.py -k test_an_uncertain_block_names_its_rewrite` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Authorization 0s) / OK [ran] [tree 42a7dec63ac5] (2026-10-03T19:25:26Z)
- (audit self) `self: the test (three uncertain kinds name their rewrite, a certain block names none); fm replay confirms no verdict changed` → no findings [tree 42a7dec63ac5] (2026-10-03T19:25:26Z)
- (audit adversary) `self: the test (three uncertain kinds name their rewrite, a certain block names none); fm replay confirms no verdict changed` → message text only — no category, verdict or coverage changes (fm replay: 0 newly allowed, 0 newly blocked); the hints suggest literal paths and set-once variables, which the guard then checks normally, never a grant [tree 42a7dec63ac5] (2026-10-03T19:25:31Z)
- (audit self) `self: the test (three uncertain kinds name their rewrite, a certain block names none); fm replay confirms no verdict changed` → no findings [tree 42a7dec63ac5] (2026-10-03T19:25:31Z)
## Log
- 2026-10-03T19:12:03Z created
- 2026-10-03T19:24:08Z planned from capture
- 2026-10-03T19:24:08Z focused
- 2026-10-03T19:25:31Z done
- 2026-10-03T19:25:31Z committed d68d829 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- T-0183 [FIX M, done, 3 steps] Guard: unknown-target guesses come from the command's own words, pair up across unknown parts, and know a literal set once before any branc…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research brainstorm-20260926-slate: drive no-progress watchdog: exists (fmhooks _progressed + DRIVE_MAX 50) · eval rules drift test: exists (test_docs.test_eval_cases_em…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A refusal should carry its way out: the cost of a false block is the guess that follows it, and the guard already knew why it was unsure.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
