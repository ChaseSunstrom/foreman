# Brainstorm — lens: delight

- **Draw the plan in pencil and ink it when proved** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: assumption: the pack shows steps and check chips, but a pending step and a proven one look alike apart from color. Pending steps render as light dashed strokes (`╌`, `⠒`). When the proving command passes, a check draws itself stroke by stroke and the row firms into solid ink. This ties motion to the discipline Foreman sells (nothing is solid until it is proved).
  Done when: a golden-frame sequence shows one step going dashed → mid-stroke → solid on a pass, and staying dashed on a fail.

- **Dissolve between views with an ordered-dither wipe** — FEATURE — value 3 — effort M — risk low — category: transitions
  Why: assumption: the pack proposes cross-fades, but a true fade needs truecolor. A Bayer-matrix dither dissolve built from half-block glyphs looks the same on 16-color and truecolor terminals. It is also deterministic, so frames can be snapshot-tested.
  Done when: switching views on a `TERM=xterm` 16-color pty renders an identical sequence of 6 or more intermediate frames in two runs.

- **Give every worker a livery** — FEATURE — value 4 — effort S — risk low — category: identity
  Why: `fm code` runs on any model or CLI, and `fm code bench` grades several. Each worker gets a stable color pair and a one-cell glyph (derived from its name, overridable in the theme). It appears on its transcript lines, Gantt bars and token columns, so a mixed fleet or a bench run reads at a glance.
  Done when: a bench frame with 3 workers shows 3 distinct liveries, and the same worker keeps its livery across runs.

- **Paint the last frame instantly, then wake it up** — PERFORMANCE — value 4 — effort M — risk low — category: startup
  Why: assumption: cold start currently waits on the harness before anything appears. Paint the previous session's final frame within the first tick, dimmed with a "waking" shimmer, then cross over to live state as events arrive. The TUI feels instant, and the dimmed frame is never mistaken for live data.
  Done when: the first byte of a frame is written in under 100 ms in a bench, and the stale frame is visibly dimmed until the first live event.

- **Make the boot sequence the real `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: startup
  Why: the gates list `fm doctor`, and the pack's ideas include a two-minute opening and a first-run legend. Instead of a decorative splash, show 5–6 checks (guard armed, hooks wired, model reachable, themes valid) ticking green in about a second. A red one stays on screen and names its fix.
  Done when: breaking one check (an unwired guard) leaves the boot screen stopped on that line with its fix, and a healthy boot finishes in under 1.5 s.

- **Change the cursor shape with the run's state** — FEATURE — value 2 — effort S — risk low — category: micro-detail
  Why: assumption: nobody has used the terminal cursor itself as a signal. It becomes a steady bar when the user types, a blinking block when the run waits on the user, and an underline while the model works. It uses DECSCUSR and restores the original shape on exit and on a hard kill.
  Done when: a pty test sees the three sequences emitted on those transitions, and the reset sequence on every exit path.

- **Add a job-site voice pack for microcopy** — FEATURE — value 3 — effort S — risk low — category: microcopy
  Why: the product is named Foreman, yet the status words are generic. Use "clocked in", "inspecting", "signed off", "knocked off for the day", and "hold: needs you". It is a theme-level string table with a plain-English default toggle, so screen readers and recordings keep stable text.
  Done when: swapping the string table changes every status word with no layout shift, and `--plain` restores the neutral set.

- **Toast personal records and milestone numbers** — FEATURE — value 3 — effort M — risk low — category: reward
  Why: assumption: Foreman's local task and run history is enough to compute these. Examples: "fastest first-time pass this week", "10 proved in a row", "T-1300 closed". Toasts are quiet, one line, local only, and off in `--calm`. They reward discipline rather than raw volume.
  Done when: replaying a fixture history triggers exactly the expected toasts, each once, and none appear under `--calm`.

- **Show plan drift as a ghost overlay** — FEATURE — value 4 — effort M — risk med — category: insight
  Why: assumption: the first plan is stored with the later revisions. Press `d` to lay the faded original plan behind the current one, with added steps lit and dropped steps struck through. You see how the model changed course, which is hard to read from the transcript.
  Done when: for a fixture run with 2 plan revisions, the overlay marks the correct added and dropped steps.

- **Grow a repo treemap as edits land** — FEATURE — value 3 — effort L — risk med — category: visualization
  Why: assumption: the file-touch events are in the event log. Draw the repo as a block treemap that lights cells as files are touched, with brightness cooling over time. Replaying it gives a five-second time-lapse of where the work happened. This differs from the existing risk heat-tint, which is a static overlay.
  Done when: replaying a fixture log yields a treemap whose lit cells match the set of edited files, and the time-lapse covers the whole log in the requested duration.

- **Add momentum scrolling with a soft edge bounce** — FEATURE — value 2 — effort S — risk low — category: feel
  Why: assumption: scrolling is currently line-by-line. Spring physics (the springs idea is already listed) applied to the transcript and diff scroll gives inertia and a one-row overshoot at the ends. A "N new" chip shows when the follow-camera is released.
  Done when: a wheel burst of 5 events scrolls farther than 5 lines and settles in under 400 ms. With reduced motion it scrolls exactly 5 lines.

- **Wild: Play "call the verdict" while verify runs** — FEATURE — value 2 — effort M — risk low — category: playful
  Why: wild. During a long verify run, `p` or `f` lets you bet on pass or fail, and a quiet tally keeps your calibration. It turns waiting into engagement and shows the user how often they trust the run correctly. Off by default.
  Done when: a bet is stored and scored against the actual result, and the tally appears in the receipt only when enabled.

- **Wild: Stamp each run with a procedural maker's mark** — FEATURE — value 3 — effort M — risk low — category: keepsake
  Why: wild. Hash the run's task ids and diff stats into a small unique glyph, built like a woodworker's brand from braille and box characters. It is stamped on the receipt and collected in a local gallery (`fm code marks`), and the same run always yields the same mark.
  Done when: the same input log produces a byte-identical mark twice, and two different runs produce different ones.

- **Wild: Hold a "shift handover" where the model signs off in its own words** — FEATURE — value 3 — effort M — risk med — category: ending
  Why: wild. At the end of an unattended run, a three-line handover card appears: what's done, what's risky, what to look at first. Each claim is linked to the proof it came from, and a claim with no proof is shown struck through. It makes the model's closing words honest, which is Foreman's whole point.
  Done when: every line on the card resolves to a logged proof, and a seeded unproved claim renders struck through.
