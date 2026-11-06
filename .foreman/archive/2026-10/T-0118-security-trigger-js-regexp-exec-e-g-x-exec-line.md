---
id: T-0118
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-03T03:48:42Z
updated: 2026-10-03T03:58:38Z
base: 781cab45591ed1f9b520065af00855ef32f91fad
verified: ok
---
# Security trigger: a JS regex literal's .exec( is not code execution
## Raw request
> Security trigger: JS RegExp .exec( (e.g. /x/.exec(line)) reads as exec() code execution; skip method calls on a regex or identifier
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] regex-literal .exec( not flagged; child_process exec and bare exec( still are — verify with `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then strip regex-literal .exec( before matching
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py -k regex_literal_exec` → ✗ exit 1 · Ran 1 test in 0.008s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree daec3ab18489] (2026-10-03T03:49:18Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py -k regex_literal_exec` → ✗ exit 1 · Ran 1 test in 0.009s / FAILED (failures=1) [ran] [tree daec3ab18489] (2026-10-03T03:49:18Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py -k regex_literal_exec` → ✗ exit 1 · Ran 1 test in 0.007s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree a7c4b7cb5c39] (2026-10-03T03:55:14Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py -k regex_literal_exec` → exit 0 · Ran 1 test in 0.011s / OK [ran] [tree a7c4b7cb5c39] (2026-10-03T03:55:14Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py` → exit 0 · Ran 8 tests in 3.014s / OK [ran] [tree a7c4b7cb5c39] (2026-10-03T03:55:17Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py` → pass (2026-10-03T03:55:17Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q -p test_round_i.py` → exit 0 · Ran 8 tests in 3.060s / OK [ran] [tree a7c4b7cb5c39] (2026-10-03T03:58:38Z)
- (audit self) `self: only /…/flags.exec( is stripped, after string literals are blanked; bare exec( and child_process.exec( still flag (tested)` → no findings [tree a7c4b7cb5c39] (2026-10-03T03:58:38Z)
## Log
- 2026-10-03T03:48:42Z created
- 2026-10-03T03:49:13Z planned from capture
- 2026-10-03T03:49:13Z focused
- 2026-10-03T03:55:06Z user approved core in Claude Code's permission prompt
- 2026-10-03T03:58:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r2-edge: ect, not just the offending one. Fix: `gates = {shape(x) for x in (c.read_meta(p).get(\"checks\") or []) if isinstance(x, str)}`, and/or wrap `ch…
- research t0036-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:341-364` (`_pin_problem`) and `~/.claude/foreman/plugin/lib/fmguard.py…
- playbook Security Bounty Hunter (skills/playbooks/references/security/bounty-triage.md)
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
## Files touched
- plugin/tests/test_round_i.py
- plugin/lib/fmcore.py
