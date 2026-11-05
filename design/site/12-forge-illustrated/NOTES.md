# 12 · The illustrated forge

**Idea:** the approved mark's world, drawn out to a whole forge in the mark's own hand.
The anvil on its rune-cut stone stands in front of a hearth of dry-laid stone. A bonfire of layered gradient tongues burns there in many colours.
The hammer falls every 3.4 s, and every blow throws coloured sparks that climb into a turning starry sky and stay there as stars.
Everything is vector, alive, and coloured from one palette. Each section is a close view of the same forge, with its own fire.

This is now Sampo's theme. Every drawing comes from one set of Python functions (`_src/art.py`), so the page, the mark, the icon and the README banners share one hand.

## The scene (hero)
The scene is a 1200 × 1000 stage split into parallax layers: far, mid, fore and near. The rune stone and anvil are the mark itself at 3.2×, drawn in its own 256 grid. One fire lights all of it.

- **Sky.** A page-level canvas, redrawn only when something visible changes. Its backing store is capped near 2.6 million pixels.
  - It holds 1300 stars as 1–2 px squares, with no trails. Only the brightest, about 25, carry a faint 5 px cross flare.
  - Otava is drawn from real right ascension and declination. The sky turns once every 20 minutes about the pole, and the scroll turns it too.
  - The pole star (the mark's engraved four-point star) and Otava belong to the hero. The pole rides up at 0.3× scroll and leaves the view; beyond the hero they dim to 15 %.
  - Over the fire column the stars wobble in the heat haze.
  - A shooting star crosses every 32–48 s. It is the only streak in the sky: 1.2 px wide, tangent to the turn about the pole where it starts.
  - **Spark-stars.** An ember that stops in the cold air above the fire, or leaves the fire's frame, settles as a star, scattered over a 2-D field (±200 × ±120 px) round where it left, so no arc forms over the fire.
    - Each flashes for two frames as a 3 px square, then is a point like the field's and cools over 6 s to the faint stars round it, and turns with the sky.
    - At most 30 are kept, the oldest retired, and none are drawn outside the hero.
- **Far.** The Copper Mountain range in three depth bands, the farthest close to the sky's colour.
  - Every peak is split into four facets, two to a side, each side split by a crease. Two lightings are drawn, one per theme: by night the faces toward the forge take the fire, by day the faces toward the dawn at the upper right take the sun.
  - Snow lines, a haze band in front of each ridge line, a copper rim layer whose opacity follows the fire, and a haze band drifting in steps.
  - Three standing stones carry faint runes.
- **Hearth.**
  - The hearth face is courses of chamfered stone blocks under a radial falloff from the fire (`hearthRad`): brightest under the flames, darker toward the ends and the floor.
  - Dagaz and othala are cut into it.
  - **Coals:** dark crusts lit on their top edges, each with a fissure drawn as a tapered wedge, hottest at its middle, with heat bleeding onto the crust round it. Only the coals under the plumes are white-hot, and a few glint blue, green or violet.
  - The anvil throws a contact shadow on the face.
  - A capstone rim runs along the top; its fire-lit edge is strongest at the centre.
- **Bellows.** Pear-shaped great bellows (142 × 88, about 1.6:1), seen from above at an angle:
  - they rest in a wooden cradle on a dry-laid stone plinth built against the hearth's left end;
  - the bottom board is fixed, and the top board, with brass studs and a handle, is hinged at the neck;
  - the pleated leather belly (five folds) swells to 1.3× the boards as they open and sags as they shut;
  - a short iron nozzle with a bound collar runs into the hearth wall, its mouth glowing on each breath.
  - The top board opens from 6° to 16° every 4.2 s. As it shuts, a bright wave runs through the coal bed from left to right in 400 ms, the plumes lean away, and the fire's heat rises with it.
- **Fire.** Drawn on its own canvas at 30 fps into a half-resolution backing store, in scene units, with the mark's flame anatomy:
  - a red haze sheet and a gold sheet along the bed;
  - nine plumes: red haze, outer gold-orange, a second tongue, copper-green and violet salt tongues, a cream middle and, in three of them, a blue-to-white core with a white diamond at the root;
  - the coal bed breathing in soft pools, brightened by the bellows' wave and by a pointer near it;
  - the embers riding the convection, each a glowing point, never a streak;
  - soft, edgeless smoke drifting right, its underside lit warm (lighter and greyer by day).
- **Heat haze.** The air over the fire bends the hammer's handle: three still displacement noises (`hz0`–`hz2`, scale 3) on the handle alone, a new one every 140 ms, so its layer re-rasters seven times a second and never per frame. The head keeps its hard edges at 2×, and the fist is not bent. Off under reduced motion.
- **Fore.**
  - The stone's three facets carry hand-cut hatch, pits, chisel marks, cracks, warm and cool rim light, and a fire-lit bevel.
  - A nine-rivet iron band with hammer dents.
  - Five runes cut as a V, not lit tubes (`art.rune_cut`): the cut's opening in the stone's own dark, the upper-left wall in shadow, the lower-right wall and a lip along that edge catching the fire, and the heat only on the narrow floor, in the fire's colour and faint at the cut's ends (`rfl-<colour>`, no pale core). No outline, no blur; the warmth reaches a tenth of the groove past its edge. An ember runs along a rune only when a blow or a pointer calls it, never on a loop.
  - The molten seam is a pool with a meniscus climbing the anvil's foot, rounded ends, and a spill past the near corner. It has a white-hot core, skin islands and drips, and its light is cast down the stone.
  - **The anvil, one steel everywhere** (`art.anvil()`, also in the Smith, the Ward, the How path, the footer and every mark):
    - a mid-tone body, warm where the fire reaches it and cool where the sky does, with a foot in shadow but lit from the seam below;
    - the face seen just from above, warm at the fire's end and cool toward the horn, with the flames reflected in it;
    - mill scale, a blue-white specular along the horn, and a 1 px dark edge;
    - Louhi's hallmark.
  - Real tongs (jaws, a riveted boss and reins to the smith) hold the billet. They are their own sheet over the scene (`.scene .tongs`, `hero.tongs_ov()`), sharing a wrapper with the billet (`.carry`) so the two move as one; the Smith's figure draws them with `<use href="#hz-tongs">`.
  - **The billet is hot steel** (`hero.billet()`). Under everything is the floor of its heat: orange-hot along its length and dull red in the jaws (`billetW`), so between blows it cools through colour and never to the brown of cold steel. Over that is the fresh heat (`.barhot`): white-yellow where the hammer lands (78 % along the bar, `billetH`, `billetHTop` and a soft `hotSpot`), orange toward the free end. Its light lies on the anvil's face (`faceGlow`) and in the air round it (`barGlow`), in its own group (`.barglow`). The edge darkening, the lower edge and the scale (on the free end, the coolest) sit on top, so the bar keeps its form at any heat. Each blow flares the bar white where it was struck (`.bflare`, 260 ms).
- **Light rig** (one fire, everywhere):
  - a pool of fire light on the near flagstones;
  - a light on the anvil's face and horn;
  - the anvil's shadow thrown toward us, skewing and swaying with the flicker;
  - the hero glow;
  - the ridge rim.
  - Each follows the fire's flicker, the bellows breath and the blow flash, written at 15 Hz in steps of .03 (every frame through a flash). A screen-blended bloom lifts the whole scene on every blow; it is shown only for its 160 ms.
- **Near.** A stone quench trough seen a little from above. Its water is a dark mirror with the sky in its far edge, holding the forge's reflection: the flame upside down, drawn out toward us and cut into rows of lens-shaped slivers that slide on a swell (`art.broken_reflection`), with two dashed arcs of ripple. Two steam wisps rise from it, each four soft-edged shapes stacked, widening and thinning as they lift over 5.2 s (`art.wisp`). Its two runes are wet-lit from below. Out-of-focus foreground rocks and hot scale lie on the floor.
- **By day,** the stone and the plinth throw long shadows across the flags toward the lower left.
- **One masonry.** Every course, flag and plinth sits on a joint fill (`.jt`, the `--joint` token): #09080C by night, #3C3942 by day (#5E5A66 at 60 % over the night joint). By day the brick faces are lit (`--sb1a`…`--sb4b`), so the joints stay darker than the faces in both themes.

**A blow** happens every 3.4 s. The hammer is a side-on cross-peen:

- a faceted head with a hard-shouldered peen wedge, a warm fire-side cheek and orange rim, the flames glinting in its white face, and an eye boss;
- an ash handle (`hero.fist()`), gripped near its end by the smith's right hand, gloved and seen from its back: one mass; four knuckles raised under the leather, each its own size, lean and light (`knuckleG`), with no outline; the gaps between the fingers as shadow lines running up between the knuckles; the wrap a curved ridge where the fingers turn under; the thumb laid across the index finger; and one warm rim, on the fire side only. A flared, stitched gauntlet cuff, its hem lit on the fire side. The bare forearm is a tapering limb (the wrist, then the muscle's belly swelling toward the elbow) in skin tone, with a soft terminator, the far half in shadow and a warm rim on the fire side, running up into a rolled linen sleeve out of frame;
- the cheek's warm tint reaches 50 % on the lower-left face of the head (`cheekG`).

Its cycle:

1. it holds raised at 46° with a slight bob;
2. it lifts before the blow (0.46 s): the head rises 34 units and the wrist cocks back 8°;
3. it comes down (0.16 s, accelerating), with a three-frame smear of its head;
4. it strikes at −12° and rebounds on a spring;
5. it lifts again.

On impact:

- a white-blue bloom over the scene, the four-point glint and a long horizontal streak;
- 60 sparks with gravity and drag, cooling white-blue → gold → orange → red, with tapered three-stroke trails:
  - about one in seven burns copper-green, violet or blue, and about one in seven climbs and may settle as a star;
  - sparks bounce off the anvil face and die in the coals;
  - slow ones lie on the floor as scale that cools over 3 s;
- ten flakes of mill scale spall off the billet, are thrown clear of the hot length and cool on the face and floor, never on the bar;
- the billet flattens a little with each blow (up to 7 % after five blows) and flashes. Its fresh heat fades blow by blow (to .83, .66, .49, .32) over the orange-hot floor, and its light to no less than .55. After every fifth blow, once the hammer has lifted clear (0.6 s), the tongs carry it back into the fire (38 units left, 24 up, 0.45 s), hold it in the coals while the fire flares and it loses its flattening (0.6 s), and bring it back white-yellow (0.45 s), before the next lift.
- a 4 px camera jolt;
- the runes pulse outward from the blow, and an ember crawls along one of them (the only time one does);
- one rivet goes blue-hot and cools through gold;
- the flames flare.

You can call a blow yourself: click or tap the forge, or use "Strike the anvil", which works from the keyboard. A pointer near the fire bends the plumes and brightens the coals; over the stone it kindles the nearest rune.

**Arrival:**

1. The still layers are set in from far to near, one per task, and the coals come up first (0–0.6 s). The billet and its tongs (one wrapper, `.carry`), the anvil light, floor shadow and ridge rim wait at 0 until the anvil is lit in; the billet and tongs come in over 0.9–1.5 s, so nothing stands in the sky before the hearth. The hammer waits off the frame on every width (phones show the scene 120 % wide) until it swings in.
2. The fire catches at 0.6 s with a spring overshoot.
3. The anvil and stone are lit into view at 0.55–1.5 s.
4. The hammer swings in from out of frame at 0.85–1.45 s.
5. The runes kindle in turn at 1 s.
6. The first blow lands at 1.6 s and strikes the headline, which waits as cold iron until then (the `--engrave-dim` gradient, at least 6.4:1 by night and 6.6:1 by day; a 3.2 s fail-safe). Its letters flash white-blue, then cool through gold to engraved brass.

**Camera:**

- an idle drift on two slow sines, in half-pixel steps, each layer written only when its step changes;
- scroll parallax at 0.34, 0.17, 0.08 and −0.12 (far, mid, fore, near);
- a dolly-in of 5 % as you leave the hero;
- each station figure is pushed in as it arrives, from scale 1.07 and 26 px down to rest, driven by scroll.

## The stations (each its own fire and vignette)

| Station | Fire | Vignette, with real data |
|---|---|---|
| How | gold | **The forge road** (`stations.how()`): one scene in one eye-level camera, a road along the flank of a hill at night, from the mine at the left to the record house at the right, the eight stations on it at the hero's scale (each 250–400 px wide at 1440, 150–200 px at 390), each lit by its own fire and casting its shadow down the road. I Capture: the mine mouth, timbered, rails out of it, a laden ore tub and a lantern. II Expand: a brass balance on a dressed pillar, ore against a weight, weights stacked by it. III Ground: the assayer's table against the bedrock, a touchstone with four reference streaks and the ore's streak, assay needles, a copper brazier. IV Plan: a lean-to against a dry-laid wall, a slate on a trestle with the piece, its dimension line and steps chalked on it. V Execute: a helve hammer driven by a water wheel and its flume over an anvil and a hot bar. VI Verify: a long stone trough fed by the flume, tongs resting on a trestle and holding a bar in the water. VII Reflect: a grindstone over its trough, a bar held to it. VIII Record: a punch in a press frame over the finished bar, the record house with its lit door and a rack of finished work. Three layers (far ridges with a fog band, the road, near rocks out of focus) pan at .5, 1 and 1.25; as the list is read the camera travels to the station (1.2 s), which lights (its pool on the road, its lamp's bloom, warm rims) and works once. Each station keeps its rune on a waystone at the road's edge. The art has no box: the sky is the page's own, and the frame fades at its sides and foot. Desktop: the road is pinned beside the list (the list has room under it, so the road is whole when the last row is read). Phones and tablets (≤900 px): the road is pinned at the top, 44 % of the screen, and the rows scroll under it; the row just under it is the one read. Without script the road scrolls sideways from the mine, every station lit. By day the hill is at dusk (`--hill-a`, `--hill-b`, `--hill-rock`, `--grass`, `--fog`). |
| Smith | orange | The hero's own forge, closer, through `<use>` of the hero's hearth, hearth front and anvil, with the hearth behind and above. The billet is in the tongs, and the side-on hammer meets it on a 2.6 s beat (keyframes generated from the hero's poses), with sparks and flash. The figure fades out left, right and bottom. The fist and forearm come into frame on the downswing. The session log shows every line from the start: the first three in full colour and the rest in `--ink-dim` (at least 6:1 in both themes); each blow lights two more and the line it ran. Long lines wrap under their own text (`pre-wrap`, a 2ch hanging indent): paths break only after a "/", the long test name only after an underscore, and task ids, flags and diff counts stay whole, so no line is cut at 320 or 1440; a wrapped line's last two words stay together, so none ends on a lone word. |
| Rune | copper green | **A pitch, not a report.** The quench at night: an iron brazier burns copper green, and gen 4 goes into a stone tub of water at an angle in its tongs: the part under the water is dark and bent by refraction, the brazier's flames hang upside down in the water, a lit meniscus and ripples ring the entry, and steam lifts. It plays once each time the section arrives (the bar goes in, the heat dies back, the water rings, the steam bursts and thins); at rest the bar stands in the water, steaming a little. Far behind, on a dark ridge with its crest lit and fog at its foot, the Rune tower stands as the tower page draws it, small and hazed: a foundation with its lit door, four ashlar courses with their rune tiles and their bands (blue, violet, gold, and gen 4 in orange heat), a crenellated crown with its fire, and the first moons kindling above it in violet, gold and red. A nearer ridge closes the foot. The figure dissolves into the page on all four sides (`.fade-x`). The text is two sentences and a "Climb the tower" plate. |
| Ward | blue | The whole stone and anvil in frame. Each of the nine rivets in the band is set blue-hot in turn: blue flame licks up beside it, then it cools through gold to iron. Pressing a command in the gate flashes every rivet: blue for refused, gold for allowed. The gate's commands are what an agent tries mid-session; the piped download says so ("Inside an agent session, a download piped into a shell"), since the hero's own install is a piped download a person runs. |
| Moons | violet-silver | No grid. Otava in true proportions, its pointers dotted to the pole. Built from the catalogue at build time (`build.moons_from_export()` reads the tower's `genesis.json`, its `moonshots` block): the copy says 58 moonshots, and the arc carries the 20 rated wild 4 or 5, wildest first (the six 5s brighter), shaded toward their terminators and numbered below on leader ticks. Each is drawn at its stage: ideas a thin sliver, kill tests a crescent (M-02, dashed); a built one would be full. The list beside it is the same 20, each with its title, wildness and stage, and links to the whole sky on the Rune page. On the horizon stands the hero's forge seen from afar: hearth courses, coal bed and flames, the stone with its band and the anvil against the glow. Above it are a glow dome and a column of rising sparks. The ridge is a filled, faceted silhouette, its faces toward the forge lit warm (`ridgeLit`) and its far faces in shadow. Each crescent's terminator is soft: the lit side is drawn three times, each a little further into the dark at less light, over a faint earthshine. Below it, the Underworld lists the ideas waiting on a blocker, each by its title with its codename as a small mono tag. |
| Record | gold heat | Each gauge is a forged heat bar lying on an engraved brass ruler: cherry along its length, with scale flakes on the cooler half, and a square-cut end whose white core fades over 20 px under a soft rectangular glow. The Ward's over-budget zone is red. The 21 working days are stacked ingots of ten tasks each, and the peak day is blue-white hot. Hover or focus a day for its evidence runs. |
| Footer | banked | The forge banked for the night, in the hero's perspective: hearth courses, the bed under ash with its cracks breathing slowly, two low blue flames, the stone with its band and cold runes, the anvil with the hammer laid on its face, and embers rising. Its courses sit on the joint fill, so by day the joints are dark and the faces lit. It fades into the page on all four edges. The mark and the heading share one baseline in the left column. |

Every number is the one in direction 10, from stats.json and `fm genesis` (2 November 2026): 1,662 / 7,390 / 690 / 1,349; 414 lanes; 570 blocks; 89 exam results; 252 of 1,472 cells.

## The mark (three levels, one silhouette)
The three levels share the wide rune-cut stone, the anvil over it and the low fire behind.

- **`logo.svg` (96 px and up, 256 grid).**
  - The stone's facets carry hatch, pits, chisel marks and cracks.
  - A nine-rivet band and five engraved runes.
  - The seam pool, and the outline-free anvil with a hot billet.
  - The bonfire has a sheet, five plumes, blue cores and copper-green and violet salts.
  - One engraved star sits above.
- **`logo-simple.svg` (32–96 px, used for the header brand).** The same silhouette with the detail taken out:
  - three plumes with a blue core;
  - one band with three rivets;
  - the seam, the anvil with its lit face, and the billet;
  - no runes and no pits.
- **`icon-16.svg`.** Drawn on the 16 grid with edges on whole and half pixels: the wide stone in three facets with its band, the seam, the anvil, a low three-tongue fire with a blue core.
- **One steel.** Every level uses the same anvil as the page: a mid-tone body and a face warm at the fire's end and cool at the horn.
- **`logo-animated.svg`.**
  - Each plume burns at its own rate, and the seam breathes.
  - The runes kindle and the rivets heat in turn.
  - The side-on hammer swings and strikes the billet every 2.6 s, with a flash and 16 sparks; it rests clear of the star. Its head is the hero's head (hard shoulder, warm cheek, fire-side rim) at the hero's head-to-handle ratio.
  - Embers rise.
  - Reduced motion stops it all on the raised pose.
- **`banner-dark.svg` and `banner-light.svg` (1280 × 320, README header).**
  - The mark's scene with embers.
  - "Sampo" in Bodoni Moda, outlined to paths. Its engraved gradient runs in user space from the cap top to the descender's foot (y 92–212), and its last stop equals the baseline stop, so the p's foot is the same metal as every other foot. By day that bronze is #3C3426.
  - The tagline in Bodoni italic, the "formerly Foreman" line in Martian Mono, and an engraved rule. The night banner has stars and Otava.

## Design tokens
The repo's `design/sampo/tokens.json` can be rebuilt from this section.

### Page colours

| Token | Night (dark) | Daylight |
|---|---|---|
| `night` (page) | `#060819` | `#EEF0F6` |
| `night-2` (raised) | `#0B1030` | `#E2E6F1` |
| `plate` | `#10173D` | `#D6DBEA` |
| `ink` (text) | `#EEF0FA` | `#12163A` |
| `ash` (body) | `#BAC0DD` | `#343A63` |
| `muted` | `#9097BC` | `#555B80` |
| `ink-dim` (steps not being read, unlit log lines) | `#8A90B4` | `#4B5278` |
| `brass` | `#D4AE66` | `#7A5A26` |
| `brass-2` | `#F0D392` | `#5E4418` |
| `rule` | `rgba(212,174,102,.34)` | `rgba(122,90,38,.38)` |
| `rule-2` | `rgba(212,174,102,.6)` | `rgba(122,90,38,.7)` |
| `line` | `rgba(238,240,250,.11)` | `rgba(18,22,58,.13)` |
| `blue` | `#6E9BFF` | `#2448B8` |
| `gold` | `#FFC24D` | `#8A5A00` |
| `green` | `#45E0A0` | `#0F6E48` |
| `violet` | `#BC8BFF` | `#6A3BB5` |
| `orange` | `#FF9440` | `#A2460C` |
| `red` | `#FF6A4A` | `#B12E16` |
| `white-hot` | `#EAF2FF` | `#12163A` |
| `chip` | `rgba(6,8,25,.9)` | `rgba(238,240,246,.95)` |
| `scrim` | `rgba(6,8,25,.92)` | `rgba(238,240,246,.94)` |
| `engrave` (display text) | `#FFF6DD → #F0D392 34% → #B9873F 56% → #E9C98A 78% → #FFF1CC` | `#2A2140 → #12163A 50% → #3A2E1A` |
| `engrave-dim` (the headline before the first blow: cold iron) | `#A4AACA → #8A90B4 56% → #9CA2C4` | `#4B5278 → #454B70 56% → #4B5278` |
| `log-bg` (the Smith's log plate) | `#050714` | `#F4F5FA` |
| `joint` (mortar and the gaps between flags) | `#09080C` | `#3C3942` (#5E5A66 at 60 % over the night joint) |
| `nrock` (the out-of-focus rocks at the hero's foot) | `#07060A` | `#5E5A66` |
| brick faces `sb1a/b` … `sb4a/b` (top / foot of each course gradient) | `#4A4550/#24222A`, `#433F4B/#1F1E26`, `#504853/#2A2630`, `#3C3A46/#1B1A21` | `#7A7482/#524E5A`, `#736E7C/#4E4A56`, `#807884/#58525E`, `#6C6876/#4A4652` |
| `vapor` / `vapor-g` (steam, and the green-lit steam at the quench) | `#E2E8F2` / `#C8F5E2` | `#7E869E` / `#5E8A7C` |
| `sheen` (the sky in the far edge of still water) | `.05` | `.2` |
| Moons ridge `ridge-a` / `ridge-m` / `ridge-b` (near the forge → far) | `#5A2C26 / #2A1A2A / #14132A` | `#B08478 / #9A94AE / #8C96B6` |
| far band 3 (farthest): body / lit upper / lit lower / shade upper / shade lower (`b3a`, `b3k1`, `b3k2`, `b3s1`, `b3s2`) | `#22264A / #383256 / #2E2A4E / #202448 / #1C2042` | `#C8CEE2 / #DEDAE0 / #D4D2DC / #BCC4DA / #B4BCD4` |
| far band 2 (`b2…`) | `#121330 / #36243F / #2A1E38 / #0F1029 / #0C0D24` | `#B4BBD4 / #E2D8D2 / #D6CCCA / #A8B0CC / #9EA6C4` |
| far band 1, nearest (`b1…`) | `#0A0A1A / #2E1C2C / #22162A / #08081A / #060616` | `#9CA4C2 / #E8DCCE / #DACEC4 / #8E98B8 / #848EB0` |
| snow (at .6) / crease | `#9298C4 / rgba(0,0,0,.42)` | `#FFFFFF / rgba(40,46,90,.2)` |
| lit faces | toward the forge (fire) | toward the dawn at the upper right (sun) |
| `plate-bg` (the install command's plate) | `#080B1F` | `#F4F5FA` |
| header bar | `night`, opaque | `night`, opaque |
| standing stones | `#121020 / #1E1A30` | `#6E6A80 / #8A869C` |
| ridge rim (its layer's opacity follows the fire) | `#E09060` | `#C0703C` |
| primary button (forged plate), text on it | `#FFE9B4 → #E9C98A 22% → #C9984C 62% → #8E6226`, text `#1A1206` | same |
| haze peak | `rgba(30,32,78,.6)` | `rgba(238,240,246,.7)` |
| floor wash | none | `rgba(226,230,241,.38)` |
| fire red-haze opacity | `.65` | `.35` |

Contrast, text on `night` (WCAG AA), computed on `night` (and `muted` on `night-2`):

- Night: ink 17.5:1, ash 11.0:1, muted 6.9:1 (6.5:1), ink-dim 6.4:1 (5.6:1 on `plate`), gold 12.4:1, blue 7.4:1, green 11.8:1, violet 7.8:1, orange 9.1:1, red 7.0:1, brass 9.5:1.
- Daylight: ink 15.3:1, ash 9.5:1, muted 5.8:1 (5.3:1), ink-dim 6.6:1 (5.5:1 on `plate`), gold 5.2:1, blue 6.8:1, green 5.5:1, violet 6.3:1, orange 5.4:1, red 5.6:1, brass 5.6:1.
- Engraved figure text, `#9AA3B8` on the slab's stone: 5.9:1.
- The forged plate: `#1A1206` on its face is 11.6:1 at the top and 7.1:1 at mid-height, where the text sits.

### The illustration palette
The forge keeps its own light in both themes, like the mark on daylight.

- **Stone facets:**
  - lit `#5A5560 → #2B2830` (diagonal);
  - front `#3B3A44 → #1C1B22` (vertical);
  - shade `#22232C → #15151B → #3A4258` (cool bounce);
  - top `#8A7F86 → #4A4450`;
  - blocks `#4A4550→#24222A`, `#433F4B→#1F1E26`, `#504853→#2A2630` and `#3C3A46→#1B1A21`.
- **Stone detail:**
  - pits `#000` at .34, with a lip of `#E8E2F0` at .16;
  - hatch `#000` at .17 and `#F4E8E0` at .07;
  - cracks `#08080B`;
  - rim light warm `#FFB070`, cool `#8FA6D6`, bevel `#FFC48A`.
- **Steel (one anvil everywhere):**
  - body `#B8A496 → #7A7476 (6%) → #5A5F6C (22%) → #3C414D (55%) → #1C2029`; base edge `#000` at .3 over the last 15 %; outline `#0B0D12` at .7, 1 px;
  - the face seen from above `#C89A78 → #E8B890 (25%) → #B8B0B0 (55%) → #9AA8C4 (82%) → #C8D8F0` (fire end to the horn), the flames reflected in it `#FFB050` at .55;
  - face line `#FFC48A → #FFE6C8 → #FFD2A8 → #C9D8F0`; horn specular `#DCE8FF` at .5; the foot lit from the seam `#FF8A3A` at .45 → clear;
  - the hero's face light (screen, capped at .42) `#FFB060 → #FF9A4A .8 → #FF8A3A .15 → clear` along the face;
  - hammer head `#C8A890 → #7A7274 (30%) → #3E424C (70%) → #1E2128`, fire-side cheek `#FF9A5A` at .22;
  - `#C9D2DE → #6E7684 (8%) → #2E333C (45%) → #16181D` (other steel);
  - side tint warm `#FF8A3A` at .45 to cool `#7DA2FF` at .35;
  - face line `#F2F6FF`;
  - hammer `#9AA4B6 → #4E5562 → #1B1E25`.
- **Iron:**
  - band `#4A4E58 → #2E3038 → #17181D`, highlight `#A9B4C6`;
  - rivet `#B9C2D2 → #6B7180 → #22252D`;
  - rivet set hot `#FFFFFF → #CFE0FF → #4C78FF`, cooling through `#FFB050` to iron `#6B7180`.
- **Wood, leather and brass:**
  - wood `#7A4E30 → #4E2F1C → #2A1910`; fire-lit top board `#A87448 → #5E3A22 → #2E1A0E`;
  - handle `#B07A4C → #6E4428 → #2E1A0E`;
  - bellows leather, light folds `#8A4A2C → #4A2216 → #1E0C08`, dark folds `#2A120C`;
  - brass studs `#FFF1CC → #E9C98A → #9A6F30`; brass ruler `#FFE6A8 → #E9C98A → #B9873F → #7A5420`;
  - tongs reins `#5A5A62 → #26272D → #0E0F12`;
  - the smith's glove `#5A4434 → #34261E → #140E0B` (`gloveG`), thumb `#5A4030 → #2A1C14`, rim `#FF9A5A`; forearm skin `#2E1A14 → #5E3A2C → #8A5A44 → #B07858 → #D49670` across the limb, shadow side to fire side (`skinG`); sleeve linen `#5E5446 → #3A332A → #1E1A15`, its roll `#A8967A → #6E6250 → #3A322A`.
- **Water:** a dark mirror `#2A2232 → #0E0C16 (35%) → #050408`, the fire's reflection `#FF9440` and `#FFE2A0`, glints `#6E9BFF` and `#45E0A0`, ripples `#C8D8F0` at .22.
- **Light rig:**
  - hearth falloff, radial from the fire (650, 404), r 520: `#FFB060` at .46 → `#E0541A` at .2 (30 %) → `#3A0E06` at .18 (62 %) → `#000` at .6;
  - seam cast `#FF8A3A` at .6 → `#E0541A` at .22 → clear, over 25 units below the seam;
  - floor pool and anvil light use `halo` (`#FFB050` at .5 → `#FF7A2A` at .16 → clear);
  - blow bloom `rgba(235,242,255,.9) → rgba(160,190,255,.35) → clear`, screen blend, peaking at .55 opacity for 160 ms.
- **Billet** (free end → jaws): the floor of heat `#E8661E → #FF8A2C (45%) → #FFA23E (76%) → #E8601C (90%) → #7A2010`, top `#FF9A44 → #FFC874 (76%) → #FF8A36 (90%) → #9A2E14`; the fresh heat `#FFB444 → #FFD866 (34%) → #FFF2B4 (62%) → #FFFCEC (78%, where the hammer lands) → #FFC050 (90%) → #B8361A`, top `#FFD27A → #FFEFB0 (40%) → #FFFFF6 (76%) → #FFD880 (90%) → #D2501E`; the hot spot `#FFFFF4` at .9 → `#FFF6D0` at .45 → clear. Its light: on the anvil face `#FFC060` at .9 → `#FF8A2A` at .45 → clear (`faceGlow`), round the bar `#FFC86A` at .62 → `#FF7A2A` at .22 → clear, centred over the hot zone (`barGlow`).
- **Gen 4 in the quench:** `#121014 → #2A1412 (45%) → #6A1A10 (75%) → #B8301A`, with its heat `#E2481A → #FF8A2A → #FFC24D` fading as it is plunged.
- **Ash** (the banked fire): `#6E6A72 → #2A272E`.
- **Seam:** `#7A1E10 → #E2481A → #FFB03C → #FFF8E6` (centre) and back. Glow `#FF6A1E`, drips `#FFD27A → #E2481A`.
- **Runes:**
  - the V-cut: opening `#2A2226` at .9, lit lower-right wall `#6A5C5C` at .7, lip `#D8CABA` at .42, shadowed upper-left wall `#120E12` at .55; the floor `rfl-<colour>`: the fire colour at .25 at the ends and full from 28 % to 72 % (blue, gold, green, violet, orange, white `#DCE8FF`, red);
  - fires: blue `#6E9BFF`, gold `#FFC24D`, copper green `#45E0A0`, violet `#BC8BFF`, orange `#FF9440`, white-blue `#DCE8FF`;
  - burning: white-gold `#FFE7A8` with a `#FFF8E8` core.

### The fire palette
- **Flame layers** (each runs from its tip at the top down to its base):

  | Layer | Tip → base |
  |---|---|
  | outer | `#FF7022` (transparent) → `#FA621E` at .6 (16 %) → `#F66820` at .94 (30 %) → `#FF8A1F` at .6 → `#FFC24D`: orange as it thins, never a deep red over the night sky |
  | red haze, the outer shell | `#FF7828` clear to 30 % of its height from the tip → `#FA6E24` at .3 (55 %) → `#F86822` at .62 (80 %) → `#F66E28` at .85: a glow round the flame's lower body, gone above 70 % of its height |
  | middle | `#FFB040` (transparent) → `#FFC24D` at .35 → `#FFF1C8` |
  | core | `#3D6BFF` (transparent) → `#4C78FF` at .4 → `#9FC0FF` at .85 → `#EAF2FF` |
  | salt tongues | copper green `#45E0A0 → #A8F5D2`, violet `#BC8BFF → #E2CCFF` |
  | Ward licks | `#3D6BFF` (transparent) → `#4C78FF` at .35 → `#9FC0FF` at .8 → `#EAF2FF` |
  | copper brazier (Rune) | `#1FA87A` (transparent) → `#2FC88E` at .3 → `#7CF0C4` at .75 → `#E6FFF4` |
  | base | `#F4F8FF` |

- **Coal bed:** `#5A1408 → #C8381E → #FFB03C → #FFE9B0` at the hottest. Coals are `#120C10`, lit `#4A2A22`, with edges `#FFE2A0 / #FFB03C / #FF7A2A` and blue, green and violet glints.
- **Sparks, by heat:** `#EAF2FF` (1.0) → `#FFF0C8` (.8) → `#FFC24D` (.6) → `#FF9440` (.4) → `#E2481A` (.2) → `#781E10` (0). Salts take green `#45E0A0`, violet `#BC8BFF` or blue `#6E9BFF` below .85 heat.
- **Strike flash:** `#EBF2FF → #96B9FF → #FF963C`, with a four-point glint `#F4F8FF` and a streak `#DCE8FF`.
- **Heat bar** (record gauges, left to the leading end): `#4A160C → #A8301A (35%) → #F06A1C (65%) → #FFC24D (86%) → #FFF6E0`; the end's white core `#FFF6E0` fades in over 20 px; scale flakes `#2A0C06` at .55; the glow `#FFE2A0 .8 → #FF9A3A .25 → clear`.
- **Moons:** the lit crescent `#F4ECFF → #D2C0F4 → #8A72C8` toward the terminator; the forge far off `#3A2228` (hearth) and `#0B0914` (stone and anvil) by night, `#8A7480` and `#3A3450` by day.
- **Ingots:** `#FFD27A → #FF8A1F → #6A2410`, cap `#FFF1CC` at .5; the peak day and hover `#EAF2FF → #9FC0FF → #2448B8`.
- **Smoke:** `rgba(150,96,70,a)` at the lit underside → `rgba(84,74,92,.7a)` → clear, with `a` .13 by night and .2 by day.
- **Fire by day:** the outer shell keeps its hue and drops its alpha: the haze sheet from .62 to .12 (`--red-op` .14 on the static flames), so no pink haze hangs round the flames.
- **Sky:** stars `#EBF0FF / #AAC4FF / #FFD6A0`, Otava lines `#D4AE66` at .3, pole star `#F0D392`.
- **Station fires:** How gold, Smith orange, Rune green, Ward blue, Moons violet, Record gold.

### Type
The fonts are self-hosted woff2 in `fonts/`, with `font-display: swap` and the display face preloaded. Each family has a short system fallback stack: a long stack cost about 55 ms of cold fontconfig lookups on first layout.

- **Display: Bodoni Moda** (wght 400–600, italic, opsz 6–96). Fallback: `Didot, Georgia, serif`.
  - h1: `clamp(44px,4.5vw,84px)/1`, −0.012em, filled with the engrave gradient.
  - h2: `clamp(38px,4.4vw,66px)/1.02`, −0.01em; its emphasis is italic in the station's fire colour.
  - h3: italic 500, 27px. Label titles: italic 500, 22px.
  - Big numbers: 50–128px.
- **Body: Archivo**, 400–600: 17px/1.62. Fallback: `"Helvetica Neue", Arial, sans-serif`.
  - The lede is 18px, and small text runs 13–15.5px.
  - Navigation is 500 at 15px.
  - The primary and secondary buttons are 600 at 15px, 44px tall.
- **Mono: Martian Mono**, 400–500. Fallback: `Menlo, Consolas, monospace`.
  - Eyebrows, categories, tags and stamps: 12px, 0.12–0.16em, uppercase.
  - Cues: 13px.
  - The smallest text anywhere is 12px, including `code` in the "Or inside Claude Code" line and all figure text (12 SVG units).
  - Code: 0.82em.

### Shape and space
- Radius `2px`. Buttons are cut angular: a 9px chamfer on each corner (`clip-path`), never rounded.
- Gutter `clamp(16px,5vw,80px)`.
- Engraved rules: a 1px hairline in `rule-2`, a 12px tick in `rule` and a 60px major tick.

### Motion: durations and easings
- **Easings:**
  - `spring` is `cubic-bezier(.2,.9,.25,1.05)`;
  - `spring-2` (overshoot) is `cubic-bezier(.3,1.4,.4,1)`;
  - the h1 strike uses `cubic-bezier(.2,.7,.25,1)`.
- **Arrival:**
  - layers rise in over 1.2s on `spring`, 34px up and from 0.98 scale; the far layer takes 2s;
  - the coals come up over 0–0.6s;
  - the fire takes at 0.6s with a spring: 1 − e^(−5t)·cos(6t);
  - the anvil and stone are lit in over 1s from 0.55s; overlays fade in for 0.7s after 0.8s;
  - the hammer swings in over 0.85–1.45s, cubic ease-out from out of frame;
  - the runes kindle at 1s, 140ms apart;
  - the first blow lands at 1.6s; the headline waits at 16 % until then (fail-safe at 3.2s).
- **Hammer (3.4s cycle):** strike pose (731.7, 324.4) at −12°, raised (905, 92) at 40°, wound up (918, 78) at 44°, in scene units about the head's centre.
  - rebound spring for 0.46s: amplitude 20, ω 15, decay 6;
  - lift 0.96s, cubic ease-in-out;
  - hold with a bob: ±3–4 units at 1.9–2.6 rad/s;
  - wind-up 0.46s, cubic ease-out;
  - downswing 0.16s, accelerating with an exponent of 2.4.
- **Blow:**
  - flash 0.5s, quadratic falloff;
  - jolt 4px·e^(−14t)·cos(55t);
  - rune pulse 1.5s, delayed 1.1ms per unit of distance;
  - rivet blue 1.0s, then gold 2.8s;
  - bar cools over 2.8s;
  - fire flare decays at 1.6 per second.
- **Fire:**
  - tongue waves at 5.4 and 9.1 rad/s;
  - height flicker at 7.3, 12.9 and 2.7 rad/s (±8 %, ±5 %, ±4 %);
  - bellows on a 4.2s period: the top board opens 7–18°, giving up to +13 % heat; the puff runs through the bed as it shuts;
  - embers at 6 per second;
  - smoke on a 12–20s life, drifting right;
  - the light rig flickers at 11.3 and 17.9 rad/s.
- **Billet:** flattens up to 2.5 % wider and 7 % lower over five blows (easing at 14/s); its fresh heat cools over 2.8 s after each blow; every fifth blow it goes back to the fire (1.5 s, starting 0.6 s after the blow).
- **Sky:** one turn per 1200s, plus 0.00035 rad per px of scroll; the pole rides up at 0.3× scroll (at most 0.8 of the viewport); redrawn when the farthest star moved 0.5px, at most every other frame; spark-stars fade over 20s; a shooting star every 32–48s, crossing in 0.9s.
- **Bellows:** the top board opens 6–16° on the 4.2s cycle; the belly bulges 0.08–0.3; the puff runs through the bed at 2.75s into each cycle, crossing it in 0.4s and fading over 0.5s.
- **Fire and sparks:** the fire canvas is drawn at 30fps; the spark canvas on the fire's frames (30fps) during a burst, at 10fps while scale cools, never when empty.
- **Light rig:** 15 Hz, in .03 steps, every frame through a flash; the shadow's skew in quarter-degree steps.
- **Camera:** drift in half-pixel steps; each station figure is pushed in from scale 1.07 and 26px down, eased cubic over 85 % of the viewport's height.
- **Station beats:**
  - Smith 2.6s;
  - Ward rivets 6.3s, 0.7s apart;
  - runes idle 4.5s, 0.6s apart;
  - How: the camera travels to a station in 1.2s (`cubic-bezier(.45,0,.2,1)`); the station works once as it arrives (the helve 1.15s ×2 and its wheel 2.8s, the punch 0.9s ×2, the grindstone 2.4s, the balance 1.8s, the chalk and the touchstone streak 1.4s, steam 1.8s ×2, sparks ×2–3); before row I reaches the reading line the camera walks the road once, a station every 2.6s, and rests at the record house; from then on only the row being read moves it;
  - Rune quench, once per arrival: the bar goes in over 0.75s, the heat dies back over 2.8s, three rings over 1.8s, steam over 3.4s;
  - Ward flame licks with the rivets, 6.3s, peaking at 3 %;
  -   - the banked bed's cracks breathe on 5s;
  - a rune's ember crawl, 1.5s, on kindle only;
  - seam breath 3.6s;
  - still flame breath 1.5–2.3s;
  - steam 6s;
  - the far haze band drifts over 38s in 38 steps.
- **Reveals:**
  - text: 0.9s opacity, then 1.3s `spring` translate;
  - Ward bars 1.1s;
  - gauges 1.6s on `spring-2`;
  - ingots 1.2s on `spring-2`, 30ms apart;
  - moons 1s on `spring-2`, 80ms apart;
  - the log shows three lines at once, and each Smith blow sets down two more;
  - the How station lights over 0.7s.
- **Micro-interactions:**
  - nav underline 0.5s `spring`;
  - the forged plate brightens and lifts 1px on hover, and presses to 0.98;
  - buttons scale to 0.95–0.97 on press;
  - gate rows slide 4px and their stamps tilt;
  - the stamp lands in 0.7s on `spring-2`;
  - moons scale to 1.35 on hover;
  - totals lift 3px;
  - gauges glow on hover;
  - the brand icon tilts −4°.

## Fallbacks and quality
- **No JavaScript.** Every drawing is markup inside `<noscript>`, so it renders as-is: the whole hero with the hammer raised, the still flames on the hearth (the live fire's geometry at one instant), 14 faint embers, a still sky with Otava, and every station figure.
  - CSS idle life still runs: the flames breathe, runes and rivets cycle, the Smith hammer strikes, the quench plunges with ripples and steam, and the banked coals breathe.
  - The "Strike the anvil" button stays hidden, and so does Copy (`:root:not(.js) .copy`).
- **Reduced motion.** A still but complete scene: the hammer raised, the still flames, the still sky, and every data reveal shown at once. Steam and sparks are off, and no animation runs.
  - "Strike the anvil" stays. A click shows the strike pose and a still glint and spark for 300 ms, then the raised pose again.
- **Daylight.**
  - A dawn sky with faceted ridges lit from the upper right, a white snow line and haze.
  - Long shadows from the stone and plinth across the flags, visible smoke and a softer red haze.
  - The hearth keeps its own night light, and every page colour is a token.
- **Phones.** At 320 and 390 there is no horizontal overflow. The nav is a disclosure menu ("Sections", 12 px at 320). Both navs carry the same links, "Rune" going to the tower page. The hero runs headline, scene, caption, copy, with the scene 120 % wide so the anvil's waist sits at the centre.
- **Fonts.** The four woff2 files are self-hosted in `fonts/`, and the page uses no other host. With the font files blocked, the system stacks hold the layout at 320, 390 and 1440 with no overflow (checked).
- **Performance:**
  - The still layers of the hero and every station figure are raw text in `<noscript>` until a script sets them in, one per task. Sections render lazily (`content-visibility`) and are made whole one per task after load.
  - Fire, sparks and sky are canvases with their backing stores capped near 2.6 MP. The fire is at half resolution and 30 fps.
  - The spark canvas covers only where sparks, flakes, the smear and the flash can go (scene x 340–1180, y 40–960) at 1.25× at most, and is drawn on the fire's frames; it clears and redraws only the box its particles cover. The sky redraws only on visible change.
  - The scene is its own layer (`will-change: transform` with script), so the scroll zoom moves it rather than re-rastering every layer at each new scale. The screen-blended bloom is `visibility: hidden` except for its 160 ms: even at opacity 0 it cost a blend pass over the scene every frame.
  - No layer whose opacity or transform animates carries a filter.
  - The light rig (glow, pool, anvil light, shadow, rim) is written at 15 Hz in 0.03 steps, on change only; the camera writes a layer only when its half-pixel step changes. Layout is read only after scroll or resize.
  - Offscreen stations pause, and the hero loop does nothing while the hero is out of view.

## Files
- `index.html`: the page, self-contained but for the fonts.
- `site/`: the same page split as the repo will carry it: `index.html`, `style.css`, `site.js` and `fonts/`.
- `fonts/`: the four OFL woff2 files (Bodoni Moda upright and italic, Archivo, Martian Mono).
- `logo.svg`, `logo-simple.svg`, `logo-animated.svg`, `icon-16.svg`, `banner-dark.svg` and `banner-light.svg`: the three mark levels, the animated mark and the README headers.
- `_src/`: the build.
  - The drawing functions live in one place:
    - `art.py`: the vocabulary (stone, runes, band, the one anvil, flames, overlays);
    - `hero.py`: the scene;
    - `stations.py`: the stations and the footer vignette;
    - `marks.py`: the marks and banners. Run it with `uv run --with fonttools --with brotli`.
  - `style.css` holds the CSS, `page.js` the script and `page.html` the markup. `build.py` fills in the drawings, the Smith's generated keyframes and the mark's CSS, then writes `index.html` and `site/`.
  - The QA scripts are `shot.py`, `sections.py`, `fullpage.py`, `frames.py`, `crops.py`, `measure.py` and `sheetshot.py`. They read the page from `http://127.0.0.1:8712/`; serve the folder with `python3 -m http.server 8712`.
- **QA images:** `hero-1440.png`, `hero-1440-light.png`, `phone-390.png`, `phone-320.png`, `section-<name>-1440.png`, `full-1440.png`, `hero-frames.png`, `qa-2x-crops.png` and `logo-sheet.png`.

## QA (headless Chromium, software raster, no GPU)
Round-5 numbers come from `_src/measure.py` (`qa12/measure4.py` in the review's scripts), which takes rAF intervals over 6 s of hero idle, then 7 s of scrolling, plus `longtask` entries buffered from navigation. Main-thread time per frame comes from CDP `Performance.getMetrics`. The machine is shared, so each run gives the 1-minute load it ran at; all ran below 12.

| Run | Load | Hero idle | p95 | Main thread per frame | Scrolling | Long tasks |
|---|---|---|---|---|---|---|
| 1440 @ 2×, five runs | 4.05–4.51 | 58.7–59.3 fps | 16.7–16.8 ms | 5.4–5.6 ms | 58.7–59.3 fps, p95 16.7–16.8 ms | none |
| 1440 @ 1× | 4.15 | 59.5 fps | 16.8 ms | 4.2 ms | 59.6 fps, p95 16.8 ms | none |
| 390 @ 2× | 4.51 | 60.0 fps | 16.7 ms | 3.5 ms | 60.0 fps, p95 16.7 ms | none |

`measure.py`'s scroll steps 90 px every 50 ms, and with `scroll-behavior: smooth` each step restarts the glide, so most of its 7 s is spent in the hero. `qa12/scrollprof.py` scrolls the whole page 30 px a frame instead: every section holds a median of 16.7 ms and a p95 of 16.8 ms at 1440 @ 2×.

- **What it took** (each found by hiding one layer at a time at 1440 @ 2×, since the main thread was only 5–7 ms a frame):
  - the spark canvas sized to where sparks can go, at 1.25× at most, and drawn on the fire's frames;
  - the light rig at 15 Hz in .03 steps (every frame through a flash): each write recomposites a layer the size of the scene;
  - the bloom hidden but for its 160 ms: a screen-blended layer over the whole scene costs a blend pass each frame even at opacity 0;
  - the scene as its own layer, so the scroll zoom moves it instead of re-rastering every layer at each new scale (scrolling past the hero had fallen to 29 fps).
- **Kept from rounds 3 and 4:** `scrollY` read once a frame before any write; the fire at half resolution and 30 fps; the sky drawn only on visible change; no filter on any layer whose opacity or transform animates (the haze sits inside the hammer's layer, on the handle only, and changes 7 times a second).
- **Geometry and the hard bar** (`qa12/r4qa.py`, 30 loads across `index.html` and `site/`, 320 / 390 / 1440, dark and light, with script, reduced motion and no script; `qa12/ovf.py` at nine widths from 320 to 1440 for both pages):
  - no page or console errors, no other host, and no horizontal overflow;
  - `site/` identical to the page once inlined;
  - all HTML text at 12 px or more;
  - the How steps and the Smith log at 6.0:1 or more in both themes, with nothing dimmed by opacity.
- **Checked:**
  - the no-JS full page (13 figures), with no Copy button;
  - reduced motion: no running animations, the strike still poses, and no haze;
  - Daylight, phones at 320 and 390, and 2× crops.
  - Focus is a 2 px gold ring on every control.

## Weakest points (honest)
1. **The frame budget at 1440 @ 2× is met with little to spare.** The idle p95 is 16.7–16.8 ms in five of five runs at load 4–4.5, with 0–3 doubled frames in 6 s. The cost is the display compositor blending a 2880 × 1800 frame in software. Any new full-scene layer that changes every frame will push it back over, so a new effect should be measured by hiding it, as above.
2. **The first render can still be one 70–90 ms task under load.** The page is about 1 MB, almost all of it vector art, and the first parse and style pass is one task. In calm runs there was none.
3. **The station vignettes are CSS loops, not physics.** The Smith's hammer, sparks, quench, licks, steam and tally share no particles with the hero.
4. **The Smith shows the smith's fist only at the blow,** half under the figure's right-edge fade; for the rest of the beat the handle runs out of frame. The closer frame (scene x 420–1060) has no room for the arm at the raised pose.
5. **On phones the Moons chart's numbers shrink with the drawing** (the tower agent set them in ink with a page-colour halo and labels every other one below 560 px); the HTML list beside it carries the same facts. All HTML text is 12 px or more.
6. **The fist and arm are drawn, not painted.** They are now one gloved mass with a ridge, a wrap and a thumb, and a shaded, rimmed forearm. At 2× it reads as a gloved fist; it is still flatter than the anvil, with no knuckle highlights or leather grain.
7. **The Moons section is built from a copy of the export.** `build.py` reads `tower/genesis.json` at build time; the port reads the catalogue itself. The export's summary says `killed: 1`, but no row is at a killed stage (56 ideas, 2 kill tests), so the copy says nothing about kills beyond the two kill tests.
8. **One critique item was not taken:** the 2–3 % idle flicker on the stone's runes (it would repaint a static layer).
9. **The How road is a new drawing** (round 7). Its stations are drawn side-on at the hero's scale with their own lights and shadows, but in flat fills and rims; none yet has the hero's material depth (the anvil's specular, the stone's chisel work).
