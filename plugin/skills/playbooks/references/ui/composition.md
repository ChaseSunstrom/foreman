<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Composition, depth and states

Use when a web or app screen gets its layout: where things sit, what is in front of what, how a landing page runs
from top to bottom, and what every screen looks like when the data is missing, slow, broken or too long. For
terminals see `terminal-ui.md`.

The generic look is a kit, not a layout: every section a row of equal cards, every card the same shadow, everything
centred, and only the happy state ever designed. This playbook replaces the kit with decisions a reviewer can mark
pass or fail. It owns space, alignment, layering and states. `design-direction.md` owns the stance and the density
knob, `type-and-colour.md` owns sizes, measure and colour roles, `motion.md` owns timing and loading thresholds;
this file points at them rather than repeating them. **Precedence:** `DESIGN.md` sets the values (spacing unit,
shadow style, how many grid breaks); the rules here say how those values are used, and the state atlas and the
contrast floors hold whatever `DESIGN.md` says.

## The procedure

1. **Write the screen's job in one line**: who arrives, and the one thing they came to do or learn.
2. **Rank the content** (see Hierarchy) before drawing anything.
3. **Pick the grid** from the direction (table below) and set the spacing tokens.
4. **Wireframe three layouts** that differ in kind, not in detail; score them with the table in
   "Three layouts for one brief"; keep one, reject two in writing.
5. **Build the full state,** then **fill the state atlas** for the screen. A screen whose atlas has blank rows isn't
   built.
6. **Run the probe** (Measure it) at 360 and 1280 wide, then the Checks.

## Grid and rhythm

**Spacing is a scale, like type.** One unit from the density knob in `DESIGN.md` (4 px for dense directions,
8 px for the rest), a fixed ladder of steps, in `rem` so spacing grows when the reader enlarges text:

```css
/* tokens/space.css: the only file allowed raw lengths for margin, padding, gap and inset */
:root {
  --space-1: 0.25rem;  --space-2: 0.5rem;  --space-3: 0.75rem; --space-4: 1rem;   --space-5: 1.25rem;
  --space-6: 1.5rem;   --space-7: 2rem;    --space-8: 3rem;    --space-9: 4rem;   --space-10: 6rem;
  --measure: 65ch;     /* the text column; type-and-colour.md sets the 45–75ch range */
}
```

**The rhythm ratio.** Space says what belongs together, so it comes in three tiers, each at least 1.5× the one
below: *inside a group* (label to field, title to its text), *between groups* (one field to the next, one card's
content to the next card), *between sections*. Typical sets: 8 / 16 / 48 px for calm, 4 / 8 / 24 px for technical,
16 / 32 / 128 px for premium. Pass: pick any heading in the built screen; the space above it is larger than the
space below it, and no two tiers share a value.

**Pick the grid from the direction, not from the framework.**

| Grid | Columns | Fits the directions | Its tell |
|---|---|---|---|
| Single column | one text column at `--measure`, media allowed to bleed | Civic, Raw, Soft utility, any form | nothing beside the text competes with it |
| Manuscript | a main column plus a narrow margin column (about 3:1) | Field guide, editorial | notes, captions and asides live in the margin, level with what they gloss |
| Twelve-column | 12 equal tracks, content spans 3, 4, 6 or 8 | Broadsheet, Instrument | hairline rules in the gutters; several stories at once |
| Asymmetric | two unequal columns, 5:7 or 4:8, the narrow one empty or quiet | Poster, bold | a big empty field that makes the one thing in the other column loud |
| Modular | a fixed module (for example 4 × 4 units) everything snaps to | Instrument, Blueprint, dashboards | panels of exact multiples; numbers line up across panels |
| One per view | one work fills the viewport, the scroll moves between works | Gallery | the margin is the frame |
| Collage | a grid that items deliberately break, overlap or rotate | Riso zine, Toybox, wild | the break is the composition; it still lines up somewhere |

Rules that hold on any grid:

- **Every margin, padding, gap and inset is a `--space-*` token.** Pass:
  `grep -rnE "(margin|padding|gap|inset)[a-z-]*\s*:[^;]*[0-9.]+(px|r?em|ch)\b" src | grep -v tokens/` returns
  nothing.
- **Columns come from content, then the viewport.** The text column's width is `--measure`; outer columns take
  what's left. A full-bleed layout on named lines does this without wrapper divs:

  ```css
  .page {
    display: grid;
    grid-template-columns:
      [full-start] minmax(var(--space-6), 1fr)
      [content-start] minmax(0, var(--measure)) [content-end]
      minmax(var(--space-6), 1fr) [full-end];
  }
  .page > * { grid-column: content; }
  .page > .bleed { grid-column: full; }   /* images, bands and the hero's artefact */
  ```

- **Breakpoints come from the content breaking,** not from device names: a layout changes where a line passes
  75ch, a column drops under 45ch, or a table needs a sideways scroll. Components switch on their own width with
  container queries (`fm lib show container-queries`), so a card works in a sidebar and in a main column.
- **Source order is reading order.** On every width, the order you see is the order a screen reader and the Tab key
  follow (WCAG 1.3.2 and 2.4.3). Lay out the phone order in the DOM and let wider grids place items without
  reordering them. Pass: each hit of
  `grep -rnE "\border\s*:\s*-?[1-9]|grid-(row|area)(-start)?\s*:\s*-?[0-9]|(row|column)-reverse|\bdense\b" src`
  moves only decoration, or comes with a note on why reading order still holds.
- **Collections that can hold one item use `auto-fill`, not `auto-fit`.** `repeat(auto-fit, minmax(16rem, 1fr))`
  collapses the empty tracks, so a lone result stretches across the whole row; `auto-fill` keeps it card-sized.
- **Grid and flex children that hold text get `min-width: 0`** (or `minmax(0, 1fr)` tracks). Their default minimum
  is their longest word, so one long name or URL widens the column and pushes the page sideways.
- **Breaks are counted.** The audacity dial in `design-direction.md` sets how many sections may leave the grid
  (safe 0, bold 1, wild as many as the direction wants). A break still aligns with something: an edge of the grid,
  the section boundary it straddles, the line of the headline. A 12 px offset that lines up with nothing is a bug,
  not a break.

**Alignment is a choice per section, not a default per element.**

- **Flush left** (flush to the start side in right-to-left scripts) is the default for anything read: it gives the
  eye one edge to return to.
- **Centred** is for ceremony: three lines or fewer, one action at most, symmetrical content (a closing call to
  action, a quotation, an empty state's message). Centred running text over three lines fails.
- **Right** (end) alignment is for numbers in columns, so the units digits line up (with `tabular-nums`, see
  `type-and-colour.md`).
- **Count the axes.** Every line of text in a viewport starts, centres or ends on an axis. Pass (with the probe
  below): at 1280 wide, four axes or fewer carry two or more lines each; at 360 wide, three or fewer. A
  multi-column direction (Broadsheet, Instrument, Modular) may raise the desktop limit to its column count plus one,
  written in `DESIGN.md`. More axes than that means things sit near each other instead of on each other.

## Hierarchy

Hierarchy is a ranking you write down first and then make visible. Type steps (`type-and-colour.md`) are one lever
among six.

1. **Rank before you draw.** List the screen's elements in the order the reader should meet them. Each viewport has
   one rank-1 item, a few rank-2 items, and the rest. Pass: the list is in the brief, and a person who hasn't seen
   the screen, shown it for three seconds, names the rank-1 item when asked what they saw first.
2. **Use the cheapest lever that works,** in this order: **space** (isolation: the rank-1 item has the most empty
   space around it in its viewport), **position** (first in reading order, at the start of the top), **size**,
   **weight**, **colour** (the accent is spent on rank 1 only), **motion** (the one orchestrated moment of
   `motion.md` belongs to rank 1). Two levers usually do it; reaching for all six flattens everything again.
3. **Three levels per viewport,** no more: primary, secondary, and everything else at body weight. A fourth level
   of emphasis competes with the first.
4. **The action comes after its reason.** A primary button follows the content that motivates it in reading order;
   it is never above the headline it acts on, and never the first focusable thing in a section.
5. **Group with the weakest tool that works.** Space first, then alignment, then a hairline, then a tint
   (`--surface-sunken`), then a border, and a raised card last. A card is earned when the thing is an object the
   person handles as a unit: selects, drags, opens, or compares with its siblings. Pass: no raised surface sits inside
   another raised surface (the probe's `nestedRaised` is empty), and each card on the screen passes the "handled as
   a unit" test.
6. **Equal is a statement.** Items given equal size and weight read as equal in importance. Three features in three
   equal cards say "we couldn't choose"; if one matters most, make it bigger and give the other two a line each.

## Depth without WebGL

Depth tells the reader what is in front of what: what floats, what is underneath, what blocks the page until it's
dealt with. It is built from five cues, and they all have to agree on one light.

**One light source, stated.** `DESIGN.md` says where the light comes from (straight above is the safe default).
Every shadow falls away from it, so every shadow has the same sign of x and y offset, and its offset and blur grow
with height. A shadow pointing the other way, or a glow where a shadow should be, breaks the illusion for the whole
screen. Directions with hard shadows (Toybox's 4 px offset with no blur) follow the same rule: one direction, one
colour.

**Elevation is a short table, and stacking order comes from the same table.** Three heights are enough; each one
means something, so a reviewer can ask "why is this floating?".

| Level | Means | Examples | Shadow | Stacking |
|---|---|---|---|---|
| 0 flat | part of the page | sections, rows, inline panels | none | normal flow |
| 1 raised | an object you can handle, or chrome that stays put | a selectable card, the sticky header | `--shadow-1` | `--z-raised`, `--z-sticky` |
| 2 floating | about this page, dismissed lightly | menus, popovers, toasts, tooltips | `--shadow-2` | the top layer (`popover` attribute) |
| 3 blocking | stops the page until answered | dialogs, sheets | `--shadow-3` plus a scrim | the top layer (`<dialog>` opened with `showModal()`) |

```css
/* tokens/depth.css: light from straight above; shadow ink from the neutral ramp in tokens/colour.css */
:root {
  --shadow-ink: color-mix(in oklch, var(--n-18) 16%, transparent);
  --shadow-1: 0 1px 2px var(--shadow-ink), 0 2px 6px var(--shadow-ink);    /* contact + ambient */
  --shadow-2: 0 2px 4px var(--shadow-ink), 0 8px 24px var(--shadow-ink);
  --shadow-3: 0 4px 8px var(--shadow-ink), 0 24px 48px var(--shadow-ink);
  --scrim: color-mix(in oklch, var(--n-18) 65%, transparent);    /* clears the body-text row of the scrim table */
  --z-raised: 1; --z-sticky: 10;      /* floating and blocking layers use the top layer, not z-index */
}
```

- **Shadows and z-index come only from tokens.** Pass: `grep -rnE "box-shadow\s*:[^;]*[0-9]px|z-index\s*:\s*-?[0-9]"
  src | grep -v tokens/` returns nothing, and the probe lists at most three distinct shadows plus any inset
  highlights. `z-index: 9999` is a fail on sight.
- **Each shadow is a pair:** a tight, darker contact shadow that says "touching" and a wide, faint ambient one that
  says "how high". One soft blur alone reads as a smudge.
- **Shadow ink is the surface's hue,** not black: a shadow on warm paper is a darker warm, from the neutral ramp.
  In dark mode shadows mostly disappear and height is carried by lightness and a lighter 1 px edge, as
  `type-and-colour.md` sets out; the levels and their meanings stay the same.
- **Popovers and dialogs use the top layer** (`popover`, `showModal()`), which sits above every `z-index` on the
  page, so the z-index ladder stays two rungs long and no sticky header can cover a menu. A non-modal `dialog.show()`
  does not use the top layer.
- **Light can shape a surface, not only lift it.** A raised control may carry a 1 px highlight on the side facing
  the light (`inset 0 1px 0` in a lighter tone) and a surface may brighten by 0.02 L toward the light. Both are
  optional; if used, they face the same light as the shadows.

**Layers and atmosphere.** At most three planes per viewport: background, content, and one floating layer. Planes
further back lose contrast and chroma (not sharpness: blurred text is unreadable, not distant). An element may
overlap a section boundary to tie two sections together, counted against the grid breaks above; it never covers
text or a control (the probe's `covered` list is empty).

**Backdrops.** Text over an image, a video or a moving page needs a backdrop it can rely on.

- **The white-image test.** Swap the image under light text for pure white (or under dark text for pure black). The
  text must still pass its contrast floor. If it passes over white, it passes over any photo, today's and next
  year's. For light text (L about 0.97) over a scrim of the darkest neutral (L about 0.18), the scrim needs at least
  this opacity directly behind the text:

  | Text | Floor | Scrim opacity behind it |
  |---|---|---|
  | large (24 px, or 18.67 px bold) | 3:1 | 0.48 |
  | body | 4.5:1 | 0.61 |
  | dark-mode body (Foreman's rule) | 7:1 | 0.73 |

  A gradient scrim holds that opacity across the whole text box, not just at its darkest end.
- **Frosted glass is earned by movement.** `backdrop-filter: blur()` is for a surface with content moving under it
  (a sticky header over a scrolling list, a sheet over the page). The colour behind the blur must pass the
  white-image test on its own, because the blur is decoration and is missing in some renderers and in
  forced-colours mode. Glass over a static blurred gradient is default 7 in `design-direction.md`.
- **A scrim behind a dialog** dims the page to say "not now"; it isn't a contrast fix for the dialog, which sits on
  its own opaque surface.

Parallax and scroll-linked depth are motion: they follow `motion.md`, including its reduced-motion path.

## The hero

The hero is the first viewport. Its job is to make a stranger understand what this is by showing it. Open with the
subject's most characteristic thing: the one thing this product, place or person has that a competitor doesn't.

**Pick the opening move from what the subject is:**

| The subject is | Open with | Not with |
|---|---|---|
| a tool or app | the real interface mid-task, with real-looking data, cropped to the interesting part | a laptop mock-up of a blurred screenshot; floating UI fragments |
| a physical product | the object at true scale or bigger, in use, in its material | a 3D blob, a gradient, a lifestyle photo where the product is small |
| a service | the result: the deliverable, the before and after, the finished room | people shaking hands, a team photo |
| a data product or API | a real query and its real output, side by side | a diagram of boxes and arrows |
| content (a publication, a course, a podcast) | the best piece itself, readable or playable right there | a list of topics |
| a place or event | where, when and who, set as type, with the place itself | a countdown timer as the whole hero |
| a person or studio | the work, large, with the name small | a portrait and a list of skills |

Rules, each pass or fail:

- **The mute test.** Hide the headline. From the rest of the hero alone, a stranger can say what this does. (It
  complements the cover test in `design-direction.md`, which hides the logo.)
- **The swap test.** Put a competitor's name into the headline. If it is still true, it says nothing that is yours;
  rewrite it around the characteristic thing.
- **One primary action, named as the act:** a verb and its object ("Book a wheel", "Try it on your repo"), not
  "Get started". Any second action is a text link.
- **It fits the first viewport** at 1280×720 and 360×640: headline, the primary action, and the artefact (or its
  most telling part) are visible without scrolling.
- **It shows there is more.** At 1280×720 the next section shows at least a line of itself, or the hero ends on a
  visible cue. A hero of exactly `100vh` with nothing below the fold reads as the whole page. A full-screen hero is
  allowed when `DESIGN.md` lists it (Gallery, Poster).
- **The artefact is the largest paint** and loads first (`fetchpriority="high"`, never lazy, real `width` and
  `height`: `fm lib show image-optimization`), and it never starts invisible (`motion.md`).
- **A live hero has states.** A hero that shows real data (the example below does) gets its own rows in the state
  atlas: loading, stale and empty.

## Landing page structure

A landing page is an argument. Each section answers the next question a reader has, in the order they have it, and
the page ends when the questions do.

1. **Write the questions first,** one per section, in the reader's words: What is it? Does it work? Is it for me?
   What does it cost? What could go wrong? How do I start? Pass: each section in the brief has its question; two
   sections answering the same question become one.
2. **Answer with evidence, not adjectives.** A worked example, an annotated screenshot, a numbered sequence, a
   comparison table or a price list beats any row of icon cards (default 3 in `design-direction.md`).
3. **Proof is specific:** numbers with units and their source, quotes with a full name and role, customer logos in
   one row at most.
4. **Vary the rhythm.** Alternate dense and airy sections, and wide and narrow ones. Pass: list each section's
   layout in a word (split, sequence, table, gallery, single column…); no layout appears three times in a row.
   Image-left, image-right, image-left, image-right is one layout four times.
5. **Close with the hero's action, in the hero's words.** The last section repeats the primary action unchanged, so
   the reader who scrolled to decide finds the same button they skipped.
6. **Length follows the questions,** usually five to eight sections. A section added "for balance" fails step 1.

## Three layouts for one brief

Draw three layouts that differ in kind before building one. The brief here is Kilnroom, the invented pottery studio
from the `design-direction.md` example (Field guide direction, bold, paper and celadon, kiln shelves as the
signature move): a landing page for people who haven't joined yet.

```text
A  Notebook spread: main column plus a margin of notes (manuscript grid)
+------------------------------------------------------------------------+
| Kilnroom                                       Classes  Firings  Join  |
+------------------------------------------------------------------------+
|                                                                        |
|  Wheel time, a kiln shelf and a                 | 1 cone 6, fired      |
|  glaze notebook, three streets                  |   every Thursday     |
|  from the station.                              |                      |
|                                                 | 2 sketch: a bowl     |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~         |   foot, trimmed      |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~                     |                      |
|                                                 |                      |
|  [ Book a first evening ]   Prices ->           | 3 "Glaze 14 runs at  |
|                                                 |   the foot: wax it"  |
|  +-------------------------------------------+  |                      |
|  | photo: a notebook page, test tiles taped  |  |                      |
|  | in, firing notes in pencil                |  |                      |
+------------------------------------------------------------------------+
     the fold at 1280x720 cuts the photo: the characteristic thing is late
```

```text
B  Kiln cross-section: the hero is this week's kiln, filling as people book
+------------------------------------------------------------------------+
| Kilnroom                                       Classes  Firings  Join  |
+------------------------------------------------------------------------+
|                                                                        |
|  This week's wheels               +----------------------------------+ |
|  and kiln, live.                  | Thursday firing   cone 6  1222 C | |
|                                   | ================================ | |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~       | [bowl] [mug] [mug] [vase] [    ] | |
|  ~~~~~~~~~~~~~~~~~~~~             | ================================ | |
|                                   | [jug] [    ] [    ] [    ] [   ] | |
|  [ Book Thursday, 18:00 ]         | ================================ | |
|  3 wheels left this week          | wheels  Mon ##  Tue #.  Thu #..  | |
|  Prices ->                        +----------------------------------+ |
|                                                                        |
|  An evening, start to finish  ->  (next section peeks in)              |
+------------------------------------------------------------------------+
```

```text
C  One tile: a single glaze test tile, three times life size (asymmetric)
+------------------------------------------------------------------------+
| Kilnroom                                                         Join  |
|                                                                        |
|               +------------------------------------------------+       |
|               |                                                |       |
|               |   photo: one celadon test tile, the glaze      |       |
|  GLAZE        |   pooling green at its lower edge              |       |
|  YOUR         |                                                |       |
|  OWN.         |                                                |       |
|               |                                                |       |
|               +------------------------------------------------+       |
|  [ Join the studio ]                                                   |
|                                                                        |
+------------------------------------------------------------------------+
```

Score them against the rules, not against taste:

| Check | A Notebook spread | B Kiln cross-section | C One tile |
|---|---|---|---|
| Opens with the characteristic thing | the notebook, but below the fold | yes: no other studio has this kiln this week | a tile says "pottery", not "this studio" |
| Mute test (headline hidden) | a pottery studio, probably | book wheel time, see what's firing | a ceramics shop? a glaze brand? fails |
| Swap test on the headline | passes (the station) | passes (live slots) | fails: anyone can print it |
| Primary action names the act | yes | yes, with the next real slot | "Join", vague |
| Axes at 1280 | 3 | 3 | 2 |
| At 360 wide | margin notes fold under their paragraphs | the kiln crops to Thursday's shelves | strong, but the photo pushes the action down |
| New states it brings | none | kiln data: loading, stale, full week | none |
| Cost | a photo shoot | live data on a marketing page | one photo |

**Chosen: B.** It is the only one that passes the mute test for the job (booking), and it makes the signature move
the hero. **Runner-up: A,** whose margin notes become the texture of section 3 instead. **Rejected: C,** a strong
poster for a brand that doesn't need explaining; Kilnroom does. B's cost is real: its hero now has states.

The chosen layout at 360 wide, with the DOM in this order so no reordering is needed:

```text
+--------------------------------+
| Kilnroom                  Menu |
+--------------------------------+
| This week's wheels             |
| and kiln, live.                |
|                                |
| [ Book Thursday, 18:00 ]       |
| 3 wheels left this week        |
| +----------------------------+ |
| | Thursday firing   cone 6   | |
| | [bowl] [mug] [mug] [vase]  | |
| | [jug]  [    ] [    ]       | |
| +----------------------------+ |
| ~~~~~~~~~~~~~~~~~~~~~~~~~~     |
+--------------------------------+
```

And its sections, each with its question and layout word, so the rhythm check can be run on paper:

| # | Section | Question it answers | Layout |
|---|---|---|---|
| 1 | Hero: the live kiln | What is it, and can I get in? | split |
| 2 | An evening, start to finish | What happens when I turn up? | numbered sequence with photos |
| 3 | The glaze notebook | What could I make? | manuscript, with margin notes |
| 4 | Prices | What does it cost? | table |
| 5 | Members' shelf | Is it any good, and who goes? | gallery, with names |
| 6 | Questions | Clay, mess, pieces that crack in the kiln | single column |
| 7 | Close | How do I start? | centred, "Book Thursday, 18:00" |

## State atlas

Every screen is designed in all its states, not just the one in the mock-up. The atlas is a table per screen: one
row per state, each designed (its words written), built, and reachable on demand for review.

| State | The screen shows | It never shows | Force it for review |
|---|---|---|---|
| **Loading, first time** | the real chrome (header, title, filters) and a skeleton in the content's exact boxes; timing per `motion.md` | a centred spinner on a blank page; a layout that jumps when data arrives | delay the request 3 s (devtools throttling, or a test route that waits before continuing) |
| **Loading, refresh** | the current data, marked as updating | a skeleton over data the reader already had | trigger a refetch with a slow response |
| **Empty, first use** | what will appear here, one action that fills it, and a glimpse of it full (a sample row, a ghosted example) | a blank region; an illustration with no action | a new account or empty fixture |
| **Empty, no results** | the query echoed back, which filter emptied it, a one-click way to widen it | "No results" alone | a filter that matches nothing |
| **Empty, all done** | good news, said as such, and what happens next | first-use wording ("Get started") on a cleared inbox | finish every item |
| **Partial** | what loaded, in place; each failed part says so where it would have been, with its own retry | the whole screen failing because one panel did; silent gaps | fail one endpoint, keep the rest |
| **Error, the screen** | what happened in plain words, that the reader's input is kept, the next action; a reference code in small print | a stack trace; "Something went wrong" alone; a cleared form | answer the main request with a 500 |
| **Error, an action** | the message beside the control that caused it, focus moved there, the input kept | a toast as the only notice (`fm lib show toasts`); a cleared field | reject one submit |
| **Offline** | one quiet banner; cached content with its age ("as of 17:42"); network-only actions disabled with the reason, or queued and marked pending; recovery without a reload | a modal; a blank page; actions that fail silently | devtools Offline, or a test browser context set offline |
| **Stale** | the data's age whenever it is older than its refresh interval | numbers that might be hours old, unmarked | mock an old timestamp |
| **No access** | what this is, who can grant access, a way to ask | a bare 403 with no way back | a role without the permission |
| **Overflow** | long, short, empty and right-to-left text, counts of 0, 1 and many, and a 1,000-item list, all by the rules below | text on text; a sideways scroll; "1 items" | the overflow fixture below |

**Rules for the atlas:**

- **Every row is filled for every screen.** "n/a" needs a reason ("no network calls on this screen"). Pass: the atlas
  table is in the brief or the PR with no blank cell.
- **Each state is reachable on demand** without editing code: a story per state, a fixture, or a route mocked in a
  test. A state you can only see by unplugging the router doesn't get reviewed.
- **States keep the layout.** Empty, error and offline states sit inside the screen's normal chrome, at the place
  the content would be, so the reader still knows where they are and what to try next. A full-page takeover is for
  the whole app being unreachable, not for one list.
- **Failure is contained to its part.** Independent panels fail independently (`fm lib show error-boundaries`).
- **States are announced.** Loading, the arrival of results, errors and going offline reach a screen reader through
  a polite live region, once each, not on every retry.

**Overflow rules:**

- **Truncate only what is one step from its full value:** the row opens it, or a focusable control reveals it. A
  `title` tooltip alone doesn't count (no keyboard, no touch). Never truncate amounts, dates, or the part of a name
  that tells two items apart; for file names and IDs, cut the middle and keep the ending.
- **One-line truncation** is `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` on a box with a width.
  **Multi-line** is `-webkit-line-clamp` (with `display: -webkit-box; -webkit-box-orient: vertical; overflow:
  hidden`), two or three lines at most.
- **User-written text** (names, comments, titles) gets `overflow-wrap: anywhere` on its container. Headlines don't:
  they follow `type-and-colour.md`.
- **Counts are words, not numbers glued to nouns.** Zero is the empty state, not "0 items"; plurals come from the
  message catalogue (`fm lib show i18n`); large counts may use compact notation (`Intl.NumberFormat` with
  `notation: 'compact'` gives "1.2K", or "1,2 Mio." in German) with the exact number in the accessible name.
- **Long lists stay usable:** past about 100 items, paginate, virtualise or load more on request
  (`fm lib show infinite-scroll`, `fm lib show data-tables`), and one item still looks deliberate (`auto-fill`, as
  in Grid and rhythm).
- **Translations grow.** German and Finnish run 30–40% longer than English; buttons and tabs size to their label,
  never to a fixed width (`fm lib show i18n` has the pseudo-locale run).

**The overflow fixture.** Load these values into the screen's real components (a story, a seed, a test fixture) and
look at every place they land:

```json
{
  "long_word": "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz",
  "long_name": "María Guadalupe Ximénez-Ó Súilleabháin de la Cruz",
  "short_name": "Ö",
  "empty": "",
  "unbroken_id": "inv_7f3a9c2e5b8d4f1a6e0c9b7d2a5f8e3c1b4d7a0f",
  "url": "https://example.com/shared/2026/q4/kiln-schedules/thursday-evening-firing-plan-final-v3.pdf",
  "rtl": "حجز عجلة الخزف يوم الخميس",
  "mixed_direction": "Order #4412: طلب رقم ٤٤١٢",
  "emoji_sequence": "👩🏽‍🔬 Glaze lab",
  "cjk": "陶芸教室の木曜日夜間焼成スケジュール",
  "counts": [0, 1, 2, 12, 1000, 1234567],
  "amounts": [0, -0.5, 0.005, 1234567.89],
  "list_lengths": [0, 1, 2, 7, 101, 1000]
}
```

Pass: with each value in place, the probe reports no sideways scroll and no spills, nothing overlaps, and every
truncated value is one step from its full form.

**The atlas for one screen**, filled in for Kilnroom's slot list (the hero's live kiln reuses rows 1, 3 and 7):

| State | Kilnroom's slot list shows | Forced by |
|---|---|---|
| Loading, first | header, week picker and day headings real; slot rows as skeleton bars of the real row height | `slots` request delayed 3 s |
| Loading, refresh | current slots, the week picker's label reads "updating" | week change with a slow response |
| Empty, all done | "Every wheel this week is booked. Next week opens Sunday at 18:00." and a "Remind me" button | fixture with all slots taken |
| Empty, first use | n/a: the studio always publishes a week of slots | — |
| Partial | slots load, the kiln panel says "Firing status didn't load. Retry" in its own box | `kiln` endpoint returns 500 |
| Error, the screen | "We couldn't load this week's slots. Your booking basket is safe. Retry" | `slots` endpoint returns 500 |
| Error, an action | at the slot: "Someone booked this a moment ago. The next free wheel is 19:30." | booking request returns 409 |
| Offline | banner "Offline: showing slots as of 17:42"; Book buttons disabled with "Booking needs a connection" | browser context offline |
| Stale | "as of 17:42" beside the week heading once the data is over five minutes old | mocked timestamp |
| No access | n/a: the slot list is public | — |
| Overflow | a 40-character member name on a kiln shelf wraps to two lines; the waitlist shows "No one waiting", "1 person waiting", "12 people waiting" | the overflow fixture |

## Measure it

Paste this into the devtools console on the built screen at each width you check (or run it with `page.evaluate`
in a browser test). It measures the first viewport: the alignment axes, centred blocks over three lines, content
spilling out of its box, controls something sits on top of, cards inside cards, and the distinct shadows and
z-index values in use.

```js
// composition-probe.js: paste into the devtools console on a built screen, or page.evaluate() it in a test.
// Measures the first viewport only; scroll and run again for the next one.
(() => {
  const vw = innerWidth, vh = innerHeight, near = v => Math.round(v / 4) * 4;  // 4 px buckets absorb subpixel noise
  const css = el => getComputedStyle(el);
  const block = el => { while (el.parentElement && css(el).display.startsWith('inline')) el = el.parentElement; return el; };
  const inView = r => r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < vh;
  const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList[0] ? '.' + el.classList[0] : '');
  // 1. Alignment axes: where each line of text starts (left), ends (right) or centres, by its block's text-align.
  const lines = new Map();                                       // block → Map(line top → [left, right])
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = walk.nextNode());) {
    if (!n.textContent.trim() || n.parentElement.checkVisibility?.() === false) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    const b = block(n.parentElement), m = lines.get(b) || new Map(); lines.set(b, m);
    for (const r of range.getClientRects()) {
      if (!inView(r)) continue;
      const k = near(r.top), [l, rt] = m.get(k) || [Infinity, -Infinity];
      m.set(k, [Math.min(l, r.left), Math.max(rt, r.right)]);
    }
  }
  const axes = new Map(), longCentred = [];
  for (const [b, m] of lines) {
    const a = css(b).textAlign, rtl = css(b).direction === 'rtl';
    const side = a === 'center' ? 'C' : a === 'right' || (a === 'end' && !rtl) || (rtl && a !== 'left' && a !== 'end') ? 'R' : 'L';
    for (const [l, r] of m.values()) {
      const key = side + near(side === 'C' ? (l + r) / 2 : side === 'R' ? r : l);
      axes.set(key, (axes.get(key) || 0) + 1);
    }
    if (side === 'C' && m.size > 3) longCentred.push(name(b) + ` (${m.size} lines)`);
  }
  // 2. Spills: content wider than its box (long words, min-width: auto in grid and flex). Deepest offenders only.
  const all = [...document.body.querySelectorAll('*')];
  const spill = all.filter(el => el.clientWidth > 0 && css(el).overflowX === 'visible' && el.scrollWidth > el.clientWidth + 1);
  // 3. Covered controls: something sits on top of a link, button or field at its centre.
  const covered = all.filter(el => el.matches('a[href], button, input, select, textarea, [tabindex]') && inView(el.getBoundingClientRect()))
    .filter(el => { const r = el.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
      if (x < 0 || x >= vw) return false; const hit = document.elementFromPoint(x, y); return hit && !el.contains(hit) && !hit.contains(el); });
  // 4. A raised surface inside another raised surface: the card-in-a-card.
  const raised = el => css(el).boxShadow !== 'none' && !el.matches('a, button, input, select, textarea');
  const nested = all.filter(el => { if (!raised(el)) return false; let p = el.parentElement;
    while (p && !raised(p)) p = p.parentElement; return !!p; });
  const report = {
    sidewaysScroll: document.documentElement.scrollWidth > vw,
    axes: [...axes].sort((a, b) => b[1] - a[1]).map(([k, n]) => `${k} ×${n}`),
    longCentred,
    spills: spill.filter(a => !spill.some(b => b !== a && a.contains(b))).map(name).slice(0, 10),
    covered: covered.map(name).slice(0, 10),
    nestedRaised: nested.map(name).slice(0, 10),
    shadows: [...new Set(all.map(el => css(el).boxShadow).filter(v => v !== 'none'))],
    zIndexes: [...new Set(all.filter(el => css(el).position !== 'static').map(el => css(el).zIndex).filter(v => v !== 'auto'))],
  };
  console.table(Object.fromEntries(Object.entries(report).map(([k, v]) => [k, Array.isArray(v) ? v.length + ': ' + v.join(' | ') : v])));
  return report;
})();
```

Reading it: an axis is written `L40 ×5` (five lines start at x = 40), `C640` (centred on x = 640) or `R1180` (lines
end there). Axes with a single line are usually button labels and badges; count the ones carrying two or more.
`spills` names the box whose content is too wide (the fix is usually `min-width: 0` on it or on its grid or flex
child). The probe sees what is rendered, so a screen it passes at one width can still fail at another; run it at
360 and 1280 at least, and on each state of the atlas.

## Checks

Each line is pass or fail on the built screens.

- [ ] The brief has the screen's job line, the ranked content list, and the three wireframes with the scoring table
      and a reason for each rejection.
- [ ] Every margin, padding, gap and inset is a `--space-*` token (the spacing grep returns nothing); the three
      rhythm tiers are each at least 1.5× the one below.
- [ ] The probe at 1280 and at 360: no sideways scroll, no spills, nothing covered, no nested raised surfaces, no
      centred block over three lines, and the axis count within the limit (or the `DESIGN.md` exception).
- [ ] Reading order equals source order at every width (each hit of the reordering grep is justified).
- [ ] At most three shadow tokens and two z-index tokens, all from `tokens/depth.css`; popovers and dialogs use the
      top layer; every shadow falls the same way.
- [ ] Text over images or video passes the white-image test.
- [ ] The hero passes the mute test and the swap test, fits the first viewport at 1280×720 and 360×640 with its
      action, and shows there is more below.
- [ ] Each landing section has its question; no layout runs three times in a row; the close repeats the hero's
      action word for word.
- [ ] Every screen has its state atlas with no blank cell, every state can be forced for review, and each built
      state was looked at (a screenshot per state in the PR).
- [ ] The overflow fixture renders in every component that shows user or translated text without spills, overlap
      or unrecoverable truncation.

## Library cards

The code side lives in the stack library: `fm lib show css-layout` (grid, flexbox, logical properties),
`fm lib show container-queries`, `fm lib show responsive-design` (320 px to wide screens, zoom),
`fm lib show layout-shift` (reserving space for what loads late), `fm lib show skeleton-loading`,
`fm lib show error-boundaries` (partial failure), `fm lib show offline-first` and `fm lib show pwa` (the offline
state), `fm lib show data-tables` and `fm lib show infinite-scroll` (long lists), `fm lib show image-optimization`
(the hero's artefact), `fm lib show toasts`, `fm lib show i18n` (plurals, pseudo-locale, right-to-left),
`fm lib show accessibility` (reading order, live regions). Add `--section verify` for just the checks.
