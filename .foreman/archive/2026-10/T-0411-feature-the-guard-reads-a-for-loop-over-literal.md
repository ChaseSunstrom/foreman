---
id: T-0411
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T04:50:33Z
updated: 2026-10-09T05:07:06Z
base: 78aaba75a89dc5e73d61ec4d883c17b831a3f7d1
base_tree: d7e892160c01c82c6306ffd09f1532717c23e17f
verified: strong
---
# FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w
## Raw request
> FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w …; done) as each value in turn, instead of an unknown variable (JARVIS: 'find -delete under unresolvable target .claude/worktrees/$w' twice) — only when the words are plain literals and the body never reassigns the variable; real-bash differential rows for the loop forms
## Interpretation
JARVIS keeps writing for w in agent-a agent-b; do find .claude/worktrees/$w … ; done and the guard refuses: inside a loop $w is unknown, so the target is unresolvable. When the loop's words are plain literals the values are known exactly; the guard should check each.
## Assumptions (confidence)
## Acceptance criteria
- [x] JARVIS's literal loops pass; loops over ~, globs, braces, a reassigned variable or a write outside still refuse; real bash agrees — verify with `python3 plugin/tests/run.py -k test_literal_for_loops_expand`
## Non-goals
## Approach (options → choice → why)
(A, chosen) rewrite a top-level for loop with plain literal words (no ~ glob brace quote $ backtick), a body with no nested loop/case/heredoc and no assignment to the variable, into the sequence BODY[w1]; …; VAR=wN before every other analysis. break/continue only make bash do less than checked. (B, rejected) take loop words even when the body reassigns the variable — unsafe. (C, rejected) a hint only — the refusal stays.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: allowed and refused loop rows + real-bash rows
2. [x] expand literal loops in check_bash before analysis
3. [x] replay, gate, changelog, ship
## Resume here
<!-- auto -->
- 2026-10-09T04:53:55Z step 1/3: test-first: allowed and refused loop rows + real-bash rows
- git: foreman/build; 3 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py
- touched since last checkpoint: plugin/lib/fmguard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_guard.py
## Docs impact
CHANGELOG entries for T-0411 and T-0412
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_literal_for_loops_expand` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LiteralLoops 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 165d79def478] (2026-10-09T04:59:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_literal_for_loops_expand` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: LiteralLoops 0s) / OK [ran] [tree 165d79def478] (2026-10-09T04:59:49Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py -p test_guard.py` → exit 0 · Ran 78 tests in 1.5s (28 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 165d79def478] (2026-10-09T04:59:51Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 04:56 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree bec652ffb4bb] (2026-10-09T05:00:50Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py -p test_guard.py` → exit 0 · Ran 78 tests in 1.5s (28 classes, 16 at a time; slowest: GuardAgainstBash 2s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree b7b98402274e] (2026-10-09T05:03:35Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py -p test_guard.py` → exit 0 · Ran 78 tests in 1.5s (28 classes, 16 at a time; slowest: GuardAgainstBash 2s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree 00fb2d1aa11b] (2026-10-09T05:05:42Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.5    33.2     150  [0] / SessionEnd                  29.8    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 944 tests in [ran] [tree 00fb2d1aa11b] (2026-10-09T05:06:52Z)
- (ac 1) `python3 plugin/tests/run.py -k test_literal_for_loops_expand` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: LiteralLoops 0s) / OK [ran] [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
- (audit intent) `self: diff read twice; one fm-reviewer pass (research T-0411-review) found 3 holes, plus 2 from the automated security review; all 5 fixed test-first with real-bash rows; replay 0 newly allowed` → JARVIS's two literal loops (find … -exec rm -r {} +; rm -rf …/$w/.pytest_cache, and git -C …/${w} status) pass; nothing else loosened [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
- (audit adversary) `self: diff read twice; one fm-reviewer pass (research T-0411-review) found 3 holes, plus 2 from the automated security review; all 5 fixed test-first with real-bash rows; replay 0 newly allowed` → argument done, loops behind &&/||/|, IFS, escaped separators, comments, ~/globs/braces/quotes, reassignment, break/continue — each refuses or is checked per word (rows in test_guard + test_guard_diff); T-0412 link in a linked folder judged in its real folder [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
- (audit edge) `self: diff read twice; one fm-reviewer pass (research T-0411-review) found 3 holes, plus 2 from the automated security review; all 5 fixed test-first with real-bash rows; replay 0 newly allowed` → done after & in the body, newline bodies, ${w}, a loop in $( ), a pipe or redirect after done (V not kept) — tested or left unexpanded (as before) [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
- (audit operator) `self: diff read twice; one fm-reviewer pass (research T-0411-review) found 3 holes, plus 2 from the automated security review; all 5 fixed test-first with real-bash rows; replay 0 newly allowed` → no new message or setting; a loop the guard can't read is refused exactly as before [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
- (audit maintainer) `self: diff read twice; one fm-reviewer pass (research T-0411-review) found 3 holes, plus 2 from the automated security review; all 5 fixed test-first with real-bash rows; replay 0 newly allowed` → one function plus a regex beside _mask_quotes, docstring names every bail-out; the T-0412 change is one line in classify_write [tree 00fb2d1aa11b] (2026-10-09T05:07:06Z)
## Log
- 2026-10-09T04:50:33Z created
- 2026-10-09T04:51:07Z focused
- 2026-10-09T04:52:37Z scope: test_an_uncertain_block_names_its_rewrite used a literal loop to get an uncertain target; it is now certain (core on plugin/lib/a), so the example becomes a computed list (for f in $(ls)), still uncertain
- 2026-10-09T04:53:55Z paused: focus moved to T-0412
- 2026-10-09T04:59:27Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T04:59:27Z focused
- 2026-10-09T05:02:55Z review: 3 holes — an unquoted 'done' argument ended the body early; V=last set after a loop behind &&/||/| (not run, or run in a subshell); IFS splits the substituted word. Also fixing here (same uncommitted diff, one commit): T-0412's link check missed a link inside a linked folder (security review) — the link is also judged in its folder's real location
- 2026-10-09T05:05:40Z security review: an escaped separator (echo \; done) could end the matched body early; loops in a command with a backslash are no longer expanded (rows added)
- 2026-10-09T05:07:06Z done
- 2026-10-09T05:07:06Z committed 5065f86 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0370 [FIX M, done, 2 steps] Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known — lesson: Before widening what the guar…
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
## Lessons
- A text rewrite ahead of the guard must reproduce bash's own word boundaries (reserved words only in command position, escapes, IFS) or bail: each shortcut was a bypass the reviewer found.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- CHANGELOG.md
- plugin/tests/test_hooks.py
