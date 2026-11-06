---
id: T-0178
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,plugin/tests/test_guard_diff.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T09:59:58Z
updated: 2026-10-03T18:54:49Z
base: 37d04caeda49e9ddda71dd3ba397c111aadabb5a
base_tree: a6f2e8cc9e94c6494ddfe553c340321a91daa610
verified: strong
---
# Guard: a heredoc starts only outside quotes — a quoted heredoc marker hid every later line from the guard
## Raw request
> Guard: text arguments to fm (--interpretation, --approach, capture text) that describe code are read as interpreter code; only --run is masked — evidence: T-0176's brief was blocked state-direct for quoting the friction's code
## Interpretation
Grounding T-0178 (fm text that quotes code read as interpreter code) found the cause and a bypass: the four heredoc scanners take any quoted heredoc marker for a start, so the lines after it become a body. In an fm command that hides its later arguments from masking; in any command it hides real commands — echo '<<EOF' on one line, then git push --force on the next, passes the guard.
## Assumptions (confidence)
## Acceptance criteria
- [x] a quoted heredoc marker hides nothing — verify with `python3 plugin/tests/run.py -k test_a_quoted_heredoc_marker_hides_nothing`
- [x] real bash agrees — verify with `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked`
## Non-goals
## Approach (options → choice → why)
A: one helper gives a line's heredoc starts only where the text before it (the command so far, bodies left out, comments stripped) is outside every quote; all four scanners use it. B (rejected): patch only _mask_fm's count check — leaves the bypass in check_bash. A heredoc inside a double-quoted command substitution is no longer taken as one, so its body is checked as shell: stricter only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] top-level heredoc starts in all four scanners
3. [x] gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: heredoc starts)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_quoted_heredoc_marker_hides_nothing` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree 5ad4a3ef1b22] (2026-10-03T18:53:18Z)
- (step 1) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / FAILED (1 classes) [ran] [tree 5ad4a3ef1b22] (2026-10-03T18:53:20Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_quoted_heredoc_marker_hides_nothing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 4dcad22f3f84] (2026-10-03T18:53:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 4dcad22f3f84] (2026-10-03T18:53:44Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.0    32.4     150  [0] / SessionEnd                  28.1    29.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 18:50 UTC; python3 plugin/tests/run.py → e [ran] [tree 4dcad22f3f84] (2026-10-03T18:54:38Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_quoted_heredoc_marker_hides_nothing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 1b87a1940b1f] (2026-10-03T18:54:48Z)
- (ac 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 1b87a1940b1f] (2026-10-03T18:54:48Z)
- (audit intent) `self-review: the change only removes heredoc starts the guard accepted, so nothing new can be hidden; the bash differential test runs the three quoted-marker forms; 603 tests` → the original friction (an fm brief quoting heredoc code, blocked as an interpreter write) is allowed, and the bypass it led to is closed [tree 1b87a1940b1f] (2026-10-03T18:54:48Z)
- (audit adversary) `self-review: the change only removes heredoc starts the guard accepted, so nothing new can be hidden; the bash differential test runs the three quoted-marker forms; 603 tests` → before, any '<<WORD' text started a heredoc and hid the lines after it (echo '<<EOF' then git push --force passed, confirmed in real bash); now a start needs the text before it outside every quote, comments stripped, across lines; the starts recognized are a subset of before, so a misread can only turn a real body into checked shell (stricter), never hide a line [tree 1b87a1940b1f] (2026-10-03T18:54:48Z)
## Log
- 2026-10-03T09:59:58Z created
- 2026-10-03T18:43:02Z RSI pass 3: _mask_fm returns the command unmasked on any '#' and when _heredocs takes a quoted <<'PY' for a heredoc start; replace the blanket '#' bail with a word-start unquoted comment test (_strip_comments) or accept heredoc starts only at top level
- 2026-10-03T18:52:54Z planned from capture
- 2026-10-03T18:52:54Z focused
- 2026-10-03T18:53:07Z the user, mid-task: 'keep super improving foreman, make it smarter, better, etc.' (standing; queue continues after this)
- 2026-10-03T18:54:48Z done
- 2026-10-03T18:54:49Z committed a5903df (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Lessons
- A false-positive report can sit on top of a bypass: chasing why fm text was misread found that the same misreading hid real commands, so ground every friction to its mechanism before relaxing anything.
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
