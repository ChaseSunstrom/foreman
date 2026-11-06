---
id: T-2741
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: [T-2742]
source: followup
created: 2026-11-03T00:44:22Z
updated: 2026-11-04T14:14:36Z
base: 375a5a2b4a19decb28053a92952b96cb3b6abe22
base_tree: a76f0dd3614f3a93b45f844e87bd9f2e7c4d0d3e
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T14:01:56Z
plan0_scope: []
verified: strong
---
# fm code's first printed line names the project slug and its root, so a run started with a -p prefix (T-1344) shows which project it resolved to
## Raw request
> fm code's first output line names the project and its root, so a run started with a -p prefix shows which project it resolved to (the unbuilt part of T-1344's request)
## Interpretation
Reading 1 (chosen): the start event (fmcode.py ~2579, emitted quiet) becomes a printed first line naming the project and its root, and its data gains both. Reading 2 (ruled out): print it only when -p was a prefix. Ruled out: the line costs one row and answers 'which project' for every run.
## Assumptions (confidence)
## Acceptance criteria
- [x] a run's first output line is 'fm code in <slug> (<root>)' and the start event carries project and root — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1. Make the start emit print 'fm code in <slug> (<root>)' and add project/root to its data. Likely outcome: two lines changed. 2. Print it from cmd_code before the run starts. Fails if: a resumed run skips that path. 3. Use what exists: run.emit already prints and journals. Choice 1 on 3 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] print the start line (fmcode.py's start emit is quiet today)
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG line (T-2741)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.SelfRunningNote` → ✗ exit 1 · Ran 2 tests in 7.1s (1 classes, 16 at a time; slowest: SelfRunningNote 6s) / FAILED (1 classes: test_code.SelfRunningNote) [ran] [tree 34f60040dc3c] [world 2f1906870a] (2026-11-04T14:04:45Z)
- (step 2) `python3 plugin/tests/run.py test_code test_code_worker test_code_planner` → exit 0 · Ran 487 tests in 75.4s (105 classes, 16 at a time; slowest: Worker 75s, CodeFakes 36s, OutcomeEscalation 29s) / OK [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:11:46Z)
- (step 3) `grep -c T-2741 CHANGELOG.md` → exit 0 · 1 [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:11:47Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 487 tests in 74.8s (105 classes, 16 at a time; slowest: Worker 75s, CodeFakes 35s, OutcomeEscalation 28s) / OK [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:13:06Z)
- (step 1) `python3 plugin/tests/run.py test_code.SelfRunningNote` → exit 0 · Ran 2 tests in 2.8s (1 classes, 16 at a time; slowest: SelfRunningNote 2s) / OK [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:13:06Z)
- (audit edge) `self: the start emit now prints its text and carries project and root; test_code's event-order tests still pass with the printed line` → a --json run prints the start event as JSON with project and root; the resume and recheck start emits stay quiet, as they print their own line [tree 09ba3246ae3f] (2026-11-04T14:13:06Z)
- (audit self) `self: the start emit now prints its text and carries project and root; test_code's event-order tests still pass with the printed line` → no findings [tree 09ba3246ae3f] (2026-11-04T14:13:06Z)
## Log
- 2026-11-03T00:44:22Z created
- 2026-11-03T00:46:33Z planned from capture
- 2026-11-03T00:46:38Z set depends_on=['T-1476']
- 2026-11-03T01:00:24Z set depends_on=['T-2742']
- 2026-11-04T14:01:55Z focused
- 2026-11-04T14:01:56Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T14:14:34Z done
- 2026-11-04T14:14:36Z committed 36c83154 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1344 [FEATURE M, done, 3 steps] fm code home ranked by need, with a changed-since line and type-to-jump — lesson: A request with several clauses needs each clause as a…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_code.py
- plugin/lib/sampo/smith.py
- CHANGELOG.md
