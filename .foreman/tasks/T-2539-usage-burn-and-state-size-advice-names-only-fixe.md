---
id: T-2539
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T04:35:24Z
updated: 2026-11-02T05:08:14Z
batch: [T-2537, T-2538]
base: 912d89cca38abdd21556f2ac1e6f71ca0b6f70f3
base_tree: 6205a9436f420cd41b6446918cf3928e8ada3c5b
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T04:41:24Z
plan0_scope: []
verified: strong
---
# Usage-burn and state-size advice names only fixes that act here: the user's own compact window, and the exam/ part tidy…
## Raw request
> T-2537: fm cost/doctor's usage-burn advice says 'fm install-user sets Foreman's 200k compact window', a no-op when the user's settings set CLAUDE_CODE_AUTO_COMPACT_WINDOW higher on purpose (1000000, the user's 2026-10-30 ask); name the user's window and advise /compact at task boundaries instead (fmcost.py:199)
> T-2538: fm doctor's state-size row says 'fm tidy --apply prunes and rolls it' when most of the size is exam/ (2328 MB of long-exam work copies: exam/long/l001-l003), which fm tidy never touches (fmdoctor.py:349); name what tidy can't reach
## Interpretation
Reading 1: do T-2537, T-2538 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2539. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670). Reading 2: each one alone; ruled out because one plan read and one gate run serve them all cheaper.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2537: fm cost/doctor's usage-burn advice says 'fm install-user sets Foreman's 200k compact… works — verify with `python3 plugin/tests/run.py test_usage_burn test_cost`
- [x] T-2538: fm doctor's state-size row says 'fm tidy --apply prunes and rolls it' when most of the… works — verify with `python3 plugin/tests/run.py test_doctor.DoctorStateSize`
- [x] with CLAUDE_CODE_AUTO_COMPACT_WINDOW above Foreman's 200k in the environment, fm cost's usage-burn advice names that window as the user's and advises /compact at task boundaries, not fm install-user; at or below 200k (or unset) the old advice stays — verify with `python3 plugin/tests/run.py test_cost`
- [x] when a project's largest state part is exam/, the doctor's state-size row says fm tidy doesn't prune exam runs and names the part; other parts keep the tidy advice — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2537: fm cost/doctor's usage-burn advice says 'fm install-user sets Foreman's 200k compact…
2. [x] T-2538: fm doctor's state-size row says 'fm tidy --apply prunes and rolls it' when most of the…
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_usage_burn.UsageBurn.test_a_window_the_user_set_above_foremans_is_named_not_install_user` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: UsageBurn 0s) / FAILED (1 classes: test_usage_burn.UsageBurn) [ran] [tree a08473cc4b9e] [world 2f1906870a] (2026-11-02T04:41:36Z)
- (step 2) `python3 plugin/tests/run.py test_doctor.DoctorStateSize` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / FAILED (1 classes: test_doctor.DoctorStateSize) [ran] [tree a08473cc4b9e] [world 2f1906870a] (2026-11-02T04:41:37Z)
- (step 1) `python3 plugin/tests/run.py test_usage_burn test_cost` → ✗ exit 1 · Ran 25 tests in 8.4s (9 classes, 16 at a time; slowest: TaskCostCap 8s, SkillUsage 3s, CostForecast 1s) / FAILED (1 classes: test_usage_burn.UsageBurn) [ran] [tree 7217a12a45be] [world 2f1906870a] (2026-11-02T04:42:13Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 104 tests in 4.1s (34 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree 7217a12a45be] [world 2f1906870a] (2026-11-02T04:42:18Z)
- (step 1) `python3 plugin/tests/run.py test_usage_burn test_cost` → exit 0 · Ran 25 tests in 8.0s (9 classes, 16 at a time; slowest: TaskCostCap 8s, SkillUsage 2s, CostForecast 1s) / OK [ran] [tree 38e294d3e3db] [world 2f1906870a] (2026-11-02T04:42:36Z)
- (ac 1) `python3 plugin/tests/run.py test_usage_burn test_cost` → exit 0 · Ran 25 tests in 7.0s (9 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 2s, CostForecast 0s) / OK [ran] [tree 7e4e01da5928] [world 2f1906870a] (2026-11-02T04:49:05Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor.DoctorStateSize` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / OK [ran] [tree 7e4e01da5928] [world 2f1906870a] (2026-11-02T04:49:05Z)
- (ac 3) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 20 tests in 6.9s (7 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 2s, CostForecast 0s) / OK [ran] [tree 7e4e01da5928] [world 2f1906870a] (2026-11-02T04:49:05Z)
- (ac 4) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 104 tests in 4.1s (34 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree 7e4e01da5928] [world 2f1906870a] (2026-11-02T04:49:05Z)
- (audit edge) `self-review: the burn advice reads the window from the environment first, then settings.json; only a window above Foreman's 200k changes the advice; the state-size row names exam/ only when it is the largest part` → no window anywhere keeps the install-user advice; a window at Foreman's 200k drops it (already set); an unreadable settings.json reads as no window; a project whose biggest part is research keeps the tidy advice [tree 7e4e01da5928] (2026-11-02T04:49:05Z)
- (audit self) `self-review: the burn advice reads the window from the environment first, then settings.json; only a window above Foreman's 200k changes the advice; the state-size row names exam/ only when it is the largest part` → no findings [tree 7e4e01da5928] (2026-11-02T04:49:05Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree a452a4909a68] [world 2f1906870a] (2026-11-02T05:08:14Z)
## Log
- 2026-11-02T04:35:24Z created
- 2026-11-02T04:35:32Z set tier=S
- 2026-11-02T04:35:53Z step 6 removed: remove
- 2026-11-02T04:35:54Z step 5 removed: remove
- 2026-11-02T04:35:54Z step 4 removed: fmcost reads the window from the environment (fmsetup.COMPACT_WINDOW as the line); fmdoctor's state-size row names exam/ as out of tidy's reach
- 2026-11-02T04:35:54Z step 3 removed: red tests: test_cost (window 1000000 vs unset) and test_doctor (an exam/ heavy project vs a ledger heavy one)
- 2026-11-02T04:41:24Z focused
- 2026-11-02T04:41:24Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T04:42:43Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_usage_burn test_cost`
- 2026-11-02T04:42:43Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_doctor.DoctorStateSize`
- 2026-11-02T04:42:57Z scope: fmcost._window reads CLAUDE_CODE_AUTO_COMPACT_WINDOW (env, else settings.json env) and burn_findings' fix names a user window above fmsetup.COMPACT_WINDOW; fmdoctor.check_state_size names exam/ as out of tidy's reach; tests in test_usage_burn and test_doctor
- 2026-11-02T04:49:27Z done
- 2026-11-02T04:49:30Z committed bff2c77d (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-2493 [FIX S, done, 2 steps] Two fm CLI fixes: fm decide refuses a user-steer row without --check; a mistyped flag's hint names only the typed comma… — lesson: Say a ga…
- T-2296 [FEATURE M, done, 2 steps] Batch: The friction digest's guard example is …; Fmfriction give-up lines name task ids … — lesson: A test must log through the same fu…
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
## Lessons
- advice that names a fix must check the fix acts here; a command that respects a user's explicit value is a no-op as advice against that value
## Plan gaps
- failed first: step 1 T-2537: fm cost/doctor's usage-burn advice says 'fm install-user sets Foreman's 200k compact…
- failed first: step 2 T-2538: fm doctor's state-size row says 'fm tidy --apply prunes and rolls it' when most of the…
## Files touched
- plugin/tests/test_usage_burn.py
- plugin/tests/test_doctor.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
