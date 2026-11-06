# Brainstorm — lens: tower archaeology

- **Resume by replaying the questions past resumers asked** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: assumption: the earlier ideas fix the reading path by design (RESUME.md, tiers), but nothing learns it. Log which tower files a resuming session opens first and what it greps for before acting, then promote those answers to the top of the tower.
  Done when: after 3 logged resumes, `fm genesis status` front matter lists the 5 most-asked questions, each linked to its answer file, and a test shows the order changed.

- **Give every decision a "reopen if" trigger** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: pack evidence: the dropped items carry reasons ("already fixed in ee98a137"), and those reasons go stale. A rewrite that lost, or a spike parked in not-yet, says why. It doesn't say what would change the verdict (a new model, an exam that grew, a blocker gone). Store a machine-checkable trigger and evaluate it on open.
  Done when: a fixture decision with trigger "exam scenarios > 12" is flagged "reopen" on open once the exam grows to 13, and stays quiet at 12.

- **Reproduce a historical result in a pinned worktree** — FEATURE — value 4 — effort L — risk med — category: reproducibility
  Why: assumption: claims like "gen-2 closed 7 of 9" are narrated, and the project has moved since. `fm genesis reproduce gen-2 [scenario]` checks out the recorded commit, the exam seed and the arm config, re-runs, and reports match or drift.
  Done when: on a fixture tower the command reproduces a recorded score. After a doctored score entry it prints the mismatch with both numbers.

- **Chain the generations by hash so history can't be quietly rewritten** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: assumption: archaeology only works if past generations are trusted. Each close record carries the hash of the previous close plus its own files. A hand edit to a past doc then shows as "amended after close", and the user's edit is logged as a steer rather than blocked.
  Done when: editing a closed generation's doc makes `fm genesis status` print "gen-1 amended after close" with the file, and an unedited tower passes verification.

- **Compact old generations with a verified round trip** — PERFORMANCE — value 4 — effort M — risk med — category: scale
  Why: assumption: by gen 5 a stranger can't read everything, and tiered reading only orders the files. Fold old generations into a strata summary, keep the originals addressable by hash, and accept the summary only if a tool-less reader answers 5 sampled questions the same from the summary as from the full text.
  Done when: a 5-generation fixture compacts to under 30% of its size, and the round-trip check fails on a summary with a deliberately dropped decision.

- **Keep a ledger of what was considered but never run** — FEATURE — value 3 — effort S — risk low — category: negative space
  Why: the not-yet ledger covers attempted-and-blocked work, and dead rewrites cover tried-and-lost. Options dismissed in a brainstorm or critique (cost, ambition, "later") appear in neither, so a new session re-proposes them. Record each with its reason and source line.
  Done when: a mission that matches an entry in the untried ledger is shown the original reason before spending anything.

- **Lint tower citations and follow renames** — CLEAN — value 3 — effort M — risk low — category: integrity
  Why: assumption: tower docs cite code paths, mission files and scenario ids. Renames and pruned files leave dangling references, and churn-decay alone says "stale" without fixing it. Resolve citations through git rename detection and flag the ones that can't be resolved.
  Done when: renaming a cited file in a fixture makes the lint rewrite the citation, and deleting one makes it list the citation as dangling.

- **Build a tower glossary of coined terms** — CLEAN — value 2 — effort S — risk low — category: legibility
  Why: pack evidence: the steers use "mission 8 overload", "held-out third", "gap map #13", "tier 3". A cold session meets these without the chat that defined them. Extract each term's first definition and generation into one file the resume path links.
  Done when: every term in a fixture tower's docs that isn't common English resolves to a glossary entry, and the lint fails on an undefined one.

- **Anchor human marginalia to tower lines** — FEATURE — value 3 — effort M — risk low — category: user notes
  Why: assumption: the user's steers are captured verbatim, but a note like "rejected this because it felt gimmicky" is tied to one doc line and is lost when the doc regenerates. Store the note against a content anchor, re-attach it on regeneration, and surface it on resume and on the site page.
  Done when: a note on a line survives a regeneration that moves the line, and a deleted line leaves the note listed as orphaned.

- **Attach raw evidence to each verdict, not prose** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: assumption: a "why it lost" card is only as honest as its author. Store a capped, hashed excerpt of the actual failing exam output and the scores next to every verdict, so a later reader can check the claim.
  Done when: each lost rewrite's card links to an evidence file whose hash matches, and the card lints as incomplete without one.

- **Wild: Run `fm genesis whodunit "scenario 4 regressed"`** — FEATURE — value 3 — effort L — risk med — category: forensics
  Why: wild. Bisect across generations automatically. Check out each generation's project commit and tower state, re-run the scenario, and name the generation and rewrite where it first flipped, then ask a tool-less child to explain it from the diff.
  Done when: on a fixture tower with a planted regression the command names the right generation and prints the diff that caused it.

- **Wild: Hold a cold-resume drill with a stranger session** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: wild. Once per generation close, spawn a tool-less child with only the tower files. Have it state the next step and the three riskiest open items. Grade it against the orchestrator's own answer and write the disagreement into the front of RESUME.md as "unclear to a newcomer".
  Done when: a fixture tower with an ambiguous next step produces a drill disagreement, and a clear one produces none.

- **Wild: Mark the dig site with a "do not rediscover" sign** — FEATURE — value 2 — effort S — risk low — category: legibility
  Why: wild. The tower page plots dead ends, untried ideas and reopen triggers as a map of the ground already covered, with the frontier edge highlighted. The user sees at a glance where Genesis hasn't been.
  Done when: the exported page renders the three layers from a fixture, and a click on the frontier shows the next suggested mission.

Next question: What does a resuming session do when the tower contradicts the user's newest steer in chat, and where is that precedence written down?
Next question: Which tower files does nothing read after they are written, and would anyone notice if they vanished?
