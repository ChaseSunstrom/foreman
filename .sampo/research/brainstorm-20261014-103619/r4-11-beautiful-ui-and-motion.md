# Brainstorm — lens: beautiful UI and motion

- **Preview every outbound publish as a diff before it leaves** — SECURITY — value 5 — effort M — risk low — category: privacy UI
  Why: Artifact, PushNotification and ArtifactData are all unused, and each publishes content that may be cached or indexed. Assumption: a redactor already exists, but nothing shows the user what it removed.
  Done when: any Artifact or push payload first renders as original-vs-redacted with changed spans highlighted, nothing is sent until the preview is accepted or an opt-in auto-send setting is on, and a test with a seeded secret shows the span struck out in the preview.

- **Print a day barcode that makes idle stretches impossible to miss** — FEATURE — value 4 — effort M — risk low — category: observability viz
  Why: T-0758 ("make sure it doesn't sit idle") is a live complaint, and idleness is invisible after the fact. One row per minute, coloured working, blocked-on-user, gate running, idle-with-queue or away, with idle-with-queue drawn brightest. Click a gap to jump to the ledger at that minute. Wild.
  Done when: a fixture ledger with a 12-minute idle-with-queue gap renders as a visibly distinct block, and clicking it opens the ledger entry at that time.

- **Show write-conflict states when two surfaces edit the queue** — FEATURE — value 4 — effort M — risk med — category: multi-surface
  Why: earlier ideas let Artifact comments, buttons and phone steers reorder the queue while the terminal and desktop edit it too, with no design for a collision. Assumption: ArtifactData writes are last-write-wins.
  Done when: a scripted reorder from the terminal and from a fake Artifact client within one second shows a "changed on phone · kept / yours" chip on both surfaces, with one-key resolution and no silent loss.

- **Degrade the band through a colour-depth and glyph ladder** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: the band, statusline and pane are drawn with a bespoke palette and glyphs, and T-0744 gave the screenshot harness its own tmux socket. Assumption: only truecolor is snapshotted today. Render each state at truecolor, 256, 16, NO_COLOR and ASCII-only and snapshot the full matrix.
  Done when: `fm smoke --matrix` produces the five variants for the band and pane, and CI fails if any state is indistinguishable from another in the 16-colour, NO_COLOR or ASCII variants.

- **Show a per-turn hook waterfall in the pane** — PERFORMANCE — value 4 — effort M — risk low — category: perf viz
  Why: hooks are latency-gated by bench_hooks.py, but the user only sees pass/fail at release. Draw each turn's hook events as bars (spawn vs work, which hook, ms). Regressions then appear in daily use, not only in the bench.
  Done when: the pane lists the last 20 turns, each with bars for every hook that fired and a total Foreman-added time, and a deliberately slowed hook shows as the longest bar.

- **Mask secret-looking strings at render time, with logged reveal** — SECURITY — value 4 — effort M — risk low — category: privacy UI
  Why: redaction at write time is covered, but the band, pane, Artifacts, notifications and pasted close-outs also display raw tool output. Render a token as `sk-…••••`, reveal it on one keypress, and write the reveal to the ledger.
  Done when: a fixture containing a fake key shows masked in the band, pane and push text, the reveal key shows it once, and the ledger records the reveal.

- **Make the pane mouse-native, with a key for every action** — FEATURE — value 3 — effort M — risk low — category: interaction
  Why: the cockpit frontier asks the user to steer and rewind the plan, but a terminal pane is keyboard-only today. Use SGR mouse reporting for click-to-expand a step, drag-to-reorder queue rows, wheel scrolling and hover for the evidence peek. Every gesture also has a documented key, so nothing is mouse-only.
  Done when: a pty test sends mouse escape sequences, a drag reorders two queue rows with the same result as the keyboard path, and `fm doctor` fails if any gesture has no key binding.

- **Reflow panes by need with hysteresis, so nothing jumps** — FEATURE — value 3 — effort S — risk low — category: layout
  Why: assumption: the band and pane reorder as state changes. Sort sections by what needs the human (asks, then failing, then running) but move a section only after a 2-second dwell and animate it as a slide, not a repaint.
  Done when: a replay of a flapping state (blocked, running, blocked within 1.5 seconds) causes zero section moves, and a sustained change moves one section with a single animation.

- **Lint motion hygiene: tabular numerals, no layout shift, interruptible** — CLEAN — value 3 — effort S — risk low — category: motion
  Why: the earlier motion-grammar ideas set durations but not behaviour under input. Numbers use tabular figures and tween by rolling digits. No animation changes element size. Any keypress or click cancels motion within a frame. The Artifact and desktop CSS are linted for this.
  Done when: a linter flags a fixture with proportional-digit counters or a size-animating transition, and an interaction test shows a keypress cancels a running animation in one frame.

- **Add a linear narration mode for screen readers** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: cursor-moving band redraws are hostile to screen readers. `fm view --linear` appends plain state changes as lines ("T-0759 step 2 of 5 started", "gate failed: exit 1") with no redraws, and the same lines feed the Artifact's aria-live region.
  Done when: the same event fixture yields append-only output with zero cursor-control sequences, and the Artifact renders the lines in an aria-live region.

- **Swipe-review diff hunks as cards (wild)** — FEATURE — value 3 — effort M — risk med — category: review UX
  Why: wild. Swipes on a phone Artifact are the only mobile-friendly way to review code. Each hunk shows with its step and evidence, swipe right to approve and left to request a change with one spoken or typed line, and the pattern of swipes is recorded as a taste signal. This extends the ask deck to hunks.
  Done when: a three-hunk fixture produces two approvals and one change request in the ledger, each tied to a hunk id, and the change request becomes a queue item.

- **Grow a growth-ring tree for each project's releases (wild)** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Each release adds a ring to an Artifact tree cross-section. Width is tasks shipped, dark scars are reverts or escapes, and thin years show where the project was quiet. It's a poster the user would show people, and it's drawn from data the release script already has.
  Done when: running the release script on a fixture history of five releases writes an SVG with five rings, widths proportional to task counts and a scar mark on the release that contains a revert.
