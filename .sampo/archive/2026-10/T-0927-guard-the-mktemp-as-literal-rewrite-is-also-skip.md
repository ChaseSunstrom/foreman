---
id: T-0927
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:38:33Z
updated: 2026-10-15T19:39:31Z
base: bd9f1d0e60aa9d44fb4073d79ab78c6e6bf8811a
base_tree: 88e9cd426faaae2a966ea86e347f5a955952c015
verified: strong
---
# Guard: the mktemp-as-literal rewrite is also skipped for any mention of TMPDIR/PATH (TMPDIR[0]=, ${TMPDIR:=…}), BASH_ENV/ENV, --rcfile/--init-file and alias … mktemp= (round-7 review)
## Raw request
> Guard: the mktemp-as-literal rewrite is also skipped for any mention of TMPDIR/PATH (TMPDIR[0]=, ${TMPDIR:=…}), BASH_ENV/ENV, --rcfile/--init-file and alias … mktemp= (round-7 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the reviewer's reproducers are refused; T-0892/T-0906 cases still pass — verify with `python3 plugin/tests/run.py -p 'test_guard*.py'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing cases, then widen _MKTEMP_MOVED and cover the nested bash -c
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k KnownVars` → ✗ exit 1 · Ran 7 tests in 0.6s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 97d4e6e51400] (2026-10-15T19:39:26Z)
- `python3 plugin/tests/run.py -k KnownVars` → exit 0 · Ran 7 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 97d4e6e51400] (2026-10-15T19:39:26Z)
- (ac 1) `python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 98 tests in 4.4s (40 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree 97d4e6e51400] (2026-10-15T19:39:30Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_guard*.py'` → exit 0 · Ran 98 tests in 4.4s (40 classes, 16 at a time; slowest: GuardAgainstBash 4s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree 97d4e6e51400] (2026-10-15T19:39:30Z)
- (audit adversary) `self + adversary: the reviewer's four confirmed bypasses (TMPDIR[0]=, PATH[0]=, BASH_ENV=/ENV= before a nested shell) and the alias-with-options form are refused; the rewrite now skips any mention of TMPDIR, PATH, BASH_ENV or ENV, --rcfile/--init-file, and runs on the whole command only (a nested shell's text alone missed its caller's env); fm replay: 0 newly allowed` → ': ${TMPDIR:=~}', 'TMPDIR[0]=', 'PATH[0]=', 'BASH_ENV=f bash -c', 'ENV=f sh -c', 'alias -- mktemp=' all refused as rm-outside [tree 97d4e6e51400] (2026-10-15T19:39:30Z)
- (audit edge) `self + adversary: the reviewer's four confirmed bypasses (TMPDIR[0]=, PATH[0]=, BASH_ENV=/ENV= before a nested shell) and the alias-with-options form are refused; the rewrite now skips any mention of TMPDIR, PATH, BASH_ENV or ENV, --rcfile/--init-file, and runs on the whole command only (a nested shell's text alone missed its caller's env); fm replay: 0 newly allowed` → a nested bash -c with nothing moved still reads its fresh temp folder as scratch [tree 97d4e6e51400] (2026-10-15T19:39:30Z)
- (audit self) `self + adversary: the reviewer's four confirmed bypasses (TMPDIR[0]=, PATH[0]=, BASH_ENV=/ENV= before a nested shell) and the alias-with-options form are refused; the rewrite now skips any mention of TMPDIR, PATH, BASH_ENV or ENV, --rcfile/--init-file, and runs on the whole command only (a nested shell's text alone missed its caller's env); fm replay: 0 newly allowed` → no findings [tree 97d4e6e51400] (2026-10-15T19:39:30Z)
## Log
- 2026-10-15T19:38:33Z created
- 2026-10-15T19:38:33Z focused
- 2026-10-15T19:39:31Z done
- 2026-10-15T19:39:31Z committed ce4667a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0906 [SECURITY S, done, 1 steps] Guard: the mktemp-as-literal rewrite (T-0892) is skipped when the command sets TMPDIR or PATH or shadows mktemp
- T-0590 [SECURITY M, done, 2 steps] Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline — lesson: a text…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar finished tasks took 1–2 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
