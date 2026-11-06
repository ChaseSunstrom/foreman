---
id: T-2296
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T08:19:34Z
updated: 2026-10-31T08:50:57Z
batch: [T-2280, T-2295]
builder_model: sonnet
base: 0d7500422fab4b4a87d74d9a4257a5a8f11985de
base_tree: 46811fc59d5172739b117f8269e036abee97689d
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T08:21:54Z
plan0_scope: []
verified: strong
---
# Batch: The friction digest's guard example is …; Fmfriction give-up lines name task ids …
## Raw request
> T-2280: The friction digest's guard example is the command's first 160 chars (fmfriction.py:132), which cuts a heredoc before the line the guard judged (_writes_unrun_source): build the example with heredoc bodies dropped (the guard's _drop_data_heredocs) and append the rule's hint
> T-2295: fmfriction give-up lines name task ids only: append each task's block reason so the friction report says why it gave up
## Interpretation
Do T-2280, T-2295 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2296. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2280: the digest's guard example drops data-heredoc bodies (the guard's own _drop_data_heredocs) before fitting to 160 chars and appends the blocking rule's hint, so the judged line shows — verify with `python3 plugin/tests/run.py test_friction`
- [x] T-2295: each give-up line names every task with its block reason (c.plain, fitted), from the task_block event's data — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
Options: 1) re-run the guard's parser on the stored cmd and show the judged line only; 2) drop heredoc bodies with the guard's existing _drop_data_heredocs, then fit, plus the rule hint from the event; 3) store a cleaned example at block time in the guard. Choice 2: reuses the guard's own function read-only, no guard edit (protected), and old events gain it too. Give-ups: read the block reason from the task_block event's data (option 1), the brief's block line (2), or fm task show (3); choice 1, already in the events loaded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2280: The friction digest's guard example is the command's first 160 chars…
2. [x] T-2295: Fmfriction give-up lines name task ids only: append each task's block reason so the…
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_friction 2>&1 | tail -15` → ✗ exit 1 · Ran 18 tests in 65.2s (5 classes, 16 at a time; slowest: Friction 63s, UserPromptSubmit 6s, BoardIdeas 1s) / FAILED (1 classes) [ran] [tree 9ea9bde550af] (2026-10-31T08:25:15Z)
- (ac 2) `python3 plugin/tests/run.py test_friction 2>&1 | tail -15` → ✗ exit 1 · Ran 18 tests in 65.2s (5 classes, 16 at a time; slowest: Friction 63s, UserPromptSubmit 6s, BoardIdeas 1s) / FAILED (1 classes) [ran] [tree 9ea9bde550af] (2026-10-31T08:25:15Z)
- (step 1) `python3 plugin/tests/run.py test_friction -k heredoc` → exit 0 · Ran 1 tests in 4.5s (1 classes, 16 at a time; slowest: Friction 2s) / OK [ran] [tree 13983beff066] (2026-10-31T08:28:17Z)
- (step 2) `python3 plugin/tests/run.py test_friction -k give_up` → exit 0 · Ran 2 tests in 3.6s (2 classes, 16 at a time; slowest: Mining 2s, Friction 1s) / OK [ran] [tree 13983beff066] (2026-10-31T08:28:23Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_friction && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 153 tests across 4 files. [95.56s] [ran] [tree 13983beff066] (2026-10-31T08:31:08Z)
- (ac 1) `python3 plugin/tests/run.py test_friction 2>&1 | tail -12` → ✗ exit 1 · Ran 18 tests in 22.4s (5 classes, 16 at a time; slowest: Friction 22s, UserPromptSubmit 2s, BoardIdeas 1s) / FAILED (1 classes) [ran] [tree b6889f204942] (2026-10-31T08:42:02Z)
- (ac 2) `python3 plugin/tests/run.py test_friction 2>&1 | tail -12` → ✗ exit 1 · Ran 18 tests in 22.4s (5 classes, 16 at a time; slowest: Friction 22s, UserPromptSubmit 2s, BoardIdeas 1s) / FAILED (1 classes) [ran] [tree b6889f204942] (2026-10-31T08:42:02Z)
- (ac 1) `python3 plugin/tests/run.py test_friction 2>&1 | tail -8` → exit 0 · Ran 18 tests in 26.9s (5 classes, 16 at a time; slowest: Friction 26s, UserPromptSubmit 3s, BoardIdeas 1s) / OK [ran] [tree 172f71693e61] (2026-10-31T08:42:37Z)
- (ac 2) `python3 plugin/tests/run.py test_friction 2>&1 | tail -8` → exit 0 · Ran 18 tests in 26.9s (5 classes, 16 at a time; slowest: Friction 26s, UserPromptSubmit 3s, BoardIdeas 1s) / OK [ran] [tree 172f71693e61] (2026-10-31T08:42:37Z)
- (step 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 18 tests in 13.2s (5 classes, 16 at a time; slowest: Friction 13s, UserPromptSubmit 2s, BoardIdeas 1s) / OK [ran] [tree 172f71693e61] (2026-10-31T08:42:53Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_friction && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [33.07s] [ran] [tree 172f71693e61] (2026-10-31T08:43:40Z)
- (step 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 18 tests in 6.1s (5 classes, 16 at a time; slowest: Friction 6s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree 846c5909c186] (2026-10-31T08:49:17Z)
- (step 2) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 18 tests in 9.9s (5 classes, 16 at a time; slowest: Friction 10s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree 846c5909c186] (2026-10-31T08:49:28Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 18 tests in 10.2s (5 classes, 16 at a time; slowest: Friction 10s, UserPromptSubmit 1s, Mining 0s) / OK [ran] [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (ac 2) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 18 tests in 10.2s (5 classes, 16 at a time; slowest: Friction 10s, UserPromptSubmit 1s, Mining 0s) / OK [ran] [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator): 1 MEDIUM (transcript lookup keyed on the head-160 text missed the hook's windowed log, so the drop never fired in production; test logged the head) and LOWs (hint when allowed, examples for unshown keys, fm edit bodies dropped, uncapped command, hint width); all fixed test-first by the builder, the test now logs through fmhooks._window; I read the fixed diff` → the digest shows the judged line and the rule's hint, and why each blocked task gave up [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator): 1 MEDIUM (transcript lookup keyed on the head-160 text missed the hook's windowed log, so the drop never fired in production; test logged the head) and LOWs (hint when allowed, examples for unshown keys, fm edit bodies dropped, uncapped command, hint width); all fixed test-first by the builder, the test now logs through fmhooks._window; I read the fixed diff` → fmguard only called; the command is redacted before the drop; transcript paths come from a regex-checked session id; output c.plain'd and fitted [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator): 1 MEDIUM (transcript lookup keyed on the head-160 text missed the hook's windowed log, so the drop never fired in production; test logged the head) and LOWs (hint when allowed, examples for unshown keys, fm edit bodies dropped, uncapped command, hint width); all fixed test-first by the builder, the test now logs through fmhooks._window; I read the fixed diff` → a short logged window could match an unrelated command in that session (only the example changes); no transcript falls back to the logged text [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator): 1 MEDIUM (transcript lookup keyed on the head-160 text missed the hook's windowed log, so the drop never fired in production; test logged the head) and LOWs (hint when allowed, examples for unshown keys, fm edit bodies dropped, uncapped command, hint width); all fixed test-first by the builder, the test now logs through fmhooks._window; I read the fixed diff` → examples built only for shown keys, commands capped at 20k, one transcript scan shared with the recheck [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator): 1 MEDIUM (transcript lookup keyed on the head-160 text missed the hook's windowed log, so the drop never fired in production; test logged the head) and LOWs (hint when allowed, examples for unshown keys, fm edit bodies dropped, uncapped command, hint width); all fixed test-first by the builder, the test now logs through fmhooks._window; I read the fixed diff` → _lookup shared by _example and _recheck, fixing the recheck's same head-160 miss [tree 30eb4d30b7c4] (2026-10-31T08:50:01Z)
## Log
- 2026-10-31T08:19:34Z created
- 2026-10-31T08:19:51Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_friction`
- 2026-10-31T08:19:51Z criterion 1 text: T-2280: The friction digest's guard example is the command's first 160 chars… works → T-2280: the digest's guard example drops data-heredoc bodies (the guard's own _drop_data_heredocs) before fitting to 160 chars and appends the blocking rule's hint, so the judged line shows
- 2026-10-31T08:19:51Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_friction`
- 2026-10-31T08:19:51Z criterion 2 text: T-2295: Fmfriction give-up lines name task ids only: append each task's block reason so the… works → T-2295: each give-up line names every task with its block reason (c.plain, fitted), from the task_block event's data
- 2026-10-31T08:21:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2296.builder.md
- 2026-10-31T08:21:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2296.builder.md
- 2026-10-31T08:21:51Z focused
- 2026-10-31T08:21:54Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T08:49:10Z merged worktree-agent-a3b6630ecd8b9ca05 (2 file(s))
- 2026-10-31T08:49:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3b6630ecd8b9ca05
- 2026-10-31T08:49:10Z focused
- 2026-10-31T08:49:50Z scope: plugin/lib/fmfriction.py, plugin/tests/test_friction.py, MASTER.md, CHANGELOG.md
- 2026-10-31T08:50:50Z done
- 2026-10-31T08:50:57Z committed d67b33b6 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- T-0817 [FIX M, done, 3 steps] Guard refusals read better: /dev/null on a data-only python -c, a state-direct hint that points to fm research, and pat… — lesson: A refusa…
- decision 2026-10-31: [revisited: Standing rule from gen 2 on: one Mission per generation is a moonshot] [cites: the user's steer 2026-10-30 (fifth): moonshot Mission fro…
## Lessons
- A test must log through the same function production logs through (fmhooks._window), or it proves a format production never writes
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- MASTER.md
- CHANGELOG.md
