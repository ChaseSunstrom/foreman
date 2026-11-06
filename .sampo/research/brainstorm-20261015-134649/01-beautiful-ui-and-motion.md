# Brainstorm — lens: beautiful ui and motion

- **Pin a one-glance "Now" hero at the top of the pane** — FEATURE — value 5 — effort M — risk low — category: layout
  Why: user said "reorganize things so they're on the top"; today the active task sits below the header among ~12 equal cards. Hero = type/tier chip, id, title, stage rail, current step, next line; everything else drops below.
  Done when: at 76 columns the first 8 rows of `fm ui` pane show the task title, stage, current step and next action with no scrolling, and the other cards follow in priority order.

- **Replace the stage list with a horizontal stage rail** — FEATURE — value 5 — effort S — risk low — category: task view
  Why: "● planning ● ready ◉ executing ○ verifying…" wraps and is noisy. Evidence: 8 stages from `fm ui --json`. A rail like `━━●━━◉╌╌○╌╌○` with the current stage's label only; done segments filled, current pulsing.
  Done when: the rail fits in ≤ 40 columns, shows all 8 stages, and only the current stage is animated, verified by a snapshot at 70 and 80 columns.

- **Draw step and criteria progress as a braille/half-block gauge with a travelling highlight** — FEATURE — value 4 — effort M — risk low — category: graphs
  Why: the user asked for better graph visuals; Raster supports braille 2×4 and ▁–█ with 24-bit colour, and `blit` can repaint at 60 fps without a redraw. Gauges get sub-cell precision and a smooth eased fill when steps complete.
  Done when: completing a step animates the gauge fill over ~300 ms, using `blit` only, and there is no redraw while idle.

- **Add a live "work timeline" lane chart (Gantt of tool calls and subagents)** — FEATURE — value 5 — effort L — risk med — category: detail
  Why: the mod sees every tool call with start/end and each subagent; the user wants "more detail" on "things going on". Lanes: main, each subagent, background shells. Bars are coloured by tool kind, with failures in red, over the last ~5 minutes.
  Done when: a 3-subagent session shows 4 lanes with bars that line up with real start/end times, and the chart scrolls while work is live and freezes when idle.

- **Make colour semantic and quiet: a single palette with a "signal budget"** — CLEAN — value 4 — effort M — risk low — category: design language
  Why: constraint "muted grey cards, colour only where it signals". Define about 6 tokens (idle, active, needs-you, ok, warn, fail), used everywhere in the pane, band and transcript rows, so no card colours itself ad hoc.
  Done when: a grep shows no raw colour literals outside the palette module, and at idle only the active-task and needs-you cards carry colour.

- **Collapse cards by priority and fold the quiet ones into a one-line "ticker" footer** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: Bench, Research, Brainstorm, Spend, Files, Gates, Activity are all full cards even when empty. Empty or healthy cards become a single dim row (`Gates ✓ 4/4 · Spend $2.1/$25 · Hooks p95 38ms`) that expands on hover or click.
  Done when: with no bench, research or brainstorm data the pane has no empty cards, and hovering a folded row reveals the full card.

- **Rework the size legend into a typical-time "ghost bar" on the progress gauge** — FEATURE — value 3 — effort S — risk low — category: detail
  Why: the pack calls the legend line "noisy", but the data (typical minutes per TYPE/TIER, `on_task_s`) is useful. Show elapsed against typical as a faint marker on the gauge, which turns amber when it overruns.
  Done when: the legend line is gone, the gauge shows a typical-time tick, and elapsed past typical changes its colour.

- **Give every state a designed empty, loading and error face** — FEATURE — value 3 — effort M — risk low — category: states
  Why: an idle pane with "0 queued · 0 in inbox" is a dead zone. Idle shows a calm dim summary (today's closed tasks as a small day strip); loading uses a skeleton shimmer; a failed `fm ui --json` shows a legible error card with a retry button instead of stale data.
  Done when: killing `fm` shows an error card with Retry, and an empty queue shows a designed empty state with the last closed task.

- **Wild: Turn the mascot into a status narrator whose pose mirrors the work** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the mascot already dances. Pose by state: reading/searching with a magnifier, editing typing, verifying squinting at a checklist, a red gate making it wince, a done task a small confetti burst. It sleeps (static) when idle.
  Done when: five distinct poses are chosen from live tool kinds, and idle draws a static frame with zero timers.

- **Wild: Render the context window as a "tide" Raster that rises and calms** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the band's context gauge is a plain bar. A one-row braille wave whose level is context % and whose amplitude follows tool activity, going flat at idle, warns by turning amber at 80%.
  Done when: the wave amplitude is non-zero only while a tool runs, and the colour changes at the 80% threshold.

- **Wild: Add a completion "stamp" moment when a task closes with its grade** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: closed tasks carry a grade and lenses, but closing is silent. A 600 ms sweep across the hero card, then a grade stamp (A/B/C), then it settles into the "today" strip.
  Done when: closing a task plays the sweep once, then the timers stop, and a reduced-motion setting skips it.

- **Wild: Draw a minimap of the fleet as a live constellation** — FEATURE — value 2 — effort M — risk low — category: fleet
  Why: fleet sessions each have a task and context %. Nodes sized by context %, linked to the parent session, pulsing when active, and a click focuses the steer input for that session.
  Done when: three sessions render as three nodes, with the active one pulsing and the others static, and clicking a node focuses its steer input.

- **Add an animation governor: one frame clock, tiered rates, reduced-motion switch** — PERFORMANCE — value 4 — effort M — risk low — category: motion
  Why: constraints "calm when idle, no flicker, no CPU burn". Today an 8 fps clock is shared everywhere. Use a single scheduler where 60 fps `blit` runs only during short eased transitions, 8 fps only for live spinners, and 0 when idle, with an `fm ui` setting for reduced motion.
  Done when: an idle pane shows 0 timer wakeups over 10 s, and a profile of a live run stays below a set CPU ceiling.

- **Make the Needs-you card a sticky, attention-grabbing banner above the hero** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: approvals waiting on the user are the one thing that blocks all progress, yet today they are a mid-pane card. It is pinned at the very top with a single slow pulse and Approve/Deny buttons with hotkeys, and it vanishes when empty.
  Done when: a pending approval appears above the hero at any scroll position, with hotkeys working, and it takes zero rows when none are pending.
