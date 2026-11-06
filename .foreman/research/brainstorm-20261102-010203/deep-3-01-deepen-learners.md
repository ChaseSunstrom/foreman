# Brainstorm — lens: deepen: learners

**Answers first.** Poisoned input: the trigger-precision demoter, the lessons recall, and the user model (`fmforesight._requests` already leaked mistaken captures) have, as far as the pack shows, never been fed a deliberately bad input. Trusted gauge: nothing in the pack shows a gauge checked against ground truth except the CI-settled bets.

- **Route every learner write through one immune gate** — FEATURE — value 5 — effort L — risk med — category: learners
  Why: the pack lists 8+ "require a second signal" variants, one per learner. They belong in a single choke point. A candidate rule or lesson is naive, then runs in shadow, then needs two independent signal classes (e.g. CI outcome and user steer) plus a replay self-test before it goes live. Prior art: none found in coding harnesses. Better by: it is one audited path instead of per-learner patches. Novelty 4.
  Done when: `fm learn gate --list` shows every learner's pending, shadow and live items, and a test proves that no learner writes live state without passing it.

- **Run a nightly poison drill against every learner** — SECURITY — value 5 — effort M — risk low — category: learners
  Why: it answers the earlier question about learners never tested with poisoned input. `fm night` feeds each learner a seeded bad input: a false CI red, a mistaken capture, a steer that contradicts MASTER.md, a noisy trigger. Prior art: none found. Better by: learners are proven resistant continuously, not once. Novelty 4.
  Done when: the digest lists one pass/fail per learner, and a learner that absorbs the poison turns the sweep red.

- **Shadow-fire new lessons before they speak** — FEATURE — value 4 — effort M — risk low — category: learners
  Why: clonal selection says a new detector should not act at once. A lesson logs "would have fired" on real tool calls and is promoted only when its hits precede a CI red or a user steer. Prior art: shadow mode in ML ops, not in harness memory. Better by: lessons earn their injected chars with evidence, which the lean ratchet already tracks. Novelty 3.
  Done when: a lesson with zero shadow hits after N sessions never goes live, and one with hits does.

- **Mutate lessons and duel the variants (affinity maturation)** — FEATURE — value 4 — effort L — risk med — category: learners
  Why: ablation duels and the 124-case replay corpus already exist. Generate scope and wording variants of a lesson, duel them on replay and exam scenarios, and keep the cheapest one that holds the pass. Prior art: prompt optimisers such as DSPy, not applied to per-file lessons. Better by: selection uses Foreman's own ground truth and charges chars. Novelty 3.
  Done when: `fm bench duel --mature <lesson>` replaces it with a variant that passes the same cases at fewer chars.

- **Bind each lesson to its evidence and expire it when the evidence goes (antigenic sin + prion check)** — CLEAN — value 4 — effort M — risk low — category: learners
  Why: lessons are recalled per file, yet nothing says the cited file or commit still exists. Store provenance per lesson and flag three kinds: lessons whose source code changed, lessons backed only by other lessons, and lessons imprinted on a first incident. Prior art: none found. Better by: staleness is detected from git and the ledger, not by an LLM re-read. Novelty 3.
  Done when: renaming a cited file marks its lessons "stale" in `fm doctor`.

- **Leave tombstones and apply negative selection** — FIX — value 4 — effort S — risk low — category: learners
  Why: a dropped lesson, a demoted trigger or a mistaken capture can be re-learned from the same input. A tombstone records the signature and the reason. Negative selection also deletes candidates that contradict "self" (MASTER.md clauses, the user's recorded steers) before release. The dropped-as-mistake captures in the pack are the evidence. Prior art: none found. Novelty 3.
  Done when: replaying the input that produced a tombstoned lesson creates no new lesson.

- **Add a regulatory T-cell budget that caps learning after harm** — SECURITY — value 4 — effort M — risk low — category: learners
  Why: the risk budget lowers autonomy after harm, but learners keep adapting. After an incident, a fever state freezes or shrinks all learner step sizes and caps rule changes per day until a clean window passes. Prior art: none found. Better by: it links two existing mechanisms, the risk budget and the learners. Novelty 4.
  Done when: after a recorded harm event, `fm doctor` shows "learning fever" and a second learned change that day is refused.

- **Score every learner against ground truth and mute the ones that fail** — FEATURE — value 5 — effort M — risk low — category: learners
  Why: the earlier question asks which gauge is ever checked against ground truth. Each learner emits predictions (this trigger will matter, this lesson will help). Settle them against CI and steers, and mute any learner whose Brier score trails its base rate. Prior art: none found. Better by: it reuses the calibration ledger. Novelty 3.
  Done when: `fm outcomes --by learner` prints a Brier score per learner, and one below baseline is auto-muted.

- **Cap each detector at one vote per source (one input per detector)** — FIX — value 3 — effort S — risk low — category: learners
  Why: a single noisy session can teach a rule several times. Dedupe by session and by source so one event counts once. Assumption: the current learners count raw events. Prior art: none found. Novelty 2.
  Done when: replaying one session's events 10 times moves a learner's counter once.

- **Wild: add a vaccination arm to the exam** — FEATURE — value 4 — effort M — risk low — category: learners
  Why: wild. The exam plants a plausible but wrong lesson in the project memory and measures whether the agent obeys it. This extends the guard-only arm idea. Prior art: none found. Better by: it measures resistance to bad memory, not just task success. Novelty 5.
  Done when: `fm exam run --agent foreman --poison` reports the bad-lesson follow rate.

- **Wild: archive retired lessons as dormant memory cells** — FEATURE — value 3 — effort M — risk low — category: learners
  Why: wild. When a lesson is dropped for context cost, keep a compact signature. If the same failure shape reappears, re-awaken the lesson in one call (the fast second response) and note that it came from the archive. Prior art: none found. Better by: the lean ratchet stays low and nothing learned is lost. Novelty 4.
  Done when: a failure matching an archived signature reinjects its lesson within the same session.

- **Wild: hold a weekly tournament for context slots** — FEATURE — value 3 — effort M — risk med — category: learners
  Why: wild. Lessons and triggers compete for a fixed injected-chars budget. The bottom 10% are sent to shadow and the top ones may mature. Prior art: none found. Better by: the lean ratchet gets a mechanism, not just a cap. Novelty 4.
  Done when: the digest lists the week's evicted and promoted items, and total injected chars never rises.

- **Wild: autopsy a harm back to the learners that changed beforehand** — FEATURE — value 4 — effort M — risk low — category: learners
  Why: after any incident, list every learner change in the prior 7 days (lessons added, triggers demoted, thresholds moved) with the evidence for each, and flag the likeliest culprit. Prior art: none found. Better by: it makes cytokine-storm causes traceable. Novelty 4.
  Done when: `fm autopsy <incident>` prints a ranked list of learner changes with their sources.

Next question: which learner decision, if it were wrong for a month, would the user never notice, and how would we find out?
Next question: can any learned lesson be traced to one source line of the user's own words, and what happens to the lesson when the user later contradicts that line?
