---
id: T-1800
type: PERFORMANCE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-27T22:42:28Z
updated: 2026-10-28T01:22:06Z
revisit: 2026-10-28T02:00
base: 1033aefbe0c517b727822e106c384fd2b338288b
base_tree: 7ea87a2b9ae9b7fed3f4ba3845107c0258f99e0d
plan0_at: 2026-10-28T01:04:12Z
plan0_scope: []
verified: strong
---
# Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest)
## Raw request
> PERF: Foreman notices its own usage burn without being told. User (2026-10-27): 'I shouldn't have even had to tell you about the usage things, foreman should've figured it out itself.' Today fmbudget only pauses optional work when usage runs ahead of pace; it never diagnoses why. Done when: at session start and in fm doctor/digest, Foreman reads its own transcripts (as the T-1796 analysis did) and flags, with the cause and a fix: average context per reply over ~150k, a weekly forecast that runs out before reset, Opus subagents taking a big share, several sessions driving at once, or a hook/output style adding per-call context. It fixes what it owns (its env defaults, builder models) and tells the user once about the rest. Folds in T-1797's 'fm cost context per reply' item.
## Interpretation
Foreman should spot usage burn by itself: read the transcripts and the usage reading, name each cause with its fix, and show it where a session already looks (session start, fm doctor, fm digest). The rules and the reviewer reason about cost at scale, so problems are caught before any log shows them.
## Assumptions (confidence)
## Acceptance criteria
- [x] burn_findings names high context per reply, several sessions at once, Opus subagents' share and a weekly forecast that runs out early, each with its fix; a lean week says nothing — verify with `python3 plugin/tests/run.py test_usage_burn`
- [x] fm doctor warns with the findings and fm digest lists them; the session-start context carries one Usage burn line from the cached scan — verify with `python3 plugin/tests/run.py test_usage_burn`
- [x] the rules say reason ahead in one line and the reviewer's operator lens multiplies cost at scale — verify with `grep -q 'Multiply out' plugin/rules/foreman.md`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fm burn verb; (b) burn_findings in fmcost reused by doctor, digest and the detached cost refresh the Stop hook already runs, session start reading its cache; (c) only a rule line. Chose (b): no new verb, session start stays fast, and a rule line alone can't measure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] burn_findings in fmcost with a test
2. [x] fm doctor check, fm digest lines, cached scan for session start
3. [x] one rule line, reviewer cost-at-scale lens
## Resume here
<!-- auto -->
- 2026-10-28T01:05:05Z step 1/3: burn_findings in fmcost with a test
- git: foreman/build; 4 uncommitted: plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/tests/test_usage_burn.py
- touched since last checkpoint: plugin/tests/test_usage_burn.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/lib/fmcost.py
## Docs impact
plugin/rules/foreman.md: one Multiply out clause; plugin/skills/intake/references/audit.md: operator lens cost at scale; evals synced
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_usage_burn test_cost test_cost_forecast` → exit 0 · Ran 21 tests in 6.3s (8 classes, 16 at a time; slowest: TaskCostCap 6s, SkillUsage 2s, CostForecast 1s) / OK [ran] [tree ced10a90fd36] (2026-10-28T01:11:47Z)
- (step 2) `python3 plugin/tests/run.py test_usage_burn test_doctor test_hooks` → exit 0 · Ran 272 tests in 41.2s (49 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree ced10a90fd36] (2026-10-28T01:12:29Z)
- (step 3) `grep -q 'Multiply out' plugin/rules/foreman.md && grep -q 'cost at scale' plugin/skills/intake/references/audit.md` → exit 0 · (no output) [ran] [tree ced10a90fd36] (2026-10-28T01:12:29Z)
- (ac 1) `python3 plugin/tests/run.py test_usage_burn` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: UsageBurn 0s) / OK [ran] [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (ac 2) `python3 plugin/tests/run.py test_usage_burn` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: UsageBurn 0s) / OK [ran] [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (ac 3) `grep -q 'Multiply out' plugin/rules/foreman.md` → exit 0 · (no output) [ran] [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (audit intent) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → names each burn cause with its fix in doctor, digest and session start; rules line and operator lens added [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (audit edge) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → missing or corrupt burn.json and a stale scan give no line; a lean week says nothing [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (audit operator) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → cost at scale multiplied out: 0.4 s scan ≤6/hour per project, session start reads a file, never scans [tree 5b66d834148f] (2026-10-28T01:20:23Z)
- (audit intent) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → names each burn cause with its fix in doctor, digest and session start; rules line and operator lens added [tree 5b66d834148f] (2026-10-28T01:21:17Z)
- (audit edge) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → missing or corrupt burn.json and a stale scan give no line; a lean week says nothing [tree 5b66d834148f] (2026-10-28T01:21:17Z)
- (audit operator) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → cost at scale multiplied out: 0.4 s scan ≤6/hour per project, session start reads a file, never scans [tree 5b66d834148f] (2026-10-28T01:21:17Z)
- (audit adversary) `self-review in main thread (subagents paused by the usage budget): diff read line by line; found the account-wide scan ran on every per-minute cost refresh, now at most every 10 min; session start read the cache twice, now once` → eval prompt.md changes are the rules text re-synced by sync_evals.py, no guard wording changed; transcript fields are read as numbers and strings only, never run; a hostile burn.json only changes the text of one context line [tree 5b66d834148f] (2026-10-28T01:21:17Z)
## Log
- 2026-10-27T22:42:28Z created
- 2026-10-27T22:42:39Z set priority=urgent
- 2026-10-27T22:44:10Z steer (user 2026-10-27): 'foreman should just be smarter though, like you should've been able to reason about that and figure it out yourself without logs, like, just be insanely good, and not just specific to that either'. Scope widens: (1) a rule to multiply out every default, loop and hook (cost per call × calls × sessions × days) and re-check it whenever the model, window or CC version changes — the 70% override written for 200k became 700k on a 1M window, which reasoning alone catches; (2) each session start and after each reset, a sweep for what's wrong that nobody asked about (usage pace, CI on main red since 2026-10-21 unnoticed, version skew, 23 blocked tasks, tidy 12 days overdue), acting on each or saying it once; (3) a 'cost at scale' question in the reviewer's lenses so designs get it before they ship. Log-based checks (transcripts) stay as the backstop, not the first line.
- 2026-10-27T22:44:10Z set title=Foreman reasons ahead: multiply out every default, sweep for unasked problems, cost-at-scale review
- 2026-10-27T22:51:18Z deferred: weekly usage 95%: starts at the 02:00 reset (decision recorded; cron e82daac3 resumes at 02:07) (revisit 2026-10-28)
- 2026-10-28T00:53:10Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00)
- 2026-10-28T01:01:46Z set status=planned
- 2026-10-28T01:03:49Z set status=captured
- 2026-10-28T01:03:50Z planned from capture
- 2026-10-28T01:04:10Z set status=captured
- 2026-10-28T01:04:11Z planned from capture
- 2026-10-28T01:04:11Z focused
- 2026-10-28T01:22:04Z done
- 2026-10-28T01:22:06Z committed 90061eaa (12 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261027-200117.pack: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playbooks, …
- research mission-20261027-200117: Request: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playboo…
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- decision 2026-10-23: Usage pace: subagents paused at 75% weekly usage with 27% of the week gone; work continues in the main thread, security items first (T-1751, T-1749)…
## Measurements
burn scan: 0.4 s for 2 days of all projects (time python3 -c burn_findings); refresh cost: up to 60 scans/hour per project → at most 6 (10 min cache age); session start: 0 scans, one small file read
## Lessons
- Account-wide scans hung on a per-minute refresh multiply by projects; throttle them on their own cache age
## Files touched
- plugin/tests/test_usage_burn.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/rules/foreman.md
- plugin/skills/intake/references/audit.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/agents/fm-reviewer.md
