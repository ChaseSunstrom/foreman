---
id: T-1722
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:08:24Z
updated: 2026-10-23T03:22:55Z
base: 315297f86d5dd9fd0d5780f85727d60841fceb55
base_tree: dc2f7fc7878216251ae2c1321a6eded942a38778
plan0_at: 2026-10-23T03:14:10Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Check: fmsettings.in_claude_code() can be fooled by a model running script -qc 'env -u CLA
## Raw request
> Check: fmsettings.in_claude_code() can be fooled by a model running script -qc 'env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT fm settings set …' (a pty with the markers cleared); confirm the guard refuses that shell form (T-1570 _hides_claude through script -c) and add a test either way
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard refuses unsetting or overriding CLAUDECODE through script -c, sh -c, bash -c and similar wrappers — verify with `python3 plugin/tests/run.py test_guard.ClaudeEnv`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add wrapper rows to ClaudeEnv; fix the guard if any pass
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv 2>&1 | grep -E "^(FAIL|AssertionError|Ran|OK)|Expected|self-auth|cmd" | head -30` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: ClaudeEnv 1s) / FAILED (1 classes) [ran] [tree d81bd14fdc25] (2026-10-23T03:14:27Z)
- (step 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv test_guard.GuardAgainstBash` → ✗ exit 1 · run.py: no test matches test_guard.GuardAgainstBash [ran] [tree aea0444b1fc7] (2026-10-23T03:16:10Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: ClaudeEnv 1s) / OK [ran] [tree aea0444b1fc7] (2026-10-23T03:16:15Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 271 tests in 40.5s (78 classes, 16 at a time; slowest: Mutation 40s, GuardAgainstBash 33s, Trust 23s) / OK [ran] [tree aea0444b1fc7] (2026-10-23T03:17:06Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv 2>&1 | grep -E "^(FAIL|OK)|arg=" | head` → ✗ exit 1 · FAILED (failures=4) / FAILED (1 classes) [ran] [tree 56280092b390] (2026-10-23T03:21:10Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 271 tests in 12.2s (78 classes, 16 at a time; slowest: Mutation 12s, GuardAgainstBash 8s, Trust 6s) / OK [ran] [tree 3a7d2704443a] (2026-10-23T03:22:06Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ClaudeEnv 0s) / OK [ran] [tree 3a7d2704443a] (2026-10-23T03:22:07Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ClaudeEnv` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: ClaudeEnv 0s) / OK [ran] [tree 11b03248e412] (2026-10-23T03:22:21Z)
- (audit adversary) `self: read _hides_claude and _strip_wrappers end to end; the env scan stops at env's first non-option, non-assignment word so a command's own arguments (grep CLAUDECODE) aren't read; -u/-C/-S and long forms consume their value; probed script -qc, script --command, sh -c, bash -c, setsid, timeout, unbuffer [-p], chrt, taskset, stdbuf -o L and a brace form` → an unknown wrapper before env no longer hides env -u CLAUDECODE or env CLAUDECODE=; the remaining gap is interpreter code (python os.environ.pop), already noted as a ponytail ceiling, where fm's verbs that matter fail closed off a terminal (T-1572) [tree 11b03248e412] (2026-10-23T03:22:21Z)
- (audit edge) `self: read _hides_claude and _strip_wrappers end to end; the env scan stops at env's first non-option, non-assignment word so a command's own arguments (grep CLAUDECODE) aren't read; -u/-C/-S and long forms consume their value; probed script -qc, script --command, sh -c, bash -c, setsid, timeout, unbuffer [-p], chrt, taskset, stdbuf -o L and a brace form` → the word env as another command's argument (echo env -u CLAUDECODE) now refuses: fails closed, rare [tree 11b03248e412] (2026-10-23T03:22:21Z)
- (audit self) `self: read _hides_claude and _strip_wrappers end to end; the env scan stops at env's first non-option, non-assignment word so a command's own arguments (grep CLAUDECODE) aren't read; -u/-C/-S and long forms consume their value; probed script -qc, script --command, sh -c, bash -c, setsid, timeout, unbuffer [-p], chrt, taskset, stdbuf -o L and a brace form` → no findings [tree 11b03248e412] (2026-10-23T03:22:21Z)
## Log
- 2026-10-23T03:08:24Z created
- 2026-10-23T03:14:01Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-23T03:14:08Z focused
- 2026-10-23T03:22:52Z done
- 2026-10-23T03:22:55Z committed 438c6d0b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1574-review: Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I c…
- research T-1573-review: Verdict:** approve with nits. I found no way for a kept value to differ from the previewed one, or for the app to stay in the previewed look afte…
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
T-1570's table listed each wrapper by name, and env was only read when _strip_wrappers had reached it; no row put an unknown wrapper before env
## Lessons
- When a check depends on unwrapping a command, look for the dangerous word anywhere in it rather than only after the wrappers you know
## Plan gaps
- failed first: step 1 add wrapper rows to ClaudeEnv; fix the guard if any pass
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
