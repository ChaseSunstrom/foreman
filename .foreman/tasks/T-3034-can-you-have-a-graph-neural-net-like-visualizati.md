---
id: T-3034
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T23:44:44Z
updated: 2026-11-05T07:14:54Z
base_note: 
builder_model: haiku
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T23:46:10Z
plan0_scope: []
group: agent and model graph visualization
lane_branch: worktree-agent-a4f7803bf931750a2
base: c51a8108fbfb8427437080e3bdf3819d4a5fe922
base_tree: a738db8fb881dc6c9d4a1b1f8907222cfca88afa
lane_stop: refused 2026-11-05T06:57:50Z
verified: strong
unproven: [meaning]
---
# Can you have a graph/neural net like visualization mode for the different…
## Raw request
> can you have a graph/neural net like visualization mode for the different agents/models/tools working together? on the local/website? etc.? also keep going on genesiss while all of the otehr stuff is going, etc.
## Interpretation
Reading 1 (chosen): a second view mode on the live page (http://127.0.0.1:46459/), beside the forge scene: the same live snapshot drawn as a network, like a neural net. Agents (the session at the anvil, each builder lane, the machine's other live sessions) on the left, the tools and jobs they run (sampo verbs from the call log: moons grow, exam run, cards grow; running jobs: check, exam, grow) in the middle, the models (local on the GPU, Jarvis, Claude) on the right. Edges are the calls of the last minutes, their weight the call count; every new call fires a pulse along its edge in its kind's colour (write, judge, embed, train, plan, act, review); nodes glow with activity and dim when idle. A toggle in the header switches Forge and Network, kept in the URL hash (#view=net) and per viewer; same data, no new endpoint unless the graph needs a field the snapshot lacks. Reading 2 (ruled out for now): a separate page or a terminal (TUI) view; the website is what the user named first, the TUI can follow.
## Assumptions (confidence)
## Acceptance criteria
- [x] on the local website the page has a Forge/Network toggle (kept in #view=net and across reloads); the network view draws agents, tools/jobs and models from the snapshot fixtures as three columns with edges for the calls, a pulse travels an edge when a new call arrives, and switching views keeps the stream and the rail working — verify with `python3 plugin/tests/run.py test_live_page`
- [x] on the live service at desktop and phone the network view renders with no console errors and no sideways scroll, with reduced motion honoured (no pulses, edges light) — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
keep going on genesis while all of the other stuff is going: not this task's work; the genesis mandate's queue keeps running beside it (the user's standing ask)
## Approach (options → choice → why)
1) A hand-drawn canvas renderer in live.js reading the same snapshot: three layered columns with a gentle force relax inside each column, bezier synapses, pulses as travelling glows, depth (parallax and soft bloom) in the forge palette; reduced motion: no pulses, edges light instead. Likely outcome: a crafted, live neural-net look with no dependency. Fails if: many nodes crowd a column (cap and group the rest as '+N').
2) Use what exists: a graph library (d3-force, cytoscape). Likely outcome: layout for free. Fails if: the page loads nothing external (CSP default-src none, a test forbids external URLs) and vendoring a library is heavy.
3) Do less: draw lines over the forge scene between existing nodes. Fails if: it isn't the separate network view asked for.
Choice 1 (85%): the page already draws the forge scene by hand on a canvas from the same snapshot, so a second renderer is the same kind of code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing page tests: the toggle and hash, the three columns from fixtures, a pulse on a new call, reduced motion
2. [x] the network renderer and toggle in live.js/live.css/index.html, forge palette, crafted motion
3. [x] shots on the live service at desktop and phone, a cold design review, fix rounds
## Resume here
<!-- auto -->
- 2026-11-05T06:47:10Z steps 3/3 done
- git: worktree-agent-a4f7803bf931750a2; 0 uncommitted
## Docs impact
none: the live page's own legend explains the view; CHANGELOG had its line at merge
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 22 tests in 64.0s (2 classes, 16 at a time; slowest: Page 64s, Files 0s) / OK [ran] [tree a9e806059bb5] [world 2f1906870a] [rewound] (2026-11-05T00:04:34Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 70 tests in 66.5s (11 classes, 16 at a time; slowest: Page 66s, Serve 13s, Act 11s) / OK [ran] [tree a9e806059bb5] [world 2f1906870a] [rewound] (2026-11-05T00:05:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [11.91s] [ran] [tree a9e806059bb5] [world 2f1906870a] (2026-11-05T00:06:14Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · (no output) [ran] [tree 406c47ae209b] [world 2f1906870a] (2026-11-05T00:18:48Z)
- (ac 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · (no output) [ran] [tree 406c47ae209b] [world 2f1906870a] (2026-11-05T00:18:48Z)
- (step 3) `python3 plugin/tests/run.py test_live_page` → exit 0 · (no output) [ran] [tree 406c47ae209b] [world 2f1906870a] [rewound] (2026-11-05T00:18:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [47.68s] [ran] [tree 2fe7176d6cbd] [world 2f1906870a] (2026-11-05T00:27:06Z)
- `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 34 tests in 138.6s (2 classes, 16 at a time; slowest: Page 138s, Files 0s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T06:56:48Z)
- `sampo shot http://127.0.0.1:46459/#view=net --frames 2 --every 3000 --width 1280,390` → exit 0 · poster.png (frame-00.png: the most painted of 2) / note: still loading after 30 s; taken as it stood [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T06:57:45Z)
- (step 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 34 tests in 167.8s (2 classes, 16 at a time; slowest: Page 167s, Files 0s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:06:01Z)
- (step 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 34 tests in 200.2s (2 classes, 16 at a time; slowest: Page 200s, Files 0s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:09:37Z)
- (step 3) `sampo shot http://127.0.0.1:46459/#view=net --frames 2 --every 3000 --width 1280,390` → exit 0 · poster.png (frame-01.png: the most painted of 2) / note: still loading after 30 s; taken as it stood [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:14:39Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:09:37Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:14:50Z)
- (ac 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:09:37Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:14:50Z)
- (audit intent) `builder lane reviewed (37db4efa carried the review's fixes) and merged earlier; criteria re-run on main green (34 page tests); network view shot at 1280 and 390 on the live service: three columns, a live moon-grow edge to the model, the legend and the event strip` → the ask was a graph/neural-net view of agents, tools and models working together on the local site: a Network toggle beside the Forge, edges pulsing on calls [tree 9ff1569cf979] (2026-11-05T07:14:50Z)
- (audit edge) `builder lane reviewed (37db4efa carried the review's fixes) and merged earlier; criteria re-run on main green (34 page tests); network view shot at 1280 and 390 on the live service: three columns, a live moon-grow edge to the model, the legend and the event strip` → no running jobs shows the columns and legend with no edges; more agents than fit collapse into +N; reduced motion drops the pulses [tree 9ff1569cf979] (2026-11-05T07:14:50Z)
## Log
- 2026-11-04T23:44:44Z created
- 2026-11-04T23:45:36Z planned: it has criteria and steps
- 2026-11-04T23:45:37Z set approved=True
- 2026-11-04T23:45:49Z criterion 1 text: the page has a Forge/Network toggle (kept in #view=net and across reloads); the network view draws agents, tools/jobs and models from the snapshot fixtures as three columns with edges for the calls, a pulse travels an edge when a new call arrives, and switching views keeps the stream and the rail working → on the local website the page has a Forge/Network toggle (kept in #view=net and across reloads); the network view draws agents, tools/jobs and models from the snapshot fixtures as three columns with edges for the calls, a pulse travels an edge when a new call arrives, and switching views keeps the stream and the rail working
- 2026-11-04T23:45:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3034.builder.md
- 2026-11-04T23:46:09Z focused
- 2026-11-04T23:46:10Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:03:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae00d7256d46bcd7c (branch worktree-agent-ae00d7256d46bcd7c kept: not merged)
- 2026-11-05T03:08:30Z blocked: built (37db4efa, branch kept after a gate hold); in the merge queue behind T-3055, T-3083, T-3093, T-3087, T-3047
- 2026-11-05T05:19:19Z unblocked
- 2026-11-05T05:19:20Z lane: ~/.claude/foreman.lanes/T-3034 on foreman/T-3034
- 2026-11-05T05:19:38Z lane removed: ~/.claude/foreman.lanes/T-3034
- 2026-11-05T05:19:38Z already in main (37db4efa, the network view review); its re-created lane was empty and is removed; to close
- 2026-11-05T06:43:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3034.builder.md
- 2026-11-05T06:43:19Z focused
- 2026-11-05T06:48:25Z rewind: the working files (tree a738db8fb881) are back to before the proof of step(s) 1, 2, 3: reopened, their proofs kept as rewound
- 2026-11-05T06:51:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4f7803bf931750a2 (branch worktree-agent-a4f7803bf931750a2 kept: not merged)
- 2026-11-05T06:53:54Z focused
- 2026-11-05T07:14:54Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3024 [FEATURE M, planned, 3 steps] The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-pr…
- research live-schema: Server: `sampo live [--port N]`
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Lessons
- Check git log --grep ID before briefing a builder: a merged task waiting only on its close got a duplicate builder
## Files touched
- plugin/tests/test_live_page.py
- plugin/web/live/index.html
- plugin/web/live/live.css
- plugin/web/live/live.js
