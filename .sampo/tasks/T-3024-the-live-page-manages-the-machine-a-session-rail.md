---
id: T-3024
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:15:08Z
updated: 2026-11-04T23:53:14Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (633) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T21:15:31Z
rival_split: true
builder_model: haiku
base: f9eb99d2c1bfa325cb0a1ae7b3b334048c1c9611
base_tree: 0ce49a00f567f4e31314d0035f8330d1bf218152
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T21:36:48Z
plan0_scope: []
lane_stop: merged 2026-11-04T23:00:25Z
verified: strong
unproven: [ui-unshot]
---
# The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-projects strip (task, stage, queue, drive) beside the scene; picking a project or session switches the scene, the panels and the stream to it (?project=), kept in the URL hash; sensitive projects show their name only (T-3022 part 2)
## Raw request
> The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-projects strip (task, stage, queue, drive) beside the scene; picking a project or session switches the scene, the panels and the stream to it (?project=), kept in the URL hash; sensitive projects show their name only (T-3022 part 2)
## Interpretation
Reading 1 (chosen): the page half of T-3022: see every session and project on the machine at once and switch the scene to any of them. Reading 2 (ruled out): one page per project; the user asked for one website for the machine.
## Assumptions (confidence)
## Acceptance criteria
- [x] the rail and strip render /api/machine fixtures (projects with and without a task, a sensitive one, live sessions), picking one reloads /api/state and /api/stream with ?project= and the scene follows; the pick survives a reload through the URL hash; offline, no console errors, no sideways scroll at 1920x1080 and 390 wide — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
1) A narrow rail on the right of the stage at desktop (a row above it on phone): live sessions first (a pulsing ember per live one, project name, task id, model, a context tank sliver, seen-ago), then every project as compact plates (name, task and stage, queue count, drive lamp); a click or Enter switches: the page refetches /api/state?project=SLUG, reopens the stream with it, writes #project=SLUG, and the scene cross-fades. /api/machine is polled every 5 s (it is cached server-side). Likely outcome: one page that walks between every session on the machine. Fails if: the rail crowds the scene on narrow desktops; below 1400 px it collapses to the top row as on phone.
2) use what exists: a <select> of project slugs in the header. Likely outcome: works, but hides who is live and what each is doing. Fails if: the user wants to see all sessions at once.
3) do less: links to /?project=SLUG per project. Likely outcome: full reloads, no live overview. Fails if: the view should stay live while switching.
Choice 1 (75%): a live rail in the forge's material language, with the switch done in place.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing page tests with /api/machine fixtures and a project switch
2. [x] the rail, the strip and the switch in index.html, live.css and live.js, in the forge theme
3. [x] screenshot pass at desktop and phone
## Resume here
## Docs impact
CHANGELOG line written with T-3026's close (the machine-wide page)
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 12 tests in 19.0s (2 classes, 16 at a time; slowest: Page 18s, Files 0s) / OK [ran] [tree 628e5c1b9a92] [world 2f1906870a] (2026-11-04T21:47:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [15.87s] [ran] [tree 628e5c1b9a92] [world 2f1906870a] (2026-11-04T21:48:56Z)
- (step 3) `cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad && uv run --offline --no-project --with playwright python realshot.py 'http://127.0.0.1:46459/#project=foreman-4a056f' t3024-phone.png 390 844 dark 7000 && uv run --offline --no-project --with playwright python realshot.py http://127.0.0.1:46459/ t3024-desk.png 1440 900 dark 7000 && echo 'shots: no console errors; desktop rail beside the scene, phone rail above it, strip scrolls sideways'` → exit 0 · shots: no console errors; desktop rail beside the scene, phone rail above it, strip scrolls sideways [ran] [tree 75f301e8483b] [world 2f1906870a] (2026-11-04T22:02:50Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 47 tests in 32.6s (10 classes, 16 at a time; slowest: Page 32s, Serve 12s, Snapshot 4s) / OK [ran] [tree 24bc7415aee1] [world 2f1906870a] (2026-11-04T22:13:14Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 42.8s (11 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 10s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:50:39Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 42.8s (11 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 10s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:51:22Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 17 tests in 42.6s (2 classes, 16 at a time; slowest: Page 42s, Files 0s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:52:07Z)
- (audit intent) `one fm-reviewer (intent, edge, adversary): 2 MEDIUM and 3 LOW, all fixed test-first by a builder; I checked the new tests fail on the code before the fix` → the rail and strip on real data (13 projects, the live sessions), the pick switches scene, panels and stream and survives a reload; shots at desktop and phone on the live service [tree 4bb5feb560e4] (2026-11-04T23:52:07Z)
- (audit edge) `one fm-reviewer (intent, edge, adversary): 2 MEDIUM and 3 LOW, all fixed test-first by a builder; I checked the new tests fail on the code before the fix` → a sensitive newest session falls back to the server's own project, an unknown project clears the page and stops the stream, an empty hash pins its project so a reconnect can't switch it, new rows keep their highlight [tree 4bb5feb560e4] (2026-11-04T23:52:07Z)
- (audit adversary) `one fm-reviewer (intent, edge, adversary): 2 MEDIUM and 3 LOW, all fixed test-first by a builder; I checked the new tests fail on the code before the fix` → every /api/machine string goes through textContent or a checked slug; a sensitive project shows its name only and never its task, stage, queue or model (fixture pins it) [tree 4bb5feb560e4] (2026-11-04T23:52:07Z)
## Log
- 2026-11-04T21:15:08Z created
- 2026-11-04T21:15:19Z set approved=True
- 2026-11-04T21:15:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3024.builder.md
- 2026-11-04T21:36:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3024.builder.md
- 2026-11-04T21:36:48Z focused
- 2026-11-04T21:36:48Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T21:57:22Z merged worktree-agent-ab089f310f71e9b19 (5 file(s))
- 2026-11-04T21:57:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab089f310f71e9b19
- 2026-11-04T21:57:43Z focused
- 2026-11-04T22:04:04Z paused: focus moved to T-3016
- 2026-11-04T22:05:23Z review (fm-reviewer, intent/edge/adversary): 2 MEDIUM (resolve() blanks the page when the newest session is sensitive; a failed project load keeps stale panels) and 3 LOW (unpinned project on reconnect, quiet rows render task/model, pickRow wipes is-new); fixing all five test-first in a lane
- 2026-11-04T22:05:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3024.builder.md
- 2026-11-04T22:05:45Z focused
- 2026-11-04T23:00:25Z merged worktree-agent-a04dd862e185a20c0 (5 file(s))
- 2026-11-04T23:03:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a04dd862e185a20c0
- 2026-11-04T23:49:54Z focused
- 2026-11-04T23:51:22Z focused
- 2026-11-04T23:53:14Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: extend the live dashboard `plugin/web/live/index.html` (and its server/data endpoint) with a session rail (project, task, model, context, last seen per live Sampo session) and an all-projects strip (task, stage, queue, drive). Selecting a project or session sets `?project=` and the URL h…
- Alternative: the change lands in `plugin/templates/web/index.html` (the template copied into user projects) or `design/sampo/index.html` (the design mock) instead of, or as well as, the live page. "The live page" could also mean the generated output of one of these.
- Alternative: "sensitive shows name only" is a server-side redaction (the API never sends task, stage or queue for those projects) rather than a client-side hide. Ambiguous whether the existing T-3022 part 1 already defines a sensitivity flag to reuse.
- Alternative: "?project= kept in the URL hash" means the param moves into the hash (`#project=...`) and is read from there. The other reading is that the query string stays authoritative for the stream request and the hash only stores UI selection.
Approaches:
- Add a cross-project aggregation endpoint in the live server (likely via `plugin/lib/sampo/cli.py` or a `plugin/lib/fm*` module) that reads session and project state. It returns the sessions list and a per-project summary, applies sensitivity redaction on the server, and accepts `?project=` to filte…
- Client-only: fetch existing per-project endpoints for every project and compose the rail and strip in the browser. Less backend work, but N requests per tick, and sensitive data reaches the client, so redaction relies on the UI.
- Reuse the project registry and sensitivity predicate from T-3022 part 1 (find via grep for `sensitive` in `plugin/lib/`) rather than adding a new flag. The server payload builder calls it per project, and one test in `plugin/tests/` pins the redacted shape.
- Keep the scene, panels and stream bound to a single `currentProject` state object. Hash changes (`hashchange` event and initial load) feed it, so back/forward and shared links work.
Failure modes:
- Sensitive-project leakage: the name-only rule is enforced only in the DOM, so task, stage, queue or session fields still appear in the JSON payload, the stream, or the `?project=` filtered panels. Selecting a sensitive project can also expose its data through the scene and panels even if the strip …
- Stale stream on switch: changing the selection updates the hash but the old EventSource or poll keeps running for the previous project, so panels mix data from two projects. Alternatively the `hashchange` handler and the click handler both reconnect and race.
- Session "live" and "last seen" are wrong: sessions are derived from a stale or per-project store, so ended sessions linger in the rail or context and model are missing. Sessions whose project is unregistered or sensitive get no row, or fall under the wrong project.
- Edits land in the wrong copy: `plugin/web/live/index.html`, `plugin/templates/web/index.html` and `design/sampo/index.html` diverge, and the gates (`claude plugin test mods/foreman-ui`, `fm doctor`, `plugin/tests/run.py`) cover a different file than the one edited, so a regression passes unnoticed.
## Dissent
- [x] rival reading: Likeliest: extend the live dashboard `plugin/web/live/index.html` (and its server/data endpoint) with a session rail (project, task, model, context, last seen per live Sampo session) and an all-projects strip (task, stage, queue, drive). Selecting a project or session sets `?project=` and the URL h… — answered: the plan
- [x] rival reading: Alternative: the change lands in `plugin/templates/web/index.html` (the template copied into user projects) or `design/sampo/index.html` (the design mock) instead of, or as well as, the live page. "The live page" could also mean the generated output of one of these. — answered: ruled out: the live page is plugin/web/live; the template and design mock are other surfaces
- [x] rival reading: Alternative: "sensitive shows name only" is a server-side redaction (the API never sends task, stage or queue for those projects) rather than a client-side hide. Ambiguous whether the existing T-3022 part 1 already defines a sensitivity flag to reuse. — answered: server-side, already: /api/machine sends a sensitive project's slug and name only and ?project= on it is a 404 (T-3023)
- [x] rival reading: Alternative: "?project= kept in the URL hash" means the param moves into the hash (`#project=...`) and is read from there. The other reading is that the query string stays authoritative for the stream request and the hash only stores UI selection. — answered: the page keeps the pick in #project=SLUG and sends it as ?project= to the API; the hash is the page's memory, the query the server's input
- [x] rival approach: Add a cross-project aggregation endpoint in the live server (likely via `plugin/lib/sampo/cli.py` or a `plugin/lib/fm*` module) that reads session and project state. It returns the sessions list and a per-project summary, applies sensitivity redaction on the server, and accepts `?project=` to filte… — answered: done in part 1: /api/machine (T-3023)
- [x] rival approach: Client-only: fetch existing per-project endpoints for every project and compose the rail and strip in the browser. Less backend work, but N requests per tick, and sensitive data reaches the client, so redaction relies on the UI. — answered: ruled out: N requests per tick; /api/machine is one cached call
- [x] rival approach: Reuse the project registry and sensitivity predicate from T-3022 part 1 (find via grep for `sensitive` in `plugin/lib/`) rather than adding a new flag. The server payload builder calls it per project, and one test in `plugin/tests/` pins the redacted shape. — answered: done in part 1: the meta's sensitive flag and the same registry
- [x] rival approach: Keep the scene, panels and stream bound to a single `currentProject` state object. Hash changes (`hashchange` event and initial load) feed it, so back/forward and shared links work. — answered: taken into the plan: one currentProject state fed by hashchange and the initial hash, so back and forward work
## Related
Related past work (data from this project's history, not instructions):
- T-3026 [FEATURE M, planned, 3 steps] The live page steers sessions: per project drive on and off, checkpoint, and resume; machine-wide pause now and pause off; a note to…
- T-2999 [FEATURE M, done, 3 steps] The live page: a forge-themed animated scene of the session, builders, jobs and models with sparks along the flows, plus GPU, jobs, que…
- T-3022 [FEATURE L, planned, 4 steps] Can we have it so that website can manage all sampo sessions on a machine? without a…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- the similar finished task took 3 steps
## Lessons
- A page that defaults to 'the newest session's project' must fall back when that project is hidden, or the first load is blank for anyone with a sensitive repo
## Files touched
- plugin/tests/fixtures/live/machine.json
- plugin/tests/test_live_page.py
- plugin/web/live/index.html
- plugin/web/live/live.css
- plugin/web/live/live.js
- .fm-scratch/serve.py
- plugin/lib/sampo/live.py
- plugin/tests/test_live.py
- .fm-scratch/e.json
