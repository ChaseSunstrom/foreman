---
id: T-3106
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:07:10Z
updated: 2026-11-05T17:31:44Z
builder_model: haiku
base: cdac8696380c16c8db96a42314496d44d3650d4e
base_tree: bc5d04e447d9fea4b29dad34e09d4f8a56340e78
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:16:10Z
plan0_scope: []
builder_returned: 2026-11-05T11:32:48Z
lane_stop: merged 2026-11-05T15:34:02Z
lane_verified: 37d09c710551e069f49477a504605c4e7bab3d63
verified: strong
unproven: [docs]
---
# Design works part 1: render every SVG headless and check it by its type's measurable gates, with perceptual dedupe (T-3104)
## Raw request
> Design works part 1: render every SVG headless and check it by its type's measurable gates, with perceptual dedupe (T-3104)
## Interpretation
Reading 1 (chosen): a works module that sanitises an SVG (no script, no external refs), renders it to PNG at its sizes in light and dark with the headless chrome shell, and scores gates per type: valid XML, not blank, nothing clipped by the viewBox, text contrast 4.5:1, palette size, path count and file size bounds, icon-set stroke and grid consistency, animated frames that differ and loop; a perceptual hash of the render drops near duplicates. Reading 2: XML validity only; rejected, a valid SVG can be blank, clipped or unreadable.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo works check FILE renders it and prints each gate's verdict with its number; a blank, clipped, low-contrast, scripted or oversized SVG fails the named gate; an animated one whose frames don't change fails — verify with `python3 plugin/tests/run.py test_design_works`
- [x] two renders whose perceptual hashes are within the bar are one work; the later is a duplicate — verify with `python3 plugin/tests/run.py test_design_works`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the site's chrome shell for renders, Pillow if present else the shell's own pixel readout, gates as small functions per type; likely outcome: every candidate gets a verdict with reasons in seconds. 2. Do less: validity and size; fails if: broken renders pass. 3. A vision model as the only judge; fails if: models advise and proof decides, so gates must be measurable. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests with fixture SVGs for each gate
2. [x] the works module: sanitise, render, gates, dedupe, the check verb
## Resume here
<!-- auto -->
- 2026-11-05T11:20:18Z step 1/2: failing tests with fixture SVGs for each gate
- git: worktree-agent-ad1b3494e641d9d7f; 2 uncommitted: plugin/lib/sampo/design.py, plugin/tests/test_design_works.py
- touched since last checkpoint: .fm-scratch/hostile.py, plugin/tests/test_design_works.py, plugin/lib/sampo/design.py
## Docs impact
CHANGELOG line; sampo works in the CLI help; works.py's docstring names the gates
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_works` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.5s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree b0850d934463] [world 2f1906870a] (2026-11-05T10:25:47Z)
- (step 2) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 17 tests in 11.9s (4 classes, 16 at a time; slowest: Rendered 11s, WithoutBrowser 1s, StaticGates 0s) / OK [ran] [tree 9dddd90165d0] [world 2f1906870a] (2026-11-05T10:51:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [13.11s] [ran] [tree c89ffc8ba917] [world 2f1906870a] (2026-11-05T11:00:20Z)
- (step 2) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 18 tests in 10.4s (4 classes, 16 at a time; slowest: Rendered 10s, WithoutBrowser 1s, StaticGates 0s) / OK [ran] [tree b6450dbb35df] [world 2f1906870a] (2026-11-05T11:09:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [12.90s] [ran] [tree b6450dbb35df] [world 2f1906870a] (2026-11-05T11:18:29Z)
- (step 2) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 25 tests in 6.9s (5 classes, 16 at a time; slowest: Rendered 6s, StaticGates 1s, WithoutBrowser 0s) / OK [ran] [tree c4677fd317d2] [world 2f1906870a] (2026-11-05T11:24:45Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_shot test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [23.31s] [ran] [tree c4677fd317d2] [world 2f1906870a] (2026-11-05T11:32:21Z)
- (step 2) `python3 plugin/tests/run.py test_design_works test_design` → exit 0 · Ran 148 tests in 5.5s (36 jobs, 16 at a time; slowest: Extract 5s, Tokens 4s, Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 4s) / OK [ran] [tree f417f3c83626] [world 2f1906870a] (2026-11-05T17:31:07Z)
- `python3 plugin/tests/run.py test_design_works` → ✗ exit 1 · Ran 0 tests in 2.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (start tree + this task's tests) [ran] [tree f417f3c83626] [world 2f1906870a] (2026-11-05T17:31:20Z)
- `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 25 tests in 3.9s (9 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 3s, Rendered.test_cards_low_contrast_and_scripted_fail_their_gates 3s, Rende [ran] [tree f417f3c83626] [world 2f1906870a] (2026-11-05T17:31:20Z)
- (ac 1) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 25 tests in 3.9s (9 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 3s, Rendered.test_cards_low_contrast_and_scripted_fail_their_gates 3s, Rende [ran] [tree 9f290ed458f0] [world 2f1906870a] (2026-11-05T17:31:36Z)
- (ac 2) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 25 tests in 3.9s (9 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 3s, Rendered.test_cards_low_contrast_and_scripted_fail_their_gates 3s, Rende [ran] [tree 9f290ed458f0] [world 2f1906870a] (2026-11-05T17:31:36Z)
- (audit intent) `re-ran test_design_works + test_design on main after the merge (148 OK), proved red→green; built on Opus, adversary review's 3 HIGH + 4 lower findings fixed before merge (verified: bounded regexes, browser env ENV_KEEP + NET_OFF)` → works check renders each SVG light and dark, holds it to its type's measured gates and flags near-duplicates (a turned hand or one added stroke is an original) [tree 9f290ed458f0] (2026-11-05T17:31:36Z)
- (audit adversary) `re-ran test_design_works + test_design on main after the merge (148 OK), proved red→green; built on Opus, adversary review's 3 HIGH + 4 lower findings fixed before merge (verified: bounded regexes, browser env ENV_KEEP + NET_OFF)` → hostile SVGs fail only their own work: non-finite colours, a 1e-307 viewBox, use fan-out and cycles, megabyte regex traps (1 MiB: >30 s to 0.1 s), hung renders (the browser restarts), crashing files; the browser gets no secrets and no network [tree 9f290ed458f0] (2026-11-05T17:31:36Z)
- (audit edge) `re-ran test_design_works + test_design on main after the merge (148 OK), proved red→green; built on Opus, adversary review's 3 HIGH + 4 lower findings fixed before merge (verified: bounded regexes, browser env ENV_KEEP + NET_OFF)` → three hung works in a row stop the batch; a failed save loses only that work's pictures [tree 9f290ed458f0] (2026-11-05T17:31:36Z)
## Log
- 2026-11-05T03:07:10Z created
- 2026-11-05T03:08:10Z set approved=True
- 2026-11-05T03:08:33Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T10:15:58Z unblocked
- 2026-11-05T10:15:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3106.builder.md
- 2026-11-05T10:16:09Z focused
- 2026-11-05T10:16:10Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:33:22Z verified: COLOUR bounded to [^)]{0,200}, DOCTYPE strip bounded {0,512}, browser env = ENV_KEEP + NET_OFF (works.py:37-40, :528); queued for merge
- 2026-11-05T14:40:44Z user approved core in Claude Code's permission prompt
- 2026-11-05T15:34:02Z merged worktree-agent-ad1b3494e641d9d7f (8 file(s))
- 2026-11-05T15:34:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad1b3494e641d9d7f
- 2026-11-05T15:40:37Z verified: the full suite is green on 37d09c710
- 2026-11-05T17:30:59Z focused
- 2026-11-05T17:31:37Z affected tests waived: names that can't match are T-3160's modules (merged and reverted inside this window, not on disk); T-3106's own tests pass (148 OK)
- 2026-11-05T17:31:40Z done
- 2026-11-05T17:31:44Z committed 098b7584 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Visual QA: screenshots, an eyeball pass and a receipt (fm playbooks show ui/visual-qa)
- research T-2788-design-review: Verdict: SHIP WITH FIXES. The landing is faithful to the converged forge and the hard bar holds. One High on the tower page (rules grid br…
- T-3112 [FEATURE M, blocked, 3 steps] Design works part 4: fill to 3,000 kept across 10+ types over nights; local models learn SVG techniques as cards and join when their…
- decision 2026-11-03: [outward] [revisited: Kirjokansi fused with Ilmarinen's forge] [cites: user steer 2026-11-03: super improve the fuse completely, combined/animated l…
## Lessons
- A renderer fed by models needs its own adversary pass: every input is untrusted, so bound each pattern and fail one work, never the batch
## Plan gaps
- failed first: step 1 failing tests with fixture SVGs for each gate
## Files touched
- plugin/tests/test_design_works.py
- plugin/lib/sampo/works.py
- plugin/lib/fmworks.py
- plugin/lib/sampo/cli.py
- .fm-scratch/w/clock.svg
- .fm-scratch/w/clock2.svg
- .fm-scratch/w/plus.svg
- .fm-scratch/w/clock3.svg
- .fm-scratch/w/card.svg
- .fm-scratch/w/forge.svg
- .fm-scratch/w/faint.svg
- .fm-scratch/w/scripted.svg
- MASTER.md
- docs/map/files-lib-3.md
- .fm-scratch/w/stopwatch.svg
- .fm-scratch/w/blue.svg
- .fm-scratch/w/thin.svg
- .fm-scratch/measure.py
- .fm-scratch/hostile.py
- plugin/lib/sampo/design.py
- plugin/lib/sampo/shot.py
- CHANGELOG.md
