---
id: T-0906
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:36:45Z
updated: 2026-10-15T18:38:42Z
base: 0911faadf923bcd812ac60cd7cf98a8b50f385a7
base_tree: 3c89bc44fa993cb6c4a007d31674d87e43f8e5db
verified: strong
---
# Guard: the mktemp-as-literal rewrite (T-0892) is skipped when the command sets TMPDIR or PATH or shadows mktemp
## Raw request
> Guard: the mktemp-as-literal rewrite (T-0892) is skipped when the command sets TMPDIR or PATH or shadows mktemp
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] export TMPDIR=$HOME; T=$(mktemp -d); rm -rf "$T/.." and a shadowed mktemp() are refused; T-0892's cases still pass — verify with `python3 plugin/tests/run.py -k KnownVars`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing cases in KnownVars, then skip the rewrite on TMPDIR=/PATH=/mktemp() /function mktemp/alias mktemp
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k KnownVars` → ✗ exit 1 · Ran 7 tests in 0.5s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fe3fca48b24d] (2026-10-15T18:37:23Z)
- `python3 plugin/tests/run.py -k KnownVars` → exit 0 · Ran 7 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree fe3fca48b24d] (2026-10-15T18:37:23Z)
- (step 1) `python3 plugin/tests/run.py -k 'KnownVars|RmOutside|PipeShell'` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree fe3fca48b24d] (2026-10-15T18:37:26Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 98 tests in 4.4s (40 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree fe3fca48b24d] (2026-10-15T18:37:46Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 98 tests in 4.4s (40 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree f82c07773852] (2026-10-15T18:38:17Z)
- (ac 1) `python3 plugin/tests/run.py -k KnownVars` → exit 0 · Ran 7 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 6d71610aae15] (2026-10-15T18:38:41Z)
- `python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 98 tests in 4.3s (40 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree 6d71610aae15] (2026-10-15T18:38:41Z)
- (audit adversary) `self + adversary: reviewer's PATH reproducer was a real bypass (mktemp in a PATH dir echoing /); probed further vectors as tests — hash -p was a second bypass, fixed; TMPDIR=, function/alias shadowing, source, eval were already refused (kept as regression cases); fm replay: 0 newly allowed` → PATH=, hash -p, enable, TMPDIR=, mktemp(), function/alias mktemp, source, eval+base64 all refused [tree 6d71610aae15] (2026-10-15T18:38:41Z)
- (audit edge) `self + adversary: reviewer's PATH reproducer was a real bypass (mktemp in a PATH dir echoing /); probed further vectors as tests — hash -p was a second bypass, fixed; TMPDIR=, function/alias shadowing, source, eval were already refused (kept as regression cases); fm replay: 0 newly allowed` → T-0892 scratch cases still pass (rm -r of a plain $(mktemp -d) folder allowed) [tree 6d71610aae15] (2026-10-15T18:38:41Z)
- (audit self) `self + adversary: reviewer's PATH reproducer was a real bypass (mktemp in a PATH dir echoing /); probed further vectors as tests — hash -p was a second bypass, fixed; TMPDIR=, function/alias shadowing, source, eval were already refused (kept as regression cases); fm replay: 0 newly allowed` → no findings [tree 6d71610aae15] (2026-10-15T18:38:41Z)
## Log
- 2026-10-15T18:36:45Z created
- 2026-10-15T18:36:45Z focused
- 2026-10-15T18:38:42Z done
- 2026-10-15T18:38:42Z committed 27b3d75 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0590 [SECURITY M, done, 2 steps] Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline — lesson: a text…
- T-0892 [FIX S, done, 1 steps] Guard: T=$(mktemp -d) resolves to a scratch folder, so a later rm -r $T isn't an unresolvable target
- T-0151 [FEATURE M, done, 1 steps] Guard: rm resolves $VAR set to a literal earlier in a straight-line command — lesson: Resolve state only where the shell's own control …
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar finished tasks took 1–2 steps
## Plan gaps
- failed first: step 1 failing cases in KnownVars, then skip the rewrite on TMPDIR=/PATH=/mktemp() /function mktemp/alias …
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
