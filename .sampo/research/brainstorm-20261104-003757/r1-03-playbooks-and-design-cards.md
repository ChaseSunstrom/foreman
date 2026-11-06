# Brainstorm — lens: playbooks and design cards

- **Ship a tool-gap ladder card** — FEATURE — value 5 — effort S — risk low — category: playbooks
  Why: Mission 7 #5 asks for find, build, test, use, but the pack shows no single ordered path a small model can follow. The shellcheck case ended as "dropped". Assumption: today's path is split across `fm plugins find` and ad hoc builds.
  Done when: a 4B model, given only the card, resolves a planted missing-tool scenario by stepping through numbered rungs (existing tool, host tool, `fm plugins find`, script, MCP server) and logs which rung it used.

- **Add fill-in script skeleton cards** — FEATURE — value 4 — effort M — risk low — category: design cards
  Why: `plugin/templates/mcp-server/test_server.py` already exists. Small models fail at blank-page building, not at filling slots. Assumption: skeletons for CLI wrapper, JSONL filter and file-walker cover most gaps.
  Done when: three skeleton cards each ship with a test that fails until the slots are filled, and the 9B passes all three from the card alone.

- **Standardize the install-grant request card** — FEATURE — value 4 — effort S — risk low — category: playbooks
  Why: "install grants queued" is in the request, and the standing rule says no installs without a grant. A fixed shape (what, why, source hash, command, rollback, who grants) makes the queue judgeable at a glance.
  Done when: `sampo` refuses to queue a grant missing any field, and the grant list renders one card per item.

- **Gate every card on a measured lift** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the steer says local models match frontier through scaffolding, and Louhi's Smith-on-local arm (T-2908) now exists. A card that does not beat no-card on held-out scenarios is noise.
  Done when: `sampo exam` prints per-card lift for one local model, and cards with zero or negative lift are flagged hidden.

- **Graduate repeated cards into scripts** — FEATURE — value 4 — effort M — risk med — category: capability
  Why: a card followed successfully N times is a procedure a script could run with no model. This removes a model step from the hot path. Assumption: the card store logs use counts and outcomes.
  Done when: a card used ≥5 times with all passes is proposed as a script plus test, and the card's next use calls the script.

- **Write per-model quirk cards from exam failures** — FEATURE — value 4 — effort M — risk low — category: small models
  Why: the pack's own work (T-2893, reasoning switch and empty replies) shows qwen, gemma, granite and gpt-oss each fail differently. One generic card does not fit them.
  Done when: for at least 3 models, the exam's top failure class has a model-keyed card, and the retrieval path serves the model-matching card.

- **Retrieve cards at the failure, not at the start** — FEATURE — value 4 — effort M — risk med — category: retrieval
  Why: the earlier list is full of context-weight complaints. A tool error such as "command not found" can pull the gap ladder at that moment, with zero start-up cost.
  Done when: a "command not found" in a Smith session injects the ladder card exactly once, and the injection is absent in sessions that never hit the error.

- **Check built tools with a conformance card** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: a self-built script or MCP server is unvetted. A fixed checklist runs it in a scratch home under the Ward: idempotent, no network, bounded output, exit codes, secret scan.
  Done when: a built tool lands in "trusted" only after the checklist's commands pass, and a planted network-calling tool is rejected.

- **Compile a frontier tool-building run into a branching playbook** — FEATURE — value 5 — effort L — risk med — category: distillation
  Why: the steer wants frontier results through scaffolding. A frontier trace that built a tool has decision points that can be turned into numbered menus with a checker per step.
  Done when: one recorded Claude run becomes a playbook, and a 27B finishes the same scenario using it, graded by the same exam.

- **Lint design cards for a size and checker budget** — CLEAN — value 3 — effort S — risk low — category: card quality
  Why: the write-time admit in T-2909 exists, but cards also need to fit a 4B's effective context. Each card needs a worked example and one runnable check.
  Done when: admit rejects a card over its token budget or without a check command, with the reason printed.

- **Wild: Hold a card duel, where two small models write rival cards for one gap** — FEATURE — value 3 — effort M — risk low — category: tournament
  Why: wild. A third model executes each card on held-out gaps and the winner is kept. This tests the cheap writers without frontier tokens.
  Done when: a duel runs overnight on one gap class and writes the winner and the loser's score to the card store.

- **Wild: Dream shelf of pre-built tools** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: wild. An idle local model reads ledgers of past "missing tool" blocks and drafts likely scripts into a quarantine shelf, each with a test. Nothing activates without the conformance card passing and a grant.
  Done when: after one night the shelf holds at least 3 drafted tools, each with a passing test, none installed.

- **Wild: Cassette cards, replayable recordings that a small model follows step by step** — FEATURE — value 3 — effort M — risk med — category: playbooks
  Why: wild. A recorded successful tool-build is replayed with the model filling only the diffs, which gives a very strong scaffold for 4B models.
  Done when: a 4B replays a cassette against a changed repo and reaches the same passing test, with step divergences reported.

Next question: what share of "missing tool" moments in real sessions are actually a missing card or skill versus a missing binary, and does the ledger distinguish them?
Next question: when a card's lift flips sign after a model swap on llama-swap, who retires it, and is that decision automatic under the standing push grant?
