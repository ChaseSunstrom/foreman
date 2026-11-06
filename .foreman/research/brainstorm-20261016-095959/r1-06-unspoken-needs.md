# Brainstorm — lens: unspoken needs

- **Ship a provider-neutral model adapter with a local-model slot-filling loop** — FEATURE — value 5 — effort L — risk med — category: harness core
  Why: the planner notes say the user wants small local models to be "super good" and Foreman to enforce discipline itself. The unspoken need is that the harness, not the model, owns intake→plan→execute→verify, and the model only fills small structured slots. Assumption: an OpenAI-compatible HTTP client in stdlib (urllib) is enough for Ollama, LM Studio, llama.cpp and vLLM.
  Done when: `fm code "add a --days flag"` finishes a fixture task against a stub OpenAI-compatible server returning only JSON slot fills, and the task closes with evidence logged.

- **Run the existing guard inside Foreman's own tool executor** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: the guard is the product's trust anchor (T-1194, T-1195, T-1204 are all recent guard work), and today it lives in hooks of other harnesses. A native loop that calls `fmguard` before every tool call gets the same refusals with no hook layer, and it must never fail open. Assumption: fmguard can be called as a library without the hook process.
  Done when: a test feeds the labelled cases in `plugin/tests/fixtures/guard_cases.jsonl` through the native executor and every refusal is reproduced, including when the guard module raises (the call is refused).

- **Treat claude, codex, gemini, opencode and aider as interchangeable workers behind one driver interface** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: builder lanes only use `claude -p` today, while `fm agents install` already reaches three other CLIs. T-0335/T-0336 are blocked on live verification, so the unspoken need is one lane runner that picks a worker by availability and cost. Assumption: each CLI has a usable headless mode.
  Done when: `fm lane run T-X --worker NAME` works for two different fake CLIs on PATH, and the lane result is merged and verified identically.

- **Route each step to the cheapest model that passes, and learn the routing from outcomes** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: pillar 1 asks for "the cheapest model that can", and T-0217 (lesson confidence) shows the user wants measured, not guessed, behaviour. Assumption: first-time pass rate per model and task type is already derivable from the ledger.
  Done when: after seeded history shows a local model failing a task type three times, `fm route T-X` names a stronger model for it and prints the pass rates it used.

- **Run a conformance suite that scores any model or CLI as a Foreman worker** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: T-0035 (eval capture) and T-0866 (bench vs plain Claude) are deferred for lack of cases. The user can't claim "better than CC" or "works with small models" without a number. Assumption: the redacted-case corpus can double as the fixture set.
  Done when: `fm bench --worker NAME` prints a held-rate, guard-violation count and cost for a fixture corpus, and fails on a worker that skips a required proof step.

- **Make every session resumable and portable between workers** — FEATURE — value 4 — effort M — risk med — category: continuity
  Why: T-0798 (recovery, transcript repair) is deferred, and mixed workers make crash-and-switch likely, such as a rate-limited Claude moving to a local model. Foreman state is already file-based via `fm`. Assumption: task brief, evidence and focus are enough to rebuild context without the transcript.
  Done when: killing a lane mid-task and running `fm lane resume --worker other` continues from the last checkpoint and closes the task.

- **Show a plain-language "why this model, why this step" trace in the web UI** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: T-0795 (close-out legibility) and the user's steady stream of receipt-style tasks suggest they want to see why a harness decision was made, especially with many workers. Assumption: the web UI can read the ledger events.
  Done when: the task page lists each step with the worker, the cost and the gate result.

- **Replay any past session through a different model** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: `fm replay` and `fm guard mine` already replay guard cases, and the user wants proof that Foreman beats plain CC. Re-running a closed task's brief on another worker gives a head-to-head with no new cases. Assumption: brief and acceptance command are stored per task.
  Done when: `fm replay T-X --worker local` runs the brief in a scratch worktree and reports pass/fail against the original `DONE-WHEN`.

- **Wild: Let a weak model ask a strong one only when stuck** — FEATURE — value 4 — effort M — risk med — category: escalation
  Why: wild. Assumption: the loop can detect stuck states (repeated guard refusal, the same failing test three times) and make one capped call to a stronger model for a hint, not for the work.
  Done when: a stub small model that loops on one failure triggers exactly one escalation call, logged with its cost, and the task finishes.

- **Wild: Self-hosting, where `fm code` builds Foreman's next release with a local model overnight** — FEATURE — value 4 — effort L — risk high — category: dogfood
  Why: wild. The queue is full of small, well-specified S/M briefs with `DONE-WHEN` lines, which are ideal slot-filling targets. Assumption: the simplest briefs (e.g. T-1203, T-1208) are within a local model's reach.
  Done when: a local-model run closes at least one real S brief from the queue with the full gate green and a human-readable receipt in the morning.

- **Wild: Pair-programming mode where two different models must agree before a commit** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: wild. Cross-model review catches errors a single model's blind spots share, and `fm-reviewer` findings are already parsed into events. Assumption: reviewer lenses can run on a different worker than the builder.
  Done when: a commit is blocked in a test when the second worker's reviewer logs a blocking finding, and allowed when it logs none.

- **Detect the missing CLI and say how to get it, instead of failing** — FIX — value 3 — effort S — risk low — category: setup
  Why: codex and gemini aren't installed here, and T-0336/T-0337 are blocked on exactly that; the `--until "when CMD succeeds"` request shows the user hits this repeatedly. Assumption: `fm doctor` can check each worker's presence and login.
  Done when: `fm doctor` lists each worker as ready, missing or unauthenticated, with one install line for each missing one, and the blocked tasks unblock when the command appears.

- **Give the new harness a name and a first-run path that works with no Claude account** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: "Foreman Code" must stand alone, yet the README frames Foreman as a layer for Claude Code. T-0862/T-0863 (tour, start ladder) are deferred pending first-run evidence. Assumption: someone with only Ollama installed is a target user.
  Done when: on a machine with only a stub local server, `fm code --init` detects it, runs a demo task and exits 0 without any Anthropic credential.
