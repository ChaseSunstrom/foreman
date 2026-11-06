# Brainstorm — lens: bold bets

- **Append every proof to a public transparency log** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: Proofs and receipts live only on the local machine, and the site publishes builds without evidence. Assumption: a verifier outside the repo wants to check a claimed pass without trusting the operator. The log is append-only, so a changed past proof is detectable.
  Done when: `fm proof verify <task>` checks an inclusion proof against a published root, and it fails when one stored proof byte is edited.

- **Deny network egress by default for every run** — SECURITY — value 4 — effort M — risk med — category: sandboxing
  Why: The guard hook inspects command strings, not what a process opens. Assumption: a model-written script can reach any host, and the guard never sees it. Each playbook would declare its allowlist.
  Done when: a gated script that calls a host not on its playbook's allowlist fails before the connection opens, and the refusal names the allowlist entry it would need.

- **Give each subagent a revocable capability token scoped to its paths** — SECURITY — value 4 — effort M — risk med — category: least privilege
  Why: Subagents inherit the parent's full file and shell reach. The queued "abort on out-of-set edit" idea only detects a breach after it happens.
  Done when: a subagent holding a token for `src/a` that writes `src/b` gets a denial at the write, and the same token is rejected after the run closes.

- **Cap model subprocesses in a cgroup with hard memory and CPU limits** — PERFORMANCE — value 3 — effort M — risk low — category: resource limits
  Why: The hook bench p95 ran over budget under load (dropped item), and a runaway check can starve the box. Assumption: a process-level cap fixes this more reliably than a timeout.
  Done when: a fork bomb inside a gated check stops at the cap, the desktop stays responsive, and the receipt reports the cap that applied.

- **Swap the playbook index atomically while routing continues** — PERFORMANCE — value 4 — effort M — risk low — category: routing
  Why: The 10,000-playbook request needs routing to stay fast during rebuilds. Many queued ideas propose an index without saying how a rebuild avoids a half-written read. Assumption: readers should see either the old index or the new one, never a mix.
  Done when: routing 10,000 synthetic entries stays under 5 ms p95 while a rebuild runs in a loop, and no lookup ever returns a result from a partial index.

- **Ship a provenance attestation with every site deploy** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: The site publishes from `build` with no record tying the served files to a commit. The queued "show the live commit" idea displays it, but does not prove the bytes match.
  Done when: the deployed site serves an attestation file whose hashes match the built output and name the commit, and a changed file makes the check fail.

- **Require a hardware-key tap for destructive commands on marked paths** — SECURITY — value 3 — effort M — risk low — category: human approval
  Why: The quorum-of-checks idea uses model-side checks only. Nothing in the pack asks a human to confirm a destructive command with a second factor. Assumption: the user would accept one tap for rare dangerous actions.
  Done when: a guarded delete on a marked path blocks until a registered security key signs the request, and the request times out closed without a signature.

- **Expose the gate as an MCP tool any editor's agent can call** — FEATURE — value 4 — effort M — risk med — category: integrations
  Why: The gate is reachable only through Claude Code hooks, and the surfaces list has no MCP entry. Assumption: other agents would call a verdict tool instead of re-deriving whether a change passes.
  Done when: an MCP client lists a `gate_check` tool, and its verdict for a commit matches the output of `fm check` on the same commit.

- **Commit to the model's claimed result before the proof runs** — FEATURE — value 4 — effort M — risk low — category: integrity — wild
  Why: (wild) Commit-reveal: the model records a hash of its claimed pass before the check runs, so a test cannot be quietly edited to match a result after the fact. Assumption: tests get tuned to pass, and the record exposes that.
  Done when: a claim whose recorded hash differs from the check's actual output fails the close, and the failure names both hashes.

- **Turn each fixed bug into a generated property test** — FEATURE — value 4 — effort L — risk med — category: testing
  Why: The proof shows one example failing before the fix. One example can pass for the wrong reason. Assumption: a generator over the bug's input shape finds a case the example missed.
  Done when: for a fixed bug, a generator produces inputs that fail the pre-fix code and pass the fix, and the saved test is a property test that keeps running.

- **Score each codebase directory as a tabletop character** — FEATURE — value 2 — effort S — risk low — category: play — wild
  Why: (wild) Each directory gets hit points that rise with green gates and drop with reverted fixes. The delight lens asks for joy, and the pack shows recent Foreman work on game-like surfaces.
  Done when: `fm health` prints one score per directory, and a revert in a directory lowers that score on the next run.

- **Cut a model's loop when its output starts repeating itself** — PERFORMANCE — value 3 — effort S — risk low — category: cost control — wild
  Why: (wild) A run that repeats a sentence or a command several times is burning usage. Assumption: repetition shows up in the transcript early enough to stop it.
  Done when: a run that repeats the same tool call three times in a row is stopped, the stop is written to its journal, and a test feeds it a looping transcript.
