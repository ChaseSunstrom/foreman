# Brainstorm — lens: approaches

- **Run Claude Code on any model through a local gateway** — FEATURE — value 5 — effort M — risk med — category: providers
  Why: the ask is "better than CC that works with other models", and Foreman already is the CC plugin with the guard, drive and UI mod. A stdlib `fm gateway` that speaks the Anthropic Messages API on localhost and translates to OpenAI-compatible, Ollama or Gemini endpoints gives that without writing a new loop. Assumption: Claude Code honors a base-URL override and tool-call translation is good enough.
  Done when: with `ANTHROPIC_BASE_URL` pointed at `fm gateway` and a fake OpenAI-compatible server behind it, a scripted `claude -p` prompt completes one tool call round trip and the test sees both translated requests.

- **Use installed CLIs as completion providers** — FEATURE — value 4 — effort M — risk med — category: providers
  Why: this differs from running CLIs as whole-task workers. `claude -p`, `codex exec` and `gemini -p` become a plain text backend for slot filling in `fm code`, so it needs no API key and works on the user's existing logins. Assumption: this is permitted under each vendor's terms, which the first-run notice should state.
  Done when: `fm code --provider cli:claude` fills one plan slot through a fake `claude` on PATH and logs the call in the cost ledger with a cost of unknown.

- **Judge the diff, not the process** — SECURITY — value 4 — effort M — risk low — category: admission control
  Why: hookless CLIs can't be gated before each call (T-0337: Gemini's Stop isn't wired). Run any worker in a throwaway worktree and admit only a diff that passes path policy, secret scan and the gate, reverting the rest. This gives a guarantee even where no hook exists.
  Done when: a fake worker that edits `.env` and a file outside its lease gets those hunks stripped and reported, while an in-lease edit lands.

- **Constrain slot decoding with grammars** — PERFORMANCE — value 4 — effort S — risk low — category: small models
  Why: the earlier ideas repair malformed slots after the fact. Passing a JSON schema to Ollama `format`, llama.cpp GBNF or vLLM `guided_json` makes invalid output impossible and cuts retries on small models.
  Done when: against a fake endpoint that records its request body, every slot call carries the schema field for that backend, and a backend without support falls back to validate-and-repair.

- **Define the harness as an editable workflow file** — FEATURE — value 4 — effort M — risk med — category: extensibility
  Why: `plugin/workflows` exists, and the intake→plan→execute→verify phases are fixed in code. A TOML or YAML state machine of phases, slot schemas, gates and escalation rules lets users and weak-model profiles change the harness without touching Python.
  Done when: swapping in a workflow file with an extra "review" phase makes `fm code --dry-plan` list that phase, and an invalid file is rejected with the line number.

- **Do the mechanical work with tools, leave the decision to the model** — FEATURE — value 4 — effort M — risk med — category: edit quality
  Why: T-0788 defers LSP for references and renames. Rename, move and import-fix verbs run through LSP, ast-grep or a formatter, so a small model chooses a target and never rewrites 40 call sites by hand.
  Done when: `fm refactor rename OLD NEW` changes every reference in a fixture repo, and a model-edit path is never invoked.

- **Compile skills into per-model prompt packs** — FEATURE — value 4 — effort M — risk low — category: context
  Why: 1158 skill files load on demand and are written for a large context. A compiler that distills the active card and playbook to a token budget from the model profile lets a 8k-context model use them.
  Done when: compiling one playbook for a 4k budget yields a pack under 4k tokens that keeps its "done when" lines, checked by a test.

- **Run a bake-off of the approaches on replayed history** — FEATURE — value 4 — effort S — risk low — category: decision
  Why: the open design question is a native loop versus orchestrating CLIs versus both. Replay five closed tasks through each prototype with the gate as the judge, and pick on pass rate and cost. Assumption: closed tasks have enough saved briefs and fixtures to replay.
  Done when: one report table lists pass, steps and tokens per approach for the same five tasks.

- **Unblock the trio with recorded fake CLIs** — FIX — value 3 — effort S — risk low — category: testing
  Why: T-0336 and T-0335 are blocked because codex and gemini aren't installed here. Cassette-style fakes recorded from documented CLI behavior let `fm agents` and ask-grant tests run in CI, and a live run later only re-records them.
  Done when: tests for `fm agents install` and the guard hook payloads for codex, gemini and opencode pass using fakes on a machine without those CLIs.

- **Compile one rules source into every CLI's native config** — CLEAN — value 3 — effort S — risk low — category: do less
  Why: T-0365 proposes a generated section, and `fm agents install` writes per-tool rules. One source generates CLAUDE.md, AGENTS.md, GEMINI.md and permission files, with `fm doctor` flagging drift.
  Done when: hand-editing a generated file makes `fm doctor` name it and the file regenerates on `--fix`.

- **Supervise hookless CLIs through a PTY** — FEATURE — value 3 — effort L — risk high — category: fallback
  Why: for a tool with no hook API, Foreman can sit in a pty, read the screen, refuse to forward approval keystrokes for guarded commands and inject the next task. It is a last resort when diff admission isn't enough. Assumption: screen scraping stays stable enough on one or two CLIs.
  Done when: a scripted fake TUI that prompts to run `rm -rf` gets a "no" keystroke from the supervisor, and a safe prompt gets "yes".

- **Red-team the guard every night with a model (wild)** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: `guard_cases.jsonl` and `fm guard mine` already hold labelled refusals and replay. A model attempts to smuggle forbidden commands past the guard, and every success becomes a new failing labelled case. This is wild.
  Done when: a run with a fake attacker adds one bypassing command to the case file, and `fm replay` fails until the guard is fixed.

- **Run the work as an email-style patch series (wild)** — FEATURE — value 2 — effort M — risk med — category: workflow
  Why: assumption: a model's only output channel is `git format-patch` files, each patch reviewed by a different model and applied with `git am`. This gives granular rollback and natural cross-vendor review. This is wild.
  Done when: a three-patch series applies in order, and rejecting the second leaves the first committed.

- **Run the harness in the browser on a local WebGPU model (wild)** — FEATURE — value 3 — effort L — risk high — category: zero install
  Why: with the website task (T-1206) and `fm serve` already present, a page could drive a small WebGPU model against a repo through the File System Access API. This gives a first-run demo with no account, key or install. Assumption: a viable in-browser model exists at that size. This is wild.
  Done when: opening the demo page on a fixture folder produces one gated edit with no network calls after the model download.
