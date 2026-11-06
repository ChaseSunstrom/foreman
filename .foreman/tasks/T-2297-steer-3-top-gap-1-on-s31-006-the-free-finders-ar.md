---
id: T-2297
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T08:29:41Z
updated: 2026-10-31T09:33:03Z
builder_model: sonnet
base: b6557ebb0584bf2fa4c76b3f74c2908b7643b281
base_tree: 4005eb75fe990326bc8c42553b0e2fdb90515309
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T08:38:03Z
plan0_scope: []
verified: strong
---
# Sessions account for every fm find lead they were shown: fixed, reported or refuted before the turn ends
## Raw request
> Steer 3 top gap (#1): on s31-006 the free finders arm found 16/18 with 0 false alarms while the foreman session arm (Haiku) found 15/18 with 4; the session path should start from fm find's ranked, proven leads and report nothing unproven, so it never scores below the free arm. Read the arm's answers under the s31-006 run to see which finding it missed and where the 4 false alarms came from
## Interpretation
T-2184 shows fm find's leads at session start (s31-006 foreman went 6/18 -> 15/18), but the session still dropped leads it saw (rank-rust: clamp untested, named in its own notes, never reported) and reported unproven suspicions on a clean repo (clean-rust: overflow, CJK width, 'no failing test yet'), so the free arm still out-found it (16/18, 0 false alarms). Make the session path hold itself to the leads it was given and keep unproven suspicions labeled as leads.
## Assumptions (confidence)
## Acceptance criteria
- [x] When session start showed fm find leads, the Stop hook holds the turn once if any of those leads is still present on a re-scan and the final reply names neither its symbol nor its file:line, listing each such lead with the three ways out (fix test-first, report it, refute it with the reason); a reply that names them, or a second stop, passes — verify with `python3 plugin/tests/run.py test_hooks`
- [x] The leads shown are recorded per session (keys only, under the session's state) so the Stop check needs no model call, stays under the hook's time budget (re-scan capped as at session start), and a session that saw no leads is untouched — verify with `python3 plugin/tests/run.py test_hooks`
- [x] The session-start leads note and the hold say a suspicion with no failing test is reported as a lead, not a finding — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: 1) Stop-hook accounting: record the leads shown at session start, hold once at Stop for any still present and unnamed in the reply; 2) change the exam's prompt so the foreman arm lists fm find output (rejected: arms must share one prompt, that games the metric); 3) a deterministic report: fm find's proven leads appended to every session's final answer by a hook. Choice 1: it is the session path holding itself to its own tool on any repo, costs no model call, and leaves the decision (fix, report, refute) with the session; 3 would report leads nobody checked, adding false alarms.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: a session that saw 2 leads stops with a reply naming 1 -> held once listing the other; naming both -> passes; second stop -> passes; no leads -> untouched
2. [x] Record shown lead keys at SessionStart (_leads_note), check them in the Stop hook with a capped re-scan, add the lead-vs-finding wording
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 222 tests in 123.7s (29 classes, 16 at a time; slowest: Stop 122s, NoTaskGate 80s, PreToolUse 77s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:41:40Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 222 tests in 123.7s (29 classes, 16 at a time; slowest: Stop 122s, NoTaskGate 80s, PreToolUse 77s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:41:40Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 222 tests in 123.7s (29 classes, 16 at a time; slowest: Stop 122s, NoTaskGate 80s, PreToolUse 77s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:41:40Z)
- (step 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 222 tests in 123.7s (29 classes, 16 at a time; slowest: Stop 122s, NoTaskGate 80s, PreToolUse 77s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:41:40Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 222 tests in 107.1s (29 classes, 16 at a time; slowest: Stop 106s, NoTaskGate 73s, PreToolUse 68s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:43:30Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 222 tests in 161.1s (29 classes, 16 at a time; slowest: Stop 160s, PreToolUse 80s, NoTaskGate 80s) / OK [ran] [tree d314de5ecaa9] (2026-10-31T08:46:12Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_compact test_drive_side test_guard_evasions test_hooks test_memory test_onwrite test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.60s] [ran] [tree d314de5ecaa9] (2026-10-31T08:47:27Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → ✗ exit 1 · Ran 226 tests in 98.8s (29 classes, 16 at a time; slowest: Stop 98s, NoTaskGate 57s, PreToolUse 52s) / FAILED (1 classes) [ran] [tree 6672db1e888f] (2026-10-31T08:52:21Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → ✗ exit 1 · Ran 226 tests in 98.8s (29 classes, 16 at a time; slowest: Stop 98s, NoTaskGate 57s, PreToolUse 52s) / FAILED (1 classes) [ran] [tree 6672db1e888f] (2026-10-31T08:52:21Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → ✗ exit 1 · Ran 226 tests in 98.8s (29 classes, 16 at a time; slowest: Stop 98s, NoTaskGate 57s, PreToolUse 52s) / FAILED (1 classes) [ran] [tree 6672db1e888f] (2026-10-31T08:52:21Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 95.9s (29 classes, 16 at a time; slowest: Stop 95s, NoTaskGate 57s, PreToolUse 50s) / FAILED (1 classes) [ran] [tree ace0267df65a] (2026-10-31T08:54:12Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 95.9s (29 classes, 16 at a time; slowest: Stop 95s, NoTaskGate 57s, PreToolUse 50s) / FAILED (1 classes) [ran] [tree ace0267df65a] (2026-10-31T08:54:12Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 95.9s (29 classes, 16 at a time; slowest: Stop 95s, NoTaskGate 57s, PreToolUse 50s) / FAILED (1 classes) [ran] [tree ace0267df65a] (2026-10-31T08:54:12Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 169.4s (29 classes, 16 at a time; slowest: Stop 169s, NoTaskGate 83s, PreToolUse 79s) / FAILED (1 classes) [ran] [tree 92cf5b3ce379] (2026-10-31T08:57:08Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 169.4s (29 classes, 16 at a time; slowest: Stop 169s, NoTaskGate 83s, PreToolUse 79s) / FAILED (1 classes) [ran] [tree 92cf5b3ce379] (2026-10-31T08:57:08Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → ✗ exit 1 · Ran 226 tests in 169.4s (29 classes, 16 at a time; slowest: Stop 169s, NoTaskGate 83s, PreToolUse 79s) / FAILED (1 classes) [ran] [tree 92cf5b3ce379] (2026-10-31T08:57:08Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 56 tests in 146.7s (1 classes, 16 at a time; slowest: Stop 146s) / OK [ran] [tree 3ecf52c3fa9f] (2026-10-31T09:08:11Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_compact test_drive_side test_guard_evasions test_hooks test_memory test_onwrite test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [41.74s] [ran] [tree 3ecf52c3fa9f] (2026-10-31T09:10:19Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 226 tests in 58.7s (29 classes, 16 at a time; slowest: Stop 58s, NoTaskGate 37s, PreToolUse 32s) / OK [ran] [tree cdc8cb49eb5d] (2026-10-31T09:29:44Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 226 tests in 62.0s (29 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 38s, PreToolUse 32s) / OK [ran] [tree cdc8cb49eb5d] (2026-10-31T09:30:46Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 226 tests in 39.8s (29 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 226 tests in 39.8s (29 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 226 tests in 39.8s (29 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): MEDIUM (a question turn spent the one hold), MEDIUM (bare substring matching named 'get' in 'budget'), LOWs (strict file:line forms, Stop errors logged as SessionStart, no pruning, no stacking test); all fixed test-first by the builder; I read the fixed diff` → a session shown fm find's leads can't end a working turn having silently dropped one; it fixes, reports or refutes each, and unproven suspicions are labeled leads [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): MEDIUM (a question turn spent the one hold), MEDIUM (bare substring matching named 'get' in 'budget'), LOWs (strict file:line forms, Stop errors logged as SessionStart, no pruning, no stacking test); all fixed test-first by the builder; I read the fixed diff` → lead text is c.plain'd, fitted and JSON-quoted as data; the record path is a hashed session id; a hostile repo can only shape the one hold's quoted rows [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): MEDIUM (a question turn spent the one hold), MEDIUM (bare substring matching named 'get' in 'budget'), LOWs (strict file:line forms, Stop errors logged as SessionStart, no pruning, no stacking test); all fixed test-first by the builder; I read the fixed diff` → reply-only turns never spend the hold; word-boundary and basename:line matching; a lead fixed mid-session drops off the re-scan; a re-scan past the deadline skips without holding [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): MEDIUM (a question turn spent the one hold), MEDIUM (bare substring matching named 'get' in 'budget'), LOWs (strict file:line forms, Stop errors logged as SessionStart, no pruning, no stacking test); all fixed test-first by the builder; I read the fixed diff` → no model call; one capped re-scan per session that was shown leads; records pruned after 7 days [tree 5258155f1370] (2026-10-31T09:31:53Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): MEDIUM (a question turn spent the one hold), MEDIUM (bare substring matching named 'get' in 'budget'), LOWs (strict file:line forms, Stop errors logged as SessionStart, no pruning, no stacking test); all fixed test-first by the builder; I read the fixed diff` → _leads_scan shared by session start and Stop; the hold runs only when no other Stop reason exists [tree 5258155f1370] (2026-10-31T09:31:53Z)
## Log
- 2026-10-31T08:29:41Z created
- 2026-10-31T08:37:38Z planned from capture
- 2026-10-31T08:37:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2297.builder.md
- 2026-10-31T08:38:01Z focused
- 2026-10-31T08:38:03Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T09:28:43Z merged worktree-agent-ae9482278f8ff7f77 (2 file(s))
- 2026-10-31T09:28:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae9482278f8ff7f77
- 2026-10-31T09:28:44Z focused
- 2026-10-31T09:31:13Z scope: plugin/lib/fmhooks.py (_leads_scan, _leads_note, _leads_hold, _lead_named, _tools_ran), plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md
- 2026-10-31T09:32:54Z done
- 2026-10-31T09:32:56Z committed af2cb346 (2 files)
- 2026-10-31T09:33:03Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
- the similar finished task took 4 steps
## Lessons
- Showing a session a tool's output isn't the session using it: close the loop at Stop with a deterministic check of what it was shown, held once
## Files touched
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
- MASTER.md
- CHANGELOG.md
