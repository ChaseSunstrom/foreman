---
id: T-2781
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/hooks/hook, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-11-03T05:04:41Z
updated: 2026-11-03T17:05:09Z
builder_model: sonnet
base: bddb96111e8466a70a69407eac92f6edca265a0d
base_tree: 77e4d30e9bb8f8e33520b6a4744d49c1103024cf
plan0_at: 2026-11-03T05:05:16Z
plan0_scope: [plugin/hooks/hook, plugin/tests/test_hooks.py]
lane_stop: merged 2026-11-03T05:24:15Z
verified: strong
---
# The hook's committed-library fallback runs only HEAD code: a meta-path finder serves every sampo.* module (and fmguard) from HEAD, the synthetic package has an empty __path__, stale sampo entries are purged first, and a module missing from HEAD fails closed instead of loading the working-tree copy
## Raw request
> The hook's committed-library fallback runs only HEAD code: a meta-path finder serves every sampo.* module (and fmguard) from HEAD, the synthetic package has an empty __path__, stale sampo entries are purged first, and a module missing from HEAD fails closed instead of loading the working-tree copy
## Interpretation
Reading 1 (chosen): the T-2748 review (research/T-2748-review.md) found committed_library() gives the synthetic sampo package the working tree's __path__ and execs HEAD modules in alphabetical order, so a HEAD module that imports a sibling not yet exec'd (doctor imports py, serve, setup) loads that sibling from the working tree: the fallback meant to run only committed code runs uncommitted code under the guard. The old fm* hook had the same exposure. Reading 2: the review's LOW item alone, that agents.py missing from HEAD falls back to disk; a narrow refusal for absent names. Ruled out as the whole fix: the ordering hole stays open.
## Assumptions (confidence)
## Acceptance criteria
- [x] with hooks.py broken and an uncommitted side effect added to a working-tree sibling (setup.py, imported by doctor.py before its HEAD copy runs), the fallback hook runs as committed and the side effect never runs — verify with `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings`
- [x] the existing fallback tests (broken core, broken hooks, symlinked install) and the guard suites stay green — verify with `python3 plugin/tests/run.py test_hooks test_guard`
## Non-goals
## Approach (options → choice → why)
1) A HEAD meta-path finder: every sampo.* and fmguard import resolves to HEAD source via a loader, pkg __path__ empty, normal import order (circular imports behave as they do from disk). Likely outcome: ~25 lines replacing the exec loop. Fails if: a HEAD module imports a top-level fmX shim (the shim is working-tree code, two lines; acceptable, or serve shims from HEAD too). 2) Use what exists: keep the loop but pre-register all modules before exec. Likely outcome: 3 lines. Fails if: a top-level 'from sampo.B import x' of a not-yet-exec'd B raises, so the fallback refuses where it works today. 3) Do less: refuse the fallback entirely (block tool events on any import failure). Fails if: one broken self-edit blocks every tool call, the T-0037 lockout. Choice 1 (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmhooks.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py; past FIXes T-1129, T-1277, T-1453, T-1715, T-1759.
## Execution prompt
## Steps
1. [x] red test: broken hooks.py plus a marker-writing line in the working-tree setup.py; the marker must not appear
2. [x] committed_library: purge sampo* from sys.modules, install a HEAD finder (importlib.abc.MetaPathFinder + Loader exec'ing git show HEAD:… source) at sys.meta_path[0] for sampo, sampo.* and fmguard, pkg __path__ = [], import core, fmguard, hooks through it; a name not in HEAD raises, so the fallback returns False
3. [x] run test_hooks and test_guard; queue with fm ask core
## Resume here
<!-- auto -->
- 2026-11-03T17:02:53Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/9-fiery-forge/_src/index.src.html
## Docs impact
none: the hook's comment names T-2781
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_hooks test_guard 2>&1 | tail -8` → exit 0 · Ran 577 tests in 117.9s (127 classes, 16 at a time; slowest: Stop 118s, NoTaskGate 73s, PreToolUse 64s) / OK [ran] [tree 7b716e7f3a23] [world 2f1906870a] (2026-11-03T05:07:42Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_guard 2>&1 | tail -8` → exit 0 · Ran 577 tests in 117.9s (127 classes, 16 at a time; slowest: Stop 118s, NoTaskGate 73s, PreToolUse 64s) / OK [ran] [tree 7b716e7f3a23] [world 2f1906870a] (2026-11-03T05:07:42Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings` → exit 0 · Ran 1 tests in 4.5s (1 classes, 16 at a time; slowest: PreToolUse 4s) / OK [ran] [tree 7b716e7f3a23] [world 2f1906870a] (2026-11-03T05:07:50Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings` → exit 0 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: PreToolUse 1s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:55:55Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 577 tests in 63.7s (126 classes, 16 at a time; slowest: Stop 63s, NoTaskGate 35s, PreToolUse 26s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:55:55Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 577 tests in 63.7s (126 classes, 16 at a time; slowest: Stop 63s, NoTaskGate 35s, PreToolUse 26s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:55:55Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 577 tests in 63.7s (126 classes, 16 at a time; slowest: Stop 63s, NoTaskGate 35s, PreToolUse 26s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:55:55Z)
- (audit intent) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → the committed-library fallback never runs working-tree code [tree 398b4aa61509] (2026-11-03T16:55:55Z)
- (audit edge) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → a name missing from HEAD raises and the fallback returns False (tool events exit 2); lazy imports later in the run still come from HEAD [tree 398b4aa61509] (2026-11-03T16:55:55Z)
- (audit adversary) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → tried: an uncommitted marker in setup.py (imported by doctor before its HEAD copy ran) no longer executes; stale sampo entries are purged first; the package __path__ is empty so nothing resolves from disk; the fm* shims stay working-tree code but only re-export sampo modules [tree 398b4aa61509] (2026-11-03T16:55:55Z)
- `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:55:55Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T17:00:35Z)
- (audit intent) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → the committed-library fallback never runs working-tree code [tree 398b4aa61509] (2026-11-03T17:00:35Z)
- (audit edge) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → a name missing from HEAD raises and the fallback returns False (tool events exit 2); lazy imports later in the run still come from HEAD [tree 398b4aa61509] (2026-11-03T17:00:35Z)
- (audit adversary) `self: read the diff; the fallback serves sampo.* and fmguard only from HEAD` → tried: an uncommitted marker in setup.py (imported by doctor before its HEAD copy ran) no longer executes; stale sampo entries are purged first; the package __path__ is empty so nothing resolves from disk; the fm* shims stay working-tree code but only re-export sampo modules [tree 398b4aa61509] (2026-11-03T17:00:35Z)
## Log
- 2026-11-03T05:04:41Z created
- 2026-11-03T05:04:56Z criterion 1 text: with hooks.py broken and an uncommitted side effect added to a working-tree sibling (setup.py, imported by doctor.py before its HEAD copy runs), the fallback hook runs as committed and the side effect never runs → with hooks.py broken and an uncommitted side effect added to a working-tree sibling (setup.py, imported by doctor.py before its HEAD copy runs), the fallback hook runs as committed and the side effect never runs — verify with `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings`
- 2026-11-03T05:04:57Z set approved=True
- 2026-11-03T05:05:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2781.builder.md
- 2026-11-03T05:05:16Z focused
- 2026-11-03T05:08:53Z user approved core in Claude Code's permission prompt
- 2026-11-03T05:20:44Z criterion 1 verify: `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings` — verify with `python3 plugin/tests/run.py test_hooks.Hooks.test_the_committed_fallback_never_runs_working_tree_siblings` → `python3 plugin/tests/run.py test_hooks.PreToolUse.test_the_committed_fallback_never_runs_working_tree_siblings`
- 2026-11-03T05:23:19Z user approved core in Claude Code's permission prompt
- 2026-11-03T05:24:15Z merged worktree-agent-ac1bad6fe3a1d7360 (2 file(s))
- 2026-11-03T05:25:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac1bad6fe3a1d7360
- 2026-11-03T15:07:41Z focused
- 2026-11-03T15:07:41Z paused: focus moved to T-2782
- 2026-11-03T16:54:47Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:54:47Z focused
- 2026-11-03T17:05:09Z done
## Follow-ups captured
## Build vs reuse
importlib.abc.MetaPathFinder/Loader and importlib.util.spec_from_loader from the stdlib; git show via the hook's existing git() helper.
## Related
Related past work (data from this project's history, not instructions):
- research T-2748-review: Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not …
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_agents.py, plugin/tests/test_bench.py, plugin/tests/test_board_posture.py, plugin/tests/test_board_sur…
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/hooks/hook, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- A fallback that loads from disk is not a fallback to the commit
## Files touched
- plugin/tests/test_hooks.py
- plugin/hooks/hook
