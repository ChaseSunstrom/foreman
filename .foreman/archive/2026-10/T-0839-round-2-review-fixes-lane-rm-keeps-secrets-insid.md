---
id: T-0839
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T19:47:55Z
updated: 2026-10-14T19:52:44Z
base: fc60fd94ed0bcc497a73d7e757bec052e50a2861
base_tree: 049d083d9143cfe7f35d49a4f4b4f30e1cf6a86b
verified: strong
---
# Round-2 review fixes: lane rm keeps secrets inside build dirs, step pointer ignores extensionless names, broken pipe exits 141, tidy prune race-safe and keeps read marks, compact survives lone surrogates
## Raw request
> Round-2 review fixes: lane rm keeps secrets inside build dirs, step pointer ignores extensionless names, broken pipe exits 141, tidy prune race-safe and keeps read marks, compact survives lone surrogates
## Interpretation
The round-2 final review's verified findings 1-5 and 7 (6 checked: comm is 'claude' because Linux takes it from the exec'd name).
## Assumptions (confidence)
## Acceptance criteria
- [x] lane rm refuses an ignored build dir holding a .env/.pem/.key or dotfile; step pointer doesn't move on an extensionless name like fm — verify with `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse`
- [x] compact passes a lone surrogate through without crashing; tidy keeps seen-* and survives a file vanishing — verify with `python3 plugin/tests/run.py test_compact test_tidy`
## Non-goals
## Approach (options → choice → why)
Options: (a) local fixes per finding; (b) a --clean flag on lane rm instead of cache rules; (c) revert T-0833. Chose (a): keeps T-0833's no-throwaway-task removal for real build output while refusing anything secret-shaped inside it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests
2. [x] Fixes in fmlanes, fmhooks, compact, fmtidy, bin/fm
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse test_compact test_tidy` → exit 0 · Ran 63 tests in 13.2s (14 classes, 16 at a time; slowest: PreToolUse 13s, Contract 6s, Brief 3s) / OK [ran] [tree 8fe4b0546f8b] (2026-10-14T19:50:01Z)
- (step 2) `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse test_compact test_tidy` → exit 0 · Ran 63 tests in 13.3s (14 classes, 16 at a time; slowest: PreToolUse 13s, Contract 6s, Brief 3s) / OK [ran] [tree 8fe4b0546f8b] (2026-10-14T19:50:15Z)
- `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse test_compact test_tidy` → ✗ exit 1 · Ran 63 tests in 13.7s (14 classes, 16 at a time; slowest: PreToolUse 13s, Contract 6s, Brief 3s) / FAILED (4 classes) (start tree + this task's tests) [ran] [tree 8fe4b0546f8b] (2026-10-14T19:50:42Z)
- `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse test_compact test_tidy` → exit 0 · Ran 63 tests in 13.3s (14 classes, 16 at a time; slowest: PreToolUse 13s, Contract 6s, Brief 3s) / OK [ran] [tree 8fe4b0546f8b] (2026-10-14T19:50:42Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.1    35.6     150  [0] / SessionEnd                  30.9    32.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 8fe4b0546f8b] (2026-10-14T19:52:20Z)
- (ac 1) `python3 plugin/tests/run.py test_builder test_hooks.PreToolUse` → exit 0 · Ran 43 tests in 13.1s (7 classes, 16 at a time; slowest: PreToolUse 13s, Contract 6s, Brief 3s) / OK [ran] [tree 8fe4b0546f8b] (2026-10-14T19:52:43Z)
- (ac 2) `python3 plugin/tests/run.py test_compact test_tidy` → exit 0 · Ran 20 tests in 1.7s (8 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree 8fe4b0546f8b] (2026-10-14T19:52:43Z)
- (audit intent) `self: each of the round-2 review's findings 1-5 and 7 fixed with a failing test first; finding 6 checked live (comm is 'claude': Linux takes it from the exec'd name, claude.exe here, a 'claude' symlink in native installs); hook bench within SLO with the extra note` → lane rm still removes a lane with only build output (T-0833 case) but refuses a .pem/.key/.env/id_* or credentials file inside one; bin/fm edits no longer move a step that says 'run fm check'; a reader quitting gives exit 141, so a command cut short never reads as success; tidy keeps read marks and survives races; compact writes a lone surrogate as U+FFFD [tree 8fe4b0546f8b] (2026-10-14T19:52:43Z)
- (audit edge) `self: each of the round-2 review's findings 1-5 and 7 fixed with a failing test first; finding 6 checked live (comm is 'claude': Linux takes it from the exec'd name, claude.exe here, a 'claude' symlink in native installs); hook bench within SLO with the extra note` → secret-name pattern kept narrow so Rust's env_logger-*.d and libsecret-*.rlib don't refuse; the walk stops after 5 hits; an extensionless file only moves the pointer when the step names its path [tree 8fe4b0546f8b] (2026-10-14T19:52:43Z)
## Log
- 2026-10-14T19:47:55Z created
- 2026-10-14T19:47:55Z focused
- 2026-10-14T19:52:43Z done
- 2026-10-14T19:52:44Z committed 950a1c1 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
## Why not caught
none: found by the final cross-task review, the check meant to catch them
## Lessons
- A cache rule that deletes a whole folder must still look inside it for things no build makes
## Files touched
- plugin/tests/test_builder.py
- plugin/tests/test_hooks.py
- plugin/tests/test_compact.py
- plugin/tests/test_tidy.py
- plugin/lib/fmlanes.py
- plugin/lib/fmhooks.py
- plugin/bin/fm
- plugin/hooks/compact
- plugin/lib/fmtidy.py
