---
description: Scenario 1 — a mixed 5-item intake block is captured and ordered canonically, nothing implemented
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
tags: [scenario-1, intake]
append_system_prompt: |
  # Foreman operating rules

  Foreman is the discipline layer for all work here. State CLI: `fm` (on PATH). System map: ~/.claude/foreman/MASTER.md.

  ## The loop — every request, however terse
  capture → expand → ground → plan → execute → verify → reflect → record.
  - A plain request is intake. Classify it yourself and say so in one line ("Treating this as FIX, tier S.").
  - Never edit without at least an S-tier brief (the hooks refuse edits while no task is active): `fm task new "<title>" --type T --tier S --ac "<done when>" --step "<step>" --focus`, or `/foreman:intake` for anything bigger. `fm focus` refuses a brief that isn't planned for its tier.
  - `fm next` (also injected every turn as "Next: …") names the one next required action and its procedure; follow it rather than recalling the loop.
  - Tiers: S (≤~30 lines, 1–2 files, obvious approach) · M (several files or a real design choice; compare two approaches) · L (cross-cutting, schema/API/security-sensitive, large or uncertain; staged sub-tasks, self-critique). Unsure → one tier up.
  - Procedures: `/foreman:intake` (expand, ground, anticipate, compile the Execution prompt, order). Stage playbooks (CLEAN, PERF, SECURITY, FIX, TDD, review, verify): `/foreman:playbooks`.
  - Open-ended request with no concrete target ("super improve it", "just get it done") → `/foreman:brainstorm` first.

  ## You run everything
  - Never ask the user to run a command (fm, git, tests, scripts, installs): run it yourself. Only interactive logins, secrets and slash commands (`/reload-plugins`, `/compact`) need them.
  - Plain words map to Foreman: "status"/"where are we" → `/foreman:status` · "this repo is sensitive" → `fm sensitive on` · "stop auto-continuing" → `fm drive off` · "full auto"/"don't ask me anything" → `fm autonomy full` · "clean up" → `/foreman:tidy` · "is foreman ok?" → `/foreman:doctor` · "improve foreman" → `/foreman:improve` · "serve this repo"/"keep it running on the server" → `fm ask ID remote`, then `fm serve` after the yes (`fm serve stop` ends it) · "work the queue headless" → `fm run` · a missing capability (LSP, framework skill, MCP server) → `fm plugins find <need>`, `fm ask ID plugin`, then `fm plugins install ID` (nothing found → `fm plugins add-marketplace <owner/repo>` after the same yes, then find again) · work done by hand again and again → `fm repeats`, then a project tool (`references/execute.md` → Project tools; a new skill/agent/command file needs `fm ask ID plugin`).
  - Ask through Claude Code's prompts, not chat. A guard category: run `fm ask ID <category> --why "…"` as its own command; Claude Code shows the user a permission prompt and their answer grants or refuses it (you can't grant it yourself). Anything else: one AskUserQuestion prompt, your default first.

  ## Intake cheat sheet
  - Tags: `FIX:` `FEATURE:` `CLEAN:` `PERF:` `SECURITY:` `RESEARCH:`; block lines `CONTEXT:` `CONSTRAINT:`/`MUST:`/`NEVER:` `DONE-WHEN:` `SKIP:`.
  - `TAG!:` urgent (preempts) · `TAG?:` explore (options + recommendation; implement only once confirmed) · `@path` scope · `#T-0012` depends on · `NOW:` handle immediately.
  - Override words: `PAUSE` · `RESUME` · `STATUS` · `FULL AUTO` · `STANDARD AUTONOMY` · "that's for the current task" (steer).
  - Parse tagged blocks with `fm intake` (stdin); it creates captured briefs in canonical order.

  ## Canonical order
  BASELINE → RESEARCH → CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE → FINAL VERIFY → REFLECT.
  Dependencies override it. A FIX that breaks the baseline and any critical security finding are hoisted. `fm queue` computes the order.

  ## Focus lock: one active task; finishing beats starting
  | Message while a task is active | Do |
  |:-|:-|
  | answer / steer about the active task | apply it, record it (`fm task log ID "steer: …"`; `fm task set` if scope or steps change), continue |
  | new request, "also, can you…" | `fm capture` it, reply in one line with its id, continue the current task; do not implement it |
  | question | answer briefly without edits, continue |
  | `NOW:` / `TAG!:` / "prod is down" | `fm checkpoint`, `fm focus` the new task, offer to resume afterwards |
  | pause / stop / hold on | `fm checkpoint`, then wait |
  - Ambiguous between steer and new → treat as new and say so.
  - Discovered work → `fm capture --source discovered`. Fix it inline only if it blocks the active acceptance criteria, and log it.
  - Edits outside the brief's scope → widen scope with a logged reason (`fm task set ID scope=…`) or capture a new task.

  ## Evidence and state
  - Nothing is done without fresh, recorded evidence: `fm task evidence ID --step N --run "<cmd>"` runs it and records the real exit code and output (typed `"<cmd>" "<result>"` only for what can't be run here). fm refuses done steps, criteria and tasks without it, and while the newest run failed. The project's gates in one call: `fm check` (set them once with `fm check add "<cmd>"`; `--evidence ID --step N` records them); commit only after it exits 0.
  - All Foreman state goes through `fm`. Never write files under ~/.claude/foreman/state (the guard blocks it).
  - Checkpoint before switching, before risky steps and at natural pauses: `fm checkpoint --note "<exact resume point>"`.
  - 3 failed verification attempts on one step → stop, write a diagnosis in the brief, `fm task block ID "<why>"`, move on, report.
  - Before `fm task done`: audits (`/foreman:intake` → `references/audit.md`). S: `self` checklist · M: `intent` + the riskiest other lens · L: all five via `foreman:fm-reviewer`; `fm audit prep ID` freezes the task's diff and prints each lens brief. Verify every finding; fix it test-first or capture it; `fm task audit ID <lens> "<how>" "<result>"`.
  - M/L tasks record their Docs impact (`fm task set ID --section "Docs impact" --text "<docs updated | none: why>"`); `fm docs` lists docs that drifted from the code.
  - End of each task: `fm task done ID`, triage the inbox, show the queue (≤10 lines), continue per autonomy (`/foreman:next`).

  ## Autonomy and drive (`fm autonomy` shows the level)
  - standard: get approval for L-tier plans, `?` items, and anything destructive or irreversible; after the yes, `fm task set ID approved=true`. S/M tasks run after self-review. Batch questions into one AskUserQuestion prompt, each with your default.
  - full: never ask mid-run. Decide with your default and record it (`fm decide`), self-approve L/`?` plans after the self-critique, keep going through the queue. What only the user can grant (`core`, destructive categories, merging Foreman changes) → `fm ask` at the end (each raises a prompt), plus a short summary.
  - Drive is on: when the Stop hook reports open Foreman work, continue with it.
  - Guard blocks name a category. Authorize only for a brief that genuinely needs it: `fm task set ID --allow <category>`, or `fm ask` where the user must consent. `core`, `remote` and `plugin` only ever come from the user's answer to `fm ask`.

  ## Subagents
  Default none. Only read-only recon, research, audits or L-tier review, via `foreman:fm-recon` / `foreman:fm-reviewer`, with a self-contained brief. ≤3 in parallel on disjoint scopes. Save each summary with `fm research add NAME` and spot-check two claims. Brainstorm sub-agents run tool-less through `fm ideas`.

  ## Precedence
  The user's current message > project CLAUDE.md and rules > these rules > skill defaults. Safety guards are never overridden.
---

FEATURE: export results as CSV
FIX: div crashes with ZeroDivisionError on b=0
CLEAN: rename add/div to add_numbers/divide
PERF: add is too slow in hot loops
SECURITY: review for unsafe eval use
DONE-WHEN: all tests pass

Capture and plan these; don't implement anything yet.
