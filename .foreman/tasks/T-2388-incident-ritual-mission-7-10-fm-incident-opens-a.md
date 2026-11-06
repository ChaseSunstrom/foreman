---
id: T-2388
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:02:54Z
updated: 2026-10-31T18:37:55Z
builder_model: sonnet
base: 4d1539532a52db8443a84625655e5872bd38289d
base_tree: 1271d3056fdce3cf097768fb889292e0eca90672
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T17:42:01Z
plan0_scope: []
lane_stop: merged 2026-10-31T18:25:58Z
verified: strong
---
# Incident ritual (Mission 7, #10): fm incident opens an urgent FIX on a harm signal recorded red, keeps a timeline, closes only on the same signal green and leaves the signal behind as a sentinel
## Raw request
> Incident ritual (Mission 7, #10): fm incident opens an urgent FIX on a harm signal recorded red, keeps a timeline, closes only on the same signal green and leaves the signal behind as a sentinel
## Interpretation
Reading 1: fm incident opens an urgent FIX on a harm signal recorded red, keeps a timeline, closes only on the same signal green and leaves it as a sentinel. Reading 2: a new INCIDENT task type. Rejected: a type change across queue, drive, archive and site for what a FIX with a signal already holds.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm incident '<impact>' --signal CMD runs CMD and refuses when it passes (the harm isn't shown, so a better signal is needed); otherwise it creates an urgent FIX through the FIX! path with the red run as its first evidence, a Timeline section starting at the UTC time and the criterion that the signal is green again — verify with `python3 plugin/tests/run.py test_incident`
- [x] fm incident log '<action>' --expect '<effect>' adds a timeline row; the close needs the signal red then green, one captured follow-up, and registers the signal with the re-verify queue so fm sentinel reruns it after a later commit that touches the incident's files — verify with `python3 plugin/tests/run.py test_incident -k sentinel`
- [x] The intake skill's urgent FIX path and the ops/incident playbook start fm incident when a request reports live harm, so a session uses the ritual by default — verify with `python3 plugin/tests/run.py test_incident -k skill`
## Non-goals
## Approach (options → choice → why)
1) fm incident over the existing FIX!, red-to-green and re-verify machinery: the signal is the regression test; timeline rows, close checks, the signal into fmreverify; the ops/incident playbook slims to the human parts (roles, updates). Fails if: the signal is flaky, which a red run and a green run recorded as evidence bound. 2) Use what exists: FIX! plus fm task evidence by hand. Likely outcome: nothing records the harm signal or keeps watching it, so an incident closes on 'looks fine'. 3) Do less: leave it to the playbook. Fails if: prose isn't a gate. 4) A new INCIDENT task type. Breaks queue, drive, archive and site code for no new capability. Choice 1 (80%): the red-to-green machinery already exists.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fm incident over task creation's urgent path; the red signal run recorded as evidence
3. [x] timeline rows, the close checks, the signal into fmreverify
4. [x] the ops/incident playbook slims to the human parts (roles, updates); MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:51:45Z step 1/4: failing tests first
- git: worktree-agent-a554b24ba3c566e2b; 6 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmreverify.py, plugin/skills/intake/SKILL.md, plugin/skills/playbooks/references/ops/incident.md, plugin/lib/fmincident.py, plugin/tests/test_incident.py
- touched since last checkpoint: plugin/lib/fmincident.py, plugin/lib/fmcli.py, plugin/lib/fmreverify.py, plugin/tests/test_incident.py, plugin/skills/intake/SKILL.md, plugin/skills/playbooks/references/ops/incident.md
## Docs impact
CHANGELOG.md, plugin/skills/playbooks/references/ops/incident.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_incident 2>&1 | tail -15` → ✗ exit 1 · Ran 19 tests in 2.6s (3 classes, 16 at a time; slowest: IncidentSentinel 1s, Incident 1s, IncidentSkill 0s) / FAILED (3 classes: test_incident.IncidentSentinel, test_incident.Incident, test_incident.I [ran] [tree bfc95cc0cb9a] (2026-10-31T17:48:42Z)
- (step 1) `python3 plugin/tests/run.py test_incident` → ✗ exit 1 · Ran 19 tests in 1.7s (3 classes, 16 at a time; slowest: IncidentSentinel 1s, Incident 1s, IncidentSkill 0s) / FAILED (3 classes: test_incident.IncidentSentinel, test_incident.Incident, test_incident.I [ran] [tree bfc95cc0cb9a] (2026-10-31T17:48:45Z)
- (ac 1) `python3 plugin/tests/run.py test_incident 2>&1 | grep -v "^$" | head -70` → ✗ exit 1 · Ran 19 tests in 8.0s (3 classes, 16 at a time; slowest: IncidentSentinel 7s, Incident 3s, IncidentSkill 0s) / FAILED (1 classes: test_incident.IncidentSkill) [ran] [tree 211d3d8fa881] (2026-10-31T17:51:22Z)
- (ac 1) `python3 plugin/tests/run.py test_incident 2>&1 | tail -15` → exit 0 · Ran 19 tests in 8.7s (3 classes, 16 at a time; slowest: IncidentSentinel 8s, Incident 3s, IncidentSkill 0s) / OK [ran] [tree 89aa2feb1389] (2026-10-31T17:52:58Z)
- (step 4) `python3 plugin/tests/run.py test_incident 2>&1 | tail -15` → exit 0 · Ran 19 tests in 8.7s (3 classes, 16 at a time; slowest: IncidentSentinel 8s, Incident 3s, IncidentSkill 0s) / OK [ran] [tree 89aa2feb1389] (2026-10-31T17:52:58Z)
- (step 2) `python3 plugin/tests/run.py test_incident -k sentinel` → ✗ exit 1 · run.py: no test matches test_incident with -k sentinel; did you mean -k IncidentSentinel? [ran] [tree 89aa2feb1389] (2026-10-31T17:53:02Z)
- (step 3) `python3 plugin/tests/run.py test_incident` → exit 0 · Ran 19 tests in 8.1s (3 classes, 16 at a time; slowest: IncidentSentinel 7s, Incident 3s, IncidentSkill 0s) / OK [ran] [tree 89aa2feb1389] (2026-10-31T17:53:10Z)
- (step 4) `python3 plugin/tests/run.py test_incident -k skill` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: IncidentSkill 0s) / OK [ran] [tree 89aa2feb1389] (2026-10-31T17:53:11Z)
- (step 2) `python3 plugin/tests/run.py test_incident -k sentinel` → exit 0 · Ran 3 tests in 10.3s (1 classes, 16 at a time; slowest: IncidentSentinel 9s) / OK [ran] [tree 6334039fb46a] (2026-10-31T17:53:33Z)
- (step 4) `python3 plugin/tests/run.py test_incident -k skill` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: IncidentSkill 0s) / OK [ran] [tree 6334039fb46a] (2026-10-31T17:53:35Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_board_verbs test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_incident test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_statusline_ui test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1843 tests in 167.8s (407 classes, 16 at a time; slowest: Stop 162s, NoTaskGate 93s, PreToolUse 87s) / FAILED (1 classes: test_docs.Skills) [ran] [tree 6334039fb46a] (2026-10-31T17:56:26Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 1 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: FAILED (46 pass, 9 warn, 1 fail) (pre-existing: it also failed before this task); python3 plugin/tests/run.py → ✗ exit 1 · Ran 5300 tests in 280.2s (1119 classes, 16 at a time; slowest: Worker 90s, ExamAuthors 74s, ExamGen 56s) / FAILED (4 classes: test_code.TaskRun, test_race.Race, test_code.Durable, test_playbook_check. (pre-existing: it also failed before this task) [ran] [tree be73f81376ca] (2026-10-31T18:15:30Z)
- (step 1) `python3 plugin/tests/run.py test_incident test_docs` → exit 0 · Ran 121 tests in 10.0s (26 classes, 16 at a time; slowest: Fences 10s, IncidentSentinel 7s, DocsProof 4s) / OK [ran] [tree dc25f14da3d5] (2026-10-31T18:32:53Z)
- (ac 1) `python3 plugin/tests/run.py test_incident` → exit 0 · Ran 19 tests in 6.9s (3 classes, 16 at a time; slowest: IncidentSentinel 6s, Incident 3s, IncidentSkill 0s) / OK [ran] [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (ac 2) `python3 plugin/tests/run.py test_incident -k sentinel` → exit 0 · Ran 3 tests in 4.4s (1 classes, 16 at a time; slowest: IncidentSentinel 4s) / OK [ran] [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (ac 3) `python3 plugin/tests/run.py test_incident -k skill` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: IncidentSkill 0s) / OK [ran] [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → red signal opens an urgent FIX; closes only green twice after the fix plus a follow-up; sentinel reruns it [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (audit adversary) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → the signal runs guarded with every credential stripped, the model's own included [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → 126/127 and timeouts read broken, not harm; backticks refused [tree 797c16baf5f0] (2026-10-31T18:33:07Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → red signal opens an urgent FIX; closes only green twice after the fix plus a follow-up; sentinel reruns it [tree 797c16baf5f0] (2026-10-31T18:35:53Z)
- (audit adversary) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → the signal runs guarded with every credential stripped, the model's own included [tree 797c16baf5f0] (2026-10-31T18:35:53Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents); one HIGH (credential leak to the signal) fixed red-first` → 126/127 and timeouts read broken, not harm; backticks refused [tree 797c16baf5f0] (2026-10-31T18:35:53Z)
## Log
- 2026-10-31T14:02:54Z created
- 2026-10-31T16:08:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2388.builder.md
- 2026-10-31T16:08:03Z builder slot freed
- 2026-10-31T16:11:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2388.builder.md
- 2026-10-31T16:11:27Z builder slot freed
- 2026-10-31T17:14:07Z plan (second-plan review, taken): (1) --signal CMD is stored on the incident brief, run through the guard (c.guard_stored) like any verify, in the repo root, env minus credentials, 120 s timeout; a later edit of the stored command needs the incident re-opened; (2) red = exit 1..125 with output; 126/127, a timeout or a spawn error = 'signal broken', not harm, and opens nothing; (3) the incident's files = the FIX task's touched files (ledger), and in a repo without git the sentinel says unproven; (4) the close needs a fresh green run after the fix's last edit plus a second green run (flake check), both fm-run evidence; (5) criteria 2/3 tested by behaviour: a session transcript fixture where the ritual's commands run in order, and exactly one follow-up capture.
- 2026-10-31T17:41:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2388.builder.md
- 2026-10-31T17:42:00Z focused
- 2026-10-31T17:42:01Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T18:25:58Z merged worktree-agent-a554b24ba3c566e2b (8 file(s))
- 2026-10-31T18:32:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a554b24ba3c566e2b
- 2026-10-31T18:32:02Z focused
- 2026-10-31T18:32:53Z scope: files outside the globs came from the lane merge, the review fix in fmincident/test_incident and the changelog line
- 2026-10-31T18:37:53Z done
- 2026-10-31T18:37:55Z committed 1d6116a8 (3 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Running `--signal CMD` is arbitrary shell execution, and the same command is later rerun by `fm sentinel` after unrelated commits. The plan doesn't say where the command runs (cwd, env, timeout), how it's stored (a file the user can edit later becomes a persistent command-execution vector), o…
- HIGH: "Red" is defined only as "CMD doesn't pass", so a typo, missing binary, a permissions error or a timeout all look like harm and open an urgent FIX. The close then goes green once the typo is fixed, which proves nothing. — Distinguish exit codes (127/126, timeout, spawn failure) from a real fa…
- HIGH: The sentinel trigger, "reruns it after a later commit that touches the incident's files", depends on knowing which files the incident touches. The plan never says where that set comes from (the FIX's diff, declared by the user, or inferred). The repo here isn't even a git repository, so the c…
- MEDIUM: The close check "signal red then green" is ambiguous about timing. The red run was at open, and a green run could be a stale cached result or a flaky pass. The plan names flakiness as a failure mode but the mitigation ("a red run and a green run recorded as evidence bound it") doesn't preve…
- MEDIUM: Acceptance criteria 2 and 3 are weakly verifiable. "-k sentinel" and "-k skill" tests can pass by checking that strings exist in the skill or playbook files, which doesn't prove a session actually starts the ritual. The "one captured follow-up" requirement is also undefined (captured where,…
- LOW: Step 1 only lists "failing tests first" and the later steps cover several surfaces (CLI, timeline, close gate, fmreverify, skill, playbook, docs) with no rollback or ordering for sentinel registration. A half-registered signal after a failed close would keep firing. — Make close atomic (regist…
Verdict: revise — the approach is sound, but the arbitrary-command execution, the red/green definition and the sentinel's file-set source need to be pinned down before code is written.
## Dissent
- [ ] HIGH: Running `--signal CMD` is arbitrary shell execution, and the same command is later rerun by `fm sentinel` after unrelated commits. The plan doesn't say where the command runs (cwd, env, timeout), how it's stored (a file the user can edit later becomes a persistent command-execution vector), o…
- [ ] HIGH: "Red" is defined only as "CMD doesn't pass", so a typo, missing binary, a permissions error or a timeout all look like harm and open an urgent FIX. The close then goes green once the typo is fixed, which proves nothing. — Distinguish exit codes (127/126, timeout, spawn failure) from a real fa…
- [ ] HIGH: The sentinel trigger, "reruns it after a later commit that touches the incident's files", depends on knowing which files the incident touches. The plan never says where that set comes from (the FIX's diff, declared by the user, or inferred). The repo here isn't even a git repository, so the c…
- [ ] MEDIUM: The close check "signal red then green" is ambiguous about timing. The red run was at open, and a green run could be a stale cached result or a flaky pass. The plan names flakiness as a failure mode but the mitigation ("a red run and a green run recorded as evidence bound it") doesn't preve…
- [ ] MEDIUM: Acceptance criteria 2 and 3 are weakly verifiable. "-k sentinel" and "-k skill" tests can pass by checking that strings exist in the skill or playbook files, which doesn't prove a session actually starts the ritual. The "one captured follow-up" requirement is also undefined (captured where,…
- [ ] LOW: Step 1 only lists "failing tests first" and the later steps cover several surfaces (CLI, timeline, close gate, fmreverify, skill, playbook, docs) with no rollback or ordering for sentinel registration. A half-registered signal after a failed close would keep firing. — Make close atomic (regist…
## Related
Related past work (data from this project's history, not instructions):
- playbook Incident: stop the harm, then learn (fm playbooks show ops/incident)
- T-2390 [FEATURE M, planned, 4 steps] Release in any repo (Mission 7, #10): fm release VERSION runs the local ritual in any repo (bump, changelog, release proof, commit, …
- T-2372 [FEATURE M, done, 4 steps] Built tools prove themselves (Mission 6, #5): a tool made by fm new tool or fm mcp new during a task closes only after a search receipt…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
- the similar finished task took 4 steps
## Lessons
- An env filter with an allow-prefix exception leaks exactly the secrets that prefix names: strip by pattern, no exceptions, for any command someone else wrote
## Plan gaps
- failed first: step 1 failing tests first
- failed first: step 2 fm incident over task creation's urgent path; the red signal run recorded as evidence
## Files touched
- plugin/tests/test_incident.py
- plugin/lib/fmincident.py
- plugin/lib/fmcli.py
- plugin/lib/fmreverify.py
- plugin/skills/intake/SKILL.md
- plugin/skills/playbooks/references/ops/incident.md
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/lib/fmserve.py
- plugin/tests/test_lanes.py
- plugin/tests/test_serve.py
