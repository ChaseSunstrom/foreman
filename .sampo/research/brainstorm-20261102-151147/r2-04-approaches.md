# Brainstorm — lens: approaches

- **Select from the catalogue, don't generate** — FEATURE — value 4 — effort S — risk low — category: thinking
  Why: the 525-idea catalogue, the 30+ deferred "Later from" tasks and a pack with thousands of ideas already exist, and the recent drops were mostly "already built" or "value 2 after re-grounding". That makes exhaustiveness a selection problem, not a generation problem. This is the do-less approach: reuse the existing catalogue and add no new brainstorm.
  Done when: `fm ideas --select` run over the catalogue with zero model calls prints the top 10, each with its evidence field and its "grounded at" commit, and Mission 6's briefs can be filed from that list alone.

- **Add a "Called by:" line to every idea** — FEATURE — value 4 — effort S — risk low — category: reach
  Why: the standing rule says every capability must be called by a real session path. The brainstorm output format has no field for it, so unreachable ideas only get caught later by `fm genesis check`'s reach test.
  Done when: a slate item without a `Called by:` line naming a session start, `fm next`, the drive, a skill or a hook is rejected at intake, and a test feeds it one such item.

- **Keep a refuted-assumption bank** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the format already makes brainstormers mark assumptions. The drops show the same wrong assumptions resurfacing (`fm replay`, `fm usage --prune` and `check_predictions` were each "mostly built"). Resolve each marked assumption mechanically with grep and the verb help strings, and record refuted ones as "known false: X exists at file:line". Show that list to the next round.
  Done when: after a round, a "Known false" section in the next pack lists at least the assumptions refuted by grep. A second-round brainstorm shows no idea contradicting one of them, checked by a fixture pack with a planted refuted assumption.

- **Re-ground catalogue entries when their files change** — FIX — value 3 — effort M — risk low — category: staleness
  Why: the map in this pack is "as of an older HEAD", and ideas were dropped as already built only after the user's time was spent. Store the file hashes each catalogue idea was grounded against, and flag the idea for re-grounding when those files move.
  Done when: editing a file cited by a catalogue entry makes `fm ideas --stale` list that entry, and a test proves an entry whose files did not change is not listed.

- **Backtest recall on foreign repos' later issues** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: standing rules require signals Foreman didn't author and exam scenarios from a tool-less child. Take a foreign repo at a past commit, run the brainstorm, and score how many of the issues and commits that followed it predicted. The ground truth is real and free. This gives "exhaustive" a number instead of a feeling.
  Done when: `fm exam ideas` reports recall per lens on at least 5 foreign repos, with a zero-token arm (a random-title baseline) printed beside it.

- **Union two model families and rank by single-finder novelty** — FEATURE — value 3 — effort M — risk med — category: diversity
  Why: assumption: one family's blind spots repeat across all lenses, and the huge "ideas so far" list shows heavy clustering (hundreds of immune-system variants). Run each lens on two families. An idea only one family found is probably novel, and one both found is probably obvious.
  Done when: a slate prints a `found-by` count per idea, and a test with two stub families produces the expected novelty ordering.

- **Collapse the catalogue into a subsumption tree** — CLEAN — value 3 — effort M — risk low — category: dedupe
  Why: many listed items are special cases of others ("Prove the zero-config install is safe" vs "Safe-by-default install profile"; the many "unproven" receipt-state variants). Fold specific ideas under their parent and use the child count as a demand signal, so a slate shows 40 parents instead of 500 leaves.
  Done when: `fm ideas --tree` shows each parent with its child count, and the pack's "ideas so far" section shrinks by at least 60% with no parent title lost.

- **Shuffle pack section order to measure position bias** — PERFORMANCE — value 2 — effort S — risk low — category: measurement
  Why: assumption: brainstormers lean on whatever the pack puts first or last. Run the same lens twice with the sections reordered. If the overlap is below a threshold, the lens is following the pack layout rather than the evidence.
  Done when: `fm ideas --order-probe` prints an overlap percentage per lens across 2 orderings, and a stub child that echoes the first section scores 0%.

- **Mask the verbs and let a child reinvent them** (wild) — FEATURE — value 3 — effort S — risk low — category: gaps
  Why: wild. Give a tool-less child the verb table with 20% of the verbs hidden and ask it to list what's missing. Verbs it reinvents show the surface is guessable. Verbs it proposes that don't exist are gap ideas grounded in the surface's own shape. It's cheap and needs no pack.
  Done when: a run on the real verb table prints a "guessable" rate and a list of proposed verbs, each marked "absent" or "present" by a lookup, and a planted fake verb is reported absent.

- **Test for genericity: strip the project name** (wild) — CLEAN — value 3 — effort S — risk low — category: filler
  Why: wild. Many listed ideas share a template ("Run a ... drill", "Wild: Plant canary ..."), and the standing rule rejects templated cells. Remove Foreman-specific nouns from an idea and ask a cold child to name the project. If it can't, the idea is filler and is dropped.
  Done when: running the probe on 30 catalogue ideas flags a set of generic ones, and a known-specific idea (for example one naming `fmguard.check`) is never flagged.

- **Incubate every new idea for seven days** (wild) — FEATURE — value 2 — effort M — risk med — category: filtering
  Why: wild. An idea does not enter the queue until a different lens, a different family or one of the user's later words independently matches it. Unmatched ideas expire quietly into the catalogue. This uses time as the filter, since the real intake cost is the user's attention (see the drops).
  Done when: a new idea shows "incubating, day N" in `fm ideas`, is promoted when a planted matching second source appears, and expires at day 7 otherwise, tested on a fake clock.

- **Run the same brainstorm blind, then subtract the catalogue mechanically** — PERFORMANCE — value 3 — effort M — risk low — category: tokens
  Why: this pack carries thousands of lines of "ideas so far", which costs tokens and may anchor lenses on the same phrases. Generate with no list, then remove duplicates and already-built items mechanically afterward.
  Done when: on 3 lenses, pack size drops by at least 70% while the count of ideas surviving grounding is no lower than with the list.

Next question: which of the ideas filed in the last three generations did the user actually use within two weeks, and what do those have in common that the dropped ones lack?
Next question: when two brainstorm rounds converge on the same cluster, is that exhaustion or a shared blind spot, and what signal separates them?
