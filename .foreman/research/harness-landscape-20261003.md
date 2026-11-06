Read on 2026-10-03. Quotes are from the fetched summaries, so a few are paraphrases rather than exact page text. Treat them as medium-confidence wording.

## 1. Answer and top 12 gaps
Foreman already covers gates, evidence, drive, worktrees and recall. The gaps below are mostly **codebase context, spec and requirements structure, independent review, and multi-model or cross-tool reach**. Ranked by how often and how strongly they appear.

1. **Fresh-context or parallel multi-lens review.** Dispatches several reviewers in parallel, each with a clean context.
   - claudekit: "6 parallel agents analyzing architecture, security, performance…" ([github.com/carlrannaberg/claudekit](https://github.com/carlrannaberg/claudekit)).
   - ECC: "Fresh-context code review" ([github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)).
   - Users like it because review is the bottleneck.
   - Fit: `fm audit` fans out to N lens reviewers instead of one pass. Medium-high confidence.
   - This conflicts with Foreman's token-economy rule of one reviewer pass. It would have to be opt-in.
2. **Codebase map or repo map injected as context.** Aider: "concise map of your whole git repository" ([aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)). claudekit has `codebase-map`, injected once per session. It saves tokens and makes the agent reuse existing code. Fit: a SessionStart hook that injects a symbol outline from `fm outline`. High.
3. **Spec-first pipeline (constitution, specify, plan, tasks, converge).**
   - Spec Kit: "Define what and why before deciding how to build it" ([github.com/github/spec-kit](https://github.com/github/spec-kit)).
   - Kiro has Requirements, Design and Tasks, plus Bugfix specs ([kiro.dev/docs/specs](https://kiro.dev/docs/specs/)).
   - Fit: an L-tier intake that emits spec, design and tasks artifacts with an approval gate. High.
   - Counterweight: critics call it "Waterfall Reincarnated" ([spexcode.net](http://spexcode.net/blog/ai-coding-pain-points/)).
4. **Automatic dependency-wave parallelism.** Kiro "runs independent tasks concurrently in 'waves'" (same Kiro page). Task Master has task dependencies ([github.com/eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)). Fit: use the `#T-` dependency graph to launch worktree lanes automatically. Medium.
5. **Task complexity analysis and auto-expansion.** Task Master has `analyze_project_complexity`. Fit: tier suggestion or step expansion at intake. Medium.
6. **Auto-checkpoint and restore of file state.** claudekit: "checkpoint: Auto-saves state; restore via `/checkpoint:restore`." Fit: a git-stash snapshot before risky steps, tied to `fm checkpoint`. Medium. Foreman's checkpoint may be task state only; that was not verified.
7. **File and secret guard using ignore files.** claudekit `file-guard` supports `.aiignore` and `.cursorignore`, with bash analysis. Foreman's guard covers destructive commands. Fit: add a read and write deny-list. Medium.
8. **Auto-run lint, typecheck or tests on changed files.** claudekit has `typecheck-changed`, `lint-changed` and `test-changed`. Foreman has `fm check --affected`, but it runs on demand. Fit: run it as a PostToolUse hook. Medium.
9. **Model routing and fallbacks.** claude-code-router: "ordered fallbacks… conditions on headers and bodies" ([github.com/musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)). It routes cheap tasks to cheap models. Fit: per-tier or per-agent model in the brief. Low-medium.
10. **Learned "instincts" with confidence scoring, and cross-harness memory.** ECC: "Instinct extraction with confidence scoring" and a "Unified Memory Vault". Foreman has lessons and BM25 but no confidence or decay. Medium.
11. **Cross-harness portability.** Superpowers is compatible across "Claude Code, Cursor, Devin, Gemini, GitHub Copilot" ([github.com/obra/superpowers](https://github.com/obra/superpowers)). ECC targets Codex and Cursor too. Fit: export playbooks as AGENTS.md or SKILL files. Low-medium.
12. **Statusline and live usage monitoring.** ccusage offers "5-Hour Blocks… active block monitoring" and a statusline ([github.com/ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)). Foreman has cost accounting. Fit: make sure it shows the 5-hour block in the band. Low.

Also seen but less central:
- Cline's Memory Bank ("transforms Cline from a stateless assistant into a persistent development partner") ([docs.cline.bot](https://docs.cline.bot/prompting/cline-memory-bank)).
- Copilot's cloud-sandbox async PRs ([docs.github.com](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)).
- ECC's AgentShield config scanning.

## 2. Top 5 pain points
1. **Fake or circular tests and false completion.** HN: "unit tests which are simply reinforcing the existing behaviour of the code" ([news.ycombinator.com/item?id=47234917](https://news.ycombinator.com/item?id=47234917)).
2. **Review and verification bottleneck.** "10x code but same number of reviewers" ([spexcode.net](http://spexcode.net/blog/ai-coding-pain-points/)).
3. **Prose instructions get ignored.** "frequently ignores mandatory workflow instructions" (spexcode, same page). This argues for hook enforcement, which Foreman already does.
4. **Context bloat and loss.** Specs consumed "93% of default window" (spexcode). Memory Bank and ECC session persistence exist because of this.
5. **Loss of intent and spec-code drift.** "Nobody knows why code is written that way" (spexcode).

## 3. Risks and surprises
- spexcode.net is a secondary blog and the HN themes came through a summarizer. Both are medium confidence.
- The ranking is my judgment of how often each item appears, not a measured count.
- Star counts and "89% routing accuracy" style claims from Ruflo are marketing and were ignored.

## 4. Not checked
- Cursor background agents, Codex CLI, Devin and Factory droids, OpenHands, and Roo.
- CCPM, SuperClaude, wshobson agents, the official plugin marketplace, and awesome-claude-code lists.
- PRP and Context Engineering templates.
- Reddit threads.
- Search-result listicles (dev.to, ayautomate and similar), which I did not open.
- Whether Foreman already has any of the above. I was told not to research it.
