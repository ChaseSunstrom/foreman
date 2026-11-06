# Brainstorm — lens: bold bets

- **Build `fm code`: Foreman's own agent loop with model-filled slots** — FEATURE — value 5 — effort L — risk high — category: harness core
  Why: the planner note says a deterministic intake→plan→execute→verify loop where the model only fills small structured slots is what lets small models succeed; the request is "Foreman Code". Assumption: a JSON-schema slot protocol works over plain OpenAI-compatible chat, with no native tool calling needed.
  Done when: `fm code "add --days flag"` against a stub OpenAI-compatible server returning canned slot JSON creates a brief, edits a file, runs the gate and closes the task with evidence, with no `claude` binary on PATH.

- **Add a provider layer for any OpenAI-compatible endpoint** — FEATURE — value 5 — effort M — risk med — category: models
  Why: the constraints list Ollama, LM Studio, llama.cpp, vLLM, Anthropic, OpenAI, Gemini and OpenRouter with stdlib only. Assumption: `urllib` plus SSE parsing is enough for streaming.
  Done when: `fm code --model ollama:qwen3` and `--model anthropic:...` both pass the same loop test against fake servers, with zero third-party imports (checked by an import-scan test).

- **Make the guard the single tool executor for every worker** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: the user wants Foreman to enforce discipline itself rather than rely on inconsistent agents. Today the guard runs as a hook inside each host. In `fm code`, every Bash/Edit call goes through `fmguard` before it runs, so it can't fail open by construction. Assumption: `fmguard` exposes a callable that doesn't depend on hook stdin.
  Done when: a test feeds the loop a refused command (the labelled guard_cases corpus) and it is never executed, with the refusal returned to the model as the tool result.

- **Run claude, codex, gemini, opencode and aider as interchangeable lane workers** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: builder lanes only drive `claude -p` today. `fm agents install` already reaches the other three CLIs, and T-0336 notes they are unverified live. Assumption: each CLI has a headless prompt mode that can be wrapped behind one adapter interface.
  Done when: `fm lane start T-x --worker codex` runs against a fake `codex` shim on PATH and the lane merges with the same evidence checks as a claude lane.

- **Route each step to the cheapest capable model from measured pass rates** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the pillar says "cheapest model that can", and `lens_rates` plus held-rate stats already exist (T-0829). Assumption: per-task-type pass data is recorded per model.
  Done when: `fm code --route auto` picks a local model for a CLEAN brief and escalates to a stronger one after two failed gates, shown in the event log.

- **Add a model capability probe that tunes the harness to the model** — FEATURE — value 4 — effort M — risk low — category: small models
  Why: the user asked how small local models could be "super good". Assumption: a short probe battery (JSON validity, edit-format accuracy, long context) can set slot size, retries and the edit format (whole file, search/replace or diff).
  Done when: `fm code probe --model X` writes a profile file, and a later run reads it and changes the edit format for a model that failed the diff probe.

- **Add edit-by-structured-slot with automatic repair** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: small models break edit formats. The harness validates each slot, applies it to a scratch copy, runs the syntax check, and re-asks with the exact error. Assumption: tree-sitter isn't needed, since `ast`/`compile` and per-language syntax commands cover the first languages.
  Done when: a fake model returns a malformed edit twice and then a good one, and the loop's log shows two repairs and a clean apply.

- **Replay any session against a different model (wild)** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: assumption: `fm replay` and the guard corpus give you recorded briefs and tool traces. Re-running the same brief on model B and diffing its evidence against model A's turns "better than CC" into a measurement (T-0866 bench vs plain Claude).
  Done when: `fm code replay T-x --model Y` produces a side-by-side verdict table (gate pass, turns, tokens, cost) from a recorded task.

- **Make a model tournament lane (wild)** — FEATURE — value 3 — effort L — risk med — category: lanes
  Why: lanes already run in parallel worktrees. Assumption: gates give an objective winner. The same brief goes to three different models or CLIs, and the first to pass the gate and audit merges while the others are discarded.
  Done when: `fm lane race T-x --workers a,b,c` merges exactly one lane, whose gate is green, and records the loser lanes' outcomes.

- **Serve Foreman Code as an MCP and ACP server so other editors drive it** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: an MCP server already exists, and Zed and other editors speak ACP. Assumption: the loop can stream events as JSON-RPC. This makes Foreman a harness that other tools plug into, not only the reverse.
  Done when: a scripted ACP client sends a prompt and receives streamed tool-call and result events plus a final evidence summary.

- **Show a live web-UI session view for the native loop** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: `fm serve` and a web UI already exist and the pillars require motion that explains state. The native loop emits a typed event stream rendered as stage rail, tool tree and gate lights. Assumption: the existing event log can be tailed over SSE.
  Done when: opening the page during a `fm code` run shows each stage change within 1 s, and a screenshot test captures the idle, running and failed states.

- **Make a crash-proof loop that resumes from its last checkpoint (wild)** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: the native loop owns its state, so every slot result is checkpointed through `fm`. Killing the process at any step and running `fm code --resume` continues without redoing finished steps, which T-0798 recovery hints at. Assumption: slot calls are idempotent given the stored inputs.
  Done when: a test SIGKILLs the loop after step 2 of 4 and resume completes steps 3–4 only, with no duplicate edits.

- **Offer a one-command local-model setup that downloads nothing silently** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: codex and gemini aren't installed on this machine, and users with Ollama need zero-config. `fm code doctor` detects local servers on the common ports, lists models and prints the exact `--model` flag. Assumption: probing localhost is acceptable and sends nothing out.
  Done when: with a fake server on port 11434, `fm code doctor` lists its models and exits 0, and with none running it prints install hints and exits 1.

- **Let the harness pair a small model with a big one only at stuck points (wild)** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: assumption: the stuck detector already exists in the drive hook. The local model does the routine work, and after N failed gate attempts the loop sends one compact packet (brief, failing output, relevant lines) to a frontier model for a hint, and logs the spend against `fm budget`.
  Done when: a test with a failing stub model triggers exactly one escalation call after N failures, and the cost shows in `fm budget`.
