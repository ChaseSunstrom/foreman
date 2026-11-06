# Brainstorm — lens: delight

- **Show the red-to-green flipbook** — FEATURE — value 4 — effort M — risk low — category: receipts
  Why: the demo SVG already shows Foreman's work is photogenic, and "test fails without the change" is the core proof, but it only exists as text. assumption: the red and green runs are stored with their output.
  Done when: `fm task finish` writes a self-contained SVG of about 5 seconds that plays the failing run, the diff, then the passing run, and it renders in a GitHub PR comment.

- **Offer the safe alternative when the guard blocks** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: a block is the most emotional moment in bypass mode, and a bare "no" teaches nothing. assumption: most blocked commands have a one-line safe sibling, such as `--force-with-lease`, a `--dry-run`, or a trash move instead of `rm`.
  Done when: the 20 most common guard rules each print a copy-ready alternative, and a test fails if a rule lacks one or its alternative is itself blocked.

- **Give every lane a name and colour that follow it everywhere** — FEATURE — value 3 — effort S — risk low — category: identity
  Why: lanes, the Agents graph, notifications, logs and the pane are separate surfaces, so "which one stalled?" has to be re-answered on each. assumption: a stable, memorable name works better than an id.
  Done when: one lane shows the same name and colour in the pane, the web UI, a notification and `fm doctor`, and the name derives from the id so it survives restarts.

- **Slide before/after on UI receipts** — FEATURE — value 4 — effort M — risk med — category: web UI
  Why: UI tasks are the hardest to judge from text, and the "unproven (no display)" state is already planned. A real screenshot pair makes the proven state visible. assumption: a headless browser is available when the check runs.
  Done when: a UI task's receipt in the web UI shows a draggable before/after pair, and with no display it shows a hatched "unproven" placeholder instead.

- **Collect earned stickers for firsts** — FEATURE — value 3 — effort S — risk low — category: progress
  Why: ideas so far reward the hat or the day, but not the user's own milestones. Examples are the first guard save, first red-first fail, first settled bet won, first overnight ship, and first correct steer check. A broken streak is never shown.
  Done when: `fm doctor` and the web UI show a sticker sheet of at least 10 firsts with dates and the task id that earned each, and no sticker can be lost.

- **Ask the duck** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: the lessons store and failure history are rich, but they are only consulted by the agent. A human stuck at 11pm gets nothing from them. assumption: the lessons are searchable offline.
  Done when: `fm duck "what I tried"` replies with 3 questions drawn from similar past failures, each citing its task id, and takes no model call when a local match exists.

- **Complete verbs with a reason and a next guess** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: `fm` has a large verb surface, and deferred ideas already note that users need help finding things. Completion is the place a user looks without opening docs. assumption: the shell is bash, zsh or fish.
  Done when: pressing Tab after `fm ` lists verbs with one-line descriptions, and the verb most likely to come next in the current task stage is listed first.

- **Read a fixed bug's gravestone** (wild) — FEATURE — value 2 — effort M — risk low — category: delight
  Why: every closed FIX already has a failing test, which is the bug's cause of death. A page that lists them as epitaphs turns the backlog of fixes into something a person scrolls for fun and shows to others. assumption: the test names are readable.
  Done when: `site` or the web UI has a graveyard page generated from closed FIX tasks, showing date, one-line epitaph and the test that now guards the spot.

- **Hear the factory** (wild) — FEATURE — value 2 — effort M — risk med — category: ambient
  Why: long unattended runs leave the user checking a screen. A quiet ambient layer would let them hear a stall. Soft tones mark a pass, a guard block, a usage wait and a stall, and the ambient layer is off by default.
  Done when: with `fm hum on`, a pass, a guard block and a 5-minute silence each play a distinct sound, and with it off, nothing in Foreman produces sound.

- **Show the morning as a map of the repo** (wild) — FEATURE — value 3 — effort L — risk med — category: overview
  Why: `fm map` already knows layout, with 2117 files and per-directory counts. A treemap tinted by what changed overnight, with proven tiles solid and unproven ones hatched, tells the story in one glance. assumption: the receipt state is tracked per file.
  Done when: the web UI home shows a treemap of the repo where overnight-touched areas glow, and clicking a tile opens the tasks that touched it.

- **Name the ship** — FEATURE — value 2 — effort S — risk low — category: ceremony
  Why: `fm ship` is the one moment the user is sure something real landed, but it ends the way every other command does. A short ship card is the small thing people screenshot.
  Done when: a successful ship prints the tasks shipped, tests added, days since the last ship and the longest-open item it closed, and the same card appears in the web UI.

- **Print a progress bar that is honest about uncertainty** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the forecast-then-score idea exists, but a bar that looks certain misleads. A range band that narrows as steps complete shows what Foreman actually knows. assumption: step durations are logged by kind.
  Done when: the work bar in the pane shows a low-to-high band from past tasks of the same kind and the band narrows as stages close, with a test that a task with no history shows "no estimate", not a guess.

- **Replay a mistake as a kind post-mortem card** (wild) — FEATURE — value 3 — effort M — risk low — category: trust
  Why: reversed "proven" labels and false dones are being audited, but the output is a list. One card per slip should state what Foreman believed, what was true and what check now exists, in the same plain voice every time, so that admitting a slip becomes part of how the product feels.
  Done when: each reversed label produces a card with three fixed fields and a link to the new check, and `fm doctor` shows the count of cards this month.

Next question: Which two-second moments (a block, a pass, a stall, a ship) does the user currently feel nothing at, and which surface do they happen on?
Next question: What would the user show a colleague from a Foreman session today, and what is the first thing they would apologise for?
