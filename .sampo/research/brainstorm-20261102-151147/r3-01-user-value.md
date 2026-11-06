# Brainstorm — lens: user value

These ideas go past the list, but the list is thick enough that some overlap with earlier ideas remains. Three come from defects visible in this pack.

- **Reject fragment lines as idea titles** — FIX — value 3 — effort S — risk low — category: pack hygiene
  Why: "Ideas so far" contains parser debris: "Ideas 1–4", "Most ignored trigger:", "Subtraction (T-2534/35/36):", "T-2533:". These bodiless headers take slots from real ideas and make the pack look more saturated than it is.
  Done when: a test feeds the pack builder those exact lines and none appear in the digest. Planted real titles still pass.

- **Truncate pack lines at word boundaries** — FIX — value 2 — effort S — risk low — category: pack hygiene
  Why: Open work lines are cut mid-word ("the don", "clus", "…with"), and the missed-ask list cuts mid-sentence. A cold child can't judge the cut-off briefs.
  Done when: no pack line ends mid-word, and an over-length line ends in "…" after a whole word.

- **Print a pack integrity line** — FEATURE — value 3 — effort S — risk low — category: pack hygiene
  Why: Stale map HEAD, truncated lines and rejected fragments are invisible today. Brainstormers can't discount a pack they can't see is degraded. This is the combined form of the two fixes above.
  Done when: the pack's first lines state the idea count parsed, fragments rejected, lines truncated and map age in commits, and a test with a planted stale map shows a nonzero age.

- **Rank the slate by days until the user first feels it** — FEATURE — value 4 — effort S — risk low — category: triage
  Why: Slates are ranked by value and effort, but the user's repeated "already built" and "value 2 after re-grounding" drops show that value on paper isn't value felt. The new key is the first day a user-visible surface changes (next session start, next `fm next`, next release).
  Done when: each slate line carries "felt: session N / week / never-visible", and a slate sorts on it with ties broken by value.

- **Assemble the one-card finish receipt from fields that already exist** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: separate ideas cover proven/unproven/overridden states, spend, "held back", lean delta and "you said / built / not proven". None assembles them. This is the do-less version: no new data, one renderer.
  Done when: `fm task finish` prints one card of at most 12 lines that reads only existing ledger fields. A test fails if the card ever needs a new field.

- **Slice every L task into a tracer that is useful alone** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: T-0034, T-0035 and T-1207 sit deferred or blocked as L tasks. The spike idea measures their effort, not their smallest shippable value. The tracer is the thinnest end-to-end path the user would keep even if the rest never ships.
  Done when: `fm plan --tracer T-0034` files an S task with its own Done-when and the claim "useful without the rest", and a cold read can state that benefit from the task alone.

- **Keep a topic embargo list the pack always injects** — FEATURE — value 3 — effort S — risk low — category: steering
  Why: guard, proof, tick and immune-system ideas number in the hundreds. The user has to drop or re-ground them one by one. A single user-owned list ("no new guard ideas until X") is the cheap stop.
  Done when: an embargoed cluster is stated in the pack's fence section, and a brainstorm run with a planted embargo returns zero ideas in that cluster, or ones that explicitly cite new evidence.

- **Add `fm quiet 4h`, a tired-mode that mutes everything except blocking items** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: assumption: the user's long runs and their "never block on the user" rule mean notes, Next: lines and nudges all compete for attention. A timed global dial is cheaper than tuning each emitter.
  Done when: during quiet, hook notes and receipts print at most one line each, a guard block or `fm ask` still prints in full, and quiet expires on its own.

- **Try the system-level proof on the user's own host: `fm host prove`** — FEATURE — value 3 — effort M — risk med — category: ops proof
  Why: assumption: the user runs a hardened Arch kernel and has host-level blockers (T-0325 needs `sudo pacman`). A before/after snapshot of failed units, boot time and package list around an update brings the discipline to the machine itself.
  Done when: running it around a dry package change prints a delta of failed units and packages, and a planted failing unit shows up as red.

- **Wild: resurface one old deferred idea each morning with today's evidence** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. More than 30 "Later from" deferrals rot unseen. A single daily card, "still true? yes / later / never", turns the graveyard into a slow trickle and records the answer as the wake condition.
  Done when: the session start shows one deferred item with a fresh grep or ledger fact attached, and a "never" answer closes it with the reason recorded.

- **Wild: let a dormant-idea garden stand in for the idea list** — CLEAN — value 3 — effort M — risk med — category: brainstorm cost
  Why: wild. Ideas untouched for 90 days with no new evidence compost into a 20-line seed packet. A lens may "sprout" one only by citing a fact newer than the packet, and the full list stays on disk as the dedupe index.
  Done when: the pack size drops by more than 80% with the same dedupe hit rate on a replay of the last 30 filed ideas.

- **Wild: stage a felt-change bet at each Mission open and settle it at close** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild. Each Mission states one sentence, "by Friday you'll notice X", and the close asks one yes/no. This turns the ranking key from the "felt" idea above into a score for how well the tower predicts the user's experience.
  Done when: the Mission file carries the sentence, the close records the answer, and the weekly line shows the hit rate with its denominator.

Next question: which of the roughly 3,000 prior ideas has the user actually felt in daily use? Without that, value scores are all guesses.
Next question: what blocks T-1207, T-1331 and T-1344, and is it the same unmet precondition for all three?
