---
id: T-3352
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: user
created: 2026-11-06T05:33:13Z
updated: 2026-11-06T21:59:36Z
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-06T05:57:12Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
builder_returned: 2026-11-06T06:46:04Z
lane_stop: merged 2026-11-06T18:26:22Z
verified: ok
unproven: [meaning, perf-typed, typed]
---
# Measure the hook handler: hook_ms events carry the tool name and the guard's own ms, so the PreToolUse handler's 32 → 90 ms p50 rise (Nov 3-6, quiet-machine days) can be pinned to the guard or to the note builders after it
## Raw request
> Rust where it pays: measure first, then move only the measured hot path. Candidates: (1) the per-tool-call hooks (PreToolUse guard, PostToolUse attribution) start a fresh python3 every call (~50+ ms each, x every tool call of every session and builder): try a resident hook process first (the T-3297 fork-server idea applied to hooks), and port the guard's command parser to Rust only if the resident process still leaves it slow; (2) any scan over the 300,000-file state or the test-selection graph that a profile shows CPU-bound after its algorithm is fixed. Constraints: the plugin must still work with python3 alone (a prebuilt binary is an optional speed-up with a pure-Python fallback, never a requirement), and builds come from CI, not a toolchain on the user's machine. Bench numbers before and after (bench_hooks, perf_bench). Tonight's big wins were algorithmic, not language: sync export 6-8 s → 0.4 s (T-3349). User: 'could we/should we start writing/rewriting stuff in Rust that will massively help with performance?'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every hook_ms event has tool and guard_ms fields — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test on the hook_ms event fields
2. [x] record tool and guard_ms (hooks.py ~161-165)
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_hooks.HookMs` → exit 0 · Ran 1 tests in 104.2s (1 jobs, 16 at a time; slowest: HookMs 0s) / OK (ran] (tree 66b6276d764c] (world 2f1906870a] (2026-11-06T06:04:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 629 tests in 989.5s (244 jobs, 16 at a time; slowest: Approvals 51s, UserPromptSubmit 46s, PromptApprovals 43s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 66b6276d764c] (world 2f1906870a] (2026-11-06T06:21:33Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 831.903s) · timed out after 831.903s (ran] (tree b175bf48d25e] (world 2f1906870a] (2026-11-06T06:45:48Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 5761ec5368a9] (2026-11-06T18:32:07Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 268 tests in 14.8s (215 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 8s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_takes [ran] [tree 5761ec5368a9] [world 2f1906870a] (2026-11-06T18:32:24Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 268 tests in 14.8s (215 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 8s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_takes [ran] [tree 5761ec5368a9] [world 2f1906870a] (2026-11-06T18:32:24Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 5761ec5368a9] (2026-11-06T18:32:24Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 5761ec5368a9] (2026-11-06T18:32:24Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 5761ec5368a9] (2026-11-06T18:32:24Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 5761ec5368a9] (2026-11-06T18:32:24Z)
## Log
- 2026-11-06T05:33:13Z created
- 2026-11-06T05:54:45Z planned from capture
- 2026-11-06T05:57:10Z focused
- 2026-11-06T05:57:12Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-06T18:26:22Z merged worktree-agent-aeeb57f7679090a68 in merge train
- 2026-11-06T18:32:07Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T18:32:07Z scope: widened at merge to the reviewed lane's own diff (dd51cba4b), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:33:00Z done
- 2026-11-06T18:33:04Z committed 5a77ed1f5 (1 file)
- 2026-11-06T21:59:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeeb57f7679090a68; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-06: No Rust rewrite now: a Bash tool call costs ~37 ms of process floor plus ~90 ms of Python handler work that tripled in three days; the handler's gro…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- playbook Profiling (fm playbooks show perf/profiling)
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Measurements
none: this task adds the measurement (guard_ms and the tool name on hook_ms events); it claims no speed change
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
