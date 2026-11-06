**Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP or stream-json control surface for create/resume/stop/stream. The cheapest path to a common layer is `fm mcp` plus an AGENTS.md or GEMINI.md instruction file for every agent. Then add a thin hook adapter that calls `fm` per agent. The desktop app should drive Claude Code through the Agent SDK or `-p` stream-json, opencode through `opencode serve`, Codex through `codex app-server`, and Gemini through `gemini --acp`.

**(a) Claude Code**
- Hooks include SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop and about 25 more — https://code.claude.com/docs/en/hooks (primary). PreToolUse blocks by exit 2 or `permissionDecision: "deny"`. UserPromptSubmit and SessionStart inject `additionalContext`. — high
- Quote: "additionalContext passes a string from your hook into Claude's context window" — same URL. — high
- MCP: `-p` connects the servers in a project's `.mcp.json`, and `--mcp-config` overrides them — https://code.claude.com/docs/en/headless (primary). — high
- Control: `claude -p --output-format stream-json --verbose`; resume with `--resume <id>`; SIGINT ends a turn — https://code.claude.com/docs/en/headless. The Agent SDK has Python and TypeScript packages with `interrupt()`. — high
- Storage: "stores transcripts as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`" — https://code.claude.com/docs/en/sessions. Per that page, `-p` and SDK sessions are hidden from the picker, and the entry format is "internal" and changes. — high
- Remote: Remote Control makes "outbound HTTPS requests only" via the Anthropic API — https://code.claude.com/docs/en/remote-control. It needs claude.ai subscription auth, not an API key. — high

**(b) opencode**
- Plugin events include `tool.execute.before/after`, `session.*`, `permission.asked` and `message.updated`. A throw in `tool.execute.before` blocks the call — https://opencode.ai/docs/plugins/ (primary). — high
- Plugin context injection: I only confirmed `experimental.session.compacting` (`output.context`). Other prompt-transform hooks are not verified. — low
- Via the SDK, `noReply: true` can "inject context without triggering AI response" — https://opencode.ai/docs/sdk/. — medium
- Instructions: AGENTS.md first, then `~/.config/opencode/AGENTS.md`, then `~/.claude/CLAUDE.md` as a fallback — https://opencode.ai/docs/rules/. MCP is the `mcp` key in `opencode.json`, with local and remote types — https://opencode.ai/docs/mcp-servers/. — high
- Server: `opencode serve` is an OpenAPI 3.1 HTTP server. It can list, create, abort and fork sessions, and streams SSE at `/event`. `@opencode-ai/sdk` has `session.create/list/abort/prompt` and `event.subscribe` — https://opencode.ai/docs/server/ and /sdk/. — high
- Auth: "Set `OPENCODE_SERVER_PASSWORD` to protect the server with HTTP basic auth" — https://opencode.ai/docs/server/. mDNS discovery is optional. — high

**(c) Codex CLI**
- Hooks: SessionStart, PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Stop, Interrupt and others. PreToolUse can return `permissionDecision: "deny"`. `additionalContext` works in SessionStart, UserPromptSubmit and Pre/PostToolUse. Config is `~/.codex/hooks.json`, `config.toml` `[hooks]`, or the same under `<repo>/.codex/` — https://learn.chatgpt.com/docs/hooks (primary; the fetch tool's summary, not a verbatim quote). — medium
- `codex exec --json` emits JSONL (`thread.started`, `turn.*`, `item.*`). Resume with `codex exec resume <SESSION_ID>`, and `--ephemeral` skips persistence — https://learn.chatgpt.com/docs/non-interactive-mode. — high
- `codex app-server` speaks JSON-RPC over stdio JSONL or WebSocket, with `thread/start`, `thread/resume`, `thread/list` and `turn/interrupt`. WebSocket requires auth before requests — https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md. — high
- Not verified: the on-disk session path (I believe `~/.codex/sessions`), the `codex mcp-server` details, the MCP config location (I believe `~/.codex/config.toml`), and AGENTS.md. — low

**(d) Gemini CLI**
- Hooks: SessionStart/End, BeforeAgent/AfterAgent, BeforeModel/AfterModel, BeforeTool/AfterTool, PreCompress, Notification. BeforeTool blocks via JSON or exit 2, and BeforeAgent injects context. Config is `.gemini/settings.json` or `~/.gemini/settings.json` — https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md. — high
- Instructions: `context.fileName` lets you add AGENTS.md alongside GEMINI.md. MCP is `mcpServers` in `settings.json` — https://geminicli.com/docs/reference/configuration/. — medium
- Headless: `-p` with `--output-format stream-json` emits init, message, tool_use, tool_result, error and result events — https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md. — high
- Sessions: `--resume [id]`, `--list-sessions`, `--delete-session`, stored in `~/.gemini/tmp/<project_hash>/chats/` — https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/session-management.md. — high
- `gemini --acp` is JSON-RPC over stdio with `newSession`, `loadSession`, `prompt` and `cancel` — https://geminicli.com/docs/cli/acp-mode/. — high
- Remote: no built-in remote control found. — medium

| agent | can block tools | can inject context | session API | Foreman path |
|---|---|---|---|---|
| Claude Code | yes (PreToolUse) | yes | Agent SDK / `-p` stream-json | existing plugin |
| opencode | yes (plugin throw) | partial (SDK `noReply`) | `opencode serve` HTTP + SSE | TS plugin calling `fm`, plus MCP |
| Codex | yes (PreToolUse) | yes | `app-server`, `exec --json` | hooks.json calling `fm`, plus MCP |
| Gemini | yes (BeforeTool) | yes (BeforeAgent) | ACP, headless stream-json | settings.json hooks calling `fm`, plus MCP |

**Risks / surprises**
- Hook payload and output schemas differ per agent, so each needs its own adapter.
- The Codex docs moved to learn.chatgpt.com (a 308 redirect).
- Claude transcript formats are internal and unstable, so use the SDK or `-p` rather than parsing the JSONL.

**Not checked**
- Anything marked low or unverified above.
- Any evidence against the answers, and each agent's custom commands and skills formats (except for the Claude Code `-p` notes).
- The Claude Agent SDK page itself.
- Quote accuracy: fetched pages were summarised by a small model, so quotes marked as such need the main thread's spot-check.
