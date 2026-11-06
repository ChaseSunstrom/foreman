---
id: T-1466
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T15:05:11Z
updated: 2026-10-22T15:51:27Z
base: 55c5403577a0064d432ee1a2f424fdca04e46f5f
base_tree: 8152616d27b9be4dd980a5b526ec3da59596ccc5
plan0_at: 2026-10-22T15:39:15Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
verified: strong
---
# Supply check accepts a pyc that matches its source
## Raw request
> Supply check (after T-1459): a __pycache__/*.pyc Python writes at runtime (first import, a Python upgrade) reads as a plugin change; accept a .pyc whose header (magic, source mtime and size, or hash-based) matches its source .py beside it, and keep flagging any other .pyc (a tampered or orphan one runs)
## Interpretation
After T-1459, a __pycache__/*.pyc Python writes at runtime (first import, a Python upgrade) reads as a plugin change. A pyc is derived: its 16-byte header names its source's mtime and size (or a source hash).
## Assumptions (confidence)
## Acceptance criteria
- [x] a pyc py_compile wrote for its source adds nothing; a pyc whose body differs under a matching header, an orphan pyc, or another Python's pyc still shows — verify with `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change`
## Non-goals
## Approach (options → choice → why)
Options: (1) trust a pyc whose header matches its source (mtime/size) — rejected: Python runs a timestamp pyc without checking its body, so a tampered body under a copied header is exactly the attack; (2) skip __pycache__ entirely — same hole; (3) chosen: a __pycache__/NAME.TAG.pyc gets no stand-in only when its magic is this interpreter's (importlib.util.MAGIC_NUMBER), its header matches the NAME.py beside the folder, and its body equals marshal.dumps(compile(source, source_path, 'exec', dont_inherit=True)) — the bytes py_compile writes. Any other pyc (another Python's, hash-based, orphan, mismatched, over a size cap) keeps its stand-in. Bounded: at most 200 pycs compiled per plugin, sources up to 1 MB.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skip matching pycs in the stand-ins
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change 2>&1 | tail -5` → ✗ exit 1 · Ran 1 test in 0.128s / FAILED (failures=1) [ran] [tree ea0ef31f204e] (2026-10-22T15:40:43Z)
- `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change` → ✗ exit 1 · Ran 1 test in 0.034s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 47ded3e47d9d] (2026-10-22T15:50:44Z)
- `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change` → exit 0 · Ran 1 test in 0.062s / OK [ran] [tree 47ded3e47d9d] (2026-10-22T15:50:44Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change` → exit 0 · Ran 1 test in 0.104s / OK [ran] [tree 47ded3e47d9d] (2026-10-22T15:50:46Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change` → exit 0 · Ran 1 test in 0.071s / OK [ran] [tree 47ded3e47d9d] (2026-10-22T15:50:47Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_a_pyc_matching_its_source_is_not_a_change` → exit 0 · Ran 1 test in 0.066s / OK [ran] [tree 54b988f4d191] (2026-10-22T15:51:14Z)
- (audit adversary) `builder (sonnet) test-first; red proved with fm task prove; self-review of _pyc_of_source: path must be cache_from_source(src), header must be this MAGIC + flags 0 + source mtime/size, body must re-dump equal to compile(source, abspath) re-dumped, nothing trailing; any exception → keep the stand-in. test_supply_delta + test_doctor green.` → a tampered body under a copied header differs in the code graph → flagged (tested with one flipped byte); marshal.load only builds objects (no code runs) and is capped at 8 MB; a crash in marshal on hostile data would end fm doctor, not run anything [tree 54b988f4d191] (2026-10-22T15:51:14Z)
- (audit edge) `builder (sonnet) test-first; red proved with fm task prove; self-review of _pyc_of_source: path must be cache_from_source(src), header must be this MAGIC + flags 0 + source mtime/size, body must re-dump equal to compile(source, abspath) re-dumped, nothing trailing; any exception → keep the stand-in. test_supply_delta + test_doctor green.` → re-dump comparison because marshal ref flags follow refcounts per process; a relocated or symlinked install mismatches and stays flagged (safe side) [tree 54b988f4d191] (2026-10-22T15:51:14Z)
- (audit intent) `builder (sonnet) test-first; red proved with fm task prove; self-review of _pyc_of_source: path must be cache_from_source(src), header must be this MAGIC + flags 0 + source mtime/size, body must re-dump equal to compile(source, abspath) re-dumped, nothing trailing; any exception → keep the stand-in. test_supply_delta + test_doctor green.` → runtime pycs (first import, Python upgrade under the same interpreter) stop reading as plugin changes [tree 54b988f4d191] (2026-10-22T15:51:14Z)
- (audit self) `builder (sonnet) test-first; red proved with fm task prove; self-review of _pyc_of_source: path must be cache_from_source(src), header must be this MAGIC + flags 0 + source mtime/size, body must re-dump equal to compile(source, abspath) re-dumped, nothing trailing; any exception → keep the stand-in. test_supply_delta + test_doctor green.` → no findings [tree 54b988f4d191] (2026-10-22T15:51:14Z)
## Log
- 2026-10-22T15:05:11Z created
- 2026-10-22T15:38:12Z planned from capture
- 2026-10-22T15:38:36Z set type=SECURITY
- 2026-10-22T15:38:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1466.builder.md
- 2026-10-22T15:39:14Z focused
- 2026-10-22T15:50:38Z merged worktree-agent-a0602b72a11c9020d (2 file(s))
- 2026-10-22T15:50:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0602b72a11c9020d
- 2026-10-22T15:50:41Z focused
- 2026-10-22T15:51:24Z done
- 2026-10-22T15:51:27Z committed 073726fb (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0876 [FIX S, done, 1 steps] Evidence runs never read a .pyc older than its source (a same-second, same-size edit reused stale bytecode)
- research T-1441-review: Verdict: changes needed.** The main hole is that the "gitignored and identical to the checkout" rule reads attacker-writable ignore rules. I read…
- research T-1459-review: Verdict:** changes needed (no HIGH findings; the first four MEDIUMs are real gaps). [stale: plugin/lib/fmplugins.py changed since it was written]
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- the similar finished task took 1 steps
- start here (files T-0876 touched): plugin/tests/test_cli.py, plugin/lib/fmcore.py
- likely tests for the scope: plugin/tests/test_doctor.py
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
