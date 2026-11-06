---
id: T-1158
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T12:04:30Z
base: f9916b2bc3a1683a0b851346e75b6c1eae5d68e3
base_tree: 0a3b335d7c2d17c84610eef5e80c91194f9f760b
plan0_at: 2026-10-16T11:14:07Z
plan0_scope: []
verified: strong
---
# Add `fm contract --until HH:MM --usd N` so the drive, `fm run` and the loop stop at the ti
## Raw request
> FEATURE: Add `fm contract --until HH:MM --usd N` so the drive, `fm run` and the loop stop at the time or spend bound and print a receipt of what ran.
> DONE-WHEN: a test with a fake clock and fake spend stops the run at each bound, and the receipt lists the tasks closed, the spend and which bound ended it
## Interpretation
Say once how long and how much an unattended run may take: fm contract --until HH:MM (local time, today or tomorrow if past) and/or --usd N. While the contract holds, the Stop drive, the forever loop and fm run keep going; once either bound is reached they stop continuing and print a receipt: tasks closed since it began, spend since it began, which bound ended it. fm contract shows it; fm contract off ends it.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a contract whose time or spend bound has passed, the Stop drive no longer continues, fm next says the contract ended, and fm contract receipt lists tasks closed, spend and the bound that ended it; with no contract nothing changes — verify with `python3 plugin/tests/run.py test_contract`
## Non-goals
## Approach (options → choice → why)
Options: (a) a contract in project meta {until, usd, started, spent0} that the drive (fmhooks Stop), fm next and fm run (fmserve, which already has --max-usd) consult through one fmcontract.over(p) -> reason|None, plus fm contract receipt; (b) only a new fm run flag; (c) a budget-cap reuse via fm budget. Choice: (a); why: the drive is what keeps an interactive AFK session going, and fm run's --max-usd only covers headless runs. Spend comes from the same source fm cost reads (no new accounting). Register near fm budget's registration.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_contract.py): fake clock past --until stops the drive; fake spend over --usd stops it; receipt contents; fm contract off; no contract = no change
2. [x] fmcontract.py (set/show/off/receipt/over), wired into the Stop drive, fm next and fm run
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_contract` → exit 0 · Ran 6 tests in 18.1s (1 classes, 16 at a time; slowest: Contract 17s) / OK [ran] [tree c67153dcc36d] (2026-10-16T11:17:57Z)
- (step 2) `python3 plugin/tests/run.py test_contract` → exit 0 · Ran 6 tests in 12.5s (1 classes, 16 at a time; slowest: Contract 12s) / OK [ran] [tree c67153dcc36d] (2026-10-16T11:18:10Z)
- (step 2) `python3 plugin/tests/run.py test_contract test_serve` → exit 0 · Ran 36 tests in 19.7s (6 classes, 16 at a time; slowest: Run 20s, Contract 6s, Serve 3s) / OK [ran] [tree a59bb1f6a737] (2026-10-16T11:37:12Z)
- (step 2) `python3 plugin/tests/run.py test_contract test_serve` → exit 0 · Ran 41 tests in 29.4s (6 classes, 16 at a time; slowest: Run 29s, Contract 21s, Serve 8s) / OK [ran] [tree 5462a8530773] (2026-10-16T11:54:02Z)
- (ac 1) `python3 plugin/tests/run.py test_contract test_serve test_hooks` → exit 0 · Ran 198 tests in 73.7s (25 classes, 16 at a time; slowest: Stop 74s, PreToolUse 48s, Run 34s) / OK [ran] [tree a31c38c9ce0f] (2026-10-16T12:01:29Z)
- (ac 1) `python3 plugin/tests/run.py test_contract` → exit 0 · Ran 12 tests in 15.5s (1 classes, 16 at a time; slowest: Contract 15s) / OK [ran] [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
- (audit intent) `reviewer: one fm-reviewer pass found the Stop hook re-locking its own lock (5 s self-wait, drive never stopped), fm run not recording spend, an ended contract disabling every later session, next_for still offering the loop, and an unbounded refresh spawn; builder fixed all five test-first (hook-first test under 4 s); I read the merged hook path: no relock, fails open, re-reads each call` → say once how long and how much; the run stops itself and says what it did [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
- (audit adversary) `reviewer: one fm-reviewer pass found the Stop hook re-locking its own lock (5 s self-wait, drive never stopped), fm run not recording spend, an ended contract disabling every later session, next_for still offering the loop, and an unbounded refresh spawn; builder fixed all five test-first (hook-first test under 4 s); I read the merged hook path: no relock, fails open, re-reads each call` → an unreadable contract never traps the drive (fails open); spend counts only this project's rows [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
- (audit edge) `reviewer: one fm-reviewer pass found the Stop hook re-locking its own lock (5 s self-wait, drive never stopped), fm run not recording spend, an ended contract disabling every later session, next_for still offering the loop, and an unbounded refresh spawn; builder fixed all five test-first (hook-first test under 4 s); I read the merged hook path: no relock, fails open, re-reads each call` → HH:MM in the past rolls to tomorrow; a compaction keeps an ended contract, a new session clears it with the receipt kept [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
- (audit operator) `reviewer: one fm-reviewer pass found the Stop hook re-locking its own lock (5 s self-wait, drive never stopped), fm run not recording spend, an ended contract disabling every later session, next_for still offering the loop, and an unbounded refresh spawn; builder fixed all five test-first (hook-first test under 4 s); I read the merged hook path: no relock, fails open, re-reads each call` → fm next says the contract ended; fm contract receipt shows tasks, dollars, tokens, bound [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found the Stop hook re-locking its own lock (5 s self-wait, drive never stopped), fm run not recording spend, an ended contract disabling every later session, next_for still offering the loop, and an unbounded refresh spawn; builder fixed all five test-first (hook-first test under 4 s); I read the merged hook path: no relock, fails open, re-reads each call` → one module; over() is the single check for the drive, next_for and fm run [tree 03f4af7efbf8] (2026-10-16T12:01:59Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:14:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1158.builder.md
- 2026-10-16T11:14:07Z focused
- 2026-10-16T11:59:02Z merged worktree-agent-a9b2f53aa3ea84025 (8 file(s))
- 2026-10-16T12:00:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9b2f53aa3ea84025
- 2026-10-16T12:00:15Z focused
- 2026-10-16T12:01:43Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T12:04:28Z done
- 2026-10-16T12:04:30Z committed c23cbe2a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0117 [FEATURE S, done, 2 steps] While-you-were-away row: what drive finished since the user's last message
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–3 steps
## Lessons
- a helper called from inside a locked hook must take a held flag; c.lock is not re-entrant
## Files touched
- plugin/tests/test_contract.py
- plugin/lib/fmcontract.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmserve.py
- plugin/tests/test_serve.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- MASTER.md
- CHANGELOG.md
