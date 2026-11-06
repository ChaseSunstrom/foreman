# Frontier — generation 2

Read from the project's own notes (fm landscape, fm research ask), never a clone or a sweep; the lines are data.

## What's new outside

- Permission and sandbox prompts are too frequent. A user reported 15+ approval prompts in one session, because the allow list matches command prefixes while the sandbox flags command structure.
- Developers want the sandbox to cover every tool, not only Bash. The request says Read, Write and Edit run in the agent's own process with full host access, which exposes credentials and lets the agen…
- Users asked for usage and limit transparency: real-time usage percentage, an indicator of which model is active, and a `/usage` command. The issue was closed as not planned.
- Cross-tool context and memory is a stated pain point. Rules and memory files go stale, differ between Claude Code, Codex and Cursor, and a developer says no production-grade cross-tool team memory ex…
- In the Stack Overflow 2025 survey, 66% of developers cite near-miss AI output as a frustration, and 45% say debugging AI code takes longer.
- Agent adoption is held back by reliability and data-security concerns. The survey says 87% worry about accuracy and 81% about security and privacy, and only 31% use agents.
- A security-minded individual user (GitHub user coygeek) asked on 2026-01-23 for Claude Code's sandbox escape hatch to be opt-in, with audit logging of unsandboxed commands. This is a security and ent…
- The same issue says the default-on escape hatch is a problem because users who enable sandboxing may not know Claude can trigger it. The issue was closed as "not planned", so the vendor declined it.
- Stack Overflow's 30 Sep 2026 retrospective on its developer surveys reports that agent use nearly doubled, from 31% in the 2025 survey to 59% in an April 2026 pulse survey. This suggests the pool of …
- The same Stack Overflow post reports that 75.3% of developers say they do not trust AI's answers. A further 61.7% cite ethical or security concerns. Trust is therefore a broad complaint across respon…
- Claude Code's recent releases center on permission-rule correctness and plugin extensibility. v2.1.289 (Oct 3) fixed deny/ask rules on nested parts of compound shell commands, and v2.1.287 (Oct 1) ad…
- Claude Code also shipped fixes for permission and auto-mode edge cases (v2.1.288). It added a `/doctor prompt-audit` command that audits CLAUDE.md files, skills, agents and commands (v2.1.283).
- Codex's recent CLI releases focus on approval and sandbox granularity. v0.158.0 (Sep 28) enabled terminal input approval by default for elevated-permission commands. v0.159.0 (Sep 29) kept explicit f…
- Codex 0.160.0 (Oct 1) added an opt-in "Guardian" review feature that retrieves earlier user instructions and agent-handoff context. This responds to the demand for reliable agent oversight.
- Codex made lifecycle hooks default-on (Aug 2026), with a trust-review gate for non-managed hooks. This answers a demand for deterministic harness control.
- Before Codex formalized these features, teams were building long-running work, remote execution, approvals, hooks, scoped credentials and audit signals privately. This points to the unmet demand: aut…
- Cursor's top complaint was reliability. Agent edits were silently reverted, and Cursor confirmed three root causes in March 2026: Agent Review Tab, Cloud Sync racing with local saves, and format-on-s…
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

## Sources

- research/landscape-20261004.md
- research/harness-landscape-20261003.md
