---
id: T-2645
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T21:21:30Z
builder_model: sonnet
base: 4e3fbf868231a1d435e64b90f1608de7aee66689
base_tree: aa190ec5e247a2768e4523ea647a0d61288129ff
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T21:13:29Z
plan0_scope: []
lane_stop: merged 2026-11-02T21:18:00Z
verified: strong
unproven: [meaning]
---
# c.clock(), honouring FOREMAN_NOW, for the windowed readers in fmoutcomes and fmcost, with boundary tests at each window's edge
## Raw request
> FEATURE: Route every windowed reader through one injectable clock and boundary-test the metrics (c12: Crash, fault injection and reader robustness; value 3, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
1. (chosen) One clock for the windowed readers: c.clock() returns aware UTC now, or FOREMAN_NOW (an ISO time) when set, so a test can stand exactly on a window's edge. fmoutcomes (survival and calibration windows) and fmcost (_since, the weekly line, digest windows) read it instead of datetime.now. Boundary tests pin the edges: a close exactly at a window's end counts, one second before it doesn't.
2. Route all 216 clock reads in plugin/lib through it. Rejected for now: most aren't windows (timestamps on records); the windowed readers are where T-2610's off-by-a-window bug lived.
## Assumptions (confidence)
## Acceptance criteria
- [x] with FOREMAN_NOW set, fm outcomes and fm digest count a close exactly at a window's end and not one a second before it, and every datetime.now in fmoutcomes.py and fmcost.py reads c.clock() — verify with `python3 plugin/tests/run.py test_clock_windows`
## Non-goals
## Approach (options → choice → why)
1. c.clock() beside c.now() (which then formats c.clock()), FOREMAN_NOW honoured, and the datetime.now sites in fmoutcomes.py and fmcost.py moved to it; tests at each window edge. Likely outcome: no behaviour change, edges pinned. Fails if: a reader compares naive and aware times (the clock is always aware UTC; the tests would show it).
2. use what exists: freeze time with unittest.mock.patch on datetime in each test. Fails if: fm runs as a subprocess in most tests, where an in-process patch doesn't reach.
3. do less: boundary tests only, with timestamps placed relative to the real now. Fails if: a test straddling midnight or a slow run moves an edge and flakes.
Choice 1 (85%): one env-read clock reaches subprocess tests, and the change is mechanical in two files.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red boundary tests with FOREMAN_NOW
2. [x] c.clock() and the two modules' windowed reads
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_clock_windows` → exit 0 · Ran 4 tests in 28.6s (1 classes, 16 at a time; slowest: ClockWindows 28s) / OK [ran] [tree e444daf2e13b] [world 2f1906870a] (2026-11-02T21:15:31Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_clock_windows test_core test_cost test_cost_forecast test_economics test_export test_outcomes test_round_g test_trials test_usage_burn && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.24s] [ran] [tree e444daf2e13b] [world 2f1906870a] (2026-11-02T21:16:12Z)
- (step 1) `python3 plugin/tests/run.py test_clock_windows test_doctor test_outcomes` → exit 0 · Ran 180 tests in 33.6s (58 classes, 16 at a time; slowest: ClockWindows 33s, Survival 20s, CalibrationLedgerBets 16s) / OK [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:19:19Z)
- (step 2) `python3 plugin/tests/run.py test_clock_windows test_doctor test_outcomes` → exit 0 · Ran 180 tests in 28.1s (58 classes, 16 at a time; slowest: ClockWindows 28s, Survival 15s, ModelRouter 10s) / OK [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:19:47Z)
- (step 3) `python3 plugin/tests/run.py test_clock_windows test_doctor test_outcomes` → exit 0 · Ran 180 tests in 27.7s (58 classes, 16 at a time; slowest: ClockWindows 27s, Survival 14s, ModelRouter 9s) / OK [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:20:15Z)
- (ac 1) `python3 plugin/tests/run.py test_clock_windows` → exit 0 · Ran 5 tests in 26.0s (2 classes, 16 at a time; slowest: ClockWindows 26s, PinnedClockDoctor 0s) / OK [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:20:43Z)
- (audit intent) `self: reviewed the builder diff; c.clock() falls back to the real clock on a malformed value; now() formats clock(), which pins written timestamps too when FOREMAN_NOW is set, so fm doctor warns while it is (added in review)` → windowed readers share one clock and their edges are pinned by tests [tree 3b6fbbf51909] (2026-11-02T21:20:43Z)
- (audit edge) `self: reviewed the builder diff; c.clock() falls back to the real clock on a malformed value; now() formats clock(), which pins written timestamps too when FOREMAN_NOW is set, so fm doctor warns while it is (added in review)` → a naive FOREMAN_NOW is read as UTC; an offset is converted; junk is ignored (tested); the calibration window at fmoutcomes.py:472 is covered by the grep check, not an edge test [tree 3b6fbbf51909] (2026-11-02T21:20:43Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T21:13:17Z planned from capture
- 2026-11-02T21:13:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2645.builder.md
- 2026-11-02T21:13:28Z focused
- 2026-11-02T21:13:29Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T21:18:00Z merged worktree-agent-a1639f0e415bfa388 (4 file(s))
- 2026-11-02T21:18:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1639f0e415bfa388
- 2026-11-02T21:18:00Z focused
- 2026-11-02T21:20:15Z scope: plugin/lib/fmdoctor.py (check_pinned_clock: FOREMAN_NOW outside tests pins every timestamp), CHANGELOG.md
- 2026-11-02T21:21:27Z done
- 2026-11-02T21:21:30Z committed 2e6b1eee (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2648 [FEATURE S, done, 3 steps] fm drill gains a fault that drops one ledger event class (every task_done line, say): each reader that leans on it must name what's mis…
- T-2635 [FEATURE S, done, 3 steps] A close with an unproven proof kind records it: the receipt says 'unproven: KINDS' beside its grade, the brief and task_done event keep…
- T-2643 [FEATURE S, done, 3 steps] fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still an…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
## Lessons
- A test-only override read by a shared helper reaches production writes too: give it a doctor row that says when it's set
## Files touched
- plugin/tests/test_clock_windows.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
