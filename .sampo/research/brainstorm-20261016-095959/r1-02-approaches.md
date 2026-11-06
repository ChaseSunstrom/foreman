# Brainstorm — lens: approaches

- **Orchestrate existing CLIs as workers under Foreman's loop (fm conduct)** — FEATURE — value 5 — effort M — risk low
  Why: `fm agents install` already reaches codex/gemini/opencode and builder lanes already drive `claude -p` in worktrees; a worker-adapter interface (claude, codex, gemini, opencode, aider) makes lanes model-agnostic with the least new code. Assumption: each CLI has a usable non-interactive mode.
  Done when: `fm lane run T-ID --worker NAME` runs a fake-CLI worker from a test fixture in a worktree, and the same task passes its gate with two different fake workers.

- **Build a native loop where the harness owns the phases and the model fills slots (fm code)** — FEATURE — value 5 — effort L — risk med
  Why: the planner note says discipline enforced by the harness is what lets small models succeed; Foreman already has intake, plan, evidence and gate verbs that today depend on Claude behaving. Assumption: slots (pick file, produce patch, name test command) can be schema-validated.
  Done when: with a scripted fake OpenAI-compatible server, `fm code "task"` goes intake→plan→edit→verify and closes a task with evidence, the model only ever returning JSON matching the slot schemas.

- **Ship a minimal OpenAI-compatible provider layer in stdlib (urllib)** — FEATURE — value 5 — effort M — risk low
  Why: the constraint is no new core deps and must work offline with Ollama, LM Studio, llama.cpp, vLLM, plus Anthropic/OpenAI/Gemini/OpenRouter. One chat-completions client with tool-call and JSON-mode fallbacks covers most of them.
  Done when: a test against a local stub server gets a streamed reply, a tool call, and a malformed-tool-call retry through `fmprovider`.

- **Route the Foreman guard as a local MCP/shim proxy for any tool-running agent** — SECURITY — value 4 — effort M — risk med
  Why: the guard is the thing that must never fail open; for CLIs without hook points (aider, plain shells) a PATH shim/exec wrapper applies the same guard. Assumption: such CLIs run commands via the shell.
  Done when: `fm guard shim -- sh -c 'rm -rf ~'` is refused, and a safe command runs, with the same verdicts as the hook on the guard_cases fixture.

- **Do less: first make `fm agents` live-verified and fix the blocked trio before anything new** — FIX — value 4 — effort S — risk low
  Why: T-0335, T-0336, T-0337 are blocked on codex/gemini/opencode being absent; the cheapest path to "works with other CLIs" is proving the existing adapters. Install them in a container and run roundtrip.
  Done when: roundtrip.py passes against real codex, gemini and opencode in a CI job, or each failure is recorded as a specific brief.

- **Capability-tiered slot sizing (small-model mode)** — FEATURE — value 4 — effort M — risk med
  Why: the user asked how small local models can be "super good". Probe the model with a few calibration prompts, then choose chunk size, single-file edits, constrained decoding via grammar/JSON schema, and more verification rounds.
  Done when: `fm model probe` writes a tier, and the same task under a fake weak model is split into more, smaller slots than under a strong one.

- **Make `fm code` an ACP/Zed-style server so editors and other harnesses drive it** — FEATURE — value 3 — effort M — risk med
  Why: Foreman already has `fm serve`, an MCP server and a web UI; speaking a standard agent protocol makes Foreman Code a backend, not another terminal app. Assumption: the protocol spec is stable enough.
  Done when: a scripted protocol client creates a session, sends a prompt, and receives streamed tool events from `fm code`.

- **Reuse by embedding: treat opencode or aider as the interactive shell and Foreman as the policy layer** — FEATURE — value 3 — effort S — risk low
  Why: building a polished TUI is huge; the opencode TS plugin already runs the guard in tool.execute.before. Trade-off: less control and UX depend on upstream.
  Done when: documented `fm code --shell opencode` launches opencode with the plugin, MCP and rules configured and a guarded command is refused.

- **Replayable deterministic transcripts for loop testing (fm code replay)** — CLEAN — value 3 — effort M — risk low
  Why: the user's tasks lean on fixtures, fakes and `fm replay` gates; recording model I/O makes a custom loop testable without a live model.
  Done when: a recorded session replays offline byte-identically and a changed phase prompt fails the replay.

- **Wild: Model tournament per slot — run the same slot on 3 cheap models and let the verifier pick** — FEATURE — value 3 — effort M — risk med
  Why: assumption: wild. Foreman already has gates and parallel lanes; running each slot on a local small model, a cheap API model and a strong one, taking the first passing, drives cost down automatically and records win rates per model.
  Done when: `fm code --race` closes a task using the first worker whose gate passes, and `fm usage` shows per-model win counts.

- **Wild: Distill Foreman's own history into a fine-tuning/few-shot set for local models** — FEATURE — value 3 — effort L — risk med
  Why: assumption: wild. Finished tasks with evidence, guard refusals and their rewrites (`fm guard mine`) are labelled traces of good discipline. Exporting them as redacted few-shot exemplars would make small models follow Foreman's habits.
  Done when: `fm teach export` writes a redacted JSONL of N passed tasks and a test confirms no secrets or absolute paths remain.

- **Wild: Cross-harness referee — one worker writes, a different vendor's model reviews** — FEATURE — value 4 — effort M — risk low
  Why: assumption: wild. The planned `fm audit run` with headless reviewers can pick a reviewer from a different CLI or model than the builder, decorrelating blind spots, which is a thing no single-vendor harness can offer.
  Done when: `fm audit run ID --reviewer codex` records lens verdicts from a fake codex and refuses a reviewer equal to the builder unless forced.

- **Wild: Harness-in-a-sandbox — run `fm code` in a disposable container/namespace so the guard is defense in depth** — SECURITY — value 3 — effort M — risk med
  Why: assumption: wild. Local small models plus bypass-style autonomy are riskier than Claude; a bubblewrap/podman wrapper bounds blast radius even if the guard misses.
  Done when: under `fm code --sandbox`, a test command writing outside the worktree fails while writing inside it succeeds.
