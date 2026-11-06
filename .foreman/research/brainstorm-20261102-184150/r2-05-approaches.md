# Brainstorm — lens: approaches

- **Iterate the left-out list to a fixed point** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: assumption: one pass leaves a tail. Re-run the Mission on its own "Left out" list once. If that yields new briefs, the first list wasn't exhaustive. The Mission page prints "stable after N rounds". The trade-off is one extra cheap round against a measured answer to "is that everything?".
  Done when: a planted Mission whose left-out list hides one brief-worthy item reports "not stable" and files that brief; a clean fixture reports "stable after 1".

- **Pair every outcome measure with a counter-measure** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the carried gap is that Exams name an outcome measure, and the pack asks "when a measure is gameable, who finds out first". A second reading that must not move (hook p95, doctor red count, tokens injected) catches a gamed or collateral-damaging fix. This is cheaper than a blind author and works unattended.
  Done when: filing refuses an Exam with `outcome:` but no `guard:` line, and a test with a metric-gaming fix shows the guard reading moving.

- **Replace "classify any command as read-only" with a tiny query verb** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the pack's live-state reading needs safe execution. Rather than classifying arbitrary shell, give `fm q '<noun> where … | count'` over the existing ledgers. It is read-only by construction, replayable cold, and has no side-effect surface. The trade-off is that it can't read outside Foreman's own state (assumption: most live readings are ledger-shaped).
  Done when: three real past Exam readings are expressed as `fm q` lines giving identical numbers to the originals, and `fm q` writes nothing (test asserts an unchanged state dir).

- **Run a lens-jackknife on each Mission** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: "dissents scored against outcomes" needs to know which lens mattered. Re-cluster the briefs with each lens removed. A lens whose removal drops a brief is load-bearing; one that changes nothing is redundant. This costs no new model calls, only re-clustering stored ideas.
  Done when: `fm genesis mission --jackknife` prints per-lens "briefs lost if removed" for an existing Mission, and lenses with zero are flagged.

- **Seal the left-out list before building and diff it at close** — FEATURE — value 4 — effort S — risk low — category: scope
  Why: "says what it left out" is only honest if the list can't be edited after the fact. A hash-chained record is written at filing. At close, a mechanical diff shows briefs that crept in and left-out items that were quietly built. The alternative is writing the list at the end, which can be rationalised.
  Done when: closing a Mission whose built set differs from the sealed set prints both differences; a test edits the page after sealing and gets a mismatch.

- **Weight left-out cells by where the user writes by hand** — FEATURE — value 3 — effort M — risk med — category: prioritisation
  Why: assumption: the code a user edits themselves marks what they care about. Use git blame on human-authored lines per grid cell as a zero-token weight. Rank "left out" by it, so the top of the slip is what the user would notice first.
  Done when: the slip orders cells by a printed human-edit share, and a fixture repo with hand edits in one area ranks that area first.

- **Score dissents with git-only signals, no model** — FEATURE — value 4 — effort S — risk low — category: dissent
  Why: the carried gap is scoring dissents against outcomes. The cheapest approach is a pure join. A dissent names files at filing. At +14d, count reverts or FIX commits touching them, with the build's own commits excluded. A dissent scores right if the touched files were reworked, otherwise wrong. It is coarse but free and replayable.
  Done when: `fm outcomes --dissents` prints right, wrong or unobserved for each dissent in gen 3, and the join is unit-tested on a fixture history.

- **Add a single-witness flag to left-out items** — FEATURE — value 3 — effort S — risk low — category: confidence
  Why: how many lenses independently raised an item is already known after clustering. Mark items raised by exactly one lens as "fragile": likely real signal or noise, so spend a canary there first. Items raised by three or more are core. Zero extra tokens.
  Done when: each Mission-page idea carries "witnesses: n", and the canary step runs on witnesses=1 items first (asserted in a test).

- **Do less: make "Left out" a required, parsed last line of every lens child's output** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: instead of a new gauge, put the duty at the source. Each lens must end with "Left out: …" and the aggregator unions them. A missing line marks the lens as failed, not dry. The trade-off is that self-reported omissions are only as good as the lens.
  Done when: a lens fixture with no final line is reported "no left-out line" and is excluded from coverage counts.

- **Wild: turn an unattended Mission into a scored forecast of the user's next three asks** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: assumption: a left-out list is a prediction. Seal three guessed future asks at Mission close and settle them against the typed asks of the next seven days, giving the left-out slip a hit rate that can be improved.
  Done when: a Mission close writes three sealed guesses, and a later `fm outcomes` line shows hit or miss for each. (wild)

- **Wild: let a cold child "break the claim" on every Done-when by satisfying it lazily** — FEATURE — value 4 — effort M — risk med — category: adversary
  Why: the pack shows the vacuous-pass concern. A tool-less child is told to produce the cheapest diff that turns the Exam green, and a human or cold read judges whether it really did the work. It exposes gameable outcome measures before the build.
  Done when: a planted Mission with a gameable measure is caught by the child with a concrete cheap diff; a sound measure is not. (wild)

- **Wild: print "nothing left to say" only when a canary child agrees** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the claim "covered everything" is the riskiest sentence. A separate child gets only the request and the final left-out list, and must name one thing missing. If it finds one that the aggregator accepts, the claim is withdrawn. (wild)
  Done when: a Mission with a planted gap never prints "Left out: nothing", and a trivial request still can.

- **Settle each Mission's left-out slip against the user's real asks one week later** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: the pack's earlier blind spots (T-2691 to T-2738) were all asks no idea predicted. Matching later typed asks to slip lines gives a recall number per Mission and an input to which axes to widen.
  Done when: `fm outcomes --leftout` prints per-Mission slip recall computed from the asks ledger, with a fixture of one hit and one miss.

Next question: which gen-3 Exam readings would still return the same number if run in a fresh shell by a cold process, and how many depend on session state?
Next question: does the user read the left-out slip at all, and would an unread slip be better replaced by one question asked at filing?
