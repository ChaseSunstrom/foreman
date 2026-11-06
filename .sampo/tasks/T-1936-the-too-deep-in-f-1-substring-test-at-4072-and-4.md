---
id: T-1936
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T08:11:02Z
updated: 2026-10-29T08:22:45Z
base: 914eef1b8faf2b75b9e97faba5624c04b232e307
base_tree: b315a806e29e5a70e459b3c028d88b78f80366f7
plan0_at: 2026-10-29T08:21:07Z
plan0_scope: []
verified: strong
---
# The `"too deep" in f[1]` substring test at 4072 and 4080 also matches `("rm-outside", "com
## Raw request
> The `"too deep" in f[1]` substring test at 4072 and 4080 also matches `("rm-outside", "command nesting too deep to analyse…")`. That is the finding the new code replaces. Any future "too deep" wordin…
> (noticed by an agent; research T-1931-review)
## Interpretation
In a script the guard reads, any finding whose text holds 'too deep' (a folder named so) is taken as the nesting cap and dropped; match the cap's exact refusal instead.
## Assumptions (confidence)
## Acceptance criteria
- [x] A script removing a folder named 'too deep' outside the tree is refused — verify with `python3 plugin/tests/run.py test_guard_exec_vectors -k too_deep`
## Non-goals
## Approach (options → choice → why)
Compare against the one nesting refusal string (already in UNANALYSED) by a named constant. Rejected: a category tag on findings (wider change for one string).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then exact match
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard_exec_vectors -k too_deep 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)"` → ✗ exit 1 · Ran 45 tests in 1.6s (8 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / FAILED (1 classes) [ran] [tree 6420fe0276ed] (2026-10-29T08:21:16Z)
- `python3 plugin/tests/run.py test_guard_exec_vectors -k too_deep` → ✗ exit 1 · Ran 45 tests in 3.7s (8 classes, 16 at a time; slowest: ScriptCache 2s, ScriptHook 1s, Review 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2a254742bc91] (2026-10-29T08:21:52Z)
- `python3 plugin/tests/run.py test_guard_exec_vectors -k too_deep` → exit 0 · Ran 45 tests in 1.6s (8 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 2a254742bc91] (2026-10-29T08:21:52Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors` → exit 0 · Ran 301 tests in 11.5s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 7s) / OK [ran] [tree 87f4530dba61] (2026-10-29T08:22:24Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_exec_vectors -k too_deep` → exit 0 · Ran 45 tests in 1.6s (8 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 87f4530dba61] (2026-10-29T08:22:32Z)
- (audit edge) `One-line change to an exact string compare; red-green proved; guard suites 301 OK; 124 replay cases, 0 drifted` → a nested script that really hits the nesting cap still gets the chain refusal; the T-1931 deep-script test passes [tree 87f4530dba61] (2026-10-29T08:22:32Z)
- (audit adversary) `One-line change to an exact string compare; red-green proved; guard suites 301 OK; 124 replay cases, 0 drifted` → the change only keeps more findings, never fewer, so nothing refused before is now allowed [tree 87f4530dba61] (2026-10-29T08:22:32Z)
- (audit self) `One-line change to an exact string compare; red-green proved; guard suites 301 OK; 124 replay cases, 0 drifted` → no findings [tree 87f4530dba61] (2026-10-29T08:22:32Z)
## Log
- 2026-10-29T08:11:02Z created
- 2026-10-29T08:21:04Z set tier=S, type=FIX
- 2026-10-29T08:21:06Z planned: it has criteria and steps
- 2026-10-29T08:21:07Z focused
- 2026-10-29T08:22:43Z done
- 2026-10-29T08:22:45Z committed 775098ad (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- T-1929 [SECURITY M, done, 1 steps] Guard refusals for lines too tangled to analyse are never lifted by a grant — lesson: Match refusal kinds on exact strings, never subs…
- research T-1931-review: Changes needed. One HIGH: a script that runs a second script drops the new finding before it reaches the caller. [stale: plugin/lib/fmguard.py, p…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
## Why not caught
The T-1931 tests only used real nesting, never a finding that merely mentions the words
## Lessons
- Match guard refusals by their exact text or a constant, never a substring of free text that can hold user paths
## Files touched
- plugin/tests/test_guard_exec_vectors.py
- plugin/lib/fmguard.py
- CHANGELOG.md
