---
id: T-2676
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T21:51:06Z
updated: 2026-11-02T23:15:45Z
builder_model: sonnet
base: 6a4e4a506c481f9b3d962c77382a90a5e0344f3d
base_tree: 37c80f3d08ed6a0467af181a91ae9b09c862dc51
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T22:01:03Z
plan0_scope: []
lane_stop: merged 2026-11-02T22:15:36Z
verified: strong
unproven: [tui-unshot]
---
# every plugin/lib/fm*.py module that prints a cut list says how many it left out: test_left_out's scan covers all of them
## Raw request
> Extend T-2673's left-out scan from fmcli.py to every plugin/lib/fm*.py module that prints a cut list
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_left_out's scan runs over every plugin/lib/fm*.py and finds no join(...[:N]) without a count, a c.more note or a '# not a list: <why>' mark — verify with `python3 plugin/tests/run.py test_left_out`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] widen the scan (red: it lists the silent sites in other modules)
2. [x] c.more or a not-a-list mark at each site
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree 1c8089496c02] [world 2f1906870a] (2026-11-02T22:06:19Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_approve_reads test_batch_edit test_bench test_bench_family test_board_posture test_builder test_cards_at_prompt test_code test_code_envelope test_code_tui test_code_worker test_core test_cost test_cost_forecast test_crash_hygiene test_critique test_debug test_doctor test_drill test_drive_side test_economics test_evolve test_exam test_export test_find test_friction test_genesis test_goal test_graph test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_pipes test_hooks test_judge_home test_lanes test_left_out test_lib_hostile test_loop test_mandate test_map test_mcp test_memory test_mission test_outcomes test_outside test_page test_playbook_use test_plugins test_proof test_prove test_recall test_release test_repeats test_rewind test_round_g test_runner_lint test_scene test_scene_verify test_scout test_second test_session test_settings test_settings_power test_settings_scopes test_ship test_showpieces test_split test_supply_delta test_tidy test_tool_queue test_tool_taint test_trials test_triggers test_usage_burn && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.31s] [ran] [tree 1c8089496c02] [world 2f1906870a] (2026-11-02T22:06:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_approve_reads test_batch_edit test_bench test_bench_family test_board_posture test_builder test_cards_at_prompt test_code test_code_envelope test_code_tui test_code_worker test_core test_cost test_cost_forecast test_crash_hygiene test_critique test_debug test_doctor test_drill test_drive_side test_economics test_evolve test_exam test_export test_find test_friction test_genesis test_goal test_graph test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_pipes test_hooks test_ideas test_ideation test_judge_home test_lanes test_left_out test_lib_hostile test_loop test_mandate test_map test_mcp test_memory test_mission test_outcomes test_outside test_page test_playbook_use test_plugins test_proof test_prove test_recall test_release test_repeats test_rewind test_round_g test_runner_lint test_scene test_scene_verify test_scout test_second test_session test_settings test_settings_power test_settings_scopes test_ship test_showpieces test_split test_supply_delta test_taste test_tidy test_tool_queue test_tool_taint test_trials test_triggers test_usage_burn && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.96s] [ran] [tree 5f083930218b] [world 2f1906870a] (2026-11-02T22:12:50Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree 5f083930218b] [world 2f1906870a] (2026-11-02T22:15:49Z)
- `python3 plugin/tests/run.py test_left_out` → ✗ exit 1 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: LeftOut 0s) / FAILED (1 classes: test_left_out.LeftOut) (start tree + this task's tests) [ran] [tree 7cd38697bb29] [world 2f1906870a] (2026-11-02T22:16:05Z)
- `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree 7cd38697bb29] [world 2f1906870a] (2026-11-02T22:16:05Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:16:05Z [ran] [tree 7cd38697bb29] [world 2f1906870a] (2026-11-02T22:16:49Z)
- (step 2) `python3 plugin/tests/run.py test_left_out test_core test_proof` → exit 0 · Ran 182 tests in 29.4s (37 classes, 16 at a time; slowest: Proof 29s, ConfidenceRoutes 9s, BriefIndex 4s) / OK [ran] [tree 7cd38697bb29] [world 2f1906870a] (2026-11-02T22:16:49Z)
- (step 3) `python3 plugin/tests/run.py test_left_out test_core test_proof` → exit 0 · Ran 182 tests in 29.4s (37 classes, 16 at a time; slowest: Proof 29s, ConfidenceRoutes 9s, BriefIndex 4s) / OK [ran] [tree 7cd38697bb29] [world 2f1906870a] (2026-11-02T22:16:49Z)
- (audit edge) `read every diff hunk in 0d6cef96..bbdf0f89: the user-visible cuts use c.more/joinmore, the not-a-list marks sit on stored or JSON fields or character caps; sent the proof why fields back twice until they said K left out` → joinmore with n >= len(items) adds no suffix; the scan's accept list is more( / left out / len( only [tree 7cd38697bb29] (2026-11-02T22:16:49Z)
- (audit adversary) `read every diff hunk in 0d6cef96..bbdf0f89: the user-visible cuts use c.more/joinmore, the not-a-list marks sit on stored or JSON fields or character caps; sent the proof why fields back twice until they said K left out` → the fmguard.py and fmsession.py hunks are trailing comments only (git diff 6a4e4a50 HEAD shows 4 lines, each identical code plus a # mark); no guard decision path changed [tree 7cd38697bb29] (2026-11-02T22:16:49Z)
- (audit self) `read every diff hunk in 0d6cef96..bbdf0f89: the user-visible cuts use c.more/joinmore, the not-a-list marks sit on stored or JSON fields or character caps; sent the proof why fields back twice until they said K left out` → no findings [tree 7cd38697bb29] (2026-11-02T22:16:49Z)
## Log
- 2026-11-02T21:51:06Z created
- 2026-11-02T22:00:53Z planned from capture
- 2026-11-02T22:00:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2676.builder.md
- 2026-11-02T22:01:02Z focused
- 2026-11-02T22:01:03Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T22:15:36Z merged worktree-agent-aaf3d33246aabb06d (45 file(s))
- 2026-11-02T22:15:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaf3d33246aabb06d
- 2026-11-02T22:15:53Z focused
- 2026-11-02T22:16:10Z scope: the scan touched every plugin/lib/fm*.py with a cut list (c.more / joinmore or a not-a-list mark) and CHANGELOG.md
- 2026-11-02T22:21:55Z done
- 2026-11-02T22:21:58Z committed f5ba1c41 (1 file)
- 2026-11-02T23:15:45Z includes T-2698: FIX: cross-cutting review gen-3 #5 (what got worse): the left-out scan closed covering…
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2673 [FIX S, done, 3 steps] every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore for the fmcli sites that cut silently
- T-2601 [FEATURE S, done, 2 steps] fm exam runs lists each exam run: id, tier, scenarios and how many held out, and per agent the newest grade's gen, model and date — les…
- T-1623 [FEATURE M, done, 2 steps] Five-rule UI contract gate for UI playbooks, a playbook coverage heatmap (from T-1524; wai — lesson: When a task waits on rules nobody …
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
## Why not caught
T-2673 scoped its scan to fmcli.py; the other modules' cuts were never scanned
## Files touched
- plugin/tests/test_left_out.py
- .fm-scratch/more.json
- plugin/lib/fmdesign.py
- plugin/lib/fmgraph.py
- plugin/lib/fmmap.py
- plugin/lib/fmoutside.py
- .fm-scratch/gen.py
- plugin/lib/fmbench.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmcritique.py
- plugin/lib/fmdebug.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmdrill.py
- plugin/lib/fmeco.py
- plugin/lib/fmedit.py
- plugin/lib/fmexam.py
- plugin/lib/fmfind.py
- plugin/lib/fmfriction.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmgrants.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fminstr.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlib.py
- plugin/lib/fmloop.py
- plugin/lib/fmmandate.py
