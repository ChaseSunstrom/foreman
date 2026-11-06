---
id: T-0382
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T00:51:16Z
updated: 2026-10-09T01:05:02Z
base: 9956efc35cb43db0d1f7e5b238093a0ce92ed689
base_tree: ddf47d8f94114527a46e067d956ffabed8dbc2b6
verified: strong
---
# SECURITY: fm lane merge checks only the new side of a rename; a lane moving a guarded file
## Raw request
> SECURITY: fm lane merge checks only the new side of a rename; a lane moving a guarded file passes the guard (diff --no-renames)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane that renames a guarded file is refused by fm lane merge — verify with `python3 plugin/tests/run.py -k test_lane_merge_checks_both_sides_of_a_rename`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: rename a credentials file in a lane; merge must refuse (diff --no-renames)
2. [x] gate, changelog
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_lane_merge_checks_both_sides_of_a_rename` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Contract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0f98ca3bdcf1] (2026-10-09T01:02:56Z)
- `python3 plugin/tests/run.py -k test_lane_merge_checks_both_sides_of_a_rename` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Contract 0s) / OK [ran] [tree 0f98ca3bdcf1] (2026-10-09T01:02:56Z)
- `python3 plugin/tests/run.py -k test_git_hygiene` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Checks 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 63119faba18a] (2026-10-09T01:03:43Z)
- `python3 plugin/tests/run.py -k test_git_hygiene` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 63119faba18a] (2026-10-09T01:03:43Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.4    34.8     150  [0] / SessionEnd                  29.6    31.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 906 tests in [ran] [tree d322b3c86ec6] (2026-10-09T01:04:52Z)
- (step 1) `python3 plugin/tests/run.py -k test_lane_merge_checks_both_sides_of_a_rename` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Contract 0s) / OK [ran] [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lane_merge_checks_both_sides_of_a_rename` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Contract 0s) / OK [ran] [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
- (audit adversary) `self: traced both listings against git's rename detection; red→green tests for each` → a lane renaming config/secrets.yaml is refused (credentials) and the file stays in main; --no-renames also disables copy detection, so copies list their new path as an add; plain deletions were already listed [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
- (audit edge) `self: traced both listings against git's rename detection; red→green tests for each` → names with spaces in the doctor scan now split on NUL (-z) instead of whitespace [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
- (audit intent) `self: traced both listings against git's rename detection; red→green tests for each` → closes the automated security finding on fmlanes.merge; the same blind spot in fmdoctor fixed alongside [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
- (audit self) `self: traced both listings against git's rename detection; red→green tests for each` → no findings [tree d322b3c86ec6] (2026-10-09T01:05:02Z)
## Log
- 2026-10-09T00:51:16Z created
- 2026-10-09T01:02:39Z focused
- 2026-10-09T01:03:36Z scope: same rename blind spot in fmdoctor.check_git_hygiene (--diff-filter=AM drops a staged rename+edit carrying a secret); fixed here with its test
- 2026-10-09T01:05:02Z done
- 2026-10-09T01:05:02Z committed a9e5ca9 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261008-195201.pack: super improve foreman
- research mission-20261008-195201: Request: super improve foreman
- research brainstorm-pass-5: Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensab…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
## Lessons
- Any guard or scan that lists changed files must pass --no-renames: a rename's old path is a delete the check has to see
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
