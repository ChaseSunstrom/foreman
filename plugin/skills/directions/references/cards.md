<!-- Foreman's own reference (written for Foreman, not ported). -->
# Direction cards

What the directions skill drafts, the rules the six obey as a set, the generic defaults none of them may be, the
preview page recipe, and a worked example. The knobs, the bank, the audacity dial and the DESIGN.md template live in
the UI playbook (`design-direction.md`); this file doesn't repeat them.

## The card

One card per direction, short enough to read on one screen, in this order:

```markdown
### N. <Name> (<bank row | look-NAME | own>)
- **Feels like:** <one physical thing, not a website>, for <who, doing what>.
- **Palette:** <role> <hex> · <role> <hex> · … (3 to 6); <text hex> on <ground hex> <n>:1, measured.
- **Type:** <display or heading family and class> + <text family and class> (+ mono); ratio <n>.
- **Layout:** <the product's main screen in one or two sentences, with its real content>.
- **Motion:** <what moves, how long, what is left under reduced motion>.
- **Signature move:** <the thing a screenshot is recognised by>.
- **Texture:** <shader-NAME on one surface> (optional: most cards have none).
- **Audacity:** <safe | bold | wild>, <which knobs sit off neutral>.
- **Fits because:** <one line tied to the sentence>. **Risks:** <one line: what could go wrong for this product>.
```

Name each direction for its physical thing ("Negative file"), not for a mood ("Bold & clean"). A bank row or a look
keeps its knobs and signature move; adapt its hex values to the product only with the contrast measured again. An
`own` card is built the same way: a physical thing, all five knobs, one signature move.

## The set

The six are a choice only if they differ. Check the whole set before showing it.

| Rule | Holds when |
|---|---|
| Sources | at least four come from the bank or the looks (`fm lib list --area looks`); at most two are `own` |
| Ground | at least one dark ground and at least one mid or tinted ground: not six shades of white |
| Type | at least three type classes across the six (serif, grotesk, humanist, geometric, mono, condensed, rounded display) |
| Density | at least one sparse and one dense |
| Motion | at least one still (none, or state changes only) and one lively (springs, draw-ins, stepped cuts, a stamp) |
| Audacity | safe, bold and wild each at least once |
| Pairs | any two differ on at least three of the five knobs (type, colour, density, motion, radius), and no two share a physical thing, a signature move, or both a ground and an accent family |
| Floors | every card's body text pair is 4.5:1 or more, measured; every accent hue sits 30° or more from the status hues (`type-and-colour.md`); none is indigo or violet |
| Fit | a look whose `Not for:` names this kind of product is out; every card has a reason tied to the sentence |

A card that breaks a rule is redrafted or replaced. Write the dropped ones under the comparison table, one line each,
so the user sees what was considered.

## Generic defaults

What generated design converges on when nobody chose. None of the six may be one of these, whichever bank row it
came from, and every card also obeys the playbook's "Defaults to avoid".

1. **Cream and terracotta with a serif display**: a warm off-white ground, a rust or clay accent, an old-style serif
   headline. Field guide and look-ceramic-studio stay clear only with their own accents (moss and ochre; cobalt).
2. **Near-black with one acid accent**: a #0A0A0A-ish ground with lime, electric green, neon cyan or hot orange as the
   only colour, usually glowing. Night arcade qualifies only when the sentence names night, games or music.
3. **Broadsheet hairlines**: 1 px rules, small-caps kickers, a drop cap and serif columns standing in for "editorial"
   on a product nobody reads at length. Broadsheet qualifies only for news, essays or a magazine.
4. **The SaaS card kit**: a centred hero, two equal buttons, three icon cards, 8–12 px radius and one soft shadow
   everywhere, an indigo accent (the playbook's defaults 1, 3, 4 and 13).
5. **Template chrome**: logo left and links right, hero, feature grid, testimonials, a footer of link columns: a
   page frame chosen before the content. A direction shows the product's main screen, never a landing page frame.

Broadsheet and Night arcade are bank rows that double as defaults: never offer both in one set.

## Preview pages

Only when the user asks to see the directions ("show me", "mock them up") or is torn between two. One file per
direction, `direction-<N>-<slug>.html`, in a temporary folder outside the repo (the session scratchpad or
`mktemp -d`): drafts never enter the repo; only the pick does, as DESIGN.md.

- **One screen, real content.** The product's main screen from the sentence (the booking grid, the log, the
  dashboard), its real nouns and numbers, no lorem ipsum, no template chrome (no navbar, hero or footer around it).
- **Tokens.** The card's palette as custom properties on `:root`; every colour in the page comes from one of them.
- **Self-contained.** Inline CSS, no script unless the motion needs one, no outside host: no web fonts, CDNs or
  images by URL. `font-family` names the intended family first, then a local fallback of the same class
  (`Georgia, serif`; `ui-monospace, monospace`).
- **Motion.** The card's motion, plus a `@media (prefers-reduced-motion: reduce)` path that keeps only opacity or
  nothing.
- **Signature move above the fold** at 1440×900 and at 360 px wide.
- **Check.** `fm design lint <folder>` reports nothing, or each finding is fixed or answered in the card; give the
  user the file paths. With a browser at hand, `visual-qa.md`'s frame matrix gives one shot per page.

## Example

The sentence: *"A booking site for a community darkroom: members reserve enlargers by the hour and log each print's
exposure."* Interview 1 (who and when) is assumed: a member planning tonight's session on their phone. Interview 3
(never) is assumed: never a gym or salon booking app. Surface: a new product's home, so bold is the default dial.

### 1. Contact sheet (own)
- **Feels like:** a contact sheet on the light table with the keepers circled in china marker, for a member picking
  tonight's frame of time.
- **Palette:** paper #F5F5F2 · film #161616 · marker #B0186E (hue 353, 34° from error red); #161616 on #F5F5F2
  16.57:1; #B0186E on #F5F5F2 6.00:1.
- **Type:** a neo-grotesk for text + a mono for edge numbers and times, printed like film rebate; ratio 1.618.
- **Layout:** each enlarger is a film strip running edge to edge; its hours are frames along the strip, booked ones
  exposed dark, free ones paper; strips lie up to 1° askew on the light table and may overlap.
- **Motion:** the china-marker circle draws itself once around a booking in 250 ms (stroke-dashoffset); under reduced
  motion it is simply there.
- **Signature move:** a hand-drawn circle around your booked frame; edge numbers as the time axis.
- **Texture:** `shader-grain-gradient` with all three colours set to paper and `uTime` 0: its fixed grain alone, on
  the light table behind the strips.
- **Audacity:** wild, all five knobs off neutral.
- **Fits because:** members already think in frames and strips. **Risks:** askew strips must still read as a
  schedule: straighten them below 600 px and at 200% zoom.

### 2. Lab notebook (look-lab-notebook)
- **Feels like:** the darkroom's quad-ruled exposure log, filled in ballpoint, for members who note every print's
  f-stop and seconds.
- **Palette:** the look's: surface #F1F8FD · text #202528 · ballpoint #1C508D · grid #BFD6D6; #202528 on #F1F8FD
  14.44:1; #1C508D on #F1F8FD 7.59:1.
- **Type:** a humanist sans at 400 and 600 + a mono with tabular figures for dates, f-stops, seconds and grades;
  ratio 1.25.
- **Layout:** bookings and prints are dated entries; a 10ch margin carries the date and entry number; each print
  entry ends with its exposure line and a taped-in test strip in a sunken box.
- **Motion:** state changes only, 150 ms or less; a new entry fades in.
- **Signature move:** the exposure line on every print (f/8 · 12 s · grade 3), set in mono like a measurement.
- **Audacity:** safe, two knobs off neutral (type and colour).
- **Fits because:** the log half of the sentence becomes the whole interface. **Risks:** booking can feel like
  paperwork; keep "Book an enlarger" as one entry form at the top.

### 3. Gallery (bank)
- **Feels like:** the members' show on a white wall, for people deciding whether to join.
- **Palette:** bone #F4F1EC · charcoal #222222 · label grey #5C574F · brass #9A8866 (rules and large numerals only);
  #222222 on #F4F1EC 14.12:1; #5C574F on #F4F1EC 6.36:1.
- **Type:** a light high-contrast serif display at 6× body + a grotesk for labels in small caps tracked +0.12em;
  ratio 1.5.
- **Layout:** one member's print per viewport, wall-sized margins; booking opens from each print's label ("Printed
  on the Durst M605 · Thursday · 2 hours · Book this enlarger").
- **Motion:** 400 ms opacity fades between prints, nothing else; instant under reduced motion.
- **Signature move:** captions as museum labels beside the work, with the booking link inside the label.
- **Texture:** `shader-paper-fibre` in bone, still, on the mat around each print: members print on fibre paper.
- **Audacity:** bold, three knobs off neutral (type, density, motion).
- **Fits because:** the prints are the community's pride; the site recruits as well as books. **Risks:** regulars who
  only book will find it slow; give them a direct /book route.

### 4. Instrument (bank)
- **Feels like:** the enlarger timer beside a mixing desk, for regulars who book the same slot each week.
- **Palette:** graphite #1E2124 · text #E6E8EA · muted #A3A9AF · colour only for state (free, mine, taken, error),
  the selection a 2 px outline; #E6E8EA on #1E2124 13.17:1; #A3A9AF on #1E2124 6.82:1.
- **Type:** a grotesk at 13–14 px with tabular figures for every number; ratio 1.2.
- **Layout:** each enlarger is a channel strip: its name on top, today's hours as 28 px cells down the strip, a
  sparkline of the week's use at the foot; all enlargers side by side.
- **Motion:** 100 ms or less, state changes only.
- **Signature move:** a timer readout at the top of each strip ("00:42 until your slot").
- **Audacity:** safe, two knobs off neutral (density and colour).
- **Fits because:** booking is the job and speed is the courtesy. **Risks:** dark and dense reads as a club for
  insiders; one plain "how booking works" line above the strips.

### 5. Blueprint (bank)
- **Feels like:** the enlarger's service drawing, for a newer member learning which machine takes medium format.
- **Palette:** navy #0B2545 · line white #F2F5F8 · cyan #7FD1E8; #F2F5F8 on #0B2545 14.06:1; #7FD1E8 on #0B2545
  8.93:1.
- **Type:** mono uppercase labels + a condensed sans for text; ratio 1.333.
- **Layout:** one enlarger drawn per screen on a dotted grid with room around it; its bookable hours run along the
  baseboard as a dimension line marked in hours.
- **Motion:** the drawing's lines draw in over 300 ms on first view; under reduced motion it is drawn already.
- **Signature move:** leader lines from the parts to notes ("negative carrier: 35 mm and 6×6"), and the day drawn as a
  dimension line.
- **Audacity:** bold, four knobs off neutral (all but radius).
- **Fits because:** which enlarger to book is a newcomer's real question. **Risks:** a dark field tires long reading;
  keep the notes short.

### 6. Negative file (look-shipping-manifest)
- **Feels like:** the kraft negative envelopes in the filing drawer, roll and date in boxed fields, PRINTED stamped
  across, for members filing what they made.
- **Palette:** the look's: kraft #E3D0B2 · raised #F4E0C2 · ink #1E1A13 (the accent is the ink); #1E1A13 on #E3D0B2
  11.49:1; #1E1A13 on #F4E0C2 13.43:1.
- **Type:** one grotesk with a width axis, condensed capitals for field labels and normal width for text + a mono for
  roll and frame numbers; ratio 1.333.
- **Layout:** each booking is an envelope: a field grid (ENLARGER, DATE, FROM, TO, PAPER) with tiny capital labels;
  past sessions file below as a stack of envelopes; perforated edges between sections.
- **Motion:** a stamp lands on confirmation (scale 1.04 to 1, 150 ms); nothing else moves.
- **Signature move:** BOOKED and PRINTED rubber stamps, rotated at most 4°.
- **Audacity:** bold, three knobs off neutral (type, colour, shape).
- **Fits because:** the darkroom already files negatives this way, so booking and logging share one object.
  **Risks:** kraft is a mid-tone ground: measure any new muted text on it before using it.

| # | Ground | Type | Density | Motion | Radius | Audacity |
|---|---|---|---|---|---|---|
| 1 Contact sheet | white paper, black strips | neo-grotesk + mono | dense | one draw-in | 0 | wild |
| 2 Lab notebook | cool white, quad grid | humanist + mono | medium | state only | 2 | safe |
| 3 Gallery | bone | light serif display + grotesk labels | sparse | slow fades | 0 | bold |
| 4 Instrument | graphite (dark) | grotesk, tabular | dense | state only | 2 | safe |
| 5 Blueprint | navy (dark) | mono caps + condensed sans | sparse | lines draw in | 0 | bold |
| 6 Negative file | kraft (mid) | condensed caps + mono | medium | a stamp lands | 0 | bold |

Dropped while drafting: **Safelight** (own: red light on black), the near-black-and-one-glow default in a darkroom
costume, and its red would collide with error red. **Riso zine**: its fluoro pink sat on Contact sheet's marker.

Recommended: **6. Negative file**, bold: booking and the print log become one familiar object. Runner-up:
**1. Contact sheet**, which lost because askew strips cost a booking grid its scanability.
