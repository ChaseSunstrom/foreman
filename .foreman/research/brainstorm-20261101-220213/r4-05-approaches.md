# Brainstorm — lens: approaches

## Approaches to filling the 61 empty #12 cells (best first)

- **Cover cells by mechanism, not one by one** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: assumption: the 61 cells share about six missing mechanisms (surface-tagged events, per-surface budgets, parity matrix, kill switch, liveness canary, retention). Writing 61 cell texts is the templating trap the steers ban.
  Done when: a table maps each of the 61 cells to one of at most 8 mechanisms, each with a real file path, and `fm genesis sweep` finds no cell whose evidence is a bare phrase.

- **Tag every hook, guard and context event with its surface** — FEATURE — value 5 — effort M — risk low — category: telemetry
  Why: the pack measures hooks (p95 278 ms) and context (387k per reply) only in aggregate. Bets already carry a harness field, so the same pattern extends. Cells then compute from `fm friction`/`fm cost` filtered by surface, not from prose.
  Done when: `fm doctor --by surface` prints hook p95, injected bytes and guard denies for each of the 8 surfaces, with "unmeasured" where there are no events.

- **Make each cell a test marker** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: tests are already organised by area (400 files under `plugin/tests`). A `@cell(stage, surface)` marker means a cell counts only if its test exists and passes. Prose can't fill it.
  Done when: the sweep builds the grid from markers, and deleting one marked test turns exactly that cell red.

- **Record protocol cassettes for the other agents and MCP** — FEATURE — value 4 — effort M — risk med — category: other agents
  Why: T-0335, T-0336 and T-0337 are blocked on live Codex, Gemini and opencode verification. Recorded hook payloads and replies let guard and lean cells for those hosts be tested offline. Trade-off: a cassette can go stale when the host updates, so it needs a host-version stamp.
  Done when: the guard deny-class matrix replays against cassettes for 3 hosts plus MCP with no network, and a stale cassette is reported by name.

- **Import an outside taxonomy as the safe half's rows** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: the steers say weakness-finding must use signals Foreman didn't author. OWASP's LLM and agent-security lists and MITRE ATLAS are such signals. Mapping each entry to a cell, or to a recorded n/a, is cheaper than inventing risks. Trade-off: these lists are generic and need a Foreman-specific reading.
  Done when: every imported entry maps to a cell or a recorded n/a, and the report lists entries that have no cell.

- **Give each n/a an adversary check** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: n/a is the cheapest way to fill a cell, and the least checkable. A tool-less child is given only the surface description and must name one lean or safety failure there. The n/a stands only if the failure is already covered or the child finds none.
  Done when: every n/a cell stores the child's attempt, and a seeded cell with a real hole is rejected.

- **Run the fill as 8 surface lanes with a cross-lane duplicate lint** — CLEAN — value 3 — effort M — risk med — category: process
  Why: this follows the standing rule that S/M briefs run in parallel lanes. Each lane shares one probe harness for its surface. A lint over n-grams catches phrasing reused across rows before the cold read, which saves Sonnet cold-read cost.
  Done when: 61 cells are written, the duplicate lint reports zero, and the cold read passes on its first try for at least 90% of them.

- **Ablate per surface to find what each cell earns** — PERFORMANCE — value 3 — effort M — risk med — category: lean
  Why: the lean ratchet only holds growth to account in aggregate. Switching off one optional hook per surface in a scratch copy shows which cells carry weight and which only add bytes. This is also where Foreman can subtract, as §6 demands.
  Done when: a report lists bytes, ms and exam delta per hook per surface, naming at least one removable item or stating that none was found.

- **Wild: Surface safari** — FEATURE — value 3 — effort L — risk med — category: headless/server
  Why: wild. Launch a bare container with no `claude`, then run install, `fm doctor`, one task and the web UI. Record bytes, ms and every guard decision as the headless/server column. The standing rule that Foreman works without `claude` on PATH makes this a natural proof.
  Done when: the container run passes in CI and its recorded numbers feed the headless/server cells.

- **Wild: Per-cell red team that must find a counterexample** — SECURITY — value 3 — effort M — risk med — category: safety
  Why: wild. A separate-model child sees only a safety cell's sentence and tries to craft a hook input that violates it. The cell counts only if the attempts fail within budget. Bypasses go into the guard corpus, so the grid feeds the guard.
  Done when: the nightly run files at least one corpus case from a failed cell, or states that none were found.

- **Wild: Treemap of the grid in the web UI** — FEATURE — value 2 — effort M — risk low — category: UI
  Why: wild. Area is bytes, colour is proof strength (test, measured, n/a, empty), and each tile links to its probe command. The web UI is the only surface in this mission and has no view of lean state yet.
  Done when: a screenshot shows 8×8 tiles with distinct empty, loading and error states, and keyboard navigation reaches each tile.

- **Lock the grid with probe-output hashes** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: assumption: a model could edit `coverage.md` to pass. A `coverage.lock` holds the hash of each cell's probe output, and changes only through a task that carries the new probe run.
  Done when: hand-editing a filled cell without rerunning its probe makes the sweep fail with the cell named.

Next question: Which of the 61 cells are structurally unmeasurable (the site or Desktop have no hooks to time), and what honest proxy should stand in for them?
Next question: What does the user do when the lean ratchet is red because a measurement doesn't exist yet: wait, delete, or accept "unmeasured", and where is that written down?
