---
id: T-3132
type: SECURITY
tier: S
status: active
priority: normal
scope: [plugin/tests/bench_hooks.py, plugin/tests/test_bench_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T03:51:02Z
updated: 2026-11-06T06:22:35Z
group: hook bench gate
lane: ~/.claude/foreman/.claude/worktrees/agent-a51eef1318dd31261
lane_branch: worktree-agent-a51eef1318dd31261
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:54:15Z
plan0_scope: [plugin/tests/bench_hooks.py, plugin/tests/test_bench_hooks.py, CHANGELOG.md]
builder_returned: 2026-11-06T06:22:35Z
---
# The hook bench never imports the tree's own code into its timing process: the script budget comes from a child, so a branch can't patch the clock that judges it
## Raw request
> self-change gate: bench_hooks imports the branch's fmguard in its own process, so branch code could patch resource.getrusage or statistics.median and fake its own timings (pre-existing, review of T-3131); bench in a subprocess that loads only the base's harness
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] bench_hooks.py imports nothing from the benched tree's plugin/lib in its own process; fmguard._script_budget() is read by a child python (-I) and parsed, with the old default when the child fails; a branch fmguard that patches resource.getrusage at import changes no timing the bench reports — verify with `python3 plugin/tests/run.py test_bench_hooks test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a fixture tree whose fmguard patches resource.getrusage at import; the bench's reported CPU times are unaffected and no plugin/lib module is in sys.modules after import
2. [ ] the child read of the script budget in bench_hooks  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 6 tests in 244.5s (4 jobs, 16 at a time; slowest: Modules 10s, Isolation 1s, ScriptBudget 0s) / OK (ran] (tree 8ff826ace361] (world 2f1906870a] (2026-11-06T05:58:56Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench_hooks test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 223 tests in 210.6s (67 jobs, 16 at a time; slowest: RenameScan 8s, ViewsRepair 6s, Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 6s) / FAILED (1 classes: test_left_out.Lef (ran] (tree 5a13e13784b1] (world 2f1906870a] (2026-11-06T06:20:34Z)
## Log
- 2026-11-05T03:51:02Z created
- 2026-11-05T03:51:16Z planned from capture
- 2026-11-05T03:51:16Z set approved=True
- 2026-11-05T03:51:17Z set scope=['plugin/tests/bench_hooks.py', 'plugin/tests/test_bench_hooks.py', 'CHANGELOG.md']
- 2026-11-05T03:51:17Z blocked: approved; right after T-3131 closes (the same files' neighbourhood), main thread or a builder
- 2026-11-06T03:52:34Z unblocked
- 2026-11-06T05:54:13Z focused
- 2026-11-06T05:54:15Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:22:01Z test_left_out.LeftOut fails on repro.py:31/34 from the T-3279 merge in the base; not this task's files; fixed in T-3279's close
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3131 [FIX M, done, 2 steps] The self-change gate judges a hook's median CPU time and holds only a rise seen in every pair, so identical code no longer holds by chance …
- research T-2352-review: T-2352 review (fm-reviewer, one pass): changes needed; fixed before close (tests added after the fixes, so not seen red first).
- T-2352 [FEATURE M, done, 3 steps] Self-change gate at lane merge: guard replay, hook p95 and footprint must not get worse (Mission 8, #7 #12) — lesson: A gate that runs …
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md, plugin/tests/bench_hooks.py, plugin/tests/test_bench_hooks.py; re-ground the plan against them before editing
