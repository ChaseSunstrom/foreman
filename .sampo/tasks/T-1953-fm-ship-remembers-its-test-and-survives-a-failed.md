---
id: T-1953
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:50:45Z
updated: 2026-10-29T09:58:10Z
batch: [T-1950, T-1951]
base: 00ca36e8209572704cdc47bb0c8cb1faeb1a3f7b
base_tree: bcb2c2e5f4e3b035d6f4b3155feb8ffd8588e1ad
plan0_at: 2026-10-29T09:50:54Z
plan0_scope: []
verified: strong
---
# fm ship remembers its --test and survives a failed ref write
## Raw request
> T-1950: FEATURE: fm ship remembers the last --test it was given (git config foreman.shiptest) and uses it when --test is left out, so the oldest runtime's suite isn't retyped each ship
> DONE-WHEN: a second fm ship without --test runs the first one's --test
> T-1951: FIX: fm ship reports a failure when writing refs/foreman/shipped fails after a successful push; the push landed, so it should warn and still print the shipped line
> DONE-WHEN: a failed update-ref after the push exits 0 with a warning
## Interpretation
Every ship retypes the long oldest-runtime --test; and a failed refs/foreman/shipped write after a pushed ship reports failure though main got the commits.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1950: a second fm ship without --test runs the first one's --test — verify with `python3 plugin/tests/run.py test_ship -k remembered_test`
- [x] T-1951: a failed update-ref after the push exits 0 with a warning — verify with `python3 plugin/tests/run.py test_ship -k ref_write`
## Non-goals
## Approach (options → choice → why)
Store --test in git config foreman.shiptest (local) and read it when --test is absent, before falling back to fm check. Write the shipped ref with ok=True and print a warning when it fails. Rejected: a Foreman config file (git config already persists per repo).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1950: Fm ship remembers the last --test it was given (git config foreman.shiptest) and uses it w
2. [x] T-1951: Fm ship reports a failure when writing refs/foreman/shipped fails after a successful push;
## Resume here
## Docs impact
MASTER, CHANGELOG and the --test help name the remembered test and the warning
## Verification evidence
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 12 tests in 16.6s (1 classes, 16 at a time; slowest: Ship 15s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7690d45fe489] (2026-10-29T09:52:31Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 12 tests in 15.1s (1 classes, 16 at a time; slowest: Ship 15s) / OK [ran] [tree 7690d45fe489] (2026-10-29T09:52:31Z)
- (step 1) `python3 plugin/tests/run.py test_ship -k remembered_test` → exit 0 · Ran 12 tests in 12.8s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree 7690d45fe489] (2026-10-29T09:52:49Z)
- (step 2) `python3 plugin/tests/run.py test_ship -k ref_write` → exit 0 · Ran 12 tests in 8.0s (1 classes, 16 at a time; slowest: Ship 8s) / OK [ran] [tree 7690d45fe489] (2026-10-29T09:52:58Z)
- (ac 1) `python3 plugin/tests/run.py test_ship -k remembered_test` → exit 0 · Ran 12 tests in 8.0s (1 classes, 16 at a time; slowest: Ship 8s) / OK [ran] [tree 7690d45fe489] (2026-10-29T09:57:41Z)
- (ac 2) `python3 plugin/tests/run.py test_ship -k ref_write` → exit 0 · Ran 12 tests in 8.0s (1 classes, 16 at a time; slowest: Ship 8s) / OK [ran] [tree 7690d45fe489] (2026-10-29T09:57:41Z)
- (audit edge) `self-review: --test is stored in local git config and read back when absent, printed in the testing line; a failed shipped-ref write after the push warns instead of failing; full gates green (4175 tests)` → the remembered test is per repo (local config), never global; an explicit --test always wins and replaces it [tree 7690d45fe489] (2026-10-29T09:57:41Z)
- (audit adversary) `self-review: --test is stored in local git config and read back when absent, printed in the testing line; a failed shipped-ref write after the push warns instead of failing; full gates green (4175 tests)` → the value comes from the repo's own .git/config, which clone never copies; anyone who can write it can already set core.sshCommand, so it adds no new way to run code [tree 7690d45fe489] (2026-10-29T09:57:41Z)
- (audit edge) `self-review: --test is stored in local git config and read back when absent, printed in the testing line; a failed shipped-ref write after the push warns instead of failing; full gates green (4175 tests)` → a locked refs/foreman/shipped after the push exits 0 with a warning naming the ref, and main holds the commits [tree 7690d45fe489] (2026-10-29T09:57:41Z)
- (audit self) `self-review: --test is stored in local git config and read back when absent, printed in the testing line; a failed shipped-ref write after the push warns instead of failing; full gates green (4175 tests)` → no findings [tree 7690d45fe489] (2026-10-29T09:57:41Z)
## Log
- 2026-10-29T09:50:45Z created
- 2026-10-29T09:50:51Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_ship -k remembered_test`
- 2026-10-29T09:50:52Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_ship -k ref_write`
- 2026-10-29T09:50:53Z focused
- 2026-10-29T09:58:08Z done
- 2026-10-29T09:58:10Z committed 3931eea0 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1948 [FEATURE S, done, 3 steps] fm ship remembers what it shipped and can watch CI
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–3 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
