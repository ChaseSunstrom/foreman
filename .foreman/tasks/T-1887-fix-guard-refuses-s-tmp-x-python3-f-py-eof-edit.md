---
id: T-1887
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-29T00:55:38Z
updated: 2026-10-29T01:31:26Z
base: b50f1dfe1d8c073db1e925a09f540224a5823550
base_tree: c7718c6089a5970382cd408012aa33426ff1023a
plan0_at: 2026-10-29T01:16:03Z
plan0_scope: []
verified: strong
---
# Guard reads a quoted python heredoc after NAME=value; or && like a bare one
## Raw request
> FIX: guard refuses 'S=/tmp/x && python3 - f.py <<EOF' edit scripts: _python_units (fmguard.py:1683) accepts only lowercase name=value ; prefixes; allow [A-Za-z_]\w*= with ; or &&, denylisting PATH HOME LD_* PYTHON* CLAUDE* (friction 5x)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] S=/tmp/x && python3 - <<'EOF' with fm names only in strings is parsed, PATH/LD_*/PYTHON*/exported names and ||, & are not — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: uppercase or && prefix before a heredoc
2. [x] Widen _python_units' prefix with _PRE_DENY and the exported check
3. [x] CHANGELOG and MASTER
## Resume here
<!-- auto -->
- 2026-10-29T01:25:01Z step 2/3: Widen _python_units' prefix with _PRE_DENY and the exported check
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/route_diff.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1890t.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1890i.txt
- failures met: assertionerror: false is not true : x=0 &&
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.InterpreterWrites.test_an_uppercase_variable_or_and_chain_before_a_heredoc` → red as expected (exit 1) · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree 8752993c2b7a] (2026-10-29T01:16:10Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 290 tests in 18.5s (88 classes, 16 at a time; slowest: GuardAgainstBash 17s, Mutation 17s, Trust 9s) / OK [ran] [tree 42d38566758b] (2026-10-29T01:16:37Z)
- (step 3) `grep -c T-1887 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:1 [ran] [tree 42d38566758b] (2026-10-29T01:16:38Z)
- `python3 plugin/tests/run.py test_guard.InterpreterWrites.test_an_uppercase_variable_or_and_chain_before_a_heredoc` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 42d38566758b] (2026-10-29T01:16:41Z)
- `python3 plugin/tests/run.py test_guard.InterpreterWrites.test_an_uppercase_variable_or_and_chain_before_a_heredoc` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 42d38566758b] (2026-10-29T01:16:41Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4116 tests in 231.0s (987 classes, 16 at a time; slowest: Worker 129s, Stop 69s, Bench 58s) / FAILED (1 classes) [ran] [tree 42d38566758b] (2026-10-29T01:24:41Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 01:24 UTC; claude plugin test mods/foreman- [ran] [tree 56dd1e2ddcb0] (2026-10-29T01:30:51Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 290 tests in 8.1s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 56dd1e2ddcb0] (2026-10-29T01:31:14Z)
- (audit intent) `red/green test_guard InterpreterWrites + updated test_pass4 heredoc table; full gates green (4116 tests, replay 0 drifted)` → S=… && python3 - "$S/f" <<'EOF' with fm names only in strings is parsed, not text-matched [tree 56dd1e2ddcb0] (2026-10-29T01:31:14Z)
- (audit adversary) `red/green test_guard InterpreterWrites + updated test_pass4 heredoc table; full gates green (4116 tests, replay 0 drifted)` → PATH/HOME/IFS/LD_*/PYTHON*/CLAUDE*/FOREMAN* prefixes, an already-exported name, set -a, ||, &, $( all keep the old refusal [tree 56dd1e2ddcb0] (2026-10-29T01:31:14Z)
- (audit edge) `red/green test_guard InterpreterWrites + updated test_pass4 heredoc table; full gates green (4116 tests, replay 0 drifted)` → lowercase and mixed-case names; an old test expecting x=1 && to text-match moved to the parsed list [tree 56dd1e2ddcb0] (2026-10-29T01:31:14Z)
- (audit self) `red/green test_guard InterpreterWrites + updated test_pass4 heredoc table; full gates green (4116 tests, replay 0 drifted)` → no findings [tree 56dd1e2ddcb0] (2026-10-29T01:31:14Z)
## Log
- 2026-10-29T00:55:38Z created
- 2026-10-29T01:06:07Z planned from capture
- 2026-10-29T01:16:03Z focused
- 2026-10-29T01:26:38Z widened: test_pass4 asserted x=1 && keeps the text match; T-1887 parses it now, so the test moves it to the parsed list
- 2026-10-29T01:31:24Z done
- 2026-10-29T01:31:26Z committed 81deaa25 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1585-review: Verdict: changes needed.** I could not run anything, so every finding is traced by reading `~/.claude/foreman/plugin/lib/fmguard.py`. T…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-1585-rereview: Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- A guard widening can flip an older test's expectation: grep the tests for the prefix shape before the full run
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmguard.py
- plugin/tests/test_pass4.py
