---
name: cc-subagents
title: Claude Code subagents
area: claude-code
tags: [claude-code, subagents, agents, delegation, tools, model]
detect: [file:agents/*.md]
related: [cc-plugins, cc-skills, cc-context-budget, cc-plugin-evals]
---
A subagent is a Markdown file under `agents/` whose body is its system prompt; frontmatter sets its tools, model and limits, and its description tells Claude when to delegate.

## Verify
- `claude plugin validate .`: agent files load (the manifest `agents` key takes `.md` files, not directories).
- `claude --plugin-dir ./plugin`: ask Claude to use the agent by name; it appears as `plugin:agent`.
- `head -12 agents/*.md`: frontmatter starts on line 1 and uses camelCase keys.
- `claude --agents '{"x":{"description":"d","prompt":"p"}}'`: a session-only agent to prototype a prompt before committing a file.

## Test first
Write the delegation case before the agent.
```markdown
---
description: Lookup questions go to the scout, not the main thread
max_turns: 6
timeout_seconds: 180
---
Where is the config loader defined in this repo?
```
A trace grader asserts the Agent tool call names the scout; write the agent description until it passes.

## Do
- Frontmatter: `name` and `description` (required), `tools` (allowlist), `disallowedTools`, `model` (`haiku`, `sonnet`, `opus`, `inherit` or a full ID), `maxTurns`, `effort`, `color`, `skills`, `memory`, `background`, `isolation: worktree`.
- Give read-only agents `tools: Read, Grep, Glob`; least privilege is the main safety control.
- Pick the cheapest model that can do the job (lookups on `haiku`, audits on a stronger one).
- Write the body as a self-contained brief: goal, inputs, output format, what to leave out.
- Cap with `maxTurns` so a lost agent ends.
- Use `isolation: worktree` for agents that edit files, so the main tree stays clean.
- Return summaries, not file dumps; the point is keeping the main context small.

## Avoid
- `hooks`, `mcpServers` and `permissionMode` in a plugin agent: ignored for security. Ship hooks in `hooks/hooks.json` and servers in `.mcp.json`, or copy the agent to `.claude/agents/`.
- Omitting `tools`: the agent inherits everything, including write tools. List what it needs.
- A colon in `name`: not allowed. Use kebab-case.
- Descriptions like "helper agent": Claude never delegates. State the task and when.
- Assuming a project or user agent of the same name loses to the plugin: plugin agents have the lowest priority.
- Agents that spawn work and wait forever: set `maxTurns` and ask for partial results.

## Review
- [ ] `tools` is an explicit allowlist.
- [ ] Description says when to delegate.
- [ ] Model matches the task's difficulty.
- [ ] `maxTurns` is set.
- [ ] No ignored plugin-agent fields (`hooks`, `mcpServers`, `permissionMode`).
