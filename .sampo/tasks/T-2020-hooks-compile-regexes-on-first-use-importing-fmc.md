---
id: T-2020
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T17:24:13Z
updated: 2026-10-29T17:45:13Z
base: 67768c6bfb0fc89dff2ae7cdd68eb6a4889506ba
base_tree: e1f8a6534e1a7b15b0fd68eaaa8277e2211c02dc
plan0_at: 2026-10-29T17:33:02Z
plan0_scope: []
verified: strong
---
# Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns
## Raw request
> Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns
## Interpretation
Every hook process imports fmcore, fmhooks and (PreToolUse) fmguard, compiling ~190 module-level patterns (~25 ms) of which a call uses ~44. Defer each compile to first use; behaviour unchanged.
## Assumptions (confidence)
## Acceptance criteria
- [x] importing fmcore, fmguard and fmhooks compiles no module-level pattern — verify with `python3 plugin/tests/run.py test_core -k lazy`
- [x] the PreToolUse and Notification hooks get faster (hook_t.py before/after) — verify with `python3 plugin/tests/run.py test_core test_guard test_hooks`
## Non-goals
## Approach (options → choice → why)
lazy(pattern, flags) proxy in fmcore and fmguard (fmguard imports no Foreman module): __getattr__ compiles once and caches each bound method as a plain attribute. Sites change only re.compile( -> lazy( (fmhooks: c.lazy(), applied by one fm edit draft. Rejected: patching re.compile during import (defers stdlib too), bare strings + re's cache (every call site changes), a new fmre module (hook loader orders modules by name).
## Risks and rollback
A pattern passed bare to re.* or isinstance-checked would break: reuse.py found none. Compile errors move from import to first use: the test compiles every lazy pattern. Rollback: git revert.
## Execution prompt
## Steps
1. [x] test: no module-level compile at import (red)
2. [x] lazy() in fmcore and fmguard; 191 sites via fm edit; measure
## Resume here
<!-- auto -->
- 2026-10-29T17:42:21Z step 1/2: test: no module-level compile at import (red)
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/tests/test_core.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/hook_t.py, plugin/tests/test_core.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ld_t.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ld_parts.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/rd_t.py
- failures met: fmguard.py:0:class lazy: # noqa: n0 — fmcore.lazy's twin: this module imports no other fo…
## Docs impact
CHANGELOG line added
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k lazy` → ✗ exit 1 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: LazyPatterns 0s) / FAILED (1 classes) [ran] [tree da7540c0674c] (2026-10-29T17:33:43Z)
- (ac 2) `python3 plugin/tests/run.py test_core test_guard test_hooks 2>&1 | tail -3` → exit 0 · Ran 587 tests in 64.3s (133 classes, 16 at a time; slowest: Stop 64s, NoTaskGate 53s, PreToolUse 47s) / OK [ran] [tree f20b116f9910] (2026-10-29T17:35:35Z)
- (step 2) `python3 plugin/tests/run.py test_core test_guard test_hooks` → exit 0 · Ran 587 tests in 35.1s (133 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree d24e6f8182bf] (2026-10-29T17:38:09Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.6    33.8     150  [0] / SessionEnd                  27.0    27.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 9334b345704e] (2026-10-29T17:42:34Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k lazy` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: LazyPatterns 0s) / OK [ran] [tree 9334b345704e] (2026-10-29T17:44:31Z)
- (ac 2) `python3 plugin/tests/run.py test_core test_guard test_hooks` → exit 0 · Ran 587 tests in 35.1s (133 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree 9334b345704e] (2026-10-29T17:44:31Z)
- (step 1) `python3 plugin/tests/run.py test_core -k lazy` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: LazyPatterns 0s) / OK [ran] [tree 9334b345704e] (2026-10-29T17:44:31Z)
- (audit intent) `self-review (budget spent): lazy proxies compile on first attribute use; no bare re.* use or isinstance check on these names; a test compiles every deferred pattern; gates green` → hooks stop compiling ~190 patterns at import; behaviour unchanged [tree 9334b345704e] (2026-10-29T17:44:31Z)
- (audit edge) `self-review (budget spent): lazy proxies compile on first attribute use; no bare re.* use or isinstance check on these names; a test compiles every deferred pattern; gates green` → a bad pattern now raises at first use, caught by the compile-all test; dunder lookups raise AttributeError so copy/pickle/repr stay default; two threads compiling at once is harmless [tree 9334b345704e] (2026-10-29T17:44:31Z)
- (audit adversary) `self-review (budget spent): lazy proxies compile on first attribute use; no bare re.* use or isinstance check on these names; a test compiles every deferred pattern; gates green` → a guard pattern passed to re.sub/re.match as an object or checked with isinstance would TypeError and could fail open; scanned all 87 fmguard sites, none is used that way; fm replay ran 124 labelled guard cases with 0 drifted, and the compile-all test touches every deferred guard pattern [tree 9334b345704e] (2026-10-29T17:44:31Z)
## Log
- 2026-10-29T17:24:13Z created
- 2026-10-29T17:24:18Z approaches: (1) lazy() proxy compiling on first attribute use, defined in fmcore and fmguard (fmguard imports no Foreman module) — chosen: one name per site, call sites unchanged; (2) patch re.compile during import — rejected, it also defers stdlib modules imported meanwhile; (3) raw strings + re.search(str) via re's cache — rejected, changes every call site and churns the 512-entry cache; (4) a new fmre module — rejected, hooks/hook's committed_library loader orders modules by name and needs it first. Audit: no pattern is passed bare to re.* or isinstance-checked (reuse.py: only aliases and 'is').
- 2026-10-29T17:33:01Z focused
- 2026-10-29T17:45:11Z done
- 2026-10-29T17:45:13Z committed 23bbf735 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1142 [PERFORMANCE M, dropped, 0 steps] Hook import cost: about 217 regex compiles (≈80 ms profiled) on every hook process: compil
- research T-1879-review: Verdict:** changes needed (two small gaps against the acceptance criterion). I read the diff and the surrounding code but did not run `plugin/tes…
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- decision 2026-10-23: [costly] T-1266 deferred to 2026-10-28: Foreman's measured small-task overhead is about 1 cent a task (+4% and +13% on sonnet suites, level on haiku…
## Measurements
PreToolUse min 57 -> 44 ms; Notification min 95 -> 85 ms; fm-module compiles at import 191 -> 0
## Lessons
- Module-level re.compile is import cost every hook pays; defer with a lazy proxy and keep a compile-all test
## Plan gaps
- failed first: step 1 test: no module-level compile at import (red)
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
