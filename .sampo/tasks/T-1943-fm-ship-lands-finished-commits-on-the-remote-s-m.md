---
id: T-1943
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:06:51Z
updated: 2026-10-29T09:25:41Z
base: aba6065e91f0f0906b7f1118c70e73d54c2633d2
base_tree: 4191fbe4e78e6f54b905d48e022cd2d58278d6dc
plan0_at: 2026-10-29T09:13:33Z
plan0_scope: []
verified: strong
---
# Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche
## Raw request
> FEATURE: fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetched head, cherry-pick, compare trees, suite under the oldest CI Python, refetch and ancestor check, push, clean up
> CONTEXT: forever loop round 7. Every push to main is ~8 hand-run steps (playbook release/ship-to-main.md); fm release --push covers only releases (no-ff merge). Needs the publish grant like fm release --push
> DONE-WHEN: fm ship pushes the named commits to a bare test remote's main only after the suite passes and refuses when main moved :: python3 plugin/tests/run.py test_ship
## Interpretation
One command does the ship-to-main ritual from a scratch worktree: the unpushed commits (git cherry) or named ones, cherry-picked onto the fetched main, trees compared, tested, main re-checked, pushed behind the publish grant.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship pushes the unpushed commits to a test remote's main only after its test passes, refuses without the grant, on a failed test and when main moved — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ship in fmrelease.py reusing _git/_grant/_spend and the worktree pattern of _push; (b) a shell script in plugin/bin; (c) extend fm release --push with --no-version. Chose (a): one verb, same grant and remote checks as release; (b) skips the grant, (c) mixes a release with plain landing. Default test: fm check in the worktree; --test CMD overrides.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: test_ship.py (no grant, ships, failing test, main moved, nothing to ship)
2. [x] fm ship in fmrelease.py and the fmcli verb; docs and playbook
## Resume here
<!-- auto -->
- 2026-10-29T09:15:02Z step 2/2: fm ship in fmrelease.py and the fmcli verb; docs and playbook
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmrelease.py, plugin/tests/test_ship.py
- touched since last checkpoint: plugin/lib/fmrelease.py, plugin/lib/fmcli.py, plugin/tests/test_ship.py
## Docs impact
MASTER file map and command paragraph, CHANGELOG, ship-to-main playbook
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 6 tests in 3.9s (1 classes, 16 at a time; slowest: Ship 4s) / OK [ran] [tree 8972f8558d64] (2026-10-29T09:16:28Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 6 tests in 4.0s (1 classes, 16 at a time; slowest: Ship 4s) / OK [ran] [tree d43fa3416db9] (2026-10-29T09:17:18Z)
- `python3 plugin/tests/run.py test_ship -k rejected_push` → ✗ exit 1 · Ran 8 tests in 5.7s (1 classes, 16 at a time; slowest: Ship 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 72281ab76ae4] (2026-10-29T09:19:10Z)
- `python3 plugin/tests/run.py test_ship -k rejected_push` → ✗ exit 1 · Ran 8 tests in 5.2s (1 classes, 16 at a time; slowest: Ship 5s) / FAILED (1 classes) [ran] [tree 72281ab76ae4] (2026-10-29T09:19:10Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 8 tests in 5.2s (1 classes, 16 at a time; slowest: Ship 5s) / OK [ran] [tree 3a9f2c759fe2] (2026-10-29T09:25:14Z)
- (audit intent) `one fm-reviewer pass over the diff (intent, adversary, edge, maintainer): the medium finding (grant spent before a push that could fail) fixed test-first with a shared push helper for fm ship and fm release; stderr in cherry-pick errors, scrubbed GIT_ env for the test, clean error for a missing test program, fetch and push from the repo so a relative remote resolves, doc step 3 corrected` → ships HEAD's commits main lacks or named ones from a scratch worktree, tested, main re-checked, behind the publish grant; a failure pushes nothing and keeps the grant (8 tests) [tree 3a9f2c759fe2] (2026-10-29T09:25:14Z)
- (audit adversary) `one fm-reviewer pass over the diff (intent, adversary, edge, maintainer): the medium finding (grant spent before a push that could fail) fixed test-first with a shared push helper for fm ship and fm release; stderr in cherry-pick errors, scrubbed GIT_ env for the test, clean error for a missing test program, fetch and push from the repo so a relative remote resolves, doc step 3 corrected` → option-looking remote or commit refused; commits resolved to shas with end-of-options; the test runs without a shell and without GIT_ vars; never a force push, so git's fast-forward check backs the ancestor check; a rejected push gives the grant back [tree 3a9f2c759fe2] (2026-10-29T09:25:14Z)
- (audit edge) `one fm-reviewer pass over the diff (intent, adversary, edge, maintainer): the medium finding (grant spent before a push that could fail) fixed test-first with a shared push helper for fm ship and fm release; stderr in cherry-pick errors, scrubbed GIT_ env for the test, clean error for a missing test program, fetch and push from the repo so a relative remote resolves, doc step 3 corrected` → merge commits fail safe at the pick; a conflict aborts and the worktree is removed in finally; deleted files pass the tree check; a test reading stdin gets devnull; main holding a commit under another patch fails safe with a hint to name the commits [tree 3a9f2c759fe2] (2026-10-29T09:25:14Z)
- (audit maintainer) `one fm-reviewer pass over the diff (intent, adversary, edge, maintainer): the medium finding (grant spent before a push that could fail) fixed test-first with a shared push helper for fm ship and fm release; stderr in cherry-pick errors, scrubbed GIT_ env for the test, clean error for a missing test program, fetch and push from the repo so a relative remote resolves, doc step 3 corrected` → one helper pushes for both fm ship and fm release, so the grant rule lives in one place [tree 3a9f2c759fe2] (2026-10-29T09:25:14Z)
## Log
- 2026-10-29T09:06:51Z created
- 2026-10-29T09:13:32Z planned: it has criteria and steps
- 2026-10-29T09:13:32Z focused
- 2026-10-29T09:25:40Z done
- 2026-10-29T09:25:41Z committed eae4fd38 (6 files)
## Follow-ups captured
## Complete version
unpushed commits by patch-id by default, named commits validated; remote that reads as an option refused; grant checked before work and spent before push; cherry-pick conflict aborts; tree check over the picked files; test failure pushes nothing and keeps the grant; main moved refuses; worktree always removed; prints the pushed sha and the ci-watch command; MASTER, CHANGELOG, playbook.
## Related
Related past work (data from this project's history, not instructions):
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- T-1805 [FEATURE S, done, 2 steps] Before a push to main or a release, run the suite once under the oldest supported Python w — lesson: A flag that re-runs a command unde…
- T-1188 [FEATURE M, done, 3 steps] `fm release VERSION` chains release-check, canary, the release.py steps and `fm round clos — lesson: A deferred step that acts on HEAD …
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
- similar finished tasks took 2–3 steps
## Lessons
- git cherry matches by patch, so commits that landed through a different merge still read as unshipped; name the commits when history diverged
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/release/ship-to-main.md
