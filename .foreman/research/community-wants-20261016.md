**Answer.** I could not build the ~25–40 item ranked list you asked for. My search tooling returned few upvote counts and no Reddit or HN thread pages. The strongest demand I could verify is these four wants, in this order: instructions that hold after compaction and across sessions, hooks that enforce workflow rules, cheaper subagents/skills, and AGENTS.md support. Everything below is that thinner set. The rankings are partly inferred, and I would not treat them as a final ranking.

**Findings**

*Theme 1: Continuity and memory*
- Claude forgets CLAUDE.md after compaction — claudeissues.com/issue/6354 (mirror of the GitHub issue); also /issue/868, task context lost after auto-compact. Demand: 2+ mirrored issues, no counts. Medium.
- Subagents should inherit parent context instead of re-scanning the codebase — claudeissues.com/issue/12790. Demand: 1 issue. Medium.
- Subagent state lost after compact, and custom agent instructions not injected — claudeissues.com/digest/2025-12-07 and /2025-12-11. Demand: 2 digest entries. Low.
- A hook for compaction events, and a better PreCompact payload — claudeissues.com/digest/2025-12-13/14. Low.
- Best existing tool: Anthropic's subagent `memory` frontmatter (~Feb 2026). This comes from a secondary source (search summary), so I did not verify it.

*Theme 2: Discipline and enforcement*
- Claude ignores explicit instructions and skips workflow gates — claudeissues.com/issue/20024; cited #18660 and #27032 (one blog, unverified). Demand: 3+ issues plus forum threads. Medium.
- Claude ignores a "stop" instruction on verbose comments — anthropics/claude-code #65961, 41 👍. Medium-high.
- Enforce non-negotiable rules with hooks, not CLAUDE.md — scottspence.com/posts/how-to-make-claude-code-follow-hook-instructions; aicodex.to/articles/claude-md-vs-hooks. Demand: many blogs. Medium.
- Stop the "You're absolutely right!" sycophancy — #3382, 179 👍 (page snapshot). Medium.
- Best existing tool: Claude Code hooks (exit code 2 blocks the action) — secondary sources.

*Theme 3: Cross-tool portability*
- Support AGENTS.md — #6235, 409 👍 (closed); #31005 (`.agents/skills/`), 33 👍. This is the top workflow-adjacent request I found. Medium-high.
- Superpowers on other harnesses (Copilot #217, Cursor #106, Kiro #503, Antigravity #1636, Hermes #1581), 12–24 comments each. Medium.
- A universal orchestration layer for any CLI coding tool — ruvnet/claude-flow #310, 19 comments. Medium.
- Best existing tool: superpowers is multi-harness, but users report mixed results.

*Theme 4: Token and cost control*
- Superpowers and subagent-driven development burn tokens (#1152, #750, #1194, #743 on speed), 12–26 comments each. High.
- Cache creation inflated about 20K tokens per call in one release — claude-code #46917, 43 👍. Medium.
- Leaner brainstorm/plan skills — superpowers #512 and #895 (plans over-specify), 17–24 comments. Medium.
- Best existing tool: none clear. Superpowers is tuning per model (#2017).

*Theme 5: Parallel agents and orchestration*
- Agent Teams support (TeammateTool, SendMessage) — superpowers #429, 23 comments. Medium.
- MCP tools scoped to subagents only — claude-code #6915, 89 👍. Medium-high.
- Worktree isolation as the precondition for parallel work — kestra.io/resources/ai/claude-code-agents (secondary). No dedicated issue found. Low.
- Non-interactive/headless workflow modes — claude-flow #578, 17 comments. Low-medium.
- Best existing tool: Anthropic's own `/batch` with worktree agents (secondary source).

*Theme 6: Observability, UI and permissions*
- Show which file a Read touched — #21151, 133 👍. Medium-high.
- A diff review UI — #33932, 41 👍.
- Always show thinking — #8477, 94 👍.
- Permission prompt fires on `cd` in compound commands — #28240, 48 👍.
- Audit logs and persistence for multi-agent runs — Kestra article. Low.
- Can't tell whether a skill fired — superpowers #446, 23 comments, and #54 (skills not auto-triggering). Medium.
- Best existing tool: none I could identify.

*Theme 7: Reliability of tooling*
- Install and verify must work from a clean checkout — claude-flow witness-verify issues (#3189 with 66 comments, #2047, #2970). A clear cluster, but about the repo's own tooling. Medium.
- A clean uninstall command and fast cold start — claude-flow #670, #2286.

**Risks / surprises**
- The WebFetch summaries listed issues out of 👍 order, and one listed a hit-limit bug at 1499 👍. That one is plan-limit related, so I excluded it. Verify counts on github.com before citing any of them.
- Search results mostly cover issues up to Feb 2026, so some of these may be fixed.
- claude-code-harness has only 1 open issue (#389, a Windows path panic), so it offered no demand signal.

**Not checked**
- Reddit and HN: no thread pages came back.
- SuperClaude, ECC, wshobson/agents and the awesome lists.
- Discussions tabs.
- Closed-issue resolutions.
- The "~25–40 wants" target; I found about 20.

**Noticed:** none
