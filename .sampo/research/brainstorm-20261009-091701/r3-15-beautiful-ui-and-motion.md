# Brainstorm — lens: beautiful UI and motion

- **Define a motion grammar and lint it** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: assumption: band, pane, web UI and Tauri app animate independently, and the list has many motion ideas (celebrate, breathe, morph) but no shared rules. One vocabulary (enter, commit, refuse, wait, handoff) with fixed durations and easings. Motion appears only when state changes.
  Done when: a lint in `fm check` fails on any animation or transition not drawn from the token set, and a fixture page demos all five verbs.

- **Add semantic zoom to every session view** — FEATURE — value 5 — effort L — risk med — category: information design
  Why: the user wants to "control every session and project", and 20+ queued tasks plus lanes overflow any flat list. Zoom levels: glance (one orb per project), working (task, step, next action), forensic (ledger, evidence, guard decisions). Scroll or pinch morphs between them without a page change.
  Done when: in a headless browser, three zoom levels render for the same fixture data and the element keeps its identity across the transition (shared-element test passes).

- **Encode state in a glyph alphabet that never relies on color** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: assumption: the statusline, band, pane and desktop each pick their own symbols. One shape-plus-motion alphabet (running, blocked, waiting on you, verifying, done, refused) works in monochrome terminals and for color-blind users, and honours reduced motion with a static variant.
  Done when: a snapshot test renders all states in grayscale and with reduced motion, and each is distinguishable by shape alone.

- **Make every number in the UI explain itself** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: the user reported "band stuck on step 1/5" (T-0406) and "usage runs ahead of pace" confusion. Hover or focus on any figure (step 3/5, 62% pace, cost) shows the ledger events or formula that produced it, with a link to the source.
  Done when: for the step counter, pace gauge and cost total, the popover lists the underlying events, and a test checks that the sum matches the displayed value.

- **Give optimistic actions an honest rollback animation** — FEATURE — value 3 — effort M — risk med — category: interaction
  Why: assumption: the desktop app drives `fm` over a CLI, and the guard or "no active task" refusals can reject an action after the UI has moved. The card slides to its new place immediately; if `fm` refuses, it springs back with the refusal's fix attached rather than a silent revert.
  Done when: a scripted refusal during a drag leaves the card in its original place with a visible reason, and no stale optimistic state remains after reload.

- **Gate motion on a frame budget in `fm smoke`** — FEATURE — value 3 — effort M — risk low — category: performance
  Why: `fm smoke` already drives a headless browser at desktop and phone sizes, but only checks that the UI works, not that it feels smooth. Record dropped frames and long tasks during the key transitions and fail past a budget.
  Done when: a deliberately janky fixture transition fails the smoke run and the baseline passes, with the p95 frame time in the report.

- **Fold the ledger into collapsible chapters** — FEATURE — value 3 — effort M — risk low — category: narrative
  Why: assumption: raw ledger events are a long flat tail. Auto-group them into Plan, Build, Verify and Refusals, each with a one-line summary, and expand with a smooth height animation. The live tail follows only the open chapter.
  Done when: a 500-event fixture renders as at most 6 chapters, each summary is derived from events, and expanding keeps scroll position stable.

- **Draw sparklines in the terminal band** — FEATURE — value 3 — effort S — risk low — category: terminal
  Why: the band and statusline are text only, and the budget gauge is meant to "stay quiet until 75%". Braille or block sparklines for pace, cost and step velocity add data without extra lines, falling back to plain text when width is tight.
  Done when: the band shows a pace sparkline at 80+ columns, degrades cleanly at 40, and a test compares the width-dependent output.

- **Make the diff reader evidence-anchored** — FEATURE — value 4 — effort L — risk med — category: review
  Why: `fm tour` orders changed files in the CLI, but the UI has no equivalent. Each hunk gets chips for the plan step it implements, the test that covered it, and the lens verdicts on it. Unanchored hunks glow as unexplained, and j/k moves between them.
  Done when: for a fixture task every hunk shows its step and coverage chips, and an unlinked hunk is flagged and reachable by keyboard.

- **Publish a live status badge as animated SVG (wild)** — FEATURE — value 2 — effort S — risk low — category: sharing
  Why: wild; assumption: the public repo wants a README that shows the project is alive. A generated SVG shows queue depth, last gate result and a subtle pulse while work is running, with no scripts and no data beyond counts. It is opt-in.
  Done when: `fm` writes a valid, script-free SVG from state, and it renders in a README preview with the pulse disabled under reduced motion.

- **Run lanes as characters in a tiny pixel workshop (wild)** — FEATURE — value 2 — effort L — risk low — category: delight
  Why: wild; lane, reviewer and scout states are invisible when working in the background. An optional view shows each builder at a desk and a reviewer stamping verdicts, so "what is happening" reads at a glance from across the room. It is just another encoding of the existing view model.
  Done when: toggling the view renders one character per active lane, driven only by `fm ui --json`, and it is off by default.

- **Show a stale-work patina that ages briefs and deferrals (wild)** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: wild; the open work holds T-0034, T-0035 and others deferred for a long time, and the user has said cleanup never got done. Queue cards slowly desaturate and gain a faint crack with age, and a revisit renews them, so neglect is visible without a nag.
  Done when: cards for a 60-day-old deferral and a fresh one render visibly different from the same fixture, and acting on one resets its look.

- **Choreograph a single "needs you" moment** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: the user wants fewer interruptions; the ask, approval and block surfaces each notify differently. One choreography dims everything else, lifts one card with the question and its default, and returns to calm when answered.
  Done when: with three simultaneous pending items, exactly one is lifted in order, the rest queue in a badge, and a screenshot test confirms the dimmed state.
