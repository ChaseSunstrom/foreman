---
id: T-2075
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T01:05:47Z
updated: 2026-10-31T01:23:12Z
base: a404392a1ded96029a4b6a246c9f1842fe78897d
base_tree: d5cdea5877cf3b78fa79beb523bd62a2647cb884
plan0_at: 2026-10-31T01:01:50Z
plan0_scope: []
verified: strong
---
# Loop rounds: a left-behind file that fm decide kept (why it stays) is listed again every…
## Raw request
> Loop rounds: a left-behind file that fm decide kept (why it stays) is listed again every round; skip files a decision names until they change again (T-2073 follow-up)
## Interpretation
fm loop round lists the files recent work left behind (fmloop.lag, from fmmap.drift). A file the session already decided to leave (an fm decide row naming it, with why it stays) is listed again every round. Skip a file a decision names until the file changes after that decision.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm loop round leaves out a lagging file that a decision names, and lists it again once the file changes after that decision — verify with `cd plugin/tests && python3 -m unittest -q test_loop.LagKept`
## Non-goals
## Approach (options → choice → why)
Options: (1) lag() drops a file whose path appears in a decisions.md row dated on or after the file's last commit (git log -1 --format=%cs -- FILE, with fsmonitor and hooks off), so a change to it brings it back; (2) a separate 'kept' list in meta (a second place to record what fm decide already records); (3) mute forever (hides a file that later truly lags). Choice 1: the decision is the record, and the file's own history ends the mute.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_loop with a temp repo and a decision row; then lag() filters by decision date vs the file's last commit
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_loop.LagKept 2>&1 | tail -8` → ✗ exit 1 · Ran 1 test in 0.307s / FAILED (failures=1) [ran] [tree 5194d20949fc] (2026-10-31T01:02:13Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_loop.LagKept` → exit 0 · Ran 1 test in 0.168s / OK [ran] [tree f9f2b1b66810] (2026-10-31T01:02:36Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_loop && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.11s] [ran] [tree f9f2b1b66810] (2026-10-31T01:03:05Z)
- `cd plugin/tests && python3 -m unittest -q test_loop.LagKept` → ✗ exit 1 · Ran 1 test in 0.298s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 1056db833d97] (2026-10-31T01:12:59Z)
- `cd plugin/tests && python3 -m unittest -q test_loop.LagKept` → exit 0 · Ran 1 test in 0.132s / OK [ran] [tree 1056db833d97] (2026-10-31T01:12:59Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_loop` → exit 0 · Ran 19 tests in 9.785s / OK [ran] [tree 1056db833d97] (2026-10-31T01:13:18Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_loop.LagKept` → exit 0 · Ran 1 test in 0.086s / OK [ran] [tree a7e70d742a23] (2026-10-31T01:22:53Z)
- `cd plugin/tests && python3 -m unittest -q test_loop` → exit 0 · Ran 19 tests in 6.073s / OK [ran] [tree a7e70d742a23] (2026-10-31T01:22:53Z)
- (audit edge) `self: lag() drops a file when a decision row names it (path-bounded match, so a/b.py doesn't match xa/b.py or a/b.pyc) dated on or after the file's last commit; a later commit lists it again; git failure keeps the file listed; test_loop 19 green, red-to-green proven` → same-day grain: a commit later on the decision's day still counts as kept until the next day's commit; an untracked file (empty log) counts as kept when named [tree a7e70d742a23] (2026-10-31T01:22:53Z)
- (audit self) `self: lag() drops a file when a decision row names it (path-bounded match, so a/b.py doesn't match xa/b.py or a/b.pyc) dated on or after the file's last commit; a later commit lists it again; git failure keeps the file listed; test_loop 19 green, red-to-green proven` → no findings [tree a7e70d742a23] (2026-10-31T01:22:53Z)
## Log
- 2026-10-30T01:05:47Z created
- 2026-10-31T00:56:30Z set tier=S
- 2026-10-31T00:56:31Z planned: it has criteria and steps
- 2026-10-31T00:56:32Z set approved=True
- 2026-10-31T01:01:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2075.builder.md
- 2026-10-31T01:01:49Z focused
- 2026-10-31T01:10:00Z merged worktree-agent-aa4c1800fe6f28f7e (2 file(s))
- 2026-10-31T01:10:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa4c1800fe6f28f7e
- 2026-10-31T01:22:45Z focused
- 2026-10-31T01:22:46Z scope: plugin/lib/fmloop.py lag() and test_loop
- 2026-10-31T01:23:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2074 [CLEAN S, done, 1 steps] MASTER.md forever-loop line: add T-2073's surface lag (FACES, lag(), LAG_MIN, the… — lesson: A doc follow-up written before the code land…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-23: T-1549: leave out a demo teleprompter pane, a guard near-miss gallery and per-dependency decision cards
- similar finished tasks took 1–7 steps
## Lessons
- A dismissal must expire on the thing it dismissed changing, or it silences the next real lag
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmloop.py
- plugin/tests/test_mission.py
