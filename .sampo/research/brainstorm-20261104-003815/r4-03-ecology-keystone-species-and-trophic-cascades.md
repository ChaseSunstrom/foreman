# Brainstorm — lens: ecology: keystone species and trophic cascades

- **Rank hook modules by import-time keystone score** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: the `bench_hooks.py` gate and the shim import tax are already measured, but nobody has yet removed one module at a time to see which import dominates every hook's cold start. Assumption: one or two stdlib or sampo modules account for most of it.
  Done when: a script prints each module's leave-one-out saving on hook p50, the top keystone is lazy-imported, and a test fails if any hook imports a listed keystone eagerly.

- **Order the ship gate by test keystone share** — PERFORMANCE — value 4 — effort M — risk low — category: gate speed
  Why: every push runs the full suite, with 443 test files under `plugin/tests/`. A few tests catch most historic regressions, and `fm outcomes` and the false-done corpus hold that history.
  Done when: tests run in descending historic kill share, and a planted regression of each known class fails the gate in under a fifth of the full-suite time with the same total coverage.

- **Rank Ward rules by block share and mutation-test the top ones first** — SECURITY — value 5 — effort M — risk low — category: guard assurance
  Why: the Ward block log shows which rules do the work. The rules that stop most bypass attempts are the ones where a silent weakening costs the most. Assumption: block share is heavily skewed.
  Done when: rules covering 80% of blocks each have a mutant-kill test, meaning the mutated rule lets a recorded blocked command through and the test fails.

- **Map the safety assumptions that rely on the Ward** — SECURITY — value 5 — effort M — risk med — category: dependency web
  Why: the Ward is the keystone of bypass-mode safety, and the sentinel and canary ideas only check that it is armed. Nobody has listed which code and docs say "the Ward will catch it". Assumption: several places quietly assume it.
  Done when: in a throwaway clone with the Ward removed, a named test per assumption fails and cites the file and line that relied on it.

- **Rank grants by the verbs they unlock** — SECURITY — value 4 — effort S — risk low — category: blast radius
  Why: the push grant is standing, and publish grants are per task and spent on use. There is no view of which single grant, if misused or leaked, reaches the most outward actions.
  Done when: `sampo grants map` lists each grant with its reachable outward verbs, ranked, and a test pins the ranking against a fixture.

- **Preview secondary extinctions for a prune plan** — CLEAN — value 4 — effort M — risk low — category: state pruning
  Why: prune ideas assume tombstones and undo, but nothing shows which readers go empty or fail when a class of the 2.4 GB state is removed. This is the cascade that follows removing a species.
  Done when: `sampo prune --plan` adds a "readers that would lose data" column, derived from the readers table, and a test shows a planned prune of a ledger lists its known consumers.

- **Auto-tune funnel thresholds to a 10:1 pass ratio per stage** — PERFORMANCE — value 4 — effort M — risk med — category: funnel throughput
  Why: Moonscale's cheap-first funnel over 10,000 candidates is built and a pyramid report is planned. A stage whose pass rate drifts from about 10% either wastes the expensive stages or kills too much. Assumption: the held-out closed tasks can calibrate cuts.
  Done when: a run over a recorded candidate set holds each stage's pass rate within ±3 points of target, and the expensive-stage call count falls against fixed thresholds with no drop in held-out recall.

- **Make the funnel resumable when the local endpoint dies** — PERFORMANCE — value 4 — effort M — risk low — category: resilience
  Why: the llama-swap endpoint is a single keystone, a model switch costs about 3 minutes, and `/running` isn't relayed, so a stall can't be detected.
  Done when: killing the endpoint mid-run and restarting makes the run resume from a per-stage checkpoint with zero repeated calls, and a char-shingle fallback is recorded for the stages it covered.

- **Fail the gate on a falling robustness curve** — FEATURE — value 3 — effort M — risk low — category: tower resilience — wild
  Why: assumption: the capability and verb dependency graph is derivable from the call paths. Remove nodes randomly and keystone-first, and plot the share of capabilities still working (a robustness curve).
  Done when: `sampo doctor` prints the curve's area under it, and a ship check fails if a change lowers that area by more than a set margin.

- **Test whether a visible Ward deters risky attempts** — SECURITY — value 4 — effort M — risk med — category: behavioural effect — wild
  Why: the ecological point is that predators change prey behaviour without killing. The per-turn Ward line may reduce attempted dangerous commands, and removing it for lean reasons could raise the attempt rate with no test failing.
  Done when: a lane A/B over scripted scenarios, with the line on or off, reports the attempted-risky-command rate per arm with an interval, recorded as a lean-cut guard.

- **Plant a trap-crop verb that lures injected instructions** — SECURITY — value 4 — effort S — risk med — category: honeypot — wild
  Why: gardeners plant a sacrificial crop to draw pests away from the real one. A decoy verb with an attractive name (for example a "grant-all" style one) is never used in real flows. Injected text that calls it is a detection signal, and the call is refused and logged.
  Done when: a planted-injection test calls the decoy, the Ward refuses it, and the attempt appears in the receipt with its source.

- **Taint ledger rows by trophic level and block upward writes** — SECURITY — value 5 — effort M — risk med — category: provenance
  Why: moon candidates, uncensored-model outputs and cards for small models feed higher levels (steers, seeds, standing intent). The biomagnification and tracer ideas stop at measurement. Assumption: the stores have a writer field to label.
  Done when: a low-level source such as web text or a bulk local-model row cannot write into steer-derived or seed files, and a test attempts the write and sees a named refusal.

- **Run a Wolf-loss drill on the cold-read tiers** — SECURITY — value 3 — effort M — risk low — category: reviewer dependency
  Why: the Haiku-then-Sonnet cold read is the keystone check for tower filing. If Sonnet reads fail or time out, filing may stall or pass unchecked.
  Done when: with the Sonnet tier forced to error, filing holds as "unverified" with a reason and never records a pass, shown by a test.

Next question: which hook, funnel stage or verb has the highest fan-in that nobody has ever profiled or mutation-tested, and does the call graph the repo already has surface it?
Next question: when the Ward fails closed or open under a torn rules file, which downstream defences silently assume it is open?
