---
id: T-1371
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T07:49:17Z
updated: 2026-10-21T13:37:08Z
base: 92a1746057410c739a5ec8fc6ac9e718797f3845
base_tree: 40280250167512c77dd1bbf3d3298bc795f6f43a
plan0_at: 2026-10-21T07:49:19Z
plan0_scope: []
verified: strong
---
# Remove the stray --check/ site build T-1330 committed; site/build.py refuses an option as its output folder
## Raw request
> Remove the stray --check/ site build T-1330 committed; site/build.py refuses an option as its output folder
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no file under --check/ is tracked, and python3 site/build.py --check exits 2 saying it takes an output folder, writing nothing — verify with `test -z "$(git ls-files -- ./--check)" && ! python3 site/build.py --check 2>/dev/null && test ! -e ./--check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] site/build.py: an argument starting with - is refused (exit 2)
2. [x] git rm the --check/ folder
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 48 tests in 1.8s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d6cf6a68b4d6] (2026-10-21T13:36:39Z)
- `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 48 tests in 1.3s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree d6cf6a68b4d6] (2026-10-21T13:36:39Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 48 tests in 1.3s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree d6cf6a68b4d6] (2026-10-21T13:36:43Z)
- (step 2) `test -z "$(git ls-files -- ./--check)" && ! python3 site/build.py --check 2>/dev/null && test ! -e ./--check` → exit 0 · (no output) [ran] [tree cc59015e65a1] (2026-10-21T13:36:52Z)
- (ac 1) `test -z "$(git ls-files -- ./--check)" && ! python3 site/build.py --check 2>/dev/null && test ! -e ./--check` → exit 0 · (no output) [ran] [tree cc59015e65a1] (2026-10-21T13:36:58Z)
- (audit edge) `self: build.py refuses any first argument starting with -, exit 2, before safe_out or any write; the 34 stray files are removed` → a real folder named with a leading dash can still be given as ./-name [tree cc59015e65a1] (2026-10-21T13:36:58Z)
- (audit self) `self: build.py refuses any first argument starting with -, exit 2, before safe_out or any write; the 34 stray files are removed` → no findings [tree cc59015e65a1] (2026-10-21T13:36:58Z)
- (audit edge) `self: build.py refuses any first argument starting with -, exit 2, before safe_out or any write; the 34 stray files are removed` → a real folder named with a leading dash can still be given as ./-name [tree cc59015e65a1] (2026-10-21T13:37:05Z)
- (audit adversary) `self: build.py refuses any first argument starting with -, exit 2, before safe_out or any write; the 34 stray files are removed` → the removed files are generated copies of site pages (guard.html, permissions.html among them); the sources in site/ are untouched and the real site builds to _site [tree cc59015e65a1] (2026-10-21T13:37:05Z)
- (audit self) `self: build.py refuses any first argument starting with -, exit 2, before safe_out or any write; the 34 stray files are removed` → no findings [tree cc59015e65a1] (2026-10-21T13:37:05Z)
## Log
- 2026-10-21T07:49:17Z created
- 2026-10-21T07:49:18Z focused
- 2026-10-21T13:36:49Z user approved core in Claude Code's permission prompt
- 2026-10-21T13:36:58Z scope: --check/ (removed), plugin/tests/test_docs.py
- 2026-10-21T13:37:07Z done
- 2026-10-21T13:37:08Z committed 070e9e9f (36 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-1321 [FEATURE S, done, 1 steps] Release 1.2.46: fm code takes any request, real examples on the site, linked state folders
- T-0833 [FEATURE S, done, 1 steps] Fm lane rm: offer to delete the lane's ignored build output (target/, voltc/target/) itsel — lesson: git status --ignored collapses a f…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–5 steps
## Lessons
- A script that takes a bare positional path must refuse option-looking arguments; one guessed flag became a folder that got committed
## Files touched
- site/build.py
- plugin/tests/test_docs.py
- --check/assets/code-tui.svg
- --check/assets/examples/docs.svg
- --check/assets/examples/feature.svg
- --check/assets/examples/fix.svg
- --check/assets/examples/javascript.svg
- --check/assets/examples/new-project.svg
- --check/assets/examples/question.svg
- --check/assets/examples/rename.svg
- --check/assets/foreman.svg
- --check/assets/poster.jpg
- --check/data/bench.json
- --check/data/stats.json
- --check/demo/code-tui.mp4
- --check/demo/demo.svg
- --check/demo/live.mp4
- --check/features/benchmarks.html
- --check/features/cards.html
- --check/features/code.html
- --check/features/drive.html
- --check/features/guard.html
- --check/features/index.html
- --check/features/lanes.html
- --check/features/learning.html
- --check/features/panel.html
- --check/features/permissions.html
- --check/features/planning.html
- --check/features/proof.html
- --check/features/releases.html
