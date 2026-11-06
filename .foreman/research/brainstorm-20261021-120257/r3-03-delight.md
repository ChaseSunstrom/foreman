# Brainstorm — lens: delight

- **Warm the runner on the first keystroke** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: T-1336 stall work, "it just isn't doing anything", and the 31k-to-15k startup tax all come from the dead wait after Enter. Assumption: the CLI can be spawned and handshaked with no model call.
  Done when: with a fake runner, a worker process exists before Enter and the first event shows within 1s of Enter. An Esc or empty box reaps it with no orphan.

- **Freeze the run with one key** — FEATURE — value 4 — effort M — risk med — category: control
  Why: stop currently kills, and the pack shows no pause. The run is already one process group, so SIGSTOP/SIGCONT gives a lossless pause. Assumption: in-flight API calls may time out on resume, so it falls back to a retry.
  Done when: pause puts the whole worker group in state T with 0% CPU, resume continues the same run id and step, and a pause longer than the stall limit raises no "stalled" event.

- **Never lock the request box: type to steer** — FEATURE — value 4 — effort M — risk low — category: TUI
  Why: the user's steers ("don't stop until complete") arrive mid-run. Making that natural fits their habit. The steer-file idea is listed, but not as a box that stays live with visible feedback.
  Done when: text typed during a run writes a steer record and a chip "folded in at step 3" appears within one frame. Esc cancels an unsent steer.

- **End failed runs with a fail-forward card** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: stalls and failures currently end in a log and a "Next:" line. The card carries a restart brief the run wrote itself: what it learned, the narrowed question, and a suggested runner.
  Done when: a killed fake-runner run produces a card with those three fields, and Enter starts a new run seeded with them.

- **Show "the line that fixed it" on FIX receipts** — FEATURE — value 3 — effort M — risk med — category: receipts
  Why: hunk ablation is listed as a gate, not as something the user sees. The receipt would name the single hunk that turned red to green. Assumption: this only works when one hunk is decisive.
  Done when: on a seeded-bug run the receipt highlights one hunk, and reverting only that hunk turns the test red again.

- **Keep a draft shelf for half-typed requests** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: the user types long, "etc."-style requests, and closed terminals and crashes are in the pack. "Persist the last view" is listed, but not drafts.
  Done when: killing the app mid-typing and relaunching restores the text in that project's box, and the home screen lists drafts across projects.

- **Pre-fill the release sentence in the user's style** — FEATURE — value 3 — effort S — risk low — category: release
  Why: their release asks follow a pattern ("Release 1.2.44: fm code bench, worker leases fixed, macOS CI fixes…"), and they said to stop asking them. Assumption: merged-task titles are close enough to those phrases.
  Done when: given five merged-task fixtures, `fm release` proposes a one-line "Release X.Y.Z: a, b, c" of 160 characters or fewer, using the user's past phrasing where it matches.

- **Tag a fix with "because you said" the first time you hit it** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: complaints get fixed, but the user never sees the connection. This shows a one-time tag at the exact spot, for example the live "heard N s ago" line, quoting their words. It is related to closing the loop on complaints, but fires at the moment of use.
  Done when: a fixed friction item with a stored quote shows a one-time tag on first encounter, and it never shows again.

- **Play a trailer in an empty project** — FEATURE — value 3 — effort M — risk low — category: first run
  Why: the home screen for a project with an empty queue is a dead end. Instead, a muted animated preview of the stations plays a first task derived from the repo's own TODOs. Assumption: the dry-plan path supplies the plan with no model.
  Done when: an empty project with a TODO shows the looping preview, and Enter starts that task for real.

- **Unlock themes from real milestones** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the user asked for looks beyond static colours. Cosmetics earned from the ledger fit that, for example a "night shift" palette after the first unattended run, or a "scar" accent after a recovered failure. Assumption: the ledger can be read for these milestones.
  Done when: seeded ledgers unlock named themes, and `fm code theme` lists locked ones with their unlock condition.

- **Wild: Offer a cookbook recipe of the day as a guided run** — FEATURE — value 3 — effort L — risk med — category: upstream
  Why: assumption: the cookbook's registry.yaml can be indexed. Tips from local usage are listed, but not an upstream notebook turned into a 60-second trial-lane task on the user's own repo.
  Done when: the home screen offers one pinned recipe matching the project's stack, and Try runs it in a throwaway lane and shows the result without touching the tree.

- **Wild: Pay back Foreman's mistakes with a gift task** — FEATURE — value 3 — effort M — risk med — category: goodwill
  Why: a time-debt ledger and a leftover-quota gift are both listed separately. Combined, each stall or false refusal Foreman causes adds to a debt that leftover budget repays with a small proved fix the user didn't ask for. Assumption: debts can be estimated from the stall and refusal events.
  Done when: after a logged stall, the next idle window queues a small gift task on a branch, and the return card says which mistake it repays.

- **Wild: Let a failed check show a replay of its own near-miss** — FEATURE — value 2 — effort L — risk high — category: motion
  Why: assumption: the journal holds the step before the failure. On red, the TUI replays the last 5 seconds before the check, with the failing assertion lit in the diff, instead of dumping a log. It builds on the red-to-green moment and golden-frame replay, but is triggered by failure.
  Done when: a seeded failing check opens the replay automatically, the line that failed is highlighted, and any key skips it.
