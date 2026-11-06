---
id: T-0158
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T07:06:05Z
updated: 2026-10-03T07:15:29Z
base: 6279376f54077b877672ad64ae3f43aa00f5fd56
base_tree: 2c5cb9a1aa2f406e962d44850e003b7596939495
verified: ok
---
# Guard: one quote-aware reader for command substitutions (nested, quoted, backticks)
## Raw request
> Guard: one shared quote-aware scanner for substitutions — the dollar-paren reader (_SUBST) misses nested parentheses inside double quotes, and _top_level, _backtick_bodies and _mask_fm each scan quotes their own way; three review rounds found edge cases (dollar-single-quote, double-quoted backticks); consolidate into one tested scanner that returns every substitution body with nesting
## Interpretation
Three review rounds found substitution edge cases one at a time. The dollar-paren reader is a token regex without nesting, so a substitution with parentheses inside double quotes goes unread; backticks have their own scanner. One reader, used everywhere check_bash recurses, removes the class.
## Assumptions (confidence)
## Acceptance criteria
- [x] nested and double-quoted substitutions with parentheses inside are read; single-quoted and escaped ones are not; arithmetic isn't a substitution; dollar-single-quote reads every span — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
A) a context-stack scanner: each $( opens a fresh quoting context, backticks inside any context, single quotes inert, escapes skipped, $(( arithmetic skipped; $'…' gives up and reads every span greedily. B) keep patching regexes: the class stays. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] _subst_bodies; check_bash recurses through it only
3. [x] gates, one reviewer pass (adversary)
## Resume here
## Docs impact
CHANGELOG; MASTER guard limits paragraph
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → 4 red: two nested/quoted substitutions unread, two never-running forms blocked (2026-10-03T07:09:14Z)
- (step 2) `test_guard.py + fm check` → guard OK; gates 5/5 (552 tests) (2026-10-03T07:09:14Z)
- (step 3) `fm check; reviewer (research T-0158-review) + 2 automated reviews; scratchpad t158_check.py` → gates 5/5; all 5 reviewer bypasses and both automated ones blocked, plus a comment bypass found while tracing (later lines after a # were never read); non-running forms pass; 8 substitutions 4 ms, not 'too deep' (2026-10-03T07:15:28Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: PluginChanges 0s, GitDestructive 0s, Publish 0s) / OK [ran] [tree 669eb98437fe] (2026-10-03T07:15:29Z)
- (audit intent) `one fm-reviewer adversary pass plus two automated reviews, each finding reproduced in t158_check.py before and after` → one reader now finds every substitution a shell runs; the class of edge cases the reviews kept finding is handled in one place, failing closed where bash syntax can't be followed [tree 669eb98437fe] (2026-10-03T07:15:29Z)
- (audit adversary) `one fm-reviewer adversary pass plus two automated reviews, each finding reproduced in t158_check.py before and after` → reviewer findings (dollar-single-quote fallback anchoring, unquoted heredoc bodies, case/comment early close, $(( subshell fallback, nested escaped backticks) and automated ones (fm blanking trusting any path named fm, comments) all reproduced and blocked; tracing found that a # comment hid every later line of a command (blocked now). Over-blocks accepted where they fail closed (a commented interpreter line next to fm, single-quoted text after dollar-single-quote) [tree 669eb98437fe] (2026-10-03T07:15:29Z)
- (audit edge) `one fm-reviewer adversary pass plus two automated reviews, each finding reproduced in t158_check.py before and after` → many substitutions in one command (tails don't spawn tails: 8 in 4 ms, not 'nesting too deep'), arithmetic $((1+2)) passes, quoted heredocs and single-quoted text aren't read, an unbalanced quote still splits commands in the fallback tokenizer [tree 669eb98437fe] (2026-10-03T07:15:29Z)
## Log
- 2026-10-03T07:06:05Z created
- 2026-10-03T07:07:34Z planned from capture
- 2026-10-03T07:07:34Z focused
- 2026-10-03T07:10:41Z steer: automated review (HIGH) — T-0153's fm blanking trusted any path ending in /fm; blank only the real Foreman fm (realpath), folded in here (same file)
- 2026-10-03T07:15:29Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0153 [SECURITY M, done, 1 steps] Guard: an fm command's own arguments are data, not interpreter code — lesson: Blanking text to avoid false positives is only safe wher…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- research T-0120-review: Verdict
- the similar finished task took 1 steps
- start here (files T-0153 touched): plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Patch a text scanner one bypass at a time and reviews keep finding the next; one reader with a fail-closed fallback ended the series
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmguard.py
