---
id: T-2751
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T01:45:24Z
updated: 2026-11-03T03:06:46Z
builder_model: sonnet
base: 3defe6f63d2f982119749c0d1575dabe1e074e2d
base_tree: 56486740dbca53ce5abffcf68e83a2a6506e040e
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T01:45:47Z
plan0_scope: []
lane_stop: merged 2026-11-03T02:37:09Z
verified: strong
unproven: [docs, meaning]
---
# Runestone ships: the cold design review's fixes (a redrawn 16 px icon of dark disc, bronze rim and hot eye crossed by the rynd bar; lighter curved harp furrows; runes that read as no Latin letter; no centre dot; a wordmark in the display face; sparks from the rim; a full turn before it settles; a parchment light variant) and every variant (favicon, app icon, README header, share image, pane glyph, Desktop icon) (T-2742 step 6)
## Raw request
> Runestone ships: the cold design review's fixes (a redrawn 16 px icon of dark disc, bronze rim and hot eye crossed by the rynd bar; lighter curved harp furrows; runes that read as no Latin letter; no centre dot; a wordmark in the display face; sparks from the rim; a full turn before it settles; a parchment light variant) and every variant (favicon, app icon, README header, share image, pane glyph, Desktop icon) (T-2742 step 6)
## Interpretation
Reading 1 (chosen): apply every finding the cold review (fable) raised on Runestone, then derive each variant SAMPO.md's Logo paragraph names; a second cold review must find no HIGH issue before it replaces the hard hat anywhere. Reading 2 (ruled out): ship the drafts and fix later. Ruled out: SAMPO.md says it doesn't ship until the review passes.
## Assumptions (confidence)
## Acceptance criteria
- [x] design/sampo/logo/ holds the refined mark, icon-16, mono, wordmark, animated mark with its still, a light variant, favicon.svg and .ico, app icons at 512 and 1024, readme-header.svg, share.png at 1200x630, a pane glyph and a Desktop icon, all well-formed and loading nothing from other hosts — verify with `python3 plugin/tests/run.py test_sampo_design`
- [x] a second cold design review on fable passes the refined mark (no HIGH finding) — verify with `test -f design/sampo/logo/REVIEW.md && grep -q 'Verdict: pass' design/sampo/logo/REVIEW.md`
## Non-goals
## Approach (options → choice → why)
1. Hand-edit the Runestone SVGs per finding, redraw the 16 px icon as its own geometry, rasterise app icons and the share image with rsvg-convert from the SVGs, and look at renders at 16, 32, 64 and 512 px before the second review. Likely outcome: one logo folder, PNG variants generated from SVG sources. Fails if: the second review raises a new HIGH; then fix and review again.
2. Scale the full mark down for the icon. Fails if: the review showed a scaled mark reads as a brightness toggle at 16 px.
3. Use what exists: the Runestone files, tokens.json's roles, rsvg-convert for rasters, test_sampo_design for the checks. Likely outcome: no new tooling.
4. Do less: fix only the HIGH findings. Fails if: the MEDIUM ones (furrows, runes as letters, the lens dot) are what an art director rejects next.
Choice 1 on 3 (80%).
## Risks and rollback
New files under design/sampo/logo; the hard hat is replaced on surfaces only in the visible-surfaces and site steps. Rollback: delete the folder.
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py.
## Execution prompt
## Steps
1. [x] the review's fixes on the Runestone files
2. [x] every variant
3. [x] renders at 16, 32, 64 and 512 px looked at; tests
## Resume here
<!-- auto -->
- 2026-11-03T02:27:39Z steps 3/3 done
- git: worktree-agent-a52414488f989efaa; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_sampo_design.py, .fm-scratch/zoom.py, .fm-scratch/build.py, design/sampo/logo/app-icon-1024.png, design/sampo/logo/app-icon-512.png, design/sampo/logo/app-icon.svg, design/sampo/logo/desktop-icon-1024.png, design/sampo/logo/desktop-icon.svg, design/sampo/logo/favicon.ico, design/sampo/logo/favicon.svg, design/sampo/logo/icon-16.svg, design/sampo/logo/mark-animated.svg, design/sampo/logo/mark-light.svg, design/sampo/logo/mark.svg, design/sampo/logo/mono.svg
## Docs impact
CHANGELOG.md; design/sampo/logo/README.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -15` → ✗ exit 1 · Ran 24 tests in 1.4s (4 classes, 16 at a time; slowest: Directions 0s, Tokens 0s, Logo 0s) / FAILED (1 classes: test_sampo_design.Logo) [ran] [tree 1a6ef3cdbd7c] [world 2f1906870a] (2026-11-03T01:58:50Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.4s (4 classes, 16 at a time; slowest: Tokens 0s, Logo 0s, Directions 0s) / OK [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:07:08Z)
- (step 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.4s (4 classes, 16 at a time; slowest: Tokens 0s, Logo 0s, Directions 0s) / OK [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:07:08Z)
- (step 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.3s (4 classes, 16 at a time; slowest: Tokens 0s, Logo 0s, Directions 0s) / OK [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:07:32Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.4s (4 classes, 16 at a time; slowest: Logo 0s, Tokens 0s, Directions 0s) / OK [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:07:34Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.3s (4 classes, 16 at a time; slowest: Logo 0s, Tokens 0s, Directions 0s) / OK [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:07:38Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_audit_run test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_lanes test_looks_gallery test_motion_score test_motion_verify test_receipts test_sampo_design && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.40s] [ran] [tree ffd27384350e] [world 2f1906870a] (2026-11-03T02:08:19Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 24 tests in 0.3s (4 classes, 16 at a time; slowest: Logo 0s, Tokens 0s, Directions 0s) / OK [ran] [tree 6e99ba8209f1] [world 2f1906870a] (2026-11-03T02:08:56Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 26 tests in 0.7s (4 classes, 16 at a time; slowest: Preview 0s, Logo 0s, Directions 0s) / OK [ran] [tree a8e79947c1fd] [world 2f1906870a] (2026-11-03T02:24:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_audit_run test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_lanes test_looks_gallery test_motion_score test_motion_verify test_receipts test_sampo_design && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.20s] [ran] [tree a8e79947c1fd] [world 2f1906870a] (2026-11-03T02:25:20Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → ✗ exit 1 · FAILED (1 classes: test_sampo_design.Logo) / ✗ exit 1 (0.9 s; last 19 of 19 lines) [ran] [tree 5be8650bb10d] [world 2f1906870a] (2026-11-03T02:29:40Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · ✓ exit 0 (1.6 s) · OK [ran] [tree ce6f29131749] [world 2f1906870a] (2026-11-03T02:31:47Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 27 tests in 1.0s (4 classes, 16 at a time; slowest: Logo 0s, Preview 0s, Tokens 0s) / OK [ran] [tree ce6f29131749] [world 2f1906870a] (2026-11-03T02:31:57Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_audit_run test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_lanes test_looks_gallery test_motion_score test_motion_verify test_receipts test_sampo_design && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [25.63s] [ran] [tree ce6f29131749] [world 2f1906870a] (2026-11-03T02:33:18Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 27 tests in 0.9s (4 classes, 16 at a time; slowest: Logo 0s, Preview 0s, Tokens 0s) / OK [ran] [tree 28ffc0e3492b] [world 2f1906870a] (2026-11-03T02:37:18Z)
- (ac 2) `test -f design/sampo/logo/REVIEW.md && grep -q 'Verdict: pass' design/sampo/logo/REVIEW.md` → exit 0 · (no output) [ran] [tree 28ffc0e3492b] [world 2f1906870a] (2026-11-03T02:37:19Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 27 tests in 1.6s (4 classes, 16 at a time; slowest: Logo 1s, Tokens 0s, Directions 0s) / OK [ran] [tree 83b5c05c4dc5] [world 2f1906870a] (2026-11-03T02:37:34Z)
- (ac 2) `test -f design/sampo/logo/REVIEW.md && grep -q 'Verdict: pass' design/sampo/logo/REVIEW.md` → exit 0 · (no output) [ran] [tree 83b5c05c4dc5] [world 2f1906870a] (2026-11-03T02:37:34Z)
- (audit intent) `reviewed 250ff2ad+494022fe: generator rebuild test byte-exact, 27 design tests green, wordmark render checked by eye after the font swap` → SAMPO.md Logo paragraph — 16 px icon, mono, wordmark, animated+still, every listed variant, three directions picked by cold review (REVIEW.md pass on fable) [tree 83b5c05c4dc5] (2026-11-03T02:37:34Z)
- (audit edge) `reviewed 250ff2ad+494022fe: generator rebuild test byte-exact, 27 design tests green, wordmark render checked by eye after the font swap` → icon-16 is its own drawing at 16 px, not a downscale; share.png 1200x630; light variant on parchment [tree 83b5c05c4dc5] (2026-11-03T02:37:34Z)
- (audit adversary) `reviewed 250ff2ad+494022fe: generator rebuild test byte-exact, 27 design tests green, wordmark render checked by eye after the font swap` → SVGs carry no scripts, no external hrefs, no foreignObject (test_sampo_design checks); font licence moved off AGPL to GUST/LPPL [tree 83b5c05c4dc5] (2026-11-03T02:37:34Z)
## Log
- 2026-11-03T01:45:24Z created
- 2026-11-03T01:45:36Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2751.builder.md
- 2026-11-03T01:45:45Z focused
- 2026-11-03T01:45:47Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T02:37:09Z merged worktree-agent-a52414488f989efaa (23 file(s))
- 2026-11-03T02:37:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a52414488f989efaa
- 2026-11-03T02:37:12Z focused
- 2026-11-03T02:37:30Z scope: CHANGELOG.md line for the logo; build.py/README.md/glyphs.json font swap (P052 AGPL → Pagella GUST) inside design/sampo/logo
- 2026-11-03T02:39:01Z done
- 2026-11-03T02:39:07Z committed 8aa8ad27 (1 file)
- 2026-11-03T02:40:56Z guard authorization added: publish
- 2026-11-03T03:06:46Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2747 [FEATURE M, done, 3 steps] Sampo's design system and three logo directions (SAMPO.md, Design): tokens (palette, type, motion rules) one source every surface reads…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (draft at least three directions, pick by a cold design review)] Sampo's logo is the Runestone direction (a rune r…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- the similar finished task took 3 steps
## Lessons
- A builder's 'someone should confirm the licence' is a decision to make before the merge: swap to a permissive source of the same design (Pagella for P052) rather than carry the question
## Files touched
- plugin/tests/test_sampo_design.py
- .fm-scratch/build.py
- design/sampo/logo/app-icon-1024.png
- design/sampo/logo/app-icon-512.png
- design/sampo/logo/app-icon.svg
- design/sampo/logo/desktop-icon-1024.png
- design/sampo/logo/desktop-icon.svg
- design/sampo/logo/favicon.ico
- design/sampo/logo/favicon.svg
- design/sampo/logo/icon-16.svg
- design/sampo/logo/mark-animated.svg
- design/sampo/logo/mark-light.svg
- design/sampo/logo/mark.svg
- design/sampo/logo/mono.svg
- design/sampo/logo/readme-header-dark.svg
- design/sampo/logo/readme-header-light.svg
- design/sampo/logo/share.png
- design/sampo/logo/share.svg
- design/sampo/logo/wordmark.svg
- design/sampo/logo/pane-glyph.txt
- design/sampo/logo/REVIEW.md
- design/sampo/directions/runestone/README.md
- design/sampo/logo/README.md
- .fm-scratch/zoom.py
- design/sampo/logo/build.py
- design/sampo/logo/glyphs.json
- CHANGELOG.md
