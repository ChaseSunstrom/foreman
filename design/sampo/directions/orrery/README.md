# Orrery: a brass orrery-gear mill in blueprint linework

Feels like: a patent drawing for a machine that runs the heavens, pinned up in the smithy.
Look bank: look-observatory (blue-black, pale cyan reticles) and look-cartographer (drafting lines, a title block).

## Concept

The Sampo as a mechanism. The Kalevala's Sampo has a lid of many colours that turns, and its three mills grind grain,
salt and gold out of nothing. Here that lid is a brass gear wheel, and the three mills are three bodies orbiting a forge
sun, each on its own arm, like an orrery. The inside is a blueprint: dash-dot centre lines, a graduated rim and a dashed
middle orbit. Myth comes from the three mills and the cosmic scale, machine from the gear, the arms and the
drafting. The wordmark is set in drafting capitals inside a title block, with a dimension line under the name.

## Palette

- Gear: blueprint `#0E2A47` filled, hammered bronze `#B07A3B` outline, graduations and arms.
- Linework: blueprint line `#9CCBEB` for the orbits, the centre lines and the lettering.
- Sun: forge light `#FF9E3D`, the only warm light in the mark.
- The three mills: grain in parchment `#F6F0E4`, salt in blueprint line `#9CCBEB`, gold in dark-theme bronze `#D9A870`.
- Mono: one ink, everything as outline except the sun and the three bodies, which are solid.

## Motion

The gear winds back two teeth while the three arms come round into place, inner fastest (360, 240 and 120 degrees
over 4 s), like an orrery being wound. The orbits draw in from faint to full one after another. At the end the sun
flares once. Reduced motion shows the still with the mills at rest.

## Strong

- It is the most "machine" of the three and the most explainable: three outputs from one engine is exactly what
  Sampo does (tasks in, work out).
- The blueprint palette is distinctive: no other dev tool owns brass on blueprint.
- The title-block wordmark gives a ready layout system for docs, release notes and the site, with drafting frames,
  dimension lines and callouts.
- The colour-coded mills can map to status or to lanes in the UI.

## Weak

- It is the most detailed mark. The thin linework (0.6 to 0.9 units) disappears below 48 px, and at 16 px only a gear
  with a dot is left, which risks reading as a generic "settings" cog.
- Gears are a common tech motif. The orbits carry the uniqueness, and they are the first thing to go at small sizes.
- On parchment the dark gear disc is heavy, and the drafting lines lose their glow.
- It is the least warm: the forge reads as a small sun rather than as fire.
