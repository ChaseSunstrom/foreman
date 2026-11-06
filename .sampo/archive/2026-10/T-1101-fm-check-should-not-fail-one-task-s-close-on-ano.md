---
id: T-1101
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/run.py, plugin/tests/test_check_paths.py]
depends_on: []
source: self
created: 2026-10-16T04:52:15Z
updated: 2026-10-16T05:36:35Z
base: fc4d390035c49096f06da261f685bc1f9786cd15
base_tree: 6790c65645a4ae7ad253b5f7cccab6e6638e3143
verified: strong
---
# Fm check should not fail one task's close on another checkpointed task's recorded red test
## Raw request
> fm check should not fail one task's close on another checkpointed task's recorded red tests (its step-1 failing evidence): the suite run excludes test files that are only another open task's red-first tests, and says so, instead of making Claude park files by hand
## Interpretation
`fm check` runs the gates as stored strings (fmcli.py:3066-3074). With the project's suite as a gate, another open task's recorded failing tests fail this task's close. The user gets a run that leaves those test files out and says so. Already covered: `run.py` takes names and `-k` (run.py:46-56) but has no exclude option; `c.run_command` accepts `env` (fmcore.py:429); step evidence has the `(step N)` tag, the cmd and a ✗ mark (fmcore.py:903, 1206-1212).
## Assumptions (confidence)
## Acceptance criteria
- [x] With task B holding step-1 red evidence for `test_x`, `fm check` for task A passes and names `test_x` as skipped — verify with `python3 plugin/tests/run.py test_check_paths`
- [x] `run.py` honours `FOREMAN_SKIP_TESTS` — verify with `python3 plugin/tests/run.py test_check_paths`
## Non-goals
## Approach (options → choice → why)
(a) Rewrite the gate command. This is fragile with arbitrary strings. (b) Pass the exclusions in an env var that `run.py` honours. (c) Park the files by hand, which is today's behaviour. Choice: (b). - New `red_first_tests(p, act)` in fmcli.py. For every other brief with status in `c.OPEN` and not the active one, it reads step-1 evidence lines that are ✗ and whose cmd contains `tests/run.py`, takes the module names, and keeps only names with no passing evidence line. Names that also appear in the active task's evidence or scope are never excluded. - `cmd_check` passes `env={**os.environ, "FOREMAN_SKIP_TESTS": "a,b"}` to `run_command`. - `run.py` `classes()` drops modules in that env var. - Output gains a line "skipped N test file(s) that are only task T-XXXX's red-first tests: …".
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_check_paths.py (or a new test_check_skip.py): `run.py` with the env var omits the module; `fm check` output contains "skipped".
2. [x] Implement `red_first_tests`, the env pass-through and the `run.py` filter.
## Resume here
## Docs impact
README.md fm check line; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_check_skip` → ✗ exit 1 · Ran 2 tests in 2.3s (1 classes, 16 at a time; slowest: CheckSkip 2s) / FAILED (1 classes) [ran] [tree 03872deb7c87] (2026-10-16T05:15:40Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.3s (2 classes, 16 at a time; slowest: CheckSkip 3s, CheckPaths 2s) / OK [ran] [tree 89267202333b] (2026-10-16T05:19:01Z)
- (ac 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.4s (2 classes, 16 at a time; slowest: CheckSkip 3s, CheckPaths 2s) / OK [ran] [tree 89267202333b] (2026-10-16T05:19:08Z)
- (ac 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.3s (2 classes, 16 at a time; slowest: CheckSkip 3s, CheckPaths 2s) / OK [ran] [tree 89267202333b] (2026-10-16T05:19:11Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.9s (2 classes, 16 at a time; slowest: CheckSkip 4s, CheckPaths 2s) / OK [ran] [tree bc552d184c38] (2026-10-16T05:20:22Z)
- (ac 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.9s (2 classes, 16 at a time; slowest: CheckSkip 4s, CheckPaths 2s) / OK [ran] [tree bc552d184c38] (2026-10-16T05:20:26Z)
- (ac 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 7 tests in 3.3s (2 classes, 16 at a time; slowest: CheckSkip 3s, CheckPaths 2s) / OK [ran] [tree bc552d184c38] (2026-10-16T05:20:30Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths` → ✗ exit 1 · Ran 10 tests in 7.2s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 3s) / FAILED (1 classes) [ran] [tree f8233df04789] (2026-10-16T05:31:25Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 6.0s (2 classes, 16 at a time; slowest: CheckSkip 6s, CheckPaths 2s) / OK [ran] [tree 9543e21686a4] (2026-10-16T05:32:23Z)
- (ac 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 6.1s (2 classes, 16 at a time; slowest: CheckSkip 6s, CheckPaths 2s) / OK [ran] [tree 9543e21686a4] (2026-10-16T05:32:30Z)
- (ac 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 5.8s (2 classes, 16 at a time; slowest: CheckSkip 6s, CheckPaths 2s) / OK [ran] [tree 9543e21686a4] (2026-10-16T05:32:36Z)
- (ac 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 7.4s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 2s) / OK [ran] [tree 2ca0aba5d3f1] (2026-10-16T05:36:35Z)
- (ac 2) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 7.4s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 2s) / OK [ran] [tree 2ca0aba5d3f1] (2026-10-16T05:36:35Z)
- (step 1) `python3 plugin/tests/run.py test_check_paths` → exit 0 · Ran 10 tests in 7.4s (2 classes, 16 at a time; slowest: CheckSkip 7s, CheckPaths 2s) / OK [ran] [tree 2ca0aba5d3f1] (2026-10-16T05:36:35Z)
- (audit self) `review: one fm-reviewer full pass; 3 findings (cache key overwritten, look-alike tests folder, inherited env) fixed by the builder test-first` → no findings [tree 2ca0aba5d3f1] (2026-10-16T05:36:35Z)
## Log
- 2026-10-16T04:52:15Z created
- 2026-10-16T05:01:17Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/run.py', 'plugin/tests/test_check_paths.py']
- 2026-10-16T05:01:17Z set tier=S
- 2026-10-16T05:11:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1101.builder.md
- 2026-10-16T05:11:51Z focused
- 2026-10-16T05:15:11Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/run.py', 'plugin/tests/test_check_paths.py', 'plugin/tests/test_check_skip.py']
- 2026-10-16T05:15:11Z scope: the tests go in a new plugin/tests/test_check_skip.py, as the brief's step 1 offers
- 2026-10-16T05:18:57Z tests moved into test_check_paths.py (CheckSkip), so the criteria's verify command runs them; test_check_skip.py dropped
- 2026-10-16T05:18:58Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/run.py', 'plugin/tests/test_check_paths.py']
- 2026-10-16T05:31:17Z review fixes (coordinator): gate loop's skip shadowed the red-first set; proof by folder not bare name; inherited FOREMAN_SKIP_TESTS stripped
- 2026-10-16T05:36:17Z merged worktree-agent-a03a910084fabdd00 (3 file(s))
- 2026-10-16T05:36:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a03a910084fabdd00
- 2026-10-16T05:36:20Z focused
- 2026-10-16T05:36:26Z scope: README.md, CHANGELOG.md — docs for the skip
- 2026-10-16T05:36:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmtidy.py changed since it was written]
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
- start here (files T-0808 touched): plugin/tests/test_run.py, plugin/lib/fmlanes.py, plugin/tests/run.py, plugin/tests/test_lanes.py
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A loop variable that reuses an outer name silently changes what a later cache key records: name loop locals for the loop
## Plan gaps
- failed first: step 1 Failing tests in test_check_paths.py (or a new test_check_skip.py): `run.py` with the env var omits…
## Files touched
- plugin/tests/test_check_skip.py
- plugin/tests/run.py
- plugin/lib/fmcli.py
- plugin/tests/test_check_paths.py
- CHANGELOG.md
- README.md
