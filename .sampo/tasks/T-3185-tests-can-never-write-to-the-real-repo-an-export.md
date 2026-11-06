---
id: T-3185
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T09:06:39Z
updated: 2026-11-05T09:09:34Z
base: a2dfd36a074ffee2196e6674b1377ff6f0bc2146
base_tree: 2a443c5667f9e8c5d3bc3edd22ce65064695d6e2
plan0_at: 2026-11-05T09:06:40Z
plan0_scope: []
verified: strong
---
# Tests can never write to the real repo: an exported GIT_DIR (or GIT_WORK_TREE, GIT_INDEX_FILE, GIT_COMMON_DIR) is dropped before any test runs, so git -C <temp repo> can't land on the project's .git (at 02:54 the real .git/config got bare=true and user t@example.com, and every merge failed)
## Raw request
> Tests can never write to the real repo: an exported GIT_DIR (or GIT_WORK_TREE, GIT_INDEX_FILE, GIT_COMMON_DIR) is dropped before any test runs, so git -C <temp repo> can't land on the project's .git (at 02:54 the real .git/config got bare=true and user t@example.com, and every merge failed)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] With GIT_DIR pointing at a real repo, the test helpers' git_repo() and a git init --bare in a test leave that repo's config untouched, because the test harness strips GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_COMMON_DIR and GIT_OBJECT_DIRECTORY from its environment at import — verify with `python3 plugin/tests/run.py test_helpers_env`
- [x] sampo doctor fails loudly when a project with a working tree has core.bare=true in its .git/config, naming the fix — verify with `python3 plugin/tests/run.py test_integrity`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce the leak in scratch repos, then a failing test
2. [x] strip the variables in helpers.py at import, and the doctor check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_helpers_env` → ✗ exit 1 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: GitEnvIsolation 0s) / FAILED (1 classes: test_helpers_env.GitEnvIsolation) [ran] [tree 0af17dcf7e1e] [world 2f1906870a] (2026-11-05T09:07:13Z)
- (step 2) `python3 plugin/tests/run.py test_integrity test_helpers_env test_doctor` → exit 0 · Ran 122 tests in 6.7s (45 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 5s, Command 3s) / OK [ran] [tree 6b7340951e1c] [world 2f1906870a] (2026-11-05T09:08:51Z)
- `python3 plugin/tests/run.py test_integrity test_helpers_env` → ✗ exit 1 · Ran 10 tests in 2.4s (3 classes, 16 at a time; slowest: Check 1s, Repair 0s, GitEnvIsolation 0s) / FAILED (1 classes: test_integrity.Check) (start tree + this task's tests) [ran] [tree 6b7340951e1c] [world 2f1906870a] (2026-11-05T09:08:55Z)
- `python3 plugin/tests/run.py test_integrity test_helpers_env` → exit 0 · Ran 10 tests in 1.1s (3 classes, 16 at a time; slowest: Check 1s, Repair 0s, GitEnvIsolation 0s) / OK [ran] [tree 6b7340951e1c] [world 2f1906870a] (2026-11-05T09:08:55Z)
- (ac 1) `python3 plugin/tests/run.py test_helpers_env` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: GitEnvIsolation 0s) / OK [ran] [tree 532c9dc81da2] [world 2f1906870a] (2026-11-05T09:09:09Z)
- (ac 2) `python3 plugin/tests/run.py test_integrity` → exit 0 · Ran 8 tests in 1.1s (2 classes, 16 at a time; slowest: Check 1s, Repair 0s) / OK [ran] [tree 532c9dc81da2] [world 2f1906870a] (2026-11-05T09:09:09Z)
- (step 1) `python3 plugin/tests/run.py test_helpers_env` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: GitEnvIsolation 0s) / OK [ran] [tree 532c9dc81da2] [world 2f1906870a] (2026-11-05T09:09:09Z)
- (audit adversary) `self: one place strips the redirecting GIT_ variables, the helpers module every test imports, so all scratch-repo git calls and their child processes are isolated; doctor reads core.bare with --git-dir so the broken flag can't hide; the real repo was restored (bare=false, repo-level fixture identity removed, backup kept in the scratchpad) and no commit was made under the fixture identity` → reproduced the leak in scratch repos (GIT_DIR set: git -C <scratch> config wrote into the other repo); with the fix the same run leaves it untouched; a test that sets GIT_DIR on purpose for one subprocess still can (it passes env=), only inherited values are dropped [tree 532c9dc81da2] (2026-11-05T09:09:09Z)
- (audit edge) `self: one place strips the redirecting GIT_ variables, the helpers module every test imports, so all scratch-repo git calls and their child processes are isolated; doctor reads core.bare with --git-dir so the broken flag can't hide; the real repo was restored (bare=false, repo-level fixture identity removed, backup kept in the scratchpad) and no commit was made under the fixture identity` → GIT_EDITOR and other non-redirecting GIT_ variables stay; a non-git root is skipped by the doctor check [tree 532c9dc81da2] (2026-11-05T09:09:09Z)
- (audit self) `self: one place strips the redirecting GIT_ variables, the helpers module every test imports, so all scratch-repo git calls and their child processes are isolated; doctor reads core.bare with --git-dir so the broken flag can't hide; the real repo was restored (bare=false, repo-level fixture identity removed, backup kept in the scratchpad) and no commit was made under the fixture identity` → no findings [tree 532c9dc81da2] (2026-11-05T09:09:09Z)
## Log
- 2026-11-05T09:06:39Z created
- 2026-11-05T09:06:40Z focused
- 2026-11-05T09:08:39Z criterion 2 verify: `python3 plugin/tests/run.py test_doctor` → `python3 plugin/tests/run.py test_integrity`
- 2026-11-05T09:08:39Z criterion 2 text: sampo doctor fails loudly when a project with a working tree has core.bare=true, or when its repo config holds the test identity t@example.com → sampo doctor fails loudly when a project with a working tree has core.bare=true in its .git/config, naming the fix
- 2026-11-05T09:09:31Z done
- 2026-11-05T09:09:34Z committed a2ec3766 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research T-0291-review-1: Changes needed. Fix 2 (the `confirm` flag) can be bypassed by the working session itself, and fix 3 has one gap that runs a planted driver. [st…
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
## Plan gaps
- failed first: step 1 reproduce the leak in scratch repos, then a failing test
## Files touched
- plugin/tests/test_helpers_env.py
- plugin/tests/helpers.py
- plugin/tests/test_integrity.py
- plugin/lib/sampo/doctor.py
- CHANGELOG.md
