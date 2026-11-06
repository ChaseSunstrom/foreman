---
id: T-0161
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-03T07:30:21Z
updated: 2026-10-03T07:40:33Z
base: d1c942dbf460612a652fdb8727ef479d2ea5aaa4
base_tree: e4b8de5b16a0f93f1990c3a47d860355ab327a34
verified: strong
---
# Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151)
## Raw request
> Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151)
## Interpretation
The automated review found T-0151's resolver keeps a variable's earlier literal when bash changes it another way (array or append assignment, export/declare behind command or builtin, a keyword before an assignment, cd setting PWD, $_, a DEBUG trap, word splitting, prefix assignments that persist). Every such case must leave the variable unresolved, which blocks as before T-0151.
## Assumptions (confidence)
## Acceptance criteria
- [x] Every new EXTRA case in the differential test (run by real bash) is blocked — verify with `python3 -m unittest plugin/tests/test_guard_diff.py`
- [x] The resolved safe forms from T-0151 still pass — verify with `python3 plugin/tests/run.py -k test_guard`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) add each missed builtin and form to _SETS_VARS one by one; (b) model what can change a variable: only shell builtins and keywords can, so stop resolving at any builtin outside a small inert list, treat any non-plain assignment word or prefix assignment as unknown, never resolve names bash sets itself (_, PWD, OLDPWD, DIRSTACK, BASH*), stop at IFS, and drop values with whitespace. Choice: (b), because the builtin list is finite and an allowlist fails closed on forms nobody thought of; (a) is the blacklist that just missed six.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: add the bypass forms to the differential test's EXTRA list
2. [x] Allowlist the resolver in check_bash
3. [x] Docs: CHANGELOG and the MASTER guard-limits paragraph
## Resume here
## Docs impact
MASTER guard-limits paragraph (how rm variables are resolved, comments) and CHANGELOG.
## Verification evidence
- (ac 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.878s / OK [ran] [tree 57bf178d0315] (2026-10-03T07:39:52Z)
- (ac 2) `python3 plugin/tests/run.py test_guard` → ✗ exit 2 · usage: run.py [-h] [-j J] [-k K] [-p P] / run.py: error: unrecognized arguments: test_guard [ran] [tree 57bf178d0315] (2026-10-03T07:39:52Z)
- (step 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.884s / OK [ran] [tree 57bf178d0315] (2026-10-03T07:39:53Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff` → ✗ exit 2 · usage: run.py [-h] [-j J] [-k K] [-p P] / run.py: error: unrecognized arguments: test_guard test_guard_diff [ran] [tree 57bf178d0315] (2026-10-03T07:39:54Z)
- (step 3) `grep -q 'T-0161' CHANGELOG.md && grep -q 'read as written' MASTER.md` → exit 0 · (no output) [ran] [tree 57bf178d0315] (2026-10-03T07:39:54Z)
- (ac 2) `python3 plugin/tests/run.py -k Guard` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 57bf178d0315] (2026-10-03T07:39:57Z)
- (step 2) `python3 plugin/tests/run.py -k Guard` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 57bf178d0315] (2026-10-03T07:39:58Z)
- (ac 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 46 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 57bf178d0315] (2026-10-03T07:40:04Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 46 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree 57bf178d0315] (2026-10-03T07:40:05Z)
- (ac 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.892s / OK [ran] [tree 57bf178d0315] (2026-10-03T07:40:16Z)
- (ac 2) `python3 -m unittest plugin/tests/test_guard.py` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 57bf178d0315] (2026-10-03T07:40:16Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 07:39 UTC); cached (fm check --fresh reruns) [ran] [tree 57bf178d0315] (2026-10-03T07:40:16Z)
- (ac 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 46 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree 57bf178d0315] (2026-10-03T07:40:33Z)
- (audit intent) `One fm-reviewer pass (intent + adversary) over the first fix found 5 more: command/builtin-prefixed and quoted NAME= words, readonly, bash-set names beyond _ and PWD, and a mid-word # cutting the line in shlex. Each was confirmed in real bash via the differential test (red), fixed, and is now green there; gates pass.` → the fail-closed claim now holds for all 31 variable forms and both # forms run through real bash; the docs say what the resolver does (reads words as written, inert-builtin allowlist, bash-set names never resolved) [tree 57bf178d0315] (2026-10-03T07:40:33Z)
- (audit adversary) `One fm-reviewer pass (intent + adversary) over the first fix found 5 more: command/builtin-prefixed and quoted NAME= words, readonly, bash-set names beyond _ and PWD, and a mid-word # cutting the line in shlex. Each was confirmed in real bash via the differential test (red), fixed, and is now green there; gates pass.` → 3 HIGH (command D=, quoted/escaped NAME=, readonly) and 2 MEDIUM (special names, mid-word #) from the review all fixed and covered in test_guard_diff; $'…' quoting turns both new readers off (fails closed) [tree 57bf178d0315] (2026-10-03T07:40:33Z)
## Log
- 2026-10-03T07:30:21Z created
- 2026-10-03T07:30:21Z focused
- 2026-10-03T07:40:26Z criterion 2's verify command corrected: run from the repo root, unittest can't import the tests' helpers; the runner can
- 2026-10-03T07:40:33Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0151 [FEATURE M, done, 1 steps] Guard: rm resolves $VAR set to a literal earlier in a straight-line command — lesson: Resolve state only where the shell's own control …
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0160 [SECURITY M, done, 3 steps] Guard differential test: real bash in a bubblewrap sandbox with logging stand-ins finds what check_bash misses — lesson: Test a text-b…
- research T-0120-review: Verdict
- similar finished tasks took 1–3 steps
- start here (files T-0151 touched): plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard_diff.py
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Fail-closed means an allowlist over what the shell can do (builtins, unquoted words), not a list of the forms you thought of; and run every reviewer candidate through real bash, since the review's own fifth finding (shlex mid-word #) was older and worse than the change under review.
## Files touched
- plugin/tests/test_guard_diff.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
