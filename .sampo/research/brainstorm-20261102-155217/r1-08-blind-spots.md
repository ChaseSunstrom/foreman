# Brainstorm — lens: blind spots

- **Offer to ship when a session ends with landed, unshipped work** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: "Ship this session's landed work to main (fm ship)" is a recurring manual ask, and the push grant is already standing. The blind-spot question is "what finished state is still unpublished when the user stops?" Assumption: a landed-vs-pushed diff is cheap to compute from git and the ledger.
  Done when: ending a session with 2 landed, unpushed tasks prints "2 landed, not shipped: run `fm ship`" with the gate status. A session with nothing pending prints nothing.

- **Recheck a brief's claims when it is picked up, not just when it is filed** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2659 and the "dropped: mostly built" lines show briefs going stale between filing and work. About 30 "Later from" tasks sit deferred for weeks. Only the grounding pass at filing checks them.
  Done when: `fm next` on a brief older than 7 days re-runs its stored canary greps and prints "claim X no longer holds: <file:line>". A fixture brief that cites a since-deleted function gets flagged.

- **Lint that every verb has a MASTER.md anchor with a "use when" line** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the grounding step was changed to read MASTER.md first. That only works if MASTER.md covers the verb table, and the pack shows 2139 files and many "already built" drops that a complete index would have caught.
  Done when: `fm doctor` lists verbs with no MASTER.md entry. Adding a fixture verb with no entry turns that row red.

- **Record effort before and after grounding, per lens** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: "re-grounded to S" and "value 2 after re-grounding" show brainstorm sizes shrinking on contact with the code. Nothing records the shrink, so lenses that inflate scores keep doing it.
  Done when: the funnel ledger stores the raw and grounded value and effort for each idea. `fm ideas stats` prints the mean shrink per lens.

- **Run the suite and hooks under a different uid, an unset HOME and a path with spaces** — FIX — value 3 — effort M — risk med — category: reliability
  Why: assumption: many paths are built from `/run/user/1000` and `$HOME`. Install and verbs have so far been exercised only on the owner's account. The existing "hostile environment matrix" idea does not name uid or HOME.
  Done when: a CI job runs `fm doctor` and the hook tests as uid 1234 with HOME unset and a state dir under "a b". It finds no hardcoded `1000` or `~`.

- **Fire every never-fired hook, verb and guard rule once in a scratch home** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the T-2667 miss was a channel nobody had ever seen fire, and the "no session path" verbs likewise. Counting code that has never run is cheap, while a bug there only shows up later.
  Done when: `fm drill --first-fire` lists code paths with zero ledger hits in 60 days, triggers each in a temp home, and reports crash or silence per path.

- **Replay the same ask in three phrasings and require intake to file one task** — FIX — value 3 — effort M — risk low — category: user value
  Why: the user's asks arrive as terse, varied sentences, and Foreman's own filings show duplicates and "exact duplication" drops. Assumption: intake dedupe is keyed on wording more than on meaning.
  Done when: a fixture of 10 asks × 3 paraphrases produces 10 tasks, not 30, or the gap is reported as a count.

- **Give new guard and gauge tests a mandatory "fails on the planted defect" twin** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: T-2668 shipped with a planted quadratic pattern proving the test can fail. This is the right habit but exists as one task's choice. Without the twin, a test that cannot fail still passes.
  Done when: `fm check` flags a new test file in `plugin/tests` that has no marked planted-defect case. A green test with no twin is listed.

- **Show a "closest existing thing" line when a user ask is filed** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: several recent asks (fm tidy --verbs, the fm doctor row, the gauge cross-check) were mostly already built. The user found out only after a re-grounding pass.
  Done when: filing an ask prints the top 2 matching verbs or closed tasks with ids. The `fm tidy --verbs` ask prints `fm usage --prune`.

- **(wild) Hold a weekly "what surprised me" interview with a cold child that has only the last week's ledger** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the pack's missed asks all looked obvious in hindsight. A reader who did not build the thing sees gaps its authors cannot. The result is filed as candidate asks, not tasks.
  Done when: a Sunday job writes at most 5 questions to the inbox, each citing a ledger line, and the next brainstorm pack lists which were answered.

- **(wild) Keep a "nobody asked, nobody noticed" shelf of Foreman's own silent behaviours, each with a check that someone would notice if it broke** — FEATURE — value 3 — effort L — risk med — category: reliability
  Why: the open questions "what does the user see after a silent fail-open?" and "which unattended paths ever ran on a real clock?" are unanswered. A silence census would give them a home.
  Done when: each silent behaviour (fail-open hook, skipped pace drop, muted prediction kind) has a visible "last heard" time in `fm doctor`. Breaking one on purpose in a drill turns a row red.

- **(wild) Play the user's recent asks back as a test the harness must pass** — FEATURE — value 4 — effort L — risk med — category: user value
  Why: the user's messages are the one signal Foreman did not author. A frozen set of 100 past asks, each with the outcome the user accepted, can score any change to intake, grounding or lenses.
  Done when: `fm exam asks` replays the 100 asks through intake and prints how many match the original task or drop, with the diffs listed.

Next question: Which asks did the user make in plain sessions outside Foreman that never reached any ledger, and how would Foreman learn of them?
Next question: Of the 8 blind spots in this pack, how many were caught by a gauge or test that already existed but nobody ran?
