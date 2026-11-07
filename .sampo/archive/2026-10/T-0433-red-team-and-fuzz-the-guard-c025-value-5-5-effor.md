---
id: T-0433
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:44:22Z
base: 9c2722c0d3fa69dd182def0bcb29790d5825e4e4
base_tree: 4e8eb5df022ae8d3538751faef700cb6f1a82128
verified: ok
---
# Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked
## Raw request
> SECURITY: Red-team and fuzz the guard (C025, value 5/5, effort M, risk med)
>   first version: First version: a differential fuzzer in tests that generates shell snippets from a grammar of mutations on known-blocked fixtures, runs fmguard and asserts no known-dangerous effect passes (oracle: bash -n plus a dry effect list in a tmp dir); escapes are saved as test fixtures. Read-only against the guard, so it only tightens.
>   what it is: Attack the guard unattended with adversary agents, fuzzers and leagues, and keep every escape as a regression case.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
A seeded mutation fuzzer inside the real-bash differential test: nest FORMS wrappers inside each other and mutate EXTRA rows (quoting, ${}, $IFS, line breaks, backslash continuation); each case runs in bwrap and fails when dangerous() fires while check_bash returned nothing. Tests and fixtures only: the guard itself never changes here; every escape becomes a fixture plus its own guard-fix task.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixed-seed fuzz of 300 cases finds no bypass, and enough cases really ran — verify with `python3 plugin/tests/run.py -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] every saved escape fixture stays blocked — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked`
## Non-goals
## Approach (options → choice → why)
(A, chosen) grammar nesting + character mutations with a fixed seed: deterministic, no spend. (B, rejected) an LLM adversary agent: spend and nondeterminism; later. Risks: a mutation that makes bash fail early passes vacuously, so keep a 'ran' floor; cap N and the 10 s timeout.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: the fuzz test with its vacuity floor
2. [x] mutators (nest, mutate) beside dangerous() in test_guard_diff.py
3. [x] one wider seed sweep; save each escape as a fixture and capture a guard-fix task (don't fix the guard here)
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / FAILED (1 classes) [ran] [tree c377d1be76c8] (2026-10-09T14:35:00Z)
- (step 2) `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/sweep.py ~/.claude/foreman/.claude/worktrees/agent-a1f57d63268697f32/plugin/tests 433 300` → exit 0 · "bash${IFS}-c 'echo a#b && echo `true`#x; git pus\\h --force or''igin main'" / 'true # c\nrm${IFS}-rf $HOME' [ran] [tree edfd316e401e] (2026-10-09T14:37:59Z)
- (step 1) `python3 plugin/tests/run.py -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 1 tests in 5.3s (1 classes, 16 at a time; slowest: GuardAgainstBash 5s) / OK [ran] [tree 836969f67256] (2026-10-09T14:41:14Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 3 tests in 11.0s (1 classes, 16 at a time; slowest: GuardAgainstBash 11s) / OK [ran] [tree 836969f67256] (2026-10-09T14:41:25Z)
- (step 3) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 836969f67256] (2026-10-09T14:41:26Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (30 pass, 3 warn, 0 fail) (slower: 14.6 s vs a usual 7.5 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.3    36.0     150  [0] / SessionEnd                  30.4    31.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/ [ran] [tree 836969f67256] (2026-10-09T14:42:50Z)
- (step 1) `python3 plugin/tests/run.py -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 2 tests in 3.7s (1 classes, 16 at a time; slowest: GuardAgainstBash 4s) / OK [ran] [tree 1c7534581e86] (2026-10-09T14:44:11Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 3 tests in 6.8s (1 classes, 16 at a time; slowest: GuardAgainstBash 7s) / OK [ran] [tree 1c7534581e86] (2026-10-09T14:44:18Z)
- (step 3) `wider seed sweep` → seeds 1-4 x 6000: ~18.5k dangerous runs, ~3.1k escapes in 9 classes; minimal examples saved as open fixtures; T-0576..T-0584 captured [tree 1c7534581e86] (2026-10-09T14:44:18Z)
- (ac 1) `python3 plugin/tests/run.py -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 1 tests in 3.2s (1 classes, 16 at a time; slowest: GuardAgainstBash 3s) / OK [ran] [tree 1c7534581e86] (2026-10-09T14:44:22Z)
- (ac 2) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 1c7534581e86] (2026-10-09T14:44:22Z)
- (audit adversary) `builder branch read: tests and fixtures only, fmguard.py untouched; vacuity floor (half the cases must make a real dangerous call); open fixtures pinned both ways` → the point of the task; nine escape classes found and each has a fix task [tree 1c7534581e86] (2026-10-09T14:44:22Z)
- (audit intent) `builder branch read: tests and fixtures only, fmguard.py untouched; vacuity floor (half the cases must make a real dangerous call); open fixtures pinned both ways` → an unattended red team for the guard, as the brainstorm asked; no LLM spend [tree 1c7534581e86] (2026-10-09T14:44:22Z)
- (audit edge) `builder branch read: tests and fixtures only, fmguard.py untouched; vacuity floor (half the cases must make a real dangerous call); open fixtures pinned both ways` → changing the corpus changes which cases seed 433 makes, so saved escapes may need re-saving [tree 1c7534581e86] (2026-10-09T14:44:22Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:32:34Z planned from capture
- 2026-10-09T14:32:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0433.builder.md
- 2026-10-09T14:32:49Z focused
- 2026-10-09T14:41:35Z sweep: seeds 1-4 x 6000 cases via FM_FUZZ_SEED and FM_FUZZ_CASES: about 18.5k ran, 3.1k escapes, 9 classes; minimal reproducers saved open in plugin/tests/fixtures/guard_fuzz_escapes.txt; guard-fix tasks left to the main thread
- 2026-10-09T14:43:40Z merged worktree-agent-a1f57d63268697f32 (2 file(s))
- 2026-10-09T14:43:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1f57d63268697f32
- 2026-10-09T14:43:48Z focused
- 2026-10-09T14:44:22Z done
- 2026-10-09T14:44:22Z committed 799455a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0503 [SECURITY M, dropped, 0 steps] Red-team and fuzz the guard (C025, value 5/5, effort M, risk med)
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- T-0550 [SECURITY M, dropped, 0 steps] Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
- decision 2026-10-04: Brainstorm pass 4: 4 grounded ideas (cd-prefixed python heredocs parsed by the guard, test lockout of the real claude, untrusted-text sinks in the a…
## Lessons
- A guard's own tests find what its authors imagined; a mutation fuzzer in real bash finds the rest (3.1k escapes on the first sweep).
## Files touched
- .claude/worktrees/agent-a1f57d63268697f32/plugin/tests/test_guard_diff.py
- .claude/worktrees/agent-a1f57d63268697f32/plugin/tests/fixtures/guard_fuzz_escapes.txt
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmagents.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmfriction.py
- plugin/lib/fmhooks.py
- plugin/lib/fmnight.py
- plugin/lib/fmrecall.py
- plugin/lib/fmserve.py
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/tests/test_agents.py
- plugin/tests/test_cli.py
- plugin/tests/test_friction.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_hooks.py
- plugin/tests/test_night.py
- plugin/tests/test_parallel.py
- plugin/tests/test_serve.py
