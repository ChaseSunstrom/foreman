---
id: T-3055
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/web/live/index.html, plugin/web/live/live.css, plugin/web/live/live.js, plugin/lib/sampo/live.py, plugin/tests/test_live_page.py, plugin/tests/test_live.py]
depends_on: []
source: user
created: 2026-11-05T00:27:50Z
updated: 2026-11-06T14:49:20Z
builder_model: haiku
base: a0f6762fe1caa0759184a50b4705d78d478a5878
base_tree: ae20954afbff4dbcfd45898b44f40b3d28341f56
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T01:17:25Z
plan0_scope: [plugin/web/live/index.html, plugin/web/live/live.css, plugin/web/live/live.js, plugin/lib/sampo/live.py, plugin/tests/test_live_page.py, plugin/tests/test_live.py]
builder_returned: 2026-11-06T12:48:54Z
---
# Live page part 1: a modern theme by default (clean dashboard shell, tokens, type, layout) and the forge look as a setting (T-3054)
## Raw request
> Live page part 1: a modern theme by default (clean dashboard shell, tokens, type, layout) and the forge look as a setting (T-3054)
## Interpretation
Reading 1 (taken): part 1 of T-3054: the page's look splits into two themes, modern (the default: a clean, current dashboard) and forge (today's look, opt-in), with the forge-only parts (the scene, forge words, brass, serif) behind the forge theme; charts are part 2. Reading 2 (ruled out): restyle in place with no theme switch: the user asked for the forge as a setting.
## Assumptions (confidence)
## Acceptance criteria
- [ ] More modern, less forge-specific by default: with no setting the page is a modern dashboard (neutral palette, system sans, no serif, no forge scene, no forge words like Furnaces, anvil or ember, the Network view as the hero), in light and dark — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [ ] Unless turned on as a setting: theme forge brings back today's forge look exactly (scene, palette, fonts, words); a header toggle keeps the viewer's choice; sampo settings sets the default the server sends — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [ ] Nothing a user already has breaks: the rail, actions, stream, Network view and keyboard paths keep working in both themes; no console errors and no sideways scroll at 1440 and 390 — verify with `python3 plugin/tests/run.py test_live test_live_page`
## Non-goals
## Approach (options → choice → why)
1) use what exists: CSS custom properties per [data-theme] on the root, the current forge values moved under forge, a modern token set as the default; forge-only DOM and the scene shown only under forge; the Network view (T-3034) as the modern hero: likely outcome: today's forge preserved byte-for-byte in look. 2) two stylesheets swapped at runtime: fails if: shared rules duplicate and drift. 3) a separate modern page: fails if: rail, actions and stream are built twice. 4) do less: hide the scene only: fails if: brass and serif still read as forge. Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/fixtures/live/snap-5.json, plugin/lib/sampo/moonscale.py, plugin/web/live/charts.js, CHANGELOG.md, plugin/tests/fixtures/live/machine.json; past FIXes T-3014, T-3021, T-3199.
## Execution prompt
Read the parent's brief (state/projects/foreman-4a056f/tasks/T-3054-can-you-update-the-live-view-website-to-be-more.md). The live page lives in plugin/web/live (index.html, live.css, live.js, fonts) served by plugin/lib/sampo/live.py (sampo watch --web; the systemd unit sampo-live serves http://127.0.0.1:46459/). Modern theme direction: a current product dashboard (think Linear, Vercel, Grafana's newer panels): neutral greys with one cool accent (no brass/gold), system UI sans (no serif display font; a mono only for ids and numbers), 8px radius cards with a hairline border, generous spacing, clear hierarchy, subtle motion; light and dark from prefers-color-scheme. Words: 'Jobs' not 'Furnaces', no 'live forge' tagline. The forge theme must look exactly as today: capture forge shots before your first edit and compare after. The theme choice: a header toggle (localStorage sampo-live-theme), a default from the server (sampo settings key for the live theme; find how settings are read in live.py or add one), forge words and the scene only under forge. Tests in test_live_page (both themes, toggle persistence, no forge words by default, no console errors, no sideways scroll at 390). Shots: uv run --offline --no-project --with playwright python /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/realshot.py URL OUT W H scheme waitms (read it first), saved as /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3054-*.png and read.
## Steps
1. [x] theme tokens and the modern shell, the forge gated (tests first)
2. [x] the toggle and the settings default (tests first)
3. [x] shots in both themes at desktop and phone
## Resume here
<!-- auto -->
- 2026-11-05T01:42:16Z step 3/3: shots in both themes at desktop and phone
- git: worktree-agent-ad0c70bbc80ef7cc5; 9 uncommitted: plugin/lib/sampo/live.py, plugin/lib/sampo/settings.py, plugin/lib/sampo/smithtui.py, plugin/tests/test_live.py, plugin/tests/test_live_page.py, plugin/web/live/index.html, plugin/web/live/live.css, plugin/web/live/live.js, plugin/web/live/theme.js
- touched since last checkpoint: .fm-scratch/js_edits.json, plugin/web/live/live.js, .fm-scratch/srv_edits.json, plugin/lib/sampo/smithtui.py, plugin/lib/sampo/settings.py, plugin/lib/sampo/live.py, plugin/tests/test_live.py, plugin/web/live/index.html, plugin/tests/test_live_page.py, .fm-scratch/shots.py, plugin/web/live/live.css
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live_page` → ✗ exit 1 · Ran 32 tests in 221.5s (2 classes, 16 at a time; slowest: Page 221s, Files 0s) / FAILED (1 classes: test_live_page.Page) [ran] [tree 5390a29575ee] [world 2f1906870a] (2026-11-05T01:27:18Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 81 tests in 106.6s (11 classes, 16 at a time; slowest: Page 106s, Serve 15s, Act 12s) / OK [ran] [tree 2c18b60887ec] [world 2f1906870a] (2026-11-05T01:41:33Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 81 tests in 100.6s (11 classes, 16 at a time; slowest: Page 100s, Serve 11s, Act 10s) / OK [ran] [tree 2559ef1ed1e4] [world 2f1906870a] (2026-11-05T01:46:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_settings test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [27.23s] [ran] [tree 2559ef1ed1e4] [world 2f1906870a] (2026-11-05T01:48:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_settings test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [12.54s] [ran] [tree 2559ef1ed1e4] [world 2f1906870a] (2026-11-05T01:49:48Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 81 tests in 87.9s (11 classes, 16 at a time; slowest: Page 88s, Serve 11s, Act 10s) / OK [ran] [tree d6e9f92f657c] [world 2f1906870a] (2026-11-05T01:57:38Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 96.7s (36 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 18s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree ae20954afbff] [world 2f1906870a] (2026-11-06T12:48:46Z)
## Log
- 2026-11-05T00:27:50Z created
- 2026-11-05T00:27:51Z set approved=True
- 2026-11-05T01:17:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3055.builder.md
- 2026-11-05T01:17:21Z focused
- 2026-11-05T01:17:25Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T03:10:25Z merged worktree-agent-ad0c70bbc80ef7cc5 (9 file(s))
- 2026-11-05T03:10:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad0c70bbc80ef7cc5
- 2026-11-05T03:20:52Z blocked: merged (live page restarted, modern theme served); its close runs after the merge queue lands (closes yield to merges)
- 2026-11-06T03:54:46Z unblocked
- 2026-11-06T12:47:05Z focused
- 2026-11-06T14:49:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a973805b231a9e319
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3054 [FEATURE L, planned, 4 steps] The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting
- T-3024 [FEATURE M, done, 3 steps] The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-proje…
- T-2852 [FEATURE M, done, 3 steps] Port 12's look to every section page (site/pages.py's template and blocks) and the Rune tower (site/genesis: index.html, genesis.css, g…
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_live_page] A brand theme dresses brand surfaces; a working tool defaults to a plain, modern look and carrie…
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_design_surfaces.py, plugin/tests/test_design_tokens.py, plugin/tests/test_docs.py, plugin/tests/test_edit_cards.…
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/live.py, plugin/tests/test_live.py, plugin/tests/test_live_page.py, plugin/web/live/index.html, plugin/web/live/live.css, plugin/web/live/live.js; re-ground the plan against them before editing
