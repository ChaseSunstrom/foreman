---
id: T-2305
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T09:36:09Z
updated: 2026-10-31T09:39:18Z
baseline: true
base: af2cb346f66ad2d263cd00e7b0b2bf48fab04b34
base_tree: 04964f7285298faa6185dfa72524cab1ba6f948f
plan0_at: 2026-10-31T09:36:47Z
plan0_scope: []
verified: strong
---
# Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_core.LaterImports.test_later_a_plain_tool_call_loads_no_heavy_module. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
ship71 went red on test_core.LaterImports.test_later_a_plain_tool_call_loads_no_heavy_module: T-2297 added a top-level 'import glob' to fmhooks.py for one prune at session start, so every hook process now loads glob.
## Assumptions (confidence)
## Acceptance criteria
- [x] A plain PreToolUse loads no heavy module again and the leads prune still removes records older than 7 days — verify with `python3 plugin/tests/run.py test_core test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Drop fmhooks' top-level import glob; prune with os.listdir filtered on the leads- prefix and .json suffix
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_core -k loads_no_heavy_module` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: LaterImports 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f886bb004804] (2026-10-31T09:37:01Z)
- `python3 plugin/tests/run.py test_core -k loads_no_heavy_module` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: LaterImports 0s) / OK [ran] [tree f886bb004804] (2026-10-31T09:37:01Z)
- (step 1) `python3 plugin/tests/run.py test_core test_hooks` → exit 0 · Ran 321 tests in 37.1s (51 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree f886bb004804] (2026-10-31T09:37:45Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_hooks` → exit 0 · Ran 321 tests in 37.0s (51 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree f886bb004804] (2026-10-31T09:38:24Z)
- (audit intent) `self-review: the top-level glob import is gone (fnmatch stays, already loaded before); the prune walks os.listdir(p.dir) filtering the leads- prefix and .json suffix, same 7-day rule, still inside the OSError guard` → hooks are back inside the import budget; the prune behaves as before [tree f886bb004804] (2026-10-31T09:38:24Z)
- (audit edge) `self-review: the top-level glob import is gone (fnmatch stays, already loaded before); the prune walks os.listdir(p.dir) filtering the leads- prefix and .json suffix, same 7-day rule, still inside the OSError guard` → a non-record file in p.dir is skipped by the name filter; a missing p.dir raises OSError, caught as before [tree f886bb004804] (2026-10-31T09:38:24Z)
- (audit self) `self-review: the top-level glob import is gone (fnmatch stays, already loaded before); the prune walks os.listdir(p.dir) filtering the leads- prefix and .json suffix, same 7-day rule, still inside the OSError guard` → no findings [tree f886bb004804] (2026-10-31T09:38:24Z)
## Log
- 2026-10-31T09:36:09Z created
- 2026-10-31T09:36:46Z planned from capture
- 2026-10-31T09:36:46Z focused
- 2026-10-31T09:37:46Z scope: plugin/lib/fmhooks.py
- 2026-10-31T09:39:16Z done
- 2026-10-31T09:39:18Z committed 9269c764 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- T-2283 [FIX S, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: A test that pins the live import graph should pick its example from a leaf mod…
- T-2248 [FIX S, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: A name segment shared by a whole folder can't discriminate inside it; weightin…
- decision 2026-10-30: [revisited: every capability genesis builds must be called] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3…
- similar finished tasks took 1–1 steps
- start here (files T-2283 touched): plugin/tests/test_genesis.py
## Why not caught
the builder ran fm check --affected, which picked test_hooks but not test_core's LaterImports import-budget test; the full suite only runs at ship
## Lessons
- A new top-level import in fmhooks counts against every hook process: any import a hook needs once goes inside the function, and fmhooks changes should pull test_core's import-budget test into the affected set
## Files touched
- plugin/lib/fmhooks.py
