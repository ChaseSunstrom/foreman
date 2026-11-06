# Brainstorm — lens: capability map

- **Rewrite an app's Claude model calls for a new model** — FEATURE — value 4 — effort M — risk low — category: ecosystem
  Why: assumption: users build on Claude, and cookbook and environment model IDs change per family (Claude 5 IDs listed). Nothing in the pack handles a model-ID migration in the user's own code.
  Done when: `fm code migrate-model --to claude-sonnet-5-5` on a fixture app rewrites IDs, flags removed or renamed parameters, runs its tests, and reports one line per change.

- **Watch the model roster for drift** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: `models.json` is hand-written, and local models need real context sizes (planned). Stale IDs, aliases or prices silently skew routing and cost.
  Done when: `fm doctor` queries each endpoint's model list, flags unknown or renamed IDs and changed context sizes, and prints a one-line proposed `models.json` edit.

- **Reconcile the cost ledger against provider bills** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: cost per call is "planned", but the ledger is only an estimate, and the user asked for "full management". Assumption: provider usage exports (CSV or API) can be fed in.
  Done when: `fm cost reconcile FILE` imports a usage export, shows estimate-versus-billed per model, and stores a correction factor the forecaster uses.

- **Reject elided-code output and track per-model laziness and refusals** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: any-model support means weak models write "…rest unchanged", truncate files, or refuse security-adjacent steps. The edit-format ladder doesn't mention detecting this.
  Done when: an edit slot containing an elision marker is rejected and re-asked, and `fm code runners` shows a laziness-and-refusal rate per model per task kind that routing reads.

- **Open a slot workbench in the app** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: the prompt-tutorial repo is about iterating prompts, yet no idea lets a user edit one slot's prompt and re-run it. Whole-run replay exists, per-slot does not.
  Done when: in the TUI, picking a past slot call lets you edit its prompt, rerun it on two runners side by side, and save the winner as a bench case.

- **Manage everything Claude Code reads from one panel** — FEATURE — value 4 — effort L — risk med — category: management
  Why: the user wants "full management" and cites the claude-code repo's MCP, hooks, subagents, permissions and plugins. Only audits exist, not one editable view with per-item token cost and guard status.
  Done when: a Config tab lists permissions, MCP servers, hooks, agents, commands and plugins from user and project scope, shows each one's startup-token cost, and toggles one with a diff preview.

- **Digest compiler and test output into ranked diagnostics per toolchain** — PERFORMANCE — value 3 — effort S — risk low — category: small-model quality
  Why: small local models choke on long cargo, tsc, go and pytest output. Runner digesters exist for CLI runners, not for gate output.
  Done when: a failing gate hands the next slot at most five parsed `file:line: message` items, with golden tests for pytest, tsc, cargo and go.

- **Read office documents and read-only data through stdlib tools** — FEATURE — value 3 — effort M — risk med — category: data and documents
  Why: the skills repo's docx, pdf, pptx and xlsx skills and the financial-services database category show requests that aren't code. Only verification of xlsx and docx is listed. Assumption: OOXML via `zipfile` and `sqlite3` or csv, row-capped and read-only through the guard.
  Done when: any runner can call `read_doc` on a docx or xlsx and `query` on a sqlite or csv file, a write attempt is refused, and results over 200 rows are truncated with a notice.

- **Protect regions inside a file with inline markers** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: path-level classes (generated, vendored, frozen) are proposed. Nothing protects a hand-tuned block inside an otherwise editable file.
  Done when: a diff touching lines between `fm:keep` and `fm:end` markers is refused by the per-file judge and the refusal names the marker.

- **Provision and health-check language servers** — FEATURE — value 3 — effort M — risk med — category: developer experience
  Why: LSP-backed blast radius and diagnostics are proposed repeatedly, and the plugins-official repo ships LSP plugins. Nothing detects a missing server, pins it, or checks that it responds.
  Done when: `fm doctor` lists the servers for the languages found in the repo, shows missing, stale or non-responding ones with the install command, and installs nothing silently.

- **Wild: Pretend a model is gone** — FEATURE — value 4 — effort M — risk low — category: resilience — wild
  Why: assumption: providers retire or rate-limit models without warning, and routing tables, recipes and defaults pin names.
  Done when: `fm code --pretend-gone MODEL` lists every default, route and recipe that would break, then shows the fallback chosen for each and the bench grade of the fallback.

- **Wild: Audit a new model overnight when it appears** — FEATURE — value 4 — effort M — risk med — category: model ops — wild
  Why: combines roster drift with replay. When the roster check finds a new model, shadow-replay last week's closed slots on it under a dollar cap.
  Done when: a new model ID in the roster produces a morning card with pass rate, cost and "switch or stay", having spent no more than the cap.

- **Wild: Heat-map diffs by self-consistency** — FEATURE — value 3 — effort M — risk low — category: review UI — wild
  Why: the pack proposes sampling claims and plans several times, but not edit slots. Sampling the edit slot three times cheaply and colouring hunks where samples disagree tells a reviewer where to look.
  Done when: the diff view tints hunks by agreement across three samples, and a fixture with one injected ambiguous hunk marks exactly that hunk.
