# Brainstorm — lens: simplicity

- **Collapse the three plans into one `fm code` verb with a `--worker` switch** — FEATURE — value 5 — effort M — risk low — category: simplicity
  Why: the ideas list holds native loop, conduct, and worker interfaces as separate things; the planner's "both" question is easier as one verb where `--worker native` is the built-in loop and `--worker 'CMD template'` shells out.
  Done when: `fm code BRIEF --worker native` and `fm code BRIEF --worker 'claude -p {prompt}'` both reach the same gate and write the same evidence file shape, checked by one test with a fake model and a fake CLI.

- **Add a zero-config first run that picks a model from what is already on the machine** — FEATURE — value 5 — effort S — risk low — category: onboarding
  Why: codex and gemini are not installed here, so the user's own machine shows the missing-CLI case; assumption: users would rather not write a provider file first.
  Done when: with only an Ollama port open and no keys set, `fm code "task"` names the endpoint it found, runs, and with nothing found prints one line naming the single next step.

- **Reuse `fm run` as the loop's outer shell instead of writing a new queue runner** — CLEAN — value 4 — effort S — risk low — category: reuse
  Why: `fm run` already is a headless queue worker over `claude -p` lanes; swapping the spawned command for the worker template avoids a second scheduler.
  Done when: `fm run` and `fm code` share one function that spawns a worker, and deleting the duplicate path leaves the existing run tests green.

- **Cut the native tool set to what the guard already understands** — CLEAN — value 4 — effort S — risk low — category: scope
  Why: the guard parses Bash and Edit; a tool list of read, search, edit, run, finish adds no new surface to defend. Assumption: no tool outside those five is needed for the first release.
  Done when: the native loop rejects any tool name outside the five, and the guard test corpus runs unchanged against it.

- **Make the model profile a plain file with defaults for unknown models** — FEATURE — value 3 — effort S — risk low — category: config
  Why: the user wants small local models to be "super good", which needs a knob for weak ones; an unknown model should get the strictest slot settings rather than an error.
  Done when: an unlisted model name runs with small-slot defaults, and a test shows a profile edit changes the slot size.

- **Delete adapter code that the worker template makes redundant** — CLEAN — value 3 — effort M — risk med — category: pruning
  Why: `fm agents install` carries per-tool glue, and T-0794 already lists "retire adapters"; assumption: only the guard-hook install survives, since the guard is the part that needs a hook.
  Done when: the adapter count drops, the guard install for codex, gemini and opencode still passes its tests, and the doc table matches.

- **Print one status line per step instead of a TUI** — FEATURE — value 3 — effort S — risk low — category: output
  Why: the existing web UI and stdout already exist; a line like `plan ok · edit 2 files · gate red` needs no new surface.
  Done when: a run on a fake model prints exactly one line per phase and the same events appear in `fm serve`.

- **Fail with the exact command to run when a prerequisite is missing** — FIX — value 4 — effort S — risk low — category: errors
  Why: T-0335 to T-0337 are blocked on tools absent here, and T-1208 shows a criterion that names a nonexistent test module and fails confusingly.
  Done when: running with a missing worker CLI or a nonexistent verify module exits non-zero with a message naming the missing thing and the fix.

- **Wild: Make the whole harness one stdlib file that regenerates itself from the repo** — FEATURE — value 3 — effort L — risk med — category: packaging
  Why: wild; assumption: a copyable single file lets someone try Foreman Code on a server with only Python, with the plugin tree being the source of truth.
  Done when: `fm code --bundle out.py` writes a file that, on a clean machine with only Python 3, completes the fake-model demo task.

- **Wild: Let the brief itself be the whole config** — FEATURE — value 3 — effort M — risk med — category: config
  Why: wild; model, worker, budget and gate could live in the brief's frontmatter, so a task is one file that runs the same anywhere and no settings screen is needed.
  Done when: a brief naming its own worker and budget runs under `fm code` with no other flags and no global settings read.

- **Wild: Ship a "do nothing" dry mode that proves the harness works with no model at all** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild; a scripted stub model replaying a fixture gives users and CI a one-command proof that intake, guard, gate and evidence are wired, with no keys.
  Done when: `fm code --selftest` runs a canned task end to end offline in under ten seconds and exits 0.

- **Hold the first release to one provider call shape** — FEATURE — value 4 — effort S — risk low — category: scope
  Why: the pack constraints say OpenAI-compatible HTTP covers Ollama, LM Studio, llama.cpp, vLLM and OpenRouter; native Anthropic and Gemini can arrive later as shims.
  Done when: one urllib client passes tests against a local fake server, and no provider-specific branch exists in the loop.
