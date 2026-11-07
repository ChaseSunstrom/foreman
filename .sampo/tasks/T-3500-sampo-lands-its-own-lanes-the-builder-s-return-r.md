---
id: T-3500
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T19:05:57Z
updated: 2026-11-07T03:41:35Z
lane: ~/.claude/foreman.lanes/T-3500
lane_branch: foreman/T-3500
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:19:58Z
plan0_scope: []
lane_passed: {"tree": "940d3e90c4e106d7f7e43312b7d0d01626912e1d", "cmds": ["python3 plugin/tests/run.py test_lane_land"]}
---
# Sampo lands its own lanes: the builder's return records the changelog line, lesson and numbers, and sampo lane land trains, closes, parks and ships with no hand-made scripts
## Raw request
> Sampo lands its own lanes: the builder's return records the changelog line, lesson and numbers, and sampo lane land trains, closes, parks and ships with no hand-made scripts
## Interpretation
Reading 1 (chosen): the close fields a builder already prints (CHANGELOG/TITLE/LESSON/NUMBERS, plus DOCS) are recorded on its brief at SubagentStop from its report, sampo task finish reads them when its flags are absent (lesson, numbers, docs; the CHANGELOG line is added under Unreleased), and sampo lane land does run_train2.sh + land.sh in-process: merge-tree pre-check, train in batches, lane rm + focus + finish each landed lane from its fields, park the rest with stop_mark, ship on an existing publish grant. Reading 2: a new sampo verb the builder must call to record its fields (rejected: one more command to remember, which is what the user asked to remove).
## Assumptions (confidence)
## Acceptance criteria
- [ ] a builder's return records its changelog line, title, lesson and numbers in its brief, and sampo lane land trains every finished lane in batches, closes each from its brief, parks the rest with the reason and ships after when publish is granted; the drive's line names sampo lane land when 2+ lanes wait and no land runs — verify with `python3 plugin/tests/run.py test_lane_land`
## Non-goals
Starting lane land from a hook in the background (optional in the request): a detached land would focus and close tasks in the checkout the session is working in; the drive line names the verb instead. Automating audits: land closes only lanes with recorded audits.
## Approach (options → choice → why)
1) parse the builder's report at SubagentStop into a Close fields brief section (free text, so a ' #' or a list-looking value survives, unlike meta); fails if: a builder omits the lines (then the lane is landed and named for a hand close) 2) use what exists: meta keys via sampo task set k=v; fails if: meta parsing drops ' #...' and reads [..] as lists 3) do less: only a land verb that takes a TSV like queue.tsv; fails if: the main session still retypes every column. Choice 1 (80%): the report is already written, so recording it costs the builder nothing; sampo task set --section 'Close fields' is the manual path. Land calls train.train and cli.main in-process (no subprocess), refuses while main has an active task, takes one flock, and never grants publish.
## Risks and rollback
## Execution prompt
## Steps
1. [x] brief fields for the close (changelog, title, lesson, numbers, docs) recorded at the builder's return and read by sampo task finish, test-first
2. [x] sampo lane land: train in batches, close each from its brief, park the rest with reasons
3. [x] the drive names sampo lane land when 2+ lanes wait; ship after when granted
4. [x] review fixes: Close fields provenance, sanitized title and changelog line, lane removed only after a clean finish, audits naming the lane tip
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_land` → ✗ exit 1 · Ran 10 tests in 50.8s (2 jobs, 16 at a time; slowest: Land 10s, CloseFields 2s) / FAILED (2 classes: test_lane_land.Land, test_lane_land.CloseFields) [ran] [tree ad799e963a88] [world 2f1906870a] (2026-11-06T19:25:08Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_land.CloseFields` → exit 0 · Ran 3 tests in 6.0s (1 jobs, 16 at a time; slowest: CloseFields 3s) / OK [ran] [tree 49f2856f7a41] [world 2f1906870a] (2026-11-06T19:26:51Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_lane_land.Land test_lane_train` → exit 0 · Ran 15 tests in 20.4s (15 jobs, 16 at a time; slowest: Land.test_land_trains_closes_each_from_its_brief_and_parks_the_rest 6s, Land.test_lanes_go_through_in_batches 5s, Land.test_it_ships_after_landin [ran] [tree 940d3e90c4e1] [world 2f1906870a] (2026-11-06T19:36:02Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_lane_land test_lanes` → exit 0 · Ran 216 tests in 34.5s (182 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, Land.test_lanes_go_through_in_batches 4s, CloseFields 4s) / OK [ran] [tree 940d3e90c4e1] [world 2f1906870a] (2026-11-06T19:36:41Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_lane_land` → ✗ exit 1 · Ran 14 tests in 2.4s (10 jobs, 16 at a time; slowest: Land.test_lanes_go_through_in_batches 2s, Land.test_it_ships_after_landing_on_a_grant_already_given_and_never_grants_one 2s, CloseFields 1s) / FAI [ran] [tree d70a2872be2b] [world 2f1906870a] (2026-11-06T19:58:23Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_lane_land test_lane_train test_lanes test_audit test_selfcheck` → exit 0 · Ran 278 tests in 30.2s (202 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, PostMergeVerify 9s, CloseFields 5s) / OK [ran] [tree 83d183ec58a7] [world 2f1906870a] (2026-11-06T20:01:13Z)
## Log
- 2026-11-06T19:05:57Z created
- 2026-11-06T19:06:16Z lane: ~/.claude/foreman.lanes/T-3500 on foreman/T-3500
- 2026-11-06T19:19:56Z focused
- 2026-11-06T19:19:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T19:20:29Z steer (user, 13:20: 'how come there still hasn't been a recent push to github with the latest trains'): the hand ship loop passed --test 'python3 plugin/tests/run.py -j 6', which never matches the gates' test, so T-3468's reuse never hit and each ship reran the suite (17 min) after a 15-min sleep; lane land must ship right after a train with the gates' own test
- 2026-11-06T22:26:58Z focused
- 2026-11-07T00:57:23Z focused
- 2026-11-07T03:41:35Z left out of a merge train: its merge turns the gates red: python3 plugin/tests/run.py on 187 affected test module(s), failing test_rename_scan.PluginIds
    -  'plugin/tests/test_lane_land.py:71:        for agent in ("foreman:fm-scout", '
    -  '"foreman:fm-recon", "Explore", "Plan", "foreman:fm-reviewer",',
    -  'plugin/tests/test_lane_land.py:72:                      '
    -  '"foreman:fm-debugger", "foreman:fm-reproducer", "code-reviewer"):'] : 4 lines write an old plugin namespace or id (sampo: and sampo@foreman now; a reader takes both via c.NAMESPACES): ['plugin/tests/test_lane_land.py:36:        r = self.hook("SubagentStop", {"agent_type": "foreman:fm-builder", "agent_id": "a1b2c3d4",', 'plugin/tests/test_lane_land.py:60:    def stop(self, tid, msg, agent="foreman:fm-builder"):', 'plugin/tests/test_lane_land.py:71:        for agent in ("foreman:fm-scout", "foreman:fm-recon", "Explore", "Plan", "foreman:fm-reviewer",', 'plugin/tests/test_lane_land.py:72:                      "foreman:fm-debugger", "foreman:fm-reproducer", "code-reviewer"):']
    
    ----------------------------------------------------------------------
    Ran 4 tests in 0.088s
    
    FAILED (failures=1)
    
      failed class: test_rename_scan.PluginIds
    
    Ran 5327 tests in 321.0s (2242 jobs, 16 at a time; slowest: Rendered 108s, LeanKindGateHookDelay 97s, LeanKindGateGuardAllow 77s)
    
    FAILED (1 classes: test_rename_scan.PluginIds)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3120 [PERFORMANCE S, done, 2 steps] sampo task finish reuses a full-gates pass on the same tree from any task when the only change since is CHANGELOG.md lines, rerunni…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-11-06: Post-merge suite back on (supersedes the pause): a close runs only its criteria and affected tests, not the full suite, so the post-merge run is the…
