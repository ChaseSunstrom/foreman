---
id: T-0163
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-03T07:56:08Z
updated: 2026-10-03T07:58:58Z
base: 5afeacba460093c246bb112744c76f0507b7567a
base_tree: dabcd62aa99b04bcac7638fa92ada3c14ef3dc95
verified: strong
---
# Guard: a # right after a closing ) is mid-word, not a comment
## Raw request
> Guard: a # right after a closing ) ($(true)#x, $((1))#x) is mid-word in bash, but _strip_comments cut the line there, hiding what follows (automated security review of T-0161)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] $(true)#x and $((1))#x before a dangerous call are blocked — verify with `python3 -m unittest plugin/tests/test_guard_diff.py`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: the forms in the differential test
2. [x] A ) no longer starts a comment in _strip_comments
3. [x] CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.
## Verification evidence
- (step 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.986s / OK [ran] [tree e12e4fdfb9c9] (2026-10-03T07:58:50Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 46 tests in 1.1s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree e12e4fdfb9c9] (2026-10-03T07:58:51Z)
- (step 3) `grep -q T-0163 CHANGELOG.md` → exit 0 · (no output) [ran] [tree e12e4fdfb9c9] (2026-10-03T07:58:51Z)
- (ac 1) `python3 -m unittest plugin/tests/test_guard_diff.py` → exit 0 · Ran 1 test in 0.963s / OK [ran] [tree e12e4fdfb9c9] (2026-10-03T07:58:58Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 07:58 UTC); cached (fm check --fresh reruns) [ran] [tree e12e4fdfb9c9] (2026-10-03T07:58:58Z)
- (audit adversary) `self: red run showed $(true)#x and $((1))#x hiding all three payloads in real bash; a ) no longer counts as a word start for #, so those stay visible; a subshell's (true)#x now over-checks (bash reads a comment there), which fails closed; the substitution reader doesn't cut comments, so it had no twin` → other characters a substitution word can end in (a backtick, }) were never boundaries and are now in the differential test; $'…' still turns comment cutting off [tree e12e4fdfb9c9] (2026-10-03T07:58:58Z)
- (audit self) `self: red run showed $(true)#x and $((1))#x hiding all three payloads in real bash; a ) no longer counts as a word start for #, so those stay visible; a subshell's (true)#x now over-checks (bash reads a comment there), which fails closed; the substitution reader doesn't cut comments, so it had no twin` → no findings [tree e12e4fdfb9c9] (2026-10-03T07:58:58Z)
## Log
- 2026-10-03T07:56:08Z created
- 2026-10-03T07:57:36Z planned from capture
- 2026-10-03T07:57:36Z focused
- 2026-10-03T07:58:58Z done
- 2026-10-03T07:58:58Z committed 60a4d37 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0161 [SECURITY M, done, 3 steps] Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151) — lesson: Fail-closed mean…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- T-0162 [SECURITY S, done, 3 steps] Guard: rm variable resolution stops at a computed command name — lesson: Every place the resolver reads a command word, ask what bash …
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A character that closes a construct isn't a word boundary: list boundaries from the shell grammar (operators and blanks), not from what looks like punctuation.
## Files touched
- plugin/tests/test_guard_diff.py
- plugin/lib/fmguard.py
- CHANGELOG.md
