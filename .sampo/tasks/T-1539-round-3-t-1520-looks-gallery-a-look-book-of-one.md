---
id: T-1539
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, site, plugin/skills/library/cards/looks, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:48Z
updated: 2026-10-22T20:59:28Z
---
# Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second po
## Raw request
> Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second posters, a shader sketchbook with live thumbnails, a tested shader-recipe set, style dice, a sentence that rolls the theme, a reversible look as one transaction, looks as trading cards, and a gallery where every design playbook has a reproducible example (a152 c112 a024 a161 a050 a112 a157 a132 b100 a023 a038 a100). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second posters, a shader sketchbook with live thumbnails, a tested shader-recipe set, style dice, a sentence that rolls the theme, a reversible look as one transaction, looks as trading cards, and a gallery where every design playbook has a reproducible example (a152 c112 a024 a161 a050 a112 a157 a132 b100 a023 a038 a100). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm design roll picks a coherent look from the cards (seeded) and applies it as one reversible patch; the gallery page builds with a specimen per look — verify with `cd plugin/tests && python3 -m unittest test_looks_gallery`
## Non-goals
## Approach (options → choice → why)
Options: a static gallery page; chosen: a looks gallery built from the look and shader cards (T-1498, T-1499): each look a one-file living specimen with a 3-second poster, a shader sketchbook with live thumbnails, style dice and 'a sentence rolls the theme' (fm design roll), a look applied as one reversible transaction (a patch over the token file), trading-card export; shown on the site and as an fm page artifact.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] roll and reversible apply
3. [ ] specimens and gallery page
4. [ ] shader sketchbook
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:48Z created
- 2026-10-22T18:05:57Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'site', 'plugin/skills/library/cards/looks', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md']
- 2026-10-22T20:59:28Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1539
## Follow-ups captured
