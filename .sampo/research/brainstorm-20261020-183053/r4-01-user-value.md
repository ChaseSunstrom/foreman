# Brainstorm — lens: user value

- **Mark a bad frame as a task** — FEATURE — value 5 — effort S — risk low — category: feedback
  Why: the user said the TUI "looked like crap" and had to say so in chat; assumption: a one-key capture is easier than describing it.
  Done when: pressing `!` writes a queued `fm task` with the current frame as text, the theme name, terminal size and `$TERM` attached, and the task shows up in `fm task list`.

- **Calibrate glyphs by eye on first launch** — FEATURE — value 4 — effort S — risk low — category: compatibility
  Why: assumption: tofu boxes and misaligned braille or block glyphs are the likeliest cause of "looks bad", and a terminal can't report its font coverage. Existing ideas auto-degrade but never ask the person looking.
  Done when: first launch shows one row of the glyph sets (blocks, braille, box-drawing, sextants) with "all clean? y/n", the answer picks the glyph profile, and `fm code tui --recalibrate` redoes it.

- **Add a density dial** — FEATURE — value 5 — effort M — risk low — category: layout
  Why: the user steered away from "all the text" toward pictures, but some moments still need words (a refusal, a red test). One continuous `+`/`-` control between pictures-only and full prose settles both, per station.
  Done when: three density levels render different frames of the same event log, the choice persists per station, and a red verify run forces its text open at any level.

- **Direct the camera automatically** — FEATURE — value 4 — effort M — risk med — category: navigation
  Why: assumption: with many views, the user is usually looking at the wrong one when something happens.
  Done when: a guard refusal or failing verify moves focus to that view with a one-line "switched because …" breadcrumb, any manual view key locks the camera, and `L` unlocks it.

- **Share a look as a short code** — FEATURE — value 3 — effort S — risk low — category: themes
  Why: themes, density, motion and glyph profile are all now settings, and the user has no cheap way to move them between machines or to a teammate.
  Done when: `fm code tui --look export` prints a string under 80 characters, `--look import <code>` reproduces identical golden frames, and a malformed code is refused with the reason.

- **Fold idle stretches into time-lapse gaps** — FEATURE — value 4 — effort S — risk low — category: charts
  Why: the Gantt and token charts spend most of their width on long model thinking, which hides the events that matter.
  Done when: any quiet gap over 20 s draws as a compressed `⋯ 3m12s` segment in the Gantt and sparklines, with a key to expand it to true scale.

- **Pin margin notes to events** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the pack shows lessons (T-0217) and steering notes living outside the run. A note on "this refusal was wrong" at the moment of seeing it is the best lesson input there is.
  Done when: `n` on a selected event saves a note tied to the run id and event index, replay shows it at that point, and `fm lessons` can list notes.

- **Turn the TUI's dev loop into scenario packs** — CLEAN — value 3 — effort M — risk low — category: testing
  Why: the golden-frame ideas need inputs that exist. A fixed library of named scenarios makes every view and animation checkable without a model call and gives agents something to iterate against.
  Done when: `fm code tui --scenario guard-storm|100-steps|compaction|empty|crash` plays a scripted event log, and the golden tests render every scenario at three terminal sizes.

- **Hold time-to-first-frame under 150 ms** — PERFORMANCE — value 3 — effort S — risk low — category: startup
  Why: assumption: a stdlib Python launcher that imports everything before painting feels sluggish, which undercuts the "better looks" goal on the first impression.
  Done when: a bench test measures launch to first painted skeleton frame under 150 ms on CI and fails the ratchet above it.

- **Wild: Ship a cockpit skin that changes the layout** — FEATURE — value 3 — effort L — risk med — category: skins
  Why: wild; the user wants more than "static colors". A skin can change structure too: round gauges for context fuel and cost, a plan as a checklist strip, guard verdicts as warning lamps.
  Done when: `--skin cockpit` renders all existing views from the same event log with no data lost, and the golden frames pass for it.

- **Wild: Make the failing test morph into green** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: wild; `fm task prove` (fails without the change, passes with it) is the product's signature moment, as the demo shows. The TUI should stage it as one two-beat animation, not two chips.
  Done when: a proved task plays red chip → diff stamp → green chip in under 1.5 s, is skipped with reduced motion, and the final frame is identical either way.

- **Wild: Leave a morning-after postcard when unattended runs end** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: wild; the user asks for marathon unattended runs. The first screen after one should be a single card (tasks closed, money spent against the cap, what needs a decision) that clears with any key.
  Done when: relaunching after a finished unattended run shows the card once, `--no-postcard` suppresses it, and it fits 80×24.

- **Pick a theme from the work in progress** — FEATURE — value 2 — effort S — risk low — category: themes
  Why: wild-ish; assumption: a user running three repos can't tell panes apart at a glance.
  Done when: each repo gets a stable accent derived from its path hash, shown in the header and tab title, and a setting turns it off.
