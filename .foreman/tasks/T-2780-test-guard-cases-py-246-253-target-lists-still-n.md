---
id: T-2780
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/tests/test_guard_cases.py]
depends_on: []
source: discovered
created: 2026-11-03T05:03:52Z
updated: 2026-11-03T17:29:46Z
builder_model: sonnet
base: 7271b3d8f0fa459c6866106f38afc87e61cf3c39
base_tree: 0d208b7bd16ebd4fefcbef9bc516f7d4fa6ce39c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T05:37:32Z
plan0_scope: [plugin/tests/test_guard_cases.py]
lane_stop: merged 2026-11-03T14:27:26Z
verified: strong
unproven: [meaning]
---
# test_evolve_never_revises_the_guards_own_files tries the guard's files under their sampo names too (plugin/lib/sampo/hooks.py, replay, evolve, mutate, bench), not only the fm* shims, so the lock is tested where the code now lives
## Raw request
> - test_guard_cases.py:246-253 target lists still name shimmed fm paths
> (noticed by an agent; research T-2748-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the target list holds both the fm* and the plugin/lib/sampo/ paths and the test passes (evolve.GUARD already matches both) — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the sampo/ paths to the target list; run test_guard_cases
## Resume here
## Docs impact
none
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree f49132869b08] [world 2f1906870a] (2026-11-03T06:03:49Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 2.3s (2 classes, 16 at a time; slowest: GuardCases 2s, AllowCorpus 0s) / OK [ran] [tree 1d91becbc3e2] [world 2f1906870a] (2026-11-03T06:04:02Z)
- (step 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 1.9s (2 classes, 16 at a time; slowest: GuardCases 2s, AllowCorpus 0s) / OK [ran] [tree 1d91becbc3e2] [world 2f1906870a] (2026-11-03T06:04:06Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_guard_cases && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.46s] [ran] [tree 1d91becbc3e2] [world 2f1906870a] (2026-11-03T06:04:32Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 1.9s (2 classes, 16 at a time; slowest: GuardCases 2s, AllowCorpus 0s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:29:28Z)
- (audit intent) `self: read the diff; the evolve-lock targets include the sampo paths` → the guard's no-revise lock is tested where the code now lives [tree 07445d19b39c] (2026-11-03T17:29:28Z)
- (audit edge) `self: read the diff; the evolve-lock targets include the sampo paths` → the fm* entries stay; the five sampo files exist [tree 07445d19b39c] (2026-11-03T17:29:28Z)
- (audit adversary) `self: read the diff; the evolve-lock targets include the sampo paths` → only makes the guard's own test stricter [tree 07445d19b39c] (2026-11-03T17:29:28Z)
- (audit self) `self: read the diff; the evolve-lock targets include the sampo paths` → no findings [tree 07445d19b39c] (2026-11-03T17:29:28Z)
## Log
- 2026-11-03T05:03:52Z created
- 2026-11-03T05:37:18Z planned from capture
- 2026-11-03T05:37:18Z set approved=True
- 2026-11-03T05:37:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2780.builder.md
- 2026-11-03T05:37:31Z focused
- 2026-11-03T05:37:32Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T14:21:19Z user approved core in Claude Code's permission prompt
- 2026-11-03T14:27:26Z merged worktree-agent-a4a9b7d99115a881c (1 file(s))
- 2026-11-03T14:28:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4a9b7d99115a881c
- 2026-11-03T15:07:46Z focused
- 2026-11-03T15:15:30Z paused: focus moved to T-2779
- 2026-11-03T17:05:17Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:17Z focused
- 2026-11-03T17:05:18Z paused: focus moved to T-2779
- 2026-11-03T17:29:24Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:29:24Z focused
- 2026-11-03T17:29:46Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- research T-2748-review: Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not …
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/tests/test_guard_cases.py; re-ground the plan against them before editing
## Lessons
- Move a lock's tests with the files it protects
## Plan gaps
- failed first: step 1 add the sampo/ paths to the target list; run test_guard_cases
## Files touched
- plugin/tests/test_guard_cases.py
