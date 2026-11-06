---
id: T-1141
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T09:46:20Z
updated: 2026-10-16T10:02:35Z
base: b979918016350d4284844b981011411603306e95
base_tree: 99c37fe7c38b4f92bbd5fb874700bb7d487d8d7c
plan0_at: 2026-10-16T09:58:44Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard false positive: 'fm edit <<EOF … import fmcli … EOF' followed by '; python3 plugin/t
## Raw request
> Guard false positive: 'fm edit <<EOF … import fmcli … EOF' followed by '; python3 plugin/tests/run.py …' in the same command is refused as interpreter code driving Foreman's modules: the heredoc feeds fm edit (data), but any python3 in the command makes heredoc bodies count as python. A heredoc's reader should decide whether its body is code
## Interpretation
'fm edit <<EOF … import fmcli … EOF; python3 plugin/tests/run.py …' was refused as interpreter code driving Foreman's modules. Any python3 in the command made every heredoc body count as code, though this heredoc feeds fm edit (data: edit blocks it applies through the guard's own Edit check).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm edit's heredoc with import fmcli lines plus a python3 test run in one command is allowed; the same body fed to python3 - is still refused as core — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
In _drop_data_heredocs, a quoted-delimiter heredoc whose line starts 'fm edit' (no pipe or substitution on the line) is data, like cat and tee. The same body fed to python3 - stays code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then treat fm edit's heredoc as data
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k an_fm_edit_heredoc test_guard` → exit 0 · Ran 114 tests in 7.8s (49 classes, 16 at a time; slowest: GuardAgainstBash 8s, Hook 2s, Proxy 1s) / OK [ran] [tree 7066cadf32da] (2026-10-16T09:58:59Z)
- (step 1) `python3 plugin/tests/run.py -k an_fm_edit_heredoc test_guard` → ✗ exit 1 · Ran 114 tests in 15.2s (49 classes, 16 at a time; slowest: GuardAgainstBash 15s, Hook 4s, PluginChanges 1s) / FAILED (1 classes) [ran] [tree 30c889832034] (2026-10-16T09:59:32Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_batch_edit` → ✗ exit 1 · Ran 137 tests in 17.5s (53 classes, 16 at a time; slowest: GuardAgainstBash 17s, BatchEdit 17s, Sub 5s) / FAILED (1 classes) [ran] [tree 263b448e9d65] (2026-10-16T09:59:57Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_batch_edit test_guard_diff` → ✗ exit 1 · Ran 137 tests in 18.7s (53 classes, 16 at a time; slowest: BatchEdit 18s, GuardAgainstBash 18s, Sub 6s) / FAILED (1 classes) [ran] [tree 159c9f638f79] (2026-10-16T10:00:26Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_batch_edit test_guard_diff` → ✗ exit 1 · Ran 137 tests in 8.1s (53 classes, 16 at a time; slowest: BatchEdit 8s, GuardAgainstBash 5s, Sub 2s) / FAILED (1 classes) [ran] [tree 2733ddf0fd59] (2026-10-16T10:01:14Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_batch_edit test_guard_diff` → exit 0 · Ran 137 tests in 7.7s (53 classes, 16 at a time; slowest: BatchEdit 8s, GuardAgainstBash 5s, Sub 2s) / OK [ran] [tree 53d76e8efe9f] (2026-10-16T10:01:31Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 114 tests in 5.6s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 53d76e8efe9f] (2026-10-16T10:01:51Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 114 tests in 4.9s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / OK [ran] [tree 53d76e8efe9f] (2026-10-16T10:01:51Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 114 tests in 5.0s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / OK [ran] [tree 8769fdbbea7f] (2026-10-16T10:01:56Z)
- (audit adversary) `self + adversary: reproduced through the real hook (refused only with a module call in the body and python3 elsewhere); fm edit never executes stdin, it applies edit blocks through the guard's own Edit check (T-1089), so its heredoc is data; the line must start with 'fm edit' and carry no pipe, ;, & or substitution, so 'fm edit <<EOF | python3' or '… ; python3 - <<' still count; the same body fed to python3 - stays refused (tested)` → a heredoc only becomes data when fm edit is the line's first command and nothing else on the line could read it [tree 8769fdbbea7f] (2026-10-16T10:01:56Z)
- (audit self) `self + adversary: reproduced through the real hook (refused only with a module call in the body and python3 elsewhere); fm edit never executes stdin, it applies edit blocks through the guard's own Edit check (T-1089), so its heredoc is data; the line must start with 'fm edit' and carry no pipe, ;, & or substitution, so 'fm edit <<EOF | python3' or '… ; python3 - <<' still count; the same body fed to python3 - stays refused (tested)` → no findings [tree 8769fdbbea7f] (2026-10-16T10:01:56Z)
## Log
- 2026-10-16T09:46:20Z created
- 2026-10-16T09:58:43Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-16T09:58:44Z focused
- 2026-10-16T10:01:51Z scope: CHANGELOG.md — release note
- 2026-10-16T10:02:34Z done
- 2026-10-16T10:02:35Z committed 828f1d3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 6 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Whether a heredoc body is code depends on its reader, not on what else the command runs
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
