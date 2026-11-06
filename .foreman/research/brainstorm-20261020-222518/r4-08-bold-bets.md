# Brainstorm — lens: bold bets

- **Serve the harness as an OpenAI-compatible model** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: assumption: the planned MCP/ACP server covers tools that call `fm code`, but Continue, aider, Open WebUI and scripts only speak chat-completions. "foreman-1" would be a model whose reply is a plan, proof and commit.
  Done when: `curl localhost:PORT/v1/chat/completions` against a fixture repo with a fake runner returns a message naming a closed task id and commit hash.

- **Hold out blind acceptance checks** — SECURITY — value 5 — effort M — risk med — category: proof
  Why: a worker that wrote its own tests can game them (the pack has a cheat-corpus idea but no holdout). A second runner sees only the request, writes checks the builder never sees, and they run at close.
  Done when: a fixture where the builder special-cases its visible test fails the hidden check and the task stays open.

- **Promote a repeated correction into a standing rule** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: the user said "stop asking to release", "full permission" and "don't stop, full auto" in separate sessions. The second identical steer should become a scoped, expiring, plain-words rule with a receipt, not a third repetition.
  Done when: replaying two fixture steers saying the same thing creates a rule visible in `fm code config explain`, and a later release proceeds without asking.

- **Escalate a stuck step up a runner ladder** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: assumption: the planned fallback fires on runner failure, not a red check. After N red attempts the same step moves to the next runner (local, then CLI, then strongest) carrying the failing output and prior diffs, and every rung is priced in the receipt.
  Done when: a fake weak runner fails twice, a fake strong runner passes, and the receipt shows both rungs with cost.

- **Warm a clean-tree baseline at launch** — FEATURE — value 4 — effort S — risk low — category: speed and truth
  Why: while the planner is silent for minutes (the nixie run), the harness runs the project's gates on the untouched tree. "Fails first" then means "newly fails", and pre-existing red is named instead of blamed on the run.
  Done when: a fixture repo with one already-red test shows "already red: X" before the plan arrives and the close does not count it against the run.

- **Mutation-prove every diff** — SECURITY — value 4 — effort M — risk low — category: proof
  Why: `fm task prove` already shows the test fails without the change. Extend it to revert each hunk in turn; a hunk whose removal breaks no check is flagged "unproved change".
  Done when: a diff with one tested hunk and one decorative hunk closes with the decorative one listed as unproved.

- **Log whether the user kept the result** — FEATURE — value 4 — effort M — risk low — category: outcome truth
  Why: assumption: the held-rate and bench grades measure proof, not whether the user was happy. A local ledger watches for reverts, amends and large follow-up edits to `fm code` commits within a week and feeds the runner report card.
  Done when: in a fixture repo, reverting a run's commit marks the run "regretted" in `fm code why` and lowers that runner's score.

- **Recall proved runs as few-shot exemplars for small models** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: local models are the weak spot of "any model". Retrieving this repo's past proved (request, plan, diff) triples by similarity into the JSON-slot prompts makes them improve on the user's own code, all on-box.
  Done when: bench pass-rate for a fixed fake-small-model fixture rises with the library on versus off, and no exemplar leaves the machine (socket-denied test).

- **Decide with a timeout when the user is away** — FEATURE — value 4 — effort S — risk med — category: unattended
  Why: "full auto" and "don't stop until complete" mean a "needs you" prompt at 3am wastes the night. Each blocking question carries a pre-declared safe default and a deadline. The default is taken and logged, never one that widens permissions.
  Done when: a fixture run with a pending question resumes after the deadline using the default and the digest lists it.

- **Tune its own config overnight and show the evidence** — FEATURE — value 3 — effort L — risk med — category: self-improvement — wild
  Why: assumption: the pack has startup-tax probes, an audition and a canary, but nothing closes the loop. Overnight Foreman A/B-tests runner choice, nested-profile slimming and timeouts on the user's own recent requests, then proposes a config diff with measured savings. Applying it is one reversible key.
  Done when: a fixture history produces a proposed change with before/after numbers, and undo restores the previous config byte for byte.

- **Transplant a session between CLIs** — FEATURE — value 3 — effort L — risk high — category: interop — wild
  Why: assumption: adopting a live session is planned, but not translating one. When Claude hits a usage limit, its transcript converts to a handoff packet that codex or gemini continues cold, with files touched, decisions and open steps.
  Done when: a recorded Claude transcript fixture yields a packet that a fake second runner resumes, finishing the plan's remaining steps.

- **Read the editor's cursor as request context** — FEATURE — value 3 — effort M — risk low — category: editor — wild
  Why: assumption: "fix this" and "rename that" are the commonest human requests, and the pack only goes the other way (hand off to $EDITOR). A tiny local socket or file written by an editor plugin gives the open file, selection and diagnostics, and the echo-back names them.
  Done when: with a fixture context file, `fm code "fix this"` echoes the file and line range and the plan's scope is that function.

- **Open a shadow week before acting** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: a newcomer is wary of a harness that edits for them. For a week Foreman only reads the user's plain Claude Code transcripts and reports what the guard, plan and proof checks would have caught. It then offers to take over, backed by their own numbers.
  Done when: `fm code shadow` over fixture transcripts prints counted "would have caught" events with ids and writes nothing to the repo.
