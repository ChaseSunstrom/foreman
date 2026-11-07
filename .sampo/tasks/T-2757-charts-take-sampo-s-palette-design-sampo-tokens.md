---
id: T-2757
type: FEATURE
tier: M
status: done
priority: normal
scope: [design/sampo/**, site/style.css, site/build.py, plugin/tests/test_site_sampo.py, plugin/tests/test_sampo_design.py, CHANGELOG.md]
depends_on: [T-2742]
source: discovered
created: 2026-11-03T03:25:11Z
updated: 2026-11-03T03:36:02Z
builder_model: sonnet
base: ca345c60ebd0bf9ea7eaeec7ab92f2cd51274552
base_tree: 7871c445ef4abeaf140e4f5c701b8d0610434730
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T03:29:34Z
plan0_scope: [design/sampo/**, site/style.css, site/build.py, plugin/tests/test_site_sampo.py, plugin/tests/test_sampo_design.py, CHANGELOG.md]
lane_stop: merged 2026-11-03T03:32:51Z
verified: strong
unproven: [ui-unshot]
---
# Charts take Sampo's palette: tokens.json gains a six-series chart palette per theme (forge hues, distinguishable, AA 3:1 against the chart panel), style.css's --s1..--s6 and the design preview are generated from it (T-2757)
## Raw request
> FEATURE: charts take Sampo's palette: design/sampo/tokens.json gains a chart palette (six series, AA against the surface in light and dark); site/style.css's --s1..--s6 and design/sampo/index.html read it instead of hand-typed values (the Ward page's bars are still the old blue) #T-2742
## Interpretation
Reading 1 (chosen): the site's charts still use the old Foreman blue/orange/green set hand-typed in style.css; SAMPO.md asks for one design system on every surface, so the chart series join tokens.json and are generated like every other colour. Reading 2: recolour the six values by hand in style.css; rejected: it repeats the two-copies drift T-2753 removed.
## Assumptions (confidence)
## Acceptance criteria
- [x] tokens.json holds chart.s1..s6 for light and dark; each series meets 3:1 against the chart panel in its theme and adjacent series differ in hue; the token block site/build.py writes carries them and style.css has no hand-typed --s values — verify with `python3 plugin/tests/run.py test_site_sampo test_sampo_design`
- [x] the site builds and its chart pages render in the new palette at 1280 dark and 390 light — verify with `python3 plugin/tests/run.py test_site test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Add a chart group to tokens.json per theme and extend site/build.py's token block to emit --s1..--s6; delete the hand-typed lines. Likely outcome: one source, small diff. Fails if: the block writer only knows color roles (extend it to the chart group).
2. Derive the series from existing roles (bronze, ember, accent, success, warning, error). Likely outcome: no new tokens. Fails if: status colours double as series and read as good/bad.
3. Use what exists: site/build.py's --tokens block writer and its staleness test (T-2753), design/sampo/index.html's preview, and the dataviz skill's palette method and validator. Likely outcome: no new tooling. Fails if: the validator's defaults assume a white panel (pass the panel colours).
4. Do less: leave charts blue. Fails if: the Ward page visibly breaks the palette.
Choice 1 with 3 (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py; past FIXes T-1129, T-1131, T-1132, T-1133, T-1134.
## Execution prompt
## Steps
1. [x] red: a test that the --s values come from tokens.json and pass the contrast and hue-spacing checks
2. [x] pick the palette with the dataviz skill's method and validator (bronze, ember, verdigris, rune blue and the like from the forge direction, never the old SaaS blue), add it to tokens.json, generate it into the CSS block and the design preview
3. [x] screenshots of the Ward and Benchmarks pages in both themes; a CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_sampo test_sampo_design` → exit 0 · Ran 37 tests in 1.0s (6 classes, 16 at a time; slowest: Built 1s, Logo 0s, Tokens 0s) / OK [ran] [tree c8b39bffec46] [world 2f1906870a] (2026-11-03T03:32:04Z)
- (step 2) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 45 tests in 6.0s (23 classes, 16 at a time; slowest: Header 6s, Landing 3s, Session 2s) / OK [ran] [tree c8b39bffec46] [world 2f1906870a] (2026-11-03T03:32:11Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sampo test_sampo_design` → exit 0 · Ran 38 tests in 0.8s (6 classes, 16 at a time; slowest: Built 0s, Logo 0s, Tokens 0s) / OK [ran] [tree 8ae8bf3cf68e] [world 2f1906870a] (2026-11-03T03:32:54Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 46 tests in 5.1s (23 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 2s) / OK [ran] [tree 8ae8bf3cf68e] [world 2f1906870a] (2026-11-03T03:33:00Z)
- (step 3) `python3 site/build.py /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/site-main && /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/shot.sh /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/site-main/features/guard.html /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/ward-dark.png 1280 1400 dark reduce 6000 && /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/shot.sh /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/site-main/features/benchmarks.html /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/bench-light.png 1280 2400 light reduce 6000` → exit 0 · /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/ward-dark.png / /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpa [ran] [tree 029e559af46b] [world 2f1906870a] (2026-11-03T03:34:00Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sampo test_sampo_design` → exit 0 · Ran 38 tests in 2.7s (6 classes, 16 at a time; slowest: Built 2s, Logo 1s, Preview 0s) / OK [ran] [tree 029e559af46b] [world 2f1906870a] (2026-11-03T03:34:24Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 46 tests in 7.9s (23 classes, 16 at a time; slowest: Header 7s, Landing 5s, Session 5s) / OK [ran] [tree 029e559af46b] [world 2f1906870a] (2026-11-03T03:34:24Z)
- (audit intent) `reviewed 836ea14f: screenshots of the Drive page (five series stacked) at 1280 in light and dark and the Ward page at 1280 dark under reduced motion: every series tells apart from its neighbours in both themes, the Ward's bars are bronze, no SaaS blue left; contrast and hue spacing are tested numbers, the writer regenerates style.css and the preview from tokens.json` → SAMPO.md Consistency: one palette on every surface; charts were the last hand-typed colours on the site [tree 029e559af46b] (2026-11-03T03:34:24Z)
- (audit edge) `reviewed 836ea14f: screenshots of the Drive page (five series stacked) at 1280 in light and dark and the Ward page at 1280 dark under reduced motion: every series tells apart from its neighbours in both themes, the Ward's bars are bronze, no SaaS blue left; contrast and hue spacing are tested numbers, the writer regenerates style.css and the preview from tokens.json` → the light theme's darker series (bronze #8A6212, verdigris #1F7F73) stay 4.7:1+ on the raised panel; stacked thin segments (Research) still visible in both themes [tree 029e559af46b] (2026-11-03T03:34:24Z)
- (audit adversary) `reviewed 836ea14f: screenshots of the Drive page (five series stacked) at 1280 in light and dark and the Ward page at 1280 dark under reduced motion: every series tells apart from its neighbours in both themes, the Ward's bars are bronze, no SaaS blue left; contrast and hue spacing are tested numbers, the writer regenerates style.css and the preview from tokens.json` → tokens.json values are written into CSS unescaped, so a value could carry a declaration or url(); the file has the same trust as style.css (a commit to this repo), and the build's T-1411 check scans the built stylesheet and fails on any other-host load, so an injected url() cannot ship [tree 029e559af46b] (2026-11-03T03:34:24Z)
## Log
- 2026-11-03T03:25:11Z created
- 2026-11-03T03:29:12Z planned from capture
- 2026-11-03T03:29:17Z set approved=True
- 2026-11-03T03:29:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2757.builder.md
- 2026-11-03T03:29:32Z focused
- 2026-11-03T03:29:34Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T03:32:51Z merged worktree-agent-ad3baa5a5d0fbe494 (5 file(s))
- 2026-11-03T03:32:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad3baa5a5d0fbe494
- 2026-11-03T03:32:51Z focused
- 2026-11-03T03:33:09Z scope: CHANGELOG.md line
- 2026-11-03T03:33:42Z paused: focus moved to T-2742
- 2026-11-03T03:33:54Z focused
- 2026-11-03T03:35:58Z done
- 2026-11-03T03:36:02Z committed 80045ce3 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2753 [FEATURE M, active, 4 steps] The site takes Sampo's design system (T-2742 step 7a): style.css reads design/sampo/tokens.json, the Runestone mark and its variants …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_audit_run.py, plugin/tests/test_design_diverge.py, plugin/tests/test_design_gates.py, plugin/tests/test_design…
## Lessons
- Judge a categorical palette on the page with the most series stacked (Drive: five), not on a single-series chart
## Files touched
- plugin/tests/test_sampo_design.py
- design/sampo/tokens.json
- site/build.py
- site/style.css
- design/sampo/index.html
- .fm-scratch/e.json
- CHANGELOG.md
