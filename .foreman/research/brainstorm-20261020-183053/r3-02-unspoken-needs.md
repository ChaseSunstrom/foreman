# Brainstorm — lens: unspoken needs

- **Add a "look-away safe" screen state** — FEATURE — value 5 — effort M — risk low — category: attention
  Why: the user runs unattended marathons and asks for "needs you" style runs, but a TUI that animates constantly gives no way to tell "fine" from "stuck" at a glance across a room. Assumption: they glance at it while doing other things.
  Done when: a test feeds a fake event log through three states (progressing, waiting on human, wedged) and the rendered frames differ in a single header token and background tint that a golden-frame test asserts.

- **Persist the user's TUI choices across runs** — FEATURE — value 4 — effort S — risk low — category: settings
  Why: the request is "customizable"; the pack shows themes and keybinds but no mention of remembering the last theme, view, motion level or collapsed panels per project. Assumption: it currently restarts at defaults.
  Done when: set theme and motion, quit, relaunch `fm code tui`, and the same theme, view and motion level load with no flags (tested in a pty).

- **Show what changed in the TUI since the previous release** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: the user releases every few hours (1.2.41 to 1.2.44 in one session) and rewrites the TUI after "looked like crap" feedback; a returning user cannot tell what moved. Assumption: no in-product changelog exists for the TUI.
  Done when: first launch after a version bump shows a dismissible two-line "new in 1.2.45" strip that does not reappear on the next launch.

- **Make a "boring mode" the default for CI and recordings** — FEATURE — value 4 — effort S — risk low — category: determinism
  Why: the user has fought CI timing flakes repeatedly (CPU bounds, 3.12 runs, annotations); animation that depends on wall clock will do the same to TUI tests. Assumption: tick loops read real time.
  Done when: with `FM_TUI_CLOCK=fixed`, two runs of the same event log produce byte-identical output on Linux and macOS CI.

- **Rate-limit the TUI's own redraw cost against the harness** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: the user's whole thesis is cheaper and faster than Claude Code, and the bench measures CPU and context tax; a prettier TUI that steals CPU from a worker on a small machine contradicts that. Assumption: render and worker share a host.
  Done when: a bench case runs the same task with TUI on and off, and wall-time delta stays under a stated percentage that CI enforces.

- **Keep all TUI state and exports on the local machine by default** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the pack's thin area is privacy, and proposed features (share as SVG, phone view, recorded clips, crash bundles) all leak paths, prompts and secrets once they leave the box. Assumption: exports currently carry raw text.
  Done when: every export command refuses to write outside the project's state directory without an explicit flag, and a test shows a seeded fake secret and home path replaced in the exported SVG.

- **Add a "why is this so quiet" line during long thinking** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: Haiku marathons with forced compactions have long silent stretches; stillness reads as a hang. Assumption: the harness knows whether it is waiting on the model, a test, or compaction.
  Done when: during a fake 30 s model wait, the footer names the cause and elapsed time, and changes to "compacting" on a compaction event.

- **Let the TUI show Foreman's own overhead honestly** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: the user built `fm cost` Foreman-share and the context-tax ratchet, so they care about proving the tax is small; the TUI could surface it live. Assumption: the data is already computed per session.
  Done when: the token view has a labelled "Foreman's share" column matching `fm cost` output for the same session to the digit.

- **Wild: Turn the TUI into a diegetic "shift log" you can read in ten seconds** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; the user disliked "all the text" and loves pictures. A closing frame of icons only, one glyph per task (proved, red, skipped) in order, summarizes a whole night.
  Done when: finishing a queue prints a one-line glyph strip with counts, and it fits 80 columns for 40 tasks.

- **Wild: Let the user paint a station with their own ASCII art** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; "customizable, extendable" taken literally means personal art, and a text file per station is cheap.
  Done when: dropping `stations/plan.txt` in the theme directory replaces the plan glyph in the next frame, and a malformed file falls back with one warning.

- **Wild: Make the TUI answer "are we winning?" against the Claude Code baseline** — FEATURE — value 3 — effort L — risk med — category: benchmarks
  Why: wild; the user's steer is "better than CC, cheaper/faster". Use stored bench medians to show a live ahead/behind marker for cost and time on the current task type.
  Done when: for a task kind with stored bench data, the header shows a signed cost and time delta versus the baseline median, and shows nothing when no data exists.

- **Fail loudly when a theme makes text unreadable on the docked pane** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: T-1217 shows Claude Code paints the docked pane #262626; static theme colors already clashed with it. Assumption: themes are not contrast-checked on load.
  Done when: loading a theme with a foreground under 4.5:1 contrast against the detected or declared background prints the failing slot and substitutes a corrected color.
