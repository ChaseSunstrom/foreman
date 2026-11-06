---
id: T-0142
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_round_i.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-03T05:51:31Z
updated: 2026-10-03T06:24:43Z
base: 34622efa650ce21892fe2998b46b59a945658222
base_tree: 730835bdb2bcd6d952155c6cff758b85459a8b17
verified: strong
---
# fm task finish closes a step that already has evidence, and names what still needs --run
## Raw request
> fm task finish says 'give --run: a step or criterion has no verify command of its own' without naming which, even after step evidence is recorded; name the step/criterion and accept recorded evidence
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a step with evidence recorded by fm task evidence --step closes in finish without --run; a step or criterion with neither names itself in the error — verify with `python3 plugin/tests/run.py -p test_round_i.py -k finish`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- `python3 plugin/tests/run.py -p test_round_i.py -k finish` → ✗ exit 1 · Ran 4 tests in 1.0s (1 classes, 16 at a time; slowest: RoundI 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree adca9f345e63] (2026-10-03T06:23:23Z)
- `python3 plugin/tests/run.py -p test_round_i.py -k finish` → ✗ exit 1 · Ran 4 tests in 0.9s (1 classes, 16 at a time; slowest: RoundI 1s) / FAILED (1 classes) [ran] [tree adca9f345e63] (2026-10-03T06:23:23Z)
- `python3 plugin/tests/run.py -p test_round_i.py -k finish` → ✗ exit 1 · Ran 4 tests in 1.0s (1 classes, 16 at a time; slowest: RoundI 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b86b615f8e65] (2026-10-03T06:23:58Z)
- `python3 plugin/tests/run.py -p test_round_i.py -k finish` → exit 0 · Ran 4 tests in 1.0s (1 classes, 16 at a time; slowest: RoundI 1s) / OK [ran] [tree b86b615f8e65] (2026-10-03T06:23:58Z)
- (ac 1) `python3 plugin/tests/run.py -p test_round_i.py -k finish` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: RoundI 1s) / OK [ran] [tree b86b615f8e65] (2026-10-03T06:24:43Z)
- (step 1) `python3 plugin/tests/run.py -p test_round_i.py -k finish` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: RoundI 1s) / OK [ran] [tree b86b615f8e65] (2026-10-03T06:24:43Z)
- (audit self) `self: 15-line change in task_finish; a step closes only with evidence and no newer failed run (mark_step re-checks); the error names each missing item; the T-0129 small-task case still passes` → no findings [tree b86b615f8e65] (2026-10-03T06:24:43Z)
## Log
- 2026-10-03T05:51:31Z created
- 2026-10-03T06:23:12Z planned from capture
- 2026-10-03T06:23:13Z focused
- 2026-10-03T06:24:43Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research T-0120-review: Verdict
## Lessons
- Name the thing in an error: 'a step or criterion' cost a guess every time
## Files touched
- plugin/tests/test_round_i.py
- CHANGELOG.md
- plugin/lib/fmcli.py
