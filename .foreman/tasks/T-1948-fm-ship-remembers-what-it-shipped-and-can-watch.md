---
id: T-1948
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:39:17Z
updated: 2026-10-29T09:49:29Z
batch: [T-1945, T-1946]
base: c46d33307cb1c75846848ff77f085c6abce98dcb
base_tree: 8580d1221144b7cf729c3ecd838d324a023ed1b3
plan0_at: 2026-10-29T09:39:25Z
plan0_scope: []
verified: strong
---
# fm ship remembers what it shipped and can watch CI
## Raw request
> T-1945: FEATURE: fm ship remembers the last commit it shipped (a ref under refs/foreman/) and its default picks start after it (git cherry's limit), so commits that reached main through a merge under other patches no longer block a plain fm ship
> DONE-WHEN: after one ship, a plain fm ship skips everything up to the shipped commit even when git cherry still lists it
> T-1946: FEATURE: fm ship --watch runs fm ci-watch on the pushed sha after the push, in the same job, and exits with its code
> DONE-WHEN: fm ship --watch pushes, then watches the pushed commit and returns the watch's code
## Interpretation
A plain fm ship lists commits main already holds through a merge (7 old playbook commits), so the user must name commits each time; and CI is watched by a second command. Remember the last shipped commit and start default picks after it; --watch watches CI on the pushed sha in the same job.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1945: after one ship, a plain fm ship skips everything up to the shipped commit even when git cherry still lists it — verify with `python3 plugin/tests/run.py test_ship -k shipped`
- [x] T-1946: fm ship --watch pushes, then watches the pushed commit and returns the watch's code — verify with `python3 plugin/tests/run.py test_ship -k watch`
- [x] default picks start after the last shipped commit; --watch watches CI on the pushed sha — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
After a push, update-ref refs/foreman/shipped to the last pick; default picks use git cherry's limit argument when that ref exists. --watch calls fmci.watch on the tip after the push and returns its code. Rejected: per-remote refs (one remote in practice); a separate config file (git refs already persist).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1945: Fm ship remembers the last commit it shipped (a ref under refs/foreman/) and its default p
2. [x] T-1946: Fm ship --watch runs fm ci-watch on the pushed sha after the push, in the same job, and ex
3. [x] failing tests, then the shipped ref and --watch
## Resume here
## Docs impact
MASTER, CHANGELOG and the ship-to-main playbook name the shipped ref and --watch
## Verification evidence
- (ac 3) `python3 plugin/tests/run.py test_ship 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|Error:" | head` → ✗ exit 1 · Ran 10 tests in 6.5s (1 classes, 16 at a time; slowest: Ship 6s) / FAILED (1 classes) [ran] [tree 5a30b1dd8cbf] (2026-10-29T09:40:37Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 10 tests in 7.3s (1 classes, 16 at a time; slowest: Ship 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:43:56Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 10 tests in 6.6s (1 classes, 16 at a time; slowest: Ship 6s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:43:56Z)
- (step 1) `python3 plugin/tests/run.py test_ship -k shipped` → exit 0 · Ran 21 tests in 6.6s (11 classes, 16 at a time; slowest: Ship 6s, Coverage 2s, Loop 1s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:44:03Z)
- (step 2) `python3 plugin/tests/run.py test_ship -k watch` → exit 0 · Ran 21 tests in 6.5s (5 classes, 16 at a time; slowest: Ship 6s, Watch 3s, CiWatch 2s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:44:10Z)
- (step 3) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 10 tests in 6.6s (1 classes, 16 at a time; slowest: Ship 6s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:44:17Z)
- (ac 1) `python3 plugin/tests/run.py test_ship -k shipped` → exit 0 · Ran 21 tests in 6.6s (11 classes, 16 at a time; slowest: Ship 6s, Coverage 2s, Loop 1s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (ac 2) `python3 plugin/tests/run.py test_ship -k watch` → exit 0 · Ran 21 tests in 6.6s (5 classes, 16 at a time; slowest: Ship 6s, Watch 3s, CiWatch 2s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (ac 3) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 10 tests in 6.6s (1 classes, 16 at a time; slowest: Ship 6s) / OK [ran] [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (audit edge) `self-review: the shipped ref is written after a successful push and used as git cherry's limit only when it is an ancestor of HEAD; --watch reuses fmci.watch on the pushed tip; full gates green (4173 tests)` → a branch behind the shipped ref (or a rebased one) ignores the ref and falls back to plain git cherry, so nothing is hidden by a stale ref; named commits move the ref to the last one named [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (audit edge) `self-review: the shipped ref is written after a successful push and used as git cherry's limit only when it is an ancestor of HEAD; --watch reuses fmci.watch on the pushed tip; full gates green (4173 tests)` → if update-ref itself failed after the push, fm ship would report an error though main got the commits; a re-run then says nothing to ship [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (audit adversary) `self-review: the shipped ref is written after a successful push and used as git cherry's limit only when it is an ancestor of HEAD; --watch reuses fmci.watch on the pushed tip; full gates green (4173 tests)` → the ref is local and read back as a sha from rev-parse, never as an option; --watch only reads CI and briefs failures as untrusted data like fm ci-watch [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
- (audit self) `self-review: the shipped ref is written after a successful push and used as git cherry's limit only when it is an ancestor of HEAD; --watch reuses fmci.watch on the pushed tip; full gates green (4173 tests)` → no findings [tree bcb2c2e5f4e3] (2026-10-29T09:49:01Z)
## Log
- 2026-10-29T09:39:17Z created
- 2026-10-29T09:39:25Z focused
- 2026-10-29T09:39:37Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_ship -k shipped`
- 2026-10-29T09:39:37Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_ship -k watch`
- 2026-10-29T09:49:27Z done
- 2026-10-29T09:49:29Z committed 00ca36e8 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- T-0884 [FEATURE M, done, 3 steps] Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout -- — lesson: A hook that does real work before …
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/release/ship-to-main.md
