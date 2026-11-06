---
id: T-3210
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/tests/fixtures/golden.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tools/shot.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T13:57:50Z
updated: 2026-11-05T18:13:27Z
builder_model: opus
base: 2209f680fb93c642ffe55a0e6215658abd550a4f
base_tree: 398301880bbb80fe42e84882b58157c12d49d4ae
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T15:25:29Z
plan0_scope: []
builder_returned: 2026-11-05T15:33:46Z
lane_stop: merged 2026-11-05T17:47:59Z
verified: strong
unproven: [meaning, ui-unshot]
lane_verified: 46c00bc441374051aaa168c6c0a7fd2bb09e4945
---
# The crest's Sampo mark reads muddy at half-block resolution (anti-aliased downscale…
## Raw request
> The crest's Sampo mark reads muddy at half-block resolution (anti-aliased downscale leaves grey noise at its base, ~10 cells wide in a 7-row box): redraw it crisp: threshold to a clean silhouette of 3-4 tones, use the box's height, keep the flame; judge from shot.py shots in both widths (Opus, UI routing)
## Interpretation
Reading 1 (chosen): the crest's Sampo mark (MARK_TOKENS in mods/foreman-ui/hooks/kit.ts, a 12x12 px half-block raster of design/sampo/logo/mark-simple.svg) carries anti-aliased in-between shades, so at terminal size it reads as a muddy mosaic with grey noise at its base; redraw it crisp. Reading 2 (ruled out): replace the mark with a different logo; the user asked for the Sampo logo, so the mark stays and only its rendering changes.
## Assumptions (confidence)
## Acceptance criteria
- [x] the 12 px and 6 px marks use at most 4 distinct colours each, no cell is an in-between shade of two neighbours, and the mod's crest tests pass — verify with `claude plugin test mods/foreman-ui`
- [x] shots of the crest (shot.py, idle and working, 200 and 150 columns) read as a clean mill-and-flame silhouette with no grey noise at the base, filed in research as crest-shots-2 — verify with `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/crest-shots-2.md`
## Non-goals
## Approach (options → choice → why)
1) use what exists: re-rasterise mark-simple.svg with a palette of 3-4 tones (flame gold/orange, the mill's body, its shadow) and hard edges (no anti-aliasing), hand-correct stray pixels, and use the box's full height where the dock allows; likely outcome: a clean, recognisable mill-and-flame silhouette. 2) braille or sextant cells for finer detail: fails if: one fg colour per cell flattens the flame's two colours. 3) a larger mark only: fails if: the noise grows with it. 4) do less: drop the base row that holds most of the noise: fails if: the mark loses its foot and reads as a floating flame. Choice 1 (80%): the noise is the anti-aliasing, so a posterised, hand-tuned raster fixes it at its cause.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: the mark's palette has at most 4 colours and no in-between shades
2. [x] re-rasterise and hand-tune both marks
3. [x] shots in the harness, filed as research crest-shots-2 (sampo research add)
## Resume here
## Docs impact
CHANGELOG line; research crest-shots-2
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 174 tests across 6 files. [21.92s] [ran] [tree f17013de9ef9] [world 2f1906870a] (2026-11-05T15:27:56Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.99s] [ran] [tree 676be3c8d8f7] [world 2f1906870a] (2026-11-05T15:30:49Z)
- (step 3) `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/crest-shots-2.md` → exit 0 · (no output) [ran] [tree b08e6e2a58e1] [world 2f1906870a] (2026-11-05T15:32:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_claims test_cli test_code_tui test_design_surfaces test_docsdrift test_doctor test_left_out test_models test_plugins test_rename_scan test_settings test_shot test_suite_hygiene test_supply_delta test_ui test_ui_replay && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [11.90s] [ran] [tree b08e6e2a58e1] [world 2f1906870a] (2026-11-05T15:33:27Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 174 tests across 6 files. [51.69s] [ran] [tree 4446da47039e] [world 2f1906870a] (2026-11-05T17:50:12Z)
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 174 tests across 6 files. [35.47s] (start tree + this task's tests) [ran] [tree 4446da47039e] [world 2f1906870a] (2026-11-05T17:51:22Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 174 tests across 6 files. [26.80s] [ran] [tree 4446da47039e] [world 2f1906870a] (2026-11-05T17:51:22Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:51:22Z [ran] [tree 4446da47039e] [world 2f1906870a] (2026-11-05T17:51:34Z)
- (ac 2) `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/crest-shots-2.md` → exit 0 · (no output) [ran] [tree 4446da47039e] [world 2f1906870a] (2026-11-05T17:51:34Z)
- (audit intent) `lane diff reviewed in a design pass before merge; shots filed as crest-shots-2; merged by the queue, post-merge verify green` → both marks are hand-tuned pixel art in at most 4 flat tones, no in-between shades [tree 4446da47039e] (2026-11-05T17:51:34Z)
- (audit design) `lane diff reviewed in a design pass before merge; shots filed as crest-shots-2; merged by the queue, post-merge verify green` → shots at 200 and 150 columns, idle and working, read as a clean mill-and-flame silhouette [tree 4446da47039e] (2026-11-05T17:51:34Z)
- (audit edge) `lane diff reviewed in a design pass before merge; shots filed as crest-shots-2; merged by the queue, post-merge verify green` → the 6 px mark keeps the flame distinct from the stone at half-block resolution [tree 4446da47039e] (2026-11-05T17:51:34Z)
- (audit self) `lane diff reviewed in a design pass before merge; shots filed as crest-shots-2; merged by the queue, post-merge verify green` → no findings [tree 4446da47039e] (2026-11-05T17:51:34Z)
## Log
- 2026-11-05T13:57:50Z created
- 2026-11-05T14:14:50Z set tier=S
- 2026-11-05T14:14:51Z planned: it has criteria and steps
- 2026-11-05T14:14:52Z set approved=True
- 2026-11-05T15:25:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3210.builder.md
- 2026-11-05T15:25:28Z focused
- 2026-11-05T15:25:29Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T17:47:59Z merged worktree-agent-a506d9519135dded0 (4 file(s))
- 2026-11-05T17:49:04Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a506d9519135dded0
- 2026-11-05T17:49:14Z focused
- 2026-11-05T17:50:17Z set scope=['mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/tests/fixtures/golden.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/tools/shot.py', 'CHANGELOG.md']
- 2026-11-05T17:50:17Z scope: the files the merge 46c00bc4 changed, plus the CHANGELOG line
- 2026-11-05T17:51:38Z affected tests waived: merged lane; the post-merge verify already ran the full suite
- 2026-11-05T17:51:42Z done
- 2026-11-05T17:51:48Z committed 300e0783 (1 file)
- 2026-11-05T18:13:27Z verified: the full suite is green on 46c00bc44
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research crest-shots: Taken 2026-11-05 after the merge, with mods/foreman-ui/tools/shot.py: Claude Code 2.1.318 in a tmux harness with the merged mod, in a scratch folde…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2853 [FEATURE S, done, 2 steps] Port 12's palette to the panel (the foreman-ui mod's colours) and the share card (design/sampo/logo/share.svg and share.png, 1200x630),…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Why not caught
a palette-count test on the mark, now in the mod's tests
## Lessons
- tiny terminal marks must be drawn as pixel art in a fixed palette; a downscale always leaves grey noise
## Plan gaps
- failed first: step 1 failing test: the mark's palette has at most 4 colours and no in-between shades
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- .fm-scratch/notes.md
- .fm-scratch/mark.py
- .fm-scratch/edit.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/fixtures/golden.ts
- .fm-scratch/crop.py
- mods/foreman-ui/tools/shot.py
- .fm-scratch/crest-shots-2.md
- CHANGELOG.md
