---
id: T-1279
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-20T16:55:30Z
updated: 2026-10-20T17:29:38Z
base: d168d412caac0b1a0a1a324d2213e47d543ea862
base_tree: a6ae6d753208c23a99f25a98fc93e29bb6ee5cd3
plan0_at: 2026-10-20T17:20:29Z
plan0_scope: []
verified: strong
---
# Reply format in the rules; fm install-user stops setting Foreman's output style and takes back the one it set
## Raw request
> Foreman's reply format in the rules file (sent once a session) instead of only the output style, whose per-turn reminder was 2.1% of the context; fm doctor says what the style costs per turn and that the rules now carry it (the user's style setting is left alone)
## Interpretation
Claude Code adds '<style> output style is active. Remember to follow the specific guidelines for this style.' to every turn while a non-default style is selected; with Foreman's style that was 2.7% of what entered the context over three days, the largest part of Foreman's 6.8%. Foreman's installer chose that style for users who had none. Carry the reply format in the rules file (sent once a session, cached) and stop choosing the style; take back the style where Foreman chose it.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/rules/foreman.md carries Foreman's reply format in at most 600 more characters, and a test keeps the rules file under 6,800 bytes — verify with `python3 plugin/tests/run.py test_docs`
- [x] fm install-user no longer sets outputStyle; where Foreman set it (outputStyle_set) and it is still foreman:Foreman, install removes it and says why; a style the user chose is left alone — verify with `python3 plugin/tests/run.py test_setup`
## Non-goals
## Approach (options → choice → why)
Options: (a) rules carry the format, install stops setting the style and takes back its own; (b) shorten the style (the reminder is Claude Code's fixed text, so no saving); (c) leave it and only report the cost. Choice: (a); the style file stays for anyone who picks it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: the rules' reply section and size budget; install takes back Foreman's own style and leaves a user's
2. [x] Rules section, fmsetup change, docs (README, MASTER, CHANGELOG)
## Resume here
## Docs impact
CHANGELOG, MASTER output-style row and doctor's rules cap; README had no mention
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_setup test_docs` → exit 0 · Ran 77 tests in 4.9s (17 classes, 16 at a time; slowest: Install 5s, TaskLifecycle 3s, Uninstall 2s) / OK [ran] [tree 3522abc7c02d] (2026-10-20T17:23:17Z)
- (step 2) `python3 plugin/tests/run.py test_setup test_docs` → exit 0 · Ran 77 tests in 2.9s (17 classes, 16 at a time; slowest: Install 3s, TaskLifecycle 1s, Uninstall 1s) / OK [ran] [tree 3522abc7c02d] (2026-10-20T17:24:21Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 46 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- (ac 2) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 32 tests in 2.3s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 1s) / OK [ran] [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- `python3 plugin/tests/run.py test_setup test_docs test_doctor test_cost` → exit 0 · Ran 143 tests in 29.8s (41 classes, 16 at a time; slowest: Command 30s, ViewsRepair 20s, TaskCostCap 6s) / OK [ran] [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- (audit intent) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → the largest part of Foreman's own context share was Claude Code's per-turn output-style reminder, there only because Foreman's installer chose the style; the format now rides in the rules, sent once a session [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- (audit edge) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → a user's own style (no flag) is never touched, nor foreman:Foreman when the user chose it; a style changed since install keeps the user's choice and only the flag goes; re-running install does nothing [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- (audit adversary) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → install edits only the outputStyle key Foreman's own manifest says it set; nothing reads user input into settings [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- (audit self) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → no findings [tree 6a1d2a7c35b5] (2026-10-20T17:27:46Z)
- `python3 plugin/tests/run.py test_setup test_docs test_doctor test_cost` → exit 0 · Ran 143 tests in 33.1s (41 classes, 16 at a time; slowest: Command 33s, ViewsRepair 26s, TaskCostCap 6s) / OK [ran] [tree 6a1d2a7c35b5] (2026-10-20T17:29:04Z)
- (audit intent) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → the largest part of Foreman's own context share was Claude Code's per-turn output-style reminder, there only because Foreman's installer chose the style; the format now rides in the rules, sent once a session [tree 6a1d2a7c35b5] (2026-10-20T17:29:04Z)
- (audit edge) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → a user's own style (no flag) is never touched, nor foreman:Foreman when the user chose it; a style changed since install keeps the user's choice and only the flag goes; re-running install does nothing [tree 6a1d2a7c35b5] (2026-10-20T17:29:04Z)
- (audit adversary) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → install edits only the outputStyle key Foreman's own manifest says it set; nothing reads user input into settings [tree 6a1d2a7c35b5] (2026-10-20T17:29:04Z)
- (audit self) `main session read the diff: install takes back only the style it set (outputStyle_set) and only while it is still foreman:Foreman; the rules section is 335 bytes; evals re-synced` → no findings [tree 6a1d2a7c35b5] (2026-10-20T17:29:04Z)
## Log
- 2026-10-20T16:55:30Z created
- 2026-10-20T17:20:15Z planned from capture
- 2026-10-20T17:20:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1279.builder.md
- 2026-10-20T17:20:29Z focused
- 2026-10-20T17:27:11Z merged worktree-agent-a2955efc9d1cf01f7 (11 file(s))
- 2026-10-20T17:27:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2955efc9d1cf01f7
- 2026-10-20T17:27:12Z focused
- 2026-10-20T17:29:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1257 [FEATURE M, done, 2 steps] Fm cost shows Foreman's own share of the context: its skill-listing part, hook notes and f — lesson: Transcript attachments carry their…
- T-1276 [PERFORMANCE M, done, 3 steps] fm output: measure it right (fm-only commands), then trim the biggest verbs' default output — lesson: Check a measurement's attribu…
## Measurements
Per turn: Claude Code's output-style reminder (~100 characters: 'foreman:Foreman output style is active. Remember to follow the specific guidelines for this style.') → 0 once the style is off; per session: the style prompt 1,448 → the rules' Replies section 335 characters (wc -c). Over three days on this repo the style was 2.7% of what entered the context (fm cost --days 3); the after figure needs sessions without the style.
## Lessons
- Measure before choosing what to cut: the style reminder, not fm output, was Foreman's biggest share
## Files touched
- plugin/tests/test_setup.py
- plugin/tests/test_docs.py
- plugin/lib/fmsetup.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- MASTER.md
- plugin/lib/fmdoctor.py
