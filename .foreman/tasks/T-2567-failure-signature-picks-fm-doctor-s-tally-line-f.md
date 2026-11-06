---
id: T-2567
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T07:41:56Z
updated: 2026-11-02T08:22:13Z
base: 8d8884ae6560cddf122d0b1777c30e1634c0e4a9
base_tree: 968f70c1c7a36f29588c74de4281eb29a3e4f519
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T07:47:44Z
plan0_scope: []
verified: strong
---
# failure_signature skips fm doctor's tally line, so a doctor failure is signed by the FAIL row naming its check
## Raw request
> FIX: failure_signature picks fm doctor's tally line ('fm doctor: failed (N pass, N warn, N fail)', numbers zeroed) instead of the FAIL row naming the check, so fm digest's Recurring failures shows 25 identical, uninformative doctor failures; treat the doctor tally like _TALLY_LINE (fmrecall.py:507)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] failure_signature of doctor output with a FAIL row and the 'fm doctor: failed (N pass, N warn, N fail)' tally returns the FAIL row's signature; a doctor output with only its tally has no signature — verify with `python3 plugin/tests/run.py test_recall`
## Non-goals
## Approach (options → choice → why)
1) Add doctor's tally ('fm doctor: OK|FAILED (N pass, N warn, N fail)') to _TALLY_LINE and print doctor's FAIL rows last, next to the verdict, so the newest error line is the failing check. Likely outcome: each doctor failure signs by its check. 2) use what exists: _TALLY_LINE already drops test runners' tallies (T-1769); only the doctor pattern is added, with no row reordering. Fails if: a WARN row printed after the FAIL row carries an error word and wins. 3) do less: leave the signature and filter doctor sigs out of the digest. Fails if: recurring doctor failures disappear instead of being named. Choice 1 (85%): the tally pattern plus the reordering is two lines and also helps a reader.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] add the doctor tally to _TALLY_LINE
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall.Tally test_doctor` → ✗ exit 1 · Ran 108 tests in 5.4s (37 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, Command 2s) / FAILED (2 classes: test_doctor.Command, test_recall.Tally) [ran] [tree 99f6c41ab9b3] [world 2f1906870a] (2026-11-02T07:48:10Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_doctor` → exit 0 · Ran 142 tests in 19.0s (47 classes, 16 at a time; slowest: Recall 19s, OtherProjects 5s, Consolidate 4s) / OK [ran] [tree b972cb519262] [world 2f1906870a] (2026-11-02T07:49:05Z)
- `python3 plugin/tests/run.py test_recall.Tally test_doctor` → ✗ exit 1 · Ran 108 tests in 5.1s (37 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / FAILED (2 classes: test_doctor.Command, test_recall.Tally) (start tree + this task's tests) [ran] [tree 196313a865da] [world 2f1906870a] (2026-11-02T07:59:26Z)
- `python3 plugin/tests/run.py test_recall.Tally test_doctor` → exit 0 · Ran 108 tests in 4.0s (37 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree 196313a865da] [world 2f1906870a] (2026-11-02T07:59:26Z)
- (ac 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 36 tests in 13.7s (11 classes, 16 at a time; slowest: Recall 13s, OtherProjects 5s, Consolidate 3s) / OK [ran] [tree 196313a865da] [world 2f1906870a] (2026-11-02T07:59:41Z)
- (audit intent) `self-review: _TALLY_LINE gains doctor's exact summary shape; doctor's plain output sorts FAIL rows last (stable, WARN order kept); --json untouched` → a doctor failure signs by its FAIL row (test); a tally-only output has no signature (test); FAIL rows print last (test on a fresh HOME that has FAILs) [tree 196313a865da] (2026-11-02T07:59:41Z)
- (audit edge) `self-review: _TALLY_LINE gains doctor's exact summary shape; doctor's plain output sorts FAIL rows last (stable, WARN order kept); --json untouched` → a WARN row with an error word can no longer outrank a FAIL row since FAILs print after every WARN; the 42 old zeroed rows age out of the digest's week window [tree 196313a865da] (2026-11-02T07:59:41Z)
- (audit self) `self-review: _TALLY_LINE gains doctor's exact summary shape; doctor's plain output sorts FAIL rows last (stable, WARN order kept); --json untouched` → no findings [tree 196313a865da] (2026-11-02T07:59:41Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:22:13Z)
## Log
- 2026-11-02T07:41:56Z created
- 2026-11-02T07:42:11Z planned from capture
- 2026-11-02T07:47:44Z focused
- 2026-11-02T07:47:44Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T07:59:27Z scope: plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py — FAIL rows print last so the signature's newest error line is the failing check
- 2026-11-02T08:00:11Z done
- 2026-11-02T08:00:14Z committed dccffb96 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1769 [FIX S, done, 1 steps] A test runner's tally became the failure signature, so red-first runs read as a recurring obstacle
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- research T-1076-review: Verdict: approve with nits.** The code is correct on the paths I traced. None of these findings is HIGH. I did not run the tests, and I could not…
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar finished tasks took 1–7 steps
- start here (files T-1769 touched): CHANGELOG.md, plugin/lib/fmrecall.py, plugin/tests/test_recall.py
## Lessons
- A summary tally at the end of any tool's output outranks the line that names the failure; every runner Foreman wraps needs its tally in _TALLY_LINE
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_recall.py
- plugin/tests/test_doctor.py
- plugin/lib/fmrecall.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
