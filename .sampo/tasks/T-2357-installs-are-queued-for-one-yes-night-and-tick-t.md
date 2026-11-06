---
id: T-2357
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmguard.py, plugin/lib/fmdoctor.py]
depends_on: [T-2374, T-2356]
source: user
created: 2026-10-31T14:01:01Z
updated: 2026-10-31T21:59:01Z
builder_model: sonnet
door_seen: [061176cb2621]
base: 15175702b7b0b7219f9d99bdded2457651cd7405
base_tree: c42010247bbee71c3995b349b6fe1a7b4db79536
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T21:47:34Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmguard.py, plugin/lib/fmdoctor.py]
verified: strong
---
# Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11)
## Raw request
> Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11)
## Interpretation
Reading 1: fm night --install stages the unit files in state, records one fm ask, and installs only after the user's yes; the guard classifies it as system (gap map #11 install queue). Reading 2: install the timers directly and tell the user. Rejected: gen-0 #11 says installs are queued for one yes and NEVER grant yourself anything, and a Python install path would bypass the guard, which sees only the fm command.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm night --stage (on the active task or --task ID) writes the nightly fm night and hourly fm night --tick units, plus a crontab fallback, into state as staged files and queues one install grant (fmgrants, category plugin) naming each unit, its schedule, its budget and how to remove it, and, each as its own line, the GitHub issue watch (--watch-issues OWNER/REPO) and the CI check when no session is open (--watch-ci); nothing is written outside state — verify with `python3 plugin/tests/run.py test_serve -k night`
- [x] The guard classifies fm night --install as plugin (user-only; system is grantable by fm task set --allow), so only the user's yes passes it; --install installs the staged units, enables the timers, turns on the issue watch and CI check only for the lines that were staged and asked, and records them; fm night --uninstall disables and removes them — verify with `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp`
- [x] fm doctor names staged units waiting for the yes and installed units pointing at another Foreman home; --print-timer is removed — verify with `python3 plugin/tests/run.py test_doctor test_serve -k night`
## Non-goals
## Approach (options → choice → why)
1) Stage then ask: fm night --install with no grant writes the units (nightly fm night, hourly fm night --tick) into state as staged files and records one ask (fm ask ID system: each unit, when it runs, its budget, how to remove it); the guard classifies the command as system so only the user's yes passes it; after the yes it installs and enables them; fm night --uninstall removes them; --print-timer goes. Fails if: staging writes outside state, which a test pins. 2) Use what exists: fm night --print-timer, whose unit the user pastes by hand. Likely outcome: today's state, nothing stages, asks or tracks it, so work never starts without a session. 3) Do less: cron only, no systemd units. Fails if: a laptop asleep at the hour misses the run, which systemd's Persistent= catches. Cron stays the fallback where systemd --user is absent. Choice 1 (85%): it is the only option that is both automatic and a user-only grant.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md, plugin/tests/test_doctor.py, plugin/lib/fmcli.py; past FIXes T-0859, T-0892, T-0921, T-0928, T-0951.
## Execution prompt
## Steps
1. [x] red tests: staging stays inside the project's own folder; the plugin category; install after the yes; the undo; doctor lines
2. [x] staging and install in fmnight; the guard line (protected core: candidate plus fm ask core)
3. [x] docs: MASTER, README setup, CHANGELOG
## Resume here
## Docs impact
README (night timers line), MASTER (fmnight T-2357), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_serve test_guard -k night` → ✗ exit 1 · Ran 3 tests in 1.7s (2 classes, 16 at a time; slowest: GuardCases 1s, NightInstall 1s) / FAILED (1 classes: test_serve.NightInstall) [ran] [tree 024dd6bf2958] (2026-10-31T21:48:17Z)
- (step 1) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → ✗ exit 1 · Ran 7 tests in 2.6s (3 classes, 16 at a time; slowest: NightInstall 2s, GuardCases 1s, PluginChanges 0s) / FAILED (2 classes: test_serve.NightInstall, test_guard.PluginChanges) [ran] [tree 1e13ce12ce98] (2026-10-31T21:48:36Z)
- (ac 2) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp 2>&1 | grep -E "^(FAIL|ERROR):|Error|assert|^OK|FAILED" | head -10` → exit 0 · OK [ran] [tree 8c194206b54a] (2026-10-31T21:49:43Z)
- (step 1) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → exit 0 · Ran 7 tests in 3.5s (3 classes, 16 at a time; slowest: NightInstall 3s, GuardCases 1s, PluginChanges 0s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:03Z)
- (step 2) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → exit 0 · Ran 7 tests in 3.4s (3 classes, 16 at a time; slowest: NightInstall 3s, GuardCases 1s, PluginChanges 0s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:07Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 10.1s (24 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, TaskLifecycle 2s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:18Z)
- (ac 1) `python3 plugin/tests/run.py test_serve -k night` → exit 0 · Ran 4 tests in 3.2s (1 classes, 16 at a time; slowest: NightInstall 3s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:22Z)
- (ac 2) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → exit 0 · Ran 7 tests in 3.5s (3 classes, 16 at a time; slowest: NightInstall 3s, GuardCases 1s, PluginChanges 0s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:26Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor test_serve -k night` → ✗ exit 1 · run.py: no test matches test_doctor with -k night [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:27Z)
- `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → ✗ exit 1 · Ran 7 tests in 3.6s (3 classes, 16 at a time; slowest: NightInstall 2s, GuardCases 1s, PluginChanges 0s) / FAILED (2 classes: test_serve.NightInstall, test_guard.PluginChanges) (start tree + this task's tests) [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:35Z)
- `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → exit 0 · Ran 7 tests in 3.6s (3 classes, 16 at a time; slowest: NightInstall 3s, GuardCases 1s, PluginChanges 0s) / OK [ran] [tree 4731f92eaf0d] (2026-10-31T21:51:35Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor test_serve -k night` → exit 0 · Ran 5 tests in 3.9s (2 classes, 16 at a time; slowest: NightInstall 3s, NightTimers 2s) / OK [ran] [tree be4ca2aae912] (2026-10-31T21:52:13Z)
- (ac 1) `python3 plugin/tests/run.py test_serve -k night` → exit 0 · Ran 4 tests in 2.1s (1 classes, 16 at a time; slowest: NightInstall 2s) / OK [ran] [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (ac 2) `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp` → exit 0 · Ran 7 tests in 2.1s (3 classes, 16 at a time; slowest: NightInstall 2s, GuardCases 1s, PluginChanges 0s) / OK [ran] [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor test_serve -k night` → exit 0 · Ran 5 tests in 2.1s (2 classes, 16 at a time; slowest: NightInstall 2s, NightTimers 1s) / OK [ran] [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green incl. fm replay (124 labelled guard cases, 0 drifted)` → --stage writes only state and queues one plugin request naming each line (nightly, hourly, budget, undo, issue watch, CI); --install after the yes; --uninstall; doctor rows; --print-timer gone [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green incl. fm replay (124 labelled guard cases, 0 drifted)` → fm night --install (and abbreviations) is plugin, a user-only category, so fm task set --allow can't self-grant it; quiet/at wrappers are rechecked by the existing recursion; a project path with a control character writes no unit, and % is escaped for systemd specifiers; watch lines come only from the staged plan, repos re-matched against OWNER/REPO [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green incl. fm replay (124 labelled guard cases, 0 drifted)` → re-staging the same plan dedupes on its hash; --install with nothing staged stages the defaults; no systemctl refuses and names the staged crontab lines; uninstall without systemd still removes the files [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
- (audit operator) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green incl. fm replay (124 labelled guard cases, 0 drifted)` → fm doctor names timers staged and waiting, and installed units whose FOREMAN_HOME is another home [tree 38ccdc5e37ea] (2026-10-31T21:58:19Z)
## Log
- 2026-10-31T14:01:01Z created
- 2026-10-31T16:07:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2357.builder.md
- 2026-10-31T16:07:11Z builder slot freed
- 2026-10-31T16:11:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2357.builder.md
- 2026-10-31T16:11:03Z builder slot freed
- 2026-10-31T17:11:33Z set depends_on=['T-2374', 'T-2356']
- 2026-10-31T21:32:51Z criterion 1 verify: `python3 plugin/tests/run.py test_night` → `python3 plugin/tests/run.py test_serve -k night`
- 2026-10-31T21:32:51Z criterion 1 text: fm night --install with no grant writes the nightly and hourly units into state as staged files and records one system ask naming each unit, its schedule, its budget, how to remove it, and, each as its own line, the repo's GitHub issue watch and the CI check when no session is open; nothing is written under ~/.config/systemd or to crontab → fm night --stage (on the active task or --task ID) writes the nightly fm night and hourly fm night --tick units, plus a crontab fallback, into state as staged files and queues one install grant (fmgrants, category plugin) naming each unit, its schedule, its budget and how to remove it, and, each as its own line, the GitHub issue watch (--watch-issues OWNER/REPO) and the CI check when no session is open (--watch-ci); nothing is written outside state
- 2026-10-31T21:32:51Z criterion 2 verify: `python3 plugin/tests/run.py test_night test_guard` → `python3 plugin/tests/run.py test_serve test_guard -k night`
- 2026-10-31T21:32:51Z criterion 2 text: The guard classifies fm night --install as system, so only the user's yes passes it; after the yes it installs and enables the units, turns on the issue watch only if that line was approved, and records them; fm night --uninstall removes them → The guard classifies fm night --install as plugin (user-only; system is grantable by fm task set --allow), so only the user's yes passes it; --install installs the staged units, enables the timers, turns on the issue watch and CI check only for the lines that were staged and asked, and records them; fm night --uninstall disables and removes them
- 2026-10-31T21:32:51Z criterion 3 verify: `python3 plugin/tests/run.py test_doctor test_night` → `python3 plugin/tests/run.py test_doctor test_serve -k night`
- 2026-10-31T21:32:51Z steer: category plugin, not system: system is self-grantable through fm task set --allow under full autonomy, and the AC asks that only the user's yes passes; staging is its own flag (--stage) because a guarded --install never runs to stage
- 2026-10-31T21:47:31Z step 1 text: red tests: staging writes nothing outside state; guard category; install after the yes; uninstall; doctor lines → red tests: staging stays inside the project's own folder; the plugin category; install after the yes; the undo; doctor lines
- 2026-10-31T21:47:33Z focused
- 2026-10-31T21:47:34Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T21:48:14Z scope: tests in plugin/tests/test_serve.py (its systemctl stub and temp HOME) and test_guard.py; the --print-timer test there goes with the flag; docs README, MASTER, CHANGELOG; fmcli.py for the flags
- 2026-10-31T21:48:32Z criterion 2 verify: `python3 plugin/tests/run.py test_serve test_guard -k night` → `python3 plugin/tests/run.py test_serve test_guard -k night -k plugin_mcp`
- 2026-10-31T21:52:13Z scope: plugin/tests/test_doctor.py NightTimers pins the doctor row; README, MASTER, CHANGELOG; fmcli.py flags; test_night.py drops the stale print_timer arg
- 2026-10-31T21:58:59Z done
- 2026-10-31T21:59:01Z committed b34fa629 (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_guard.py, plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmdoctor.py, plugin/lib/fmguard.py, plugin/lib/fmnight.py; re-ground the plan against them before editing
## Lessons
- A guarded install verb can't stage itself (the guard stops it first): stage under its own unguarded flag that writes state only, and guard the install under a user-only category; system is self-grantable through fm task set --allow
## Plan gaps
- failed first: step 1 red tests: staging stays inside the project's own folder; the plugin category; install after the ye…
## Files touched
- plugin/tests/test_serve.py
- plugin/tests/test_guard.py
- plugin/lib/fmnight.py
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- plugin/lib/fmdoctor.py
- README.md
- plugin/tests/test_night.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_doctor.py
