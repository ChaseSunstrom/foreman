# Brainstorm — lens: approaches

- **Answer the ask by searching the catalogue first** — FEATURE — value 5 — effort S — risk low — category: reuse
  Why: the pack's "ideas so far" holds roughly 3,000 titles, and 3 of 4 slate items in T-2659 were already built. A new ask is most likely already filed. Trade-off: it misses the genuinely new, but it is the cheapest approach and is the base for the rest.
  Done when: `fm ideas find "<ask>"` returns the top 5 nearest filed ideas, with ids and status (built, dropped, open), in under a second and with zero tokens. A fixture ask seeded from a known duplicate returns that duplicate first.

- **Extract each brief's load-bearing claims and resolve them mechanically** — FEATURE — value 5 — effort M — risk low — category: grounding
  Why: Mission 6 requires "spot checks on each claim a brief rests on", and T-2659 shows grounding was skipped or too loose. A brief would carry `claim: verb fm tidy exists`, `claim: file fmreplay.py`, `claim: flag --dry-run absent`. A script resolves these by grep, `fm help` and `git grep`. Trade-off: it only covers claims that can be written as symbols.
  Done when: filing a brief with a false claim (a nonexistent verb) is refused and names the claim. A true claim passes.

- **Fit a discovery curve to cluster labels and stop on estimated unseen mass** — FEATURE — value 4 — effort M — risk low — category: stopping rule
  Why: the pack's lists repeat heavily (proof, tick, immune, goal themes recur across dozens of rounds). A Chao1-style estimate over per-round cluster counts gives "exhaustive" a number. Trade-off: cluster labels are noisy. Earlier ideas covered saturation counts and capture-recapture only for plan rows.
  Done when: `fm ideas saturation` prints observed clusters, the estimated unseen count and a stop/continue verdict. A synthetic run with 5 new clusters per round continues, and one with 0 new clusters over 3 rounds stops.

- **Brainstorm by morphological grid, one idea per cell** — FEATURE — value 4 — effort M — risk low — category: enumeration
  Why: the standing rule already uses grids for coverage.md. This applies the same idea to ideation: actor × object × stage × failure-mode axes taken from MASTER.md, with each lens child owning a slice of cells. Exhaustiveness is then the filled-cell share. Trade-off: cells can produce filler, so the existing "no templated phrasing" rule applies.
  Done when: a run prints "cells filled / total" and lists the empty cells. Re-running only assigns the empty ones.

- **Make every unexplained ledger row owe an idea** — FEATURE — value 4 — effort M — risk low — category: evidence-first
  Why: the lens rules prefer ideas with evidence, and the "missed asks" list shows imagination misses what the user actually needs. The approach joins `fm friction`, `fm outcomes` and the dropped and deferred ledgers. A row with no linked idea after a round is a gap. Trade-off: it finds only gaps that already left traces.
  Done when: `fm ideas owed` lists the ledger rows with no idea referencing them. A seeded friction row appears there, and it disappears once an idea cites it.

- **Pre-register a kill probe with each idea** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: "Done when" says how to confirm success, but nothing says how to show the idea is already built or pointless. Each idea would add `Dead if: <command that returns true>`, run at intake. Trade-off: some ideas have no cheap kill probe, and those are marked unprobed.
  Done when: intake runs the probes. An idea whose probe is true is filed as "already built" with the output, and a probe that errors is marked unprobed rather than passed.

- **Score each lens by hindsight hit rate** — FEATURE — value 3 — effort M — risk low — category: lens quality
  Why: T-0829 (scale lenses from `lens_rates`) is deferred for want of a measure. Replay past brainstorm outputs against the user's asks since then, and count which lens predicted them. Trade-off: the user's asks are partly shaped by the slate, so this is circular unless the contaminated asks are excluded (see "slate-origin" in the pack).
  Done when: the report gives each lens a hit count over a stated denominator, with slate-origin asks excluded.

- **Do less: freeze the pack at a clustered digest of at most 100 lines** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: this pack carries several thousand "ideas so far" lines, and each child pays for them. Trade-off: children can no longer see exact titles, so near-duplicates slip through unless the digest filter above runs after.
  Done when: the pack builder output stays under a set byte cap with the same cluster coverage, and the dedupe step still catches a planted repeat.

- **Chain lenses as an exquisite corpse** — FEATURE — value 3 — effort S — risk med — category: diversity
  Why: independent lenses overlap (the same proof/immune themes recur). Here each lens sees only the previous lens's single best title and must be orthogonal to it. Trade-off: it is sequential and slower, and it loses lens independence.
  Done when: two runs, chained and independent, are compared on distinct-cluster count at the same token spend, and the result is recorded either way.

- **(wild) Have a child reconstruct the project's roadmap from only the closed-task titles, then diff** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: assumption: the closed-task titles encode the implicit roadmap. The gaps between the child's reconstruction and the real open work show the themes nobody thought to brainstorm.
  Done when: the diff lists at least 3 themes absent from the catalogue, or reports zero explicitly.

- **(wild) Settle ideas in a market: each lens stakes a point budget, and use pays out** — FEATURE — value 3 — effort L — risk med — category: calibration
  Why: assumption: an idea that is built and still used after 30 days is a cleaner signal than the slate's value 1–5 self-score. Lens budgets then drift toward the lenses that predict use.
  Done when: a ledger shows stake, settlement and a per-lens balance for at least 20 ideas.

- **(wild) Run an adversarial "already built" hunter with a grep tool and a bounty per hit** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: 3 of 4 slate items in T-2659 were already built, so a tool-bearing child paid only for finding existing implementations would catch that class. Trade-off: it costs tokens per slate, so cap it by idea count.
  Done when: seeded with three known-built ideas in a ten-idea slate, it flags all three and cites the file for each.

Next question: which of the user's asks in the last 30 days were already answered by a filed idea, so the real miss is retrieval rather than generation?
Next question: does the extracted-claim check slow intake enough that briefs get filed without it?
