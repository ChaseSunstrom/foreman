# Brainstorm — lens: user value

- **Dry-run every brief's detector on the real state before building** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: two steered results show a brief resting on a claim that failed against live data. The asks/depends_on grouping "found nothing" on the real pile of 44 blocked tasks, and the first M-02 output was only a tail.
  Done when: filing a brief whose detector is a reader or finder prints its hit count on the live state, and a zero count blocks filing unless the brief states why zero is expected.

- **Auto-ship a green batch under the standing push grant** — FEATURE — value 4 — effort M — risk med — category: shipping
  Why: about 7 of the user's last 20 asks are "Ship N commits to main", and their steer says to push to main without asking. assumption: the grant can be spent on a batch without a per-task publish grant.
  Done when: with 3 or more unshipped commits, a green suite and an idle queue, one tick runs `fm ship` and the next `fm next` shows "shipped N commits, main matches local" with no typed ask.

- **Split user-held steps out of a Done-when at filing** — FIX — value 4 — effort S — risk low — category: briefs
  Why: a drop reads "criterion 3 bundled the user-held deletion (T-2702) and can't be edited after a failing run". One unsatisfiable criterion killed an otherwise good brief.
  Done when: `fm task new` with a criterion that needs a user-only action (delete, approve, hardware) files it as a separate "user-held" line, and the agent-side criteria can pass without it.

- **Skip review findings that review.md already marks as gap or by-design** — FIX — value 3 — effort S — risk low — category: noise
  Why: three of five recent drops are cross-cutting review FIX items (#23, #24, #25), dropped because review.md marked them "gap" or "by design". Foreman filed work it had already judged.
  Done when: the review-to-task filer reads the review's own status and files nothing for a gap or by-design row, and a test plants one of each.

- **Keep the full output of any run cited as evidence** — CLEAN — value 3 — effort S — risk low — category: evidence
  Why: the recorded M-02 output was only its 301-byte tail, so the user had it rerun with a second approach.
  Done when: `fm` stores a kill or exam script's whole stdout beside its result, and a test fails if a cited result file is shorter than its run's output.

- **Offer the width of an exhaustive pass with its price at intake** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the request is "cover the whole space", but a full pass costs reading time and tokens, and nothing lets the user choose how far to go. assumption: widths narrow, standard and full; the default is learned from the user's picks.
  Done when: the intake prints three widths with an estimated cost and review minutes, the pick is recorded on the task, and the next intake defaults to it.

- **Show the other readings only when two cold readers disagree** — FEATURE — value 3 — effort M — risk low — category: ambiguity
  Why: the user's need is a stated intent met exactly (the "gen-0 §3 contradiction" and "comma vs space" fixes were misreadings found late). A silent pass costs nothing, while a split between readers is the signal worth interrupting for.
  Done when: filing a brief runs two blind interpretations of its Done-when, and a split prints both readings with a choose-one command while agreement prints nothing.

- **Close each Mission with its own use counts for the previous Mission's capabilities** — FEATURE — value 3 — effort S — risk low — category: outcomes
  Why: Mission 7 was asked to "report Mission 6's two use counts", which suggests the user wants proof that built capabilities get used. assumption: Missions currently report these only when asked.
  Done when: every Mission file opens with a line per capability from the previous Mission, giving its session-path call count in the last 14 days or "0 — unused".

- **Give every Mission page a five-line plain twin that a cold child can act on** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: the user's follow-ups are mostly small contradictions between pages (seed vs gen-0, printed command vs parser). Short text that is actually used exposes them sooner.
  Done when: a tool-less child given only the twin names the first command to run, and a Mission whose twin fails this check isn't marked filed.

- **Dedupe a finish-time followup against the commit that caused it** — CLEAN — value 2 — effort S — risk low — category: queue
  Why: T-2691/2693 and T-2720/2722/2724 are fixes to the previous task's output. assumption: they could have been caught by one pass over the task's own printed lines at finish.
  Done when: `fm task finish` re-runs each command and path it printed against the parser, and the next task's fix tasks of that class drop in a 30-day count.

- **Wild: Seal a drop-rate forecast on every Mission and score it** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild; the user drops a steady share of Foreman-filed items, so a forecast of that share per Mission would show whether Foreman knows its own hit rate.
  Done when: the Mission file carries "expect N of M briefs dropped" before intake, and at close the actual count and the error print beside it.

- **Wild: Hold each lens to a refund when its brief is dropped** — FEATURE — value 3 — effort M — risk low — category: accountability
  Why: wild; a dropped brief costs the user reading time, and nothing yet charges that cost to the lens that proposed it.
  Done when: a lens's budget in the next Mission shrinks by its drop count, and the lens table in the pack shows kept vs dropped per lens.

- **Wild: Add a one-keystroke grade at the next session start** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: wild; there's no cheap channel for "the last Mission was fine / meh / wrong" besides typing a new ask. assumption: a single y/n/meh at session start feeds the lens weights.
  Done when: session start shows one line asking for the grade of the last closed Mission, and a keypress stores it where `fm outcomes` can read it.

Next question: which closed tasks in the last 30 days were fixes to the output of the task just before them, and what one check at finish would have caught each?
Next question: how many of the user's typed asks are "ship" or "continue" style, and can they be removed by a standing grant without widening what is pushed?
