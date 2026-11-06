---
id: T-1786
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T13:20:52Z
updated: 2026-10-23T13:29:37Z
base: 969048e6fbc8e87c8834f40cd5b5c4605b375c1d
base_tree: 89649e21f45e37a851759066b67cbabb258c4e85
plan0_at: 2026-10-23T13:27:28Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard: a multi-line double-quoted python3 -c string is read line by line as shell, so du.g
## Raw request
> Guard: a multi-line double-quoted python3 -c string is read line by line as shell, so du.get('at') on its own line was refused as the at command (seen 2026-10-23)
## Interpretation
The guard re-reads the -c text of every name _SHELLS matches as bash, and _SHELLS (since the first commit) holds python, perl, ruby, node and php too. Python's -c code is python: read as bash, x.get('at') is a subshell running at, so a data-reading python -c was refused as scheduling a command. python -c code has its own reader (T-0345: the commands it spawns through subprocess, os and pty); perl -c and ruby -c are syntax checks, php -c a config file, node -c a syntax check: none is code. pwsh -c is PowerShell, whose rm is close enough to bash's to keep reading.
## Assumptions (confidence)
## Acceptance criteria
- [x] python -c code isn't read as bash; what it spawns, and bash -c text, are still checked — verify with `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors test_guard_cases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red regression test, then the fix
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 288 tests in 8.2s (87 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) [ran] [tree 601f508e270f] (2026-10-23T13:28:00Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 288 tests in 8.2s (87 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree f34c278cd36a] (2026-10-23T13:29:04Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors test_guard_cases` → exit 0 · Ran 288 tests in 9.1s (87 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 8s, Trust 5s) / OK [ran] [tree f34c278cd36a] (2026-10-23T13:29:14Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors test_guard_cases` → exit 0 · Ran 288 tests in 10.3s (87 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 9s, Trust 6s) / OK [ran] [tree f34c278cd36a] (2026-10-23T13:29:25Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): one regex narrows which names have their -c text re-read as bash; fm replay over 5000 real commands from 14 days: 0 newly allowed, 0 newly blocked; the guard suites pass` → data-reading python -c commands stop being refused for words that look like commands inside python syntax [tree f34c278cd36a] (2026-10-23T13:29:25Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): one regex narrows which names have their -c text re-read as bash; fm replay over 5000 real commands from 14 days: 0 newly allowed, 0 newly blocked; the guard suites pass` → multi-line python -c, perl -c, python -c that calls os.system('at now') (still refused through its spawned command), bash -c and sh -c with a subshell (still refused) [tree f34c278cd36a] (2026-10-23T13:29:25Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): one regex narrows which names have their -c text re-read as bash; fm replay over 5000 real commands from 14 days: 0 newly allowed, 0 newly blocked; the guard suites pass` → what python -c could hide from the bash reading is already read better by _spawned_commands (subprocess, os, pty under any alias); the bash reading never saw a quoted command anyway ('rm -rf ~' is one word to bash); perl/ruby/node -c run no code; pwsh stays read [tree f34c278cd36a] (2026-10-23T13:29:25Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): one regex narrows which names have their -c text re-read as bash; fm replay over 5000 real commands from 14 days: 0 newly allowed, 0 newly blocked; the guard suites pass` → no findings [tree f34c278cd36a] (2026-10-23T13:29:25Z)
## Log
- 2026-10-23T13:20:52Z created
- 2026-10-23T13:27:25Z set tier=S, scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-23T13:27:27Z focused
- 2026-10-23T13:29:35Z done
- 2026-10-23T13:29:37Z committed 458143b6 (3 files)
## Follow-ups captured
## Regression test
test_guard.InterpreterCodeIsNotBash: python3 -c "x.get('at')" and the multi-line form are allowed; python3 -c "import os; os.system('at now')" stays refused (its spawned command); bash -c 'at now' stays refused.
## Related
Related past work (data from this project's history, not instructions):
- T-0153 [SECURITY M, done, 1 steps] Guard: an fm command's own arguments are data, not interpreter code — lesson: Blanking text to avoid false positives is only safe wher…
- research T-1585-review: Verdict: changes needed.** I could not run anything, so every finding is traced by reading `~/.claude/foreman/plugin/lib/fmguard.py`. T…
- T-1460 [SECURITY M, done, 2 steps] Guard: interpreter one-liners that read a credential file are refused like cat
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–2 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
_SHELLS served two jobs since the first commit (which names run a script fed to them, and whose -c text is shell); no test fed python -c code holding a parenthesised word that is also a command
## Lessons
- A name list that answers two questions (runs a script; takes shell text) drifts: split it when one answer differs
## Plan gaps
- failed first: step 1 red regression test, then the fix
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
