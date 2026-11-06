# Brainstorm — lens: inversion: how a self-running harness fails: the same miss recurs, corrections are forgotten, subagents run on the priciest model, stopped lanes rot, work waits for the user, hooks and context bloat, predictions are never scored

- **Run a self-fix pre-mortem ledger** — FEATURE — value 4 — effort M — risk low — category: self-repair
  Why: the pack's loops (T-2272, T-2276, T-2290) create fixes and predictions, but nothing shows the *inverse*: which fixes the harness shipped that the same signature then outlived. Assumption: fix-to-recurrence isn't joined today.
  Done when: `fm doctor` prints, per self-born FIX, "held N days" or "recurred on T-NNNN", and a seeded recurrence in a test appears as recurred.

- **Make a correction expire loudly unless it is re-proven** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: the user's words are full of corrections and steers; "corrections are forgotten" is the harness's quietest failure. Assumption: steers have checks (fm decide --check), but corrections that are not steers have no replay.
  Done when: a correction older than 30 days with no replay run is listed by `fm doctor` as "unverified", and a replay that passes clears it.

- **Bill every lane to its model tier and flag overspend** — FEATURE — value 4 — effort S — risk low — category: orchestration cost
  Why: T-2291 picks the model from history, yet nothing reports where the top tier was used when a cheaper one had already passed that tier and type. Assumption: lane records carry model and outcome.
  Done when: `fm lane report` shows "top-tier lanes where a cheaper model passed N of last M same-tier tasks", and a fixture with such history prints the line.

- **Give stopped lanes a rot clock with a recorded disposition** — FIX — value 4 — effort S — risk low — category: lanes
  Why: stopped lanes rotting is named in the lens; T-2289 shows lane rm edge cases already hurting. Assumption: no age-based disposition exists.
  Done when: a lane stopped over 24h without a disposition is listed by `fm doctor` and `fm lane sweep` resumes, salvages or removes it, writing the reason.

- **Count the user's waiting items as a debt with an age** — FEATURE — value 4 — effort M — risk low — category: blocked-on-user
  Why: T-0325, T-0335, T-0352, T-0418 and others sit "blocked" for the user; installs queue for "one yes". Nothing shows how long each has waited or what the user's yes costs. Assumption: blocked reasons are free text.
  Done when: the session start line shows "3 waiting on you, oldest 19 days" with one batched command to answer all, and the count drops after the answer.

- **Fail the ratchet on dead weight, not only on growth** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: T-2281 warns only when the footprint grows; with 1,388 skill files and a 6,400-char rules cap that the user already overrode once, a footprint that never shrinks still bloats. Assumption: no per-rule "last used" is tracked.
  Done when: `fm doctor` lists always-on rules and skill descriptions not matched by any session in 60 days, and a fixture with one unused rule shows it.

- **Time-box every prediction with a mute switch** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: T-2290 scores predictions, but nothing acts on a bad score. Assumption: scores are stored per tier and type with no consequence.
  Done when: a predictor whose last 20 scores are below the "repeat the median" baseline is muted and `fm doctor` says so, and a fixture proves the muting.

- **Test that each self-fix would have caught its own trigger** — FIX — value 4 — effort M — risk low — category: self-repair
  Why: the signal-to-fix loop (T-2272) creates FIX tasks from recurring signatures. The failure mode is a fix that passes its own new test but not the original failure. Assumption: the test is written by the same session.
  Done when: closing a self-born FIX requires replaying the original failing transcript or command and `fm task finish` refuses without it.

- **Wild: Run a "ghost week" that replays last week's inputs against today's build** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild; the user's inputs (requests, corrections) are recorded, so replaying them with a stub model shows which corrections the current build would draw again.
  Done when: `fm replay --week` prints N inputs, M that now trigger a gate the user had to correct, with ids.

- **Wild: Make the harness file a complaint against itself weekly** — FEATURE — value 3 — effort M — risk low — category: self-critique
  Why: wild; the lens's failures are invisible when nobody complains. A forced weekly one-page "what I got wrong" built from recurrences, waits, rot and overspend turns silence into a signal.
  Done when: a dated file exists each week with the five sections and links to tasks, and an empty week states "none" with the counts behind it.

- **Wild: Let a cheap model audit the expensive model's lane before merge** — FEATURE — value 3 — effort M — risk med — category: orchestration cost
  Why: wild; inversion of the router: instead of choosing by history, a Haiku reader tries the lane's task first and the expensive model only takes it on a Haiku failure with the Haiku transcript attached.
  Done when: the lane log shows Haiku-first attempts with pass or escalate and a cost comparison line.

- **Reject a self-change that adds a hook cost beyond its measured benefit** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: hooks have a bench (`bench_hooks.py`) and a p50 in the ratchet, but no per-change budget tied to the miss it fixes. Assumption: the fix task doesn't record added milliseconds.
  Done when: a self-born fix that adds over a set p50 delta fails `fm task finish` unless it records the miss it prevents.

- **Pair every unscored artefact with a scorer or a stated reason** — CLEAN — value 3 — effort M — risk low — category: measurement
  Why: the earlier question "which numbers have never been checked by someone other than the code that produced them" is still open. Assumption: predictions, router picks and trigger precision are written and read by the same module.
  Done when: `fm doctor` lists each stored metric with its independent checker or "none", and none are silently absent.

Next question: Which of Foreman's self-made changes in the last month are still in force, and which did the user quietly undo by hand?
Next question: What does the harness do at the moment a usage limit ends mid-lane, and who sees what resumed?
