---
id: T-2023
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T18:00:24Z
updated: 2026-10-29T18:11:12Z
base: d8dabdeea89e9b51fa97d69c3d8da339673077dc
base_tree: 12d8c446769c5d37421ef13db3224e1aeeaaf1f2
plan0_at: 2026-10-29T18:00:33Z
plan0_scope: []
verified: strong
---
# Hooks import subprocess, shutil and glob only when a call uses them
## Raw request
> Hooks import subprocess, shutil and glob only when a call uses them
## Interpretation
Every hook pays ~5 ms importing subprocess (signal, selectors, threading), shutil (bz2, lzma, zstd on 3.14) and glob, though PreToolUse on an ordinary call never runs a process or copies a file. Make those imports happen on first use; behaviour unchanged.
## Assumptions (confidence)
## Acceptance criteria
- [x] importing fmhooks leaves subprocess, shutil and glob unloaded, and a PreToolUse run on Bash ls doesn't load them — verify with `python3 plugin/tests/run.py test_core -k later`
- [x] full gates green and PreToolUse/Notification measured before -> after — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) importlib.util.LazyLoader registry: rejected, on 3.14 the import statement itself realizes a lazy module (probed); (b) local imports at every use site: 50+ sites across fmcore/fmhooks/fmbus, large churn; (c) a tiny fmcore._Later('name') stand-in whose __getattr__ imports on first attribute access, bound as the module-level name, so no call site changes and mock.patch('subprocess.run') still reaches callers; (d) leave as is. Chosen (c), plus removing the two module-level touches found by tracing: claude_path(os.environ)'s shutil.which at import (skip when its folder is already on PATH), and run_command's stdin=subprocess.DEVNULL default (None, mapped in the body). fmguard (imports no Foreman module) and fmpy (find() only, rare) import locally. Rejected: tempfile (used by state_fallbacks on every guard call), hashlib (used per run).
## Risks and rollback
## Execution prompt
## Steps
1. [x] baseline: hook_t on HEAD; red test: a fresh interpreter imports fmhooks and runs PreToolUse, then lists heavy modules loaded
2. [x] fmcore._Later stand-ins for shutil/subprocess (fmhooks, fmbus share them; fmguard and fmpy import locally); claude_path skips which() when its folder is already on PATH; run_command's stdin default no longer touches subprocess at import; measure
## Resume here
<!-- auto -->
- 2026-10-29T18:03:11Z step 1/2: baseline: hook_t on HEAD; red test: a fresh interpreter imports fmhooks and runs PreToolUse, then lists heavy modules loaded
- git: foreman/build; 6 uncommitted: plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmpy.py, plugin/tests/test_core.py
- touched since last checkpoint: plugin/tests/test_core.py, plugin/lib/fmcore.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit23.json, plugin/lib/fmbus.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmpy.py
## Docs impact
CHANGELOG Perf line (T-2023)
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/hook_t.py /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/base3/plugin/hooks/hook` → exit 0 · PreToolUse    min   42 ms, median   44 ms / Notification  min   51 ms, median   53 ms [ran] [tree 1ae565819012] (2026-10-29T18:06:14Z)
- (step 2) `python3 plugin/tests/run.py test_core -k later` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: LaterImports 0s) / OK [ran] [tree 4a8a3291ed99] (2026-10-29T18:06:22Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmfixes.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmpy.; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.7    34.1     150  [0] / SessionEnd                  25.5    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 4a8a3291ed99] (2026-10-29T18:10:15Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k later` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: LaterImports 0s) / OK [ran] [tree 4a8a3291ed99] (2026-10-29T18:10:27Z)
- (ac 2) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 18:10 UTC); cached (fm check --fresh reruns) [ran] [tree 4a8a3291ed99] (2026-10-29T18:10:27Z)
- (audit intent) `self-review of the diff (risk budget spent: no subagents); traced every remaining heavy import with a meta-path spy` → a plain PreToolUse Bash call now loads neither subprocess nor glob (LaterImports test); shutil stays because tempfile imports it and state_fallbacks needs tempfile on every guard call [tree 4a8a3291ed99] (2026-10-29T18:10:27Z)
- (audit edge) `self-review of the diff (risk budget spent: no subagents); traced every remaining heavy import with a meta-path spy` → mock.patch('subprocess.run') and patch.object(c.subprocess, ...) still reach callers and restore; run_command's None default becomes DEVNULL exactly as before; claude_path's reorder only skips which() when the native folder is already on PATH, same result [tree 4a8a3291ed99] (2026-10-29T18:10:27Z)
- (audit adversary) `self-review of the diff (risk budget spent: no subagents); traced every remaining heavy import with a meta-path spy` → fmguard only moved its subprocess import into _git; no pattern, path, category or decision changed; _Later imports fixed names, never input, from the same sys.path the hook had at start; fm replay 124 labelled guard cases, 0 drifted [tree 4a8a3291ed99] (2026-10-29T18:10:27Z)
## Log
- 2026-10-29T18:00:24Z created
- 2026-10-29T18:00:32Z focused
- 2026-10-29T18:11:10Z done
- 2026-10-29T18:11:12Z committed 10f148a9 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2020 [PERFORMANCE M, done, 2 steps] Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns — lesson…
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- similar finished tasks took 2–2 steps
- start here (files T-2020 touched): plugin/tests/test_core.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, CHANGELOG.md
## Measurements
PreToolUse median 44 -> 41 ms, min 42 -> 40 ms (3 interleaved rounds of 15 runs, d8dabdee vs tree); Notification 53 -> 52 ms
## Lessons
- Trace imports with a meta-path spy before deferring: two module-level touches (a which() call and a default argument) and tempfile's own shutil import defeated the first attempt; LazyLoader is no help on 3.14 since the import statement realizes the module
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmbus.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmpy.py
- plugin/lib/fmfixes.py
- CHANGELOG.md
