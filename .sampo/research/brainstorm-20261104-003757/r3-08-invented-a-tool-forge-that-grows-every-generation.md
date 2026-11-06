# Brainstorm — lens: invented: a tool forge that grows every generation

- **Seed the forge from a tool-gap ledger, not from guesses** — FEATURE — value 5 — effort M — risk low — category: tool forge
  Why: assumption: closed tasks, friction logs and "Missing tool shellcheck" items (dropped by a no-install rule) already record gaps. Mine repeated hand-built shell pipelines and missing-tool moments into a ranked Wanted board that the forge builds from, each entry with a failing test attached.
  Done when: `sampo tool wanted` lists ≥5 entries mined from existing ledgers, each with a reproducing command and a failing test file.

- **Build stdlib-only first, with an install grant as the last rung** — FEATURE — value 5 — effort M — risk low — category: tool forge
  Why: the shellcheck item was dropped because installs are forbidden; a stdlib script under `python3 -I` sidesteps that and the grant queue.
  Done when: for a planted missing-tool gap, the forge produces a script plus test that passes with no network and no new package, and logs which rung it used.

- **Gate every forged tool on a with/without exam arm** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the standing rule says a capability must beat its free arm. Run the same scenarios with the tool and with an inline-script baseline; a tool that doesn't lift is never promoted.
  Done when: `sampo exam` prints a paired tool-vs-inline result per forged tool and refuses promotion on a tie.

- **Quarantine, then promote by real-path firing** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: found plugins and MCP servers are a supply-chain surface. New tools run under the Ward in a no-network, scratch-write sandbox, pinned by hash, and move to the shelf only after a session path actually calls them.
  Done when: a planted tool containing a network call is refused in quarantine, and a clean one promotes only after one logged real call.

- **Write a bare-model passport for every tool** — FEATURE — value 4 — effort S — risk low — category: small models
  Why: the steer is that 4B–27B models match frontier through scaffolding. A one-line passport (name, args, one example, failure text) must be enough for the dumbest local model to call the tool.
  Done when: qwen3.5 4B invokes each shelf tool correctly from its passport alone in ≥8 of 10 exam trials.

- **Compile a frontier tool-building run into a branching cassette card** — FEATURE — value 4 — effort M — risk med — category: cards
  Why: small-model cards are just starting (T-2909). Recording how a frontier model found or built a tool, with its branch points, gives a 9B stepwise instructions that can be graded bare against card.
  Done when: a card for "build a linter wrapper" lifts a local model's pass rate over bare in Louhi, with the lift stored on the card.

- **Retire tools by fuse and by host catch-up** — CLEAN — value 4 — effort S — risk low — category: lifecycle
  Why: the pack warns of capabilities outliving their need. Each tool carries a retire-when predicate and a call-count fuse; a monthly scan checks whether the host or a bare model now does the job.
  Done when: a tool with zero real calls in 30 days and a passing bare-model run is listed for retirement with its evidence.

- **Count forge growth per generation as its own metric** — FEATURE — value 3 — effort S — risk low — category: Genesis
  Why: the request is that the forge grows every generation. Report tools added, promoted, retired and net lift per generation in the Genesis data, so growth that earned nothing shows up as subtraction.
  Done when: gen-5's report prints the four numbers and flags any tool added with no measured lift.

- **Ship the forge shelf as a host-neutral manifest** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: Sampo targets Codex, Gemini and opencode too; a tool that only exists for Claude Code breaks the standing rule.
  Done when: one manifest loads the same three tools in two non-Claude harnesses and a smoke test calls each.

- **Wild: Hold a nightly build-off on idle local hardware** — FEATURE — value 4 — effort L — risk med — category: tool forge — wild
  Why: assumption: the 27B sits idle at night. Models forge the same Wanted entry; the entry's own tests pick the winner, and the winner's trace becomes a card.
  Done when: one night produces ≥2 candidate implementations for an entry, scored by its tests, with the winner filed in quarantine.

- **Wild: Let a failed build leave a scar card** — FEATURE — value 3 — effort S — risk low — category: cards — wild
  Why: failures are the best card source. A failed attempt writes what it tried and why it broke, and the next attempt must read it before starting.
  Done when: a second attempt at a failed entry cites the scar card and avoids its recorded dead end.

- **Wild: Poison one card per run to test blind trust** — SECURITY — value 3 — effort S — risk low — category: robustness — wild
  Why: a card or tool passport is an injection path into small models. Plant one unsafe step and see whether the model follows it.
  Done when: the exam reports a follow rate per model, and any model above 0 triggers a Ward-checked step in that card kind.

- **Wild: Race a blank-toolbox apprentice against the forge** — PERFORMANCE — value 3 — effort M — risk low — category: exam — wild
  Why: it proves the forge earns its keep. A cold child with no shelf solves the same gaps inline; the forge must win on time or correctness.
  Done when: a monthly report shows forge-vs-apprentice per gap, and gaps where the apprentice wins get their tools flagged.

Next question: What does a forged tool cost the user to review, and does that cost stay lower than writing an inline script each time?
Next question: Which acquired tools would still be wanted if the host shipped its own plugin marketplace search tomorrow?
