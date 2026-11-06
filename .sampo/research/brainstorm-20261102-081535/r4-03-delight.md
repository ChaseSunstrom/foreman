# Brainstorm — lens: delight

- **Narrate each proof step in plain words as it runs** — FEATURE — value 4 — effort M — risk low — category: proof output
  Why: assumption: the pack shows verdicts and receipts but nothing that lets the user follow a run as it happens.
  Done when: `fm flow` on a fixture prints one line per step ("opened /settings, found Save, clicked it, toast appeared in 0.4s"), and `--quiet` suppresses it.

- **Keep a warm headless browser so `fm shot` feels instant** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: assumption: a cold browser start per shot is the slowest part of UI proof, and the bench gates already track hook latency.
  Done when: the second `fm shot` in a session finishes in under 1s on the fixture app, and the daemon exits after an idle timeout.

- **Overlay the user's mockup on the shot with an onion-skin slider** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: "does it do what the user meant" is often a picture the user already has. The pack has reference-artifact ideas for goals but not a visual compare.
  Done when: `fm shot --mock design.png` writes an HTML page with a draggable 0–100% blend, and a deliberately shifted fixture shows the offset.

- **Pick the most telling frame as each flow's thumbnail** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: the last frame is often a blank "done" state, and the useful moment is just after the action settles.
  Done when: on a fixture flow the thumbnail is the first frame after the last network and animation idle, not the final frame.

- **Turn a spoken complaint into a standing check, with a visible thank-you** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: the user's recurring corrections are the strongest signal in the pack. A "learned from you" line makes it visible that a complaint became a region contract that now runs every time.
  Done when: after "the Save button drifted", a region contract is stored, the next `fm shot` prints "checking Save position (from your note, Nov 2)", and moving the button turns it red.

- **Add a "noticed in passing" line to every shot** — FEATURE — value 3 — effort S — risk low — category: proof output
  Why: assumption: prover runs already see console warnings, clipped text and tiny contrast issues, and nobody reports them unless asked.
  Done when: a fixture page with one console warning and one overflowing label prints both under the verdict, without changing pass or fail.

- **Send a desktop toast with the thumbnail when an overnight proof ends** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: the night tick already runs unattended and the pack lists "unread outputs" as a recurring gap.
  Done when: a finished night proof calls `notify-send` with its verdict line and thumbnail, and the call is skipped (with a ledger line) if `notify-send` is missing.

- **Show a visible ghost cursor and click ripples in flow replays** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: replay SVGs are on the list, but a person can't follow a replay without seeing where it clicked.
  Done when: the replay of a fixture flow shows a cursor path and a ripple at each click, and it is off under reduced-motion.

- **Add a j/k/y/n review mode in the terminal** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the web "tap meant / not meant" idea exists, but this user lives in the terminal. Kitty or sixel graphics inline would keep the review there.
  Done when: `fm review` steps through a task's shots with j/k, y/n records "meant" or "not meant" in the proof ledger, and a terminal without graphics falls back to file paths.

- **Add a "window display" page of every flow's latest frame, greying when stale** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: contact sheets are per finish. A standing page tells the user at a glance which screens were last proven when and which have gone stale since.
  Done when: the web UI page shows one tile per flow, tiles older than the last change to their files get a gray "stale" badge, and an empty project shows a single-sentence empty state.

- **Check the screens a user would show others with `fm demo-ready`** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: assumption: the user shows this project to people (the README carries a demo SVG and a site), so presentability is a real, unstated check.
  Done when: the command shots the named screens, flags clipped text, console errors and placeholder strings, and a clean fixture prints "ready to show".

- **Wild: keep a scrapbook of passing final frames with a hard-hat sticker, flipped monthly** — FEATURE — value 2 — effort M — risk low — category: keepsake
  Why: wild. The proofs already produce pictures, so the project's visual life becomes a collectible and a shareable timelapse.
  Done when: each green flow appends a stamped frame to a scrapbook folder, and `fm scrapbook month` writes an animated page of that month.

- **Wild: race the previous run and this run as two ghost cursors** — FEATURE — value 3 — effort M — risk low — category: performance
  Why: wild. Slowdowns are easier to feel than to read as numbers, and the pack already names noise floors and A/B timing for performance claims.
  Done when: `fm flow --race` plays two ghost runs side by side, ends with the gap in milliseconds, and says "inconclusive" when the gap sits inside the noise floor.

- **Wild: render a failing shot as a "wanted poster"** — FEATURE — value 2 — effort S — risk low — category: failure display
  Why: wild. A red result becomes a shareable one-pager with the region circled, "last seen green" as the last-good commit, and the reproduce command.
  Done when: a red fixture flow writes `wanted.html` showing the circled region, the last-green commit and the exact command to reproduce it.

Next question: Which proof output has the user actually opened, shared or screenshotted in the last month, as recorded by their own file or paste history rather than Foreman's guess?
Next question: What would the user want Foreman to say when a proof can't run on this machine at all, without it reading as a failure?
