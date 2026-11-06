# Brainstorm — lens: capability map

- **Publish `sampo capability map` as the decider's spec** — FEATURE — value 5 — effort M — risk low — category: governance
  Why: The request asks "what it is trained on, how it is measured, how it improves every Rune generation" but the pack has no single artifact naming the decider's capability surface; earlier brainstorms listed slots but never a checklist a reviewer can hold a generation to. The user's words ("we will want it to be a generic model… and maybe brainstorm on features the model should have") want an explicit, auditable list.
  Done when: `sampo capability map` prints a table of every slot (decide, close-holds, loop-predict, cost-router, ward-tighten, next-ask), each with its input schema, output grammar, measurement, fallback, and a green/red "earned" flag from the latest Rune.

- **Define the serving & failover contract as a first-class capability** — FEATURE — value 5 — effort M — risk med — category: serving
  Why: The request explicitly asks "how it is served on this box," and the earlier brainstorm left "what does the model path do when the GPU is busy with the moons funnel" as an open question. The pack shows a slot pool and Ollama on this box; no idea names the serving lifecycle (warm, cold, swapped, dead) as a capability with a measured response.
  Done when: `sampo doctor` reports for each model slot: resident, warm, cold-swap (with cost), and unreachable (with the fallback that fired), and the ship gate fails if any adopted slot has no tested fallback.

- **Make the Rune-generation improvement loop a named, causal capability** — FEATURE — value 5 — effort M — risk low — category: training
  Why: The request asks "how it improves every Rune generation," but the pack's ideas stop at "retrain and re-bench." No idea defines the loop as a capability with a measurable delta: what the generation changed, what it measured, and what it must beat to keep the slot. This is the causal spine the whole request hangs on.
  Done when: Each Rune generation emits an `improvement.md` naming, per slot, the change, the holdout delta, and the kill condition; `samo genesis check` fails a generation that adopts a slot whose delta is not statistically positive over the last two generations.

- **Wire every slot to a named session path with a free-arm baseline** — FEATURE — value 5 — effort M — risk low — category: adoption
  Why: The user's standing rule says a capability whose free arm beats the session arm is a top gap, and that every capability must be called by a real session path. The decider slots (decide, close-holds, loop-predict) are currently only "exist as a verb" in the ideas. The pack's open work (T-0034, T-0035) and the "what a user who never read MASTER.md needs" question earlier make this the adoption gap.
  Done when: `samo genesis check`'s reach names, for each model slot, the verb the missions name that a session path calls, and the free-arm (kNN or rules) baseline for the same scenario; a slot with no session path is red.

- **Add a per-slot statistical floor and abstain curve to the capability spec** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: Earlier ideas say "make every model abstain" and "add a statistical floor to every adopt decision" but no idea defines these as the *capability* the decider must have. The user's standing rule on exam recall per language/bug type and the "below-20-briefs" open question mean the spec must name the minimum evidence a slot needs before it may vote.
  Done when: Each slot's spec file declares its abstain threshold, its minimum holdout size, and its confidence interval; `samo doctor` flags any slot operating below its declared floor.

- **Define the genericity and provenance capability with a redaction contract** — FEATURE — value 5 — effort M — risk med — category: genericity
  Why: The user's words ("generic in the sense that we don't want it to just work on the sampo repo itself") and the earlier "below-20-briefs" question mean the decider must be a capability that proves it generalises, not just trains. The pack's "hold out whole projects" idea covers it partially, but no idea names the redaction and leak-scan as the *capability* with a testable check.
  Done when: `samo capability map` shows a "genericity" row per slot with the leave-one-project-out score, the redaction pass result, and a "proven on N projects" count; a slot below the floor for its project size is marked "not yet generic."

- **Name the "user who never read MASTER.md" capability with a one-screen view** — FEATURE — value 4 — effort S — risk low — category: surface
  Why: An earlier brainstorm left the question "what would a user who never read MASTER.md need to see to know which slot is model-driven and how to turn it off" open. The pack's web UI is the surface, and the rename (Foreman→Sampo) means the docs are in flux. No idea defines this as a capability the decider must provide.
  Done when: `samo status` (or the web UI's decider card) shows, in ≤5 lines, every model-driven slot, its current state (on/shadow/off), its last measured delta, and the one command to turn it off; a cold child can answer "which decisions does the model make?" from that output alone.

- **Add the fail-safe & degradation capability set to the spec** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: The pack's ideas cover "hold the model out of the Ward" and "pin a deterministic fallback per slot" but no idea defines the full degradation ladder as a capability: what happens when the endpoint is cold, swapped, dead, or the weights are corrupt, and what the user sees at each rung. The user's steer "budgets are a backstop, never a reason to stop" means degradation must be visible and recoverable.
  Done when: `samo doctor` shows a degradation ladder per slot (resident → warm → cold → dead → fallback) with the measured transition cost and the fallback that fired last; the ship gate fails if any rung has no tested response.

- **Define the training pipeline as a capability with inputs, gates, and a resumable contract** — FEATURE — value 5 — effort L — risk med — category: training
  Why: The user's request asks "how it is trained," and the pack's ideas list "make training resumable and VRAM-safe" and "retrain by a content hash" but no idea defines the pipeline as a capability with a named input (the outcome lake), a gate (the holdout bench), and a contract (idempotent, resumable, one command). The earlier "GPU busy with the moons funnel" question means the pipeline must name its resource contract.
  Done when: `samo decide train --help` prints the input, the gate, the output artifact, and the VRAM/time budget; running it twice on the same lake produces the same artifact; the ship gate verifies the artifact's hash before adoption.

- **Map the "how it improves every Rune" as a causal loop with a measurable delta** — FEATURE — value 5 — effort M — risk low — category: training
  Why: This is the second-order capability the whole request asks for but no idea defines: not just "retrain" but "the generation changed X, the delta on holdout was Y, and the slot is kept only if Z." The user's standing rule on lean substance ("growth whose capability has no exam or outcome measurement yet waits") means this loop must be the gate for every adoption.
  Done when: Each Rune generation's report includes, per slot, the causal claim ("this change improved close-holds by N%"), the measurement, and the kill condition; `samo genesis check` refuses to close a generation that adopts a slot without a positive delta over the last two.

- **Define the model-slot registry as the single source of truth** — FEATURE — value 4 — effort M — risk low — category: governance
  Why: The pack's ideas list "champion/challenger model registry" and "per-call-site adoption registry" but no idea defines the registry as the *capability* that answers "which model is doing what, on which slot, with what evidence, and how do I roll it back." The rename and the multi-harness support (Claude, Codex, Gemini, opencode) make this the coordination gap.
  Done when: `samo capability map` reads from one registry file that names every slot, its current model, its champion/challenger, its adoption date, its holdout score, and its rollback command; `samo doctor` verifies the registry matches the live state.

- **Wild: Let the decider write its own capability map and defend it** — FEATURE — value 3 — effort M — risk med — category: capability map
  Why: The user's standing rule that "no idea is killed for ambition" and the moonshot wildness requirement make this a natural second-order idea: the decider, having trained on the ledger, can generate its own spec and be challenged by a cold reviewer. The pack's "the model writes the next Moonshot before you ask" idea is in this family but no idea does it for the capability map itself.
  Done when: `samo capability map --generate` uses the local model to draft the spec from the ledger and the last three generations; a cold reviewer (stronger model) scores it against the user's standing rules, and the draft is filed as a brief if it passes.

- **Wild: Ship the decider's capability map as a public "Sampo Discipline" spec** — FEATURE — value 3 — effort M — risk low — category: capability map
  Why: The user's standing rule "Foreman isn't specific to Claude Code" and the earlier "make the discipline a portable spec" idea mean the capability map is not just internal governance but a public artifact any harness can implement. The pack's site and README already publish the discipline; no idea publishes the *decider's* spec as a standalone, versioned document.
  Done when: `site/` publishes a `discipline-spec.md` generated from the registry, with every slot, its grammar, its measurement, and its fallback; a `samo spec --version` command prints the spec's content hash, and the CI gate verifies the site matches the registry.

- **Wild: Run a "capability extinction" drill each Rune generation** — FEATURE — value 3 — effort M — risk med — category: capability map
  Why: The user's standing rule on lean substance and the earlier "retire a tool when the bare model passes" idea mean the capability map must be able to *remove* rows. No idea defines a drill that tests whether a slot is still needed by running the generation with that slot off. The pack's "keystone score" and "retire-when" ideas are adjacent but no idea runs the drill.
  Done when: Each Rune generation includes a "capability extinction" section: for each slot, the holdout delta with the slot off vs. on; a slot whose delta is not positive for two consecutive generations is marked "retire-when: next generation" and the retirement is filed as a brief.
