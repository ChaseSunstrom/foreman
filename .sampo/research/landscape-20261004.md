# Research: What do developers want from AI coding-agent harnesses and plugins (Claude Code, Codex, Cursor, Aider, Cline) that they say is missing or unreliable today (October 2026)? Name concrete capabilities and who asks for them.

Asked 2026-10-04 · 3 sub-question(s) · 21 claims: 12 quote found, 7 quote not found, 2 unchecked. ✓ means the quoted words are on the cited page, not that the claim is true; 'also:', 'single source' and possible conflicts come from word overlap between claims, not from reading them.

## What specific capabilities do developers say are missing or unreliable in AI coding-agent harnesses like Claude Code, Codex, Cursor, Aider, and Cline as of 2026 (e.g., long-running task reliability, context and memory management, permissions and sandboxing, cost and usage transparency, multi-agent orchestration, plugin/MCP stability)?
- ✗ Permission and sandbox prompts are too frequent. A user reported 15+ approval prompts in one session, because the allow list matches command prefixes while the sandbox flags command structure. — https://github.com/anthropics/claude-code/issues/37839 "The allow list matches on command prefix (`Bash(python3:*)`) but the sandbox flags are on command structure (newlines, `#` comments, empty quotes, `&`)." (community, 2026-03-23; not found: the quoted words aren't on the page) · single source
- ✗ Developers want the sandbox to cover every tool, not only Bash. The request says Read, Write and Edit run in the agent's own process with full host access, which exposes credentials and lets the agent edit its own config. — https://github.com/anthropics/claude-code/issues/26616 "enforces filesystem and network restrictions only on the Bash tool and its child processes." (community, 2026-02-18; not found: the quoted words aren't on the page) · single source
- ✓ Users asked for usage and limit transparency: real-time usage percentage, an indicator of which model is active, and a `/usage` command. The issue was closed as not planned. — https://github.com/anthropics/claude-code/issues/3329 "Claude Code should display real-time usage metrics to help users understand their current usage limits and which model (Opus 4 vs Sonnet 4) is actively being used." (community, 2025-07-11 (older than a year); quote found) · single source
- ✓ Cross-tool context and memory is a stated pain point. Rules and memory files go stale, differ between Claude Code, Codex and Cursor, and a developer says no production-grade cross-tool team memory exists. — https://forum.cursor.com/t/how-are-people-handling-context-across-different-ai-coding-tools/159891 "the context/memory part is starting to annoy me" (community, 2026-05-06; quote found) · single source
- ✓ In the Stack Overflow 2025 survey, 66% of developers cite near-miss AI output as a frustration, and 45% say debugging AI code takes longer. — https://survey.stackoverflow.co/2025/ai "AI solutions that are almost right, but not quite" (primary, 2025 (older than a year); quote found) · single source
- ✓ Agent adoption is held back by reliability and data-security concerns. The survey says 87% worry about accuracy and 81% about security and privacy, and only 31% use agents. — https://survey.stackoverflow.co/2025/ai "have concerns about the security and privacy of data when using AI agents" (primary, 2025 (older than a year); quote found) · single source

Against:
- ✗ The sandbox-scope request (#26616) and the usage-transparency request (#3329) were both closed as "not planned". The vendor may have shipped other fixes, or may not treat them as priorities, and I did not check. Only the permission-prompt issue (#37839) was not shown as closed. — https://github.com/anthropics/claude-code/issues/26616 "enforces filesystem and network restrictions only on the Bash tool and its child processes." (community, 2026-02-18; not found: the quoted words aren't on the page)
- ✓ The survey data predates 2026 and covers AI tools broadly, not harnesses specifically. Agent users are a minority (31%), so these complaints may not represent harness users. — https://survey.stackoverflow.co/2025/ai "have concerns about the security and privacy of data when using AI agents" (primary, 2025; quote found)

Open:
- I did not verify long-running task reliability, multi-agent orchestration, or MCP/plugin stability complaints, and found no primary sources for them.
- I did not check Codex, Aider, or Cline issue trackers, so I can't say who is asking for what beyond Claude Code and Cursor users.
- The sources contain no October 2026 data. The newest item is the Cursor forum thread from June 2026.
- The cost and usage claim rests on a 2025 issue. I did not look for newer 2026 complaints.

## Who is asking for these capabilities (e.g., individual developers, enterprise teams, security and platform engineers, open-source maintainers), and where are the requests documented (GitHub issues and feature requests, Hacker News, Reddit, developer blogs, surveys)?
- ✗ A security-minded individual user (GitHub user coygeek) asked on 2026-01-23 for Claude Code's sandbox escape hatch to be opt-in, with audit logging of unsandboxed commands. This is a security and enterprise-governance request filed in the vendor's public issue tracker. — https://github.com/anthropics/claude-code/issues/20259 "Make sandbox escape hatch opt-in and add audit logging for `dangerouslyDisableSandbox` usage" (primary, 2026-01-23; not found: the quoted words aren't on the page) · single source
- ✓ The same issue says the default-on escape hatch is a problem because users who enable sandboxing may not know Claude can trigger it. The issue was closed as "not planned", so the vendor declined it. — https://github.com/anthropics/claude-code/issues/20259 "Users enabling sandboxing for security may not realize there's an escape hatch that Claude can trigger" (primary, 2026-01-23; quote found) · single source
- ✓ Stack Overflow's 30 Sep 2026 retrospective on its developer surveys reports that agent use nearly doubled, from 31% in the 2025 survey to 59% in an April 2026 pulse survey. This suggests the pool of people making requests is growing quickly and is not limited to early adopters. — https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/ "31% of respondents indicating they were using them" (primary, 2026-09-30; quote found) · single source
- ? The same Stack Overflow post reports that 75.3% of developers say they do not trust AI's answers. A further 61.7% cite ethical or security concerns. Trust is therefore a broad complaint across respondents, not one niche group's. — https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/ "75.3%" (primary, 2026-09-30; unchecked: quote too short to check (under 4 words)) · single source

Against:
- ? The quotes for the Stack Overflow claims come from a summarizer's extract of the page, and "75.3%" and "31% of respondents indicating they were using them" are very short. The page's wording may differ slightly. The ADTmag page (secondary coverage of the Stack Overflow survey) returned HTTP 403, so I could not verify the "87% accuracy concern, 81% security concern" figures that appeared in search snippets. — https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/ "61.7%" (primary, 2026-09-30; unchecked: quote too short to check (under 4 words))

Open:
- I did not fetch any Hacker News or Reddit threads, so I can't say which groups ask for these capabilities there.
- I found no first-party survey that splits requests by role (enterprise platform or security engineers versus individuals versus open-source maintainers).
- I did not check whether Codex, Cursor, Aider or Cline issue trackers show the same requests. I only verified one Claude Code issue.
- I did not fetch other Claude Code issues that appeared in search (#39971 on unit-testing permission rules, #88389 on security audit capabilities), so I can't say who filed them or what they ask for.

## Which of these requests are most frequent or highest-priority across the tools, and how do the tools' maintainers or recent releases respond to them (roadmaps, changelogs, official statements)?
- ✓ Claude Code's recent releases center on permission-rule correctness and plugin extensibility. v2.1.289 (Oct 3) fixed deny/ask rules on nested parts of compound shell commands, and v2.1.287 (Oct 1) added "Claude Mods", which let plugins modify deeper behavior. — https://www.gradually.ai/en/changelogs/claude-code/ "Added Claude Mods: plugins may now modify deeper behavior" (secondary, 2026-10 (third-party changelog aggregator); quote found) · single source
- ✗ Claude Code also shipped fixes for permission and auto-mode edge cases (v2.1.288). It added a `/doctor prompt-audit` command that audits CLAUDE.md files, skills, agents and commands (v2.1.283). — https://www.gradually.ai/en/changelogs/claude-code/ "Added `/doctor prompt-audit` to audit your CLAUDE.md files, skills, agents and commands for prompting patterns" (secondary, 2026-10; not found: the quoted words aren't on the page) · single source
- ✗ Codex's recent CLI releases focus on approval and sandbox granularity. v0.158.0 (Sep 28) enabled terminal input approval by default for elevated-permission commands. v0.159.0 (Sep 29) kept explicit filesystem denials on approved commands and protected `.aws` directories by default. — https://learn.chatgpt.com/docs/changelog "Approved commands retain explicit filesystem denials, and `.aws` directories are protected by default under writable roots." (primary, 2026-09-29; not found: the quoted words aren't on the page) · single source
- ✓ Codex 0.160.0 (Oct 1) added an opt-in "Guardian" review feature that retrieves earlier user instructions and agent-handoff context. This responds to the demand for reliable agent oversight. — https://learn.chatgpt.com/docs/changelog "Added opt-in Guardian review capabilities to retrieve earlier user instructions and include context from agent handoffs." (primary, 2026-10-01; quote found) · single source
- ✓ Codex made lifecycle hooks default-on (Aug 2026), with a trust-review gate for non-managed hooks. This answers a demand for deterministic harness control. — https://blakecrosley.com/blog/codex-hooks-make-the-harness-real "Before any non-managed hook runs, Codex requires you to review and trust its exact definition." (secondary, 2026-08-28; quote found) · single source
- ✓ Before Codex formalized these features, teams were building long-running work, remote execution, approvals, hooks, scoped credentials and audit signals privately. This points to the unmet demand: autonomy with governance. — https://blakecrosley.com/blog/codex-hooks-make-the-harness-real "long-running work, remote execution, mobile steering, approvals, hooks, scoped credentials, and audit signals" (secondary, 2026-08-28; quote found) · single source
- ✓ Cursor's top complaint was reliability. Agent edits were silently reverted, and Cursor confirmed three root causes in March 2026: Agent Review Tab, Cloud Sync racing with local saves, and format-on-save. Other complaints (crashes, usage limits, agent planning errors) had no documented response. — https://vibecoding.app/blog/cursor-problems-2026 "The Cursor team confirmed three root causes in March 2026" (community, 2026 (exact date unknown); quote found) · single source

Against:
- ✗ The Claude Code and Codex evidence comes from changelogs, which show what shipped rather than what users asked for most. I did not tie any item to issue-vote counts, so "most frequent" is inferred from release themes (permissions, hooks, reliability) and not measured. The Claude Code changelog is a third-party aggregator and the Cursor piece is a blog, so both are weaker than official sources. — https://www.gradually.ai/en/changelogs/claude-code/ "Fixed a damaged response stream showing raw errors...being retried or reported as an interrupted response" (secondary, 2026-09-28; not found: the quoted words aren't on the page)

Open:
- Vote or reaction counts on the top-requested issues in the anthropics/claude-code, openai/codex, cline/cline and Aider repos. I did not retrieve them.
- Official roadmap statements from Cline and Aider, and Cursor's official changelog for Aug–Oct 2026. I did not fetch any of these.
- Whether Claude Code's official changelog (not the aggregator) matches the quoted entries. The quotes come from the aggregator page, and I did not check them against Anthropic's own changelog.

## Since harness-landscape-20261003
- new: Permission and sandbox prompts are too frequent. A user reported 15+ approval prompts in one session, because the allow list matches command prefixes while the sandbox flags command structure.
- new: Developers want the sandbox to cover every tool, not only Bash. The request says Read, Write and Edit run in the agent's own process with full host access, which exposes credentials and lets the agen…
- new: Users asked for usage and limit transparency: real-time usage percentage, an indicator of which model is active, and a `/usage` command. The issue was closed as not planned.
- new: Cross-tool context and memory is a stated pain point. Rules and memory files go stale, differ between Claude Code, Codex and Cursor, and a developer says no production-grade cross-tool team memory ex…
- new: In the Stack Overflow 2025 survey, 66% of developers cite near-miss AI output as a frustration, and 45% say debugging AI code takes longer.
- new: Agent adoption is held back by reliability and data-security concerns. The survey says 87% worry about accuracy and 81% about security and privacy, and only 31% use agents.
- new: A security-minded individual user (GitHub user coygeek) asked on 2026-01-23 for Claude Code's sandbox escape hatch to be opt-in, with audit logging of unsandboxed commands. This is a security and ent…
- new: The same issue says the default-on escape hatch is a problem because users who enable sandboxing may not know Claude can trigger it. The issue was closed as "not planned", so the vendor declined it.
- new: Stack Overflow's 30 Sep 2026 retrospective on its developer surveys reports that agent use nearly doubled, from 31% in the 2025 survey to 59% in an April 2026 pulse survey. This suggests the pool of …
- new: The same Stack Overflow post reports that 75.3% of developers say they do not trust AI's answers. A further 61.7% cite ethical or security concerns. Trust is therefore a broad complaint across respon…
- new: Claude Code's recent releases center on permission-rule correctness and plugin extensibility. v2.1.289 (Oct 3) fixed deny/ask rules on nested parts of compound shell commands, and v2.1.287 (Oct 1) ad…
- new: Claude Code also shipped fixes for permission and auto-mode edge cases (v2.1.288). It added a `/doctor prompt-audit` command that audits CLAUDE.md files, skills, agents and commands (v2.1.283).
- new: Codex's recent CLI releases focus on approval and sandbox granularity. v0.158.0 (Sep 28) enabled terminal input approval by default for elevated-permission commands. v0.159.0 (Sep 29) kept explicit f…
- new: Codex 0.160.0 (Oct 1) added an opt-in "Guardian" review feature that retrieves earlier user instructions and agent-handoff context. This responds to the demand for reliable agent oversight.
- new: Codex made lifecycle hooks default-on (Aug 2026), with a trust-review gate for non-managed hooks. This answers a demand for deterministic harness control.
- new: Before Codex formalized these features, teams were building long-running work, remote execution, approvals, hooks, scoped credentials and audit signals privately. This points to the unmet demand: aut…
- new: Cursor's top complaint was reliability. Agent edits were silently reverted, and Cursor confirmed three root causes in March 2026: Agent Review Tab, Cloud Sync racing with local saves, and format-on-s…

Gone (in the last scan, not this one):
- Fresh-context or parallel multi-lens review. Dispatches several reviewers in parallel, each with a clean context.
- claudekit: "6 parallel agents analyzing architecture, security, performance…" (github.com/carlrannaberg/claudekit).
- ECC: "Fresh-context code review" (github.com/affaan-m/everything-claude-code).
- Users like it because review is the bottleneck.
- Fit: `fm audit` fans out to N lens reviewers instead of one pass. Medium-high confidence.
- This conflicts with Foreman's token-economy rule of one reviewer pass. It would have to be opt-in.
- Codebase map or repo map injected as context. Aider: "concise map of your whole git repository" (aider.chat/docs/repomap.html). claudekit has `codebase-map`, injected once per session. It saves token…
- Spec-first pipeline (constitution, specify, plan, tasks, converge).
- Spec Kit: "Define what and why before deciding how to build it" (github.com/github/spec-kit).
- Kiro has Requirements, Design and Tasks, plus Bugfix specs (kiro.dev/docs/specs).
- Fit: an L-tier intake that emits spec, design and tasks artifacts with an approval gate. High.
- Counterweight: critics call it "Waterfall Reincarnated" (spexcode.net).
- Automatic dependency-wave parallelism. Kiro "runs independent tasks concurrently in 'waves'" (same Kiro page). Task Master has task dependencies (github.com/eyaltoledano/claude-task-master). Fit: use…
- Task complexity analysis and auto-expansion. Task Master has `analyze_project_complexity`. Fit: tier suggestion or step expansion at intake. Medium.
- Auto-checkpoint and restore of file state. claudekit: "checkpoint: Auto-saves state; restore via `/checkpoint:restore`." Fit: a git-stash snapshot before risky steps, tied to `fm checkpoint`. Medium.…
- File and secret guard using ignore files. claudekit `file-guard` supports `.aiignore` and `.cursorignore`, with bash analysis. Foreman's guard covers destructive commands. Fit: add a read and write d…
- Auto-run lint, typecheck or tests on changed files. claudekit has `typecheck-changed`, `lint-changed` and `test-changed`. Foreman has `fm check --affected`, but it runs on demand. Fit: run it as a Po…
- Model routing and fallbacks. claude-code-router: "ordered fallbacks… conditions on headers and bodies" (github.com/musistudio/claude-code-router). It routes cheap tasks to cheap models. Fit: per-tier…
- Learned "instincts" with confidence scoring, and cross-harness memory. ECC: "Instinct extraction with confidence scoring" and a "Unified Memory Vault". Foreman has lessons and BM25 but no confidence …
- Cross-harness portability. Superpowers is compatible across "Claude Code, Cursor, Devin, Gemini, GitHub Copilot" (github.com/obra/superpowers). ECC targets Codex and Cursor too. Fit: export playbooks…
- Statusline and live usage monitoring. ccusage offers "5-Hour Blocks… active block monitoring" and a statusline (github.com/ryoppippi/ccusage). Foreman has cost accounting. Fit: make sure it shows the…
- Cline's Memory Bank ("transforms Cline from a stateless assistant into a persistent development partner") (docs.cline.bot).
- Copilot's cloud-sandbox async PRs (docs.github.com).
- ECC's AgentShield config scanning.
- Fake or circular tests and false completion. HN: "unit tests which are simply reinforcing the existing behaviour of the code" (news.ycombinator.com/item?id=47234917).
- Review and verification bottleneck. "10x code but same number of reviewers" (spexcode.net).
- Prose instructions get ignored. "frequently ignores mandatory workflow instructions" (spexcode, same page). This argues for hook enforcement, which Foreman already does.
- Context bloat and loss. Specs consumed "93% of default window" (spexcode). Memory Bank and ECC session persistence exist because of this.
- Loss of intent and spec-code drift. "Nobody knows why code is written that way" (spexcode).
- spexcode.net is a secondary blog and the HN themes came through a summarizer. Both are medium confidence.
- The ranking is my judgment of how often each item appears, not a measured count.
- Star counts and "89% routing accuracy" style claims from Ruflo are marketing and were ignored.
- Cursor background agents, Codex CLI, Devin and Factory droids, OpenHands, and Roo.
- CCPM, SuperClaude, wshobson agents, the official plugin marketplace, and awesome-claude-code lists.
- PRP and Context Engineering templates.
- Reddit threads.
- Search-result listicles (dev.to, ayautomate and similar), which I did not open.
- Whether Foreman already has any of the above. I was told not to research it.

