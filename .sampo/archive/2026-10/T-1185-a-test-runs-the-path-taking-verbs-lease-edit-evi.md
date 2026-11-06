---
id: T-1185
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:48:39Z
base: a7c61effacb70497f7d3fb6684840466491c2c4e
base_tree: 5081d10ba1235d0acce4ce7c25160d2672d9c7be
plan0_at: 2026-10-16T13:23:30Z
plan0_scope: []
verified: strong
---
# A test runs the path-taking verbs (lease, edit, evidence, check, focus) from a subdirector
## Raw request
> FEATURE: A test runs the path-taking verbs (lease, edit, evidence, check, focus) from a subdirectory and through a symlinked checkout and holds each to the same result as from the repo root.
> DONE-WHEN: `python3 plugin/tests/run.py -k subdir_matrix` passes with each verb run from root, a subdirectory and a symlink.
## Interpretation
Path bugs keep shipping (T-1148: a lease path from a subdirectory doubled; T-1165: a --file read from the root instead of the cwd). A test matrix runs the path-taking verbs (fm lease take/drop, fm edit, fm task evidence --run with a relative path, fm check --affected, fm focus, fm inbox spec, fm guard wrong, fm intake --file) from the repo root, a subdirectory, and through a symlink to the checkout, and holds each to the same result as from the root. Real bugs it finds are fixed in the same task (each a red row first).
## Assumptions (confidence)
## Acceptance criteria
- [x] each listed verb gives the same result from the root, a subdirectory and a symlinked checkout; any bug found is fixed with its row red first — verify with `python3 plugin/tests/run.py test_subdir_matrix`
## Non-goals
## Approach (options → choice → why)
Options: (a) one parametrised test module (test_subdir_matrix.py) with a helper that runs a verb from each of the three places and compares a normalised result (state written, files changed, output paths); (b) per-verb tests scattered in their modules (no single place showing coverage); (c) property-based fuzzing of paths (overkill). Choice: (a). Fix found bugs at the root cause (the shared path helper), not per verb.
## Risks and rollback
## Execution prompt
## Steps
1. [x] The matrix test (test_subdir_matrix.py); record which rows fail
2. [x] Fix each failing row at its shared path helper
## Resume here
## Docs impact
none: test only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k subdir_matrix` → exit 0 · Ran 8 tests in 26.1s (1 classes, 16 at a time; slowest: SubdirMatrix 26s) / OK [ran] [tree bcbf7458f14d] (2026-10-16T13:28:21Z)
- (step 2) `python3 plugin/tests/run.py -k subdir_matrix` → exit 0 · Ran 8 tests in 15.4s (1 classes, 16 at a time; slowest: SubdirMatrix 15s) / OK [ran] [tree 23b1ff4a80b1] (2026-10-16T13:28:37Z)
- (ac 1) `python3 plugin/tests/run.py test_subdir_matrix` → exit 0 · Ran 8 tests in 8.0s (1 classes, 16 at a time; slowest: SubdirMatrix 8s) / OK [ran] [tree fd472f89aa4d] (2026-10-16T13:37:07Z)
- (ac 1) `python3 plugin/tests/run.py test_subdir_matrix` → exit 0 · Ran 8 tests in 69.5s (1 classes, 16 at a time; slowest: SubdirMatrix 68s) / OK [ran] [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
- (audit intent) `self: reviewed the merged test; rows compare root vs subdir vs symlink results per verb; its one side effect (guard wrong writing the real corpus) fixed in T-1197` → covers lease, edit, evidence, check, focus and the other path-taking verbs from root, subdirectory and symlink as asked [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
- (audit adversary) `self: reviewed the merged test; rows compare root vs subdir vs symlink results per verb; its one side effect (guard wrong writing the real corpus) fixed in T-1197` → test-only; no guard or state code changed [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
- (audit edge) `self: reviewed the merged test; rows compare root vs subdir vs symlink results per verb; its one side effect (guard wrong writing the real corpus) fixed in T-1197` → symlinked checkout and nested subdirectory rows included; the corpus leak was the only edge found, fixed in T-1197 [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
- (audit operator) `self: reviewed the merged test; rows compare root vs subdir vs symlink results per verb; its one side effect (guard wrong writing the real corpus) fixed in T-1197` → runs in about 8 s, isolated temp repos, no real state [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
- (audit maintainer) `self: reviewed the merged test; rows compare root vs subdir vs symlink results per verb; its one side effect (guard wrong writing the real corpus) fixed in T-1197` → one table-driven test file; a new path-taking verb is one row [tree 1dd8c405acfb] (2026-10-16T13:46:39Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T13:23:19Z set tier=M
- 2026-10-16T13:23:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1185.builder.md
- 2026-10-16T13:23:30Z focused
- 2026-10-16T13:36:55Z merged worktree-agent-aa3871f99b0aabebd (1 file(s))
- 2026-10-16T13:43:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa3871f99b0aabebd
- 2026-10-16T13:45:12Z focused
- 2026-10-16T13:45:26Z scope: CHANGELOG line
- 2026-10-16T13:48:38Z done
- 2026-10-16T13:48:39Z committed a1337031 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1148 [FIX S, done, 1 steps] Fm lease take with a path relative to the repo root from a subdirectory records a doubled — lesson: Resolve a user's path the way they most…
- T-1125 [FIX S, done, 1 steps] Guard false positive: a command 'cd ROOT && python3 heredoc writing CHANGELOG.md (relative — lesson: Before calling a guard block a false p…
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Lessons
- A matrix test of cwd variants must isolate every env-driven output path, not just FOREMAN_HOME: guard wrong's corpus fell back to the real checkout
## Files touched
- plugin/tests/test_subdir_matrix.py
- plugin/tests/fixtures/guard_cases.jsonl
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/skills/playbooks/references/release/release-and-changelog.md
- plugin/tests/helpers.py
- plugin/tests/test_guard_cases.py
- plugin/tests/test_release.py
- plugin/tests/test_release_py.py
- release.py
