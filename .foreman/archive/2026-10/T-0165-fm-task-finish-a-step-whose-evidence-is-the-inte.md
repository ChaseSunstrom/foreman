---
id: T-0165
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_round_i.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T08:17:54Z
updated: 2026-10-03T08:21:54Z
base: 96d4fad48188b66a5f619f3be7312e0040cb4953
base_tree: 45b0ccbcef1758dcc6187414a6e7689fcf492c30
verified: strong
---
# A step whose newest run failed closes when the same command passed later (the red run of red→green)
## Raw request
> fm task finish: a step whose evidence is the intended red run should close when the same command later passed (for the next step), instead of asking for its own passing run (T-0164)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A task whose step 1 holds the intended red run and step 2 the same command passing finishes without another run; a later failure of that command still refuses — verify with `python3 plugin/tests/run.py -k test_round_i`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] _refuse_failed_run accepts a later pass of the same command
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_red_step -k test_a_later_failure` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RoundI 1s) / OK [ran] [tree 88d813967137] (2026-10-03T08:20:42Z)
- (step 2) `python3 plugin/tests/run.py -k test_round_i` → exit 0 · Ran 12 tests in 4.2s (1 classes, 16 at a time; slowest: RoundI 4s) / OK [ran] [tree 29150495fd5b] (2026-10-03T08:21:50Z)
- (step 3) `grep -q T-0165 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 29150495fd5b] (2026-10-03T08:21:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_round_i` → exit 0 · Ran 12 tests in 4.2s (1 classes, 16 at a time; slowest: RoundI 4s) / OK [ran] [tree 29150495fd5b] (2026-10-03T08:21:54Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:21 UTC); cached (fm check --fresh reruns) [ran] [tree 29150495fd5b] (2026-10-03T08:21:54Z)
- (audit adversary) `self: the pass must be a fm-run ((ran]) of the identical command recorded after the failure; a failure after the pass still refuses (test); applies to criteria too, since they share _refuse_failed_run` → typed evidence can't clear a failure (only (ran] lines count), and the command text must match exactly, so a different, weaker command can't stand in [tree 29150495fd5b] (2026-10-03T08:21:54Z)
- (audit self) `self: the pass must be a fm-run ((ran]) of the identical command recorded after the failure; a failure after the pass still refuses (test); applies to criteria too, since they share _refuse_failed_run` → no findings [tree 29150495fd5b] (2026-10-03T08:21:54Z)
## Log
- 2026-10-03T08:17:54Z created
- 2026-10-03T08:20:27Z planned from capture
- 2026-10-03T08:20:27Z focused
- 2026-10-03T08:21:54Z done
- 2026-10-03T08:21:54Z committed 3b20e5b (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Evidence rules should follow the check, not the slot it was recorded under: a later pass of the same command is fresher proof.
## Files touched
- plugin/tests/test_round_i.py
- plugin/lib/fmcore.py
- CHANGELOG.md
