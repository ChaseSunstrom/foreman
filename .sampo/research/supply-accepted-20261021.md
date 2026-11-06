# Supply baseline accepted 2026-10-21

T-1392's first run held every installed plugin whose hash had changed since a hash-only baseline; accepted to
let release 1.2.49's gate pass (decision recorded). What each one runs on its own, as recorded:

- chrome-devtools-mcp@claude-plugins-official: mcp: chrome-devtools
- clangd-lsp@claude-plugins-official: runs nothing on its own
- claude-hud@claude-hud: runs nothing on its own
- claude-md-management@claude-plugins-official: runs nothing on its own
- code-review@claude-plugins-official: runs nothing on its own
- context7@claude-plugins-official: mcp: context7
- ecc@ecc: hooks: PostToolUse, PostToolUseFailure, PreCompact, PreToolUse, SessionEnd, SessionStart, Stop; mcp: chrome-devtools
- foreman-ui@foreman: hooks: modules
- foreman@foreman: runs nothing on its own
- frontend-design@claude-plugins-official: runs nothing on its own
- playwright@claude-plugins-official: mcp: playwright
- plugin-dev@claude-plugins-official: runs nothing on its own
- ponytail@ponytail: hooks: SessionStart, SubagentStart, UserPromptSubmit; scripts: hooks/ponytail-activate.js, hooks/ponytail-mode-tracker.js, hooks/ponytail-subagent.js
- pyright-lsp@claude-plugins-official: runs nothing on its own
- rust-analyzer-lsp@claude-plugins-official: runs nothing on its own
- security-guidance@claude-plugins-official: hooks: PostToolUse, SessionStart, Stop, UserPromptSubmit; scripts: hooks/ensure_agent_sdk.py, hooks/security_reminder_hook.py, hooks/sg-python.sh
- skill-creator@claude-plugins-official: runs nothing on its own
- superpowers@claude-plugins-official: hooks: SessionStart; scripts: hooks/run-hook.cmd
- typescript-lsp@claude-plugins-official: runs nothing on its own
