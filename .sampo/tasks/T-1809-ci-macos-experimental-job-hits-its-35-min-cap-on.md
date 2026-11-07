---
id: T-1809
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T04:42:00Z
updated: 2026-10-28T08:08:12Z
group: CI and release pipeline gates
base: 0cfc428f6a0f12c3200f090592579ba140ecc6b7
base_tree: 8ecfad6bdd2d1c3648abde00571e3339a89fb901
plan0_at: 2026-10-28T07:56:21Z
plan0_scope: []
verified: strong
---
# CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest classes as public notices
## Raw request
> CI macOS (experimental) job hits its 35-min cap on be5743a6 (21.4 min before): find whether a class hangs past run.py's 480 s kill or the runner is slow; annotations show only the job timeout
## Interpretation
macOS has timed out at 35 min on every main run since b652c6e5 (2026-10-21; its last pass fba623d0 took 26 min), even with T-1808's 480 s class kill (be5743a6). Annotations print only at the end, so a job-level timeout leaves none, and logs need a login. Ubuntu takes 15 of its 20 min.
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py --deadline S kills classes still running at S with their stacks, fails unstarted ones as not started, and exits 1 — verify with `python3 plugin/tests/run.py test_run test_ci_annotations`
- [x] On GitHub Actions the summary (time, 5 slowest classes) prints as a ::notice, and a ::warning when the run used over 75% of its deadline — verify with `python3 plugin/tests/run.py test_ci_annotations`
- [x] The workflow passes --deadline below each job's timeout-minutes — verify with `grep -E 'run.py --deadline' .github/workflows/test.yml`
## Non-goals
## Approach (options → choice → why)
Options: (a) raise the macOS cap to 60 min: hides the cause; (b) drop macOS: loses the signal; (c) a run-wide deadline in run.py below the job cap, so the run ends itself and prints its annotations: chosen, because it turns a silent cancel into named classes and also guards Ubuntu's shrinking headroom; (d) emit annotations live per class: kept as the fallback if (c)'s output is still cut.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: deadline kill/not-started, CI notice and 75% warning
2. [x] run.py --deadline; per-class timeout = min(timeout, time left); notices on CI
3. [x] Workflow: --deadline 1920 on macOS (35 min cap), 1080 on Ubuntu (20 min)
4. [x] After the push: read the macOS job's annotations, name the slow or hung class, fix it or capture it
## Resume here
<!-- auto -->
- 2026-10-28T08:05:43Z steps 4/4 done
- git: foreman/build; 5 uncommitted: .github/workflows/test.yml, CHANGELOG.md, plugin/tests/run.py, plugin/tests/test_ci_annotations.py, plugin/tests/test_run.py
- touched since last checkpoint: plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/triage1798.md
- failures met: jq: error (at ideas.json:0): null (null) has no keys
## Docs impact
CHANGELOG Unreleased entry; run.py docstring and --deadline help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run test_ci_annotations` → exit 0 · Ran 52 tests in 4.6s (31 classes, 16 at a time; slowest: Hang 4s, Bench 3s, TimeoutWithoutProc 2s) / OK [ran] [tree 7c7226187848] (2026-10-28T07:57:49Z)
- (step 2) `python3 plugin/tests/run.py test_run test_ci_annotations test_parallel` → exit 0 · Ran 67 tests in 21.9s (34 classes, 16 at a time; slowest: Parallel 22s, Hang 4s, Bench 3s) / OK [ran] [tree 7c7226187848] (2026-10-28T07:58:11Z)
- (step 3) `grep -E 'run.py --deadline' .github/workflows/test.yml` → exit 0 · run: python3 plugin/tests/run.py --deadline ${{ matrix.experimental && 1920 || 1080 }}  # ends below the job cap, naming what was slow (T-1809) [ran] [tree 7c7226187848] (2026-10-28T07:58:12Z)
- (step 4) `grep -n "deadline - t0 < 1" -A8 plugin/tests/run.py` → exit 0 · 80-    extra = [a for x in k for a in ("-k", x)] / 81-    p = subprocess.Popen([sys.executable, "-X", "faulthandler", "-m", "unittest", "-q", cid, *extra], cwd=HERE, [ran] [tree d8fcf8b23336] (2026-10-28T08:01:55Z)
- (ac 1) `python3 plugin/tests/run.py test_run test_ci_annotations` → exit 0 · Ran 53 tests in 4.6s (31 classes, 16 at a time; slowest: Hang 4s, Bench 3s, Timeout 2s) / OK [ran] [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 4 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (ac 3) `grep -E 'run.py --deadline' .github/workflows/test.yml` → exit 0 · run: python3 plugin/tests/run.py --deadline ${{ matrix.experimental && 1980 || 1380 }}  # ends below timeout-minutes, naming what was slow (T-1809) [ran] [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (audit intent) `one fm-reviewer pass; all 8 findings fixed test-first` → CI now ends itself 2 min under each job cap and names running and unstarted classes, slowest five as a public notice [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (audit edge) `one fm-reviewer pass; all 8 findings fixed test-first` → deadline under 1 s left → not started; --deadline 0 refused; kill message names the deadline, not the 480 s cap [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (audit operator) `one fm-reviewer pass; all 8 findings fixed test-first` → Ubuntu cap 20→25 min (790–934 s suite, cancelled runs hit 1200 s); macOS 35 min with a 1980 s deadline [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (audit maintainer) `one fm-reviewer pass; all 8 findings fixed test-first` → cost at scale — 3 annotation lines per push, no extra runs; shared slowest() helper [tree 5724f740e608] (2026-10-28T08:07:36Z)
- (audit adversary) `one fm-reviewer pass; all 8 findings fixed test-first` → no input crosses a trust boundary; annotations carry only class names and times [tree 5724f740e608] (2026-10-28T08:07:36Z)
- `python3 plugin/tests/run.py test_run` → exit 0 · Ran 49 tests in 5.3s (29 classes, 16 at a time; slowest: Hang 4s, Bench 3s, TimeoutWithoutProc 2s) / OK (start tree + this task's tests) [ran] [tree 5724f740e608] (2026-10-28T08:07:55Z)
- `python3 plugin/tests/run.py test_run` → exit 0 · Ran 49 tests in 4.6s (29 classes, 16 at a time; slowest: Hang 4s, Bench 3s, Timeout 2s) / OK [ran] [tree 5724f740e608] (2026-10-28T08:07:55Z)
- (audit intent) `one fm-reviewer pass; all 8 findings fixed test-first` → CI now ends itself 2 min under each job cap and names running and unstarted classes, slowest five as a public notice [tree 5724f740e608] (2026-10-28T08:08:04Z)
- (audit edge) `one fm-reviewer pass; all 8 findings fixed test-first` → deadline under 1 s left → not started; --deadline 0 refused; kill message names the deadline, not the 480 s cap [tree 5724f740e608] (2026-10-28T08:08:04Z)
- (audit operator) `one fm-reviewer pass; all 8 findings fixed test-first` → Ubuntu cap 20→25 min (790–934 s suite, cancelled runs hit 1200 s); macOS 35 min with a 1980 s deadline [tree 5724f740e608] (2026-10-28T08:08:04Z)
- (audit maintainer) `one fm-reviewer pass; all 8 findings fixed test-first` → cost at scale — 3 annotation lines per push, no extra runs; shared slowest() helper [tree 5724f740e608] (2026-10-28T08:08:04Z)
- (audit adversary) `one fm-reviewer pass; all 8 findings fixed test-first` → no input crosses a trust boundary; annotations carry only class names and times [tree 5724f740e608] (2026-10-28T08:08:04Z)
## Log
- 2026-10-28T04:42:00Z created
- 2026-10-28T07:55:16Z planned from capture
- 2026-10-28T07:56:20Z focused
- 2026-10-28T08:03:50Z steer: review fixes — deadline wording, <1s left = not started, --deadline 0 refused, unstarted named on stderr, main() tested; root cause of a test-only miss: run.classes used unittest's shared loader, which -k filters; Ubuntu cap 20→25 min (suite 790-934 s)
- 2026-10-28T08:08:10Z done
- 2026-10-28T08:08:12Z committed 06bd383a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1808 [FIX S, done, 1 steps] run.py kills a test class that hangs and names it with its stack: CI's 20-min job cap hid where — lesson: a CI job cap kills the run before…
- research mission-20261028-025205.pack: Recursive brainstorm/build rounds after the weekly reset: make Foreman insanely good, not just specific to usage; reason ahead in …
- research mission-20261028-025205: Request: Recursive brainstorm/build rounds after the weekly reset: make Foreman insanely good, not just specific to usage; reason ahead…
- decision 2026-10-04: Friction pass deferred to the next day
- the similar finished task took 1 steps
- start here (files T-1808 touched): plugin/tests/test_run.py, plugin/tests/run.py
## Why not caught
none: the job cap killed the run before run.py could report; T-1810's session sweep now flags CI red on main
## Regression test
test_run.Hang (deadline kill, not-started, main's exit and notes) and test_ci_annotations.SummaryNotes. fm task prove can't show red: run.py lives under plugin/tests/, so prove carries the fixed run.py onto the start tree as a test file.
## Lessons
- unittest -k sets testNamePatterns on the shared defaultTestLoader: discovery inside a filtered run must use its own TestLoader()
## Files touched
- plugin/tests/test_ci_annotations.py
- plugin/tests/test_run.py
- plugin/tests/run.py
- .github/workflows/test.yml
- CHANGELOG.md
