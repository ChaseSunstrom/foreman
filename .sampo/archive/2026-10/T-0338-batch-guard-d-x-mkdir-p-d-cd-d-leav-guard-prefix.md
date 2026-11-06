---
id: T-0338
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T02:40:56Z
updated: 2026-10-06T03:01:52Z
batch: [T-0330, T-0331, T-0332, T-0334]
base: c8ba8de29bb7afc13719b9ba72d0425b1d03ac7c
base_tree: 3c757d394eee6349152054ff3d6834b67ad9ce98
verified: strong
---
# Batch: Guard: D=~/x; mkdir -p $D && cd $D leav…; Guard: _prefix_vars counts every bare w…; Fm session/claude send: opti…
## Raw request
> T-0330: Guard: D=~/x; mkdir -p $D && cd $D leaves D unknown (fmguard _track_vars drops ~ values) so a cd into a home path guesses the Foreman checkout as target; expand leading ~ to ctx.home first
> T-0331: Guard: _prefix_vars counts every bare word, so a stray -S or path segment named like a var makes S=…; (cmd > $S/log &) unknown; count only assignment targets
> T-0332: fm session/claude send: options after positional id fail (nargs=* rest + parse_args); try parse_intermixed_args or reorder-tolerant parsing
> T-0334: fm capture strips every #T- ref from the title and never records it as depends; keep mid-text refs and record refs as depends
## Interpretation
Do T-0330, T-0331, T-0332, T-0334 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0338.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0330: Guard: D=~/x; mkdir -p $D && cd $D leaves D unknown (fmguard _track_vars drops ~ values) s works — verify with `python3 plugin/tests/run.py -k test_guard`
- [x] T-0331: Guard: _prefix_vars counts every bare word, so a stray -S or path segment named like a var works — verify with `python3 plugin/tests/run.py -k test_guard`
- [x] T-0332: Fm session/claude send: options after positional id fail (nargs=* rest + parse_args); try works — verify with `python3 plugin/tests/run.py -k test_claude`
- [x] T-0334: Fm capture strips every #T- ref from the title and never records it as depends; keep mid-t works — verify with `python3 plugin/tests/run.py -k test_cli`
## Non-goals
## Approach (options → choice → why)
Each fix at its root, test-first: _track_vars expands a leading ~ before its unknown-value test (needs ctx); _prefix_vars counts only words that can be names (not after - / .); fmcli main uses parse_intermixed_args so options may follow positionals (fallback to parse_args if it raises TypeError on this parser); capture keeps #T- refs mid-text and records them as depends. Option rejected: special-casing each command's argv order.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0330: Guard: D=~/x; mkdir -p $D && cd $D leaves D unknown (fmguard _track_vars drops ~ values) s
2. [x] T-0331: Guard: _prefix_vars counts every bare word, so a stray -S or path segment named like a var
3. [x] T-0332: Fm session/claude send: options after positional id fail (nargs=* rest + parse_args); try
4. [x] T-0334: Fm capture strips every #T- ref from the title and never records it as depends; keep mid-t
5. [x] tests (red) for all four
6. [x] guard: ~ values and prefix-var counting
7. [x] cli: intermixed send args; capture refs as depends
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 5) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 798444572f91] (2026-10-06T02:44:58Z)
- (step 3) `python3 plugin/tests/run.py -k test_session.Session.test_review_fixes` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Session 1s) / FAILED (1 classes) [ran] [tree 032bc9159fbf] (2026-10-06T02:48:08Z)
- (step 4) `python3 plugin/tests/run.py -k test_cli.CaptureAndIntake` → ✗ exit 1 · Ran 7 tests in 1.1s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / FAILED (1 classes) [ran] [tree 8329ea7061e0] (2026-10-06T02:48:34Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 62 tests in 1.2s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:06Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 62 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:08Z)
- (step 5) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 62 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:09Z)
- (step 6) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 62 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:10Z)
- (step 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.8s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:15Z)
- (step 4) `python3 plugin/tests/run.py -k test_cli.CaptureAndIntake` → exit 0 · Ran 7 tests in 1.1s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:17Z)
- (step 7) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 74 tests in 14.2s (18 classes, 16 at a time; slowest: TaskLifecycle 14s, StateViews 5s, Checks 3s) / OK [ran] [tree a5b0a22bd614] (2026-10-06T02:51:31Z)
- (step 5) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 3 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 02d5616e62b6] (2026-10-06T02:55:33Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:11Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:12Z)
- (step 5) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:14Z)
- (step 6) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:15Z)
- (step 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.9s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:20Z)
- (step 7) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.9s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:26Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (ac 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 63 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (ac 3) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 6 tests in 1.6s (2 classes, 16 at a time; slowest: Claude 2s, Remote 0s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (ac 4) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 74 tests in 14.4s (18 classes, 16 at a time; slowest: TaskLifecycle 14s, StateViews 5s, Checks 3s) / OK [ran] [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (audit intent) `one fm-reviewer adversary pass (research T-0338-review): 2 HIGH bypasses + 1 MEDIUM + 3 LOW, all fixed test-first; fm replay 0 newly allowed/blocked over 5000 real commands; differential bash test with 9 new forms green` → the four friction blocks (D=~ var, -S/path-segment count, $S/app computed name, options after send id) now pass; capture keeps mid-text refs and records depends [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (audit adversary) `one fm-reviewer adversary pass (research T-0338-review): 2 HIGH bypasses + 1 MEDIUM + 3 LOW, all fixed test-first; fm replay 0 newly allowed/blocked over 5000 real commands; differential bash test with 9 new forms green` → reviewer's word-split bypass ($S/etc → eval X=/etc) closed — a path-named command is trusted only when every var in it is a known plain literal; false && HOME=/x; rm $HOME stays unknown; ~ unknown once HOME is set; replay found and fixed one false block (S= && rm $S/x …; …) [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (audit edge) `one fm-reviewer adversary pass (research T-0338-review): 2 HIGH bypasses + 1 MEDIUM + 3 LOW, all fixed test-first; fm replay 0 newly allowed/blocked over 5000 real commands; differential bash test with 9 new forms green` → ~user, ~+, quoted ~, globs stay unknown; and-chain after a non-assignment link is uncertain; message flags without -- still error [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (audit operator) `one fm-reviewer adversary pass (research T-0338-review): 2 HIGH bypasses + 1 MEDIUM + 3 LOW, all fixed test-first; fm replay 0 newly allowed/blocked over 5000 real commands; differential bash test with 9 new forms green` → the exact friction commands (S=…; pkill; ($S/app >> $S/app.log &); cd && fm next) pass in tests [tree 65893c4f7946] (2026-10-06T03:01:51Z)
- (audit maintainer) `one fm-reviewer adversary pass (research T-0338-review): 2 HIGH bypasses + 1 MEDIUM + 3 LOW, all fixed test-first; fm replay 0 newly allowed/blocked over 5000 real commands; differential bash test with 9 new forms green` → changes stay inside _prefix_vars/_track_vars/_outside/_a_path with T- comments; one new argv helper in fmcli [tree 65893c4f7946] (2026-10-06T03:01:51Z)
## Log
- 2026-10-06T02:40:56Z created
- 2026-10-06T02:44:23Z focused
- 2026-10-06T03:01:51Z done
- 2026-10-06T03:01:52Z committed 06726bb (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261006: 1. **Answer.** Four of the five friction points trace to small, local causes. The guard leaves a variable unknown when its value starts with `~`. …
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research T-0269-review-1: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict [stale: plugin/lib/fmcore.py, plugin/lib/fmguard.py chang…
## Lessons
- Making a guard trust more is a security change: every precision fix needs an adversary pass and a replay, because the obvious generalisation (a / makes it a path; an && prefix ran) is exactly where bash disagrees.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_session.py
- plugin/lib/fmcli.py
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/tests/test_guard_diff.py
