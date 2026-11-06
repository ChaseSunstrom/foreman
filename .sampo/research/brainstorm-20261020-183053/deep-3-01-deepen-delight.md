# Brainstorm — lens: deepen: delight

- **Unify motion into one state-driven animation clock** — FEATURE — value 5 — effort M — risk med — category: motion engine
  Why: the request is "not just static colors"; the existing delight list is many separate effects (breathing border, ripple, particles, plasma). Assumption: they currently have no shared timebase, so each would add its own timers and flicker. One clock with named easing, a frame budget, and a reduced-motion/low-CPU fallback makes every later effect cheap and consistent.
  Done when: a test drives the clock with fake time and asserts that two effects advance in lockstep, that frames are skipped past the budget, and that `FM_REDUCE_MOTION=1` renders zero animated cells.

- **Bind each station to a living glyph that shows its state** — FEATURE — value 5 — effort M — risk low — category: station track
  Why: the user said the TUI "looked like crap with all the text", and the redesign already made a station track. Each station (plan, steps, guard, diff, verify) gets a small animated glyph: spinner while working, a settle on pass, a hold on red. That turns the track from a status row into the thing people watch.
  Done when: a snapshot test renders each station in idle, running, passed and failed states and the four frames differ, with the running glyph cycling across at least 4 frames.

- **Add a gradient theme engine with slow palette drift** — FEATURE — value 4 — effort M — risk low — category: themes
  Why: "not just static colors" is literal. Themes today are flat per-role colors. Themes become 2–3 stop gradients with truecolor and 256-color fallbacks, applied to the work bar, borders and headers, and drifting slowly with elapsed time. It builds on the "weekday palette", "repo mood" and "failures compose the theme" ideas by giving them a single mechanism.
  Done when: `fm code tui --theme dusk` renders the work bar with at least 8 distinct color steps in truecolor and degrades to the nearest 256-color values when `COLORTERM` is unset.

- **Make the guard verdict a three-beat event (flash, cause, settle)** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: merges the verdict micro-animation, shaking frame and bouncer ideas into one staged pattern. A refusal flashes the edge, shows the rule and the one-line way forward (the recent guard hints T-1289/T-1288 already carry that text), then settles into the log. An allowed command gets only a faint tick, so the quiet case stays quiet.
  Done when: a replayed refusal produces three timed render states (flash, hint card, collapsed log row), and an allowed command produces only the tick.

- **Close a task with a proof receipt that assembles itself** — FEATURE — value 5 — effort M — risk low — category: completion
  Why: combines the receipt card, celebration, particles and keepsake file. As a task closes, the criteria tick in one at a time with the command each ran, the diff bars grow, and the time Gantt draws left to right. Then a `fm task receipt T-id` file is saved in plain text. The recent "plain receipts" brief (T-0795) shows the user wants close-out legibility.
  Done when: closing a fixture task renders the receipt in sequence, one criterion per frame group, and writes a receipt file whose content matches the final frame.

- **Add a run timeline scrubber to replay any moment** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: assumption: the TUI already receives events live, so recording them is cheap. Scrub back and forth with the arrow keys, and the stations, plan and diffs re-render as they were. It makes the "ghost of your best run" and "still frame carries the run" ideas possible and doubles as a demo recorder, which the README (`demo/live.svg`) already cares about.
  Done when: `fm code tui --replay RUN` renders the frame at 50% of the recorded duration the same way on two runs, and the left/right arrows step between recorded events.

- **Wild: Grow the plan as a garden whose weather is the run's health** — FEATURE — value 3 — effort L — risk low — category: ambient
  Why: wild; assumption. Merges the plan-tree-with-leaves, pet, mood and scar ideas. Each proved criterion sprouts a leaf, red steps wilt in place, and a calm run gets slow light while a retry-heavy one gets rain. The next run opens with the previous run's scar as a faint branch. It is optional and sits in a side pane.
  Done when: a fixture run with 3 of 5 criteria proved shows 3 leaf glyphs, and a failed step changes that branch's glyph and color.

- **Wild: Race ghosts, with your best run and plain Claude Code on one track** — FEATURE — value 4 — effort L — risk med — category: benchmarks
  Why: wild. The project is built around beating plain Claude Code on cost and time (T-1231, the bench pages, `fm code bench`). A lane per contestant, driven by recorded bench timelines, shows tasks passed against elapsed time and cost. It doubles as a visual for the Benchmarks page. Assumption: bench results hold per-task timestamps.
  Done when: `fm code tui --race A B` draws two lanes from two recorded bench runs and the leader indicator flips at the timestamp where the recorded task counts cross.

- **Wild: Turn the finished run into a title-card sequence with a haiku** — FEATURE — value 2 — effort S — risk low — category: close-out
  Why: wild; merges the title-card, haiku and "bedtime story" ideas. When a long unattended run ends, the screen plays 3–4 cards (what was asked, what changed, what was proved, what's left) and a haiku from the counts (tasks, steps, seconds). Anyone returning to a marathon run reads it in ten seconds.
  Done when: finishing a fixture run renders four cards, and the haiku has 5-7-5 syllables from a deterministic template given the same counts.

- **Wild: Sound the harness with optional quiet terminal bells and a soundscape** — FEATURE — value 2 — effort S — risk low — category: audio
  Why: wild. Unattended runs happen while the user is away. Distinct short bell patterns for "closed green", "needs you" and "red" mean they can hear it from the next room, and silence otherwise (the "harness bells itself quiet when fine" idea). Off by default.
  Done when: with `bell = true` in the TUI config, a needs-you event emits `\a\a` and a green close emits one `\a`, and with the setting off nothing is emitted.

- **Animate view transitions with fade and slide instead of cuts** — FEATURE — value 3 — effort S — risk low — category: transitions
  Why: the recent redesign note already says "views fade the screen"; extend it so panes slide, selections ease, and new log rows push in from the bottom. It is cheap once the shared clock exists.
  Done when: switching views produces at least 3 intermediate frames with decreasing old-view opacity, and with reduced motion it switches in one frame.

- **Pace animations to real throughput, so the motion is data** — FEATURE — value 4 — effort M — risk low — category: data-driven
  Why: merges the border-breathing, pulse line and token-rate ideas. The breathing rate follows tokens per second, the pulse line is the live event rate, and the border color warms as cost approaches the dollar cap. Every moving thing then means something, so it never reads as decoration.
  Done when: a fake token stream at 10 and then 100 tokens/s changes the border cycle period by at least 2x, and the cap proximity changes the border hue step.

- **Build a theme and effects gallery with live preview** — FEATURE — value 3 — effort M — risk low — category: customization
  Why: the TUI request asked for "customizable, extendable", and this grows the effects into a menu. `fm code tui --gallery` shows each theme, glyph set and effect on fake data, with a key to save the pick into config. Users can find the ones they like and show them to others.
  Done when: the gallery lists every shipped theme and effect, previews each in turn, and saving writes the chosen names to the TUI config file.

- **Wild: Let the user bring their own sprite or art pack** — FEATURE — value 2 — effort M — risk low — category: extensibility
  Why: wild; merges "paint a station with ASCII art" and the pet ideas. A pack is a directory with small frame files for station glyphs, the celebration burst and the idle pet, loaded the same way themes are. Assumption: themes already load from files.
  Done when: a pack with a custom 3-frame glyph for the verify station shows those frames in order, and a broken frame file falls back to the default with one note instead of crashing.
