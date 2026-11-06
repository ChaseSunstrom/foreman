# Brainstorm — lens: delight

- **Name every colour in the theme** — FEATURE — value 2 — effort S — risk low — category: theme
  Why: assumption: themes and palettes are shown as hex values and role slots, and none of the listed ideas gives a colour a memorable name. A stdlib name table maps any OKLCH value to its nearest evocative name ("kiln amber", "wet slate"). The names appear in the settings screen, the lookbook, and the design-direction playbook ("accent: kiln amber, never default blue"). A user can then say "less kiln, more moss" instead of nudging hex.
  Done when: `fm code tui --print-config` lists a deterministic name beside each palette role, and the same hex returns the same name on every run.

- **Mark up screenshots in red pencil** — FEATURE — value 4 — effort M — risk low — category: visual QA
  Why: the pack plans screenshot proof loops and critic panels (`fm shot`, a design-critic lens), but none of the listed ideas says how a critique is shown. The reviewer's findings are drawn as wobbly hand-drawn circles, arrows and margin notes in stdlib SVG over the real screenshot. Each mark links to its finding id, so the critique reads like an art director's markup.
  Done when: a failing `fm check design` run writes an annotated SVG in which every finding has a mark, and a finding with no mark fails the test.

- **Give motion weight in proportion to significance** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the pack's ideas cover easing, springs and a state-to-motion table, but all treat events alike. Here a 400-line diff lands with a heavier settle than a one-line read, and a big red result thuds where a small one ticks. Mass is derived from lines changed, cost or duration, and it is capped by the frame budget and disabled under reduced motion.
  Done when: a unit test shows the settle duration and overshoot rising monotonically with event size, and with `--calm` the output is identical for every size.

- **Scale the celebration to how hard the win was** — FEATURE — value 3 — effort S — risk low — category: finale
  Why: the confetti and receipt finales in the list are one-size. T-0217 already tracks first-time passes, so the data exists. A task closed green on the first try gets a quiet nod. One that survived three red verifies gets the full receipt with the near-miss replayed. This keeps the celebration meaningful instead of constant.
  Done when: golden frames for 0, 1 and 3 retries are three distinct finales, and the 0-retry one has no particles.

- **Pick colours by carving a rotating gamut cube** — FEATURE — value 4 — effort M — risk med — category: settings
  Why: the list has an OKLCH picker and a half-block rasteriser separately. Combining them gives a slowly turning OKLCH gamut solid in the settings screen, with the cursor as a point inside it and a live contrast readout against the real background. Out-of-gamut regions are hollowed out so unsafe picks are visibly impossible. Assumption: the rasteriser exists or is built for the station track.
  Done when: moving the cursor changes the candidate colour, and picking a colour with contrast below the floor is refused with the readout shown.

- **Race each easing curve on a track in the motion settings** — FEATURE — value 3 — effort S — risk low — category: settings
  Why: "mixing console" and "rotary dials" are listed, but numbers alone don't convey feel. Each motion token row shows its curve drawn in braille with a dot running along it on a loop, so two tokens can be compared by watching them race. The loop is capped at the frame budget and stops when the row loses focus.
  Done when: the row's dot position at t=0.5 matches the curve function to within one cell, and the dot is static under reduced motion.

- **Render a turntable contact sheet for 3D tasks** — FEATURE — value 4 — effort M — risk med — category: 3D proof
  Why: the request stresses 3D. The pack proposes poster frames and a 3D playbook with a perf budget, but not how a composition is judged from stills. After a 3D task, the headless browser renders six fixed camera angles and two lightings into one grid, plus a short turntable. The grid is attached to the proof, so focal depth and negative space can be checked at a glance. Assumption: `fm shot` or an equivalent headless browser path is available.
  Done when: a scene fixture produces the same 8-tile sheet on two runs (seeded, time frozen), and the sheet is listed in the task's evidence.

- **Wild: Keep tasks as metaballs that merge when proved** — FEATURE — value 3 — effort M — risk low — category: ambient
  Why: wild. Tasks float as blobs in a half-block metaball field, sized by effort. A closed-and-proved task visibly merges into one growing "proved mass" at the bottom, and a failed one is ejected, spinning. It replaces the idle "factory floor" with something calmer and legible from across a room. Assumption: the half-block canvas is available.
  Done when: the field renders from a fixed event log, and the blob count, merged mass and ejections match the ledger counts.

- **Wild: Keep a gallery of the guard's near-miss "mugshots"** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. The guard's refusals are the product's best drama, and the list only adds flashes and ripples. Each blocked command gets a small card with a stroke-drawn icon for its class (an axe for `rm -rf`, a lock for force-push), the reason and the date. `fm vetoes --gallery` is a keepsake of what Foreman saved you from. Commands are secret-scrubbed first.
  Done when: each of the 24 corpus classes renders a distinct icon, and a command containing a token string appears in no card.

- **Wild: Fill a "slop bingo" card as the detector finds generic tells** — FEATURE — value 2 — effort S — risk low — category: design gate
  Why: wild. `fm check design` is proposed with a precision corpus, but its output is a plain list. Each tell found (purple gradient, default shadow, centred hero, Inter-only) fills a square on a 5x5 card. A diff with a full row blocks the close. The playfulness makes the detector something people share instead of resent.
  Done when: running the corpus fixtures fills exactly the expected squares, and a clean crafted page leaves the card blank.

- **Wild: Let the UI wear in with use (patina)** — FEATURE — value 3 — effort M — risk med — category: personalization
  Why: wild. The list personalises by theme, accent and pet, but nothing ages. Over weeks the keys you press most get polished highlights. The panels you never open grow a thin dust tint. Edges of heavily used views soften. All counts stay local, and `--forget` plus a "factory fresh" toggle resets it. Text contrast is never reduced.
  Done when: after a scripted usage history the frames differ from fresh ones only in the patina cells, contrast checks pass, and the reset restores the fresh golden frames.

- **Sign each shipped look with a colour-and-motion "swatch strip" in the receipt** — FEATURE — value 2 — effort S — risk low — category: receipts
  Why: assumption: UI task receipts show before/after frames but no compact record of the look decisions. A one-line strip shows the palette names, the type pairing and the motion tokens used. It can be diffed between releases and lets "what changed in the look" be read in one glance. It reuses the colour names above and the existing design tokens file.
  Done when: closing a UI task appends the strip, and two tasks with identical tokens produce byte-identical strips.
