# Brainstorm — lens: crossbreed far domains

- **Cap the 10,000-moon funnel with a Lotka-Volterra controller between stages** — PERFORMANCE — value 4 — effort M — risk low — category: funnel
  Why: the pack shows a cheap-first funnel over 10,000 candidates with local models doing bulk (T-2868/2869), but no mechanism that stops a cheap stage from flooding the dearer one or starving it. Crossbreed: predator-prey dynamics from ecology plus control theory. Stage N+1 throughput sets the admit rate of stage N; the controller damps oscillation between idle and flooded.
  Done when: a replay of the funnel log on 10,000 candidates shows the queue length ahead of the Sonnet stage never exceeds a set bound, and the local model's idle share falls against the uncontrolled run.

- **Write a family "immune memory" that fast-rejects clones of past killed moons** — SECURITY — value 4 — effort M — risk low — category: dedupe
  Why: "Ideas so far" repeats the same themes (MASTER.md sharding, double SessionStart) across rounds; the funnel's dedupe is exact then embedding. Crossbreed: adaptive immunity's affinity maturation. Each killed moon leaves an antibody (embedding plus kill reason); a new candidate that binds one inherits its verdict before any model reads it.
  Done when: planted paraphrases of 50 killed moons are rejected at the embedding stage with at least 90% recall and zero kills of 50 planted novel moons.

- **Treat the injected context as a bloodstream and give it a haematocrit gauge** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: the pack's lean numbers (2,733 chars, 75,758 tokens) and many "budget" ideas lack one living-systems vital sign. Crossbreed: physiology. One scalar, the share of injected characters the model referenced in the following five turns, shown in `sampo doctor` and the pane header.
  Done when: `sampo doctor --json` prints a `used_share` between 0 and 1 computed from a recorded session transcript, and a fixture with known references yields the expected value.

- **Add a Ward "toxin-antitoxin" pair so a removed Ward fails loud** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: many ideas cover Ward liveness; none uses bacterial toxin-antitoxin addiction. Crossbreed: microbiology. The session holds a toxin (a short-lived capability to run in bypass mode) that decays unless the Ward's antitoxin token is refreshed each turn; if the Ward is missing, bypass lapses by itself rather than silently running unguarded.
  Done when: with the Ward hook deleted in a scratch install, a bypass session loses its bypass flag within N turns and prints one line saying why.

- **Pre-warm the endpoint by tidal schedule from its measured uptime and model-switch cost** — PERFORMANCE — value 4 — effort M — risk low — category: local models
  Why: the user steer says a llama-swap switch costs ~3 minutes with no detection; the earlier ideas batch by model but none forecasts. Crossbreed: tidal prediction (harmonic analysis of sea level). Fit daily harmonics to the user's usage and the endpoint's resident-model history, then switch during predicted troughs.
  Done when: replaying a week of ledger on the scheduler yields fewer user-visible switch stalls than the batch-by-model baseline, reported by one command.

- **Run a "ligand-receptor" match between a task's needs and a model's measured binding profile** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the Louhi model bench (T-2887/2894) measures each local model on Sampo's own work, and Uplift runs Smith per profile, but routing is by hand. Crossbreed: pharmacology docking. Each task kind is a pocket; each model a ligand with measured affinity; assign the best-fitting model and record the miss.
  Done when: `sampo louhi route <task>` returns a model with a score, and on held-out closed tasks beats the fixed default on pass rate.

- **Fold repeated shell sequences into enzymes (cached macros) by Michaelis-Menten saturation** — PERFORMANCE — value 3 — effort M — risk med — category: speed
  Why: the hook-latency and drive-wait fixes (T-2900/2901) show many repeated small calls. Crossbreed: enzyme kinetics. A sequence seen above a saturation rate is compiled to one verb whose output is cached by input hash.
  Done when: a recorded session with a 5x repeated sequence shows the later runs served from cache with identical output and lower wall time.

- **Wild: Let the Ward grow a "scar tissue" rule from every near-miss** — SECURITY — value 5 — effort L — risk high — category: guard
  Why: wild. Crossbreed: wound healing. A command that passed but a cold reviewer judged risky thickens the rules around that shape, tighten-only, with a decay unless re-confirmed; the user sees a scar list.
  Done when: a planted near-miss command shape is refused on its sibling after one reviewer verdict, and the scar expires after its window with no hit.

- **Wild: Cast the 10,000 moons as a coral reef that bleaches when its symbiont model is swapped** — FEATURE — value 3 — effort L — risk med — category: moons
  Why: wild. Crossbreed: coral-algae symbiosis. Each accepted moon records which model scored it; when the scoring model changes, dependent verdicts are marked bleached and rescored cheapest-first, visible in the web UI as pale tiles.
  Done when: swapping the scoring profile marks exactly the dependent moons bleached and the rescoring queue clears them.

- **Wild: Compress the guard into a DNA-style 4-letter checksum codon strip shown in the status line** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: wild. Crossbreed: genetics. Each guard clause maps to a codon; a mutated or missing clause changes the strip, so the user sees at a glance that the Ward differs from last session.
  Done when: removing any one guard clause changes the strip and restoring it returns the original.

- **Wild: Echolocate the repo: send a cheap probe verb and map the state from returns** — FEATURE — value 3 — effort M — risk low — category: map
  Why: wild; bats. Instead of injecting the map, the session fires `sampo ping <area>` and gets a few-line echo of what is near, replacing the injected block.
  Done when: a cold child answers three "where is X" questions using only ping, at lower characters than the injected map.

- **Stress-test the funnel with a "drought year": half the local capacity for a night** — PERFORMANCE — value 3 — effort S — risk low — category: resilience
  Why: ecology's drought resilience applied to the 10,000-scale run; the pack shows endpoint stalls and a 3-minute switch cost.
  Done when: a throttled replay completes with a reported loss in recall of at most a stated bound and no lost candidates.

- **Sign the funnel log as a hash-chained tree-ring** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: the funnel log is append-only (T-2868) but not tamper-evident; dendrochronology, one ring per batch.
  Done when: editing any past line makes `sampo genesis check` name the first broken ring.

Next question: Which crossbreed pairs (domain × Sampo mechanism) have actually moved a measured number in past moons, versus only sounding wild?
Next question: Does the funnel's recall at 10,000 hold when the candidate language drifts from the lens vocabulary?
