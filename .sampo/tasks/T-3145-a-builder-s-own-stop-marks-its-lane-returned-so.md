---
id: T-3145
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-05T05:12:53Z
updated: 2026-11-05T05:28:34Z
base: 9bb63c17fb770e1f5c44063ed82b088c495eb852
base_tree: e2aa1b52f5b765deae47e743411805d726b141af
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T05:13:05Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# A builder's own stop marks its lane returned, so the builder cap frees the slot even when the launching session is still alive (T-3135 follow-up)
## Raw request
> A builder's own stop marks its lane returned, so the builder cap frees the slot even when the launching session is still alive (T-3135 follow-up)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] SubagentStop for a foreman:fm-builder whose agent id names a lane (.claude/worktrees/agent-<id>) sets that task's builder_returned; a SubagentStart for the same agent clears it; lane brief and the drive's slot count treat a returned lane as finished; on 2026-11-05 twelve lanes counted as working though seven builders had returned — verify with `python3 plugin/tests/run.py test_lanes test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a SubagentStop payload for an fm-builder marks its lane's task; the cap then lets a new brief through; SubagentStart clears it
2. [x] the mark in hooks.subagent_stop and subagent_start, the count in lanes.builder_brief and hooks.lanes_free
## Resume here
<!-- auto -->
- 2026-11-05T05:20:59Z step 1/2: failing tests: a SubagentStop payload for an fm-builder marks its lane's task; the cap then lets a new brief through; SubagentStart clears it
- git: foreman/build; 6 uncommitted: plugin/agents/fm-builder.md, plugin/lib/sampo/hooks.py, plugin/lib/sampo/lanes.py, plugin/tests/test_builder.py, plugin/tests/test_lanes.py, scripts/
- touched since last checkpoint: plugin/lib/sampo/lanes.py, plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 161 tests in 64.7s (14 classes, 16 at a time; slowest: Lanes 64s, LaneRecovery 43s, RaceEvidence 31s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree dd8eece16a66] [world 2f1906870a] (2026-11-05T05:18:12Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_builders_own_stop_frees_its_slot_while_the_launcher_lives` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 7f73260ca146] [world 2f1906870a] (2026-11-05T05:23:27Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_hooks` → exit 0 · Ran 419 tests in 77.0s (45 classes, 16 at a time; slowest: Stop 77s, Lanes 55s, NoTaskGate 52s) / OK [ran] [tree e70d86d59102] [world 2f1906870a] (2026-11-05T05:24:44Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_a_builders_own_stop_frees_its_slot_while_the_launcher_lives` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Lanes 1s) / FAILED (1 classes: test_lanes.Lanes) (start tree + this task's tests) [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:25:10Z)
- `python3 plugin/tests/run.py test_lanes.Lanes.test_a_builders_own_stop_frees_its_slot_while_the_launcher_lives` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:25:10Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_hooks` → exit 0 · Ran 419 tests in 57.7s (45 classes, 16 at a time; slowest: Stop 57s, Lanes 34s, NoTaskGate 33s) / OK [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:26:12Z)
- (audit edge) `self: the mark matches only foreman:fm-builder payloads whose agent id is a safe token and whose lane path ends in agent-<id>; it runs under the project lock and swallows its own errors so a hook never fails; the done sets in builder_brief and lanes_free union the mark with finished_lanes` → a non-builder agent, a malformed agent id or a lane named after its task leave every brief untouched; a restarted builder (SubagentStart) clears the mark so it holds a slot again [tree 39051bf1655c] (2026-11-05T05:26:12Z)
- (audit adversary) `self: the mark matches only foreman:fm-builder payloads whose agent id is a safe token and whose lane path ends in agent-<id>; it runs under the project lock and swallows its own errors so a hook never fails; the done sets in builder_brief and lanes_free union the mark with finished_lanes` → agent_id comes from the hook payload; the regex keeps it to [\w-]{4,64}, so it can't widen the endswith match to another lane [tree 39051bf1655c] (2026-11-05T05:26:12Z)
- (audit self) `self: the mark matches only foreman:fm-builder payloads whose agent id is a safe token and whose lane path ends in agent-<id>; it runs under the project lock and swallows its own errors so a hook never fails; the done sets in builder_brief and lanes_free union the mark with finished_lanes` → no findings [tree 39051bf1655c] (2026-11-05T05:26:12Z)
## Log
- 2026-11-05T05:12:53Z created
- 2026-11-05T05:13:01Z set approved=True
- 2026-11-05T05:13:01Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-11-05T05:13:02Z focused
- 2026-11-05T05:13:05Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T05:28:30Z done
- 2026-11-05T05:28:34Z committed ab6499d4 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1709 [FIX S, done, 2 steps] Lane friction: the drive counts the raised lane cap, an unused brief says how to free its slot, a gone worktree says how to merge — lesson:…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3135 [FIX S, done, 2 steps] The builder cap counts builders still working, not finished lanes waiting on a merge; unmerged finished lanes get their own larger cap, so …
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py
## Plan gaps
- failed first: step 1 failing tests: a SubagentStop payload for an fm-builder marks its lane's task; the cap then lets a …
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
