# Brainstorm — lens: 2030 worked back

- **Log every missing-tool moment as a gap record** — FEATURE — value 5 — effort M — risk low — category: tool acquisition
  Why: the shellcheck item was found by hand and dropped, so no stream turns "I lacked X" into a ranked queue. Assumption: friction, failed commands and "command not found" already appear in the ledgers.
  Done when: `sampo tools gaps` lists gaps from the last 7 days with count, task ids and a find/build suggestion, and a planted "command not found" shows up within one session.

- **Trial every candidate tool in a cage before any grant** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: the steer is to find or build tools and queue grants, and by 2030 registries will be full of look-alikes. Assumption: a scratch home with no network is cheap to start.
  Done when: a fixture MCP server that opens `~/.ssh` or calls out is flagged "undeclared access" and never reaches the grant queue; a clean one gets a trace that matches its manifest.

- **Batch grants into one hash-pinned install plan** — FEATURE — value 4 — effort S — risk low — category: grants
  Why: "install grants queued" plus the rule against interrupting the user means grants must wait as data. Assumption: one yes per plan is acceptable.
  Done when: the queue renders as one page (name, source, pinned hash, the trial trace, what it replaces, expiry), and approving applies exactly those hashes and nothing newer.

- **Decide find-versus-build with a measured bake-off** — FEATURE — value 4 — effort M — risk med — category: approaches
  Why: the request says "finds or builds"; today the choice is ad hoc. Assumption: a script of ≤150 lines plus a test is cheap enough to build as the rival of a found tool.
  Done when: for 3 sample gaps the log shows both arms (found vs built) with test pass, size and dependency count, and the winner is recorded.

- **Wrap big tool schemas for small models** — FEATURE — value 5 — effort M — risk low — category: small-model uplift
  Why: the steer wants a 4B/9B to match frontier results through scaffolding, and large nested MCP schemas are a known small-model failure. Assumption: flat-argument CLI wrappers reduce malformed calls.
  Done when: on a tool-call exam, qwen3.5 4B's valid-call rate on 5 found MCP tools rises with the wrapper against the raw schema, with both numbers published.

- **Run a per-model tool-call exam as the gate for the not-yet local items** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: selfjev-4b, jeff, Jevlike and Von wait on an exam arm against the path they replace. Assumption: tool selection and argument filling can be scored without a live session.
  Done when: `sampo louhi models` prints a held-out tool-call row per model beside the Claude arm, with a decision line naming which items are promoted.

- **Promote a card to a script once it is followed mechanically** — FEATURE — value 4 — effort M — risk low — category: cards to tools
  Why: thousands of cards need a cost ceiling, and a card whose steps never vary is a script waiting to be written. Assumption: step traces show which cards are followed verbatim.
  Done when: a card with ≥5 identical traced runs triggers a generated script plus test, the card becomes "run this", and the exam shows no loss.

- **Retire cards and tools on a measured half-life** — CLEAN — value 4 — effort M — risk low — category: lifecycle
  Why: models gain ground yearly, so a card that lifts a 9B today is dead weight by 2030, and the injected-text notes above all worry about weight. Assumption: lift can be re-measured when the served model changes.
  Done when: each card and tool carries last-used and last-lift dates, and a zero-lift item moves to "dormant" automatically with a reason line.

- **Pin tools in a lockfile with a maintainer-change check** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the standing rules name injection and supply-chain defenses as deferred (T-0791). Assumption: forge APIs expose maintainer and release history.
  Done when: a fixture tool whose source owner changed since the pin is refused with the old and new owner named.

- **Mirror accepted tools locally so a night run needs no network** — FEATURE — value 3 — effort M — risk low — category: offline
  Why: the overnight and local-first threads assume work continues with the cloud away; link rot by 2030 is certain. Assumption: accepted tools are small enough to vendor.
  Done when: with the network blocked, a task that needs an accepted tool still installs it from the mirror with a matching hash.

- **Emit a harness-neutral tool passport for every built tool** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: Sampo must work on Codex, Gemini CLI and opencode, and host plugin formats will shift. Assumption: one description can generate each host's plugin, skill or MCP form.
  Done when: one built tool yields working registrations for two other hosts from the same file, each loaded by a smoke test.

- **Wild: dream the missing tools overnight** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: wild; idle local models (27B) could read the day's gap records, guess 20 tools, build each in the cage, and keep only those that pass a held-out test. Assumption: gap records are rich enough to build from.
  Done when: one morning card lists kept tools with their tests and discarded ones with the reason, and nothing was installed outside the cage.

- **Wild: cold apprentice forges the tool in ten minutes** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild; a tool-less-history child gets only the gap sentence and must build the tool, scored by a hidden test it never sees. Assumption: it measures how well the scaffolding carries a small model.
  Done when: the apprentice's pass rate is reported per model beside the frontier on 10 gaps.

- **Wild: delete a tool when the bare model can match it** — CLEAN — value 4 — effort M — risk med — category: lifecycle
  Why: wild; each tool gets a "bare arm" that tries the same job without it, and a tie for two runs retires the tool. Assumption: most small tools will be matched by 2030 models.
  Done when: a planted redundant tool is retired automatically and the log names the arm that tied it.

Next question: What does a "tool" cost the next session in context and trust, and who decides when a built one stops being worth it?
Next question: Which gaps can only be detected from what the user did by hand, not from what an agent logged?
