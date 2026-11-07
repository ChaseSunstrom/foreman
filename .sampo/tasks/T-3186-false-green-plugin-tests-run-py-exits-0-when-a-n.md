---
id: T-3186
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T09:37:52Z
updated: 2026-11-05T11:44:08Z
base: 649c130fd5512e2b371e1ec37198dca24c3ba6e4
base_tree: 946756ed98ad467484520834dd9e75a8aeb7b3c0
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T11:43:15Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# run.py exits non-zero when a named test module, class or test matches nothing, so a criterion naming a missing test can't pass
## Raw request
> False green: plugin/tests/run.py exits 0 when a named test module or test doesn't exist ('no test matches'), so a criterion's verify command naming a missing test (e.g. test_callcards_seed, test_landlock) passes; a named target that matches nothing must exit non-zero
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 plugin/tests/run.py <a name that matches no test> exits non-zero and names what matched nothing; a run with no names (the whole suite) is unchanged — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: run.py test_does_not_exist exits non-zero
2. [x] the check in run.py
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run.UnknownNames` → exit 0 · Ran 4 tests in 2.2s (4 jobs, 16 at a time; slowest: UnknownNames.test_a_name_whose_tests_a_k_filters_out_names_the_k 2s, UnknownNames.test_a_red_runs_last_line_names_the_failing_class 1s, UnknownNames [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:43:25Z)
- (step 2) `bash -c 'for n in test_does_not_exist test_run.NoSuchClass test_run.PerTestJobs.test_nope; do python3 plugin/tests/run.py $n >/dev/null 2>&1; r=$?; echo "$n -> $r"; [ $r -ne 0 ] || exit 1; done'` → exit 0 · test_run.NoSuchClass -> 1 / test_run.PerTestJobs.test_nope -> 1 [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:43:27Z)
- `bash -c 'cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wt-3186 && python3 plugin/tests/run.py test_does_not_exist >/dev/null 2>&1; r=$?; echo before T-3166 at ac225cad: run.py test_does_not_exist exits $r; [ $r -ne 0 ]'` → exit 0 · before T-3166 at ac225cad: run.py test_does_not_exist exits 1 [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:43:44Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 89 tests in 8.4s (62 jobs, 16 at a time; slowest: Bench 6s, UnknownNames 5s, State 5s) / OK [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:44:04Z)
- (audit edge) `premise checked: plain unknown names already exited 1 before T-3166 (ac225cad, detached worktree); on main module, class and method names each exit 1 and are named; test_run.UnknownNames covers it, including a -k that filters a name to nothing` → module, class and method names each exit 1; a name a -k filters to nothing names the -k [tree 946756ed98ad] (2026-11-05T11:44:04Z)
- (audit self) `premise checked: plain unknown names already exited 1 before T-3166 (ac225cad, detached worktree); on main module, class and method names each exit 1 and are named; test_run.UnknownNames covers it, including a -k that filters a name to nothing` → no findings [tree 946756ed98ad] (2026-11-05T11:44:04Z)
## Log
- 2026-11-05T09:37:52Z created
- 2026-11-05T09:39:45Z planned from capture
- 2026-11-05T09:39:45Z set approved=True
- 2026-11-05T09:39:50Z blocked: planned and approved; touches run.py like T-3166 (queued to merge), so a builder takes it after T-3166 lands
- 2026-11-05T11:43:14Z focused
- 2026-11-05T11:43:15Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:44:08Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1287 [FIX S, done, 1 steps] Plugin/tests/run.py exits 0 when one of several named test modules doesn't exist (run.py t — lesson: A runner that treats names as filters …
- T-2606 [FIX S, done, 2 steps] A criterion whose every recorded run matched no test can have its verify command edited: a command that measured nothing weakens no check —…
- research T-2630-review: Verdict:** approve with nits. I read the worktree files directly, because I had no way to run `git diff`. The code behaves as the brief intends. …
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_moons_scale test_night] A target counts the outcome the user named (kept, closed, passing, used), never an …
## Regression test
none new: at ac225cad (just before T-3166) run.py test_does_not_exist already exited 1, so the false green didn't reproduce for plain names; test_run.UnknownNames (added by T-3166) pins module, class, method and -k-filtered names exiting 1
