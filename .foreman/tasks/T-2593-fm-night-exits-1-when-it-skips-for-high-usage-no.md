---
id: T-2593
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T08:34:56Z
updated: 2026-11-02T09:16:44Z
base: cbaef56f56b31d547f50a0a258f97345a90e3c41
base_tree: 6465a969624084c45560eda0f9e41617bb79998b
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T08:55:28Z
plan0_scope: []
verified: strong
---
# fm night exits 0 when it skips for high usage, so systemd records a deliberate skip as success
## Raw request
> FIX: fm night exits 1 when it skips for high usage ('nothing runs tonight'), so systemd marks the night service failed and fm doctor / foresight report 'last run failed' for a timer working as designed (journalctl 2026-11-02 02:30); a deliberate skip should exit 0 with its line
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm night with weekly usage high prints its 'nothing runs tonight' line and exits 0, runs no job and spends nothing — verify with `python3 plugin/tests/run.py test_night`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_night
2. [x] print and return instead of raising UsageError
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night` → ✗ exit 1 · Ran 42 tests in 6.7s (13 classes, 16 at a time; slowest: Night 6s, NightInstall 2s, NightGuards 2s) / FAILED (1 classes: test_night.Night) [ran] [tree 73e98bf0cdae] [world 2f1906870a] (2026-11-02T08:55:41Z)
- (ac 1) `python3 plugin/tests/run.py test_night 2>&1 | grep -E "^(ERROR|FAIL):|^OK|FAILED" | head -4` → exit 0 · OK [ran] [tree 66cfd648b2bf] [world 2f1906870a] (2026-11-02T08:55:53Z)
- (step 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 42 tests in 6.8s (13 classes, 16 at a time; slowest: Night 7s, NightInstall 2s, NightGuards 2s) / OK [ran] [tree 66cfd648b2bf] [world 2f1906870a] (2026-11-02T08:56:12Z)
- `python3 plugin/tests/run.py test_night.Night` → ✗ exit 1 · Ran 29 tests in 7.7s (4 classes, 16 at a time; slowest: Night 6s, NightGuards 2s, NightTick 1s) / FAILED (1 classes: test_night.Night) (start tree + this task's tests) [ran] [tree 0a007bfc73d0] [world 2f1906870a] (2026-11-02T09:01:56Z)
- `python3 plugin/tests/run.py test_night.Night` → exit 0 · Ran 29 tests in 6.6s (4 classes, 16 at a time; slowest: Night 6s, NightGuards 1s, NightTick 1s) / OK [ran] [tree 0a007bfc73d0] [world 2f1906870a] (2026-11-02T09:01:56Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 42 tests in 6.7s (13 classes, 16 at a time; slowest: Night 6s, NightInstall 2s, NightGuards 2s) / OK [ran] [tree 0a007bfc73d0] [world 2f1906870a] (2026-11-02T09:02:04Z)
- (audit intent) `self-review: the high-usage branch returns fmcli.out with skipped and ran=[]; no job runs and nothing is spent; the line is unchanged; no other caller depended on the non-zero exit (grep)` → the skip exits 0 with its line, and --json says skipped with ran [] (test) [tree 0a007bfc73d0] (2026-11-02T09:02:04Z)
- (audit operator) `self-review: the high-usage branch returns fmcli.out with skipped and ran=[]; no job runs and nothing is spent; the line is unchanged; no other caller depended on the non-zero exit (grep)` → an installed night timer now records skipped nights as success, so fm doctor's timer liveness row and the session-start Watch line stop calling a working timer failed; a real failure (a crash) still exits non-zero [tree 0a007bfc73d0] (2026-11-02T09:02:04Z)
- (audit self) `self-review: the high-usage branch returns fmcli.out with skipped and ran=[]; no job runs and nothing is spent; the line is unchanged; no other caller depended on the non-zero exit (grep)` → no findings [tree 0a007bfc73d0] (2026-11-02T09:02:04Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 773b6e126ee1] [world 2f1906870a] (2026-11-02T09:16:44Z)
## Log
- 2026-11-02T08:34:56Z created
- 2026-11-02T08:35:08Z planned from capture
- 2026-11-02T08:55:27Z set approved=True
- 2026-11-02T08:55:27Z focused
- 2026-11-02T08:55:28Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T09:02:26Z done
- 2026-11-02T09:02:29Z committed 7272d2c0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2542 [FEATURE M, done, 4 steps] Installed Foreman timers known alive: systemd's last trigger and last result, in fm doctor and the next session's Watch line — lesson: …
- T-0955 [FEATURE M, done, 3 steps] fm run and night: quarantine a no-progress task across runs, keep the machine awake, print a timer line — lesson: A side door that sets…
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
## Lessons
- A deliberate skip run by a scheduler must exit 0: the scheduler's failure flag feeds Foreman's own liveness checks
## Plan gaps
- failed first: step 1 red test in test_night
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
- CHANGELOG.md
