# Brainstorm — lens: grid

- **Queue installs as one signed grant manifest** — FEATURE — value 5 — effort M — risk med — category: tool acquisition
  Cell: user × missing/unsafe, on the web UI and `fm`.
  Why: the mission says "install grants queued", and the dropped shellcheck item shows installs currently dead-end on the no-installs rule. A grant lists exact command, source, version, hash, what it touches and the undo line; one key approves it. Expired grants are dropped.
  Done when: `sampo tools grants` lists a queued grant with all fields, and approving one runs only that exact command.

- **Quarantine every candidate tool before it is offered** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Cell: unattended × unsafe.
  Why: found plugins, MCP servers and scripts are third-party code, and the pack already carries 18 injection and supply-chain ideas. Fetch into an empty directory, run it with no network, compare the files and processes it touched against its declared capabilities, and run the Ward over it.
  Done when: a planted candidate that reads `~/.ssh` is rejected with the offending open named.

- **Require a failing negative control before a tool counts as tested** — FEATURE — value 4 — effort S — risk low — category: tool verification
  Cell: agent × wrong.
  Why: "tests it" is a mission clause, and a green tool test proves little. Feed the tool a planted wrong input and mutate its output, and demand that its own test fails. Otherwise the tool is marked unproven.
  Done when: a stub tool with a tautological test is labelled unproven.

- **Show the gap-to-tool pipeline as a tool shelf in the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI
  Cell: user × unclear, web UI.
  Why: the pack's only listed surface is the web UI. The shelf shows each tool as wanted, found, built, tested, granted or retired, with who unblocks it and a hatched "unproven" look. The empty state says "nothing lacking" only when the gap miner ran.
  Done when: a tool at each state renders, and the shelf is readable with no JavaScript.

- **Mine gaps from history, not from guesses** — FEATURE — value 5 — effort M — risk low — category: initiative
  Cell: unattended × missing.
  Why: assumption: transcripts and ledgers hold "command not found", denied installs, repeated hand-run commands and dropped items like shellcheck. Rank them by how often they recur and queue the top ones overnight.
  Done when: a shopping list is produced from a fixture transcript, with a count for each gap.

- **Export acquired tools to every harness as a host-neutral manifest** — FEATURE — value 4 — effort M — risk med — category: other agents
  Cell: other agents × missing.
  Why: the product claims Claude Code, Codex, Gemini CLI and opencode, and the live verifications of codex, gemini and opencode are blocked. Emit each tool once as MCP or a plain script, with a per-harness proven matrix.
  Done when: one built tool is registered in two harness configs and the matrix shows which cell was actually exercised.

- **Decide build versus find with a priced estimate** — PERFORMANCE — value 3 — effort S — risk low — category: tool acquisition
  Cell: agent × slow.
  Why: assumption: web search and trial installs dominate time. Check a local capability index first, offline. Build a script when the estimate is under N lines and the tests are template-able, and otherwise search.
  Done when: for ten fixture gaps the chosen path and its reason are logged, and the offline path answers without network.

- **Score small models on tool building with a scaffold ladder** — FEATURE — value 5 — effort L — risk med — category: small-model uplift
  Cell: unattended × wrong, small models.
  Why: the steer wants local models (27B, 9B, 4B) to match frontier through scaffolding. A tool-building card sequence runs tests first, then a template, then a grammar-constrained script, with the exam arm against the frontier path. Cards enter only if the model with the card beats the same model without it on held-out gaps.
  Done when: `sampo exam run` shows a pass rate with and without the cards for qwen3.8-27b on held-out gaps.

- **Retire tools that never fire on a real path** — CLEAN — value 3 — effort S — risk low — category: reach
  Cell: agent × unclear.
  Why: the standing reach rule says a capability needs a session path. Log each use with its outcome, and move unused tools to the cold shelf after N days with the evidence shown.
  Done when: an unused fixture tool is moved to cold with its zero-use record.

- **Record tool provenance and drift** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Cell: user × unsafe, session start.
  Why: pin source, version, hash and licence per tool, and speak only if the hash drifts. Include a one-line removal command.
  Done when: tampering with an installed tool file triggers a one-line warning at the next start.

- **Wild: Tool forge duel** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Cell: other agents × wrong (wild).
  Why: wild. A local model and a frontier model both build the same missing tool. A third party's hidden tests decide the winner, and the loser's trace is mined into a small-model card.
  Done when: a duel report names the winner, the test count and the card produced.

- **Wild: Ghost-install film** — FEATURE — value 3 — effort M — risk low — category: delight
  Cell: user × unclear (wild).
  Why: wild. Run each install in a throwaway overlay filesystem and play back the filesystem diff as a short animation on the grant card, so the user sees what would change before approving.
  Done when: a grant card shows the diff of a fixture install, and nothing outside the overlay changed.

- **Wild: Overnight tool dreams** — FEATURE — value 4 — effort L — risk med — category: unattended
  Cell: unattended × missing (wild).
  Why: wild. Idle GPU time lets a local model draft tools for the week's top friction in a sandbox. The morning shelf marks each one "unwitnessed" until the user has seen it.
  Done when: a morning shelf lists drafted tools with test results and an unwitnessed flag.

- **Wild: Pawn shop between machines** — FEATURE — value 3 — effort L — risk high — category: sharing
  Cell: other agents × unsafe (wild).
  Why: wild, and assumption: the user runs several machines. Tested tools are traded as signed bundles, and each machine re-quarantines them on arrival.
  Done when: a bundle built on machine A installs on B only after B's own quarantine passes.

Cells left empty: user × slow, because the queue absorbs delay and the user doesn't wait on it. Other agents × slow, for the same reason. Unattended × unclear is covered by the shelf and the morning card.

Next question: When a found tool is already native to the host, who decides to skip it, and is that checked before any search?
Next question: Which small-model cards help only one model, and does the admit test catch a card that just fits the exam?
