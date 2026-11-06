# Brainstorm — lens: beautiful UI and motion

- **Show the model's slot, not just the step** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: fm code has the model fill one small checked JSON slot at a time, with bounded repair. The pack lists no view of what the model actually returned or why it was rejected, so a bad run looks like a mystery. Assumption: the events file records raw slot text and validator errors.
  Done when: replaying an events file that has a rejected slot draws that slot with the invalid field underlined and "repair 2/3" beside it, and a golden frame covers it.

- **Replay the last 15 seconds on demand** — FEATURE — value 4 — effort M — risk low — category: replay
  Why: the user's complaint is that runs go quiet ("it just isn't doing anything"). Whole-run scrubbers are listed, but a glance away needs a different tool. Pressing `b` replays the recent window at 4× in place, then snaps back to live.
  Done when: pressing `b` in a run view with a fixture log re-renders the final 15 s of events at 4× in a test and returns to live, with no extra state kept.

- **Stage the landing hero as a scroll-scrubbed replay** — FEATURE — value 4 — effort M — risk low — category: site
  Why: the user asked for "better examples of fm code on the website", and the hero is still a pre-rendered `demo/live.svg`. `site/build.py` could inline a committed events file, and a small JS reader would scrub it with scroll, with no network and no framework.
  Done when: the built `site/index.html` contains a replay element whose frames come from the committed events file, and a test checks that scroll position N shows frame N's text.

- **Coach on friction, not on a timer** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the user's friction phrases ("why can't I…", "how come … isn't recognized") show that discovery fails at the point of need. Anchored callouts can fire after a repeated wrong key, a dead-end screen or an unknown command, once each, and say what to press.
  Done when: sending three unbound keys in a pty test shows one callout naming the right key, and a fourth does not repeat it.

- **Draw a files × judges verdict matrix** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the harness judges every changed file (guard, restored Git config and hooks, a commit undone), but the run view lists files with no per-judge result. A grid of rows (files) and columns (judges), with a distinct glyph each for pass, fail and skipped, shows where a refusal came from.
  Done when: a fixture run with one guard-refused file renders a matrix with exactly one fail cell, in the right column.

- **Open an action menu on any object** — FEATURE — value 3 — effort M — risk low — category: interaction
  Why: the palette is global. A `.` menu on a selected task, run, file or check would offer only that object's verbs and print the equivalent `fm` command, so keyboard users learn the CLI as they go.
  Done when: `.` on a queued task lists run, defer and show with their `fm` commands, and `.` on a file lists a different set.

- **Mark several items and act as a batch** — FEATURE — value 3 — effort M — risk med — category: interaction
  Why: the home screen and project view can run one task, but "full management" implies acting on many. Space marks rows, a bottom bar morphs to show the count and the batch actions, and a destructive action previews first.
  Done when: marking three queued tasks and choosing defer shows a "3 tasks" preview and applies exactly those three.

- **Small-multiples run history on one time axis** — FEATURE — value 3 — effort S — risk low — category: charts
  Why: past runs are listed as rows. Drawing each as a braille strip with stations coloured by time share, on a shared axis, makes slow outliers and repeat-failure patterns visible without reading numbers.
  Done when: with 10 fixture runs, the one 3× slower run is the only strip drawn with an outline.

- **Pin any value as a watch chip** — FEATURE — value 2 — effort S — risk low — category: widgets
  Why: users cannot keep the one number they care about (failing-test count, tokens, a queue length) visible across views. A pin keeps it as a corner chip with a micro-sparkline.
  Done when: pinning the failing-test count shows the chip in the project view and the run view, and it updates when the count changes.

- **Virtualise long transcripts with scroll anchoring** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: runs with streamed claude events can grow without bound, and the TUI is supposed to stay cheap. Only the visible rows should render, and the viewport should hold its place when lines arrive above it. Assumption: today's renderer formats everything.
  Done when: a 50k-line fixture scrolls with a per-frame cost under a set budget in the bench, and the anchor row does not shift when 100 lines are prepended.

- **Wild: Render a run as sheet music** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Stations are staves, events are notes, a red check is a rest with a flat, and a retry is a repeat sign. It exports as a static SVG and is usable as an overview, since long gaps and busy passages stand out.
  Done when: `fm code score EVENTS --svg` writes a valid SVG with one staff per station that appears in the log.

- **Wild: Show the time and money box as a sundial** — FEATURE — value 2 — effort M — risk low — category: motion
  Why: wild. A request that carries a time or dollar cap gets a sundial in the header. The shadow sweeps toward the cap and shortens when budget is saved, so burn rate reads without numbers. It falls back to a plain bar when motion is off.
  Done when: a fixture at 50% of its cap draws the gnomon shadow at the midpoint glyph, and reduced motion draws a plain bar at 50%.

- **Wild: Blur the transcript by what the harness never verified** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. Model prose is rendered slightly dim and out of focus, and it sharpens only where a check or a quote-back has verified a claim. The screen then shows how much of the story rests on proof. Assumption: claims can be linked to evidence ids from the event log.
  Done when: a fixture with one verified claim and one unverified claim renders the first in normal weight and the second dim, and a `--calm` flag disables the dimming.
