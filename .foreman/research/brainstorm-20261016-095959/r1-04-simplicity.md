# Brainstorm — lens: simplicity

- **Ship `fm code` as a ~400-line loop over one OpenAI-compatible HTTP call** — FEATURE — value 5 — effort L — risk med — category: harness core
  Why: the ask is "Foreman Code"; constraints say stdlib Python, Ollama/LM Studio/vLLM/Anthropic/OpenAI/OpenRouter all speak or bridge to chat-completions. Simplicity: one adapter, one loop, and the existing guard, evidence and task state do the rest.
  Done when: with a fake local HTTP server returning a scripted tool call, `fm code "task"` edits a file, the guard is invoked before the edit, and the task closes with evidence.

- **Make the model fill slots, not drive: fixed intake→plan→edit→verify state machine** — FEATURE — value 5 — effort L — risk med — category: harness core
  Why: the planner note says small models succeed when the harness is deterministic and the model only fills small structured slots; the user asked for small models to be "super good". Fewer model decisions means fewer failure modes.
  Done when: a test with a stub model that only emits JSON for each slot (plan, one-file edit, verify command) completes a fixture task, and a malformed slot reply is re-asked at most N times then fails cleanly.

- **Reuse the existing guard in-process as the only tool gate** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: the guard is a mature asset (many recent T-1194..T-1204 commits); a new loop must not grow a second policy. Assumption: fmguard is importable as a function.
  Done when: every tool call in `fm code` passes through one `guard.check()` call, and a test shows a denied command never reaches subprocess, including when the guard raises (fails closed).

- **Limit the tool set to five: read, search, edit, run, finish** — FEATURE — value 4 — effort S — risk low — category: tools
  Why: small models degrade with big tool menus; Foreman already has fm verbs for everything else, exposed via `run`.
  Done when: the tool schema sent to the model lists exactly five tools, and a fixture task completes using only them.

- **Treat other CLIs as workers via one `--worker CMD` template, not per-tool adapters** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: `fm agents install` already covers codex/gemini/opencode, while lanes already drive `claude -p`; T-0336 shows live verification is blocked anyway. A command template with `{brief}` and `{cwd}` covers aider and anything else with no new code per tool.
  Done when: `fm lane run --worker 'aider --message-file {brief}'` runs a fake worker script in a worktree and the lane merge proceeds as with claude.

- **Define the worker contract as "exit code + diff + evidence file"** — CLEAN — value 4 — effort S — risk low — category: orchestration
  Why: orchestrating many CLIs only stays simple if Foreman judges the result itself with gates rather than parsing each tool's output.
  Done when: swapping two different fake workers yields identical close behaviour, judged only by the gates.

- **Make the model profile a single TOML of three numbers (context, tools-ok, json-ok)** — FEATURE — value 3 — effort S — risk low — category: models
  Why: local models differ mainly in context and structured-output reliability; one tiny profile selects prompt size and slot mode instead of per-model code. Assumption: no profile system exists yet.
  Done when: `fm code --model X` reads the profile, and a profile with `json-ok=false` switches to a line-based slot format in a test.

- **Do less: ship `fm code` without a TUI, streaming to the existing web UI and plain stdout** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: the pack shows a web UI surface and a heavy TUI mod (T-0166, T-0418 pain); a new terminal UI doubles the surface.
  Done when: `fm code` prints one line per step to stdout and the same events appear in `fm serve` with no new UI code.

- **Add a `fm code --dry-plan` that prints the plan slots and stops** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: cheap way to compare models and verify the loop without edits.
  Done when: the command exits 0 and prints a plan without touching the worktree (checked by a clean git status in a test).

- **Cap the loop by a fixed step and token budget from `fm budget`** — RELIABILITY-as-FIX — FIX — value 4 — effort S — risk low — category: reliability
  Why: budget and contract verbs exist; a local model looping forever is the most predictable failure.
  Done when: a stub model that never finishes is stopped at the cap with a recorded "budget" reason and a nonzero exit.

- **Wild: run the whole agent as a replay-able log, so any session can be re-executed against a different model** — FEATURE — value 4 — effort M — risk med — category: eval (wild)
  Why: assumption: `fm replay` and the guard corpus already show Foreman values recorded, replayable cases. A session log of slot calls turns every real task into a model benchmark (T-0866).
  Done when: `fm code --replay LOG --model B` re-runs the recorded task's slots and reports pass/fail versus the original.

- **Wild: model ladder, try the cheapest local model first and escalate to a bigger one only when a gate fails** — FEATURE — value 4 — effort M — risk med — category: cost (wild)
  Why: pillar 1 already says "cheapest model that can"; the gate result is an objective escalation trigger and needs no judgement.
  Done when: a test with a failing small stub and a passing large stub shows the task closing on the second model and the log naming both.

- **Wild: one-file agent, `fm code` is a single-file script that can be copied onto any machine and run with only Python** — FEATURE — value 3 — effort M — risk med — category: portability (wild)
  Why: stdlib-only and offline are stated constraints; a vendorable single file makes Foreman usable on a box with a local model and nothing else.
  Done when: copying the one file to an empty directory and running it against a fake server completes a toy task.
