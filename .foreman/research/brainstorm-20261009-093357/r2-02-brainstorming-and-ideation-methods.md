# Brainstorm — lens: brainstorming and ideation methods

- **Seed ideation with a constraint-inversion deck** — FEATURE — value 4 — effort M — risk low — category: ideation
  Why: the pack's brainstorm lens set (unspoken needs, delight, capability map…) is fixed; ideas already listed include "oblique constraints" and "reframing", but nothing generates *task-specific* inversions. Assumption: SCAMPER-style prompts (substitute, eliminate, reverse, combine) applied to the brief's own nouns produce options the lenses miss.
  Done when: `fm ideas --invert <task>` emits ≥5 ideas each tagged with the inversion operator used, and a test shows at least one differs from all lens-round outputs on a fixture brief.

- **Add a user-pull score from kept/dropped history** — FEATURE — value 5 — effort M — risk low — category: ideation feedback
  Why: "The user's own words" shows ~17 ideas asked (captured as C0xx tasks) and several dropped/steered ones; the pack lists 800+ ideas but no loop where which ideas were chosen retunes ranking. Assumption: captured-then-asked is a reliable keep signal.
  Done when: `fm ideas --rank` orders a fixture idea set by similarity to previously kept vs dropped ideas, and the top-3 changes when the kept set changes.

- **Cluster ideas into duplicates before showing them** — CLEAN — value 5 — effort S — risk low — category: dedupe
  Why: the "Ideas so far" list contains many near-duplicates (e.g. "Dream mode", "Dream overnight on old failures", "Dream at night over the day's work"; three variants of canary releases; three of lane-across-machines). The user has to read all of it. Assumption: BM25/shingle similarity over titles is enough for a first pass.
  Done when: running dedupe on the pack's list yields clusters with one canonical title each, and the three "dream" and three "across machines" variants land in the same cluster.

- **Run a blind-then-informed two-phase round** — FEATURE — value 4 — effort M — risk low — category: ideation process
  Why: round 2 children see the long prior list, which anchors them to it (this prompt included: the "don't repeat" list is ~900 lines). Assumption: independence of the first pass raises novelty; "blind first round" exists as an idea but isn't built.
  Done when: `fm ideas` runs a lens once with no prior list, then once with it, and reports how many first-pass ideas the second pass would have missed.

- **Measure idea novelty against the corpus with an embedding-free score** — FEATURE — value 3 — effort S — risk low — category: ideation quality
  Why: "stop when novelty saturates" is listed as an idea but a cheap metric (max token-overlap with all prior titles) is the precondition. Round 2 here is plainly saturating.
  Done when: each returned idea carries a novelty number, and ideas above a threshold are auto-flagged "restatement" in output.

- **Convert the idea pile into a coverage map by capability axis** — FEATURE — value 4 — effort M — risk low — category: roadmap
  Why: "Distil the idea pile into a ranked epic roadmap" exists; a coverage matrix (axis × existing idea count) would show the thin axes (e.g. only a few ideas on non-code deliverables, accessibility, onboarding) instead of what is oversupplied (guard, lanes, ledger). Assumption: axes can be derived from the command tree and MASTER.md headings.
  Done when: a report lists each axis with idea count and flags axes with <3 ideas, on the current pack.

- **Add a "kill it fast" triage pass that tries to falsify each idea in one line** — FEATURE — value 4 — effort S — risk low — category: ideation
  Why: ~900 ideas exist and the user said "I like almost all of those", meaning filtering has been weak; the real cost now is selection. Assumption: a cheap Haiku pass naming the single strongest objection per idea prunes the pile.
  Done when: each idea shown has a "strongest objection" line and a cheap-to-test flag, and an idea with a fatal objection is hidden by default.

- **Cache brainstorm answers per lens so reruns only pay for new angles** — PERFORMANCE — value 2 — effort S — risk low — category: ideation cost
  Why: each round re-sends the whole prior-ideas list to every lens. Assumption: token cost is meaningful across 10+ lenses.
  Done when: a rerun with unchanged pack makes zero child calls and prints the cached result.

- **Wild: Run an "ideas that would embarrass us" lens** — FEATURE — value 3 — effort S — risk low — category: ideation (wild)
  Why: assumption: ideas generated from "what would a critic post about Foreman on a forum" surface honest gaps (complexity, 267 files, ~25 verbs wanted) that constructive lenses skip.
  Done when: the lens produces ≥5 critique-framed ideas, each convertible to a captured task.

- **Wild: Hold an idea-market where prior brainstorm rounds are scored by the user's later keeps** — FEATURE — value 3 — effort M — risk low — category: ideation (wild)
  Why: assumption: if lenses were credited when their ideas got built (T-0439..T-0455 came from "C0xx" ids), the budget per lens could shift automatically; ties to "Tune lens budgets" but adds a visible leaderboard.
  Done when: `fm ideas --lenses` prints each lens with kept/total ratio from captured tasks.

- **Wild: Brainstorm backwards from the user's next complaint** — FEATURE — value 4 — effort M — risk med — category: ideation (wild)
  Why: the steers ("cleanup never got done", "shouldn't block until 75%") are complaints that arrived after the fact. Assumption: a lens that writes the three most likely next complaints from the friction log, then asks what feature would pre-empt each, catches things before they hurt.
  Done when: the lens outputs complaints with a matching friction-log evidence line each, and at least one maps to an open T-id.

- **Wild: Let ideas mate by incompatibility** — FEATURE — value 3 — effort M — risk med — category: ideation (wild)
  Why: existing "cross-breed top ideas" combines compatible ideas; deliberately pairing two *contradictory* ones (e.g. "fewer verbs" vs "add extension SDK") forces a resolution design. Assumption: tension pairs yield sharper designs.
  Done when: the tool picks N conflicting pairs from the list and emits a synthesis that satisfies both on a stated criterion.

- **Tag each idea with its originating need so repeats collapse into needs** — CLEAN — value 4 — effort S — risk low — category: ideation structure
  Why: the pile repeats a handful of needs (trust "done", lower cost, fewer interruptions, safer unattended runs). Assumption: grouping by need makes round selection a ~10-item decision instead of ~900.
  Done when: every idea in a run has a need tag from a fixed list of ≤12, and output groups by tag.
