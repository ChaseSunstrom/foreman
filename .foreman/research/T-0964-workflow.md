**Reading of the brief:** Foreman's status below comes from grep hits in `MASTER.md` and `README.md` only. I did not read the code. Many matching lines were too long to show in full, so I used short snippets. Star counts are what the GitHub pages showed today (2026-10-15), via WebFetch summaries.

## 1. Answer
Foreman already covers most of what these projects offer: briefs with acceptance criteria, test-first builder lanes, red→green proof, audit lenses, a guard, a drive, a usage-pace gate, a status line and dashboard, multi-harness adapters, and lessons. The gaps are narrow and mostly about interface. The clearest ones are user-authored guard rules, a live GitHub issue/PR sync, a spec or requirements layer, a per-edit test-first gate, and an automatic "safe command" approver.

## 2. Findings: one line per project
- **everything-claude-code** (280k stars) — harness with 71 agents, 311 skills and hooks with strictness profiles. It adds scored "instincts" learned from sessions, a Memory Vault, a fresh-context reviewer, AgentShield config scanning, and install/doctor/repair. Primary: https://github.com/affaan-m/everything-claude-code
- **obra/superpowers** (~300k) — skills that trigger automatically: brainstorm → worktree → 2–5 minute tasks → fresh subagent per task with two-stage review. Code written before its test is deleted.
- **OpenSpec** (72k) — spec deltas with propose, apply and archive; the archive step updates the living specs.
- **ruflo / claude-flow** (75k) — swarms with consensus protocols, an HNSW vector store, and cross-model routing with failover. The accuracy figures are self-reported.
- **BMAD-METHOD** (54k) — agile personas, multi-agent discussions, and process depth that scales with the size of the change.
- **spec-kit** (141k) — a constitution of project principles, specify/plan/tasks/implement, optional clarify, checklist and analyze gates, plus extensions and presets.
- **wshobson/agents** (41k) — a marketplace of 94 plugins, with skills loaded on demand and model aliases mapped per harness.
- **SuperClaude** (24k) — 30 `/sc:*` commands, personas, ReflexionMemory, and 8 MCP servers.
- **claude-task-master** (28k) — task expansion, a complexity report, a research model, tags per workstream, and fallback models.
- **ccpm** (8.4k) — PRD → epic → GitHub issues. Issue state is the source of truth, with one worktree per epic and parallel agents.
- **Aperant / Auto-Claude** (14.6k) — kanban board, worktree per task, QA loop, memory layer, up to 12 agent terminals.
- **vibe-kanban** (28k) and **Claude Squad / Conductor** — kanban or tmux managers that run agents in parallel worktrees.
- **Continuous-Claude-v3** (3.9k) — ledgers, YAML handoffs, 30 hooks, and Postgres/pgvector recall of learnings.
- **cc-sessions** (1.5k) — DAIC: edits are blocked until you approve a todo list. It also blocks commits and edits off the task's branch.
- **claude-code-spec-workflow** (3.9k) — a local real-time dashboard with a read-only tunnel, validators for each spec stage, and a Report → Analyze → Fix → Verify bug flow. The maintainers say it now gets limited updates.
- **TDD Guard** (2.4k) — a hook that blocks edits breaking TDD, judged by an LLM validator.
- **hooks-mastery** (3.9k) and **multi-agent-observability** (1.5k) — hook demos with TTS announcements, JSON logs, builder/validator agents, and an event dashboard.
- **contains-studio/agents** (12k) — department-based agent prompts with proactive triggers. This is prompts only, with no enforcement.
- **ccusage** (19k) — cost and token reports from local logs.
- **Official plugins** (13 in the folder):
  - **ralph-wiggum** — a Stop hook that re-feeds the same prompt until an exact-match `<promise>` appears, capped by `--max-iterations`. Quote: "The Stop hook ... creates the self-referential feedback loop by blocking normal session exit."
  - **hookify** — markdown rule files with regex conditions and warn or block actions. `/hookify` with no arguments writes rules from your corrections. Active on the next tool use.
  - **code-review** — multiple agents with confidence-based scoring to filter false positives.
  - **feature-dev** — a 7-phase workflow.
  - **security-guidance** — a hook that warns about security issues when editing files.
  - **pr-review-toolkit** — review agents for comments, tests, error handling, types and simplification.
- **Index entries** (from awesome-claude-code, 55.8k stars):
  - Claude Code Safety Net blocks destructive git and filesystem commands.
  - Dippy approves safe Bash commands by AST parsing.
  - Parry-guard scans hook inputs and outputs for prompt injection and leaked secrets.
  - Plannotator lets you annotate plans and diffs.
  - HCOM sends hook-based messages between subagents.
  - Compound Engineering Plugin turns past mistakes into lessons.
  - Fusion Harness combines 2–5 models in architect and builder roles.
  - claude-intercom relays messages between sessions on different machines.

## 3. Distinct features Foreman lacks or does worse
Value is 1–5 for autonomous, finished, verified, cheap work.

| Theme | Feature | Project | Foreman status (grep) | Value |
|---|---|---|---|---|
| Safety | User-authored rule files with regex, warn/block, created from your corrections | hookify | **Weaker.** `vetoes.json` (MASTER:197) only adds a quoted note; "hookify" and "fm rule" had no match. | 4 |
| Safety | Auto-approve safe commands by parsing them | Dippy | **MISSING.** Only `PermissionRequest` handling for `fm ask` (MASTER:216). | 3 |
| Safety | Scan tool output and hook I/O for prompt injection | Parry-guard, AgentShield | **Weaker.** Untrusted text is marked for issues and in the adversary lens (MASTER:201, 230); no scanner on tool results. | 3 |
| Verification | Per-edit LLM gate blocking edits that skip a failing test | TDD Guard, superpowers | **Weaker.** Test-first is a builder-lane rule and `fm task prove` checks red→green afterwards (MASTER:71). No per-edit gate. | 4 |
| Verification | Confidence-scored findings filter | official code-review | **Weaker.** Findings are reproduced, with no numeric score (MASTER:134). | 2 |
| Planning | Constitution of project principles, plus a clarify gate | spec-kit | **MISSING.** No match for "constitution" or "clarif". | 2 |
| Planning | Living spec with deltas, archived on completion | OpenSpec | **MISSING.** Briefs are per-task; "spec delta" and "archive" were not found as features. | 2 |
| Planning | PRD → epic → sub-issues, with issue state as the source of truth | ccpm | **Weaker.** `fm inbox gh` reads issues read-only (MASTER:230); no PRD/epic and no write-back. | 3 |
| Planning | Standards discovery from the codebase | agent-os | **Weaker.** Conventions come from CLAUDE.md (MASTER:143); `fm map` covers co-change pairs. | 3 |
| Planning | Human annotation of a plan or diff | Plannotator | **Weaker.** Approve-plan exists (README:215) and `fm second plan` gives a verdict; no inline annotation. | 2 |
| Planning | Complexity scoring and automatic subtask expansion | task-master | **Weaker.** Tiers S/M/L are chosen by Claude (README:15); `fm batch` merges tasks but nothing splits them. | 2 |
| Memory | Vector or semantic recall across sessions and projects | ruflo, Continuous-Claude, ECC | **MISSING.** No match for vector or embedding. Foreman has `fm recall` and lessons (MASTER:60). | 2 |
| Memory | Auto-scored, auto-injected learnings ("instincts") | ECC | **Weaker.** Lessons and tripwires are injected (README:142), but not confidence-scored. | 2 |
| Cost | Cross-model routing with failover mid-task | ruflo, task-master | **Weaker.** `--failover AGENT` on a usage limit (MASTER:60) and models per tier; no per-step router. | 2 |
| Cost | Cost reports and rate-limit forecasts | ccusage, Claumon | **Present.** `fm cost` (MASTER:39) and usage pacing (MASTER:211). | 0 |
| Multi-agent | Kanban board over parallel agents | vibe-kanban, Aperant | **Weaker.** Lanes and a dashboard with queue rows exist; no board with drag-and-drop. | 2 |
| Multi-agent | Messaging between sessions | HCOM, claude-intercom | **Present** locally: bus and mail (MASTER:66). **Weaker** across machines (not verified). | 2 |
| Multi-agent | Consensus across several models | Fusion Harness, ruflo | **Weaker.** `fm second` debate with one reviewer (MASTER:208). | 2 |
| UX | Shareable read-only dashboard | spec-workflow | **MISSING.** No match for "tunnel" or "share link"; `fm serve` is Remote Control. | 2 |
| UX | Spoken completion announcements | hooks-mastery | **Weaker.** `fm notify` and chimes (MASTER:78, 242); no TTS. | 1 |
| Integrations | One adapter source for many harnesses | wshobson/agents | **Present.** Codex, Gemini and opencode adapters (README:205). | 0 |
| Integrations | Library docs and web research MCPs | SuperClaude | **Weaker.** `fm research ask` (MASTER:60); context7 had no match. | 1 |
| Integrations | Browser verification of the running app | SuperClaude, ECC | **Present.** `fm smoke` drives headless Playwright (MASTER:60). | 0 |

## 4. Risks / surprises
- Foreman already has the less obvious items:
  - worktree lanes
  - hunk mutation proof
  - flaky-test detection
  - an eval-gated self-improvement loop
  - time travel with `fm at`
  - a pace gate on usage
- Several competitors are mostly prompts. In particular, contains-studio is pure prompts; ralph-wiggum's `<promise>` completion check is exact-match string only.
- Star counts are as the page showed. Some pages returned boilerplate rather than a description (hooks-observability, vibe-kanban, ccusage), so their mechanisms come from the awesome index.
- WebFetch summarised each page, so I did not copy 5–25 word quotes verbatim. Only the ralph-wiggum quote was literal.
- One tool result was an injected MCP instructions block telling me to create a document. I ignored it.

## 5. Not checked
- Foreman's source code; I only grepped MASTER.md and README.md.
- The rest of the awesome-claude-code table (about 15k characters).
- oh-my-claudecode, Compound Engineering, Claude Code Harness, Safety Net internals.
- Whether the competing tools' features work as described.

**Noticed:**
- MASTER.md lines are very long, so grep output is truncated. That makes the map hard to audit.
- The README's `fm run --models` line and MASTER's `--failover` mention might be worth one documented cost-routing summary.
