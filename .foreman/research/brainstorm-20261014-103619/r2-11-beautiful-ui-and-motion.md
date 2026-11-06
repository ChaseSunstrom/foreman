# Brainstorm — lens: beautiful UI and motion

- **Make step drift visible on the band** — FIX — value 4 — effort S — risk low — category: statusline
  Why: T-0759 reports work starting on other steps without the step pointer moving. Today that mismatch is silent.
  Done when: editing a file the plan assigns to a later step, with the pointer behind, turns the band's step glyph into an amber "drifting" state that clears on `fm step`. A pty snapshot test covers both states.

- **Show comment lifecycle chips on the Artifact** — FEATURE — value 4 — effort M — risk low — category: Artifact
  Why: ArtifactComments and ArtifactData are unused. A comment with no visible fate feels like shouting into a void, and assumption: it needs a status field in the shared db.
  Done when: each comment on the page shows a chip that moves sent → seen → in task T-#### → resolved, with a 150 ms crossfade between states. Resolving the task flips the chip without a reload.

- **Encode model and effort in the fleet timeline** — FEATURE — value 4 — effort M — risk low — category: fleet deck
  Why: the Agent tool takes per-call `model` and `effort`, and the pack lists scout=haiku, sonnet reviewers and an inheriting builder. No surface shows who ran on what.
  Done when: the pane and the Artifact draw lanes as swimlane bars. Hue is the model family, stroke weight is effort, and the legend is one line. The palette is also readable in greyscale (pattern fills).

- **Show a failure card with the first red line** — FEATURE — value 4 — effort S — risk low — category: error states
  Why: one parser now reads '✗ exit N' results (T-0750), so the failing command and its first error line are already extractable. Failures currently render as a wall of text.
  Done when: a failed gate renders a fixed card with the command, exit code, first red line and the next move. It stays under 6 terminal rows even when the output is 5,000 lines.

- **Draw a context tide gauge with a compaction mark** — FEATURE — value 3 — effort S — risk low — category: statusline
  Why: Foreman resumes at the exact step after `/compact`, but the user can't see compaction coming. Assumption: the statusline JSON exposes context usage.
  Done when: the band shows a thin gauge with a tick at the projected compact point. Crossing 85% pulses it once, and after a compact the gauge refills with a "resumed at step N" flash.

- **Adapt the statusline to terminal width** — FEATURE — value 3 — effort M — risk low — category: statusline
  Why: the band, pane and statusline all compete for columns. Assumption: today's layout is fixed-width.
  Done when: each segment has a priority and a shed order. Rendering at widths 40, 80 and 160 gives three golden snapshots, and the step and the needs-you flag always survive.

- **Replay a replan as a morph** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the plan is rewritten mid-flight on surprises. The pack's "versioned replans" idea shows the diff as text, but nothing explains the change spatially.
  Done when: in the pane, a replan animates removed steps fading to a ghost row, new steps sliding in, and kept steps keeping their position (FLIP). Reduced-motion users get an instant diff with the same markers.

- **Lint every surface for one-accent hierarchy** — CLEAN — value 3 — effort M — risk low — category: design system
  Why: band, pane, Artifact, web and desktop each grew their own urgency colours. Assumption: nothing enforces a single "red means act now".
  Done when: a smoke check fails if a rendered fixture has more than one element in the critical colour. A screenshot gallery shows the rule holding in the busiest state.

- **Paint the Artifact first from the last snapshot** — PERFORMANCE — value 3 — effort S — risk low — category: loading states
  Why: the Artifact's live data arrives after load, so a blank page reads as broken. Assumption: ArtifactData can hold the last render.
  Done when: opening the page shows the previous board immediately, dimmed with a "refreshing" shimmer. Live data replaces it with a keyed crossfade and no layout jump (CLS ≈ 0 in the smoke recording).

- **Wild: Draw the queue as a subway map** — FEATURE — value 3 — effort L — risk med — category: Artifact
  Why: wild. The queue has dependencies, lanes and blocked states, and a flat list hides all of it.
  Done when: each dependency chain is a coloured line, tasks are stations, and active lanes are small trains easing between them. Clicking a station opens its card, and a blocked line shows a closed-gate marker.

- **Wild: Use epistemic typography for claims** — FEATURE — value 3 — effort M — risk low — category: typography
  Why: wild. Typed claims and the evidence-status ladder exist in verification, but the close-out reads every sentence the same.
  Done when: close-out text renders verified claims in full weight, inferred ones lighter and italic, and unevaluated ones with a dotted underline. Hovering a sentence shows its evidence. In the terminal, the dim and bold attributes stand in.

- **Wild: Give push notifications a glyph grammar** — FEATURE — value 2 — effort S — risk low — category: notifications
  Why: wild. PushNotification is unused, and the user wants only moments that need them. A glance at the lock screen should say which kind it is.
  Done when: every push title starts with a fixed prefix glyph (needs-you, done, stalled, blocked). A test asserts the title plus a one-line default fits a phone lock-screen preview of about 60 characters.
