# Brainstorm — lens: reliability

- **File a Mission's briefs as one transaction** — FIX — value 4 — effort M — risk low — category: atomicity
  Why: assumption: a Mission files the page plus N briefs as separate writes. A kill, usage-limit wait or compaction partway leaves a page that says "N briefs" with fewer tasks behind it. The steers require resuming where it stopped.
  Done when: killing the filer after brief 2 of 5 leaves either nothing or a `pending` marker, and a re-run files only the missing 3 with no duplicates.

- **Replay every open brief's Exam in a hermetic cold shell** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: it answers the carried question "which Exam measures are re-runnable by a cold process". `fm exam replay --cold` runs each Exam in a fresh HOME, scrubbed env, empty state dir and clean checkout. It prints the re-runnable fraction and names the hidden input behind each failure. Nothing in the pack says this has been run.
  Done when: the command lists every open brief as re-runnable, session-dependent (with the dependency named) or unrunnable, and a planted brief that reads `$FM_SESSION_ID` lands in the second group.

- **Plant a positive control beside every "not built" search** — FIX — value 4 — effort S — risk low — category: canary
  Why: a grep over a stale map ("2176 files, as of an older HEAD") or a wrong scope returns zero for a feature that exists. Canaries sit near the idea but nothing proves the search could find anything. Before a "not built" claim, search the same file set for a term known to be present; if that misses, the claim becomes "search unreliable".
  Done when: with the search index pointed at an empty directory, the claim prints "search unreliable" instead of "not built".

- **Make Exam readings emit one typed line** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the gen-4 carried gap asks every Exam to name an outcome measure and a live-state reading. Free-text readings drift in format and can be satisfied by an echo. A single JSON line `{value, unit, n, as_of}` makes dissent scoring computable and lets malformed output count as "could not run".
  Done when: a reading that prints prose is rejected at filing, and a typed one is read back by the dissent scorer without parsing prose.

- **Seal each dissent before its outcome exists** — SECURITY — value 3 — effort S — risk low — category: scoring integrity
  Why: dissent scoring against outcomes is only credible if the dissent can't be reworded afterwards. Hash-chain it at write time with the lens, model and claimed measure.
  Done when: editing a dissent after its task closes makes `fm verify-ledger` fail naming that record.

- **Drill a Mission with a planted dead lens** — FIX — value 4 — effort M — risk low — category: fault drill
  Why: "exhaustive" is the claim, and a lens child that crashes, times out or returns garbage silently shrinks it. Kill or corrupt one lens in a scratch Mission and require the left-out receipt to name it as failed, not dry.
  Done when: the drill's receipt lists the killed lens under "failed" and the Mission page does not say "covered".

- **Assert sweep idempotence** — FIX — value 4 — effort S — risk low — category: tower
  Why: the tower advances itself and a red sweep files its own fix tasks. A second `fm genesis sweep` with no change in between should file nothing and print the same result. Today only refile livelock detection is on the slate, which is a different check.
  Done when: two consecutive sweeps on a fixture tower produce byte-identical output and zero new tasks.

- **Fuzz hand-edited Mission files** — FIX — value 3 — effort S — risk low — category: parsing
  Why: Mission pages and briefs are markdown the user edits by hand. A stray tab, CRLF or reordered heading shouldn't turn into a silently skipped brief.
  Done when: a corpus of 20 perturbed Mission files either parses to the same brief set or fails with a line-numbered error, never a short list.

- **Measure grid reproducibility across reruns** — FEATURE — value 3 — effort M — risk low — category: stability
  Why: assumption: the same request run twice yields different cell sets. Take the overlap of the two runs; low overlap means the grid is a sample, not coverage, and the Mission page should say so.
  Done when: the page shows a stability figure for the grid, and a deliberately halved pack produces a visibly lower figure.

- **(wild) Quiz the builder on the steers after compaction** — FEATURE — value 3 — effort M — risk med — category: context loss
  Why: wild. Long Missions get summarised, and the steers (cold reads, the no-block rule, the push grant path) are exactly what a summary drops. After a compaction, a tool-less child asks the builder five questions about the standing rules and logs any it gets wrong.
  Done when: a session whose summary omitted the "never block on the user" rule fails the quiz and the miss is recorded.

- **(wild) Hold a nightly saboteur run on the exam harness** — FEATURE — value 4 — effort L — risk med — category: measurement
  Why: wild. A child that sees only the Exam text, not the fix, tries to make the reading pass by shortcut: editing the output, changing the baseline, narrowing the scope. Each success is a gameable-measure finding filed against the brief.
  Done when: one planted weak Exam (`grep -c . file`) is defeated within a run and filed as a finding.

- **(wild) Write a "what I'd have to trust" page for each Mission** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. List every reading the Mission's pass depends on that Foreman wrote, ran and judged itself, none by an outside signal. It's the Mission's single-point-of-failure map, ranked by how much of the verdict rests on each.
  Done when: the page lists at least one self-authored reading per brief, and a brief with an outside signal is marked as such.

Next question: which readings in open briefs depend on state that exists only inside a live session, and what share of gen-3's closed Exams could be re-run today?
Next question: when the cold read, the sweep and the Mission builder disagree, which one is the tiebreaker, and where is that written down?
