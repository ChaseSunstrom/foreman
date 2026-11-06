---
id: T-3265
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T02:10:18Z
updated: 2026-11-06T05:06:09Z
builder: 2026-11-06T02:21:59Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a98bd3c1b2e46bb9d
lane_branch: worktree-agent-a98bd3c1b2e46bb9d
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T02:22:49Z
plan0_scope: []
builder_returned: 2026-11-06T04:52:27Z
---
# T-3082 review fixes: night's Kalevala rounds get a wall-clock cap and a heartbeat each…
## Raw request
> T-3082 review fixes: night's Kalevala rounds get a wall-clock cap and a heartbeat each round (a round that spends nothing and never fails looped forever and doctor read the night as stale); any exception from a round stops the rounds with its reason instead of killing the night; night.jobs() survives a damaged manifest; the restart undo quotes its paths and moves the current folder aside instead of deleting it; a bare resume needs --tower or --all so it can't clear a drift pause; a halt prints its reason and exits 3; wait and slot acts are logged only when they change
## Interpretation
Reading 1 (chosen): fix the reviewer's verified findings on the merged T-3082 code before T-3082 closes, each test-first. Reading 2: re-design the loop's termination around progress tracking; rejected for now: a wall-clock cap plus the per-round beat closes the hang and the stale reading, and progress tracking can follow.
## Assumptions (confidence)
## Acceptance criteria
- [ ] night's Kalevala rounds stop at a wall-clock cap and beat the night heartbeat every round — verify with `python3 plugin/tests/run.py test_night`
- [ ] an exception from a round ends the rounds as a failed job with its reason, and a damaged manifest skips Kalevala without breaking other night jobs — verify with `python3 plugin/tests/run.py test_night`
- [ ] the restart undo quotes its paths and moves the current folder aside; a bare resume asks for --tower or --all; a halt prints its reason and exits 6 — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] A fresh tower gets past gen 0 in a round: its spec reuses the root's newest exam run read-only instead of being refused, and a failed tower job's stderr tail is kept in the round's results (2026-11-06: all 26 towers' spec jobs failed on 'exam scenarios are read-only for a Kalevala tower') — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
1) use what exists: night's stop() callback, called before every round, gains the wall-clock deadline (KALEVALA_MAX_S, default 4 h) and calls serve.beat each round; _kalevala_rounds catches Exception into a failed job row; jobs() wraps kalevala.load; the restart undo uses shlex.quote and mv to a dated aside; resume requires --tower or --all; halts exit 3 with the reason line. likely outcome: the night can't hang or go stale, and an operator reads why it stopped.
2) a watchdog thread that kills the loop after a deadline. fails if: a kill mid-round leaves a tower half-written.
3) do less: only the wall-clock cap. fails if: doctor still reports a healthy long night as stale and a bad manifest still kills every night job.
Choice 1 (85%): each fix is small and sits on a hook that already exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for each finding
2. [x] night: cap, beat, exceptions, guarded load
3. [x] kalevala: quoted undo, resume scope, halt exit, acts logged on change
## Resume here
<!-- auto -->
- 2026-11-06T04:42:42Z steps 3/3 done
- git: worktree-agent-a98bd3c1b2e46bb9d; 2 uncommitted: plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py
- touched since last checkpoint: plugin/tests/test_kalevala.py, plugin/lib/sampo/kalevala.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_night` → ✗ exit 1 · Ran 58 tests in 8.3s (17 jobs, 16 at a time; slowest: Night 7s, KalevalaNight 4s, NightInstall 3s) / FAILED (1 classes: test_night.KalevalaNight) [ran] [tree 3865e9808511] [world 2f1906870a] (2026-11-06T02:26:27Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 75 tests in 12.8s (9 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaWatch 5s, Kalevala 3s) / FAILED (2 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaWatch) [ran] [tree 3865e9808511] [world 2f1906870a] (2026-11-06T02:26:42Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_night` → exit 0 · Ran 58 tests in 6.2s (54 jobs, 16 at a time; slowest: NightTimers 5s, NightInstall.test_night_doctor_names_staged_timers_waiting_and_units_of_another_home 5s, Night.test_a_night_runs_its_jobs_and_the_ [ran] [tree e44050c56d80] [world 2f1906870a] (2026-11-06T02:28:49Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 75 tests in 52.6s (9 jobs, 16 at a time; slowest: KalevalaStep 50s, KalevalaWatch 40s, Kalevala 26s) / OK [ran] [tree 79bda9e85a3b] [world 2f1906870a] (2026-11-06T02:34:12Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_night` → exit 0 · Ran 58 tests in 15.5s (54 jobs, 16 at a time; slowest: Night.test_a_night_records_the_tasks_the_queue_closed_and_the_digest_says_so 14s, NightTimers 10s, Night.test_a_night_runs_its_jobs_and_the_diges [ran] [tree 79bda9e85a3b] [world 2f1906870a] (2026-11-06T02:34:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_moons_scale test_night test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [78.78s] [ran] [tree fa3250d86d79] [world 2f1906870a] (2026-11-06T02:40:15Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_kalevala test_night test_kalevala_live` → exit 0 · Ran 141 tests in 112.5s (66 jobs, 2 at a time; slowest: KalevalaStep 57s, KalevalaWatch 40s, KalevalaGen 12s) / OK [ran] [tree 83e3d75d61ec] [world 2f1906870a] (2026-11-06T04:14:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_moons_scale test_night test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [25.22s] [ran] [tree 83e3d75d61ec] [world 2f1906870a] (2026-11-06T04:15:47Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_kalevala test_night test_kalevala_live` → exit 0 · Ran 146 tests in 404.8s (70 jobs, 2 at a time; slowest: KalevalaStep 142s, KalevalaWatch 92s, Kalevala 41s) / OK [ran] [tree 60eb6d872310] [world 2f1906870a] (2026-11-06T05:06:09Z)
## Log
- 2026-11-06T02:10:18Z created
- 2026-11-06T02:10:30Z planned: it has criteria and steps
- 2026-11-06T02:10:39Z blocked: waits until T-3252's slot-pool bench finishes (a builder's test runs now would skew the before/after numbers); builder lanes resume once the pool lands
- 2026-11-06T02:21:56Z unblocked
- 2026-11-06T02:21:59Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3265.builder.md
- 2026-11-06T02:22:49Z focused
- 2026-11-06T02:22:49Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T04:44:54Z criterion 3 text: the restart undo quotes its paths and moves the current folder aside; a bare resume asks for --tower or --all; a halt prints its reason and exits 3 → the restart undo quotes its paths and moves the current folder aside; a bare resume asks for --tower or --all; a halt prints its reason and exits 6
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-11-02: Recommendation: don't build the decider market; M-12 waits in not-yet.md at Stage kill. No forecaster beats chance on whether a close survives 14 da…
