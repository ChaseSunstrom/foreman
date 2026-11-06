---
id: T-1797
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-27T22:33:59Z
updated: 2026-10-28T07:56:09Z
revisit: 2026-10-28T02:00
base: c67bcbd961b5b27d968e3565b4221d45cde99260
base_tree: bfaa9df8bd5c7dca8376b375bd4cde9a2d9d7a5c
plan0_at: 2026-10-28T07:45:47Z
plan0_scope: []
verified: strong
---
# CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi
## Raw request
> CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor points at /usage (each warning now a one-line fix, f applies); check skills that say ultrathink (now xhigh on Opus/Sonnet 5.5); fm cost: show avg context per reply per session and flag one over 200k (the T-1796 regression check). Prompt/agent hook cap needs nothing (all 17 Foreman hooks are command hooks); fm run already waits out usage limits.
## Interpretation
Adopt what CC 2.1.305-312 added that Foreman should use: agents get autoCompactWindow (fm-builder has it; reviewer, recon, reproducer, debugger don't), fm doctor validates it and lists it among CC features, fm cost --sessions flags a session averaging over 200k context per reply (the T-1796 regression check), and the usage-burn warning points at /usage, where each warning is a one-line fix. Ultrathink: no skill says it, nothing to change. Prompt/agent hook cap: every Foreman hook is a command hook, nothing to change.
## Assumptions (confidence)
## Acceptance criteria
- [x] every Foreman agent but fm-scout has autoCompactWindow and fm doctor rejects a malformed one — verify with `python3 plugin/tests/run.py test_doctor test_agents`
- [x] fm cost --sessions flags a session averaging over 200k context per reply — verify with `python3 plugin/tests/run.py test_economics`
- [x] the usage-burn warning names /usage — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: (A) frontmatter + doctor field check + CC_FEATURES row + a flag column in --sessions + one more clause in the burn WARN; (B) a new fm doctor check per CC version; (C) a generic CC-changelog adopter. Choice: A, the smallest diff that uses each feature where Foreman already has the hook point; B and C add machinery for one-off adoption. Window 150000 matches fm-builder (Sonnet's 200k minus headroom); scout (Haiku, 20 turns) gets none: it never fills a window.
## Risks and rollback
## Execution prompt
## Steps
1. [x] agents: autoCompactWindow on reviewer, recon, reproducer, debugger; doctor validates it; CC_FEATURES row (2.1.312); tests first
2. [x] fm cost --sessions: a flag on a session averaging over 200k context per reply; test first
3. [x] usage-burn WARN: point at /usage (each warning a one-line fix, f applies); test first
## Resume here
<!-- auto -->
- 2026-10-28T07:49:18Z steps 3/3 done
- git: foreman/build; 10 uncommitted: CHANGELOG.md, plugin/agents/fm-debugger.md, plugin/agents/fm-recon.md, plugin/agents/fm-reproducer.md, plugin/agents/fm-reviewer.md, plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, plugin/tests/test_economics.py, plugin/tests/test_usage_burn.py
- touched since last checkpoint: plugin/tests/test_doctor.py, plugin/tests/test_economics.py, plugin/tests/test_usage_burn.py, plugin/agents/fm-debugger.md, plugin/agents/fm-recon.md, plugin/agents/fm-reproducer.md, plugin/agents/fm-reviewer.md, plugin/lib/fmdoctor.py, plugin/lib/fmcost.py, CHANGELOG.md
- failures met: assertionerror: 'over 0k' not found in 'sessions, last 0 day(s), costliest first (the con…
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 69 tests in 2.8s (24 classes, 16 at a time; slowest: ViewsRepair 2s, Command 2s, LockProbe 1s) / OK [ran] [tree f232b4a08d49] (2026-10-28T07:47:14Z)
- (step 2) `python3 plugin/tests/run.py test_economics` → exit 0 · Ran 3 tests in 0.8s (2 classes, 16 at a time; slowest: SessionCost 1s, BoundaryTokens 0s) / OK [ran] [tree f232b4a08d49] (2026-10-28T07:47:15Z)
- (step 3) `python3 plugin/tests/run.py test_usage_burn` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: UsageBurn 0s) / OK [ran] [tree f232b4a08d49] (2026-10-28T07:47:16Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_agents` → exit 0 · Ran 90 tests in 4.7s (31 classes, 16 at a time; slowest: Hook 4s, ViewsRepair 2s, Install 2s) / OK [ran] [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (ac 2) `python3 plugin/tests/run.py test_economics` → exit 0 · Ran 4 tests in 0.9s (2 classes, 16 at a time; slowest: SessionCost 1s, BoundaryTokens 0s) / OK [ran] [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 69 tests in 2.7s (24 classes, 16 at a time; slowest: ViewsRepair 2s, Command 2s, LockProbe 1s) / OK [ran] [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (audit intent) `one fm-reviewer pass (intent, operator, edge, maintainer): approved with 5 findings, all fixed test-first — subagent replies excluded from per-session averages, hint reworded, summary line past the top 15, isascii() digit guard, SESSION_OVER vs BURN_CONTEXT commented; full fm check green` → CC 2.1.296/2.1.312 agent autoCompactWindow on every sonnet agent, 2.1.311 /usage fixes named in the burn warning; no skill uses ultrathink, so nothing to adopt there [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (audit edge) `one fm-reviewer pass (intent, operator, edge, maintainer): approved with 5 findings, all fixed test-first — subagent replies excluded from per-session averages, hint reworded, summary line past the top 15, isascii() digit guard, SESSION_OVER vs BURN_CONTEXT commented; full fm check green` → a subagent transcript shares its parent's sessionId and no longer inflates its average (test); '²' rejected without a crash (test) [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (audit operator) `one fm-reviewer pass (intent, operator, edge, maintainer): approved with 5 findings, all fixed test-first — subagent replies excluded from per-session averages, hint reworded, summary line past the top 15, isascii() digit guard, SESSION_OVER vs BURN_CONTEXT commented; full fm check green` → fm cost --sessions flags a session averaging over 200k without telling users who already ran fm install-user to rerun it; doctor names the agent field from 2.1.312 [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
- (audit maintainer) `one fm-reviewer pass (intent, operator, edge, maintainer): approved with 5 findings, all fixed test-first — subagent replies excluded from per-session averages, hint reworded, summary line past the top 15, isascii() digit guard, SESSION_OVER vs BURN_CONTEXT commented; full fm check green` → cost at scale — autoCompactWindow 150000 on 5 agents caps each subagent's per-turn context below Foreman's 200k window; the session view scans transcripts once per call, as before [tree 8ecfad6bdd2d] (2026-10-28T07:55:58Z)
## Log
- 2026-10-27T22:33:59Z created
- 2026-10-27T22:34:03Z deferred: weekly usage at 95%; resumes after the 02:00 reset (revisit 2026-10-28)
- 2026-10-28T00:53:10Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00)
- 2026-10-28T07:37:55Z set status=planned
- 2026-10-28T07:45:47Z focused
- 2026-10-28T07:51:58Z review fixes: subagent replies left out of fm cost --sessions (scan sidechains=False), hint reworded so it doesn't re-send users who already ran fm install-user, an N-sessions-over-200k summary line, isascii() guard on maxTurns/autoCompactWindow, SESSION_OVER vs BURN_CONTEXT commented. Intent: no skill uses ultrathink (2.1.312 xhigh) so nothing to adopt there; only the burn warning points at /usage (2.1.311 f applies).
- 2026-10-28T07:56:07Z done
- 2026-10-28T07:56:09Z committed 0cfc428f (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- research mission-20261027-200117.pack: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playbooks, …
- research claude-code-capabilities: Method.** I read the README, the plugins/ and examples/ directory listings, the docs overview, and the CHANGELOG (about 1.06M characte…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
## Lessons
- Subagent transcripts carry their parent's sessionId (isSidechain true): any per-session figure must skip subagents/ paths
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/test_economics.py
- plugin/tests/test_usage_burn.py
- plugin/agents/fm-debugger.md
- plugin/agents/fm-recon.md
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-reviewer.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmcost.py
- CHANGELOG.md
