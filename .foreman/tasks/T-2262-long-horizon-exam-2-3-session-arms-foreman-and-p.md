---
id: T-2262
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2258]
source: followup
created: 2026-10-31T03:43:20Z
updated: 2026-10-31T05:09:56Z
base: fdba78a120f87840a3735db5a37d00921e7d1d08
base_tree: b1d536f7d5d7fbb50643bc1efcc9098f3c06ddb5
plan0_at: 2026-10-31T04:36:10Z
plan0_scope: []
verified: strong
---
# Long-horizon exam (2/3): session arms foreman and plain with planted faults
## Raw request
> Long-horizon exam (2/3): session arms foreman and plain with planted faults
## Interpretation
fm exam long run gains the two session arms (foreman, plain) beside oracle and empty, each a headless claude session per goal on the configured model (stamped like fmexam's arms so a Haiku line never decides), plus planted faults that a long task meets in real life: kill + resume, a usage-limit pause + resume, a forced compaction, and a misleading planted test the hidden checks contradict. The fault log (kind, when, resume ok) is written per scenario for slice 3's metrics. Real runs happen only at the end-of-run exam (steer 1); every test uses the stub claude.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam long run RUN --agent foreman|plain [--faults kill,pause,compaction,misleading] runs a headless session per goal on the configured model with the goal text; planted faults: kill (stop the session midway, resume it), pause (a usage-limit stop and a later resume), compaction (a forced /compact or its headless equivalent), misleading (a wrong test planted in the repo that the goal's hidden checks contradict); each fault's time and the resume are logged; tests use a stub claude (never the real one) — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
per-goal metrics and the scorecard row (T-2263); running real sessions in tests or per generation
## Approach (options → choice → why)
1) reuse fmexam._session_arm's shape: fmbench._session (claude -p, --plugin-dir for foreman with fmbench._seed; plain: no plugin, only fmbench._bare_guard settings, FOREMAN_QUIET), work in a temp copy, the tree copied back to work/<agent>/<sid> for grade; kill = first session capped by a short timeout then --resume its session_id; pause = first session told to stop at a checkpoint (or timed out) then resumed after a logged gap; compaction = fmbench's compact_at path (run_case already supports it) or /compact as a resumed turn; misleading = a wrong test file planted in the repo before the session (named in the fault log, never in the key). 2) a new runner from scratch — rejected: duplicates fmbench's env/guard isolation. 3) run faults as separate scenarios — rejected: the same goal with and without faults is the comparison slice 3 needs. Choice 1. Spend: fmbudget.check like run_agent; no per-session dollar cap by default (T-2179).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests with a stub claude: each fault injected and logged, the plain arm gets no Foreman, the foreman arm gets the plugin
2. [x] session arms and faults in fmlong
3. [x] docs
## Resume here
<!-- auto -->
- 2026-10-31T04:51:37Z step 3/3: docs
- git: worktree-agent-a1e9cce7972730ad5; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmlong.py, plugin/tests/test_long.py
- touched since last checkpoint: plugin/lib/fmbench.py, MASTER.md, plugin/tests/test_long.py, plugin/lib/fmlong.py, plugin/lib/fmcli.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -8` → ✗ exit 1 · Ran 22 tests in 12.1s (7 classes, 16 at a time; slowest: Long 10s, Approvals 3s, Stop 2s) / FAILED (1 classes) [ran] [tree f5c96dc6a19e] (2026-10-31T04:38:21Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 22 tests in 17.8s (7 classes, 16 at a time; slowest: Long 17s, Approvals 1s, Stop 1s) / OK [ran] [tree 2a70a9b26322] (2026-10-31T04:41:27Z)
- (step 2) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 60 tests in 80.8s (17 classes, 16 at a time; slowest: ExamAuthors 80s, ExamGen 63s, Long 28s) / OK [ran] [tree 2a70a9b26322] (2026-10-31T04:42:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_bench_family test_board_posture test_board_verbs test_cli test_docs test_evolve test_guard_cases test_long test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 345 tests in 63.7s (94 classes, 16 at a time; slowest: Bench 63s, TaskLifecycle 44s, Judged 37s) / FAILED (2 classes) [ran] [tree 2a70a9b26322] (2026-10-31T04:43:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_bench test_bench_family test_board_posture test_board_surfaces test_board_verbs test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_evolve test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_long test_map test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_round_g test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.80s] [ran] [tree e33a999b2a2d] (2026-10-31T05:02:46Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_bench test_bench_family test_board_posture test_board_surfaces test_board_verbs test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_evolve test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_long test_map test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_round_g test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.33s] [ran] [tree e33a999b2a2d] (2026-10-31T05:02:55Z)
- (step 1) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 67 tests in 72.3s (17 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 60s, Long 42s) / OK [ran] [tree bfd386e0248a] (2026-10-31T05:04:56Z)
- (step 2) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 67 tests in 76.9s (17 classes, 16 at a time; slowest: ExamAuthors 77s, ExamGen 57s, Long 33s) / OK [ran] [tree bfd386e0248a] (2026-10-31T05:06:13Z)
- (step 3) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 67 tests in 85.6s (17 classes, 16 at a time; slowest: ExamAuthors 85s, ExamGen 69s, Long 46s) / OK [ran] [tree bfd386e0248a] (2026-10-31T05:07:39Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 29 tests in 31.8s (7 classes, 16 at a time; slowest: Long 31s, Approvals 3s, Stop 2s) / OK [ran] [tree 7ce78a4f72ff] (2026-10-31T05:08:23Z)
- (audit intent) `self + one fm-reviewer pass (2 medium, 7 low, all fixed with tests); no real session ran: every test uses the stub claude; real runs belong to the end-of-run exam (steer 1)` → foreman and plain session arms per goal with kill, pause, compaction and misleading faults, each logged with its resume (test_long red-to-green) [tree 7ce78a4f72ff] (2026-10-31T05:08:23Z)
- (audit adversary) `self + one fm-reviewer pass (2 medium, 7 low, all fixed with tests); no real session ran: every test uses the stub claude; real runs belong to the end-of-run exam (steer 1)` → run.json goal ids validated (a ../../x id refused, nothing outside the run touched); credentials stripped by fmbench._env; plain arm gets no plugin, only the guard settings; the decoy never reaches the key [tree 7ce78a4f72ff] (2026-10-31T05:08:23Z)
- (audit edge) `self + one fm-reviewer pass (2 medium, 7 low, all fixed with tests); no real session ran: every test uses the stub claude; real runs belong to the end-of-run exam (steer 1)` → a pause that didn't stop isn't resumed; a failed resume gets one fresh turn; a killed turn's cost is logged unknown, never 0; --limit bounds goals, spend checked per goal [tree 7ce78a4f72ff] (2026-10-31T05:08:23Z)
## Log
- 2026-10-31T03:43:20Z created
- 2026-10-31T04:35:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2262.builder.md
- 2026-10-31T04:35:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2262.builder.md
- 2026-10-31T04:36:10Z focused
- 2026-10-31T05:03:37Z merged worktree-agent-a1e9cce7972730ad5 (5 file(s))
- 2026-10-31T05:03:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1e9cce7972730ad5
- 2026-10-31T05:03:38Z focused
- 2026-10-31T05:07:50Z scope: plugin/lib/fmlong.py, plugin/lib/fmbench.py (_session sid=), plugin/lib/fmcli.py (exam long flags), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T05:09:53Z done
- 2026-10-31T05:09:56Z committed 7815a289 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
- T-2258 [FEATURE M, done, 3 steps] Long-horizon exam (1/3): fm exam long gen/run/grade from local git history, oracle and empty arms — lesson: A held-out check built from…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
## Lessons
- A fault-injection harness must log whether each fault actually fired, or a fault that never happened reads as one survived
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmbench.py
- plugin/lib/fmlong.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
