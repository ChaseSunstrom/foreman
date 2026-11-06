---
id: T-2058
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmci.py, plugin/tests/test_ci_watch.py]
depends_on: []
source: discovered
created: 2026-10-29T21:39:31Z
updated: 2026-10-29T21:41:10Z
base: ee079813598e28b55bce242d6a144705bd102278
base_tree: 94fc960426baa3145652c903334d0a3519a8d46c
plan0_at: 2026-10-29T21:39:38Z
plan0_scope: [plugin/lib/fmci.py, plugin/tests/test_ci_watch.py]
verified: strong
---
# fm ship --watch / ci-watch says CI green from the first workflow run of a commit (pages)…
## Raw request
> FIX: fm ship --watch / ci-watch says CI green from the first workflow run of a commit (pages) while another (tests) failed: wait for every workflow's newest run
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a commit is green only when every workflow's newest run passed; a failed one is briefed — verify with `python3 plugin/tests/run.py test_ci_watch test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] per-workflow runs in fmci._latest; watch decides on a failed, then a running, then a green run
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 8 tests in 2.6s (1 classes, 16 at a time; slowest: CiWatch 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a3f9f9b6f4fc] (2026-10-29T21:39:52Z)
- `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 8 tests in 1.8s (1 classes, 16 at a time; slowest: CiWatch 2s) / FAILED (1 classes) [ran] [tree a3f9f9b6f4fc] (2026-10-29T21:39:52Z)
- `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 8 tests in 2.6s (1 classes, 16 at a time; slowest: CiWatch 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1ac9cd4e7113] (2026-10-29T21:40:19Z)
- `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 8 tests in 1.8s (1 classes, 16 at a time; slowest: CiWatch 2s) / OK [ran] [tree 1ac9cd4e7113] (2026-10-29T21:40:19Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch test_ship` → exit 0 · Ran 25 tests in 11.4s (2 classes, 16 at a time; slowest: Ship 11s, CiWatch 2s) / OK [ran] [tree 1ac9cd4e7113] (2026-10-29T21:40:52Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch test_ship` → exit 0 · Ran 25 tests in 11.4s (2 classes, 16 at a time; slowest: Ship 11s, CiWatch 2s) / OK [ran] [tree 1ac9cd4e7113] (2026-10-29T21:41:04Z)
- (audit edge) `self: one function; dedupe keeps each workflow's newest run (gh lists newest first, the API too), decision order failed > running > green-with-failed-job > green; single-workflow repos and fakes without workflowName behave as before (all share None); the extra jobs query runs only with 2+ workflows and only once all are green` → a workflow GitHub registers seconds after the others could still be missed on the very first poll; both of this repo's start on the same push event at the same second [tree 1ac9cd4e7113] (2026-10-29T21:41:04Z)
- (audit self) `self: one function; dedupe keeps each workflow's newest run (gh lists newest first, the API too), decision order failed > running > green-with-failed-job > green; single-workflow repos and fakes without workflowName behave as before (all share None); the extra jobs query runs only with 2+ workflows and only once all are green` → no findings [tree 1ac9cd4e7113] (2026-10-29T21:41:04Z)
## Log
- 2026-10-29T21:39:31Z created
- 2026-10-29T21:39:36Z set tier=S, scope=['plugin/lib/fmci.py', 'plugin/tests/test_ci_watch.py']
- 2026-10-29T21:39:37Z planned: it has criteria and steps
- 2026-10-29T21:39:37Z focused
- 2026-10-29T21:41:08Z done
- 2026-10-29T21:41:10Z committed 1180bd04 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1942 [FIX S, done, 2 steps] Fm ci-watch says CI green when a non-blocking (continue-on-error) job failed: the run's co
- research T-1939-review: Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP. …
- T-1052 [FEATURE M, done, 3 steps] CI-watch loop: after a push, poll the run, turn a failure log into a fix brief, retry up t — lesson: A watcher of remote state must pin…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- similar finished tasks took 2–3 steps
## Why not caught
the fakes listed one run per commit; the repo gained a second workflow (pages) after the watcher was written
## Lessons
- A commit has one run per workflow: CI is green only when each workflow's newest run is
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
