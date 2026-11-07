---
id: T-3584
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:06:30Z
updated: 2026-11-07T04:51:27Z
lane: ~/.claude/foreman.lanes/T-3584
lane_branch: foreman/T-3584
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:32:18Z
plan0_scope: []
---
# The guard compiles ~120 regexes per PreToolUse Bash (~8.6 ms CPU, ~20% of the call after…
## Raw request
> PERFORMANCE: the guard compiles ~120 regexes per PreToolUse Bash (~8.6 ms CPU, ~20% of the call after T-3577); a cross-process compiled-pattern cache (sre code keyed on Python version + pattern, kept where the guard refuses writes) or fewer patterns per allow would cut it; a hook's remaining floor is interpreter 10.5 ms + json/re 5 ms + core/hooks/fmguard module bodies ~6 ms (1.5 MB of pyc)
## Interpretation
Reading 1 (chosen): each PreToolUse hook is a new Python process, so re's in-process cache starts empty every call; the profile shows 122 compiles, 122 distinct (none repeated in a process), ~8.7 ms CPU, already compiled lazily once per process (fmguard.lazy, core.lazy). So 'compile once' must mean once across processes. Reading 2 (ruled out): the guard recompiles the same patterns within one call (re cache misses from formatting, flags or >512 patterns): the profile shows no repeats, so module constants or lru_cache would save nothing.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A pattern compiled and saved by one process is rebuilt by the next without parsing, equal to stdlib's Pattern; a corrupt, foreign-stamped or bad entry falls back to stdlib — verify with `nice -n 10 python3 plugin/tests/run.py test_fmpy`
- [ ] Every guard and hook test stays green — verify with `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_hardening test_guard_latency test_hooks test_fmpy`
## Non-goals
## Approach (options → choice → why)
1) use what exists: re's own cache, module-level constants, fmguard.lazy/core.lazy (already there): likely outcome no gain, nothing repeats within a process. 2) do less: fewer patterns per allow (pre-checks that skip pattern families): fails if a skipped family was needed, it rewrites security logic, and saves only part. 3) a long-lived daemon or the native fast path: fails here as scope, T-3571 does that lane. 4) cross-process program cache: route re._compiler.compile through (flags, code, groups, groupindex, indexgroup) entries kept per hook event in plugin/lib/sampo/__pycache__ (protected core, the pyc's own trust level), keyed on sys.version + _sre.MAGIC; a miss returns stdlib's own Pattern and stores an entry only when _sre.compile of it equals that Pattern (code compared); every failure falls back to stdlib; installed from hooks/hook only; likely outcome ~8 ms CPU per call saved (prototype: 7.6 ms -> 0.34 ms for the 122). Choice 4 (85%): the only option that removes the per-process cost without touching a security regex; in sampo/py.py (imported first by the hook already) to avoid a new module, shim and docs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: regex programs reused across processes (test_fmpy)
2. [x] Cache in sampo/py.py, installed from hooks/hook; guard tests green
3. [x] Measure PreToolUse Bash wall/CPU per call over 200 calls, before and after; docs line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fmpy.RegexPrograms` → ✗ exit 1 · Ran 4 tests in 101.5s (1 jobs, 16 at a time; slowest: RegexPrograms 1s) / FAILED (1 classes: test_fmpy.RegexPrograms) [ran] [tree ae1d698640be] [world 2f1906870a] (2026-11-07T04:42:10Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fmpy` → exit 0 · Ran 8 tests in 220.0s (3 jobs, 16 at a time; slowest: RegexPrograms 1s, HookUnderOldPython 1s, Fmpy 0s) / OK [ran] [tree 74fbd0be3dca] [world 2f1906870a] (2026-11-07T04:46:29Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fmpy` → exit 0 · Ran 8 tests in 128.4s (3 jobs, 16 at a time; slowest: RegexPrograms 1s, Fmpy 0s, HookUnderOldPython 0s) / OK [ran] [tree 272e4536b8d6] [world 2f1906870a] (2026-11-07T04:49:40Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_hardening test_guard_latency test_guard_sampo test_hooks test_fmpy test_bench_hooks test_rename_aliases test_doctor` → exit 0 · Ran 753 tests in 84.0s (309 jobs, 16 at a time; slowest: Mutation 22s, GuardAgainstBash 21s, Approvals 20s) / OK [ran] [tree 272e4536b8d6] [world 2f1906870a] (2026-11-07T04:51:06Z)
- (step 3) `nice -n 10 python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3584/ab2.py 40 PreToolUse:Bash ~/.claude/foreman ~/.claude/foreman.lanes/T-3584` → exit 0 · ~/.claude/foreman                   wall p50   73.7 mean   81.2  cpu p50   56.0 mean   56.0  (n=40) / ~/.claude/foreman.lanes/T-3584      wall p50   63.6 mean   68.2  cpu p50   48. [ran] [tree 272e4536b8d6] [world 2f1906870a] (2026-11-07T04:51:27Z)
## Log
- 2026-11-07T03:06:30Z created
- 2026-11-07T04:31:50Z set tier=M
- 2026-11-07T04:31:56Z planned: it has criteria and steps
- 2026-11-07T04:32:00Z lane: ~/.claude/foreman.lanes/T-3584 on foreman/T-3584
- 2026-11-07T04:32:18Z focused
- 2026-11-07T04:32:18Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:33:37Z criterion 1 verify: `nice -n 10 python3 plugin/tests/run.py test_py` → `nice -n 10 python3 plugin/tests/run.py test_fmpy`
- 2026-11-07T04:33:38Z criterion 2 verify: `nice -n 10 python3 plugin/tests/run.py test_guard test_hooks test_py` → `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_hardening test_guard_latency test_hooks test_fmpy`
- 2026-11-07T04:33:38Z step 1 text: Failing test: regex programs reused across processes (test_py) → Failing test: regex programs reused across processes (test_fmpy)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- T-3577 [PERFORMANCE M, active, 3 steps] PERFORMANCE hooks hot path (user 2026-11-06: fast-track the Python CPU fixes): every…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-02: Recommendation: M-02 is viable at the kill stage (3 of 3 spec-suite modules rebuilt blind passed every test) and moves to its slice: regenerate one …
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
