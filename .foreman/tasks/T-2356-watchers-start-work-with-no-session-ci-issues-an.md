---
id: T-2356
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmforesight.py, plugin/lib/fmeco.py, plugin/lib/fmorders.py, plugin/lib/fmcli.py, plugin/tests/test_night.py, plugin/tests/test_foresight.py]
depends_on: [T-2355]
source: user
created: 2026-10-31T14:01:00Z
updated: 2026-10-31T18:00:32Z
builder_model: sonnet
base: 9b08fe0d00d84d2b179a90a3049276d22dad8a3a
base_tree: 742bdf5afc8d8675b3aa6327d0b2ecf916c39584
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:12:43Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmforesight.py, plugin/lib/fmeco.py]
lane_stop: merged 2026-10-31T17:54:03Z
verified: strong
---
# Watchers start work with no session: CI, issues and file events on a zero-token tick (Mission 8, #11)
## Raw request
> Watchers start work with no session: CI, issues and file events on a zero-token tick (Mission 8, #11)
## Interpretation
Reading 1: a model-free fm night --tick that, with no session, polls standing orders' file and schedule triggers, the CI result fmforesight's existing call fetches, and new GitHub issues for approved repos, each through the trigger table (gap map #11 unattended issue/CI watch). Reading 2: a long-running file watcher that reacts to every change at once. Ruled out: it needs a resident install for sub-hour latency nothing has yet asked for, and it stays in the idea catalogue with its signal, a red main waiting past one tick twice.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm night --tick runs no model: it reads standing orders' file and schedule triggers and the CI result fmforesight cached, adding no fetch of its own; when the timer runs it with no session open, CI is fetched only if the user approved that line in T-2357's ask, and each such fetch is listed for the final report; it files each finding through the trigger table; a sensitive project or FOREMAN_NO_NET reads nothing remote — verify with `python3 plugin/tests/run.py test_night test_foresight`
- [x] New open GitHub issues are polled only for a repo whose issue watch the user said yes to (brief T-2357's ask names it); without that yes the tick sends no new request off the machine, and each poll that runs is listed for the final report — verify with `python3 plugin/tests/run.py test_night`
- [x] The tick runs by default from the Stop hook's detached sweep, at most once per sweep interval, and from the timer once installed — verify with `python3 plugin/tests/run.py test_night test_foresight`
- [x] An issue whose body asks to push, delete or run something yields one quoted capture and nothing else: no command run, no file changed — verify with `python3 plugin/tests/run.py test_night`
## Non-goals
## Approach (options → choice → why)
1) fm night --tick: standing orders' file and schedule triggers and the CI poll, each through the trigger table; GitHub issues only for a repo whose issue watch the user approved in T-2357's ask, on fm inbox gh's untrusted path (redacted, defanged, quoted); each poll listed for the final report; run from the Stop hook's detached sweep and by the timer once installed. Fails if: an issue body carries an instruction, which the quoted path never executes, and the tick does nothing when sensitive or offline. 2) Use what exists: fm inbox gh and the Stop sweep as they are, called by hand or at stop. Likely outcome: with no session nothing notices a red main, a new issue or a changed file. 3) Do less: CI watch only through the existing foresight call, no issues and no file events. Fails if: issues and file triggers stay manual, two of the three named gaps. 4) Cloud routines. Breaks 'stays on the machine': they leave it and need a grant. Choice 1 (80%): zero tokens, the trigger table already routes, and each poll has a test.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/tests/test_night.py, MASTER.md, CHANGELOG.md, plugin/tests/test_ecosystem.py; past FIXes T-0921, T-0926, T-1819.
## Execution prompt
## Steps
1. [x] red tests: the three polls; nothing when sensitive or offline; the sweep runs it; injected issue text
2. [x] fm night --tick; the sweep calls it; issues through fm inbox gh's path
3. [x] docs: MASTER night line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:56:37Z steps 3/3 done
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night` → ✗ exit 1 · Ran 29 tests in 22.2s (11 classes, 16 at a time; slowest: Night 19s, NightGuards 6s, NightTick 3s) / FAILED (1 classes: test_night.NightTick) [ran] [tree 65a3de822c2d] (2026-10-31T16:16:03Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | tail -40` → ✗ exit 1 · Ran 43 tests in 8.0s (14 classes, 16 at a time; slowest: Night 8s, NightGuards 2s, NightTick 1s) / FAILED (1 classes: test_night.NightTick) [ran] [tree 690cca25cf0f] (2026-10-31T16:18:04Z)
- (ac 3) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | tail -40` → ✗ exit 1 · Ran 43 tests in 8.0s (14 classes, 16 at a time; slowest: Night 8s, NightGuards 2s, NightTick 1s) / FAILED (1 classes: test_night.NightTick) [ran] [tree 690cca25cf0f] (2026-10-31T16:18:04Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | grep -v "ResourceWarning\|cur = open" | tail -25` → exit 0 · Ran 43 tests in 11.7s (14 classes, 16 at a time; slowest: Night 11s, NightGuards 2s, NightTick 1s) / OK [ran] [tree d2d6b684c3ae] (2026-10-31T16:18:24Z)
- (ac 3) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | grep -v "ResourceWarning\|cur = open" | tail -25` → exit 0 · Ran 43 tests in 11.7s (14 classes, 16 at a time; slowest: Night 11s, NightGuards 2s, NightTick 1s) / OK [ran] [tree d2d6b684c3ae] (2026-10-31T16:18:24Z)
- (step 2) `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 43 tests in 20.5s (14 classes, 16 at a time; slowest: Night 20s, NightGuards 6s, NightTick 3s) / OK [ran] [tree d2d6b684c3ae] (2026-10-31T16:18:49Z)
- (step 3) `grep -c 'T-2356' MASTER.md` → exit 0 · 1 [ran] [tree 0ea3c79e604a] (2026-10-31T16:18:58Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_foresight test_guard_cases test_night test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [17.85s] [ran] [tree 0ea3c79e604a] (2026-10-31T16:19:45Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | grep -v "ResourceWarning\|cur = open" | tail -40` → exit 0 · Ran 48 tests in 22.3s (14 classes, 16 at a time; slowest: Night 21s, NightGuards 4s, NightTick 3s) / OK [ran] [tree 86241c47dcaf] (2026-10-31T16:27:02Z)
- (ac 3) `python3 plugin/tests/run.py test_night test_foresight 2>&1 | grep -v "ResourceWarning\|cur = open" | tail -40` → exit 0 · Ran 48 tests in 22.3s (14 classes, 16 at a time; slowest: Night 21s, NightGuards 4s, NightTick 3s) / OK [ran] [tree 86241c47dcaf] (2026-10-31T16:27:02Z)
- (step 2) `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 49 tests in 14.9s (14 classes, 16 at a time; slowest: Night 14s, NightGuards 3s, NightTick 3s) / OK [ran] [tree cddfa981765c] (2026-10-31T16:28:49Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_docs test_ecosystem test_foresight test_goal test_guard_cases test_night test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.59s] [ran] [tree cddfa981765c] (2026-10-31T16:29:31Z)
- (step 1) `python3 plugin/tests/run.py test_night test_foresight test_ecosystem` → exit 0 · Ran 68 tests in 35.7s (22 classes, 16 at a time; slowest: Night 35s, HarnessCanary 17s, NightGuards 7s) / OK [ran] [tree 2c76251b403c] (2026-10-31T17:56:11Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 49 tests in 12.2s (14 classes, 16 at a time; slowest: Night 12s, NightGuards 2s, NightTick 1s) / OK [ran] [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (ac 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 35 tests in 14.0s (11 classes, 16 at a time; slowest: Night 14s, NightGuards 3s, NightTick 3s) / OK [ran] [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (ac 3) `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 49 tests in 12.2s (14 classes, 16 at a time; slowest: Night 12s, NightGuards 2s, NightTick 1s) / OK [ran] [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (ac 4) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 35 tests in 14.0s (11 classes, 16 at a time; slowest: Night 14s, NightGuards 3s, NightTick 3s) / OK [ran] [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed in af7ed840 before merge; T-2352's gate passed it` → a model-free tick from the Stop sweep; CI and issues only where approved; timer staged by T-2357 [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed in af7ed840 before merge; T-2352's gate passed it` → issue text defanged and quoted, nothing runs from it; gh argv only for approved, pattern-matched repos [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed in af7ed840 before merge; T-2352's gate passed it` → corrupt tick.json, lock contention, a failed gh call, the daily cap [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed in af7ed840 before merge; T-2352's gate passed it` → routine polls are ledger events, not pending-user rows; fm decide --review lists them [tree 07dd4619cbf3] (2026-10-31T17:59:10Z)
## Log
- 2026-10-31T14:01:00Z created
- 2026-10-31T16:07:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2356.builder.md
- 2026-10-31T16:07:08Z builder slot freed
- 2026-10-31T16:11:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2356.builder.md
- 2026-10-31T16:11:01Z builder slot freed
- 2026-10-31T16:12:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2356.builder.md
- 2026-10-31T16:12:42Z focused
- 2026-10-31T16:12:43Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:15:36Z set scope=['plugin/lib/fmnight.py', 'plugin/lib/fmforesight.py', 'plugin/lib/fmeco.py', 'plugin/lib/fmorders.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_night.py', 'plugin/tests/test_foresight.py']
- 2026-10-31T16:15:37Z scope widened: tests (test_night), fmorders (trigger demotion), fmcli (--tick flag); fmeco/fmcost avoided: leased by T-2355/T-2351
- 2026-10-31T16:24:20Z steer: the tick timer is T-2357's; the tick runs from the Stop sweep until then
- 2026-10-31T17:54:03Z merged worktree-agent-a6276793f658a70dd (7 file(s))
- 2026-10-31T17:54:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6276793f658a70dd
- 2026-10-31T17:55:28Z focused
- 2026-10-31T17:56:39Z paused: focus moved to T-2433
- 2026-10-31T17:58:26Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T17:58:26Z focused
- 2026-10-31T17:58:36Z scope: files outside the globs came from merging foreman/build, fmeco (issue text defang, cap), fmcli cmd_decide (--review fetches), MASTER and the changelog line
- 2026-10-31T18:00:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261031-083838: Request: Mission 8, Genesis gen 1: 7. Self-repair and self-improvement. Its own failures, friction, misses and my corrections become fi…
- research mission-20261031-083838.pack: Mission 8, Genesis gen 1: 7. Self-repair and self-improvement. Its own failures, friction, misses and my corrections become fixes,…
- research mission-20261031-083834.pack: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skill or…
- decision 2026-10-30: [revisited: defer the full foreman-vs-plain exam] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_foresight.py, plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/lib/fmforesight.py, plugin/lib/fmnight.py, plugin/lib/fmorders.py, plugin/tests/test_night.py; re-ground the plan against them before editing
## Lessons
- Text from an outside tracker reaches model context through every field, not just the body: defang titles and labels too
## Plan gaps
- failed first: step 1 red tests: the three polls; nothing when sensitive or offline; the sweep runs it; injected issue te…
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmforesight.py
- plugin/lib/fmorders.py
- plugin/lib/fmnight.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/lib/fmeco.py
- CHANGELOG.md
