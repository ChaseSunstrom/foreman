---
id: T-0151
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:52:18Z
updated: 2026-10-03T07:24:55Z
base: a3e0216390d45a03a045e9188e0ee05fbcc152e1
base_tree: dc996a4de8187a0fd0cdc02b4c1a67bd101c4e22
verified: strong
---
# Guard: rm resolves $VAR set to a literal earlier in a straight-line command
## Raw request
> Guard: rm -rf "$D" is refused as unresolvable even when D=<literal scratch path> was set earlier in the same command; resolve leading VAR=literal assignments before the rm check (D=$HOME or unset still refused) — RSI pass 1
## Interpretation
RSI pass 1: 'rm -rf "$D"' is refused as unresolvable even when D=<scratch path> was set just before; Claude then rewrites commands, and 32 failed Bash calls in the digest started with S=/F=/D= assignments.
## Assumptions (confidence)
## Acceptance criteria
- [x] D=<project path>; rm -rf "$D/x" passes; D=~ or D=$HOME or unset or reassigned, and any conditional or subshell assignment, still block — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
A) remember VAR=literal from plain assignments (and export) in commands joined only by ; or newlines, substitute $VAR/${VAR} in rm targets; anything that can make an assignment conditional or local (&&, ||, |, &, subshells, groups, control keywords) or set variables otherwise (read, source, eval, declare…) disables it, so $VAR stays unknown and blocked. B) resolve variables everywhere: conditional assignments (false && D=/safe after D=/) would make rm -rf / look safe. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: PluginChanges 0s, GitDestructive 0s, Publish 0s) / OK [ran] [tree e4b8de5b16a0] (2026-10-03T07:24:48Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: PluginChanges 0s, GitDestructive 0s, Publish 0s) / OK [ran] [tree e4b8de5b16a0] (2026-10-03T07:24:48Z)
- (audit intent) `self-review plus the differential test's variable cases in real bash` → the pass-1 friction (rm on a variable set just before, refused, forcing rewrites) is gone for the straight-line form Claude actually writes [tree e4b8de5b16a0] (2026-10-03T07:24:48Z)
- (audit adversary) `self-review plus the differential test's variable cases in real bash` → resolution happens only when nothing can make an assignment conditional or local (pipes, &&, ||, &, subshells, groups, keywords disable it) and stops at any command that can set variables; prefix assignments aren't visible to their own arguments (test); values with $, backticks or globs aren't literals; tilde values expand to home and block. The differential test runs the conditional, subshell, reassigned and tilde variants in bash and finds the guard blocking each [tree e4b8de5b16a0] (2026-10-03T07:24:48Z)
- (audit intent) `self-review plus the differential test's variable cases in real bash` → the pass-1 friction (rm on a variable set just before, refused, forcing rewrites) is gone for the straight-line form Claude actually writes [tree e4b8de5b16a0] (2026-10-03T07:24:54Z)
- (audit adversary) `self-review plus the differential test's variable cases in real bash` → resolution happens only when nothing can make an assignment conditional or local (pipes, &&, ||, &, subshells, groups, keywords disable it) and stops at any command that can set variables; prefix assignments aren't visible to their own arguments (test); values with $, backticks or globs aren't literals; tilde values expand to home and block. The differential test runs the conditional, subshell, reassigned and tilde variants in bash and finds the guard blocking each [tree e4b8de5b16a0] (2026-10-03T07:24:54Z)
## Log
- 2026-10-03T06:52:18Z created
- 2026-10-03T07:23:14Z planned from capture
- 2026-10-03T07:23:14Z focused
- 2026-10-03T07:24:54Z scope: plugin/tests/test_guard_diff.py — the variable variants checked against real bash
- 2026-10-03T07:24:55Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0120-review: Verdict
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research t0036-adversary: Confirmed: `check()` returns `Block` only when the category isn't in `ctx.allow`. Since `plugin` is in `ctx.allow` (from the earlier grant), `b…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Resolve state only where the shell's own control flow can't change it; otherwise keep it unknown
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
