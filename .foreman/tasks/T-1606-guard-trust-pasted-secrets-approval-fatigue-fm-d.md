---
id: T-1606
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/lib/fmcore.py, plugin/skills/doctor/SKILL.md, plugin/tests/test_guard_hardening.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:38:49Z
updated: 2026-10-22T22:22:26Z
base: e9576124ea04a81fbdfa0277f12391ad17db1cd1
base_tree: bc1b485752747174f3b17561859aba4887891132
plan0_at: 2026-10-22T21:47:52Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/skills/doctor/SKILL.md, plugin/tests/test_guard_hardening.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Guard trust: pasted secrets, approval fatigue, fm doctor --wrong (from T-1553)
## Raw request
> Guard trust: pasted secrets, approval fatigue, fm doctor --wrong (from T-1553)
## Interpretation
Three trust features. (1) A key-shaped secret in a user's prompt (anything fmcore.redact would replace: API keys, tokens, JWTs, private keys, password= [REDACTED], URL credentials) gets one UserPromptSubmit note that names its kind, never its text: don't repeat it, write it into files, commands or task text, and suggest rotating it if it was pasted by mistake. The prompt log already stores only redacted text. (2) Approval fatigue: fm ask counts asks per category in the asking session (meta, reset when the session changes); from the third same-category ask the reply adds a note to batch the rest (for core: --standing; otherwise one ask covering the remaining work) so the user isn't asked again and again. (3) fm doctor --wrong "CMD" [--should allow|block] [--cwd DIR] files a false alarm (or a miss) as a labelled guard case (fmreplay.add_case) and captures one FIX task naming the case for review; it never loosens the guard itself. /foreman:doctor documents it, so it works from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a key-shaped secret in a prompt gets one note and is never echoed; repeated same-category asks in a session get a fatigue note; fm doctor --wrong CMD files a labelled case for review — verify with `cd plugin/tests && python3 -m unittest test_guard_hardening.Trust`
## Non-goals
## Approach (options → choice → why)
Options for secrets: block the prompt (the user loses their message), silently redact (Claude still sees it, nobody warned), or a note. Choice: the note, redaction stays where it already is. Fatigue: a global counter (wrong across sessions), events.jsonl scans per ask (slow), or a small per-session counter in meta. Choice: the meta counter. --wrong: reuse fm guard wrong's add_case plus a capture so a person reviews it, rather than a new store. Nothing here loosens the guard.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: Trust class (secret note, fatigue note, doctor --wrong)
2. [x] secret note in user_prompt_submit
3. [x] per-session ask counter and fatigue note in fm ask
4. [x] fm doctor --wrong and the doctor skill line
5. [x] review fixes: veto redaction, pasted blocks, short note, task in the corpus's project, per-session tallies, unable wording
## Resume here
## Docs impact
~/.claude/foreman/plugin/skills/doctor/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_hardening.Trust` → red as expected (exit 1) · Ran 3 tests in 4.3s (1 classes, 16 at a time; slowest: Trust 4s) / FAILED (1 classes) [ran] [tree c038ff0d1c0d] (2026-10-22T22:10:16Z)
- (step 2) `python3 plugin/tests/run.py test_guard_hardening.Trust test_hooks.UserPromptSubmit` → exit 0 · Ran 18 tests in 7.3s (2 classes, 16 at a time; slowest: UserPromptSubmit 7s, Trust 2s) / OK [ran] [tree b1d86fa767ce] (2026-10-22T22:12:12Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening.Trust test_approvals 2>/dev/null || python3 plugin/tests/run.py test_guard_hardening.Trust` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: Trust 2s) / OK [ran] [tree b1d86fa767ce] (2026-10-22T22:12:14Z)
- (step 4) `python3 plugin/tests/run.py test_guard_hardening.Trust test_doctor test_guard_cases` → exit 0 · Ran 86 tests in 2.9s (23 classes, 16 at a time; slowest: GuardCases 3s, Trust 2s, Command 2s) / OK [ran] [tree b1d86fa767ce] (2026-10-22T22:12:18Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Trust` → exit 0 · Ran 3 tests in 1.747s / OK [ran] [tree b1d86fa767ce] (2026-10-22T22:12:20Z)
- (step 5) `python3 plugin/tests/run.py test_guard_hardening.Trust` → red as expected (exit 1) · Ran 6 tests in 4.2s (1 classes, 16 at a time; slowest: Trust 4s) / FAILED (1 classes) [ran] [tree b127473cfbdb] (2026-10-22T22:15:33Z)
- (step 5) `python3 plugin/tests/run.py test_guard_hardening.Trust test_hooks test_core test_doctor` → exit 0 · Ran 329 tests in 57.7s (60 classes, 16 at a time; slowest: Stop 58s, NoTaskGate 43s, PreToolUse 36s) / OK [ran] [tree 7840c0572fbb] (2026-10-22T22:18:49Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Trust` → exit 0 · Ran 6 tests in 3.410s / OK [ran] [tree 7840c0572fbb] (2026-10-22T22:18:53Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1606-review.md)` → the note names a kind, never the value; vetoes and their words are redacted; pasted blocks scanned; --wrong refuses key-shaped commands and never changes the guard [tree 7840c0572fbb] (2026-10-22T22:19:10Z)
- (audit edge) `review edge lens` → note under 100 characters; tallies per session; unable verdict worded apart [tree 7840c0572fbb] (2026-10-22T22:19:10Z)
- (audit operator) `fm doctor --wrong output names the corpus file and the project the task went to` → tested with a temp corpus [tree 7840c0572fbb] (2026-10-22T22:19:11Z)
- (audit maintainer) `kind names asserted one per pattern; fatigue note limited to work already in the plan` → clean [tree 7840c0572fbb] (2026-10-22T22:19:11Z)
- (audit design) `the doctor skill gained one step for Claude Code` → one line [tree 7840c0572fbb] (2026-10-22T22:19:11Z)
- (audit intent) `criterion: one note never echoing the secret; fatigue note on repeated asks; doctor --wrong files a labelled case` → met (6 tests, 329 across hooks, core, doctor) [tree 7840c0572fbb] (2026-10-22T22:19:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Trust` → exit 0 · Ran 6 tests in 3.429s / OK [ran] [tree 7840c0572fbb] (2026-10-22T22:19:16Z)
- (audit adversary) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → no path stores the secret; tasks filed where the case lives [tree 7840c0572fbb] (2026-10-22T22:19:16Z)
- (audit edge) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → short note, per-session tallies [tree 7840c0572fbb] (2026-10-22T22:19:16Z)
- (audit intent) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → met [tree 7840c0572fbb] (2026-10-22T22:19:16Z)
- (audit adversary) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → no path stores the secret; tasks filed where the case lives [tree 7840c0572fbb] (2026-10-22T22:21:12Z)
- (audit edge) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → short note, per-session tallies [tree 7840c0572fbb] (2026-10-22T22:21:12Z)
- (audit intent) `one fm-reviewer six-lens pass; 5 findings fixed test-first` → met [tree 7840c0572fbb] (2026-10-22T22:21:12Z)
## Log
- 2026-10-22T20:38:49Z created
- 2026-10-22T21:35:51Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdoctor.py', 'plugin/skills/doctor/SKILL.md', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T21:47:51Z focused
- 2026-10-22T21:48:19Z paused: focus moved to T-1609
- 2026-10-22T22:09:27Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-22T22:09:27Z focused
- 2026-10-22T22:10:11Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmcore.py', 'plugin/skills/doctor/SKILL.md', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:21:12Z scope: fmcodetui, fmcost, fmdesign, fmimg, fmlanes, fmmotion, fmplaybooks and the playbooks SKILL.md changed through other tasks' merges and closes (T-1516, T-1624, T-1630, T-1621, T-1685) while T-1606 was open; none are T-1606 edits
- 2026-10-22T22:22:24Z done
- 2026-10-22T22:22:26Z committed 1d177f86 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- research T-1517-review: Verdict:** approve with nits. I found no bypass of the guard lock, no guard rule change, and nothing dangerous or secret in the allow-corpus. The…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/tests/test_guard_hardening.py; re-ground the plan against them before editing
## Why not caught
the first test checked the prompt log only; the veto path stores the same words elsewhere
## Lessons
- A claim like 'kept redacted' must be tested by walking every file the feature can write, not the one log you had in mind
## Plan gaps
- added late: review fixes: veto redaction, pasted blocks, short note, task in the corpus's project, per-session tallies, unable word…
## Files touched
- plugin/tests/test_guard_hardening.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/doctor/SKILL.md
- plugin/lib/fmcodetui.py
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmimg.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmotion.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/verify/verification-loop.md
- plugin/tests/test_code_tui.py
- plugin/tests/test_lanes.py
- plugin/tests/test_motion_score.py
- plugin/tests/test_playbook_machinery.py
- plugin/tests/test_raster.py
- plugin/tests/test_reliability_tools.py
- plugin/tests/test_site_hero.py
- site/build.py
- site/index.html
- site/style.css
