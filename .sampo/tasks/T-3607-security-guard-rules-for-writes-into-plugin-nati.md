---
id: T-3607
type: SECURITY
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-07T04:28:02Z
updated: 2026-11-07T05:11:11Z
lane: ~/.claude/foreman.lanes/T-3607
lane_branch: foreman/T-3607
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-07T04:34:34Z
plan0_scope: []
---
# SECURITY: guard rules for writes into plugin/native by cargo (T-3571 review): treat…
## Raw request
> SECURITY: guard rules for writes into plugin/native by cargo (T-3571 review): treat cargo --artifact-dir/--out-dir and rustc/cargo -o into plugin/, RUSTC_WRAPPER/RUSTFLAGS in the env of a cargo/rustc call, and a .cargo/config.toml (or config) at or above plugin/native as writes to protected core, so no build path but the installer can produce the binary hooks/fast runs
## Interpretation
Reading 1 (chosen): the Ward reads every Bash or file write that could swap or poison plugin/native/sampo-fast (or its sha256) as a protected-core write: cargo/rustc output flags and CARGO_TARGET_DIR aimed into plugin/, build settings (RUSTC*, RUSTFLAGS, CARGO_*, PATH, --config) on a cargo call that builds the main checkout's plugin/native, .cargo/config(.toml) and rust-toolchain(.toml) at or above plugin/native, and plain writes to the binary, its sum, build.rs and Cargo.toml; lane-worktree cargo builds and reads still pass. Reading 2 (ruled out): refuse every cargo call in the main checkout's plugin/native; the brief keeps plain cargo build/test there working and names settings only.
## Assumptions (confidence)
## Acceptance criteria
- [ ] each shape (cargo/rustc output flags, CARGO_TARGET_DIR, build settings on a main plugin/native cargo call, cargo config and toolchain files at or above plugin/native, plain writes to sampo-fast/.sha256/build.rs/Cargo.toml) is blocked as core, and lane-worktree cargo builds pass — verify with `nice -n 10 python3 plugin/tests/run.py test_guard`
- [ ] existing guard suites stay green — verify with `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_latency`
## Non-goals
## Approach (options → choice → why)
1) A separate cargo checker beside check_bash. fails if: it drifts from classify_write, standing/trust yeses and messages need their own wiring. 2) A regex over the raw command. fails if: cd, env, export and wrappers evade it; the guard already parses all of those. 3) Feed the existing write mechanism: native in _CORE_DIRS (T-3571's line), cargo/rustc output dirs into _write_targets/_tree_targets, CARGO_TARGET_DIR as tree targets like git_env, config files in _is_core/_protected_roots, the settings check as one core finding in check_bash's per-command loop. likely outcome: every shape caught through classify_write/classify_tree, ~0 ms added. 4) do less: only native in _CORE_DIRS (T-3571 already does it). fails if: target-dir/config/env paths that never name sampo-fast still produce it. Choice 3 (85%): same path every other core write takes, so yeses and messages work unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: one per shape in test_guard (NativeBuild class), plus lane-worktree passes  <- CURRENT
2. [x] Fix in fmguard: native core dir, cargo config files, cargo/rustc write targets, build settings finding
3. [x] Latency: PreToolUse Bash ms per call before/after (bench_hooks, ~100 runs)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard.NativeBuild` → ✗ exit 1 · Ran 5 tests in 101.3s (1 jobs, 16 at a time; slowest: NativeBuild 0s) / FAILED (1 classes: test_guard.NativeBuild) [ran] [tree 087c628ebdc8] [world 2f1906870a] (2026-11-07T04:42:47Z)
- (step 3) `nice -n 10 python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3607/ab.py /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3607/base ~/.claude/foreman.lanes/T-3607 100` → exit 0 · {'before': 0.83, 'after': 0.846} ms CPU per call over 1200 calls each [ran] [tree 75d89321ceac] [world 2f1906870a] (2026-11-07T04:50:28Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_latency test_guard_hardening test_guard_evasions test_guard_git test_guard_diff test_guard_sampo test_guard_state_key test_safety test_replay test_approve_reads` → exit 0 · Ran 386 tests in 157.0s (109 jobs, 16 at a time; slowest: GuardAgainstBash 31s, Mutation 29s, SafetyGate 19s) / OK [ran] [tree 75d89321ceac] [world 2f1906870a] (2026-11-07T04:50:54Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard.NativeBuild` → ✗ exit 1 · Ran 10 tests in 0.8s (1 jobs, 16 at a time; slowest: NativeBuild 0s) / FAILED (1 classes: test_guard.NativeBuild) [ran] [tree 023fdd60dc29] [world 2f1906870a] (2026-11-07T04:59:50Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_latency test_guard_hardening test_guard_evasions test_guard_git test_guard_diff test_guard_sampo test_guard_state_key test_safety test_replay test_approve_reads test_docs` → exit 0 · Ran 505 tests in 38.8s (172 jobs, 16 at a time; slowest: Mutation 38s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 19s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 205ea9871207] [world 2f1906870a] (2026-11-07T05:04:47Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard.NativeBuild` → ✗ exit 1 · Ran 10 tests in 6.7s (1 jobs, 16 at a time; slowest: NativeBuild 2s) / FAILED (1 classes: test_guard.NativeBuild) [ran] [tree 441533fcd0ce] [world 2f1906870a] (2026-11-07T05:08:48Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard test_guard_cases test_guard_latency test_guard_hardening test_guard_evasions test_guard_git test_guard_diff test_guard_sampo test_guard_state_key test_safety test_replay test_approve_reads test_docs` → exit 0 · Ran 505 tests in 79.4s (184 jobs, 16 at a time; slowest: Mutation 74s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 26s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 9deda96dee26] [world 2f1906870a] (2026-11-07T05:11:11Z)
## Log
- 2026-11-07T04:28:02Z created
- 2026-11-07T04:34:12Z planned: it has criteria and steps
- 2026-11-07T04:34:17Z lane: ~/.claude/foreman.lanes/T-3607 on foreman/T-3607
- 2026-11-07T04:34:34Z focused
- 2026-11-07T04:34:34Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-07T05:08:48Z tried: `nice -n 10 python3 plugin/tests/run.py test_guard.NativeBuild` ×3 on step 1, failing the same way
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- T-3571 [FEATURE L, active, 4 steps] PERFORMANCE epic (user 2026-11-06: 'rewrite everything to rust or something, way faster…
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
- similar past tasks were L: consider --tier L
- the similar finished task took 9 steps
