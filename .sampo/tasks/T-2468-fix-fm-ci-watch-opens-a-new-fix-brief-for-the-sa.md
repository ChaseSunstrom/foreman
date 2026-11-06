---
id: T-2468
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-01T09:51:51Z
updated: 2026-11-01T17:19:49Z
base: 5b32e1efaa51b144d590a5d28e550bae27faeadb
base_tree: ce004deed49ed5d6c4915926711ee733512335ee
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T17:07:27Z
plan0_scope: []
verified: strong
---
# fm ci-watch reuses the open or blocked FIX brief that already names the same failing jobs, logging the new commit on it, instead of filing a duplicate each ship
## Raw request
> FIX: fm ci-watch opens a new FIX brief for the same failing non-blocking jobs on every ship (T-2462, T-2463, T-2467 for the macOS 3.14 pair); it should find the open or blocked brief naming those jobs and log the new commit on it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a second ci-watch run with the same failing jobs files no new brief and logs its commit on the existing one — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then reuse the brief that names the same jobs
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_green_run_with_a_failed_non_blocking_job_says_so_and_briefs_it_once test_ci_watch` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CiWatch 0s) / FAILED (1 classes: test_ci_watch.CiWatch) [ran] [tree ef1817debbe0] (2026-11-01T17:08:13Z)
- `python3 plugin/tests/run.py -k test_a_green_run_with_a_failed_non_blocking_job_says_so_and_briefs_it_once test_ci_watch` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: CiWatch 0s) / FAILED (1 classes: test_ci_watch.CiWatch) (start tree + this task's tests) [ran] [tree 00210eb04ada] (2026-11-01T17:08:40Z)
- `python3 plugin/tests/run.py -k test_a_green_run_with_a_failed_non_blocking_job_says_so_and_briefs_it_once test_ci_watch` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CiWatch 0s) / OK [ran] [tree 00210eb04ada] (2026-11-01T17:08:40Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch test_ship` → exit 0 · Ran 42 tests in 23.9s (2 classes, 16 at a time; slowest: Ship 24s, CiWatch 2s) / OK [ran] [tree 00210eb04ada] (2026-11-01T17:09:04Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 2.5s (1 classes, 16 at a time; slowest: CiWatch 2s) / OK [ran] [tree 0267db5199f9] (2026-11-01T17:09:22Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 2.4s (1 classes, 16 at a time; slowest: CiWatch 2s) / OK [ran] [tree 0267db5199f9] (2026-11-01T17:14:51Z)
- (audit intent) `main-thread lens pass over the fmci diff and the extended test` → a green run whose same non-blocking jobs fail again is logged on the open or blocked brief tagged with those jobs (meta ci_jobs = branch|sorted jobs) instead of a new brief; once that brief closes, a new failure files anew [tree 0267db5199f9] (2026-11-01T17:14:51Z)
- (audit edge) `main-thread lens pass over the fmci diff and the extended test` → a different set of failing jobs, or another branch, files its own brief; a blocked brief still collects runs; T-2462 predates the tag, so the next ship files one tagged brief and later runs join it [tree 0267db5199f9] (2026-11-01T17:14:51Z)
- (audit self) `main-thread lens pass over the fmci diff and the extended test` → no findings [tree 0267db5199f9] (2026-11-01T17:14:51Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 0267db5199f9] (2026-11-01T17:15:37Z)
## Log
- 2026-11-01T09:51:51Z created
- 2026-11-01T16:56:36Z planned from capture
- 2026-11-01T16:56:47Z criterion 1 verify: `python3 plugin/tests/run.py test_ci` → `python3 plugin/tests/run.py test_ci_watch`
- 2026-11-01T17:07:26Z focused
- 2026-11-01T17:07:27Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T17:09:19Z scope: plugin/lib/fmci.py, plugin/tests/test_ci_watch.py, CHANGELOG.md
- 2026-11-01T17:15:08Z done
- 2026-11-01T17:15:10Z committed 96aa091d (3 files)
- 2026-11-01T17:15:37Z guard authorization added: publish
- 2026-11-01T17:19:49Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2013 [FIX S, done, 1 steps] CI watch reruns a job that never got a runner instead of filing a FIX — lesson: A CI watcher must tell infrastructure cancels (no steps ran…
- T-1942 [FIX S, done, 2 steps] Fm ci-watch says CI green when a non-blocking (continue-on-error) job failed: the run's co
- research T-1939-review: Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP. …
- decision 2026-11-01: [cites: user steer 2026-10-31: finish round 1 completely, in order; no new maintenance or friction tasks until that's done unless they block a missi…
- similar finished tasks took 1–2 steps
## Lessons
- A dedupe key must name the failure, not the occurrence: a run URL changes every ship
## Plan gaps
- failed first: step 1 red test, then reuse the brief that names the same jobs
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- CHANGELOG.md
