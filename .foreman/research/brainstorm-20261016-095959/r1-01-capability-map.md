# Brainstorm — lens: capability map

- **Build `fm code`, a provider-agnostic agent loop in stdlib Python** — FEATURE — value 5 — effort L — risk med — category: core harness
  Why: the ask is "Foreman Code". Foreman today only wraps `claude -p` and plugin hooks. Aider, Codex CLI, opencode and Crush all own the loop, and that is what lets them run any model. Assumption: stdlib `urllib` streaming is enough.
  Done when: `fm code "add X"` against a fake OpenAI-compatible server runs a multi-turn tool loop (read, edit, bash) and ends with a closed task and evidence.

- **Drive the loop deterministically, with the model filling small slots** — FEATURE — value 5 — effort L — risk med — category: small models
  Why: the planner notes say the user wants even small local models to be "super good", with the harness enforcing discipline. The harness would own intake→plan→execute→verify, and the model would only emit schema-checked JSON for each step (files to touch, the edit, the verify command).
  Done when: a scripted 7B-class stub that returns only slot JSON completes a fixture task, and a malformed slot is rejected and retried without the loop leaving its stage.

- **Add a tool-call shim for models without native function calling** — FEATURE — value 4 — effort M — risk med — category: model compat
  Why: Ollama, llama.cpp and LM Studio models vary widely in tool-call support. Best-in-class harnesses fall back to text protocols or grammar-constrained JSON. Assumption: the local servers expose JSON-schema or GBNF constraints.
  Done when: the same task passes against a stub that supports native tools and one that supports only plain text, through the same tool layer.

- **Offer an edit-format ladder (whole file, search/replace, unified diff) chosen per model** — FEATURE — value 4 — effort M — risk low — category: edit quality
  Why: aider's measured gains come from matching edit format to model. Foreman already has `fm edit` and `fm lease`, so formats can route through the existing guard and lease path.
  Done when: one fixture edit applies correctly in all three formats, and a failed search block returns a specific error and a retry.

- **Add a model registry with routing, fallback and cost ledger** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the pillars say "cheapest model that can", and `fm budget` already exists. Add a table of providers (Anthropic, OpenAI, Gemini, OpenRouter, local), a per-stage model, fallback on error or rate limit, and per-task token and dollar totals.
  Done when: a stub provider that returns 429 triggers fallback to the second model, and `fm budget` shows the spend split by model.

- **Make external CLIs interchangeable workers behind one `fm worker` interface** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: the pack's design question offers orchestrating CLIs as an option. Lanes today hard-code `claude -p`. Define a spec (command, how the brief is passed, how output and exit are read, how the diff is collected) for claude, codex, gemini, opencode and aider. T-0336 is blocked on live verification.
  Done when: a lane runs the same fixture brief through two fake CLI workers and both diffs land through the same merge gate.

- **Add an MCP client and server host with per-tool guard policy** — FEATURE — value 3 — effort M — risk med — category: integrations
  Why: Foreman ships an MCP server but the pack shows no client. Claude Code, Codex, Gemini and opencode all consume MCP, so `fm code` needs it to match them. The guard must also cover MCP tool calls.
  Done when: `fm code` calls a stub MCP tool, and a call the guard denies is refused and logged.

- **Speak Agent Client Protocol so editors can host `fm code`** — FEATURE — value 3 — effort M — risk med — category: IDE
  Why: Zed and other editors use ACP to host any agent, which gives IDE reach without per-editor extensions. Assumption: ACP is stable enough to target.
  Done when: a scripted ACP client initializes a session, sends a prompt, and receives streamed updates and a permission request.

- **Run bash and edits in an OS sandbox (bwrap or Landlock) in addition to the guard** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: the guard is regex and parsing, and the recent commits are all guard corner cases (heredocs, `python -c`, `git checkout`). Codex's sandbox is the stronger model. A small local model raises the odds of bad commands. The sandbox must fail closed.
  Done when: a command that writes outside the worktree fails under the sandbox even when the guard is bypassed in a test.

- **Support session checkpoints, rewind and resume in `fm code`** — FEATURE — value 4 — effort M — risk low — category: sessions
  Why: Claude Code and others offer rewind and `--resume`. Foreman already has `fm release --resume` checkpoints and T-0798 (recovery) deferred. Snapshot the conversation and worktree per step.
  Done when: killing `fm code` mid-task and running `--resume` continues from the last step, and `rewind N` restores the files as well.

- **Add a context manager with a repo map, compaction and prompt caching** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: small-context local models need aider-style repo maps and summarization. `fm map` and the stack cards are already in the repo. Prompt caching helps cost on Anthropic and OpenAI.
  Done when: on a 200-file fixture with an 8k-token model limit, the loop completes with the prompt under limit, and its compaction events appear in the log.

- **Wild: Add a race mode that runs one brief on three different models in parallel lanes and merges the one that passes the gates** — FEATURE — value 4 — effort M — risk low — category: ensembles
  Why: wild. Worktree lanes and gates already exist, and the evidence checks decide the winner with no model judging. It also builds a per-model scoreboard.
  Done when: a brief with three stub workers merges only the one whose verify command passes, and the other two lanes are discarded with the reason recorded.

- **Wild: Derive a per-model capability profile from past task evidence and tighten the harness for weak models** — FEATURE — value 4 — effort M — risk med — category: adaptive
  Why: wild. `fm bench` and the lesson and confidence ideas (T-0217) exist. A weak model automatically gets smaller steps, stricter slots and more checks, and a strong model gets looser ones.
  Done when: after a seeded history where model A fails multi-file edits, `fm code` with model A splits a two-file task into two steps and model B does not.

- **Wild: Add a "fm code --teach" mode where a strong model writes the plan and slot templates once and a free local model executes them offline** — FEATURE — value 3 — effort L — risk high — category: hybrid
  Why: wild. It serves the offline and cheap goals: the expensive model is paid for once per task shape and cached as a playbook, and the local model replays it.
  Done when: a plan generated by a stub strong model is saved, then executed with the network disabled by a stub local model to a passing gate.

- **Add headless and SDK entry points with JSON event streaming** — FEATURE — value 3 — effort S — risk low — category: automation
  Why: Claude Code, Codex and Gemini all have non-interactive modes with JSON output. `fm run` and `fm serve` already exist, so `fm code --json` can feed the web UI and CI.
  Done when: `fm code --json "task"` emits one JSON line per event, and the web UI renders a run from that stream alone.
