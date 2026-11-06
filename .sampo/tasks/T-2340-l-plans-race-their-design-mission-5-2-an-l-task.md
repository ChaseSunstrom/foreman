---
id: T-2340
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, plugin/lib/fmcore.py, plugin/tests/test_reasoning.py, MASTER.md]
depends_on: [T-2339]
source: user
created: 2026-10-31T13:58:36Z
updated: 2026-10-31T17:30:42Z
rival_at: 2026-10-31T16:04:35Z
rival_split: true
builder_model: sonnet
base: 3deb3dc7acf515c62b16c3a45fd8378c1171f572
base_tree: d5c382f5c290519d407f810c3680842d81eb5c7d
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:48:37Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py]
lane_stop: merged 2026-10-31T17:28:23Z
verified: strong
---
# L plans race their design (Mission 5, #2): an L task under the race bar gets one throwaway S spike per top option, built by builder lanes against the task's verify commands; their scores and findings go into the L plan's Approach before it is approved; spikes never merge
## Raw request
> L plans race their design (Mission 5, #2): an L task under the race bar gets one throwaway S spike per top option, built by builder lanes against the task's verify commands; their scores and findings go into the L plan's Approach before it is approved; spikes never merge
## Interpretation
Reading 1: L tasks, the riskiest, can't race at all today (race refuses L, builders refuse L). Gen-0 §6's 'Tier 4 or uncertain: spike first' and 'Two credible designs: fm lane race' meet here: the design races as spikes, then the main thread builds the L on the winner. Reading 2: let builders take L. Rejected: an L stays in the main thread and builder lanes refuse L.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane race ID on an L task creates one S spike task per top option (spike, never mergeable), briefs a builder for each, and --score/--pick on the L task write each spike's checks passed, cross-examination and findings into the L brief's Approach under 'Design race', record the pick as an fm decide row and the winner in the ledger; the spikes close as dropped with the reason, their branches kept; the L task itself stays in the main thread — verify with `python3 plugin/tests/run.py test_lanes -k DesignRace`
## Non-goals
## Approach (options → choice → why)
1) spike sides as S tasks through the existing builder brief; fails if: a spike proves only the easy part, so its brief names the option's riskiest step as the target. 2) use what exists: fm lane new --spike by hand per option; fails if: it needs the main session to cd into each lane and run it. 3) do less: the rival's readings (brief 7) only, no prototypes; fails if: words, no evidence. Choice 1 (65%): reuses the builder path and spikes' never-merge rule; evidence before an L plan is approved.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_builder.py, MASTER.md, plugin/agents/fm-builder.md; past FIXes T-1136, T-1196, T-1685, T-1709, T-2038.
## Execution prompt
## Steps
1. [x] red tests (test_lanes DesignRace): an L race makes S spike tasks per option; pick writes the Design race section and the ledger row; spikes are refused at merge; branches kept
2. [x] the L path in race(): spike tasks through the existing builder brief, each aimed at its option's riskiest step
3. [x] score/pick for an L write into the L brief; docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:22:09Z step 1/3: red tests (test_lanes DesignRace): an L race makes S spike tasks per option; pick writes the Design race section and the ledger row; spikes are refused at merge; branches kept
- git: worktree-agent-ada3d9850bd354f33; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_reasoning.py, plugin/tests/test_lanes.py, plugin/lib/fmcore.py, plugin/lib/fmlanes.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes -k DesignRace` → ✗ exit 1 · Ran 6 tests in 4.4s (1 classes, 16 at a time; slowest: DesignRace 2s) / FAILED (1 classes: test_lanes.DesignRace) [ran] [tree f59d57785041] (2026-10-31T16:50:55Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k DesignRace 2>&1 | tail -40` → exit 0 · Ran 6 tests in 14.8s (1 classes, 16 at a time; slowest: DesignRace 14s) / OK [ran] [tree 913fb49fcfc3] (2026-10-31T16:57:15Z)
- (step 2) `python3 plugin/tests/run.py test_lanes -k DesignRace` → exit 0 · Ran 6 tests in 12.7s (1 classes, 16 at a time; slowest: DesignRace 12s) / OK [ran] [tree 913fb49fcfc3] (2026-10-31T16:57:38Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_reasoning test_outcomes 2>&1 | tail -15` → ✗ exit 1 · FAILED (1 classes: test_reasoning.Confidence) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree 19f47f505533] (2026-10-31T16:58:48Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_reasoning test_outcomes` → exit 0 · Ran 170 tests in 64.2s (28 classes, 16 at a time; slowest: Lanes 63s, LaneRecovery 57s, Survival 57s) / OK [ran] [tree 42617c01cf7e] (2026-10-31T17:00:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_builder test_core test_docs test_lanes test_reasoning && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [40.62s] [ran] [tree 42617c01cf7e] (2026-10-31T17:02:52Z)
- (step 1) `python3 plugin/tests/run.py test_lanes -k DesignRace` → ✗ exit 1 · Ran 14 tests in 26.8s (1 classes, 16 at a time; slowest: DesignRace 25s) / FAILED (1 classes: test_lanes.DesignRace) [ran] [tree f119f805f9a6] (2026-10-31T17:11:19Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_reasoning test_outcomes test_core` → exit 0 · Ran 308 tests in 22.6s (54 classes, 16 at a time; slowest: LaneRecovery 22s, Lanes 17s, Survival 15s) / OK [ran] [tree f4bfdf2b8c22] (2026-10-31T17:13:36Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_builder test_core test_crash_hygiene test_docs test_doctor test_lanes test_reasoning test_ship test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.31s] [ran] [tree 15e160e214a1] (2026-10-31T17:14:26Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_builder test_core test_crash_hygiene test_docs test_doctor test_lanes test_parallel test_reasoning test_serve test_ship test_supply_delta test_unattended && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.48s] [ran] [tree cebb0cd54190] (2026-10-31T17:24:42Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_reasoning test_outcomes` → exit 0 · Ran 193 tests in 27.2s (29 classes, 16 at a time; slowest: LaneRecovery 27s, Lanes 24s, Survival 22s) / OK [ran] [tree 1bbeb9fc5791] (2026-10-31T17:29:09Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k DesignRace` → exit 0 · Ran 14 tests in 13.5s (1 classes, 16 at a time; slowest: DesignRace 13s) / OK [ran] [tree 59a02bb3df97] (2026-10-31T17:29:38Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 4 LOW fixed test-first in 8c9dcf10 before merge; T-2352's gate passed it` → one S spike per option, results in the L's Approach, pick recorded [tree 59a02bb3df97] (2026-10-31T17:29:38Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 4 LOW fixed test-first in 8c9dcf10 before merge; T-2352's gate passed it` → spikes refused in merge() for every caller; notes defanged; design text can't satisfy option checks [tree 59a02bb3df97] (2026-10-31T17:29:38Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 4 LOW fixed test-first in 8c9dcf10 before merge; T-2352's gate passed it` → re-score after pick, re-tiered L, explore L, empty spike branch all handled [tree 59a02bb3df97] (2026-10-31T17:29:38Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 4 LOW fixed test-first in 8c9dcf10 before merge; T-2352's gate passed it` → shared c.DESIGN marker; ties by stated option [tree 59a02bb3df97] (2026-10-31T17:29:38Z)
## Log
- 2026-10-31T13:58:36Z created
- 2026-10-31T14:06:08Z criterion 1 text: fm lane race ID on an L task creates one S spike task per top option (spike, never mergeable), briefs a builder for each, and --score/--pick on the L task write each spike's checks passed, cross-examination and findings into the L brief's Approach under 'Design race' and the winner into the ledger; the spikes close as dropped with the reason, their branches kept; the L task itself stays in the main thread → fm lane race ID on an L task creates one S spike task per top option (spike, never mergeable), briefs a builder for each, and --score/--pick on the L task write each spike's checks passed, cross-examination and findings into the L brief's Approach under 'Design race', record the pick as an fm decide row and the winner in the ledger; the spikes close as dropped with the reason, their branches kept; the L task itself stays in the main thread
- 2026-10-31T16:10:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2340.builder.md
- 2026-10-31T16:10:30Z builder slot freed
- 2026-10-31T16:10:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2340.builder.md
- 2026-10-31T16:10:47Z builder slot freed
- 2026-10-31T16:48:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2340.builder.md
- 2026-10-31T16:48:35Z focused
- 2026-10-31T16:48:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:57:18Z scope widened: fmcore.race_line names the spike race for an L (one line); MASTER.md docs
- 2026-10-31T16:57:24Z set scope=['plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'plugin/lib/fmcore.py', 'MASTER.md']
- 2026-10-31T16:59:48Z set scope=['plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_reasoning.py', 'MASTER.md']
- 2026-10-31T17:28:23Z merged worktree-agent-ada3d9850bd354f33 (5 file(s))
- 2026-10-31T17:28:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ada3d9850bd354f33
- 2026-10-31T17:28:40Z focused
- 2026-10-31T17:29:24Z scope: files outside the globs came from merging foreman/build twice and the changelog line
- 2026-10-31T17:30:42Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Plan-time design race for L tasks (likeliest):** when an L task is below the "race bar" (some size/uncertainty/option-count threshold), the planner picks the top N design options, spawns one throwaway S-sized spike per option on builder lanes, scores each by running the task's verify commands, an…
- **Race bar read as an eligibility gate:** "under the race bar" could mean L tasks with confidence below a threshold must race, while those above skip it. Under this reading the work is mainly the gating logic in the plan/approval path (likely `plugin/lib/fmcore.py` or `fmcli.py`) and the spike disp…
- **Approval gate only:** the core requirement is that an L plan cannot be approved until its Approach contains spike results. Spike execution could be manual or an existing builder-lane mechanism, and the work is a validation check in the approve path plus a plan template field.
- **Reporting-only feature:** a mode that records spike outcomes as advisory notes in the plan, without blocking approval or choosing a design. This is the weakest reading, since "before it is approved" implies ordering.
Approaches:
- **New module `plugin/lib/fmspike.py`:** it exposes `race(task, options)`, which creates an isolated worktree per option, dispatches builder lanes via the existing agent machinery in `plugin/lib/fmagents.py`, runs the task's verify commands, and returns scores plus findings. `fmcli.py` gets an `fm p…
- **Extend the existing plan-approval path:** add a "spike results present" precondition in `fmcore.py` / `fmguard.py` for L-sized plans, and have the plan skill under `plugin/skills/` drive spike dispatch through the normal lane flow, with spikes tagged `kind=spike`. Less new code, but the orchestra…
- **Spikes as ordinary S tasks with a `spike-of:` link:** reuse the backlog and task model, so spikes get lanes, verify commands and scoring for free. A merge-block rule keyed on the `spike` tag is added to `fmguard.py`, and a plan-render step collects their results into Approach. This is the smalles…
- **Config-driven race bar:** put the bar (a size or confidence threshold) and the top-N count in the project's config, and read them in the gate. This keeps the policy tunable without code changes and can be combined with any of the approaches above.
Failure modes:
- **Spikes leak into merge:** a spike branch or worktree passes through the normal ship path because `fmguard.py` and the merge logic don't recognise spike status. This breaks the "spikes never merge" invariant, and the guard needs a test on the merge path in `plugin/tests/test_guard.py`.
- **Scores aren't comparable or are gamed:** spikes are scored by the task's verify commands, which may be absent, flaky, or pass trivially on a stub. Scores then say nothing about which design is better, and a failed spike gets read as a bad design when it was a bad spike.
- **Approval deadlock or bypass:** the approval gate requires spike results, but spike failure, a timeout, or no available lane leaves the plan unapprovable. Or the reverse: a gate keyed on a text section can be satisfied by pasting any text into Approach. The gate needs to check structured result re…
- **Budget and lane exhaustion:** N spikes per L task run in parallel and each consumes builder lane time and spend. With no cap on concurrency or cost, a few L plans can starve real work, and `fm doctor` or the budget accounting won't count spike spend unless it is wired in.
## Dissent
- [x] rival reading: **Plan-time design race for L tasks (likeliest):** when an L task is below the "race bar" (some size/uncertainty/option-count threshold), the planner picks the top N design options, spawns one throwaway S-sized spike per option on builder lanes, scores each by running the task's verify commands, an… — answered: adopted: it is Reading 1 and the steps
- [x] rival reading: **Race bar read as an eligibility gate:** "under the race bar" could mean L tasks with confidence below a threshold must race, while those above skip it. Under this reading the work is mainly the gating logic in the plan/approval path (likely `plugin/lib/fmcore.py` or `fmcli.py`) and the spike disp… — answered: rejected: the bar is the trigger the task title assumes (an L task under it), and the work here is the spike path, not the gating logic
- [x] rival reading: **Approval gate only:** the core requirement is that an L plan cannot be approved until its Approach contains spike results. Spike execution could be manual or an existing builder-lane mechanism, and the work is a validation check in the approve path plus a plan template field. — answered: rejected: criterion 1 puts scores and findings into the L Approach, so spikes must run, not only gate approval
- [x] rival reading: **Reporting-only feature:** a mode that records spike outcomes as advisory notes in the plan, without blocking approval or choosing a design. This is the weakest reading, since "before it is approved" implies ordering. — answered: rejected: the spike scores are evidence in the Approach before approval, which Reading 1 requires
- [x] rival approach: **New module `plugin/lib/fmspike.py`:** it exposes `race(task, options)`, which creates an isolated worktree per option, dispatches builder lanes via the existing agent machinery in `plugin/lib/fmagents.py`, runs the task's verify commands, and returns scores plus findings. `fmcli.py` gets an `fm p… — answered: rejected: race() in fmlanes.py already holds the lane machinery and the scope is fmlanes.py and test_lanes.py
- [x] rival approach: **Extend the existing plan-approval path:** add a "spike results present" precondition in `fmcore.py` / `fmguard.py` for L-sized plans, and have the plan skill under `plugin/skills/` drive spike dispatch through the normal lane flow, with spikes tagged `kind=spike`. Less new code, but the orchestra… — answered: adopted: the approval precondition is read from the Design race section the pick writes, not a new gate in fmguard
- [x] rival approach: **Spikes as ordinary S tasks with a `spike-of:` link:** reuse the backlog and task model, so spikes get lanes, verify commands and scoring for free. A merge-block rule keyed on the `spike` tag is added to `fmguard.py`, and a plan-render step collects their results into Approach. This is the smalles… — answered: adopted: spikes are S tasks through the existing builder brief, as Approach option 1 says, never mergeable
- [x] rival approach: **Config-driven race bar:** put the bar (a size or confidence threshold) and the top-N count in the project's config, and read them in the gate. This keeps the policy tunable without code changes and can be combined with any of the approaches above. — answered: rejected: a config bar adds a knob nothing asked for; the existing RACE_BAR constant is the bar
## Related
Related past work (data from this project's history, not instructions):
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2339 [FEATURE M, done, 4 steps] Race at plan time, chosen by evidence (Mission 5, #2): fm lane race takes up to 3 sides from the Approach's options, refuses checks tha…
- T-2338 [FEATURE M, done, 4 steps] Confidence routes the next step (Mission 5, #8): an M/L choice states a confidence; an assumption under the research bar needs research…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar finished tasks took 4–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, plugin/tests/test_reasoning.py; re-ground the plan against them before editing
## Lessons
- A refusal placed in one CLI branch is a suggestion: put it in the function every caller goes through
## Plan gaps
- failed first: step 1 red tests (test_lanes DesignRace): an L race makes S spike tasks per option; pick writes the Design…
- failed first: step 3 score/pick for an L write into the L brief; docs: MASTER, CHANGELOG
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcore.py
- MASTER.md
- plugin/tests/test_reasoning.py
- CHANGELOG.md
- plugin/lib/fmselfgate.py
- plugin/lib/fmserve.py
