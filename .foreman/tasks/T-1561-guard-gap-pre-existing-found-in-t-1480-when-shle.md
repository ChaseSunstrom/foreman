---
id: T-1561
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T17:48:20Z
updated: 2026-10-22T18:53:22Z
base: 7c0359e19cca57a334197c70ac6b1163ddeda222
base_tree: 3ab4e37df11747b8cc55ed8a59d11a857319f7c5
plan0_at: 2026-10-22T17:51:00Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard gap (pre-existing, found in T-1480): when shlex fails on nested quotes, _tokens' fal
## Raw request
> Guard gap (pre-existing, found in T-1480): when shlex fails on nested quotes, _tokens' fallback split keeps quote characters on words, so echo "$(echo 'a"b')" ; 'cat' ~/.ssh/id_ed25519 isn't read as cat. Strip quotes in the fallback the way bash would (or refuse unparseable lines that name a credential path), keeping the depth>0 debris logic intact
## Interpretation
When shlex can't parse a line (unbalanced quotes inside a substitution), _tokens' fallback splits on spaces and keeps quote characters on words, so a quoted command name after such a prefix isn't recognised and its classifiers never run. Make the fallback read words the way bash would, so the classifiers see them.
## Assumptions (confidence)
## Acceptance criteria
- [x] echo "$(echo 'a"b')" ; 'cat' ~/.ssh/id_ed25519 is refused like plain cat of the key; the depth>0 debris rules and every guard test still pass — verify with `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] strip quotes in _tokens' fallback as bash would (or refuse an unparseable line naming a credential path)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` → ✗ exit 1 · Ran 2 tests in 0.031s / FAILED (failures=5) [ran] [tree 175074f905d2] (2026-10-22T17:52:35Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff` → exit 0 · Ran 5 tests in 14.017s / OK [ran] [tree c0a7b8142260] (2026-10-22T17:57:18Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` → ✗ exit 1 · Ran 5 tests in 0.100s / FAILED (failures=13) [ran] [tree fa158d2560fa] (2026-10-22T18:06:02Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff test_guard_debris test_guard_pipes test_guard_evasions` → exit 0 · Ran 24 tests in 6.036s / OK [ran] [tree 16514ba149fc] (2026-10-22T18:09:55Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` → ✗ exit 1 · Ran 7 tests in 1.698s / FAILED (failures=5) [ran] [tree eb2d2d6811e1] (2026-10-22T18:22:42Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff test_guard_debris test_guard_pipes test_guard_evasions` → exit 0 · Ran 26 tests in 6.985s / OK [ran] [tree 2efdd5fbc80d] (2026-10-22T18:25:36Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` → ✗ exit 1 · Ran 8 tests in 0.114s / FAILED (failures=5) [ran] [tree 14dfe56f1a49] (2026-10-22T18:32:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff test_guard_debris test_guard_pipes test_guard_evasions test_guard_cases` → exit 0 · Ran 39 tests in 8.042s / OK [ran] [tree a843e5cdce10] (2026-10-22T18:33:58Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` → ✗ exit 1 · Ran 8 tests in 1.072s / FAILED (failures=1) [ran] [tree 276fd02eb695] (2026-10-22T18:48:08Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff test_guard_pipes test_guard_evasions test_guard_cases test_guard_debris` → exit 0 · Ran 155 tests in 40.117s / OK [ran] [tree 9b79aaa0832d] (2026-10-22T18:49:35Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff` → exit 0 · Ran 11 tests in 5.986s / OK [ran] [tree ea96435ddf04] (2026-10-22T18:51:55Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff test_guard_pipes test_guard_evasions test_guard_cases test_guard_debris` → exit 0 · Ran 158 tests in 30.990s / OK [ran] [tree ea96435ddf04] (2026-10-22T18:52:27Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.TokenFallback test_guard_diff` → exit 0 · Ran 11 tests in 10.544s / OK [ran] [tree 88cfd7673181] (2026-10-22T18:52:46Z)
- (audit intent) `fm-reviewer passes: first review (2 findings) fixed; adversary re-review found the nested-# comment cut (HIGH, plus a pre-existing balanced form) fixed in 844fc45d; second re-review found no bypass, one backtick lookbehind defect fixed in 0adaf856` → an unparseable line is read both word by word and quote-aware; quoted operators are data [tree 88cfd7673181] (2026-10-22T18:52:46Z)
- (audit adversary) `fm-reviewer passes: first review (2 findings) fixed; adversary re-review found the nested-# comment cut (HIGH, plus a pre-existing balanced form) fixed in 844fc45d; second re-review found no bypass, one backtick lookbehind defect fixed in 0adaf856` → echo "$(echo "a #")">~/.bashrc (one-liner and with a broken next line), redirects after a quote, ) or backtick, trailing backslash and open quotes all refuse; 200,000-case fuzz never makes the quote-aware reading raise [tree 88cfd7673181] (2026-10-22T18:52:46Z)
- (audit edge) `fm-reviewer passes: first review (2 findings) fixed; adversary re-review found the nested-# comment cut (HIGH, plus a pre-existing balanced form) fixed in 844fc45d; second re-review found no bypass, one backtick lookbehind defect fixed in 0adaf856` → awk '$1>4000' stays one word (debris rule); a 20,000-deep nest masks in linear time [tree 88cfd7673181] (2026-10-22T18:52:46Z)
- (audit maintainer) `fm-reviewer passes: first review (2 findings) fixed; adversary re-review found the nested-# comment cut (HIGH, plus a pre-existing balanced form) fixed in 844fc45d; second re-review found no bypass, one backtick lookbehind defect fixed in 0adaf856` → TokenFallback tests red first each round; 158 guard tests pass [tree 88cfd7673181] (2026-10-22T18:52:46Z)
- (audit self) `fm-reviewer passes: first review (2 findings) fixed; adversary re-review found the nested-# comment cut (HIGH, plus a pre-existing balanced form) fixed in 844fc45d; second re-review found no bypass, one backtick lookbehind defect fixed in 0adaf856` → no findings [tree 88cfd7673181] (2026-10-22T18:52:46Z)
## Log
- 2026-10-22T17:48:20Z created
- 2026-10-22T17:50:48Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-22T17:50:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1561.builder.md
- 2026-10-22T17:51:00Z focused
- 2026-10-22T18:22:42Z tried: `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` ×3 on step 1, failing the same way
- 2026-10-22T18:32:23Z tried: `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` ×4 on step 1, failing the same way
- 2026-10-22T18:48:08Z tried: `cd plugin/tests && python3 -m unittest test_guard.TokenFallback` ×5 on step 1, failing the same way
- 2026-10-22T18:51:36Z merged worktree-agent-a56b0b2048640bc2f (2 file(s))
- 2026-10-22T18:51:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a56b0b2048640bc2f
- 2026-10-22T18:51:40Z focused
- 2026-10-22T18:53:19Z done
- 2026-10-22T18:53:22Z committed 1fba8c8e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1480-review: Verdict: changes needed.** This was a read-only review: I could not run anything, so neither finding has been executed against the guard. Both co…
- T-1480 [SECURITY M, done, 4 steps] Guard gap: $'…' ANSI-C quoted command names and C=env; $C variable indirection get past th — lesson: A guard pre-pass must find struct…
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Why not caught
_strip_comments predated nested-quote tracking and no test put a # inside "$( "…" )"
## Lessons
- A comment scanner that tracks one quote level cuts code out of nested $( "…" ) strings: every scanner that decides what is text must track quoting per substitution context
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
