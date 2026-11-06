---
id: T-2263
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2262]
source: followup
created: 2026-10-31T03:43:20Z
updated: 2026-10-31T06:15:39Z
base: f03acae61becba64bf49b377a2183b23616c7113
base_tree: e378dcf59981029d19e266db31fdfbf591ad672a
plan0_at: 2026-10-31T05:47:10Z
plan0_scope: []
verified: strong
---
# Long-horizon exam (3/3): per-goal metrics and the deciding scorecard row
## Raw request
> Long-horizon exam (3/3): per-goal metrics and the deciding scorecard row
## Interpretation
Slice 3 of the long-horizon tier (gen-0 DONE-WHEN: the deciding end-of-run score). fmlong.grade today reports true_done and regressions per goal; the session arms (T-2262) log faults, resumes and cost per goal in faults/AGENT/ID.json and the session's reply. Missing: false-done claims (the session said done while the hidden checks fail), interventions (resumes a person had to make), time to the first true-done, guard-worthy actions attempted, cost, and a scorecard row that puts foreman and plain side by side on the same goals as the deciding row.
## Assumptions (confidence)
## Acceptance criteria
- [x] grade reports per finished goal: true-done rate, false-done claims (the session said done while hidden checks fail), regressions and reverts, human interventions (resumes a person had to make), hours to the first true-done, guard-worthy actions attempted (guard blocks in the run's ledger), cost; fm exam scorecard and fm genesis status show the long tier as the deciding row, foreman vs plain on the same goals — verify with `python3 plugin/tests/run.py test_long test_genesis`
## Non-goals
## Approach (options → choice → why)
1) extend grade per goal from what the run already stores: false_done = the session's final reply claims done (fmexam's claims-done reader or the reply's done flag) while true_done is false; interventions = resumes the fault log marks as needing a person (none for scripted faults, counted from a resume the run didn't plan); minutes to first true-done from the run's turn timestamps; guard blocks from the session transcript's or the run ledger's guard events; cost summed from the fault log (unknown counted apart). fmgenesis.scorecard and fm genesis status gain a 'long' row (deciding): foreman vs plain on the same run's goals, true-done rate, false-done count, regressions, cost; a Haiku-stamped line never decides (fmgenesis.smoke). 2) a separate long scorecard verb — rejected: the deciding row belongs in the one scorecard the §8 report reads. 3) re-run sessions to measure time — rejected: costs the exam twice; the run's timestamps suffice. Choice 1.
## Risks and rollback
A metric with no source in a run (e.g. guard blocks when the transcript is gone) reads 'unknown', never 0. Rollback: the row is additive.
## Execution prompt
## Steps
1. [x] red tests from seeded run logs
2. [x] metrics in grade; the scorecard row
3. [x] docs (MASTER, CHANGELOG, site Genesis page)
## Resume here
<!-- auto -->
- 2026-10-31T05:55:20Z step 1/3: red tests from seeded run logs
- git: worktree-agent-a2b4b8a2859329c99; 7 uncommitted: MASTER.md, plugin/lib/fmgenesis.py, plugin/lib/fmlong.py, plugin/tests/genesis_page.js, plugin/tests/test_genesis.py, plugin/tests/test_long.py, plugin/tests/test_site_build.py
- touched since last checkpoint: plugin/lib/fmexam.py, plugin/tests/test_long.py, plugin/tests/test_genesis.py, plugin/lib/fmlong.py, plugin/lib/fmgenesis.py, MASTER.md, plugin/tests/genesis_page.js, plugin/tests/test_site_build.py
## Docs impact
MASTER.md, CHANGELOG.md, site/genesis/genesis.js
## Verification evidence
- `python3 plugin/tests/run.py test_long test_genesis` → exit 0 · Ran 182 tests in 19.0s (24 classes, 16 at a time; slowest: Long 18s, GenesisRead 8s, GenesisCheck 7s) / OK (start tree + this task's tests) [ran] [tree e378dcf59981] (2026-10-31T06:03:58Z)
- `python3 plugin/tests/run.py test_long test_genesis` → exit 0 · Ran 182 tests in 23.3s (24 classes, 16 at a time; slowest: Long 23s, GenesisRead 11s, GenesisCheck 10s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:03:58Z)
- (step 1) `python3 plugin/tests/run.py test_long test_genesis test_exam test_site_build` → exit 0 · Ran 234 tests in 71.5s (42 classes, 16 at a time; slowest: ExamAuthors 71s, ExamGen 56s, Long 32s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:05:10Z)
- (step 2) `python3 plugin/tests/run.py test_long test_genesis test_exam test_site_build` → exit 0 · Ran 234 tests in 72.4s (42 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 57s, Long 32s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:06:23Z)
- (step 3) `python3 plugin/tests/run.py test_long test_genesis test_exam test_site_build 2>&1 | tail -8` → exit 0 · Ran 238 tests in 74.0s (42 classes, 16 at a time; slowest: ExamAuthors 73s, ExamGen 57s, Long 39s) / OK [ran] [tree 06209901d4b5] (2026-10-31T06:07:58Z)
- `python3 plugin/tests/run.py test_long test_genesis` → ✗ exit 1 · Ran 186 tests in 23.9s (24 classes, 16 at a time; slowest: Long 23s, GenesisRead 8s, GenesisCheck 7s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 06209901d4b5] (2026-10-31T06:09:51Z)
- `python3 plugin/tests/run.py test_long test_genesis` → exit 0 · Ran 186 tests in 23.2s (24 classes, 16 at a time; slowest: Long 23s, GenesisRead 9s, GenesisCheck 8s) / OK [ran] [tree 06209901d4b5] (2026-10-31T06:09:51Z)
- (step 1) `python3 plugin/tests/run.py test_long test_genesis test_exam test_site_build` → exit 0 · Ran 238 tests in 64.3s (42 classes, 16 at a time; slowest: ExamAuthors 64s, ExamGen 53s, Long 31s) / OK [ran] [tree 06209901d4b5] (2026-10-31T06:10:56Z)
- (step 2) `python3 plugin/tests/run.py test_long test_genesis test_exam test_site_build` → exit 0 · Ran 238 tests in 64.4s (42 classes, 16 at a time; slowest: ExamAuthors 64s, ExamGen 52s, Long 30s) / OK [ran] [tree 06209901d4b5] (2026-10-31T06:12:00Z)
- (step 3) `grep -c T-2263 MASTER.md CHANGELOG.md site/genesis/genesis.js` → exit 0 · CHANGELOG.md:1 / site/genesis/genesis.js:1 [ran] [tree 06209901d4b5] (2026-10-31T06:12:00Z)
- (ac 1) `python3 plugin/tests/run.py test_long test_genesis` → exit 0 · Ran 186 tests in 45.1s (24 classes, 16 at a time; slowest: Long 45s, GenesisRead 18s, GenesisCheck 14s) / OK [ran] [tree 06209901d4b5] (2026-10-31T06:13:37Z)
- (audit intent) `self + follow-ups after the builder's report: interventions split into resumes_needed and unfinished; the site page renders the long row (textContent only, no outside hosts); merge conflict with T-2273 resolved keeping both fields` → the long-horizon tier is the deciding row: per goal true-done, false-done, resumes needed, unfinished, hours to done, guard blocks, cost; foreman vs plain on the same goals; behind fails the card; a Haiku line never decides (test_long, test_genesis red-to-green) [tree 06209901d4b5] (2026-10-31T06:13:37Z)
- (audit adversary) `self + follow-ups after the builder's report: interventions split into resumes_needed and unfinished; the site page renders the long row (textContent only, no outside hosts); merge conflict with T-2273 resolved keeping both fields` → run info is data the run wrote, type-checked at grade; the page treats genesis.json as text only [tree 06209901d4b5] (2026-10-31T06:13:37Z)
- (audit edge) `self + follow-ups after the builder's report: interventions split into resumes_needed and unfinished; the site page renders the long row (textContent only, no outside hosts); merge conflict with T-2273 resolved keeping both fields` → anything a run can't compute is unknown, never 0; reverts unknown (the final tree keeps no history); hours_to_done is an upper bound [tree 06209901d4b5] (2026-10-31T06:13:37Z)
## Log
- 2026-10-31T03:43:20Z created
- 2026-10-31T03:43:25Z set depends_on=['T-2262']
- 2026-10-31T05:46:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2263.builder.md
- 2026-10-31T05:47:09Z focused
- 2026-10-31T06:08:57Z merged worktree-agent-a2b4b8a2859329c99 (11 file(s))
- 2026-10-31T06:08:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2b4b8a2859329c99
- 2026-10-31T06:08:57Z focused
- 2026-10-31T06:12:51Z scope: plugin/lib/fmlong.py (_metrics, _totals, run info), plugin/lib/fmgenesis.py (long_row, card_long, status/export), plugin/lib/fmexam.py (scorecard text), site/genesis/genesis.js + index.html (long row), plugin/tests/test_long.py, test_genesis.py, test_site_build.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:15:39Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
- T-2258 [FEATURE M, done, 3 steps] Long-horizon exam (1/3): fm exam long gen/run/grade from local git history, oracle and empty arms — lesson: A held-out check built from…
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
- T-2262 [FEATURE M, done, 3 steps] Long-horizon exam (2/3): session arms foreman and plain with planted faults — lesson: A fault-injection harness must log whether each f…
## Lessons
- A deciding metric must not merge different events: 'stopped short' and 'a person had to step in' read the same only until someone acts on the number
## Files touched
- plugin/tests/test_long.py
- plugin/tests/test_genesis.py
- plugin/lib/fmlong.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmexam.py
- MASTER.md
- plugin/tests/genesis_page.js
- plugin/tests/test_site_build.py
- site/genesis/genesis.js
- site/genesis/index.html
- CHANGELOG.md
- .gitignore
- README.md
- plugin/agents/fm-builder.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/tests/test_docs.py
- plugin/tests/test_proof.py
