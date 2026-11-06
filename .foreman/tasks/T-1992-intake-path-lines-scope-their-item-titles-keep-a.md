---
id: T-1992
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmloop.py, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_loop.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-29T14:01:19Z
updated: 2026-10-29T14:11:15Z
batch: [T-1989, T-1990, T-1991]
base: b4df3e9f5dd04542dc2e6b01a179cd2cd28239fd
base_tree: 2c2f2e0c5dc2c997f2785f04c3c8d19b3b2936fa
plan0_at: 2026-10-29T14:01:36Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmloop.py, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_loop.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Intake @path lines scope their item, titles keep a mid-sentence @path, the loop brief says budget-limited rounds aren't…
## Raw request
> T-1989: FIX: an intake line made only of @path tokens, right under an item or its block lines, is dropped as untagged text instead of scoping that item (fmcore.parse_intake) @plugin/lib/fmcore.py
> DONE-WHEN: parse_intake attaches an @path-only line under an item to that item's scopes :: python3 plugin/tests/run.py test_core
> T-1990: FEATURE: the forever-loop round brief says a round run while optional work is dropped isn't counted dry (fmloop._brief step 5) @plugin/lib/fmloop.py
> DONE-WHEN: the brief with optional work dropped says it isn't counted dry :: python3 plugin/tests/run.py test_loop
> T-1991: FIX: a task title drops an @path written mid-sentence, leaving a double space (fmcli._title: 'made only of  tokens'); only a leading or trailing scope is a marker, as T-0334 does for refs
## Interpretation
Do T-1989, T-1990, T-1991 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1992. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1989: parse_intake attaches an @path-only line under an item to that item's scopes — verify with `python3 plugin/tests/run.py test_core`
- [x] T-1990: the brief with optional work dropped says it isn't counted dry — verify with `python3 plugin/tests/run.py test_loop`
- [x] T-1991: a title keeps an @path written mid-sentence as its text; a leading or trailing @path is dropped — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
T-1989: (a) in parse_intake's untagged branch, a line of only @path tokens while current is set adds them to r.items[-1].scopes; (b) treat it as a continuation (append to text); (c) leave it, document indenting. Choice (a): scopes only, text stays clean. T-1990: one clause in step 5 when pace is set. T-1991: (a) strip leading/trailing @scopes, inner ones keep their text minus the @ (mirrors T-0334 refs); (b) keep inner ones with the @; (c) collapse spaces only. Choice (a): same rule as refs, reads cleanly.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1989: An @path-only intake line under an item is dropped as untagged text instead of scoping that item
2. [x] T-1990: The forever-loop round brief says a round run while optional work is dropped isn't…
3. [x] T-1991: A task title drops an  written mid-sentence, leaving a double space (fmcli._title: 'made…
## Resume here
## Docs impact
CHANGELOG Unreleased: one T-1992 entry. MASTER line 374 (forever loop): T-1990 note. plugin/rules/foreman.md already documents @path scope; behaviour now matches it, no change.
## Verification evidence
- `python3 plugin/tests/run.py test_cli.CLI.test_a_mid_sentence_scope_keeps_its_text_and_an_end_one_is_dropped test_core -k at_path_line test_loop -k ahead_of_pace` → ✗ exit 1 · run.py: no test matches test_cli.CLI.test_a_mid_sentence_scope_keeps_its_text_and_an_end_one_is_dropped (start tree + this task's tests) [ran] [tree e132b3eaff10] (2026-10-29T14:01:53Z)
- `python3 plugin/tests/run.py test_cli.CLI.test_a_mid_sentence_scope_keeps_its_text_and_an_end_one_is_dropped test_core -k at_path_line test_loop -k ahead_of_pace` → ✗ exit 1 · run.py: no test matches test_cli.CLI.test_a_mid_sentence_scope_keeps_its_text_and_an_end_one_is_dropped [ran] [tree e132b3eaff10] (2026-10-29T14:01:53Z)
- `python3 plugin/tests/run.py test_cli -k mid_sentence_scope test_core -k at_path_line test_loop -k ahead_of_pace` → ✗ exit 1 · Ran 228 tests in 29.0s (60 classes, 16 at a time; slowest: TaskLifecycle 28s, CaptureAndIntake 10s, StateViews 10s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree dc5f498acaab] (2026-10-29T14:02:53Z)
- `python3 plugin/tests/run.py test_cli -k mid_sentence_scope test_core -k at_path_line test_loop -k ahead_of_pace` → ✗ exit 1 · Ran 228 tests in 25.0s (60 classes, 16 at a time; slowest: TaskLifecycle 25s, CaptureAndIntake 10s, StateViews 10s) / FAILED (3 classes) [ran] [tree dc5f498acaab] (2026-10-29T14:02:53Z)
- `python3 plugin/tests/run.py test_cli -k mid_sentence_scope test_core -k at_path_line test_loop -k ahead_of_pace` → ✗ exit 1 · Ran 228 tests in 30.8s (60 classes, 16 at a time; slowest: TaskLifecycle 29s, CaptureAndIntake 12s, StateViews 11s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree aa3a89a562c4] (2026-10-29T14:04:01Z)
- `python3 plugin/tests/run.py test_cli -k mid_sentence_scope test_core -k at_path_line test_loop -k ahead_of_pace` → exit 0 · Ran 228 tests in 26.2s (60 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 12s, StateViews 11s) / OK [ran] [tree aa3a89a562c4] (2026-10-29T14:04:01Z)
- (step 1) `python3 plugin/tests/run.py test_core -k at_path_line` → exit 0 · Ran 76 tests in 1.9s (18 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, ActiveFast 1s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:04:51Z)
- (step 2) `python3 plugin/tests/run.py test_loop -k ahead_of_pace` → exit 0 · Ran 17 tests in 4.4s (4 classes, 16 at a time; slowest: Loop 4s, LoopReview 4s, DegradeOnPace 1s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:04:56Z)
- (step 3) `python3 plugin/tests/run.py test_cli -k mid_sentence_scope` → exit 0 · Ran 135 tests in 23.9s (38 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:05:21Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmloop.py — commit it through a task, or git checkout it back / fm doctor:; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.9    41.1     150  [0] / SessionEnd                  34.5    35.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 423798ddabfc] (2026-10-29T14:09:31Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 76 tests in 1.9s (18 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, ActiveFast 1s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (ac 2) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 15 tests in 4.3s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (ac 3) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 135 tests in 23.3s (38 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (audit intent) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → an @path-only line under an item scopes it, a mid-sentence @path stays in the title, the brief states T-1986's rule — each member's ask, nothing more [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (audit edge) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → @path line under block lines scopes the item above; after a blank line it stays untagged; title of only a scope is still 'untitled'; a@b.com untouched [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (audit adversary) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → title regexes run on untrusted text but are linear (no overlapping quantifiers); scopes only widen what the brief lists, never the guard [tree 423798ddabfc] (2026-10-29T14:10:12Z)
- (audit intent) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → an @path-only line under an item scopes it, a mid-sentence @path stays in the title, the brief states T-1986's rule — each member's ask, nothing more [tree 423798ddabfc] (2026-10-29T14:10:47Z)
- (audit edge) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → @path line under block lines scopes the item above; after a blank line it stays untagged; title of only a scope is still 'untitled'; a@b.com untouched [tree 423798ddabfc] (2026-10-29T14:10:47Z)
- (audit adversary) `self-review of the diff (optional work dropped): each change matches its member; regexes have no nested ambiguity (literal @ separates quantifiers); email-style a@b keeps its text; a continuation after an @path line keeps the scope` → title regexes run on untrusted text but are linear (no overlapping quantifiers); scopes only widen what the brief lists, never the guard [tree 423798ddabfc] (2026-10-29T14:10:47Z)
## Log
- 2026-10-29T14:01:19Z created
- 2026-10-29T14:01:35Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_cli`
- 2026-10-29T14:01:35Z criterion 3 text: T-1991: A task title drops an  written mid-sentence, leaving a double space (fmcli._title: 'made… works → T-1991: a title keeps an @path written mid-sentence as its text; a leading or trailing @path is dropped
- 2026-10-29T14:01:35Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmloop.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_loop.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T14:01:36Z focused
- 2026-10-29T14:11:13Z done
- 2026-10-29T14:11:15Z committed db2eddf2 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1987 [FIX M, done, 3 steps] Ambient waits out fm ship's run, titles cut at a word, budget-limited loop rounds aren't dry — lesson: A loop's stop rule should count only…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_loop.py
## Why not caught
intake tests only put @path on the item's own line, and no title test had an @path mid-sentence; the rules promised @path scope anywhere
## Lessons
- When a parser files a line as unclassified, check whether it only extends the item above: the syntax doc already promised it
## Files touched
- plugin/tests/test_cli.py
- plugin/tests/test_core.py
- plugin/tests/test_loop.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmloop.py
- CHANGELOG.md
- MASTER.md
