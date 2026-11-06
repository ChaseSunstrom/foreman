---
id: T-1212
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-1211]
source: user
created: 2026-10-16T15:15:51Z
updated: 2026-10-16T16:39:27Z
base: 5337fe99ef64ba18a6be2545a86320cea0ff61bc
base_tree: 6168a83e01b876cad181659e757455a4637fb33d
plan0_at: 2026-10-16T16:03:59Z
plan0_scope: []
verified: strong
---
# fm code: the harness-run loop, where the model fills slots and the harness plans, edits through the guard, verifies and closes
## Raw request
> fm code: the harness-run loop, where the model fills slots and the harness plans, edits through the guard, verifies and closes
## Interpretation
The loop of Foreman Code (T-1207), on top of fmmodels (T-1211). fm code "<request>" runs Foreman's stations itself; the model only fills a validated PLAN slot and then picks one tool action at a time; the harness makes the task through fm, applies edits, runs commands behind Foreman's guard, runs the verify commands, records evidence and closes the task.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_code.py runs fm code on a seeded bug (calc.add subtracts, with a pytest-free test) in a throwaway repo against a scripted OpenAI-compatible fake server: the task is created, the fix lands through the edit action, the verify passes and is recorded, the task closes; a scripted run of rm -rf ~ is refused and the refusal text reaches the model; a malformed plan is repaired; a failing verify goes back to the model and a second fix passes; --dry-plan changes nothing; --resume after a killed run finishes the task; an Anthropic-shaped fake works the same — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
plugin/lib/fmcode.py. PLAN slot {type FIX|FEATURE|CLEAN|PERFORMANCE|SECURITY|RESEARCH, tier S|M, title, criteria:[{text, verify}], steps:[...]} validated with bounded repair (2 retries quoting the error); the task is made with the fm CLI (fm task new … --focus): state only through fm. Then per step one action at a time, as a native tool call when the profile has tools, else a JSON object read with fmmodels.extract_json: read {path, start?, lines?} and search {pattern, glob?} run locally and bounded; edit {file, old, new} (all-or-nothing through fm edit's JSON stdin), write {file, content} and run {cmd} first go through the hook dispatcher exactly as other harnesses do (plugin/hooks/hook PreToolUse with a Claude-Code-shaped payload {tool_name: Edit|Write|Bash, tool_input, cwd, session_id}); exit 2 or a deny is a refusal sent back as the tool result and never executed; run output is cut to head and tail. done {summary} ends a step. After the last step the harness runs each criterion's verify through fm task evidence --run; a failure goes back to the model with its output (3 rounds), then --escalate MODEL if given, else fm task block with the reason. Close with fm task finish --audit "fm code (<model>): harness-run verify" (--commit unless --no-commit). A journal (the state dir's code/<task>.jsonl) records every message and action; --resume continues a crashed run from it. Output: one plain line per action, --json for an event stream. Options: --model, --escalate, --max-steps (default 40), --dry-plan (print the plan, change nothing), --resume, --no-commit; fm code models lists profiles and which answer. Register the verb in fmcli (lazy import, a help tier), MASTER rows, a README subsection. Options considered: let the model drive with free tool use like other harnesses (weak models wander), a fixed script with no model choices (can't explore), or this slot-and-action loop (chosen: the harness owns order and checks, the model owns judgment one small decision at a time).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: test_code.py with the scripted fake servers and the seeded repo
2. [x] fmcode.py: plan slot, task creation, action loop through the hook guard and fm edit, verify and retry, escalate, finish, journal and --resume, --dry-plan, fm code models
3. [x] fmcli registration, MASTER rows, README subsection
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code` → ✗ exit 1 · Ran 19 tests in 31.1s (9 classes, 16 at a time; slowest: Resume 30s, Hook 3s, Sync 2s) / FAILED (4 classes) [ran] [tree e612a8099448] (2026-10-16T16:11:05Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 21 tests in 24.5s (9 classes, 16 at a time; slowest: Repairs 24s, EndToEnd 16s, Resume 7s) / OK [ran] [tree eb7640620847] (2026-10-16T16:15:48Z)
- (step 3) `python3 plugin/tests/run.py test_code test_help test_docsdrift test_file_map_close test_cli` → exit 0 · Ran 143 tests in 28.2s (41 classes, 16 at a time; slowest: TaskLifecycle 28s, StateViews 10s, Repairs 9s) / OK [ran] [tree ab15d24fe534] (2026-10-16T16:20:36Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 21 tests in 6.1s (9 classes, 16 at a time; slowest: Repairs 6s, EndToEnd 4s, Resume 2s) / OK [ran] [tree ab15d24fe534] (2026-10-16T16:21:28Z)
- (step 2) `python3 plugin/tests/run.py test_code` → ✗ exit 1 · Ran 29 tests in 69.6s (10 classes, 16 at a time; slowest: Review 69s, Repairs 14s, EndToEnd 9s) / FAILED (2 classes) [ran] [tree 4f5a76592768] (2026-10-16T16:29:17Z)
- (ac 1) `python3 plugin/tests/run.py test_code test_models test_help test_docsdrift` → exit 0 · Ran 97 tests in 6.8s (19 classes, 16 at a time; slowest: Repairs 7s, Review 7s, EndToEnd 4s) / OK [ran] [tree c47fbd516a92] (2026-10-16T16:31:39Z)
- (step 3) `python3 plugin/tests/run.py test_code test_models test_help test_docsdrift` → exit 0 · Ran 97 tests in 44.6s (19 classes, 16 at a time; slowest: Repairs 44s, Review 43s, EndToEnd 25s) / OK [ran] [tree 44d98790e1db] (2026-10-16T16:37:35Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 29 tests in 21.6s (10 classes, 16 at a time; slowest: Repairs 21s, Review 21s, EndToEnd 16s) / OK [ran] [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (step 2) `python3 plugin/tests/run.py test_code test_models test_help test_docsdrift` → exit 0 · Ran 97 tests in 7.1s (19 classes, 16 at a time; slowest: Repairs 7s, Review 7s, EndToEnd 5s) / OK [ran] [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (audit adversary) `builder lane (opus) + one fm-reviewer pass over five lenses; all 9 findings fixed test-first in c4f47ed9 and spot-checked (credential/.git reads refused at fmcode.py:256, journal redact_obj :172, cut-off replies never run :391, killpg in finally :499)` → guard before edit/write/run fails closed; read/search refuse credentials and .git, skip FIFOs; tool output and journal redacted; /proc/PPID/environ output redacted before it reaches the model [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (audit edge) `builder lane (opus) + one fm-reviewer pass over five lenses; all 9 findings fixed test-first in c4f47ed9 and spot-checked (credential/.git reads refused at fmcode.py:256, journal redact_obj :172, cut-off replies never run :391, killpg in finally :499)` → partial multi-call kill resumes (every unanswered id answered); --max-steps stop resumable; --no-commit survives resume; cut-off write never runs [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (audit operator) `builder lane (opus) + one fm-reviewer pass over five lenses; all 9 findings fixed test-first in c4f47ed9 and spot-checked (credential/.git reads refused at fmcode.py:256, journal redact_obj :172, cut-off replies never run :391, killpg in finally :499)` → guard refusal of a verify gets one re-plan; context trimmed to last 6 results, smaller cut below 32k; fm code models lists profiles [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (audit maintainer) `builder lane (opus) + one fm-reviewer pass over five lenses; all 9 findings fixed test-first in c4f47ed9 and spot-checked (credential/.git reads refused at fmcode.py:256, journal redact_obj :172, cut-off replies never run :391, killpg in finally :499)` → public fmmodels helpers (configured, is_loopback); secret env list on Run; 22 tests in test_code [tree 44d98790e1db] (2026-10-16T16:38:27Z)
- (audit intent) `builder lane (opus) + one fm-reviewer pass over five lenses; all 9 findings fixed test-first in c4f47ed9 and spot-checked (credential/.git reads refused at fmcode.py:256, journal redact_obj :172, cut-off replies never run :391, killpg in finally :499)` → harness owns the loop: plan slot, action slot, guard, verify, close and commit; a verify passing at baseline proves nothing and goes back [tree 44d98790e1db] (2026-10-16T16:38:27Z)
## Log
- 2026-10-16T15:15:51Z created
- 2026-10-16T16:03:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1212.builder.md
- 2026-10-16T16:03:59Z focused
- 2026-10-16T16:35:32Z merged worktree-agent-a2a04367389589e04 (6 file(s))
- 2026-10-16T16:35:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2a04367389589e04
- 2026-10-16T16:35:51Z focused
- 2026-10-16T16:39:27Z done
- 2026-10-16T16:39:27Z committed 45f0bb6d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1210 [FEATURE L, dropped, 4 steps] fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
- T-1207 [FEATURE L, planned, 3 steps] Foreman Code: fm code runs Foreman's loop itself on any model or CLI
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- research mission-20261015-215750.pack: how can we make it so worktree agents can easily resumed if a session was stopped or something? etc. and super improve recursive b…
## Lessons
- A harness that sends tool output to a remote model must treat every read path as an exfiltration path: guard reads and redact output, not just commands
## Plan gaps
- failed first: step 1 Failing tests: test_code.py with the scripted fake servers and the seeded repo
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- plugin/lib/fmcli.py
- MASTER.md
- README.md
- plugin/lib/fmmodels.py
- CHANGELOG.md
