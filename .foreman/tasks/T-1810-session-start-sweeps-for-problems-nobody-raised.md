---
id: T-1810
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T07:09:15Z
updated: 2026-10-28T07:45:20Z
base: 527753e3cd8804d6d7b8b5143824348033d46941
base_tree: 23b3749aa30a6962becdfe7b4396ff1f5d11a90c
plan0_at: 2026-10-28T07:10:33Z
plan0_scope: []
verified: strong
---
# Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdue tidy, each with its action; every operator review multiplies cost at scale
## Raw request
> Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdue tidy, each with its action; every operator review multiplies cost at scale
## Interpretation
T-1800 left out the session-start sweep and cost-at-scale on every review. Session start must name problems nobody raised, each with the action that fixes it, read from caches so the hook stays fast: CI red on main, a model/window/CC change (redo the cost math), a blocked pile going stale, overdue tidy. The usage pace (burn line) and version skew (fm doctor) already exist.
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep names CI red on main, a setup change, a stale blocked pile and overdue tidy, each with its action, from caches only (no network at session start) — verify with `python3 plugin/tests/run.py test_foresight`
- [x] the reviewer multiplies cost at scale in every review, whatever the lens or task type — verify with `grep -q 'In every review, whatever the lens' plugin/agents/fm-reviewer.md`
## Non-goals
## Approach (options → choice → why)
Complete version: (a) the statusline snapshot records CC version; (b) fmcost.foresight() compares (model, window, version) with state/setup.json and on a change says so and drops burn.json so the cost math reruns; (c) the detached Stop refresh fetches GitHub check-runs for main at most every 30 min into ci.json (public API, 5 s, github remotes only) and captures one task per red sha; (d) blocked pile: count + oldest age; (e) the tidy line carries its action; (f) fm-reviewer multiplies cost at scale on every operator lens. Approaches: 1 cached sweep written by the existing detached refresh, read at session start (chosen: no network or scans in the hook); 2 live checks at session start (too slow for the ~150 ms hook budget); 3 a new fm verb run each session (a turn per session); 4 a cron job (outside CC, not plugin-portable). Deferred: auto-capture for anything but CI red (would spam the inbox).
## Risks and rollback
## Execution prompt
## Steps
1. [x] statusline snapshot records the CC version
2. [x] fmcost: foresight findings + CI cache refreshed by the Stop hook's detached refresh
3. [x] session start: one Unasked line; tidy line carries its action
4. [x] fm-reviewer: cost at scale on every operator lens
## Resume here
<!-- auto -->
- 2026-10-28T07:37:58Z steps 4/4 done
- git: foreman/build; 10 uncommitted: MASTER.md, plugin/agents/fm-reviewer.md, plugin/hooks/statusline, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/skills/intake/references/audit.md, plugin/tests/test_visibility.py, plugin/lib/fmforesight.py, plugin/tests/test_foresight.py
- touched since last checkpoint: plugin/lib/fmforesight.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/tests/test_foresight.py, MASTER.md
- failures met: fm release-check: failed (a temporary home, deleted); fm doctor: failed (0 pass, 0 warn, 0 fail)
## Docs impact
MASTER.md fmforesight bullet
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -25` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (0.4 s; last 14 of 14 lines) [ran] [tree 41d635a186c2] (2026-10-28T07:12:34Z)
- (step 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 6 tests in 0.4s (2 classes, 16 at a time; slowest: Foresight 0s, ReviewerCostAtScale 0s) / OK [ran] [tree 76df95b65396] (2026-10-28T07:14:02Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_usage_burn` → exit 0 · Ran 9 tests in 0.4s (3 classes, 16 at a time; slowest: UsageBurn 0s, Foresight 0s, ReviewerCostAtScale 0s) / OK [ran] [tree 1c19e7a9aa6a] (2026-10-28T07:14:23Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_hooks test_visibility` → exit 0 · Ran 224 tests in 41.0s (32 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree 1c19e7a9aa6a] (2026-10-28T07:15:05Z)
- (step 4) `grep -q 'In every review, whatever the lens' plugin/agents/fm-reviewer.md` → exit 0 · (no output) [ran] [tree 1c19e7a9aa6a] (2026-10-28T07:15:05Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · ✓ exit 0 (1.1 s) · OK [ran] [tree bfaa9df8bd5c] (2026-10-28T07:39:58Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 14 tests in 0.5s (3 classes, 16 at a time; slowest: Foresight 0s, CiMain 0s, ReviewerCostAtScale 0s) / OK [ran] [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (ac 2) `grep -q 'In every review, whatever the lens' plugin/agents/fm-reviewer.md` → exit 0 · (no output) [ran] [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (audit intent) `one fm-reviewer pass over the diff, 5 lenses; 10 findings fixed with tests (CiMain class plus 5 Foresight tests), 0 false positives; a live false red (cancelled newest run let an older failure speak, T-1816) fixed test-first after` → session start names CI red, setup change with the cost rerun, stale blocked pile, overdue tidy, each with its action; reviewer rule 5a multiplies cost at scale in every review [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (audit adversary) `one fm-reviewer pass over the diff, 5 lenses; 10 findings fixed with tests (CiMain class plus 5 Foresight tests), 0 false positives; a live false red (cancelled newest run let an older failure speak, T-1816) fixed test-first after` → API text plain-fitted to one line, sha must be 40 hex, so no forged CONTEXT or key matching every capture [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (audit edge) `one fm-reviewer pass over the diff, 5 lenses; 10 findings fixed with tests (CiMain class plus 5 Foresight tests), 0 false positives; a live false red (cancelled newest run let an older failure speak, T-1816) fixed test-first after` → private repo 404 retried daily, offline or rate-limited keeps the known line, clones share one call, a bad cache costs only its own line, non-main default branch read from origin/HEAD, cancelled newest run says nothing [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (audit operator) `one fm-reviewer pass over the diff, 5 lenses; 10 findings fixed with tests (CiMain class plus 5 Foresight tests), 0 false positives; a live false red (cancelled newest run let an older failure speak, T-1816) fixed test-first after` → session start reads caches only (0 calls); the Stop hook spawns one detached sweep per project per 10 min; GitHub calls at most 1 per repo per 30 min (48/day, well under 60/hour); FOREMAN_NO_NET and sensitive repos skip the network [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
- (audit maintainer) `one fm-reviewer pass over the diff, 5 lenses; 10 findings fixed with tests (CiMain class plus 5 Foresight tests), 0 false positives; a live false red (cancelled newest run let an older failure speak, T-1816) fixed test-first after` → capture_once reused, tests assert lines and calls, no new dependency [tree bfaa9df8bd5c] (2026-10-28T07:44:28Z)
## Log
- 2026-10-28T07:09:15Z created
- 2026-10-28T07:10:33Z focused
- 2026-10-28T07:15:17Z criterion 2 verify: `grep -q 'every operator lens' plugin/agents/fm-reviewer.md` → `grep -q 'In every review, whatever the lens' plugin/agents/fm-reviewer.md`
- 2026-10-28T07:15:17Z criterion 2 text: the reviewer multiplies cost at scale on every operator lens → the reviewer multiplies cost at scale in every review, whatever the lens or task type
- 2026-10-28T07:15:17Z scope: one cached sweep in a new fmforesight.py (state/foresight.json, not setup.json + ci.json); GitHub workflow runs, not check runs, so a continue-on-error job doesn't read as red; cost at scale moved from 'every operator lens' to every review (an M review may not run operator)
- 2026-10-28T07:45:19Z done
- 2026-10-28T07:45:20Z committed c67bcbd9 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- research mission-20261027-200117.pack: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playbooks, …
- decision 2026-10-23: T-1259: build the compaction storm and the window sweep, tested with the bench's fakes; the measured sweep (real Haiku sessions) waits until weekly …
## Lessons
- A cache fed only by a conditional path never fills, and tests that call the refresher directly hide it: test the trigger, not only the worker. A cancelled CI run is unknown, not skippable: skipping it lets an older red speak for a newer sha.
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- plugin/agents/fm-reviewer.md
- plugin/skills/intake/references/audit.md
- plugin/hooks/statusline
- plugin/lib/fmcost.py
- plugin/lib/fmhooks.py
- plugin/tests/test_visibility.py
- MASTER.md
- plugin/lib/fmcli.py
