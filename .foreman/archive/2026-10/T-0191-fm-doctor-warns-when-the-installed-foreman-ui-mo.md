---
id: T-0191
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py,plugin/tests/test_doctor.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T19:18:32Z
updated: 2026-10-03T19:23:04Z
base: e2b83c689d7849c434fe3bb52cf704ce8532efcf
base_tree: 27c8297f10536b8edb23df947c9dc92dae4539e3
verified: strong
---
# fm doctor warns when the installed foreman-ui lags this repo
## Raw request
> fm doctor warns when the installed foreman-ui mod (or the plugin) is older than this repo's version — brainstorm round 4 slate item 2: 0.4.0 stayed installed while the repo moved on
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor warns on a lagging foreman-ui and passes on a matching one — verify with `python3 plugin/tests/run.py -k test_mod_release`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] check_mod_release
3. [x] gates, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (foreman-ui: release lag)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_mod_release` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / FAILED (1 classes) [ran] [tree 6e5f28129e6c] (2026-10-03T19:21:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_mod_release` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 6765418a6b27] (2026-10-03T19:22:04Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.7    32.6     150  [0] / SessionEnd                  28.4    30.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 6765418a6b27] (2026-10-03T19:22:56Z)
- (ac 1) `python3 plugin/tests/run.py -k test_mod_release` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree b90f5e23a2c9] (2026-10-03T19:23:04Z)
- (audit self) `self: the test (lagging → WARN naming both versions, released → PASS, not installed → PASS) and the real doctor, which now warns 0.4.0 installed vs 0.5.0 here` → no findings [tree b90f5e23a2c9] (2026-10-03T19:23:04Z)
## Log
- 2026-10-03T19:18:32Z created
- 2026-10-03T19:21:44Z planned from capture
- 2026-10-03T19:21:44Z focused
- 2026-10-03T19:23:04Z done
- 2026-10-03T19:23:04Z committed 5b97630 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize.
- likely tests for the scope: plugin/tests/test_doctor.py
## Lessons
- Compare what runs, not what the label says: the installed mod can lag with the same version number, so the check hashes its hooks.
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
