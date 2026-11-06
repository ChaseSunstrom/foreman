---
id: T-0412
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:53:55Z
updated: 2026-10-09T04:59:25Z
base: 78aaba75a89dc5e73d61ec4d883c17b831a3f7d1
base_tree: 6db41cbf723cb38b53d043725cde405432c4af65
verified: strong
---
# Guard: rm of a symlink removes the link, not its target (JARVIS builder: rm jarvis-web/node_modules — a link to the main checkout — refused as confine)
## Raw request
> Guard: rm of a symlink removes the link, not its target (JARVIS builder: rm jarvis-web/node_modules — a link to the main checkout — refused as confine)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] rm/unlink of a symlink without a trailing slash is judged by the link's path; rm -r link/ and writes through the link still refuse — verify with `python3 plugin/tests/run.py -k test_removing_a_symlink_judges_the_link`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then classify the link's own path
## Resume here
<!-- auto -->
- 2026-10-09T04:57:07Z step 1/1: test-first, then classify the link's own path
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md, plugin/tests/test_hooks.py
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_removing_a_symlink_judges_the_link` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SymlinkRemoval 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 02da51f2f0a3] (2026-10-09T04:54:14Z)
- `python3 plugin/tests/run.py -k test_removing_a_symlink_judges_the_link` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SymlinkRemoval 0s) / OK [ran] [tree 02da51f2f0a3] (2026-10-09T04:54:14Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 944 tests in 35.9s (233 classes, 16 at a time; slowest: Stop 24s, TaskLifecycle 21s, Parallel 18s) / FAILED (1 classes) [ran] [tree 4d75afc91949] (2026-10-09T04:56:18Z)
- (step 1) `python3 plugin/tests/run.py -k test_removing_a_symlink_judges_the_link` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SymlinkRemoval 0s) / OK [ran] [tree 165d79def478] (2026-10-09T04:58:54Z)
- (ac 1) `python3 plugin/tests/run.py -k test_removing_a_symlink_judges_the_link` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SymlinkRemoval 0s) / OK [ran] [tree 165d79def478] (2026-10-09T04:59:25Z)
- (audit adversary) `self: diff read; classify_unlink only for rm targets without a trailing slash, every other write path still resolves realpath; test red→green` → rm link/ and rm link/* still follow the link (tested); a link whose own path is in state or core is still judged by that path [tree 165d79def478] (2026-10-09T04:59:25Z)
- (audit edge) `self: diff read; classify_unlink only for rm targets without a trailing slash, every other write path still resolves realpath; test red→green` → dangling link judged by its own path; non-link rm unchanged (islink false → real=True) [tree 165d79def478] (2026-10-09T04:59:25Z)
- (audit self) `self: diff read; classify_unlink only for rm targets without a trailing slash, every other write path still resolves realpath; test red→green` → no findings [tree 165d79def478] (2026-10-09T04:59:25Z)
## Log
- 2026-10-09T04:53:55Z created
- 2026-10-09T04:53:55Z focused
- 2026-10-09T04:57:06Z scope: test_a_broken_working_copy_of_the_guard_falls_back_to_the_committed_one breaks the guard by replacing the text 'def classify_write(path, ctx):'; the signature now has real=True, so its anchor follows
- 2026-10-09T04:59:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0386 [FIX S, done, 1 steps] FIX: the guard refuses writes to secret-name templates (jarvis-core/config/secrets.yaml.ex
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–1 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- plugin/tests/test_hooks.py
