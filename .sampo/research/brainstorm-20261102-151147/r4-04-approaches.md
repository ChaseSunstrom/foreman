# Brainstorm — lens: approaches

- **Gate each brief with a tiered claim resolver** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: T-2659 and the Mission 6 request both rely on "spot checks on each claim", and 3 of 4 slate items failed grounding. Spot checks by a model are the expensive path. Type each claim as existence, absence, number or behaviour. Tier 1 resolves it with grep, `fm help` or file reads for zero tokens. Tier 2 sends only the leftovers to a tool-enabled child. Tier 3 lists what's left for the user. Trade-off: the claim extractor can miss claims, so it only reports coverage and never claims completeness.
  Done when: a fixture brief with five typed claims, three of them false, resolves 3/5 at tier 1 with zero model calls, and `fm intake` refuses the brief while naming the false ones.

- **Run a grep canary before accepting any "not found"** — FIX — value 4 — effort S — risk low — category: grounding
  Why: the dropped items include "mostly built" claims that earlier searches missed, and absence claims are the riskiest class. Before an absence claim is accepted, run the same search shape and scope on a symbol known to exist. If the canary isn't found, the search can't see that area and the claim is marked unproven.
  Done when: a test searches a path outside the scope for a planted symbol, the canary misses, and the absence claim is rejected as unproven.

- **Verify every "Why:" quote against the pack** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: the ideas cite "evidence from the pack", and nothing checks that the cited text exists. A zero-token matcher finds the quoted fragment in the pack and re-labels any idea whose quote isn't there as "assumption".
  Done when: a slate with one invented quote prints that idea with an `assumption` tag and exits nonzero under `--strict`.

- **Score pack-ablation stability** — FEATURE — value 3 — effort M — risk med — category: robustness
  Why: assumption: an idea that depends on one pack fragment is fragile, and the user's steers already distrust Foreman-authored signal. Re-run a lens with random pack sections removed, keep ideas that recur in at least 3 of 5 ablated runs, and flag the rest as single-source. Costs 5× the tokens, so run it on only the top slate items.
  Done when: on a fixture pack, an idea that rests on one planted fragment is flagged single-source and a multi-evidence idea is not.

- **Add a "boring" lens** — FEATURE — value 3 — effort S — risk low — category: lenses
  Why: the lens set favours "whole capabilities" and wild ideas, so the unglamorous gaps get skipped. The user's pushback pattern (the 24 queued asks were mostly S/M hardening items) shows they value those. The lens asks only for what a competent maintainer would call obviously missing, such as an exit code, a missing test or an unhandled input.
  Done when: the lens exists in the lens table and a run on the fixture pack returns at least three S-effort items, each with a file path.

- **Mine reverts and deleted files as retired-idea seeds** — FEATURE — value 3 — effort M — risk low — category: history
  Why: the pack's "dropped" list is only the current round. `git log --diff-filter=D` and revert commits hold ideas that were tried and removed, with reasons in the message. Feed those in as "tried before, reason: …" so lenses neither repeat nor miss a changed blocker, as standing steer 1 asks for ("failed spike … goes to not-yet.md").
  Done when: `fm ideas --seeds-history` lists at least the last 20 reverted or deleted items with commit ids and reasons on this repo.

- **Keep an idea funnel ledger with typed drop reasons** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack mentions 525 ideas, 8 missed asks and many drops, but no single number shows where ideas die. Record each stage (generated, deduped, grounded, filed, built, used) with a drop reason from a closed list (duplicate, already built, wrong premise, low value). It turns "we keep missing X" into a measurable stage.
  Done when: `fm ideas funnel` prints counts per stage and per drop reason for the last Mission, and the counts sum to the number of ideas generated.

- **Add a grounding dial scaled by value** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: doing less is an option, since grounding every idea costs a lot and only filed briefs get built. Ground fully only ideas of value 4 or more, run tier-1 checks on value 3, and file value 2 or less to the catalogue as `unchecked`. The cost is that a low-value duplicate gets through.
  Done when: a mixed-value slate shows per-tier check counts and the value-2 items carry an `unchecked` label in the catalogue.

- **Audit unslated work at each Mission close** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: the blind-spot section lists asks no brainstorm predicted, but never the reverse: work that landed without being on any slate. A cold child reads the Mission diff and the slate and lists the diff's capabilities that no idea named. Those show which lens was missing.
  Done when: the close prints "N shipped items matched no slate idea", with titles, for the most recent Mission.

- **Pick the final slate by diversity, with a greedy selector (MMR)** — PERFORMANCE — value 2 — effort S — risk low — category: selection
  Why: "Ideas so far" has the same themes repeated dozens of times (guard, proof, tick). A zero-token greedy pick by title-token overlap penalty keeps the best-scored idea from each cluster.
  Done when: on a planted slate where 8 of 12 ideas are near-duplicates, the selector keeps at most 2 of them.

- **Run a blind-reinvention probe on the verb table (wild)** — FEATURE — value 3 — effort M — risk med — category: dedupe
  Why: wild; assumption: "already built" misses are frequent because titles don't match verb names. Give a tool-less child only an idea title and `fm help` output, and ask which verb already does it. If it names one, the idea needs a dedupe note before it is filed.
  Done when: planted ideas matching `fm replay` and `fm usage --prune` are matched to those verbs, and an unrelated idea gets "none".

- **Fork the same pack through the brainstorm skill and a plain prompt, then diff (wild)** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild; the steers insist on signals Foreman didn't author and on "foreman vs plain". Run the brainstorm pipeline and one plain prompt on the same pack, and score the unique grounded ideas each produces. If the plain arm matches, the pipeline's ceremony is overhead.
  Done when: a report lists the grounded-idea counts of both arms on one pack.

- **Time-box a quiet brainstorm: one lens per day, results waiting in the morning card (wild)** — FEATURE — value 2 — effort M — risk med — category: pacing
  Why: wild; assumption: the user reads a short daily result better than a 525-idea dump. Spend idle budget on one lens a day and surface the top three grounded ideas, with the funnel line.
  Done when: a scheduled run files one lens's top-3 into the morning card and logs the cost.

Next question: Which ideas on past slates did the user accept without grounding, and how many of them later turned out to be duplicates?
Next question: What is the false-negative rate of a zero-token grep resolver, measured on the 8 recorded missed asks?
