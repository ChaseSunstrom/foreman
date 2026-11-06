---
id: T-2747
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:58:38Z
updated: 2026-11-03T01:44:23Z
builder_model: sonnet
base: 70f2b836f4bbf5a8e1082dc127f2805e1924bf81
base_tree: fd1ccc3fce887568fddf42ea09a8469b9e709037
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T00:59:00Z
plan0_scope: []
inferred_deps: [T-2742]
inferred_why: T-2742: named in its request
group: Sampo rename and its steps
lane_stop: merged 2026-11-03T01:43:11Z
verified: strong
unproven: [meaning, ui-unshot]
---
# Sampo's design system and three logo directions (SAMPO.md, Design): tokens (palette, type, motion rules) one source every surface reads, and three distinct logo directions each with the full mark, a 16 px icon, monochrome, wordmark and an animated mark with its still, plus a preview page; the pick waits for a cold design review (T-2742 step 6)
## Raw request
> Sampo's design system and three logo directions (SAMPO.md, Design): tokens (palette, type, motion rules) one source every surface reads, and three distinct logo directions each with the full mark, a 16 px icon, monochrome, wordmark and an animated mark with its still, plus a preview page; the pick waits for a cold design review (T-2742 step 6)
## Interpretation
Reading 1 (chosen): SAMPO.md's Design: ancient northern forge and Kalevala myth fused with brass-and-gear machinery and modern tech (a rune-carved millstone that is a precision engine; hammered bronze and iron, forge light, runes, gears, blueprint linework, terminal-crisp type), never generic fantasy and never generic SaaS. This lane makes the shared tokens and three distinct logo directions with every required variant; the pick is made later by a cold design review, then the variants for favicon, app icon, README header, share image and pane glyph follow. Reading 2 (ruled out): pick one direction now. Ruled out: SAMPO.md asks for at least three, picked by a cold review.
## Assumptions (confidence)
## Acceptance criteria
- [x] design/sampo/tokens.json holds light and dark palettes, type and motion rules, and every color pair it names for text passes WCAG AA — verify with `python3 plugin/tests/run.py test_sampo_design`
- [x] three directions under design/sampo/directions/ each have mark.svg, icon-16.svg, mono.svg, wordmark.svg and mark-animated.svg with a reduced-motion still, all well-formed SVG that loads nothing from other hosts — verify with `python3 plugin/tests/run.py test_sampo_design`
## Non-goals
## Approach (options → choice → why)
1. Hand-authored SVG per direction (geometry, not raster), tokens.json as the one source, a static preview page with both themes and a reduced-motion still; the test parses each SVG, checks variants exist, no external hrefs, and checks text color pairs for AA. Likely outcome: three folders of five SVGs and one tokens file. Fails if: an SVG's animation lacks a still; the test requires one.
2. Raster logos from an image model. Fails if: nothing here generates images, and a raster mark can't stay crisp at 16 px or animate cheaply.
3. Use what exists: the directions skill's cards, fm looks' measured palettes and contrast test, site/assets' current SVG as the size and structure reference. Likely outcome: directions drawn from the look bank, not invented palettes.
4. Do less: one direction. Fails if: SAMPO.md asks for three and a cold pick.
Choice 1 on 3 (80%).
## Risks and rollback
New files only under design/sampo; nothing replaces the current logo until the review picks. Rollback: delete the folder.
Blast radius (fm graph blast): unknown, no co-change history for SAMPO.md.
## Execution prompt
## Steps
1. [x] read SAMPO.md's Design section, the directions skill and fm looks; draft the three directions as cards
2. [x] tokens.json and the three directions' SVGs
3. [x] preview page design/sampo/index.html and the test
## Resume here
<!-- auto -->
- 2026-11-03T01:22:16Z step 3/3: preview page design/sampo/index.html and the test
- git: worktree-agent-a2beaf3571493e4e0; 2 uncommitted: design/, plugin/tests/test_sampo_design.py
- touched since last checkpoint: design/sampo/directions/runestone/mark-animated.svg, design/sampo/directions/runestone/README.md, design/sampo/directions/orrery/mark.svg, design/sampo/directions/orrery/mark-animated.svg, design/sampo/directions/orrery/icon-16.svg, design/sampo/directions/orrery/mono.svg, design/sampo/directions/orrery/wordmark.svg, design/sampo/directions/orrery/README.md, design/sampo/directions/emberline/mark.svg, design/sampo/directions/emberline/mark-animated.svg, design/sampo/directions/emberline/icon-16.svg, design/sampo/directions/emberline/mono.svg, design/sampo/directions/emberline/wordmark.svg, design/sampo/directions/emberline/README.md, design/sampo/index.html
## Docs impact
none: design assets under design/sampo, on no surface until the review's pick
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -8` → ✗ exit 1 · Ran 12 tests in 1.4s (3 classes, 16 at a time; slowest: Directions 0s, Tokens 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree 5f9d48a2e41c] [world 2f1906870a] (2026-11-03T01:03:23Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -8` → ✗ exit 1 · Ran 12 tests in 1.4s (3 classes, 16 at a time; slowest: Directions 0s, Tokens 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree 5f9d48a2e41c] [world 2f1906870a] (2026-11-03T01:03:23Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -40` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ac42e7e53305] [world 2f1906870a] (2026-11-03T01:05:01Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -40` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ac42e7e53305] [world 2f1906870a] (2026-11-03T01:05:01Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | grep -B2 -A12 "test_sampo_design.Tokens" | head -60` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ac42e7e53305] [world 2f1906870a] (2026-11-03T01:05:03Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | grep -B2 -A12 "test_sampo_design.Tokens" | head -60` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (3 classes: test_sampo_design.Tokens, test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ac42e7e53305] [world 2f1906870a] (2026-11-03T01:05:03Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|====)|Error:" | head -30` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (2 classes: test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ceff1c50309a] [world 2f1906870a] (2026-11-03T01:05:30Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|====)|Error:" | head -30` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (2 classes: test_sampo_design.Directions, test_sampo_design.Preview) [ran] [tree ceff1c50309a] [world 2f1906870a] (2026-11-03T01:05:30Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -25` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (1 classes: test_sampo_design.Preview) [ran] [tree bf9b5a137d75] [world 2f1906870a] (2026-11-03T01:21:06Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -25` → ✗ exit 1 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / FAILED (1 classes: test_sampo_design.Preview) [ran] [tree bf9b5a137d75] [world 2f1906870a] (2026-11-03T01:21:06Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design.Tokens test_sampo_design.Directions 2>&1 | tail -4` → exit 0 · Ran 11 tests in 0.3s (2 classes, 16 at a time; slowest: Tokens 0s, Directions 0s) / OK [ran] [tree bf9b5a137d75] [world 2f1906870a] (2026-11-03T01:21:10Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design.Tokens test_sampo_design.Directions` → exit 0 · Ran 11 tests in 0.3s (2 classes, 16 at a time; slowest: Tokens 0s, Directions 0s) / OK [ran] [tree bf9b5a137d75] [world 2f1906870a] (2026-11-03T01:21:11Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree f00f7954946f] [world 2f1906870a] (2026-11-03T01:23:33Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_sampo_design && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.14s] [ran] [tree f00f7954946f] [world 2f1906870a] (2026-11-03T01:23:47Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:29Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.4s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:29Z)
- (step 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.4s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:30Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.3s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:31Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 12 tests in 0.4s (3 classes, 16 at a time; slowest: Tokens 0s, Directions 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:32Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T01:43:32Z [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:39Z)
- (ac 2) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T01:43:32Z [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:39Z)
- `python3 plugin/tests/run.py test_sampo_design test_rename_scan` → exit 0 · Ran 14 tests in 0.4s (4 classes, 16 at a time; slowest: RenameScan 0s, Tokens 0s, Preview 0s) / OK [ran] [tree 6205133e8f1d] [world 2f1906870a] (2026-11-03T01:43:39Z)
- (audit intent) `rendered all three marks and icons and looked at them: runestone (rune ring around a forge-lit millstone core) is closest to the brief, orrery (gear around blueprint orbits) reads mechanical, emberline (monoline ring with pixel sparks) reads as a letter Q; tokens pass AA for every named text pair; nothing loads from other hosts; the pick and its fixes come from a cold design review on fable (running)` → SAMPO.md asks for at least three directions picked by a cold review; three exist, none is picked here [tree 6205133e8f1d] (2026-11-03T01:43:39Z)
- (audit edge) `rendered all three marks and icons and looked at them: runestone (rune ring around a forge-lit millstone core) is closest to the brief, orrery (gear around blueprint orbits) reads mechanical, emberline (monoline ring with pixel sparks) reads as a letter Q; tokens pass AA for every named text pair; nothing loads from other hosts; the pick and its fixes come from a cold design review on fable (running)` → index.html copies token colours by hand (drift risk, noted for the pick's build); the animated marks are checked by their CSS text, not a rendered frame [tree 6205133e8f1d] (2026-11-03T01:43:39Z)
- (audit adversary) `rendered all three marks and icons and looked at them: runestone (rune ring around a forge-lit millstone core) is closest to the brief, orrery (gear around blueprint orbits) reads mechanical, emberline (monoline ring with pixel sparks) reads as a letter Q; tokens pass AA for every named text pair; nothing loads from other hosts; the pick and its fixes come from a cold design review on fable (running)` → tokens.json is plain data (colours, font stacks, durations) with no URLs or code; the SVGs carry no scripts, no external hrefs and no foreignObject (test_sampo_design.outside checks hrefs) [tree 6205133e8f1d] (2026-11-03T01:43:39Z)
## Log
- 2026-11-03T00:58:38Z created
- 2026-11-03T00:58:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2747.builder.md
- 2026-11-03T00:58:59Z focused
- 2026-11-03T00:59:00Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T01:43:11Z merged worktree-agent-a2beaf3571493e4e0 (21 file(s))
- 2026-11-03T01:43:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2beaf3571493e4e0
- 2026-11-03T01:43:27Z focused
- 2026-11-03T01:44:23Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- T-2087 [FIX M, done, 3 steps] Genesis page matches the site: shared header, footer and style.css tokens — lesson: A sub-page that loads the site stylesheet inherits its …
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- the similar finished task took 3 steps
## Lessons
- Render every mark at its real sizes and look before a review: a ring with a tail reads as a letter at a glance
## Files touched
- plugin/tests/test_sampo_design.py
- design/sampo/tokens.json
- design/sampo/directions/runestone/mark.svg
- design/sampo/directions/runestone/mark-animated.svg
- design/sampo/directions/runestone/icon-16.svg
- design/sampo/directions/runestone/mono.svg
- design/sampo/directions/runestone/wordmark.svg
- design/sampo/directions/runestone/README.md
- design/sampo/directions/orrery/mark.svg
- design/sampo/directions/orrery/mark-animated.svg
- design/sampo/directions/orrery/icon-16.svg
- design/sampo/directions/orrery/mono.svg
- design/sampo/directions/orrery/wordmark.svg
- design/sampo/directions/orrery/README.md
- design/sampo/directions/emberline/mark.svg
- design/sampo/directions/emberline/mark-animated.svg
- design/sampo/directions/emberline/icon-16.svg
- design/sampo/directions/emberline/mono.svg
- design/sampo/directions/emberline/wordmark.svg
- design/sampo/directions/emberline/README.md
- design/sampo/index.html
