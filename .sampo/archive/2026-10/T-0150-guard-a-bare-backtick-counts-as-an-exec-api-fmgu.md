---
id: T-0150
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:52:18Z
updated: 2026-10-03T06:56:12Z
base: 34bfa6cc1375e95c2349cfc198fdcb5c7746bc37
base_tree: 54c0c1b49b63dfbca19e6422dc41497eb99f6e50
verified: strong
---
# Guard: a backtick counts as code execution only where it executes, and a claude call inside backticks is caught there
## Raw request
> Guard: a bare backtick counts as an exec API (fmguard _EXEC_API), so a Python heredoc with markdown backticks next to a quoted 'claude plugin test' is blocked as plugin; backticks execute only in ruby/perl/php (and claude inside backticks there isn't matched at all) — RSI pass 1, 6 blocks
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] markdown backticks in a heredoc beside a quoted plugin-test command pass; backtick-run plugin installs are blocked; the system/subprocess/execSync forms stay blocked — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Authorization 0s) / OK [ran] [tree 83e42ab05026] (2026-10-03T06:56:12Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Authorization 0s) / OK [ran] [tree 83e42ab05026] (2026-10-03T06:56:12Z)
- (audit adversary) `self: two regex changes and one tokenizer change in fmguard; every earlier block case still blocks (guard suite green), the markdown heredoc passes, three new execution forms block` → removing the bare backtick from the exec list narrowed only the interpreter claude-check; backticks still count where they execute (ruby/perl/php), claude inside backticks is now matched, and tracing the change found shell backtick substitution unread — fixed (split like $( ), test rows); quoted substitutions were already caught by the raw-text check (scratchpad t150_check.py); a single-quoted literal still reads as a block (fails closed) [tree 83e42ab05026] (2026-10-03T06:56:12Z)
- (audit self) `self: two regex changes and one tokenizer change in fmguard; every earlier block case still blocks (guard suite green), the markdown heredoc passes, three new execution forms block` → no findings [tree 83e42ab05026] (2026-10-03T06:56:12Z)
## Log
- 2026-10-03T06:52:18Z created
- 2026-10-03T06:54:02Z planned from capture
- 2026-10-03T06:54:02Z focused
- 2026-10-03T06:56:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research T-0120-review: Verdict
- T-0144 [SECURITY L, done, 3 steps] Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid co…
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
