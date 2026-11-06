---
id: T-3271
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/hotfn.py, plugin/tests/test_hotfn.py, plugin/lib/sampo/cli.py, plugin/lib/fmhotfn.py, docs/map/files-lib-3.md, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:37Z
updated: 2026-11-06T04:54:25Z
builder: 2026-11-06T02:27:47Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-ac61d583eca6e8052
lane_branch: worktree-agent-ac61d583eca6e8052
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:27Z
plan0_scope: [plugin/lib/sampo/hotfn.py, plugin/tests/test_hotfn.py, plugin/lib/sampo/cli.py, CHANGELOG.md, MASTER.md]
---
# Moon C-001076: sampo hotfn ranks Sampo's own functions by churn x size x FIX-task touches and captures the top as refactor tasks
## Raw request
> Moon C-001076: sampo hotfn ranks Sampo's own functions by churn x size x FIX-task touches and captures the top as refactor tasks
## Interpretation
Reading 1 (chosen): a per-function hotspot ranking for Sampo's own code, joining git churn, function size and FIX-task touches, whose top rows become refactor captures. Partial: file-level fix hotspots exist at plugin/lib/sampo/find.py:181 (sampo find --hotspots) and map.py:203 (_fixy); this adds the function granularity, size and FIX-task join, and the capture step. Reading 2 (ruled out): extending find --hotspots in place, because find.py and cli.py find wiring are large shared files that parallel lanes collide in, and it would blur find's unproven-candidate meaning.
## Assumptions (confidence)
## Acceptance criteria
- [ ] hotfn.rank(rows) orders functions by churn*size weighted by FIX-task touches; pure function with fixed fixtures (ties break by path) — verify with `python3 plugin/tests/run.py test_hotfn`
- [ ] hotfn.collect(root) returns per-function rows {file,func,lines,churn,fixes} from ast (def spans), git log -L-free hunk line ranges, and closed FIX briefs' scope+commit files — verify with `python3 plugin/tests/run.py test_hotfn`
- [ ] sampo hotfn [--top N] [--capture K] prints the ranked table and with --capture files K refactor captures (dedup by func); registered in cli.py — verify with `python3 plugin/tests/run.py test_hotfn`
## Non-goals
## Approach (options → choice → why)
1. New module hotfn.py: ast def spans, churn from git log -U0 hunk ranges mapped onto spans, FIX touches from done FIX briefs' files, score = churn*size*(1+fixes); one cli.py registration line. Likely outcome: ranked per-function table, small diff, testable with a tmp git repo.
2. Extend find.hotspots with a per-function mode. Likely outcome: reuses the git parsing but edits large find.py and cli.py find args, so lane merges conflict.
3. Use git log -L per function. fails if: it runs one git process per function over thousands of functions, far too slow to run routinely.
4. Do less: file-level only, add churn and size columns to find --hotspots. Likely outcome: cheap but misses which function in hooks.py or cli.py is the hot one, the actual problem.

Choice 1 (85%): isolated new file, per-function is the missing piece. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Write test_hotfn: rank() on fixtures; collect() on a tmp git repo with two functions, one edited in a 'fix:' commit  <- CURRENT
2. [x] hotfn.py: ast def spans, per-commit hunk (git log -U0 --format) line ranges mapped to functions, FIX task touches from briefs (core.load_briefs, type FIX, done)
3. [x] rank + cmd_hotfn (--top, --capture via existing capture helper, --json); register in cli.py beside risk; CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T02:39:47Z step 3/3: rank + cmd_hotfn (--top, --capture via existing capture helper, --json); register in cli.py beside risk; CHANGELOG line
- git: worktree-agent-ac61d583eca6e8052; 4 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/fmhotfn.py, plugin/lib/sampo/hotfn.py, plugin/tests/test_hotfn.py
- touched since last checkpoint: plugin/lib/fmhotfn.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/hotfn.py, plugin/tests/test_hotfn.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_hotfn` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 3.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree d1669965f65a] [world 2f1906870a] (2026-11-06T02:33:40Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_hotfn` → exit 0 · Ran 10 tests in 41.1s (10 jobs, 16 at a time; slowest: Cli.test_capture_files_the_top_once_per_function 23s, Cli.test_table_and_json 17s, Collect.test_done_fix_brief_no_commit_names_counts_its_scope_f [ran] [tree cd06a35ff206] [world 2f1906870a] (2026-11-06T02:42:05Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_hotfn` → exit 0 · Ran 10 tests in 35.5s (10 jobs, 16 at a time; slowest: Cli.test_capture_files_the_top_once_per_function 19s, Cli.test_table_and_json 16s, Collect.test_done_fix_brief_no_commit_names_counts_its_scope_f [ran] [tree cd06a35ff206] [world 2f1906870a] (2026-11-06T02:42:46Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_hotfn test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2088 tests in 3658.5s (710 jobs, 16 at a time; slowest: LeanKindGateHookDelay 488s, LeanKindGateSessionLine 486s, CloseGaps 486s) / FAILED (47 classes: test_cli.TaskLifecycle, test_proof.Proof, te [ran] [tree 3ef84fc6c598] [world 2f1906870a] (2026-11-06T03:44:35Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_hotfn test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2387 tests in 1709.3s (1733 jobs, 16 at a time; slowest: LeanKindGateRules 435s, OutcomeEscalation 218s, LeanKindGateHookDelay 213s) / FAILED (13 classes: test_exam.ExamTs, test_hooks.PreToolUse.t [ran] [tree 3ef84fc6c598] [world 2f1906870a] (2026-11-06T04:13:48Z)
## Log
- 2026-11-06T02:27:37Z created
- 2026-11-06T02:27:46Z set scope=['plugin/lib/sampo/hotfn.py', 'plugin/tests/test_hotfn.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-11-06T02:27:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3271.builder.md
- 2026-11-06T02:28:26Z focused
- 2026-11-06T02:28:27Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:39:38Z set scope=['plugin/lib/sampo/hotfn.py', 'plugin/tests/test_hotfn.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/fmhotfn.py', 'docs/map/files-lib-3.md', 'MASTER.md', 'CHANGELOG.md']
- 2026-11-06T02:39:43Z steer: scope widened to plugin/lib/fmhotfn.py (the fm shim every plugin/lib module needs) and docs/map/files-lib-3.md (the contract's docs line)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-3275 [FEATURE M, planned, 3 steps] Moon C-000723: sampo shape FILE drafts the companions a new file is owed (test, alias, MASTER line) learned from how past files were…
- decision 2026-11-01: [revisited: free first pass] [cites: user steer 2026-10-30 (fourth): standing rule for #1 detection] [check: python3 plugin/tests/run.py test_find] …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
