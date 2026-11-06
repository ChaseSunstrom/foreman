---
id: T-0354
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T04:52:30Z
updated: 2026-10-06T04:57:10Z
base: 73caa057ac5da3e72d05b8db7ca574bf6fb90b8b
base_tree: 081fd00c56605b058aa79a753354c1b58e2b1a42
verified: strong
---
# Guard: the curl-into-python data exemption also refuses a folder that shadows any standard-library module
## Raw request
> Guard: the curl-into-python data exemption also refuses a folder that shadows any standard-library module
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a folder holding enum.py (or any X.py / X/__init__.py named like a stdlib module) makes curl … | python3 -c CODE pipe-shell again; a plain folder named like one doesn't — verify with `python3 plugin/tests/run.py -k test_guard.FrictionFalseBlocks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.FrictionFalseBlocks` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: FrictionFalseBlocks 0s) / FAILED (1 classes) [ran] [tree dec4d74d3c1e] (2026-10-06T04:52:56Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.FrictionFalseBlocks` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: FrictionFalseBlocks 0s) / OK [ran] [tree cea9473299db] (2026-10-06T04:57:09Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard.FrictionFalseBlocks` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: FrictionFalseBlocks 0s) / OK [ran] [tree cea9473299db] (2026-10-06T04:57:09Z)
- (audit adversary) `two automated security reviews of T-0344's exemption: transitive stdlib shadowing (enum.py under json → re → enum) and a module planted by the same command (echo > json.py, curl -o/-O, wget, sort -o, uniq OUT, curl -w %output{}) — each now voids it, test-first; from-/dotted imports were already refused by _open_targets; replay 0 newly allowed, the friction command still passes` → a module python -c imports can no longer come from the folder (any stdlib name, .py/.pyc/.so/package) or from a write earlier in the same command; curl and wget pass only with stdout-only flags [tree cea9473299db] (2026-10-06T04:57:09Z)
- (audit self) `two automated security reviews of T-0344's exemption: transitive stdlib shadowing (enum.py under json → re → enum) and a module planted by the same command (echo > json.py, curl -o/-O, wget, sort -o, uniq OUT, curl -w %output{}) — each now voids it, test-first; from-/dotted imports were already refused by _open_targets; replay 0 newly allowed, the friction command still passes` → no findings [tree cea9473299db] (2026-10-06T04:57:09Z)
## Log
- 2026-10-06T04:52:30Z created
- 2026-10-06T04:52:30Z focused
- 2026-10-06T04:57:09Z done
- 2026-10-06T04:57:10Z committed 7158e91 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- research smoke-tomllib: Asked 2026-10-04 · 1 sub-question(s) · 8 claims: 7 quote found, 1 quote not found, 0 unchecked. ✓ means the quoted words are on the cited page, n…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- An existence check at guard time says nothing about files the same command creates a moment later: rule out the writers, not just the files.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
