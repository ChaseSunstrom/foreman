# Crest shots 2: the hand-drawn mark (T-3210)

Follows crest-shots (T-3113), where the 12 px mark, an anti-aliased downscale of design/sampo/logo/mark-simple.svg,
read as a muddy mosaic with grey noise at its base.

## What changed
- MARK_TOKENS (70 distinct colours across the two marks) became MARK_PIXELS: hand-drawn pixel art, one character a
  pixel, in four flat tones (MARK_TONES): gold #ffc24d (C.accent, the flame's core), ember #e8531c (the flame's edge),
  steel #8a92a6 (anvil and iron band), stone #4e4a58. Each 2 pixel rows fold into one half-block row.
- 12 px (6 rows, the box's full height inside the ring): three tongues of fire, the middle one tallest with a gold core,
  behind an anvil (flat face, heel left, horn tapering right, waist, foot) on a stone bound by an iron band that
  stands out a pixel each side. 6 px (3 rows, under 60 columns): one tongue, the anvil, the banded stone.
- Test: "crest: each mark is at most 4 tones, none an in-between shade of two others" (3 to 4 tones per mark; no tone
  within 24 per channel of a 20-80% mix of two others).
- shot.py drew ▀/▄ with Hack's glyphs, which cover a little less than half a cell: a 1-2 px seam of the cell's bg ran
  through every two-tone cell (a steel line across the fire, a dark line through the anvil). Snap now draws them as
  exact half-cell rectangles, as Konsole and most terminals draw block elements. Part of the old "grey noise" in the
  crest-shots notes may have been this seam.

## Shots (shot.py, 60 rows; the dock on the right)
- 200 columns, idle: clean silhouette: fire, anvil, banded stone; ring all dim. No noise at the base; the stone's
  bottom edge is a flat stone row.
- 200 columns, working (a 30 s foreground python sleep): the same mark; the fire runs round the top of the ring (gold
  head, white lead rune, fading tail). The mark's gold matches the ring's.
- 150 columns, idle and working: the same (dock ~66 columns, still the wide crest).
- 120 columns: compact crest (6 px, 3 rows) beside "Sampo" and a rune row: reads as a flame on an anvil on a stone.
- 200 columns, 28 rows: the dock is too short for the crest; none drawn (as designed, T-3113).

## Judgement
Reads as a mill-and-flame emblem at both widths, crisp, no in-between greys. It is pixel art, not an illustration:
at 12x12 px, four tones, that is the ceiling. A richer mark would need more cells (a 16 or 20 px mark would eat the
hammer slots) or a second steel tone for the anvil's face highlight (5 tones, over the brief's 4).
