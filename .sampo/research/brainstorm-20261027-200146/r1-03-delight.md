# Brainstorm — lens: delight

- **Say who holds the gate lock and when it frees** — FIX — value 4 — effort S — risk low — category: waiting feedback
  Why: The pack says a hung check in another project held the machine-wide gate for over 40 minutes, and the 15-minute wait then runs beside it "and says so." A silent wait is the part people notice.
  Done when: while `fm check` waits on the lock, the output names the holder's project, its elapsed time, and a countdown to the 15-minute cutoff, refreshed at least once a second.

- **Make `g` during a run visibly queue** — FIX — value 4 — effort S — risk low — category: app keys
  Why: The pack reports that `g` pressed during a run "waits for it, then works the queue," but the app "only told you to press g later." The keypress should acknowledge itself.
  Done when: pressing `g` mid-run replaces the hint with "queued: starts after T-#### finishes" in the next frame, and the queued state survives a redraw.

- **Turn a stalled card's keys into a live countdown** — FEATURE — value 4 — effort S — risk low — category: stall recovery
  Why: The stalled card already offers `w` wait, `k` kill and `m` switch runner (T-1373). Nothing tells you which one to pick, or how long a stall has gone.
  Done when: after the stall threshold the card shows elapsed stall time and a suggested key with its reason, and the suggestion changes when the cause changes in a test fixture.

- **Clickable task ids in the terminal UI** — FEATURE — value 4 — effort S — risk low — category: terminal navigation
  Why: T-#### appears in every receipt, and `fm code why ID` has to be typed by hand. T-0796 (terminal UI polish: clickable ids) is deferred with no delivered step.
  Done when: each T-#### in the TUI emits an OSC 8 link that runs `fm code why <id>`, and a test checks the escape sequence in the rendered output.

- **Close each task with a plain receipt in seconds and tokens** — FEATURE — value 5 — effort S — risk low — category: close-out
  Why: T-0795 (plain receipts, seconds and tokens shown on close) is deferred. The user tracks usage closely ("cut usage burn," the weekly reset), so a per-task cost line answers the question they keep asking.
  Done when: `fm task finish` prints one line with wall seconds and tokens for the task, and the figures match `fm cost` for the same task ID.

- **Explain a guard refusal in plain English, with the safe alternative** — FEATURE — value 4 — effort S — risk low — category: guard clarity
  Why: The guard hook stops commands in bypass mode, and a bare refusal leaves the user to work out why. The pack shows the same pattern in `fm edit`, which refused a block without saying which line broke the parser.
  Done when: each guard refusal prints the rule that fired, the matched text, and one safe alternative, and each rule has a fixture test that checks all three lines.

- **Land a finished task with a short, skippable moment** — FEATURE — value 3 — effort S — risk low — category: finish motion
  Why: fm extras already has cursor choreography and sonic recipes (T-1556), so a finish cue fits the existing motion work. The brief is delight, and a finish is the moment people remember.
  Done when: a finish plays a motion of at most 1.5 seconds, `--quiet` and `NO_COLOR` skip it, and the closing receipt still prints in full after it.

- **Export a run as one offline zine file** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: fm extras already renders a run as a zine (T-1556). The next step is a file a person can send without a server.
  Done when: `fm extras zine <run>` writes one self-contained HTML file that opens with no network requests, which a test checks by grepping the output for external URLs.

- **Let the Foreman mascot show the run's state** — FEATURE — value 3 — effort S — risk low — category: character
  Why: The pack has fm marks with icons on one grid and empty states (T-1555). A mascot that changes with state gives the terminal a readable mood without extra text.
  Done when: each of the five run states (planning, editing, proving, waiting, stalled) maps to its own frame, and a snapshot test fails if two states share a frame.

- **Wild: Replay a day's runs as a terminal time-lapse** — FEATURE — value 3 — effort M — risk med — category: time travel
  Why: wild. The pack already has History and Today charts, and the journal records each run's events in order, so the data for a replay exists.
  Done when: `fm replay <day>` plays the journal at 10x, pauses on space, and steps one event at a time on the arrow keys.

- **Wild: Give each proven failing test a small badge** — FEATURE — value 2 — effort S — risk low — category: play
  Why: wild. `fm task prove` already shows a test failing before the change and passing after. Each proof is a small win that could be marked on the task.
  Done when: a task with a passing `fm task prove` shows a badge in `fm status`, and the badge goes away if the proof is rerun and fails.

- **Wild: Light the e-paper desk card only when the work bar moves** — FEATURE — value 2 — effort M — risk med — category: ambient display
  Why: wild. The pack says `fm desk` is an e-paper desk card that is never a port. An ambient card that refreshes only on change suits a display that takes seconds to repaint.
  Done when: the desk card redraws only when its displayed value changes, and a test over 60 idle seconds records zero redraws.
