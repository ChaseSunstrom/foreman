**Answer.** Foreman already covers most of what these tools do for orchestration, queueing, guard hooks, worktree lanes, cost tracking and multi-agent installs. The gaps are narrower than the tool list suggests:
- PR and CI automation, and a GitHub-triggered bot.
- Usage forecasting, and per-task model routing or fallback.
- A vector or symbol-level code index.
- Checkpoint rewind and fork.
- A review UI with inline comments, and a diff or preview UI.
- Chat-platform notifications and an LLM gateway.

Absence below means grep found nothing in `MASTER.md` or `README.md`. I did not read those files in full.

**Tools surveyed (one line each; fetched READMEs or docs, high confidence unless noted)**
1. claude-flow/Ruflo (ruvnet): queen-led swarms (hierarchical, mesh, adaptive) with Raft/Byzantine/gossip consensus, an HNSW vector store, multi-provider routing with failover, learning hooks, and mTLS federation. Many of its claims are unverified.
2. oh-my-claudecode: team pipeline (plan → PRD → execute → verify → fix), plus Ralph, autopilot, ralplan and deep-interview modes. It routes cheap or strong models by task, waits out rate limits and auto-resumes, and sends stop callbacks to Telegram, Discord or Slack. It also has `/skillify`, a HUD, and a `/ask` tri-model advisor.
3. Claude Squad: tmux session plus git worktree per agent, a TUI, auto-accept, and commit/push/pause/resume.
4. vibe-kanban (BloopAI): Kanban issues, a workspace per agent with a dev server, a diff viewer whose inline comments go back to the agent, a preview browser, and PR creation with AI descriptions. It is sunsetting.
5. Crystal/Nimbalyst: parallel worktree sessions to compare approaches. Nimbalyst adds live-edit editors and a desktop app. Crystal is deprecated.
6. Conductor: Mac app with a worktree per workspace, a diff, test and check view, and review comments sent back to the agent. Cloud workspaces are paid, so I ignore them (secondary sources, medium confidence).
7. claude-code-router: gateway with conditional routing, ordered fallback models, key pools, per-client key limits, and request traces with estimated cost.
8. ccusage: daily, weekly, monthly and session reports, 5-hour blocks, per-model breakdown, JSON output.
9. Claude Code Usage Monitor: burn rate, a forecast of when a limit runs out, plan limits set from your P90 usage, and exit codes for scripts.
10. opcode (claudia): checkpoint timeline with restore and fork, a diff viewer, custom agent library, and an MCP registry.
11. tweakcc: patches Claude Code's prompts and tools, sets toolsets, subagent models and `opusplan`, and reapplies patches via a SessionStart hook.
12. SuperClaude: 30 `/sc:` commands, 20 personas, 7 modes, and 8 MCP integrations such as Serena memory, Context7 and Playwright.
13. continuous-claude: a loop that makes a PR per iteration, waits for CI and review, then merges or discards it. It has `--max-cost`, `--max-runs` and `--max-duration` caps, a shared notes file, stall detection, and an optional reviewer on a different provider.
14. claude-code-action: GitHub Action triggered by an @claude mention or issue assignment. It reviews PRs, implements changes, and returns structured JSON outputs.
15. Aider: architect model proposes, editor model applies edits. The docs page doesn't explain the repo map, so its mechanism is unconfirmed.
16. OpenHands: container per conversation, an agent server REST API, scheduled and webhook automations, and an ACP client.
17. Roo Code: per-mode tool and file restrictions, a Boomerang orchestrator that delegates through `new_task`, and a model remembered per mode.
18. Cline memory bank: a six-file markdown project memory that is read at the start of each task.
19. Kiro: spec files (requirements, design, tasks) with a dependency graph that runs independent tasks in parallel waves. Its hooks fire on file save, pre/post tool use and stop.
20. Codex CLI and Cursor: not confirmed. The Codex AGENTS.md and Cursor background-agent fetches were redirected or empty, and I did not retry them. Foreman already installs into Codex.
21. Devin: Interactive Planning shows a plan with code citations and auto-proceeds after 30 seconds unless you intervene. Devin Wiki is auto-generated repository docs (secondary source, medium confidence).

**Feature gaps** (value 1–5 for autonomous, finished, verified, cheap, fast work)

| Feature | Tool(s) | Foreman status | Value |
|---|---|---|---|
| **Orchestration** | | | |
| PR per task, wait for CI and review, then auto-merge or discard | continuous-claude | MISSING. `gh pr` and "pull request" not found in `MASTER.md`; only `gh issue list` read-only (`MASTER.md:230`) | 5 |
| GitHub-triggered bot (@claude, issue assignment) | claude-code-action | MISSING. `fm inbox gh` only pulls issues into briefs, no write path | 3 |
| Task dependency graph run in parallel waves | Kiro | Weaker: lanes and queue ordering exist, but no wave scheduler found | 3 |
| Spec files with an approve gate | Kiro, Devin | Weaker: briefs have acceptance criteria and steps (`README.md:111`); no design file or timed approval | 2 |
| Scheduled and webhook triggers | OpenHands | Weaker: `fm night` and `fm scout` only | 2 |
| **Parallelism** | | | |
| Compare N approaches to one task | Crystal | Weaker: `fm ideas` fans out ideas, not competing implementations | 3 |
| Container-per-run sandbox | OpenHands | Weaker: the guard is "a speed bump, not a sandbox" (`README.md:235`) | 4 |
| **Cost and routing** | | | |
| Complexity-based model routing per task | oh-my-claudecode, tweakcc | Weaker: agents are pinned (Sonnet reviewer, Haiku scout, `MASTER.md:71`); no per-task tier→model rule found | 4 |
| Plan-with-strong, edit-with-cheap split | Aider, `opusplan` | MISSING | 3 |
| Provider fallback on error or limit | claude-code-router, claude-flow | MISSING | 2 |
| Limit forecast, burn rate, P90 plan limits | Usage Monitor, ccusage | Weaker: `fm cost` and `fm budget` exist; no forecast, burn rate or 5-hour block grep hits | 3 |
| Max-runs and max-duration caps on `fm run` | continuous-claude | Unclear: `max-cost` found (`MASTER.md:76`); the other caps not checked | 2 |
| **Memory and context** | | | |
| Vector or semantic code search | claude-flow | MISSING. `vector` not found; `embedding` hit is unrelated (`MASTER.md:208`) | 3 |
| Symbol map or repo map | Aider | MISSING. `repo map` and `tree-sitter` not found; `lsp` appears, not checked | 3 |
| Auto-generated repo wiki | Devin Wiki | MISSING | 2 |
| **UI and visibility** | | | |
| Checkpoint timeline: rewind and fork a session | opcode | MISSING. `rewind` not found; `fm checkpoint` saves task resume points only | 3 |
| Inline diff comments sent back to the agent | vibe-kanban, Conductor | MISSING (Desktop and `/fm` dashboard exist) | 3 |
| Preview browser or dev server per workspace | vibe-kanban | MISSING | 2 |
| **Review and verification** | | | |
| Reviewer on a different provider | continuous-claude, `/ask` | Weaker: `fm second` compares models after the fact (`MASTER.md:209`); no reviewer pass on another provider in the loop | 3 |
| Persistent verify-until-pass mode | oh-my-claudecode | Likely present via the done-gate and drive; not verified | 1 |
| **Integrations** | | | |
| Chat notifications (Slack, Telegram, Discord) | oh-my-claudecode | Weaker: `fm notify CMD` is generic (`MASTER.md:242`); no ready channels | 2 |
| LLM gateway with traces and per-client keys | claude-code-router | MISSING | 1 |
| ACP or multi-agent client | OpenHands | Partly present: Codex, Gemini and opencode adapters (`README.md:205`) | 1 |
| **Safety** | | | |
| Per-mode tool and path restrictions | Roo | Weaker: agent tool allowlists plus the `confine` category (`MASTER.md:71`) | 1 |

**Risks and surprises**
- Several fetches were redirected or empty (Codex, Cursor), and the Aider repo-map page was thin.
- A fetched page mentioned MCP docs-tool instructions. I ignored them as irrelevant.
- Grep misses can be wording misses, for example a "pull request" feature phrased as "merge".

**Not checked:** the Cursor rules, Cline checkpoints, `fm second`'s full semantics, and whether `fm run` has duration caps.

**Noticed:** `README.md:235` says the guard isn't a sandbox, so a container-per-run option could be its own task.
