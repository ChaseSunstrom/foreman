---
id: T-1356
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:46Z
updated: 2026-10-23T07:03:29Z
base: 7c130e6389a956c3efd4762fae501df11295ab3f
base_tree: bda36a4ce51c68c73d23774c84a73dff5d0c147e
plan0_at: 2026-10-23T06:54:21Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code_worker.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code limits and failover: a worker turn's failure is sorted (usage limit with its reset, sign-in, crash, timeout); a limit within the wait cap is waited out and the turn redone, past it the run stops with its resume command; other failures pass the turn to the next runner in code.toml's chain
## Raw request
> fm code limits and failover (R10): a runner's failure is sorted (usage limit with reset time, auth, crash, timeout); a usage limit is waited out up to a cap and resumed from the journal; otherwise the next runner in a configured chain takes over
## Interpretation
An unattended fm code run with a CLI worker should survive the two common ways a worker turn fails without anyone there: the plan's usage limit (wait for the reset when it's soon, else stop and say when to resume) and a runner that is broken or signed out (hand the turn to another runner the user listed).
## Assumptions (confidence)
## Acceptance criteria
- [x] a worker failure is sorted into limit (with its reset time), auth, crash or timeout from its exit and reply — verify with `python3 plugin/tests/run.py test_code_worker.Failover`
- [x] a usage limit that resets within limit_wait is waited out and the turn redone; past it the run stops with Next: fm code --resume and the reset time — verify with `python3 plugin/tests/run.py test_code_worker.Failover`
- [x] a crash, timeout or sign-in failure with a chain in code.toml passes the turn to the next runner, said in a note — verify with `python3 plugin/tests/run.py test_code_worker.Failover`
## Non-goals
## Approach (options → choice → why)
Complete version: failure_kind(code, reply) sorts a turn (limit with a reset epoch, auth, timeout, crash, or none); Run.work redoes the turn after waiting out a limit within code.toml limit_wait (default 3600 s), stops past it with a CodeError whose Next is the resume command, and on auth, crash or timeout moves to the next runner in code.toml chain = [...] (each a runner name), said in a note and journaled. Options: (1) inside Run.work, one turn at a time (chosen: the judge and journal already wrap a turn, so a redo is the same turn again); (2) fail the run and let a supervisor (fm run, the app) restart it (loses the turn's context and needs a supervisor); (3) model-level failover in fmmodels (API profiles already retry 429/5xx; workers are CLIs). Reset parsing: 'limit reached|<epoch>' and 'resets 3pm' / 'resets 15:30' as the next such local time (ponytail: a named zone is ignored). Without a chain, a crash or timeout goes on as today (the verify judges); auth without a chain stops (nothing will work).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: sorting, a short limit waited out, a long one stopping, a chain taking over
2. [x] fmcode: failure_kind, the wait and the chain in Run.work
3. [x] docs: README, CHANGELOG, MASTER
## Resume here
## Docs impact
README fm code section, CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker.Failover` → exit 0 · Ran 5 tests in 6.8s (1 classes, 16 at a time; slowest: Failover 7s) / OK [ran] [tree db2c234310c2] (2026-10-23T06:58:30Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 69 tests in 72.0s (2 classes, 16 at a time; slowest: Worker 72s, Failover 6s) / OK [ran] [tree db2c234310c2] (2026-10-23T06:59:42Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.7s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree f5c67abdd5f0] (2026-10-23T06:59:52Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 70 tests in 72.5s (2 classes, 16 at a time; slowest: Worker 72s, Failover 8s) / OK [ran] [tree a1700d68616e] (2026-10-23T07:01:44Z)
- (audit intent) `self: request re-read` → pass: failures sorted (limit with reset, auth, crash, timeout), a near limit waited out and redone, a far one stops with the resume command, a chain takes over the rest [tree a1700d68616e] (2026-10-23T07:01:51Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker.Failover` → exit 0 · Ran 6 tests in 8.0s (1 classes, 16 at a time; slowest: Failover 8s) / OK [ran] [tree a1700d68616e] (2026-10-23T07:02:00Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker.Failover` → exit 0 · Ran 6 tests in 8.0s (1 classes, 16 at a time; slowest: Failover 8s) / OK [ran] [tree a1700d68616e] (2026-10-23T07:02:00Z)
- (ac 3) `python3 plugin/tests/run.py test_code_worker.Failover` → exit 0 · Ran 6 tests in 8.0s (1 classes, 16 at a time; slowest: Failover 8s) / OK [ran] [tree a1700d68616e] (2026-10-23T07:02:00Z)
- (audit intent) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → all three criteria met [tree a1700d68616e] (2026-10-23T07:02:00Z)
- (audit adversary) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → chain names resolve only through the runner registry and code.toml (no free command); the wait is capped by limit_wait and LIMIT_WAITS a turn; auth and limit patterns read only the reply's last 600 chars, so a test log saying Unauthorized earlier can't stop a run [tree a1700d68616e] (2026-10-23T07:02:00Z)
- (audit edge) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → a chain naming a runner twice can't loop (each runner once a turn, tested); a reset already past redoes at once; a limit with no reset time stops rather than guessing; an unknown runner in the chain stops with its own error [tree a1700d68616e] (2026-10-23T07:02:00Z)
## Log
- 2026-10-21T03:47:46Z created
- 2026-10-21T17:28:59Z round 2 (A26) adds: an auth-expiry line (please log in) parks the run without spending retries and names the login command
- 2026-10-23T06:52:21Z planned from capture
- 2026-10-23T06:52:29Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code_worker.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T06:54:20Z focused
- 2026-10-23T07:03:27Z done
- 2026-10-23T07:03:29Z committed e0163ccc (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- T-1476 [FEATURE S, blocked, 2 steps] fm code stops a worker turn at a usage limit instead of waiting out every timeout
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcode.py, plugin/tests/test_code_worker.py; re-ground the plan against them before editing
## Lessons
- A failover chain needs a per-turn record of what was tried: an index into the list loops when a name repeats
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- MASTER.md
- README.md
