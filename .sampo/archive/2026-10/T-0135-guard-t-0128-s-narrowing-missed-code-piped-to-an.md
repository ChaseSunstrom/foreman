---
id: T-0135
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T05:25:17Z
updated: 2026-10-03T05:26:36Z
base: 9a25f5019f8182786755105f7bb8f29ea87a4507
base_tree: b10f4fd1c7ff892a0335521ab56530c01fb3e9ac
verified: strong
---
# Guard: T-0128's narrowing missed code piped to an interpreter beside a heredoc; scan all but fm --run args
## Raw request
> Guard: T-0128's narrowing missed code piped to an interpreter beside a heredoc; scan all but fm --run args
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] piped code beside a heredoc and python -c inside fm --run stay blocked; the T-0128 false positive stays fixed — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, narrow by removing only fm --run args, check nested runs too
## Resume here
## Docs impact
CHANGELOG.md: covered by the T-0128 entry (scan minus fm --run)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → ✗ exit 1 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Publish 0s, Remote 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1925c3b9dc4a] (2026-10-03T05:25:40Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → ✗ exit 1 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Publish 0s, PluginChanges 0s) / FAILED (1 classes) [ran] [tree 1925c3b9dc4a] (2026-10-03T05:25:40Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → ✗ exit 1 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Publish 0s, PluginChanges 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f15251950f5c] (2026-10-03T05:25:50Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Authorization 0s, PluginChanges 0s) / OK [ran] [tree f15251950f5c] (2026-10-03T05:25:50Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.3    31.7     150  [0] / SessionEnd                  28.1    29.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.78s]; python3 plugin/tests/run.py → exit 0 · Ran 540 tests in 18.0s (1 [ran] [tree f15251950f5c] (2026-10-03T05:26:36Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Remote 0s) / OK [ran] [tree f15251950f5c] (2026-10-03T05:26:36Z)
- (audit adversary) `self: scan is the whole command minus fm --run spans, which check_bash now reads with the interpreter check at every depth` → piped code beside a heredoc, python -c inside fm --run, $CODE, heredoc and -c routes all blocked (tested); interpreter names before ; & | ) now recognised; the T-0128 false positive (backticks in a heredoc + shell --run 'claude plugin test') stays fixed [tree f15251950f5c] (2026-10-03T05:26:36Z)
- (audit self) `self: scan is the whole command minus fm --run spans, which check_bash now reads with the interpreter check at every depth` → no findings [tree f15251950f5c] (2026-10-03T05:26:36Z)
## Log
- 2026-10-03T05:25:17Z created
- 2026-10-03T05:25:17Z focused
- 2026-10-03T05:26:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0016-adversary-recheck: n## Findings\n\n**CRITICAL — `claude --settings` / `claude --mcp-config` flags entirely unclassified** — `plugin/lib/fmguard.py:656-670…
- T-0128 [FIX S, done, 1 steps] Guard: interpreter check reads only the code the interpreter runs, not the whole shell command
- research t0018-r1-maintainer: "fm: {e.args[0] if e.args else e}\"` — for a `KeyError('intent')` that prints exactly `fm: intent`, which reads like a value, not an error,…
- research t0018-final-adversary: HIGH** — `plugin/lib/fmguard.py:201-222` (`classify_tree` / `_new_context_file` / `_protected_roots`) — Tree-write commands (`cp -r`, `ta…
- the similar finished task took 1 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
