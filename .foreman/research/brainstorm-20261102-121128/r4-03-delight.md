# Brainstorm — lens: delight

- **Show the red-to-green moment as a one-line "flip" on close** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: the headline claim is "test fails without the change", yet the close shows only a verdict. Earlier ideas include a flipbook, but the small version is one line in the task-finish output: `T-2624 ✗→✓ 3 tests flipped, 0.8s`. Assumption: `fm task prove` already records the before and after runs.
  Done when: closing a task whose prove step recorded a failing run and a passing run prints a single line naming both counts, and a test pins the format.

- **Name the guard's save in plain words** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the guard stops commands in bypass mode, but the pack gives no sign the user ever sees what it stopped, in a form worth showing. A block message such as "Stopped `rm -rf ~/proj`: deletes outside the repo. Nothing ran." makes the save felt. Assumption: guard rules carry a reason string.
  Done when: every guard block prints the command, the rule's one-line reason and "Nothing ran", and a test covers each rule.

- **Greet a clean `fm doctor` with one calm line** — FEATURE — value 3 — effort S — risk low — category: doctor
  Why: doctor is a wall of checks that grows with every ask (timers, canaries, ratchets). When all is well, a single `all clear: 41 checks, 0 warn, last tick 6 min ago` is a reward for keeping things healthy. Assumption: doctor can count its checks.
  Done when: with no WARN or FAIL, `fm doctor` prints at most 2 lines and `--full` restores the list.

- **Celebrate a settled bet in the feed** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: bets settle unattended via `fm night`, and the calibration data (Brier, base rate) is invisible until the user looks. A result line like `bet T-2611 settled: you said 70%, it held. Brier 0.09 ↓` makes the forecasting loop a pleasure.
  Done when: the next session start lists bets settled since the last one, each with stated chance and outcome, and none if there were none.

- **Add a "morning on the site" strip from last night's tick** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: night work is unattended and the user only learns of it from notes. A strip in the web UI (sunrise-coloured, one block per task landed overnight, hatched for blocked) turns a log into a glance. Assumption: the web UI can read the night tick's record.
  Done when: the web UI's home shows one block per overnight task with its state, and an empty night shows a designed "quiet night" state.

- **Give the hard hat a mood from today's record** — FEATURE — value 2 — effort S — risk low — category: brand (wild)
  Why: the logo is a hard hat with a check mark and the site is already a showpiece (`demo/live.svg`). Let the hat on the web UI header and in `fm` banner change: check mark when calibration beats base rate, tilted after a reversed "proven", sunglasses after a 10-task clean streak. Wild.
  Done when: the web header renders one of 3 hat variants chosen by a pure function of the calibration summary, with a test for each branch.

- **Turn a finished day into a 20-second replay SVG** — FEATURE — value 4 — effort M — risk low — category: sharing (wild)
  Why: the README's best asset is a real-session SVG, hand-made. Generate one per day from the task ledger: the stage rail advancing per task, diffs flashing past, proof lines ticking green. The user would post these. Wild. Assumption: the ledger has timestamps and stage events enough to animate.
  Done when: `fm day --svg` writes a self-contained animated SVG under 300 KB for a day with 3+ tasks and renders in a browser with no scripts.

- **Chime softly when a long run lands a pass** — FEATURE — value 2 — effort S — risk low — category: terminal
  Why: drives run unattended for hours and the user steers from elsewhere. A terminal bell (opt-in, `fm config bell on`) at "queue empty" or "blocked on you" is the smallest possible delight and respects reduced-attention setups.
  Done when: with the setting on, a drive finish emits BEL once, and with it off, nothing.

- **Show "what I almost did" when the user overrides the guard** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: overrides are a decision moment and the pack's earlier ideas record them but don't make the moment legible. A two-line card: the command, what it would have touched (paths counted), and "override recorded as not proof".
  Done when: an override prints the affected-path count and writes the override record, and a test asserts the wording includes "not proof".

- **Print each finished task's cost in plain money and minutes** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: usage at 0% and the duel goal (lower cost, less time, T-1231) both make cost the thing users show. `T-2616 · 14 min · $0.42 · 2 retries` at close feeds the duel scoreboard with a human line. Assumption: `fm cost` already tallies per-task tokens.
  Done when: closing a task prints minutes and dollars, and the number equals `fm cost T-id`.

- **Write the weekly changelog in the project's own voice (wild)** — FEATURE — value 3 — effort M — risk low — category: narrative
  Why: 2,600+ tasks have terse commit lines like "T-2610: calibration reads compare like with like". A weekly page, grouped by theme with one human sentence each ("Bets now wait 30 days before they count"), is what a person would read over coffee and the site could host. Wild.
  Done when: `fm week` produces a markdown page where each entry cites its T-id, all ids exist in the ledger, and no entry exceeds two sentences.

- **Play the queue as a train timetable** — FEATURE — value 2 — effort M — risk low — category: web UI (wild)
  Why: the queue (30+ deferred, several blocked on the user) is a flat list. A timetable view shows lanes as tracks, forecast arrival times, and blocked items as "signal red" with the single action that releases them. Wild. Assumption: forecast duration exists or can be estimated from effort letters.
  Done when: the web UI has a queue view with one row per active lane, each blocked item showing its release action, and an empty-queue state.

- **Let a task finish with a tiny "first of its kind" badge** — FEATURE — value 2 — effort S — risk low — category: receipts
  Why: firsts are real milestones (first pass on a new harness, first blind watch exam, first red-to-green on the guard) and nothing marks them. A badge line at close, derived by comparing the task's kind and proof type to history, is cheap and shareable.
  Done when: a task whose (kind, proof kind, harness) tuple never appeared before prints "first: <tuple>" at close, and a repeat doesn't.

Next question: Which moments in a Foreman session does the user already screenshot or copy out, and does any ledger record them?
Next question: Does the web UI have one shared component for verdicts, so any of these touches ship once across every screen?
