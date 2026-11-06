---
id: T-2634
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T19:18:28Z
updated: 2026-11-02T19:37:15Z
base: 50b857d472e87c1983b2784f578604c6a3b05991
base_tree: 6b01269123aa3a072845aa3c3ed02598ad3db439
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T19:35:42Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# The guard reads every argument on python's own heredoc line as a path candidate, quoted or not: python3 - ~/.claude/settings.json <<EOF with open(sys.argv[1], 'w') wrote a protected file unchecked
## Raw request
> the comment at fmguard.py:1756 wrongly says `sys.argv` is covered. An unquoted or `$S` argv path used by `open(sys.argv[n])` was already unscanned, a pre-existing hole. Glued `;>f`, `&&>f` and `|>f` …
> (noticed by an agent; research T-2629-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an unquoted protected path, ~ or $HOME path on the python - line is refused like a quoted one, and a plain relative argument writes where it resolves — verify with `python3 plugin/tests/run.py test_guard.FdAndLiterals`
- [x] the guard suites still pass — verify with `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the starter line's words as candidates
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / FAILED (1 classes: test_guard.FdAndLiterals) [ran] [tree e7cfc5a6f3c7] [world 2f1906870a] (2026-11-02T19:35:49Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine` → exit 0 · Ran 312 tests in 17.6s (91 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 12s, Trust 7s) / OK [ran] [tree 03e65ab9a74c] [world 2f1906870a] (2026-11-02T19:36:17Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 10.2s (24 classes, 16 at a time; slowest: Fences 10s, DocsProof 3s, TaskLifecycle 1s) / OK [ran] [tree 2447aa25eaca] [world 2f1906870a] (2026-11-02T19:36:37Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / OK [ran] [tree 2447aa25eaca] [world 2f1906870a] (2026-11-02T19:36:48Z)
- (ac 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine` → exit 0 · Ran 312 tests in 9.9s (91 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 2447aa25eaca] [world 2f1906870a] (2026-11-02T19:36:48Z)
- (step 1) `python3 plugin/tests/run.py test_guard.FdAndLiterals` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FdAndLiterals 0s) / OK [ran] [tree 2447aa25eaca] [world 2f1906870a] (2026-11-02T19:36:48Z)
- (audit adversary) `self (S, guard): the starter line's words join the candidates only (never remove one); shlex reads them as bash does, so quoted, unquoted, ~ and $VAR forms all reach classify_write; 312 guard tests pass` → python3 - <protected path> and python3 - ~/.claude/settings.json with open(sys.argv[1], 'w') are refused (pinned in FdAndLiterals); a quoted form still is [tree 2447aa25eaca] (2026-11-02T19:36:48Z)
- (audit edge) `self (S, guard): the starter line's words join the candidates only (never remove one); shlex reads them as bash does, so quoted, unquoted, ~ and $VAR forms all reach classify_write; 312 guard tests pass` → a relative argument resolves under the cwd as any write target does, so an edit script handing python its own file is read as writing it (accurate: it does) [tree 2447aa25eaca] (2026-11-02T19:36:48Z)
- (audit self) `self (S, guard): the starter line's words join the candidates only (never remove one); shlex reads them as bash does, so quoted, unquoted, ~ and $VAR forms all reach classify_write; 312 guard tests pass` → no findings [tree 2447aa25eaca] (2026-11-02T19:36:48Z)
## Log
- 2026-11-02T19:18:28Z created
- 2026-11-02T19:35:41Z planned from capture
- 2026-11-02T19:35:42Z focused
- 2026-11-02T19:35:42Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T19:37:12Z done
- 2026-11-02T19:37:15Z committed 410b2964 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2629-review: Verdict: changes needed.** The adversary lens found three plausible regressions, each by code reading only. I could not run anything, so check ea…
- T-2629 [FIX M, done, 3 steps] The guard reads a redirect's fd number as the fd, not a write target (cp a b 2>/dev/null was a write to ./2), and a parsed python heredoc's…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_guard.py
## Why not caught
the guard's interpreter rule scanned quoted spans only; no test passed a path to python - unquoted
## Lessons
- A write target can arrive through argv as well as through literals: every word python's own line hands it is a candidate, quoted or not
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
