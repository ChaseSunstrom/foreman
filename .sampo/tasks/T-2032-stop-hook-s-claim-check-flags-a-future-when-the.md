---
id: T-2032
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T19:04:21Z
updated: 2026-10-29T19:52:32Z
base: fdd9bc40438efb9456c5b2f88a26ce2d3603149b
base_tree: d8d7438e34eaf786e4f97d18847d2c733bc3f00a
plan0_at: 2026-10-29T19:43:01Z
plan0_scope: []
verified: strong
---
# Stop hook's claim check flags a future 'when the gates pass' as a claim, and counts a…
## Raw request
> Stop hook's claim check flags a future 'when the gates pass' as a claim, and counts a scratchpad draft (edit30.json) as an edit needing tests
## Interpretation
The Stop hook's 'tests pass' claim check (fmhooks._claims_gate) blocks a reply that only says when tests will pass ('once the gates pass'), and it treats an edit to a file outside the project (a scratchpad draft) as code edited after the last green run.
## Assumptions (confidence)
## Acceptance criteria
- [x] A conditional claim isn't blocked; an edit outside cwd doesn't make a green run stale; an edit inside still does — verify with `python3 plugin/tests/run.py test_hooks -k claim`
## Non-goals
## Approach (options → choice → why)
Options: (1) widen _NEG with conditionals - rejected, _NEG looks 40 chars back so 'when I ran it, the tests pass' would stop counting; (2) a separate tight regex for a conditional word right before the claim (12 chars) - chosen; (3) parse tense - overkill. For edits: count only edits whose absolute realpath is under the hook's cwd; relative paths still count.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: future-tense claim and an out-of-project edit don't block
2. [x] Fix _claims_gate: conditional regex and edits under cwd only
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k claim` → ✗ exit 1 · Ran 6 tests in 7.9s (1 classes, 16 at a time; slowest: Stop 7s) / FAILED (1 classes) [ran] [tree 4a1d4f9a97bf] (2026-10-29T19:43:16Z)
- `python3 plugin/tests/run.py test_hooks -k claim` → ✗ exit 1 · Ran 6 tests in 7.0s (1 classes, 16 at a time; slowest: Stop 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fbd9a6788180] (2026-10-29T19:44:17Z)
- `python3 plugin/tests/run.py test_hooks -k claim` → exit 0 · Ran 6 tests in 6.7s (1 classes, 16 at a time; slowest: Stop 6s) / OK [ran] [tree fbd9a6788180] (2026-10-29T19:44:17Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.5    30.1     150  [0] / SessionEnd                  25.8    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree fbd9a6788180] (2026-10-29T19:47:41Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks -k claim 2>&1 | tail -2` → exit 0 · OK [ran] [tree 052aa6d4c142] (2026-10-29T19:48:02Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.5    30.7     150  [0] / SessionEnd                  24.5    27.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 052aa6d4c142] (2026-10-29T19:51:37Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks -k claim` → exit 0 · Ran 6 tests in 6.7s (1 classes, 16 at a time; slowest: Stop 6s) / OK [ran] [tree 052aa6d4c142] (2026-10-29T19:51:54Z)
- (audit intent) `self-review of the diff: claim regex unchanged; a tight 12-char conditional check before a match; edits counted only under the cwd's git root` → 'once/when/if the gates pass' isn't a claim; a scratch draft outside the repo doesn't make a green run stale [tree 052aa6d4c142] (2026-10-29T19:51:54Z)
- (audit edge) `self-review of the diff: claim regex unchanged; a tight 12-char conditional check before a match; edits counted only under the cwd's git root` → 'when I ran it, the tests pass' still counts (12-char window, _NEG unchanged); relative paths still count; repo2 doesn't match repo/ (root + sep); a session cd'd into a subfolder still owns the whole repo (git_root, tested); no cwd keeps the old count-everything [tree 052aa6d4c142] (2026-10-29T19:51:54Z)
- (audit self) `self-review of the diff: claim regex unchanged; a tight 12-char conditional check before a match; edits counted only under the cwd's git root` → no findings [tree 052aa6d4c142] (2026-10-29T19:51:54Z)
## Log
- 2026-10-29T19:04:21Z created
- 2026-10-29T19:40:28Z set type=FIX, tier=S
- 2026-10-29T19:40:35Z planned: it has criteria and steps
- 2026-10-29T19:43:00Z focused
- 2026-10-29T19:52:30Z done
- 2026-10-29T19:52:32Z committed 199dcc3b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0886 [FEATURE M, done, 2 steps] The Stop hook checks the final message's specific claims (tests pass, fixed, verified) aga — lesson: Judge a run by its verdict, not by…
- research T-1669-review: Verdict:** approve with nits. I read the code but didn't run the tests; I haven't confirmed that `python3 plugin/tests/run.py test_drill test_des…
- T-1980 [FIX M, done, 4 steps] Batch keeps DONE-WHEN verify, gates name why-not-caught, fm ship marks its test run, first_touch keeps project files — lesson: A marker tha…
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–4 steps
## Lessons
- A check keyed to 'the project' should resolve the repo root, not trust the session's cwd, which follows cd into subfolders
## Plan gaps
- failed first: step 1 Red test: future-tense claim and an out-of-project edit don't block
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
