# Brainstorm — lens: capability map

- **Activate the project's own toolchain before every worker and gate** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: "work with anything" is a stated goal. The pack covers pinned gate environments and language-server provisioning, but not activating mise, asdf, direnv, nvm, pyenv, venv or nix so a gate runs under the repo's declared versions. A gate that passes on system Python and fails on the project's pinned one is false evidence. Assumption: nothing in the 1,589-file pack does this.
  Done when: in a fixture with `.tool-versions` or `.envrc`, a `fm code` gate's recorded interpreter version equals the pinned one, and the run record lists the resolved versions.

- **Answer in-source `fm:` comment markers and remove them when proved** — FEATURE — value 4 — effort M — risk med — category: surfaces
  Why: Aider's watch mode lets someone write `# fm: make this idempotent` in their editor and get the change in place. The pack has TODO capture and editor LSP ideas, but nothing that resolves the marker itself and deletes it only after the checks pass. Assumption: capturing a TODO into the queue is different from answering it in place.
  Done when: saving a file with `# fm: <ask>` starts a run, the edit lands at that spot, and the marker is gone after the checks pass. If they fail, the marker stays and a failure note is added.

- **Resolve the user's own merge and rebase conflicts from both sides' intent** — FEATURE — value 4 — effort M — risk med — category: git
  Why: the pack covers lane merge conflicts and `fm rescue` for half-finished branches. It has no verb for a human mid-`git merge` or `rebase` with conflict markers. Assumption: nobody built this; it is a daily pain that Cursor and Cline serve.
  Done when: in a fixture repo with a conflicted rebase, `fm code resolve` rewrites every marked hunk and the verify command passes. A hunk whose intents truly clash is left for the user with both commit messages quoted.

- **Match edit anchors tolerantly before spending a repair call** — PERFORMANCE — value 3 — effort S — risk low — category: edit-format
  Why: the pack has an edit-format ladder, "preserve bytes" and "reject elided code". It lacks Aider's fuzzy search/replace matching, which tolerates indentation drift and trailing whitespace and accepts a match only when it is unique. This turns many slot failures into zero-cost successes for small models. Assumption: edit-block mismatches are among the commonest small-model failures.
  Done when: a table-driven test of 20 near-miss anchors applies the unique ones and refuses the ambiguous ones, and `fm code bench` shows fewer repair calls.

- **Apply chat templates for raw completion endpoints** — FEATURE — value 4 — effort M — risk med — category: local-models
  Why: runners are "any OpenAI-compatible endpoint" and local models. Raw llama.cpp `/completion` or text-generation servers need the model's own chat template and stop tokens. Without them, slots come back malformed on some local models. Assumption: the pack has no template handling; `/props` or `tokenizer_config` provide the template.
  Done when: against a stub raw-completion server that serves a template, a slot round trip works with no manual config and the template source is shown in `fm code runners`.

- **Offer a deterministic compute tool for exact answers** — FEATURE — value 3 — effort S — risk low — category: tools
  Why: weak models guess at regex behaviour, date maths, byte counts, JSON paths and arithmetic. A sandboxed stdlib evaluator (`re`, `datetime`, `json`, `fractions`) returns the exact answer and records it as evidence. Assumption: "do the mechanical work with tools" is listed, but this specific tool is not.
  Done when: a slot that needs "days between two dates" or "does this regex match X" is answered by the tool, the call appears in the event stream, and the tool cannot reach the network or filesystem.

- **Cluster log lines into templates before showing them to a model** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: the pack digests compiler and test output per toolchain. Production and CI logs are a different shape (millions of near-identical lines). Drain-style clustering in stdlib gives the 20 distinct templates with counts and first and last occurrence. This fits "turn production errors into FIX tasks". Assumption: that idea currently has no log-volume handling.
  Done when: a 100k-line fixture log reduces to under 40 lines that keep the one anomalous template, and the output states the compression ratio.

- **Continue and stitch truncated model output** — FIX — value 3 — effort S — risk low — category: reliability
  Why: the pack detects silent prompt truncation but not output cut at `max_tokens` or `finish_reason=length`. A cut-off diff or JSON slot is currently a failed slot at best and a corrupt edit at worst. Assumption: stitching happens only for slots where the validator can prove the join (balanced JSON, complete hunk).
  Done when: a stub endpoint that truncates mid-slot yields a valid slot after one continuation, and truncation inside a code fence never reaches a write.

- **Search installed `--help` and man pages offline for flag grounding** — FEATURE — value 3 — effort M — risk low — category: grounding
  Why: models invent CLI flags in verify commands. The pack has "check that verify commands can run" and "learn a runner from `--help`", but no local index of every installed binary's help. Assumption: a stdlib BM25 over `--help` and man output, built lazily per binary, is cheap enough.
  Done when: a verify command using a nonexistent flag of an installed tool is flagged at plan time, with the closest real flag named.

- **Map one request over a list of inputs with per-item receipts** — FEATURE — value 3 — effort M — risk med — category: batch
  Why: "work with anything" and non-code work (translations, data cleanup, config sweeps) need row-level proof and resume. The pack has sharded migrations and cross-project sweeps, but not a generic `fm code map FILE` over CSV or JSONL rows. Assumption: this generalises those two.
  Done when: killing a 50-row map at row 20 and rerunning finishes only rows 21–50, and each row has its own pass or fail receipt.

- **Wild: let the harness write its own language adapter** — FEATURE — value 4 — effort L — risk high — category: self-extension
  Why: wild. On an unknown language or build system, a child drafts the gate, outline and test-runner adapter, plus a fixture to validate it. The adapter registers only after it passes that fixture inside the guard. Assumption: this combines "tool forge", "generate skills on demand" and the language-fixture matrix into something none of them does alone.
  Done when: given a small repo in a language with no built-in adapter, `fm code` produces an adapter, its fixture passes, and a deliberately wrong adapter is rejected.

- **Wild: write edits as a three-way merge against what the model read** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: wild. The pack fences or detects human edits during a run. Merging the model's patch into the file's current content, with the read snapshot as base, lets the user keep typing in the same file. Assumption: a clean merge is safe to land and a conflict becomes a prompt, not a stop.
  Done when: a test edits line 5 by hand while a run edits line 50 of the same file; both survive. An overlapping edit pauses the run with a conflict view.

- **Wild: remember each model's repair pairs and replay them as its own few-shot** — PERFORMANCE — value 3 — effort M — risk low — category: model-adaptation
  Why: wild. The pack caches accepted slot answers and recalls proved runs as exemplars. It does not keep the (bad output, repaired output) pair per model. Showing a model its own earlier mistake and the fix targets the failure it actually makes. Assumption: model-specific failures repeat, so this lifts the first-try pass rate.
  Done when: after a failed slot is repaired once, the next same-shape slot for that model includes the pair, and `fm code bench` shows a higher first-try pass rate for a stub model that repeats the same mistake.
