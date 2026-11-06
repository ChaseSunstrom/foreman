---
id: T-3228
type: CLEAN
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T18:13:17Z
updated: 2026-11-06T10:09:28Z
lane: ~/.claude/foreman/.claude/worktrees/agent-afd7abea92dfe6c3d
lane_branch: worktree-agent-afd7abea92dfe6c3d
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:32:21Z
plan0_scope: []
builder_returned: 2026-11-06T10:09:28Z
---
# Kit demo heights come from a measured render, not hand-set numbers in ui-kit.html's markers
## Raw request
> kit demo heights are hand-set numbers that depend on installed fonts: measure each demo's height in the render check instead (T-3102 noticed)
## Interpretation
Drop numbers from ui-kit.html markers; kit() measures each demo via works.check_html (shot.chrome()), cached in memory by html sha256; no browser -> h 200 (cards.js default), not cached.
## Assumptions (confidence)
## Acceptance criteria
- [ ] ui-kit.html's markers carry no height (<!-- kit: NAME -->); smallcards.kit() returns each demo's height measured by works.check_html (cached by the demo's text hash), so a different installed font changes the number, not the test — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] the site's kit.json and the cards page size each demo frame from the measured height, unchanged in shape — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
Measure in kit() with hash cache (chosen) vs runtime JS height in the page: site already reads h from kit.json, so measuring at build keeps shape.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a marker without a height parses and kit() reports the rendered height
2. [x] measure in kit() with a hash-keyed cache; drop the numbers from ui-kit.html; site build reads the measured h
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_small_cards.ExamplesRendered` → exit 0 · Ran 3 tests in 182.0s (1 jobs, 16 at a time; slowest: ExamplesRendered 52s) / OK [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:39:57Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards.ExamplesRendered` → exit 0 · Ran 3 tests in 419.3s (1 jobs, 16 at a time; slowest: ExamplesRendered 53s) / OK [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:40:45Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.CardsDemo` → exit 0 · Ran 2 tests in 10.0s (1 jobs, 16 at a time; slowest: CardsDemo 0s) / OK [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:43:17Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.Cards` → exit 0 · Ran 12 tests in 203.0s (3 jobs, 16 at a time; slowest: CardsExport 54s, CardsPage 14s, CardsDemo 0s) / OK [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:43:27Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.CardsPage` → exit 0 · Ran 7 tests in 37.7s (1 jobs, 16 at a time; slowest: CardsPage 14s) / OK [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:43:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench_family test_code_tui test_docs test_doctor test_left_out test_library test_models test_rename_scan test_scene test_showpieces test_small_cards && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 780 tests in 252.0s (180 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 13s, GraphBrowser 13s, CityBrowser 13s) / FAILED (1 classes: t [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:48:14Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 30 tests in 85.6s (8 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 11s, ExamplesRendered.test_blank_overflow_and_faint_text_fail_and_ [ran] [tree bd61cc61ebe3] [world 2f1906870a] (2026-11-06T09:50:10Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.CardsDemo test_small_cards.ExamplesRendered test_small_cards.Examples` → exit 0 · Ran 12 tests in 23.2s (5 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 10s, ExamplesRendered.test_blank_overflow_and_faint_text_fail_and_ [ran] [tree 120cdd4b7e3a] [world 2f1906870a] (2026-11-06T10:04:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench_family test_code_tui test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_library test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_scene test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.20s] [ran] [tree 120cdd4b7e3a] [world 2f1906870a] (2026-11-06T10:09:24Z)
## Log
- 2026-11-05T18:13:17Z created
- 2026-11-06T03:17:29Z planned from capture
- 2026-11-06T09:32:16Z focused
- 2026-11-06T09:32:21Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3102 [FEATURE M, done, 3 steps] Every UI card shows a rendered example of its component: a checked card-specific one where it exists, else its component's kit demo (T-…
- research T-1609-review: Verdict:** approve with nits. One finding should be fixed before merge (the silent missing-marker case). [stale: site/build.py, site/index.html, …
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- decision 2026-11-05: [cites: research T-2879-probe] T-2879: rename the plugins inside the existing 'foreman' marketplace with a renames map (foreman→sampo, foreman-ui→sa…
## Behaviour lock
kit() returns the same {component: {html, h}} shape; the site's kit.json and cards.js read h unchanged; demos' markup and visuals untouched.
