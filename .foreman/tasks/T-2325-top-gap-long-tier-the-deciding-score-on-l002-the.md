---
id: T-2325
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T12:12:07Z
updated: 2026-10-31T12:28:32Z
builder_model: sonnet
base: bde4e5142dd6fa0582024c16db9adc347c584743
base_tree: fbe320f04d11ef15919acb4abf68bd0725e0073c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T12:14:45Z
plan0_scope: []
verified: strong
---
# fm exam long keeps each session goal's activity summary, so a slow or false-done goal says where its time went
## Raw request
> TOP GAP (long tier, the deciding score): on l002 the foreman arm matched plain Claude at 4/20 hidden checks each (foreman 0/6 true done, plain 1/6), same $13.08 cost, but took about twice the wall time per goal (35-55 min vs 15-34) and claimed done on all 6 with hidden checks failing. Find where Foreman's time goes on a long goal (brief, evidence, audits, holds) from the l002 foreman fault logs and run info, and what its done-claims rested on; cut ceremony that doesn't change outcomes on long goals, and make 'done' rest on the goal's stated contract (names, values, done-when) rather than only the session's own tests
## Interpretation
l002: foreman matched plain at 4/20 checks but took twice the wall time and claimed done on 6/6 failing goals; nothing kept says why: each goal's temp state and transcript are deleted. Before the temp folder goes, keep a bounded summary of what the session did, for both session arms.
## Assumptions (confidence)
## Acceptance criteria
- [x] After a session goal, faults/<agent>/<id>.activity.json holds: tool calls by tool name, Bash commands by first word (fm verbs by verb), turns, the Foreman state's event counts by kind (stage events, holds, evidence runs, guard blocks) when present, and the session's final done claim text (c.plain'd, fitted); nothing from the repo beyond those counts and the fitted claim — verify with `python3 plugin/tests/run.py test_long`
- [x] fm exam long grade --json carries each goal's activity summary next to its metrics, and a text 'where the time went' line per arm shows the top tools and fm verbs — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
Options: 1) summarize the transcript and the temp Foreman state per goal before cleanup; 2) keep the whole temp dir per goal (large, holds repo copies); 3) rerun a goal by hand with tracing. Choice 1: bounded, keeps no repo content, answers 'where did the time go' for every goal of every run.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test with the stub claude: a goal's activity file exists with tool and fm-verb counts; grade --json includes it
2. [x] In _goal_session, before the temp dir is removed, read the session transcript (claude's project folder for the temp cwd, by session id) and the temp Foreman state's events, write the summary; read it in grade
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -25` → ✗ exit 1 · Ran 39 tests in 39.0s (7 classes, 16 at a time; slowest: Long 37s, Approvals 2s, AuditPrep 1s) / FAILED (1 classes: test_long.Long) [ran] [tree f445fa40f373] (2026-10-31T12:16:16Z)
- (ac 2) `python3 plugin/tests/run.py test_long 2>&1 | tail -25` → ✗ exit 1 · Ran 39 tests in 39.0s (7 classes, 16 at a time; slowest: Long 37s, Approvals 2s, AuditPrep 1s) / FAILED (1 classes: test_long.Long) [ran] [tree f445fa40f373] (2026-10-31T12:16:16Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | grep -v "Warning\|spans =\|open(" | tail -15` → exit 0 · Ran 39 tests in 38.6s (7 classes, 16 at a time; slowest: Long 38s, Approvals 2s, AuditPrep 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:17:05Z)
- (ac 2) `python3 plugin/tests/run.py test_long 2>&1 | grep -v "Warning\|spans =\|open(" | tail -15` → exit 0 · Ran 39 tests in 38.6s (7 classes, 16 at a time; slowest: Long 38s, Approvals 2s, AuditPrep 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:17:05Z)
- (step 1) `python3 plugin/tests/run.py test_long 2>&1 | grep -v "Warning\|spans =\|open(" | tail -15` → exit 0 · Ran 39 tests in 38.6s (7 classes, 16 at a time; slowest: Long 38s, Approvals 2s, AuditPrep 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:17:05Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 39.8s (7 classes, 16 at a time; slowest: Long 39s, Approvals 2s, AuditPrep 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:17:47Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 32.0s (7 classes, 16 at a time; slowest: Long 32s, Approvals 2s, Stop 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:18:19Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_long && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.38s] [ran] [tree a5ea88277365] (2026-10-31T12:19:12Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 28.3s (7 classes, 16 at a time; slowest: Long 28s, Approvals 1s, AuditPrep 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:23:01Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 28.2s (7 classes, 16 at a time; slowest: Long 28s, Approvals 1s, Stop 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:23:30Z)
- `python3 plugin/tests/run.py test_long -k activity` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes: test_long.Long) (start tree + this task's tests) [ran] [tree a5ea88277365] (2026-10-31T12:23:33Z)
- `python3 plugin/tests/run.py test_long -k activity` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree a5ea88277365] (2026-10-31T12:23:33Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 28.3s (7 classes, 16 at a time; slowest: Long 28s, Approvals 1s, Stop 1s) / OK [ran] [tree 4ea5920d8d9a] (2026-10-31T12:24:13Z)
- (ac 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 39 tests in 28.3s (7 classes, 16 at a time; slowest: Long 28s, Approvals 1s, Stop 1s) / OK [ran] [tree 4ea5920d8d9a] (2026-10-31T12:24:13Z)
- (audit intent) `self-review of the merged diff plus a check of the transcript shape against this session's real jsonl (type assistant, message.content[].type tool_use with name): counts only, names and words c.plain'd and capped at 30 per map, event scan capped at 50k lines, the claim fitted to 300; the test proves repo text ('secret') never lands in the file` → the next long run says where each arm's time went and what its done claims said, so l002's 2x-time gap can be diagnosed [tree 4ea5920d8d9a] (2026-10-31T12:24:13Z)
- (audit edge) `self-review of the merged diff plus a check of the transcript shape against this session's real jsonl (type assistant, message.content[].type tool_use with name): counts only, names and words c.plain'd and capped at 30 per map, event scan capped at 50k lines, the claim fitted to 300; the test proves repo text ('secret') never lands in the file` → malformed transcript lines are skipped; no Foreman state (plain arm) leaves events None; a kill-and-resume goal sums every session id's turns [tree 4ea5920d8d9a] (2026-10-31T12:24:13Z)
- (audit adversary) `self-review of the merged diff plus a check of the transcript shape against this session's real jsonl (type assistant, message.content[].type tool_use with name): counts only, names and words c.plain'd and capped at 30 per map, event scan capped at 50k lines, the claim fitted to 300; the test proves repo text ('secret') never lands in the file` → the summary keeps counts and a fitted, c.plain'd claim, never file contents or commands' arguments [tree 4ea5920d8d9a] (2026-10-31T12:24:13Z)
## Log
- 2026-10-31T12:12:07Z created
- 2026-10-31T12:14:30Z planned from capture
- 2026-10-31T12:14:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2325.builder.md
- 2026-10-31T12:14:45Z focused
- 2026-10-31T12:14:45Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T12:22:32Z merged worktree-agent-a7013ba7b45a6ec46 (2 file(s))
- 2026-10-31T12:22:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7013ba7b45a6ec46
- 2026-10-31T12:22:32Z focused
- 2026-10-31T12:23:44Z scope: plugin/lib/fmlong.py (_activity, went, _goal_session, grade), plugin/tests/test_long.py (and its stub), MASTER.md, CHANGELOG.md
- 2026-10-31T12:24:55Z done
- 2026-10-31T12:24:57Z committed feb7fdc3 (2 files)
- 2026-10-31T12:25:03Z guard authorization added: publish
- 2026-10-31T12:28:32Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2263 [FEATURE M, done, 3 steps] Long-horizon exam (3/3): per-goal metrics and the deciding scorecard row — lesson: A deciding metric must not merge different events: '…
- decision 2026-10-31: l002 long tier result recorded as measured: foreman = plain on hidden checks (4/20 each), foreman 0/6 vs plain 1/6 true done, 2x wall time; no Forem…
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
## Lessons
- Measure where time goes before deciding what to cut: keep a bounded activity summary of every graded run
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- MASTER.md
- CHANGELOG.md
