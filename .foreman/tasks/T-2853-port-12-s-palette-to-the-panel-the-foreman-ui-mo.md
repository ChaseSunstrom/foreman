---
id: T-2853
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: [T-2850]
source: user
created: 2026-11-03T22:18:03Z
updated: 2026-11-04T00:13:19Z
base_note: Calibration: this plan states Choice 75% where FEATURE S closes (249) held on the first finish 100% of the time: 25 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
inferred_deps: [T-2851]
inferred_why: T-2851: panel and card palette must match the ported site
group: port the illustrated forge look
base: ba3105064bb04ec4a9a26ee9c58c755f3ef0355a
base_tree: 1669eecd36d86afd47304363c9fd5fed087d0082
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T00:10:34Z
plan0_scope: []
verified: strong
unproven: [tui-unshot, ui-unshot]
---
# Port 12's palette to the panel (the foreman-ui mod's colours) and the share card (design/sampo/logo/share.svg and share.png, 1200x630), so the pane, band and card match the site
## Raw request
> Port 12's palette to the panel (the foreman-ui mod's colours) and the share card (design/sampo/logo/share.svg and share.png, 1200x630), so the pane, band and card match the site
## Interpretation
Reading 1 (chosen): the pane and band (mods/foreman-ui/hooks/kit.ts's C and PALETTES.default) take the forge palette from design/sampo/tokens.json's night theme and 12's fire colours: running rows in the fire's gold, reading rows in the blue flame, ok, warn and error from the site's status tokens, edits in orange, agents in violet. Meanings, the cb and riso palettes and saved custom palettes keep working. The share card already shipped in T-2850. Reading 2 (ruled out): add a 'forge' palette beside the default and leave the default as it is; the user asked for the theme on every surface, so the default is what changes.
## Assumptions (confidence)
## Acceptance criteria
- [x] kit.ts's default palette is the forge palette from tokens.json, every text colour reads at 4.5:1 on a dark terminal, and the meaning pairs stay apart — verify with `python3 plugin/tests/run.py test_design_surfaces`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: map C's default entries onto 12's named tokens (accent=blue #6E9BFF, accent2=gold #FFC24D, ok=green #45E0A0, err=red #FF6A4A, edit=orange #FF9440, agent=violet #BC8BFF, warn=brass-2 #F0D392, muted=#9097BC, track=plate #10173D), and pin that with one test reading tokens.json. Likely outcome: the pane matches the site with a 15-line diff. Fails if a pair collides on a real terminal (warn vs accent2) or a colour drops under 4.5:1 on a typical #1e1e1e background; the test checks both.
2. Add a 'forge' palette next to default/cb/riso and leave default alone. Likely outcome: no change for anyone. Fails the ask: the theme is meant to be the default everywhere.
3. Do less: change accent and accent2 only. Likely outcome: a partial match. Fails if the rows still read as the old cyan-and-pink kit.
Choice 1 (75%): it is the default the user asked for, it is checked for contrast and distinctness, and BASE plus the saved-palette path keep custom palettes working.
## Risks and rollback
## Execution prompt
## Steps
1. [x] mod colours from tokens.json
2. [x] share.svg and share.png from 12
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · Ran 29 tests in 2.6s (9 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 47ac341859d9] [world 2f1906870a] (2026-11-04T00:12:31Z)
- `python3 plugin/tests/run.py test_design_surfaces.PaneForge` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: PaneForge 0s) / FAILED (1 classes: test_design_surfaces.PaneForge) (start tree + this task's tests) [ran] [tree 47ac341859d9] [world 2f1906870a] (2026-11-04T00:12:33Z)
- `python3 plugin/tests/run.py test_design_surfaces.PaneForge` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PaneForge 0s) / OK [ran] [tree 47ac341859d9] [world 2f1906870a] (2026-11-04T00:12:33Z)
- (ac 1) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T00:12:31Z [ran] [tree 47ac341859d9] [world 2f1906870a] (2026-11-04T00:12:34Z)
- (step 2) `python3 plugin/tests/run.py test_design_surfaces` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T00:12:31Z [ran] [tree 47ac341859d9] [world 2f1906870a] (2026-11-04T00:12:34Z)
- (audit edge) `self-review: C and PALETTES.default take tokens.json's night glow/success/warning/error/text-muted plus 12's blue, orange and violet flames; every text colour >=4.5:1 on #1e1e1e and on the forge night; the meaning pairs (running vs reading, ok vs err, err vs edit, skill vs err) >60 apart in RGB; cb and riso unchanged; the mod's 153 tests pass after the golden rewrite, whose diff moves colours only` → a saved custom palette still paints over the default (T-1717 tests, now pinned to PALETTES.default, not literals); a colourblind user's cb palette is untouched [tree 47ac341859d9] (2026-11-04T00:12:34Z)
- (audit intent) `self-review: C and PALETTES.default take tokens.json's night glow/success/warning/error/text-muted plus 12's blue, orange and violet flames; every text colour >=4.5:1 on #1e1e1e and on the forge night; the meaning pairs (running vs reading, ok vs err, err vs edit, skill vs err) >60 apart in RGB; cb and riso unchanged; the mod's 153 tests pass after the golden rewrite, whose diff moves colours only` → the share card (step 2) shipped with T-2850 [tree 47ac341859d9] (2026-11-04T00:12:34Z)
- (audit self) `self-review: C and PALETTES.default take tokens.json's night glow/success/warning/error/text-muted plus 12's blue, orange and violet flames; every text colour >=4.5:1 on #1e1e1e and on the forge night; the meaning pairs (running vs reading, ok vs err, err vs edit, skill vs err) >60 apart in RGB; cb and riso unchanged; the mod's 153 tests pass after the golden rewrite, whose diff moves colours only` → no findings [tree 47ac341859d9] (2026-11-04T00:12:34Z)
## Log
- 2026-11-03T22:18:03Z created
- 2026-11-03T22:18:10Z set depends_on=['T-2850']
- 2026-11-04T00:10:33Z step 2 (share card) shipped in T-2850: share.svg and share.png are 12's
- 2026-11-04T00:10:33Z criterion 1 verify: `python3 plugin/tests/run.py test_sampo_design test_site_build` → `python3 plugin/tests/run.py test_design_surfaces`
- 2026-11-04T00:10:33Z criterion 1 text: the mod's colour tokens come from 12's palette and the share card is 12's, rendered at 1200x630 → kit.ts's default palette is the forge palette from tokens.json, every text colour reads at 4.5:1 on a dark terminal, and the meaning pairs stay apart
- 2026-11-04T00:10:33Z focused
- 2026-11-04T00:10:34Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T00:13:17Z done
- 2026-11-04T00:13:19Z committed 105e6b03 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2757 [FEATURE M, done, 3 steps] Charts take Sampo's palette: tokens.json gains a six-series chart palette per theme (forge hues, distinguishable, AA 3:1 against the ch…
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- decision 2026-11-03: [revisited: fiery forge of direction 2] [cites: user steer 2026-11-03: fiery forge/anvil, no mill, completely redesigned, many fire colours like blu…
## Why not caught
none: a theme port
## Files touched
- plugin/tests/test_design_surfaces.py
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/tests/fixtures/golden.ts
