---
id: T-1458
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T14:02:55Z
updated: 2026-10-22T14:51:03Z
base: 9a94ae65b5c6ec252d344a563dde5b55df0ea07b
base_tree: 455c1d1060b1953dd04cd6eff28da4040f434e52
plan0_at: 2026-10-22T14:46:47Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard reads a quoted name after a provable cd where python runs
## Raw request
> Guard resolves a relative path in a Bash command against the project root even after a leading 'cd DIR &&': 'cd <scratchpad> && python3 - <<EOF ... open("t1456-test.edit","w")' was refused as writing ~/.claude/foreman/t1456-test.edit (brief: written-from-interpreter-code), a false block; follow a leading literal cd (as the shell would) before resolving written paths
## Interpretation
When python's open() target isn't a literal (p = 'x'; open(p,'w')), the guard falls back to every quoted string in the command, resolved against ctx.cwd only, so 'cd <scratchpad> && python3 - <<EOF' writing a relative name was refused as a project write.
## Assumptions (confidence)
## Acceptance criteria
- [x] a relative name after cd <scratch> && python - <<EOF passes; without the cd, with a ; cd, or with another cd line it is still refused — verify with `cd plugin/tests && python3 -m unittest test_guard.InterpreterCd`
## Non-goals
## Approach (options → choice → why)
In that fallback, resolve against _chain_dir (the one folder every python unit provably runs in after cd DIR && links) when it's certain, else ctx.cwd as before. No other path changes; an uncertain cd keeps the project in play.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] chain dir in the quoted-name fallback
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterCd` → ✗ exit 1 · Ran 1 test in 0.052s / FAILED (errors=1) [ran] [tree 5ce3cf69537a] (2026-10-22T14:46:49Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterCd` → ✗ exit 1 · Ran 1 test in 0.080s / FAILED (failures=2) [ran] [tree 049705af001b] (2026-10-22T14:48:12Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.InterpreterCd` → exit 0 · Ran 1 test in 0.131s / OK [ran] [tree 925835fe4e32] (2026-10-22T14:49:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterCd` → exit 0 · Ran 1 test in 0.043s / OK [ran] [tree 67da385a2aba] (2026-10-22T14:49:21Z)
- (audit adversary) `self + adversary: _python_units now also returns the rest-lines before the last fed starter (lead); _chain_dir judges only those, and the non-literal open() fallback resolves quoted names against that proven dir. Tested both a variable and a literal open(): plain and trailing-line forms pass; bare, cd-after, a moving line before, and a second python after cd back into the repo stay refused; all 10 guard suites (195 tests) green incl. test_guard_diff's real-bash forms.` → trailing lines run after python (the starter forbids & and pipes), so they can't change its cwd; every line before the last starter still goes through _chain_dir's strict check; CDPATH/cd - still refused [tree 67da385a2aba] (2026-10-22T14:49:21Z)
- (audit edge) `self + adversary: _python_units now also returns the rest-lines before the last fed starter (lead); _chain_dir judges only those, and the non-literal open() fallback resolves quoted names against that proven dir. Tested both a variable and a literal open(): plain and trailing-line forms pass; bare, cd-after, a moving line before, and a second python after cd back into the repo stay refused; all 10 guard suites (195 tests) green incl. test_guard_diff's real-bash forms.` → two python units need the same proven dir (_chain_dir), else ctx.cwd as before [tree 67da385a2aba] (2026-10-22T14:49:21Z)
- (audit self) `self + adversary: _python_units now also returns the rest-lines before the last fed starter (lead); _chain_dir judges only those, and the non-literal open() fallback resolves quoted names against that proven dir. Tested both a variable and a literal open(): plain and trailing-line forms pass; bare, cd-after, a moving line before, and a second python after cd back into the repo stay refused; all 10 guard suites (195 tests) green incl. test_guard_diff's real-bash forms.` → no findings [tree 67da385a2aba] (2026-10-22T14:49:21Z)
## Log
- 2026-10-22T14:02:55Z created
- 2026-10-22T14:24:12Z planned from capture
- 2026-10-22T14:46:46Z focused
- 2026-10-22T14:51:02Z done
- 2026-10-22T14:51:03Z committed a4455a05 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–6 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
