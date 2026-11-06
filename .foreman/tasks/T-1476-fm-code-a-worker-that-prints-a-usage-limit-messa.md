---
id: T-1476
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T16:21:31Z
updated: 2026-11-03T00:53:33Z
group: fm code runner streams and usage limits
builder_model: sonnet
base: e0d66ada33f2e031ef587d94381383caee67c408
base_tree: d56f5fba77aad0c6667c780e4597e601bb264021
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T00:38:59Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py, CHANGELOG.md]
lane_stop: merged 2026-11-03T00:49:10Z
verified: strong
---
# fm code stops a worker turn at a usage limit instead of waiting out every timeout
## Raw request
> fm code: a worker that prints a usage-limit message still spends every timeout (step turn plus 3 fix rounds); stop early on a recognised limit and offer the failover runner (T-1361's fakes show it: usage-limit mode is only a 'stalled' event)
## Interpretation
When a worker CLI prints a rate or usage limit, the stall beat (fmcode.py ~680-692) only emits 'stalled: hit a rate or usage limit' and the turn waits out its full --worker-timeout, then the fix rounds repeat it (4 timeouts; T-1361's usage-limit fake shows it).
## Assumptions (confidence)
## Acceptance criteria
- [x] a usage-limit worker ends the run within a few seconds as blocked naming the limit, with no fix rounds — verify with `cd plugin/tests && python3 -m unittest test_code_fakes.CodeFakes.test_usage_limit_stops_the_run`
## Non-goals
## Approach (options → choice → why)
On a 'limit' stall cause, end the turn at once (kill the worker's process group as a timeout does) and end the run as blocked with the reason 'usage limit: <last line>' and, when --escalate names another runner, say to rerun with it (no automatic failover: switching models silently changes cost and behaviour). Options: retry after a backoff (limits often last hours) → rejected; automatic failover → rejected for now, captured if wanted.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test (T-1361's usage-limit fake)
2. [x] end the turn and run on a limit stall
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_code_fakes.py -k usage_limit` → ✗ exit 1 · Ran 1 test in 86.838s / FAILED (errors=1) [ran] [tree af2db424e579] [world 2f1906870a] (2026-11-03T00:40:57Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_code_fakes.py` → ✗ exit 1 · Ran 7 tests in 37.087s / FAILED (failures=1) [ran] [tree 007421fe7890] [world 2f1906870a] (2026-11-03T00:41:48Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_code_fakes.py` → exit 0 · Ran 7 tests in 35.498s / OK [ran] [tree bec338d5f3a2] [world 2f1906870a] (2026-11-03T00:42:28Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_code test_code_envelope test_code_fakes test_code_worker test_export test_judge_home test_runner_lint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 496 tests in 104.9s (106 classes, 16 at a time; slowest: Worker 103s, CodeFakes 39s, JudgeHome 32s) / FAILED (1 classes: test_code_worker.Worker) [ran] [tree bec338d5f3a2] [world 2f1906870a] (2026-11-03T00:44:13Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_code test_code_envelope test_code_fakes test_code_worker test_export test_judge_home test_runner_lint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.80s] [ran] [tree a55d629c4a8a] [world 2f1906870a] (2026-11-03T00:48:04Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_fakes.CodeFakes.test_usage_limit_stops_the_run` → exit 0 · Ran 1 test in 1.485s / OK [ran] [tree f2b13010631b] [world 2f1906870a] (2026-11-03T00:51:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_fakes.CodeFakes.test_usage_limit_stops_the_run` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:51:03Z [ran] [tree f2b13010631b] [world 2f1906870a] (2026-11-03T00:52:09Z)
- (step 1) `python3 plugin/tests/run.py test_code_fakes test_code_worker` → exit 0 · Ran 86 tests in 64.5s (6 classes, 16 at a time; slowest: Worker 64s, CodeFakes 34s, Failover 10s) / OK [ran] [tree f2b13010631b] [world 2f1906870a] (2026-11-03T00:52:09Z)
- (audit edge) `read the merged diff: a stall classed as a limit with a stated limit phrase kills the worker's process group and work() raises Blocked naming the line and the --resume command; the turn's changes are still judged and reverted; review tightened the kill to _LIMIT_FIRM, so 'quota'/'429' in passing no longer kills` → a pid of 0 or 1 or a dead pid is never killed (guarded); a limit seen only at exit still takes the old failover path [tree f2b13010631b] (2026-11-03T00:52:09Z)
- (audit adversary) `read the merged diff: a stall classed as a limit with a stated limit phrase kills the worker's process group and work() raises Blocked naming the line and the --resume command; the turn's changes are still judged and reverted; review tightened the kill to _LIMIT_FIRM, so 'quota'/'429' in passing no longer kills` → killpg targets only the worker's own session group, started by fm code (start_new_session) [tree f2b13010631b] (2026-11-03T00:52:09Z)
- (audit self) `read the merged diff: a stall classed as a limit with a stated limit phrase kills the worker's process group and work() raises Blocked naming the line and the --resume command; the turn's changes are still judged and reverted; review tightened the kill to _LIMIT_FIRM, so 'quota'/'429' in passing no longer kills` → no findings [tree f2b13010631b] (2026-11-03T00:52:09Z)
## Log
- 2026-10-22T16:21:31Z created
- 2026-10-22T16:39:19Z planned from capture
- 2026-10-22T16:39:25Z blocked: waits for T-1401's lane (both edit fmcode.py); then a builder
- 2026-11-03T00:36:17Z unblocked: their named blockers (T-1214, T-1316, T-1401) closed weeks ago; the blocked-pile line found them (T-2683)
- 2026-11-03T00:38:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1476.builder.md
- 2026-11-03T00:38:52Z focused
- 2026-11-03T00:38:59Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T00:49:10Z merged worktree-agent-aba60fe502a927e6f (3 file(s))
- 2026-11-03T00:49:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aba60fe502a927e6f
- 2026-11-03T00:49:10Z focused
- 2026-11-03T00:50:56Z steer: review made the kill need a stated limit (_LIMIT_FIRM: 'usage limit', 'rate limit reached', 'quota exceeded'…); a bare 'quota' or '429' in the last lines only labels the stall, tested both ways
- 2026-11-03T00:50:56Z scope: plugin/tests/test_code_worker.py (its rate-limit stall now ends blocked)
- 2026-11-03T00:53:30Z done
- 2026-11-03T00:53:33Z committed 4f797336 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1356 [FEATURE M, done, 3 steps] fm code limits and failover: a worker turn's failure is sorted (usage limit with its reset, sign-in, crash, timeout); a limit within th…
- T-1361 [FEATURE S, done, 2 steps] One helper for misbehaving fake runner CLIs in tests
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-11-02: [costly] Correction: Mission 3 and the loop rounds run now, bounded by fm budget
- similar finished tasks took 2–3 steps
- start here (files T-1356 touched): plugin/tests/test_code_worker.py, plugin/lib/fmcode.py, CHANGELOG.md, MASTER.md, README.md
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test (T-1361's usage-limit fake)
- failed first: step 2 end the turn and run on a limit stall
## Files touched
- .fm-scratch/e.json
- plugin/tests/test_code_fakes.py
- .fm-scratch/f.json
- plugin/lib/fmcode.py
- plugin/tests/test_code_worker.py
- SAMPO.md
- CHANGELOG.md
