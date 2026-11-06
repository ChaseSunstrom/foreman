Based on the Claude Code official documentation, here's the concise answer:

**JSON output support:** Yes, `{"hookSpecificOutput": {"hookEventName": "PostToolUseFailure", "additionalContext": "..."}}` is supported and the `additionalContext` is passed to Claude.

**PostToolUseFailure input fields:** The payload includes:
- `hook_event_name`: "PostToolUseFailure"
- `tool_name`: the tool that failed
- `tool_input`: arguments passed to the tool
- `error`: failure message (for Bash, format is "Exit code N\n..." with stderr/stdout)
- Plus common fields: `session_id`, `prompt_id`, `cwd`, `tool_use_id`, `transcript_path`

**Bash nonzero exit:** Exits with code ≥1 fire **PostToolUseFailure**, not PostToolUse. The `error` field holds both exit code and command output (stderr + stdout combined).

**additionalContext size limit:** The docs don't specify a hard limit. Text from `additionalContext` is injected as a system reminder; treat it as context-window-bound.

**Key caveat:** Tools that return `<tool_use_error>` (MCP tools with explicit error responses) produce no hook event at all—neither PostToolUse nor PostToolUseFailure fire.

Cite: https://code.claude.com/docs/en/hooks-guide.md and https://code.claude.com/docs/en/hooks.md

Sources:
- [Hooks Guide - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide.md)
- [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks.md)
