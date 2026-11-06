---
id: T-0295
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T09:02:18Z
updated: 2026-10-04T09:56:52Z
base: d32c074bd1dbbdeb10dad67d7595ed0441c0cc1c
base_tree: 7f5186dd76d843a2f0160e183588fd9a27676bf6
verified: strong
---
# CLEAN: three test-file regexes (c.TESTISH, fmbench.TEST_FILE, fmmap._TEST), four word-over
## Raw request
> CLEAN: three test-file regexes (c.TESTISH, fmbench.TEST_FILE, fmmap._TEST), four word-overlap rules (fmoutside._same, fmresearch.cross_check, fmsecond session 70%, fmrecall.covered) and four tool-less child runners (fmsecond._child, fmideas, fmresearch, fmevolve) — share one of each where the semantics match
## Interpretation
One definition each where two places mean the same thing: the test-file pattern (fmbench.TEST_FILE and fmmap._TEST become c.TESTISH, the superset: __tests__/ and spec/ folders, test_* of any language) and the tool-less child runners (one parallel runner for fm ideas lenses and fm research researchers, one sequential runner for the oracle and fm second). The four word-overlap rules stay apart: each compares differently on purpose (the shorter text, the union, one side) and one rule would change verdicts.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmbench and fmmap use c.TESTISH (a __tests__/ file is a test everywhere), and every tool-less child — ideas, research, oracle, second — runs through fmideas.run_child/run_children with FOREMAN_NO_BACKGROUND=1 — verify with `python3 plugin/tests/run.py -p test_clean_helpers.py`
- [x] the ideas, research, oracle and second suites still pass — verify with `python3 plugin/tests/run.py -p 'test_ideas*' && python3 plugin/tests/run.py -p 'test_research*' && python3 plugin/tests/run.py -p 'test_oracle*' && python3 plugin/tests/run.py -p 'test_second*'`
## Non-goals
## Approach (options → choice → why)
Aliases keep the old names (no caller churn); fmideas owns child_cmd, so it gets run_child (sequential: budget check, temp cwd, run, record, error on empty) and run_children (parallel: start all, kill all on a start failure, one deadline, record each); every child runs with FOREMAN_NO_BACKGROUND=1 (fm ideas and research children didn't). Behaviour pinned by the existing ideas/research/oracle/second suites plus a test of the shared pattern and the child environment.
## Risks and rollback
## Execution prompt
## Steps
1. [x] characterization test: test_clean_helpers.py
2. [x] share the pattern and the runners
## Resume here
<!-- auto -->
- 2026-10-04T09:52:30Z steps 0/2 done
- git: foreman/build; 8 uncommitted: MASTER.md, plugin/lib/fmbench.py, plugin/lib/fmevolve.py, plugin/lib/fmideas.py, plugin/lib/fmmap.py, plugin/lib/fmresearch.py, plugin/lib/fmsecond.py, plugin/tests/test_clean_helpers.py
- touched since last checkpoint: plugin/tests/test_clean_helpers.py, plugin/lib/fmbench.py, plugin/lib/fmmap.py, plugin/lib/fmevolve.py, plugin/lib/fmresearch.py, plugin/lib/fmsecond.py, plugin/lib/fmideas.py, MASTER.md
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 09:44 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:44 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 [ran] [tree 7f5186dd76d8] (2026-10-04T09:46:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_clean_helpers.py` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: Children 0s, Pattern 0s) / OK [ran] [tree 4c25c2f760b2] (2026-10-04T09:48:52Z)
- (step 2) `python3 plugin/tests/run.py -p 'test_ideas*' && python3 plugin/tests/run.py -p 'test_research*' && python3 plugin/tests/run.py -p 'test_oracle*' && python3 plugin/tests/run.py -p 'test_second*'` → exit 0 · Ran 11 tests in 1.0s (5 classes, 16 at a time; slowest: Session 1s, Debate 0s, LensSkills 0s) / OK [ran] [tree 4c25c2f760b2] (2026-10-04T09:48:57Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.4    31.5     150  [0] / SessionEnd                  28.6    30.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 814 tests in [ran] [tree 4c25c2f760b2] (2026-10-04T09:49:50Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_clean_helpers.py && python3 plugin/tests/run.py -p 'test_ideas*' && python3 plugin/tests/run.py -p 'test_research*' && python3 plugin/tests/run.py -p 'test_oracle*' && python3 plugin/tests/run.py -p 'test_second*' && python3 plugin/tests/run.py -p 'test_evolve*'` → 10/15 hunks proven; unproven: plugin/lib/fmevolve.py @@ -11 +10,0 @@ import re; plugin/lib/fmresearch.py @@ -18 +17,0 @@ import socket; plugin/lib/fmresearch.py @@ -20 +18,0 @@ import sys; plugin/lib/fmsecond.py @@ -9,2 +8,0 @@ import re; plugin/lib/fmsecond.py @@ -12 +9,0 @@ import tempfile [inconclusive] [ran] [tree 4c25c2f760b2] (2026-10-04T09:51:37Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.9     150  [0] / SessionEnd                  28.6    29.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 818 tests in [ran] [tree 06faac1f96ed] (2026-10-04T09:56:37Z)
- (ac 1) `python3 plugin/tests/run.py -p test_clean_helpers.py` → exit 0 · Ran 6 tests in 3.4s (3 classes, 16 at a time; slowest: Failures 3s, Children 0s, Pattern 0s) / OK [ran] [tree 06faac1f96ed] (2026-10-04T09:56:51Z)
- (ac 2) `python3 plugin/tests/run.py -p 'test_ideas*' && python3 plugin/tests/run.py -p 'test_research*' && python3 plugin/tests/run.py -p 'test_oracle*' && python3 plugin/tests/run.py -p 'test_second*'` → exit 0 · Ran 11 tests in 1.1s (5 classes, 16 at a time; slowest: Session 1s, Debate 0s, LensSkills 0s) / OK [ran] [tree 06faac1f96ed] (2026-10-04T09:56:51Z)
- (audit intent) `one foreman:fm-reviewer pass (intent + maintainer), saved as T-0295-review-1; findings fixed test-first in test_clean_helpers.Failures` → both criteria met for ideas, research, oracle, second, evolve; the bench judge and soak shadow reach run_child through fmsecond._child (the review's MEDIUM docs finding refuted from fmbench.py:288/451, sentence made explicit); c.TESTISH broader by design [tree 06faac1f96ed] (2026-10-04T09:56:51Z)
- (audit maintainer) `one foreman:fm-reviewer pass (intent + maintainer), saved as T-0295-review-1; findings fixed test-first in test_clean_helpers.Failures` → error text now keeps the end of stderr on one line (_tail), no doubled 'the oracle:'/'the brainstorm children:' prefixes, research timeout rows read 'timed out: cost unknown' as before; failure paths, ledger details and evolve's child now tested [tree 06faac1f96ed] (2026-10-04T09:56:51Z)
## Log
- 2026-10-04T09:02:18Z created
- 2026-10-04T09:45:48Z focused
- 2026-10-04T09:56:52Z done
- 2026-10-04T09:56:52Z committed 1dbf080 (8 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
## Lessons
- When a refactor funnels callers through a shared runner, test each caller's failure path (exit, timeout, ledger row), not just the happy path: the visible text and records are what changes silently
## Files touched
- plugin/tests/test_clean_helpers.py
- plugin/lib/fmideas.py
- plugin/lib/fmbench.py
- plugin/lib/fmevolve.py
- plugin/lib/fmmap.py
- plugin/lib/fmresearch.py
- plugin/lib/fmsecond.py
- MASTER.md
