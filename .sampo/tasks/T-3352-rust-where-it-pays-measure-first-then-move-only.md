---
id: T-3352
type: PERFORMANCE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-11-06T05:33:13Z
updated: 2026-11-06T06:10:37Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aeeb57f7679090a68
lane_branch: worktree-agent-aeeb57f7679090a68
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-06T05:57:12Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
builder_returned: 2026-11-06T06:10:37Z
---
# Measure the hook handler: hook_ms events carry the tool name and the guard's own ms, so the PreToolUse handler's 32 → 90 ms p50 rise (Nov 3-6, quiet-machine days) can be pinned to the guard or to the note builders after it
## Raw request
> Rust where it pays: measure first, then move only the measured hot path. Candidates: (1) the per-tool-call hooks (PreToolUse guard, PostToolUse attribution) start a fresh python3 every call (~50+ ms each, x every tool call of every session and builder): try a resident hook process first (the T-3297 fork-server idea applied to hooks), and port the guard's command parser to Rust only if the resident process still leaves it slow; (2) any scan over the 300,000-file state or the test-selection graph that a profile shows CPU-bound after its algorithm is fixed. Constraints: the plugin must still work with python3 alone (a prebuilt binary is an optional speed-up with a pure-Python fallback, never a requirement), and builds come from CI, not a toolchain on the user's machine. Bench numbers before and after (bench_hooks, perf_bench). Tonight's big wins were algorithmic, not language: sync export 6-8 s → 0.4 s (T-3349). User: 'could we/should we start writing/rewriting stuff in Rust that will massively help with performance?'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] every hook_ms event has tool and guard_ms fields — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test on the hook_ms event fields  <- CURRENT
2. [x] record tool and guard_ms (hooks.py ~161-165)
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_hooks.HookMs` → exit 0 · Ran 1 tests in 104.2s (1 jobs, 16 at a time; slowest: HookMs 0s) / OK (ran] (tree 66b6276d764c] (world 2f1906870a] (2026-11-06T06:04:54Z)
## Log
- 2026-11-06T05:33:13Z created
- 2026-11-06T05:54:45Z planned from capture
- 2026-11-06T05:57:10Z focused
- 2026-11-06T05:57:12Z predicted from its closes: 5 min, 1 attempt(s)
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
