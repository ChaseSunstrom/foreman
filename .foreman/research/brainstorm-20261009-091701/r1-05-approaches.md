# Brainstorm — lens: approaches

- **Race competing approaches per task** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: Foreman runs one plan per task, but builder lanes in worktrees and `fm bench` already exist. Assumption: the plan gate is where a wrong approach is hardest to undo.
  Done when: `fm task new … --race 3` creates three lanes with different plan seeds, and `fm lane merge` lands only the lane with the best gate result and review score. The other two are removed with their reasons recorded.

- **Run mutation checks on the proof behind "done"** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: A criterion's verify command once ran no tests (`-k a or b` not read by run.py) and still passed. Recorded evidence is only as good as its bite. Assumption: a mutation tool such as mutmut or Stryker can run on the diff's lines.
  Done when: `fm task done` mutates the changed lines, re-runs the linked tests, and refuses a task whose tests all still pass after the mutations. A deliberately toothless verify command is caught in a test.

- **Run the edit-time test sentinel** — FEATURE — value 4 — effort M — risk low — category: feedback loop
  Why: T-0214 is deferred. `fm map` already has the tests→src links and PostToolUse is already a hook.
  Done when: after an Edit, the linked tests run in the background and a failure appears in the next turn's context within 30 s. A test covers it.

- **Detect drift between the brief and the diff** — FEATURE — value 4 — effort M — risk med — category: focus
  Why: Foreman's core promise is staying on task, but it checks focus only by task id. `fm oracle` already reads the spec without the code. Assumption: a cheap model call can compare the two.
  Done when: the done-gate flags changed hunks that no brief step or criterion explains, and a seeded unrelated edit is flagged in an eval.

- **Make cleanup a first-class gate** — FEATURE — value 4 — effort M — risk low — category: hygiene
  Why: The user said cleanup requests "never got done". `fm tidy` and `fm docs` exist but nothing ties them to the task that created the debt.
  Done when: finishing a task that replaces or removes behaviour scans for now-unreferenced symbols, stale docs and briefs, and opens a linked cleanup task or blocks. A fixture replacing a function shows the dead code reported.

- **Fuzz the guard against real bash, unattended** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: Bypasses keep arriving one at a time (`bash -lc`, symlink `rm`, `python -c`, T-0275 script files). The differential tests and the 5000-command replay already exist. Assumption: a grammar-based generator can feed `fm night`.
  Done when: `fm night` generates N shell commands per run, diffs the guard's verdict against a sandboxed real-bash effect check, and files each divergence as a task with the command that triggered it.

- **Capture evals from real failures automatically** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: T-0035 is deferred. `fm evals` and `fm bench` exist, but conversion is manual. Together with T-0217 (lesson confidence) this closes the learning loop.
  Done when: a blocked or failed task produces a redacted eval case with no manual step, and `fm bench` reports its pass rate over N runs.

- **Coordinate a fleet across projects** — FEATURE — value 4 — effort L — risk med — category: multi-project
  Why: Friction keeps coming from a downstream project (JARVIS): lanes landing during other tasks, idle sessions with 20+ queued. `fm projects`, `fm session` and the desktop app already show the whole fleet. Assumption: one conductor can use the shared budget and pace.
  Done when: one drive loop splits a shared token budget across two projects' queues and hands the next task to whichever session is idle. A ledger shows the allocation.

- **Run an adversarial red-team on "done" claims** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: Done rests on self-reported evidence. A specialist reviewer, tool-less beyond `fm check`, tries to produce a state where the recorded evidence still passes but the product is broken. `fm smoke` and `fm sentinel` are the base.
  Done when: for a sampled finished task, the red-team either produces a failing scenario that is saved as a regression case or reports a written "no break found".

- **Run speculative overnight lanes ("dream queue")** — FEATURE — value 4 — effort L — risk med — category: autonomy — wild
  Why: Assumption: at night the queue's deferred or planned tasks (T-0034, T-0214) can be built in lanes and left unmerged, with full proof attached.
  Done when: by morning each speculative lane has a branch, a gate result and a `fm pr` description. The user can accept with one command, and nothing touches main.

- **Replay a whole session against a candidate plugin** — FEATURE — value 3 — effort L — risk med — category: counterfactual — wild
  Why: `fm replay` covers guard commands only. Assumption: transcripts hold enough to re-drive prompts against a new Foreman version in a sandbox.
  Done when: a recorded session's user turns are replayed headlessly under a candidate hook set, and a report shows where the task outcome, cost or step count diverged.

- **Federate Foremen across machines** — FEATURE — value 3 — effort L — risk high — category: multi-machine — wild
  Why: The ambition names multi-machine work. `fm serve` and the MCP server already expose state. Assumption: machines can reach each other over a private tunnel.
  Done when: a task on machine A can be claimed by Foreman on machine B, run in its own lane, and merged back with the evidence attached. Briefs sync via `fm sync`.

- **Do less: derive lessons from the ledger instead of a store** — CLEAN — value 3 — effort S — risk low — category: simplification
  Why: The cheapest way to reach confidence-weighted lessons (T-0217) is to compute them from existing ledger events, not to add storage. The trade-off is slower recall.
  Done when: `fm recall` ranks lessons by whether recall preceded a first-time pass, using only existing ledger data, with no new file format.

- **Write a test-first contract compiler from the brief** — FEATURE — value 3 — effort M — risk med — category: planning — wild
  Why: `fm oracle` already extracts behaviour examples and ambiguities from the spec alone. Assumption: those examples can become executable tests before the code exists.
  Done when: a FEATURE task starts with failing tests derived from the oracle examples, and the red→green pair is recorded as proof.
