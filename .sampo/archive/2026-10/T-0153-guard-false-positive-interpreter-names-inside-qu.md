---
id: T-0153
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:54:02Z
updated: 2026-10-03T07:06:53Z
base: f957228c4162fb9d7ab54ef85557e2bdc3e054d4
base_tree: 6920922e566ea0c32a6f6ed16920339037c88a41
verified: strong
---
# Guard: an fm command's own arguments are data, not interpreter code
## Raw request
> Guard false positive: interpreter names inside quoted fm arguments (an AC text mentioning ruby, perl, node, subprocess next to a quoted claude plugin command) make fm task new read as interpreter code running claude; detect interpreters by command position (tokens), not anywhere in the text — hit live while filing T-0150
## Interpretation
Live: filing T-0150 was blocked because its criterion text named interpreters next to a quoted plugin-test command; the interpreter check reads interpreter names anywhere in the text. fm's arguments never run, except --run values (checked on their own) and substitutions (read recursively).
## Assumptions (confidence)
## Acceptance criteria
- [x] an fm command whose text names interpreters beside a quoted plugin command passes; a substitution inside fm's arguments, or an interpreter chained before or after fm, still blocks — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
A) blank the arguments of top-level fm commands (segments split at unquoted separators) before the interpreter gate, giving up where the quote scan can't follow; B) detect interpreters only by command position: misses find -exec, parallel and other runners (fails open). Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, RmOutside 0s) / OK [ran] [tree 2c5cb9a1aa2f] (2026-10-03T07:06:53Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, RmOutside 0s) / OK [ran] [tree 2c5cb9a1aa2f] (2026-10-03T07:06:53Z)
- (audit intent) `self-review with the guard suite` → the live false block (an fm task's criterion naming interpreters beside a quoted plugin-test command) now passes; fm stays the only thing blanked, and only at top level [tree 2c5cb9a1aa2f] (2026-10-03T07:06:53Z)
- (audit adversary) `self-review with the guard suite` → blanking applies only to a segment whose command word is fm (after wrappers) with no substitution inside; an interpreter chained before or after fm still blocks (tests), a substitution in fm's arguments keeps the segment (test caught the nested-paren miss before it shipped), dollar-single-quote or an unknown heredoc form blanks nothing, heredoc bodies are always read; fm's --run values are checked recursively as before. Wider scanner work captured (T-0158) [tree 2c5cb9a1aa2f] (2026-10-03T07:06:53Z)
## Log
- 2026-10-03T06:54:02Z created
- 2026-10-03T07:05:36Z planned from capture
- 2026-10-03T07:05:36Z focused
- 2026-10-03T07:06:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0120-review: Verdict
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- T-0150 [SECURITY S, done, 1 steps] Guard: a backtick counts as code execution only where it executes, and a claude call inside backticks is caught there
- the similar finished task took 1 steps
- start here (files T-0150 touched): plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Blanking text to avoid false positives is only safe where every way that text can execute is read some other way; check each reader's limits (nested parens) first
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
