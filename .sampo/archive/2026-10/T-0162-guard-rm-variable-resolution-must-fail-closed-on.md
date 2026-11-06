---
id: T-0162
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-03T07:47:39Z
updated: 2026-10-03T07:51:12Z
base: 410af46067757274d19fad8bad914b741ce7d710
base_tree: 31bf7e876ce578e6e51c5592e26c9a94c6d7f2b0
verified: strong
---
# Guard: rm variable resolution stops at a computed command name
## Raw request
> Guard: rm variable resolution must fail closed on a computed command name ($X or a backtick command in command position can be read/declare and set a variable): automated security review of T-0161
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A command named by $X, a backtick command or a glob that bash runs as read is blocked — verify with `python3 -m unittest plugin/tests/test_guard_diff.py`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: the three forms in the differential test
2. [x] Fail closed on a computed command name in _track_vars
3. [x] CHANGELOG line
## Resume here
## Docs impact
CHANGELOG and the MASTER resolver sentence.
## Verification evidence
- (step 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.890s / OK [ran] [tree 6ab7d40009c9] (2026-10-03T07:51:09Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 46 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree 6ab7d40009c9] (2026-10-03T07:51:11Z)
- (step 3) `grep -q T-0162 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 6ab7d40009c9] (2026-10-03T07:51:11Z)
- (ac 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.895s / OK [ran] [tree 6ab7d40009c9] (2026-10-03T07:51:12Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 07:51 UTC); cached (fm check --fresh reruns) [ran] [tree 6ab7d40009c9] (2026-10-03T07:51:12Z)
- (audit adversary) `self: the red run showed all three forms deleting home in real bash; the fix stops resolving whenever the command word holds $, a backtick or a glob character, so any name bash computes is unknown; guard and differential tests green, gates pass` → other ways to compute a name were checked: $(…) and ${…} are already not straight-line, brace expansion uses { (not straight-line), an alias needs the alias builtin (stops resolving), a quoted or escaped builtin name unquotes to the builtin (stops) [tree 6ab7d40009c9] (2026-10-03T07:51:12Z)
- (audit self) `self: the red run showed all three forms deleting home in real bash; the fix stops resolving whenever the command word holds $, a backtick or a glob character, so any name bash computes is unknown; guard and differential tests green, gates pass` → no findings [tree 6ab7d40009c9] (2026-10-03T07:51:12Z)
## Log
- 2026-10-03T07:47:39Z created
- 2026-10-03T07:50:02Z planned from capture
- 2026-10-03T07:50:02Z focused
- 2026-10-03T07:51:11Z scope: MASTER resolver sentence names computed command names
- 2026-10-03T07:51:12Z done
- 2026-10-03T07:51:12Z committed c9397da (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0161 [SECURITY M, done, 3 steps] Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151) — lesson: Fail-closed mean…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0158 [SECURITY M, done, 3 steps] Guard: one quote-aware reader for command substitutions (nested, quoted, backticks) — lesson: Patch a text scanner one bypass at a tim…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Every place the resolver reads a command word, ask what bash would compute from it first: expansion and globbing come before builtin lookup.
## Files touched
- plugin/tests/test_guard_diff.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
