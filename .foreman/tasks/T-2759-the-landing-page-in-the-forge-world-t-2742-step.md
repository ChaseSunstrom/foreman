---
id: T-2759
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/index.html, site/style.css, site/site.js, site/assets/**, site/build.py, plugin/tests/test_site_hero.py, plugin/tests/test_site_landing.py, plugin/tests/test_site.py, plugin/tests/test_rename_scan.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-03T03:29:55Z
updated: 2026-11-03T04:05:51Z
builder_model: sonnet
base: 2e3a72c7b1f4b5596098f907f97e4c74dd4884be
base_tree: 0495ab3d29c248e9523d34d855831b1d6036da92
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T03:30:21Z
plan0_scope: [site/index.html, site/style.css, site/site.js, site/assets/**, site/build.py, plugin/tests/test_site_hero.py, plugin/tests/test_site_landing.py, plugin/tests/test_site.py, plugin/tests/test_rename_scan.py, CHANGELOG.md]
lane_stop: merged 2026-11-03T04:04:01Z
verified: strong
unproven: [ui-unshot]
---
# The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline over a forge-glow shader, the stats as gears and dials of real numbers, a scroll scene of the forge beside the Smith section, the Kalevala myth paragraph once, tactile hover and press; still and complete with no JS and with reduced motion
## Raw request
> The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline over a forge-glow shader, the stats as gears and dials of real numbers, a scroll scene of the forge beside the Smith section, the Kalevala myth paragraph once, tactile hover and press; still and complete with no JS and with reduced motion
## Interpretation
Reading 1 (chosen): SAMPO.md's Website bullets that belong to the landing page: the hero (mill turning, runes writing into the headline), a shader background (forge glow), gears and dials as live data, the forge scroll scene for Smith, tactile states, the myth paragraph once; the per-feature scenes (runes for Rune, Louhi's trials, moons forged) belong to their own pages (7c). Reading 2: rebuild the whole landing's section order and copy too; rejected: T-2753 just renamed its copy, and restructuring it is out of this slice.
## Assumptions (confidence)
## Acceptance criteria
- [x] the landing's hero, dials, forge scene and shader meet SAMPO.md's quality bar: nothing from other hosts, every animation has a reduced-motion still, the page is complete with JS off, light and dark, 320 px without horizontal scroll, AA contrast, and fm design lint passes — verify with `python3 plugin/tests/run.py test_site_landing`
- [x] the myth paragraph appears once on the site (only on the landing) and the dials show numbers from site/data/stats.json, never typed in the page — verify with `python3 plugin/tests/run.py test_site_landing test_site test_site_hero`
- [x] the rename ratchet doesn't rise — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. Progressive layers: the HTML carries the complete page (headline text, numbers, the still mark); CSS animates under prefers-reduced-motion: no-preference; a small module adds the WebGL forge-glow canvas and pauses it offscreen. Likely outcome: no JS, reduced motion and slow GPUs all see a finished page. Fails if: the shader costs frames on mid-range hardware (cap its resolution at half the CSS pixels and 30 fps).
2. A canvas-first hero drawn by script. Likely outcome: richer motion. Fails if: no JS shows nothing, against the quality bar.
3. Use what exists: design/sampo/logo/mark-animated.svg and its still, the tokens' motion rules, the shader looks and fm scene (fm playbooks show ui/scene-3d), site/data/stats.json for the numbers, build.py's asset hashing, fm shot and fm design lint for QA. Likely outcome: little new art, real data. Fails if: the animated mark's timing doesn't suit a hero (adjust its CSS, not the logo source).
4. Do less: just enlarge the animated mark in the current hero. Fails if: SAMPO.md asks for runes writing the headline, the shader and the dials.
Choice 1 with 3 (80%).
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py; past FIXes T-1129, T-1131, T-1132, T-1133, T-1134.
## Execution prompt
## Steps
1. [x] red test_site_landing: no external hosts, a reduced-motion rule for each animation, a noscript-complete hero (content present in HTML, not injected), the myth paragraph exactly once across the built site, dial numbers equal stats.json, design lint
2. [x] hero: the animated Runestone mark large and turning, runes resolving into the headline letters (CSS/SVG, still under reduced motion), a forge-glow WebGL shader behind with a CSS gradient as the still and the no-JS fallback; the shader pauses offscreen and when the tab hides
3. [x] the stats as gears and dials (SVG, values from stats.json at build time), a scroll scene of the forge (hammer, sparks, glowing billet) beside the Smith section, tactile hover and press on buttons and cards; the myth paragraph once
4. [x] screenshots at 1280, 768 and 320 in light and dark, with and without reduced motion; fix what they show; a CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-03T03:51:09Z step 1/4: red test_site_landing: no external hosts, a reduced-motion rule for each animation, a noscript-complete hero (content present in HTML, not injected), the myth paragraph exactly once across the built site, dial numbers equal stats.json, design lint
- git: worktree-agent-af8cefd0b7eafab5c; 7 uncommitted: site/build.py, site/index.html, site/site.js, site/style.css, plugin/tests/test_site_landing.py, site/assets/mark-animated.svg, site/assets/mark.svg
- touched since last checkpoint: site/index.html, site/build.py, site/style.css, site/site.js
## Docs impact
CHANGELOG.md: the landing line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_site_landing 2>&1 | tail -30` → ✗ exit 1 · Ran 8 tests in 13.2s (1 classes, 16 at a time; slowest: Landing 9s) / FAILED (1 classes: test_site_landing.Landing) [ran] [tree d5247fd5aa32] [world 2f1906870a] (2026-11-03T03:46:17Z)
- (step 1) `python3 plugin/tests/run.py test_site_landing` → ✗ exit 1 · Ran 8 tests in 8.6s (1 classes, 16 at a time; slowest: Landing 7s) / FAILED (1 classes: test_site_landing.Landing) [ran] [tree d5247fd5aa32] [world 2f1906870a] (2026-11-03T03:46:29Z)
- (step 2) `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 8 tests in 4.5s (1 classes, 16 at a time; slowest: Landing 4s) / OK [ran] [tree 9c67fcf3829c] [world 2f1906870a] (2026-11-03T03:54:55Z)
- (step 3) `python3 plugin/tests/run.py test_site_landing test_site test_site_hero` → exit 0 · Ran 53 tests in 5.3s (24 classes, 16 at a time; slowest: Header 5s, Landing 5s, Landing 2s) / OK [ran] [tree 9c67fcf3829c] [world 2f1906870a] (2026-11-03T03:55:03Z)
- (step 4) `python3 plugin/tests/run.py test_site_landing test_site test_site_hero test_site_sampo test_site_build test_rename_scan 2>&1 | tail -3` → exit 0 · Ran 55 tests in 10.1s (25 classes, 16 at a time; slowest: Landing 9s, Header 7s, Landing 5s) / OK [ran] [tree e6e8e02893fa] [world 2f1906870a] (2026-11-03T04:01:03Z)
- (step 4) `python3 plugin/tests/run.py test_site_landing test_site test_site_hero test_site_sampo test_site_build test_rename_scan` → exit 0 · Ran 55 tests in 9.9s (25 classes, 16 at a time; slowest: Landing 9s, Header 7s, Landing 6s) / OK [ran] [tree e6e8e02893fa] [world 2f1906870a] (2026-11-03T04:01:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_map test_moonshot test_motion_verify test_replay test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.03s] [ran] [tree e6e8e02893fa] [world 2f1906870a] (2026-11-03T04:02:37Z)
- (step 1) `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 8 tests in 6.3s (1 classes, 16 at a time; slowest: Landing 6s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:23Z)
- (ac 1) `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 8 tests in 6.1s (1 classes, 16 at a time; slowest: Landing 6s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:38Z)
- (ac 2) `python3 plugin/tests/run.py test_site_landing test_site test_site_hero` → exit 0 · Ran 54 tests in 5.5s (24 classes, 16 at a time; slowest: Header 5s, Landing 5s, Landing 2s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:44Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:45Z)
- (step 2) `python3 plugin/tests/run.py test_site_landing test_site_sampo test_site_build` → exit 0 · Ran 31 tests in 4.6s (11 classes, 16 at a time; slowest: Landing 4s, Landing 2s, Reproducible 1s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:50Z)
- (step 3) `python3 plugin/tests/run.py test_site_landing test_site_sampo test_site_build` → exit 0 · Ran 31 tests in 4.6s (11 classes, 16 at a time; slowest: Landing 4s, Landing 2s, Reproducible 1s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:04:55Z)
- (step 4) `python3 plugin/tests/run.py test_site_landing test_site_sampo test_site_build` → exit 0 · Ran 31 tests in 4.5s (11 classes, 16 at a time; slowest: Landing 4s, Landing 1s, Reproducible 1s) / OK [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:05:00Z)
- (ac 1) `python3 plugin/tests/run.py test_site_landing` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T04:04:38Z [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:05:12Z)
- (ac 2) `python3 plugin/tests/run.py test_site_landing test_site test_site_hero` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T04:04:44Z [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:05:12Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T04:04:45Z [ran] [tree d25566c1391b] [world 2f1906870a] (2026-11-03T04:05:12Z)
- (audit intent) `read the lane's diff (site.js fire(), build.py dials, index.html hero/forge/myth, style.css motion rules) and took my own real-time shots at 1280 dark and 320 light after the animations settle, plus virtual-time shots at 1280/320/768 light, dark and reduced` → the hero mill turns over the forge shader, runes write the headline, the dials read stats.json (1,662 tasks, 7,390 evidence runs), the forge scene and the myth paragraph once — SAMPO.md's landing as asked; shots show it settled and whole [tree d25566c1391b] (2026-11-03T04:05:12Z)
- (audit edge) `read the lane's diff (site.js fire(), build.py dials, index.html hero/forge/myth, style.css motion rules) and took my own real-time shots at 1280 dark and 320 light after the animations settle, plus virtual-time shots at 1280/320/768 light, dark and reduced` → 320 px stacks hero then mill and dials with no sideways scroll; reduced motion shows the still mark and no canvas; a failed WebGL link throws inside the try and leaves the CSS glow; the shader rests at --autoplay-limit (code read; no test runs a clock) [tree d25566c1391b] (2026-11-03T04:05:12Z)
- (audit maintainer) `read the lane's diff (site.js fire(), build.py dials, index.html hero/forge/myth, style.css motion rules) and took my own real-time shots at 1280 dark and 320 light after the animations settle, plus virtual-time shots at 1280/320/768 light, dark and reduced` → the shader is one 60-line function in site.js reading theme colours from CSS tokens, so tokens.json stays the one source; the dials' --v comes from build.py, one formula log10(n)/5 [tree d25566c1391b] (2026-11-03T04:05:12Z)
## Log
- 2026-11-03T03:29:55Z created
- 2026-11-03T03:30:04Z set approved=True
- 2026-11-03T03:30:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2759.builder.md
- 2026-11-03T03:30:20Z focused
- 2026-11-03T03:30:21Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T04:04:01Z merged worktree-agent-af8cefd0b7eafab5c (7 file(s))
- 2026-11-03T04:04:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af8cefd0b7eafab5c
- 2026-11-03T04:04:02Z focused
- 2026-11-03T04:04:16Z scope: CHANGELOG.md — the landing's line (step 4)
- 2026-11-03T04:05:50Z done
- 2026-11-03T04:05:51Z committed 17c64184 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2753 [FEATURE M, active, 4 steps] The site takes Sampo's design system (T-2742 step 7a): style.css reads design/sampo/tokens.json, the Runestone mark and its variants …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- decision 2026-11-03: [revisited: Sampo's logo is the Runestone direction] [check: python3 plugin/tests/run.py test_sampo_design] Sampo's logo is the Runestone direction …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Lessons
- headless --virtual-time-budget leaves CSS staggers half-done; check a hero's settled state with a real-time Playwright shot (executable_path to the installed headless shell)
## Plan gaps
- failed first: step 1 red test_site_landing: no external hosts, a reduced-motion rule for each animation, a noscript-comp…
## Files touched
- plugin/tests/test_site_landing.py
- site/index.html
- site/build.py
- site/style.css
- site/site.js
- .fm-scratch/shots.py
- CHANGELOG.md
- site/assets/mark-animated.svg
- site/assets/mark.svg
