# Brainstorm — lens: deepen: selection

- **Write one selection verdict file per rewrite** — FEATURE — value 5 — effort M — risk low — category: selection
  Why: the category already holds "closes more", margin, repeats, cost and ties as separate ideas; the pack shows no single place where they combine. A `verdict.json` (parent closed set, child closed set, repeats, cost, tie rule applied, ungradable count, decision) beside lineage.md makes each ruling replayable by a fresh session.
  Done when: for every rewrite in a test tower, `fm genesis status` prints the decision and `fm genesis verdict --replay` recomputes the same decision from the stored file alone.

- **Compare on paired scenarios, not totals** — FEATURE — value 5 — effort M — risk low — category: selection
  Why: assumption: totals hide swaps (child closes 3 new, reopens 2 old). Combines "ratchet" and "closes more". Report the per-scenario diff matrix (gained, lost, unchanged) and require gained > lost with zero lost among scenarios the parent closed on all repeats.
  Done when: a fixture rewrite that gains 2 and loses 1 stable scenario is rejected, and the output names the lost scenario.

- **Rank by lower confidence bound** — FEATURE — value 4 — effort M — risk med — category: selection
  Why: the list has "rerun for variance" and "margin" separately. Merge them: each side runs k repeats, the child wins only if its closure rate's lower bound beats the parent's mean; k grows only when the result is borderline, so most rewrites cost little.
  Done when: a seeded noisy fixture (flaky scenario at 50%) never wins at k=3, and a clear improvement wins at k=2 without extra reruns.

- **Hold the held-out third behind a spend counter** — SECURITY — value 5 — effort M — risk low — category: selection
  Why: inversion risk from the pack: overfitting the held-out third. Each look at the held-out score by a rewrite author, or a selection, is logged. Selection reads it once per rewrite; after N reads on one tower the held-out third is retired and a fresh third is generated.
  Done when: a test showing the (N+1)th selection on the same third triggers regeneration, and the rewrite author's context never contains held-out results.

- **Price rewrites on a Pareto front, not one scalar** — FEATURE — value 4 — effort M — risk med — category: selection
  Why: the pack's cost-per-scenario, context tax and tie-break ideas pull in different directions. Keep a front over (closed, dollars, wall-clock, tower size); a rewrite survives if non-dominated, and the default pick is the one chosen by a written dollar rule.
  Done when: `fm genesis status` lists the front for a generation, and a dominated rewrite is marked "pruned: dominated by X".

- **Mark ungradable runs and rerun them at no charge to either side** — FIX — value 4 — effort S — risk low — category: selection
  Why: "infra failures as ungradable" is listed, but not what follows. Ungradable results are retried up to a cap, excluded from both sides' denominators, and a rewrite with too many of them gets "undecided", never a loss.
  Done when: a fixture with a killed child process yields "ungradable", is retried, and the final verdict's denominators are equal for parent and child.

- **Keep the loser as a not-yet entry with the reason** — FEATURE — value 4 — effort S — risk low — category: selection
  Why: the user's standing steer is that no idea is killed for ambition and the not-yet ledger is retried each generation. A rewrite that loses should enter the ledger with the scenarios it gained, so the next generation can try to graft just those parts.
  Done when: a rejected rewrite creates a ledger entry listing its gained and lost scenarios, and the next generation's run reads it.

- **Graft winning hunks from a losing rewrite (crossbreed selection)** — FEATURE — value 4 — effort L — risk med — category: selection
  Why: the pack has fm ideas crossbreed already. A loser that gained scenario S but lost T may contain a hunk that causes S. Split the rewrite into hunks, apply each alone to the parent, and keep the ones whose paired diff is positive.
  Done when: on a fixture where a rewrite has one good and one bad hunk, the grafted child closes the good scenario and reopens none.

- **Selection audit: a cold reviewer judges the verdict, not the rewrite** — SECURITY — value 4 — effort M — risk low — category: selection
  Why: the pack asks for outside signals (fm second, outcomes survival). Give a tool-less child only the verdict file and exam keys' public parts, and ask whether the rule was applied as written. A disagreement blocks the promotion.
  Done when: a doctored verdict (a loss marked as a win) is flagged by the audit child in a test.

- **Wild: the tower plays itself under a mirrored exam** — FEATURE — value 3 — effort L — risk med — category: selection
  Why: wild. Beyond the "mirror-universe selector" in the list: also generate a twin exam with the same planted gaps in different languages and names. A rewrite that wins on the original but not the twin is recorded as overfit and demoted.
  Done when: a fixture rewrite that hardcodes original scenario names wins the original but loses the twin, and is rejected.

- **Wild: let past losers vote as a jury** — FEATURE — value 2 — effort M — risk med — category: selection
  Why: wild. Keep each retired rewrite as a frozen "juror". When a new rewrite competes, run the jurors on its borderline scenarios, and flag disagreement with the selector as a signal to add repeats. Uses the lineage that already exists.
  Done when: a borderline fixture triggers extra repeats because the jurors split, and a clear one does not.

- **Wild: a selection pressure dial the user can turn** — FEATURE — value 3 — effort S — risk low — category: selection
  Why: wild. One setting (`cheap`, `balanced`, `thorough`) maps to the repeat count, the tie-break rule and the cost ceiling, shown on the site's tower page so the user sees why a rewrite was kept. Assumption: users want one knob, not five.
  Done when: switching the dial changes the recorded repeat count and the tie rule in the next verdict, and the site page shows the dial value.

- **Carry the selection rule itself under selection** — FEATURE — value 3 — effort M — risk high — category: selection
  Why: self-modification links to the pack's concern about rewriting rules toward easier exams. A candidate selection rule may only be adopted if replaying past verdicts under it flips none that the cold audit upheld, and it is proposed as a candidate for the user's yes, never self-applied.
  Done when: a candidate rule that would reverse an audited verdict is refused with the verdict named, and an accepted rule requires a recorded user approval.

Next question: What does a generation cost end to end, so selection knows when k repeats are affordable within the usage budget?
Next question: When two rewrites win on disjoint scenario sets, should selection merge them or pick one, and who decides?
