# Brainstorm — lens: bold bets

- **Grade closed work by whether it survived** — FEATURE — value 5 — effort M — risk low — category: self-measurement
  Why: assumption: every score so far (hint hit rate, first-time pass, interventions) is judged at close, when it is cheapest to look good. Nothing checks what happened to the code afterward.
  Done when: `fm survive T-xxxx` reports the share of that task's added lines still in HEAD after 14 days. It flags tasks whose lines were touched by a later fix or revert commit, and `fm learn` lowers the trust of lessons tied to those tasks.

- **Compile each steer into a backtested checker** — FEATURE — value 5 — effort M — risk med — category: enforcement
  Why: the user keeps restating layout rules ("no gaps", "fills the dock", "no scaling issues"), and "Corrections become rules" only promotes text. Assumption: a sentence can become a deterministic predicate (a test or hook check) if it is first run against past ledger and transcript data.
  Done when: `fm steer compile "<sentence>"` writes a predicate plus a fixture. It reports false-positive and false-negative counts over the last 30 days of recorded sessions, and refuses to enable it above a set false-positive rate.

- **Answer your own asks from the user's past answers** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user said they "shouldn't need to ask for any of it", and `fm ask` interrupts them. Assumption: asks recur in a fingerprintable shape (kind, files, option set).
  Done when: replaying the last 50 recorded asks shows the predictor's precision at its confidence threshold. Above the threshold `fm ask` proceeds and prints "assumed X (91%, from T-0412)". A later contradiction by the user lowers that fingerprint's confidence.

- **Treat every interrupt as a labelled mistake** — FEATURE — value 4 — effort S — risk low — category: learning
  Why: the pack shows mostly typed corrections, but an ESC or a mid-turn message is the strongest "stop doing that" signal and nothing records it. Assumption: interrupts are detectable from the transcript's interrupted-request marker.
  Done when: `fm learn` lists interrupts per task with the 3 tool calls just before each. Three similar interrupts propose a veto or lesson.

- **Forge tools from repeated command sequences** — FEATURE — value 4 — effort M — risk med — category: self-extension
  Why: `plugin/templates/mcp-server/` (server.py, test_server.py) already exists as a scaffold. Assumption: Bash sequences repeat across sessions in matching shapes, such as the same curl/jq chain or the same 4-step gate.
  Done when: after 3 matching sequences, `fm forge` drafts a project-local script or MCP server from the template, with a passing test. It registers in `.mcp.json` only after a yes.

- **Prove the guard on a bounded exhaustive grammar** — SECURITY — value 4 — effort M — risk low — category: provable safety
  Why: the guard has known false positives and open work T-0275 on script contents. Fuzzing is already planned, but nothing states invariants. Assumption: wrapper and flag variants (sudo, env, `bash -c`, `$(…)`, base64 pipes, path spellings) can be enumerated.
  Done when: `fm guard prove` generates tens of thousands of commands from the grammar and checks declarative properties such as "no recursive delete outside the root is allowed". It writes a safety-case file and fails `fm doctor` on any counterexample.

- **Send a break-it adversary before close** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: reviewers read the diff, but only a failing input proves a hole. Assumption: a headless child rewarded only for a failing input finds more than a reader does.
  Done when: for M/L tasks, a read-only lane gets the diff and 10 minutes, and returns a runnable failing command or "none found". A found failure blocks the close until the failure is fixed or waived.

- **Check changed pure functions with generated properties** — FEATURE — value 3 — effort M — risk med — category: formal verification
  Why: assumption: type hints and docstrings give enough for Hypothesis (or CrossHair where installed) to generate properties on small pure functions. The evidence grade would be "property-checked", above "test passed".
  Done when: a FIX task touching a typed pure function records a property run with a seed in its evidence, and the grade shows in `fm task show`.

- **Garden every repo overnight with proven-safe chores** — FEATURE — value 4 — effort M — risk med — category: initiative
  Why: `fm night` runs fixed jobs and the queue only moves when the user adds work. Assumption: patch-level dependency bumps, stale-branch pruning and lint autofixes are safe when gated by the repo's own tests.
  Done when: `fm night --garden` leaves one branch per chore, each with a green gate receipt. Nothing is merged, and the morning digest lists them with a one-key accept.

- **Wild: Run a twin of the user against Foreman** — FEATURE — value 4 — effort L — risk med — category: simulation
  Why: wild; the user's steers are a rich persona (dense, filled, no gaps, one panel). Assumption: a `claude -p` child prompted with the last 30 steers can act as the user in a scripted 2-turn loop with a builder.
  Done when: `fm twin run T-xxxx` returns the twin's list of complaints about the result. Before a UI close, its objections are shown next to the diff.

- **Wild: Run a bid market between subagents with calibration scores** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: wild; the planned work routes by price and past pass rate but never asks the agent. Assumption: a haiku, sonnet or opus child can emit a one-line bid of tokens, minutes and confidence for a step.
  Done when: `fm bid` records bids and outcomes and reports a Brier score per model per step type. Dispatch picks the lowest calibrated cost that meets a confidence floor.

- **Wild: Bisect the harness itself** — FEATURE — value 3 — effort M — risk low — category: self-debugging
  Why: wild; every rule, hint and hook change is already a commit. Assumption: recorded hook stdin can replay against any older rules commit.
  Done when: `fm bisect-rules <session>` names the rule or hook commit where a bad decision first appeared. It replays the recorded events against a binary search of the rules history and prints the commit.
