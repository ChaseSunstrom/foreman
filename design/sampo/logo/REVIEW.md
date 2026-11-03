Verdict: pass (second cold review, fable)

The second cold review found no HIGH finding. Its findings were fixed before the merge (T-2751). Each finding of both
reviews is listed below with its answer.

## First review: what it asked, and where it was answered

| Finding | Severity | Answer |
|---|---|---|
| The 16 px icon reads as an OS brightness toggle | HIGH | icon-16.svg is its own drawing: a dark disc, a bronze rim, a hot eye and a 1 px rynd bar, no ticks |
| The furrows are near-invisible | MEDIUM | #4A5160 (2.2:1 on the disc), curved, eight harps of a master furrow and a shorter parallel one |
| Runes read as Latin letters (22.5°, 247.5°, 292.5°; r5 as N, r8 algiz-like) | MEDIUM | first answered with staves notched by half-bars; the second review found those read as one repeated tally, so they were redrawn again (below) |
| The eye's dark centre dot | MEDIUM | dropped; the bar stays |
| The wordmark isn't in the display face | MEDIUM | SAMPO outlined from P052 Bold (font.display's metric-compatible Palatino), so it renders without the font |
| Sparks too small and from nowhere | LOW | r=2, launched from the rim at 310°, 322° and 334°, beside the last rune to light (337.5°) |
| The turn is too short to read as a mill | LOW | one and a quarter turns (450°) easing to rest in 4.2 s; nothing runs past it |
| No light variant | LOW | mark-light.svg and readme-header-light.svg: on parchment the disc takes the light theme's stone role |

## Second review (fable): what it asked, and where it was answered

| Finding | Severity | Answer |
|---|---|---|
| Six runes (r1, r2, r5, r6, r7, r8) are one construction: a repeated tally at 512 px, identical ticks at 64 px, Ogham rather than runic | MEDIUM | each has its own silhouette now: one branch (r1), opposed hooks (r2), a chevron off the stave (r5), a cross bar and a slant (r6), a bare stave (r7), a double chevron (r8); all radial. Checked at 512 and 64 px: each is tellable from its neighbours. A test fails if two runes share a drawing or more than one is a half-bar tally |
| The sparks fly against the clockwise spin | MEDIUM | they fly along the clockwise tangent: k1 (6.5, -5), k2 (7, -3.5), k3 (5, -6.5) px, launched at 2.9, 3.0 and 3.1 s, as r8 lights (2.88 s) and while the stone still turns. A test checks each flight against the tangent and the launch against r8 |
| icon-16's full-width bar reads as a circled minus | LOW | the bar is columns 5 to 10, a pixel short of the eye (4 to 12) at each end, so forge light shows past it; a test holds both ends inside the eye |
| The README's smallest full mark (48 px) is too small for the runes | LOW | 96 px, and below 96 px the icon |
| The animated title says "turns once round"; the light title speaks "(for parchment)" | LOW | "makes a turn and a quarter"; the light variant's title is the mark's own |
| The thorn (r4) reads as a cursor or map-pin wedge | LOW | a small bump mid-stave (from 6.6 to 9.4, 1.7 deep), the stave running past it at both ends |
| favicon.svg's bar sits on a half-pixel row | LOW | row 7, the same whole-pixel row as icon-16.svg; later, favicon.svg was dropped as the same drawing as icon-16.svg, which also serves as the SVG favicon, and a test holds its bar on integer coordinates |
