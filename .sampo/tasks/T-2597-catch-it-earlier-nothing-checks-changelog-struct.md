---
id: T-2597
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-02T10:10:15Z
updated: 2026-11-02T10:41:34Z
base: 68206bb2daf573f6ce14eac4efdcd979cae1935d
base_tree: cc10ed1d95e6a4264d647ccc0ba703f6ba31301d
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T10:16:04Z
plan0_scope: []
verified: strong
---
# fm doctor warns when CHANGELOG's Unreleased section has gone 14+ days or 150+ bullets without a release
## Raw request
> T-2591 (CHANGELOG's Unreleased section opens with a short Highlights list of user-facing changes; the rest sits under Everything else; numbers carry their counts and baselines) wasn't caught before it shipped: nothing checks CHANGELOG structure or that a quoted rate carries its count; the release cadence lapsed, so the section grew for 12 days
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] check_release_age reads CHANGELOG.md: the newest '## X.Y.Z — date' heading and the Unreleased bullet count; WARN past 14 days or 150 bullets naming both and 'fm release'; PASS otherwise; a repo without CHANGELOG.md passes — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
A lint that each quoted rate carries its count: fuzzy to detect, and the cross-cutting review already grounds and flags such numbers (T-2581, T-2585).
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_doctor
2. [x] check_release_age in fmdoctor, wired into the run list
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.ReleaseAge` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ReleaseAge 0s) / FAILED (1 classes: test_doctor.ReleaseAge) [ran] [tree 4a8f45ef165d] [world 2f1906870a] (2026-11-02T10:16:18Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 108 tests in 4.1s (38 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree d133091277ab] [world 2f1906870a] (2026-11-02T10:17:16Z)
- `python3 plugin/tests/run.py test_doctor.ReleaseAge` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: ReleaseAge 0s) / FAILED (1 classes: test_doctor.ReleaseAge) (start tree + this task's tests) [ran] [tree 42d21710ff8b] [world 2f1906870a] (2026-11-02T10:23:07Z)
- `python3 plugin/tests/run.py test_doctor.ReleaseAge` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ReleaseAge 0s) / OK [ran] [tree 42d21710ff8b] [world 2f1906870a] (2026-11-02T10:23:07Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 108 tests in 4.0s (38 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree 42d21710ff8b] [world 2f1906870a] (2026-11-02T10:23:19Z)
- (audit intent) `self-review: check_release_age parses the Unreleased bullets and the newest dated version heading; WARN past 14 days or 150 bullets with fm release named; no file, no section or an empty section passes; wired after usage burn with the project root` → 20 days or 160 bullets warn; a fresh short section and no CHANGELOG pass (test) [tree 42d21710ff8b] (2026-11-02T10:23:19Z)
- (audit edge) `self-review: check_release_age parses the Unreleased bullets and the newest dated version heading; WARN past 14 days or 150 bullets with fm release named; no file, no section or an empty section passes; wired after usage burn with the project root` → an empty Unreleased never warns however old the last release is (nothing waits); a CHANGELOG without dated headings reads 'no release yet' and warns only on bullet count [tree 42d21710ff8b] (2026-11-02T10:23:19Z)
- (audit self) `self-review: check_release_age parses the Unreleased bullets and the newest dated version heading; WARN past 14 days or 150 bullets with fm release named; no file, no section or an empty section passes; wired after usage burn with the project root` → no findings [tree 42d21710ff8b] (2026-11-02T10:23:19Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:41:34Z)
## Log
- 2026-11-02T10:10:15Z created
- 2026-11-02T10:11:45Z planned from capture
- 2026-11-02T10:16:03Z set approved=True
- 2026-11-02T10:16:03Z focused
- 2026-11-02T10:16:04Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T10:23:38Z done
- 2026-11-02T10:23:41Z committed 6276aa3d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2591 [FIX M, done, 3 steps] CHANGELOG's Unreleased section opens with a short Highlights list of user-facing changes; the rest sits under Everything else; numbers carr…
- T-2595 [FEATURE M, planned, 3 steps] Release 1.2.51: the 12 days of fixes since 1.2.50 reach plugin users
- T-2052 [FEATURE L, done, 5 steps] Docs/README redesign: replace walls of text with scannable structure — hero with logo,… — lesson: Measure docs by what a reader sees: a…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Lessons
- A cadence that nothing measures lapses silently; give it a doctor row with the command that resets it
## Plan gaps
- failed first: step 1 red test in test_doctor
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
