# Brainstorm — lens: what the user asks next

- **Draft "ship the landed commits" at idle** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: the user's first ask in the pack is "Ship the landed commits to main: T-2848, T-2840…", and the push grant is standing ("push to main any time"). Unshipped landed work recurs every generation.
  Done when: with N landed-unshipped tasks, `fm next` prints a ready-to-run `fm ship` line listing exactly those ids, and it vanishes after the ship.

- **Pre-check every drive-wait claim against live processes** — FIX — value 4 — effort M — risk low — category: drive reliability
  Why: T-2873, T-2900, T-2901 and the earlier two asks are one bug class (the drive miscounts running agents). The user filed five asks on one class.
  Done when: a replay of the five recorded failure ledgers makes the drive's running set match a live-OS-process census in all five.

- **Block moons that score under wild 4 before display** — FEATURE — value 4 — effort S — risk low — category: moonshots
  Why: the user said "the moons aren't that moon-y, I want wild", and a standing rule now sets a floor of 4. Assumption: the rule is enforced only by the reviewer, not at the filing gate.
  Done when: filing a moon with wildness below 4 fails with a reason, and a test plants one.

- **Lint public surfaces for banned names at close** — FEATURE — value 4 — effort S — risk low — category: surfaces
  Why: the user corrected "jarvis" and "Claude as orchestrator" in the scene, and "jeff"/"jev" naming. Nothing checked the site, README or scenes before the user saw them.
  Done when: a seeded "jarvis" in site/ or README fails `fm check` naming the file and line, and the banned list comes from the steers.

- **Warn before a model switch costs 3 minutes** — FEATURE — value 3 — effort S — risk low — category: local models
  Why: the user steered that the llama-swap endpoint takes ~3 minutes per switch with no detection. Assumption: a queue of mixed-model jobs will trigger it again.
  Done when: a queue mixing two models orders by resident model and prints the number of switches it will cause.

- **Turn each typed correction into a sibling sweep** — FEATURE — value 5 — effort M — risk med — category: unspoken needs
  Why: "I meant jeff", "no, jev", "don't showcase it as jarvis" are three corrections in one thread. Each correction hints that the same class is wrong elsewhere.
  Done when: after a correction naming a term, a sweep lists every other file using the wrong term, and a test shows a planted instance found.

- **Predict "also do it for X" after a rename or port** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: T-2851/2852 (site ports) and the Sampo rename each produced follow-ups (tower pages, README header, UI) that the user listed one by one.
  Done when: closing a surface-change task files dormant sibling briefs for the surfaces in coverage.md the change didn't touch.

- **Show a morning "what happened, what I need" card** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: the user sleeps and wants progress by morning, and said "stop asking me for stuff". The card shows closes, stops, spend and the single user-only items.
  Done when: after an unattended run the card is the first output of the next session and fits 15 lines.

- **Wild: Let the predictor write the user's first message of the day** — FEATURE — value 4 — effort M — risk med — category: anticipation (wild)
  Why: assumption: the user's asks cluster into a few recurring shapes (ship, fix drive, more moons), so a draft is cheap to veto with one key.
  Done when: the draft appears at session start and a one-key accept files it unchanged.

- **Wild: Seal tonight's three guesses, score them at wake** — FEATURE — value 3 — effort S — risk low — category: calibration (wild)
  Why: the pack's "Next question" lines are never scored; sealing predictions turns them into a hit rate with a baseline.
  Done when: the morning card shows three sealed guesses against what the user actually typed, and a hit rate accumulates in the ledger.

- **Wild: Dry-run a scratch-worktree rehearsal of the top queued task overnight** — FEATURE — value 4 — effort L — risk med — category: unattended (wild)
  Why: the queue is long (T-0788… deferred) and the user wants progress by morning; a rehearsal on the 27B with the Exam as the judge costs no frontier tokens.
  Done when: the next morning, the top task has a branch that either passes its Exam or carries a one-line reason, and nothing touched main.

- **Count asks the user repeats and promote at three** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: ship requests, drive-wait fixes and "wilder" corrections recur; the user restates them rather than seeing a check.
  Done when: a phrase class asked three times gets a standing check created automatically and is named in `fm doctor`.

- **Hold a draft until its premise is checked against the live endpoint** — FIX — value 3 — effort S — risk low — category: local models
  Why: the model bench asks (T-2886, 2887, 2894) depend on the local endpoint being up and on the right model being loaded.
  Done when: a brief that needs a local model refuses pickup with the specific missing prerequisite when the endpoint is cold or busy.

Next question: which of the user's repeated asks did Foreman already solve once but not durably, and what would a regression test for each look like?
Next question: when the user says "keep going", what exact state of the queue do they think they are leaving behind, and does the morning card match it?
