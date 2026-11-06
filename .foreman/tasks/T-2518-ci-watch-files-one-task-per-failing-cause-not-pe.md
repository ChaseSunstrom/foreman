---
id: T-2518
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmci.py, plugin/lib/fmeco.py, plugin/tests/test_ci_watch.py, plugin/tests/test_eco.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T00:21:22Z
updated: 2026-11-02T02:18:48Z
base: e916a8dbca7966fd2fbada5a041884a88e61451c
base_tree: 5ab2aa26cabb15fe4d08e5968e7c02ceb7ca4493
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T02:04:14Z
plan0_scope: [plugin/lib/fmci.py, plugin/lib/fmeco.py, plugin/tests/test_ci_watch.py, plugin/tests/test_eco.py, CHANGELOG.md]
verified: strong
---
# ci-watch files one task per failing cause while it's open, not one per run
## Raw request
> ci-watch files one task per failing cause, not per run: its capture key is the run URL, so each new commit failing the same tests filed a new FIX (T-2462 got 9 duplicates on 2026-11-01, T-2441 3; this session T-2510/T-2512/T-2514). Key by the failing test classes or jobs in the log (e.g. 'classes failed: test_exam.LanesKind'), append the new run to the open task, file anew only for a new failing set
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two CI runs failing the same test classes on one branch file one FIX while it is open (the second run is logged on it); after that task closes, the same failure files a new one; a run whose log names no failing class keys by its URL as before — verify with `python3 plugin/tests/run.py test_ci_watch test_eco`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: _brief twice with two run ids and the same 'classes failed: test_exam.LanesKind' tail → one open task with a 'CI again: run N' log line; drop it, a third run files a new task; a tail with no class line files per URL
2. [x] fmci._brief: a 'CI cause: <branch>: <sorted classes>' line from the tail as the key, with capture_once's new open_only flag (key dedupe against open briefs only); log the run on the open task; Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_watch.CiCause` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: CiCause 0s) / FAILED (1 classes: test_ci_watch.CiCause) [ran] [tree cfcbd15c2598] [world 2f1906870a] (2026-11-02T02:04:43Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch.CiCause` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CiCause 0s) / OK [ran] [tree 44ebf1799029] [world 2f1906870a] (2026-11-02T02:06:25Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch test_eco` → exit 0 · Ran 40 tests in 3.9s (12 classes, 16 at a time; slowest: HarnessCanary 4s, CiWatch 3s, Sweep 1s) / OK [ran] [tree 44ebf1799029] [world 2f1906870a] (2026-11-02T02:06:30Z)
- `python3 plugin/tests/run.py test_ci_watch.CiCause` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: CiCause 0s) / FAILED (1 classes: test_ci_watch.CiCause) (start tree + this task's tests) [ran] [tree 44ebf1799029] [world 2f1906870a] (2026-11-02T02:06:32Z)
- `python3 plugin/tests/run.py test_ci_watch.CiCause` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CiCause 0s) / OK [ran] [tree 44ebf1799029] [world 2f1906870a] (2026-11-02T02:06:32Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch test_eco` → exit 0 · Ran 40 tests in 3.9s (12 classes, 16 at a time; slowest: HarnessCanary 4s, CiWatch 3s, Sweep 1s) / OK [ran] [tree 45c0209d236a] [world 2f1906870a] (2026-11-02T02:12:32Z)
- (audit edge) `self-review: the log/annotation read moved out of _brief into _tail (one read per run, shared by the join and the brief); _cause keys by the sorted test classes run.py names, else by named failing jobs, else None (per-run, as before); _join_or_brief joins an open brief with the same key (logging the run) or files a new one carrying the key; both the non-blocking and the blocking path use it; capture_once's URL key still stops the same run filing twice` → two shards failing one class join; a closed task's cause files anew; unnamed jobs with no class line file per run (the logged-out test); the CI log stays untrusted text (defang, redact, plain) [tree 45c0209d236a] (2026-11-02T02:12:32Z)
- (audit self) `self-review: the log/annotation read moved out of _brief into _tail (one read per run, shared by the join and the brief); _cause keys by the sorted test classes run.py names, else by named failing jobs, else None (per-run, as before); _join_or_brief joins an open brief with the same key (logging the run) or files a new one carrying the key; both the non-blocking and the blocking path use it; capture_once's URL key still stops the same run filing twice` → no findings [tree 45c0209d236a] (2026-11-02T02:12:32Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 2b66c3b16334] [world 2f1906870a] (2026-11-02T02:13:19Z)
## Log
- 2026-11-02T00:21:22Z created
- 2026-11-02T00:21:48Z planned from capture
- 2026-11-02T02:04:13Z focused
- 2026-11-02T02:04:14Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T02:06:14Z hypothesis: the remaining failures are (a) my test's runs used a headSha that isn't the repo head, so watch skipped them, (b) test_always_failing_gives_up_at_the_cap asserts one brief per run, the behaviour this task changes, (c) unnamed jobs keyed as 'None' merged distinct runs; fixed (c) in code, (a) in the test; (b) needs its expectation updated
- 2026-11-02T02:06:24Z ruled out (b): the cap test's fake jobs carry no names and its log no class line, so each run keeps its own brief and its expectation stands
- 2026-11-02T02:06:33Z scope: CHANGELOG.md entry; capture_once untouched (the join already matches open briefs only)
- 2026-11-02T02:12:49Z done
- 2026-11-02T02:12:52Z committed 97599336 (3 files)
- 2026-11-02T02:13:20Z guard authorization added: publish
- 2026-11-02T02:18:48Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2013 [FIX S, done, 1 steps] CI watch reruns a job that never got a runner instead of filing a FIX — lesson: A CI watcher must tell infrastructure cancels (no steps ran…
- T-2468 [FIX S, done, 1 steps] fm ci-watch reuses the open or blocked FIX brief that already names the same failing jobs, logging the new commit on it, instead of filing …
- research T-1939-review: Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP. …
- decision 2026-10-31: Mission 6's install-grant queue is the capability-miss captures (one durable task per missing tool, filed once ever by the hook, the tool rung and t…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-02): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
T-2468's join test used one job name on both runs and only the non-blocking path; the blocking path had no join at all, and shard numbers in job names split one cause in two (T-2512 and T-2514 this session).
## Lessons
- Key a failure by what failed (the test), not by where it ran (the run, the shard); the where changes every push
## Plan gaps
- failed first: step 1 red test: _brief twice with two run ids and the same 'classes failed: test_exam.LanesKind' tail → o…
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- CHANGELOG.md
