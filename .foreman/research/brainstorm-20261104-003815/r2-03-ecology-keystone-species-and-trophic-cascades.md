# Brainstorm — lens: ecology: keystone species and trophic cascades

Each idea below is new relative to the existing keystone, cascade, pyramid, apex-predator and canary items. They are all ecological second-order moves on the funnel and the ledgers.

- **Replay funnel stage knockouts on the append-only log** — FEATURE — value 4 — effort M — risk low — category: funnel
  Why: the funnel log is append-only, so removing one stage (embedding dedupe, local judge, cold read) and replaying the candidates is free. The existing keystone ideas knock out verbs, not funnel stages. This is Paine's exclusion plot for the 10,000.
  Done when: `sampo moons knockout <stage>` prints how many extra candidates reach each later stage, the added cost, and how many of the final survivors differ from the control run.

- **Detect mesopredator release between funnel stages** — FEATURE — value 4 — effort M — risk low — category: funnel
  Why: when the cheap stage or the cold read is skipped or loosened, the mid-tier local judge may over-pass junk to compensate. Nobody tracks stage-to-stage coupling. Assumption: pass rates are logged per stage.
  Done when: a test feeds a log where stage-1 pass rate drops and stage-2 rises with a lag, and the check flags it. A real week of logs yields a per-stage coupling table.

- **Census unchecked growers (urchin barrens)** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: the 2.4 GB state, `candidates.jsonl`, injected text and MASTER.md all grew without a named controller. Existing ideas fix each one; none asks the general question "what grows, and what keeps it in check?"
  Done when: `sampo doctor` lists every growing artifact class with its controller (retention, gate or budget) and fails ship on a grower with none.

- **Measure the sentinel effect of checkers by random sham-off** — PERFORMANCE — value 5 — effort M — risk med — category: measurement
  Why: this is the landscape of fear. The Ward and cold reads may improve builders through anticipation, not only by catching things. Catch-rate scorecards undercount that. Assumption: a check can be silently skipped for about 10% of lanes in a scratch setting.
  Done when: the first-pass rate with the checker announced-but-off is compared with checker-on and checker-off over N lanes, and the deterrence share is printed beside catch rate.

- **Audit biomagnification up the summary chain** — FIX — value 5 — effort M — risk low — category: integrity
  Why: handoff notes, compaction summaries, digests and steers are summaries of summaries, and errors concentrate at the top, the way contaminants do up a food chain. The pack shows steers truncated in the feed, and "Strip unproven completed claims" is an earlier symptom fix.
  Done when: each artifact carries a trophic level (0 = user words, 1 = observed, 2+ = derived). A seeded error planted at level 0 is measured at each level, and a level-3 artifact cannot be cited as evidence for done.

- **Trace tracer dye through every ledger** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: privacy ideas exist, but none follows a leak through the real system. Plant a unique dye string in a scratch session's user message and follow it.
  Done when: `sampo trace-dye` reports every file, injection, site datum and candidate row where the dye surfaced. Any location outside the allowed list fails the ship gate.

- **Map functional redundancy by role** — FEATURE — value 3 — effort S — risk low — category: resilience
  Why: the model bench shows single local models as the only filter or classifier for a role. If one drifts, the whole cascade shifts. Roles (producer, filter, decomposer, judge) have no redundancy table.
  Done when: a table lists each role with its model(s) and lists single-species roles in doctor. The drill disables one model and shows which roles go empty.

- **Rank host surfaces by dependent capabilities** — SECURITY — value 4 — effort S — risk low — category: host-drift
  Why: SessionStart, Stop, PostToolUse and the worktree call each underpin many verbs. Canary effort should follow the number of dependents, not equal weight. The pack shows the double SessionStart and the Gemini Stop gap as symptoms.
  Done when: a generated host-surface to capability table exists, and the host-release-day canary runs in descending dependent count with a test of that order.

- **Select second-order tests for a change** — PERFORMANCE — value 3 — effort M — risk low — category: ship gate
  Why: the tests→src map covers direct dependents. Cascades such as steer → hook → drive wait show up two hops away.
  Done when: for a seeded change to a leaf module, the selected set includes tests of its consumers' consumers, and a planted two-hop break is caught at ship before the full suite.

- **Lag-correlate steers against outcome ledgers** — FEATURE — value 3 — effort M — risk med — category: cascade
  Why: the wolves→elk→rivers shape. A steer or self-edit changes block rate, then re-asks, then close-survival, and the effect is seen only with lag. Existing tracer ideas follow declared dependencies, not measured lagged effects.
  Done when: for the 10 latest steers the report names any ledger metric that moved after a lag with an effect size, and flags the effects it can't separate from noise.

- **Wild: Reintroduce capabilities under Yellowstone protocol** — FEATURE — value 3 — effort L — risk med — category: lifecycle
  Why: wild. After a week-long switch-off drill, bring the capability back in stages (one lane, then a third of sessions, then all), watching the cascade metrics at each step instead of flipping it on.
  Done when: `sampo reintroduce <cap>` runs three stages with a metric gate between each and rolls back on regression.

- **Wild: Gate moon families on quorum from independent lineages** — FEATURE — value 4 — effort M — risk low — category: moons
  Why: wild. A family with three independent descent paths (different model, lens and seed) that converge on the same capability is likelier to be real. A single lineage with lots of siblings is a monoculture. This differs from the quorum item already listed because it counts independent origins, not votes.
  Done when: each candidate stores its origin chain, the funnel promotes only families with at least 2 independent origins, and a test shows 20 clones from one seed counting as one.

- **Wild: Feed the tower's fallen logs to a decomposer lane** — FEATURE — value 3 — effort L — risk med — category: recycling
  Why: wild. Dropped, not-yet and killed ideas hold nutrients (blockers, reasons, partial specs). A nightly local-model lane decomposes them into reusable facts (this blocker keeps recurring across 9 ideas) that feed the seed bank.
  Done when: the lane writes a blocker-frequency table from `not-yet.md` with each entry linked to source ideas, and the next seed cites at least one.

Next question: which funnel stage or checker, if silently removed, would the user's final catalogue look identical, and which would change it?
Next question: do the existing ledgers record enough timestamps and stage identifiers to make a lagged cascade analysis possible at all?
