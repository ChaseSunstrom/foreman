1. **Answer**
All three can do (a) and (c). For (b), Codex and Gemini inject context through `hookSpecificOutput.additionalContext`. opencode has no command hooks. A TS plugin can block by throwing and can append context through `experimental.chat.system.transform`, which is an experimental hook. Several details below were not read on a page, and the Codex tool names are the main conflict.

2. **Findings**

**Codex CLI** (all from https://learn.chatgpt.com/docs/hooks, primary tier; the page is a redirect from developers.openai.com and shows no date)
- Config locations are `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json` and `<repo>/.codex/config.toml`. High confidence.
- JSON shape is `{"hooks":{"PreToolUse":[{"matcher":"^Bash$","hooks":[{"type":"command","command":"...","timeout":30,"statusMessage":"..."}]}]}}`. Events shown on the page are SessionStart (matcher `startup|resume`), UserPromptSubmit, PreToolUse, PostToolUse (matcher `Edit|Write`) and Stop. High confidence.
- The TOML form is `[[hooks.UserPromptSubmit]]` followed by `[[hooks.UserPromptSubmit.hooks]]` with `type="command"`, `command=…` and `timeout=30`. High confidence.
- Stdin carries `session_id`, `cwd`, `tool_name`, `tool_input` and `turn_id`. Bash input is `tool_input.command` (a string). `apply_patch` input is `tool_input.command` holding the patch text. The shell tool name on the page is `Bash`, not `shell`. Medium confidence, because the page does not say whether the legacy `shell` array form still exists, and its `Edit|Write` matcher suggests aliases.
- To deny, either exit 2 with the reason on stderr, or print `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"…"}}`. A legacy `{"decision":"block","reason":…}` is also accepted. High confidence.
- To add context, print `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"…"}}`. The page's quote is "Plain text: Treated as developer context (SessionStart, UserPromptSubmit, SubagentStart only)", so plain stdout also works for those events. Default timeout is 600 seconds. A `[features] hooks = false` flag turns hooks off. High confidence.
- MCP goes in `~/.codex/config.toml` or `.codex/config.toml` (trusted projects only), per https://learn.chatgpt.com/docs/extend/mcp?surface=cli. The snippet is `[mcp_servers.fm]` with `command = "fm"` and `args = ["mcp"]`. The page's own example uses `npx`, so `fm` is my substitution. High confidence.
- Instructions: `~/.codex/AGENTS.override.md`, then `~/.codex/AGENTS.md`, per https://learn.chatgpt.com/docs/agent-configuration/agents-md. The project file is found by walking from the git root. High confidence.

**Gemini CLI** (https://geminicli.com/docs/hooks/ and /docs/hooks/reference/, primary tier, no date shown)
- Files are `.gemini/settings.json` (project), `~/.gemini/settings.json` (user) and `/etc/gemini-cli/settings.json` (system).
- Shape is `{"hooks":{"BeforeTool":[{"matcher":"write_.*","hooks":[{"type":"command","command":"…","name":"…","timeout":60000}]}]}}`. High confidence.
- Event names are `SessionStart`, `BeforeAgent` (this is the user-prompt-submit equivalent), `BeforeTool`, `AfterTool` and `AfterAgent` (the stop equivalent). The `AfterAgent` mapping is inferred. High confidence for the names.
- Tool events use a regex matcher; lifecycle events use an exact string, and `"*"` or `""` matches everything. The default timeout is 60000 ms. High confidence.
- Stdin carries `session_id`, `transcript_path`, `cwd`, `hook_event_name` and `timestamp`. `BeforeTool` adds `tool_name` and `tool_input`. High confidence.
- Tool inputs: `run_shell_command` takes `{command, description?, dir_path?, is_background?}` (https://geminicli.com/docs/tools/shell/). `write_file` takes `{file_path, content}`. `replace` takes `{file_path, instruction, old_string, new_string, allow_multiple?}` (https://geminicli.com/docs/tools/file-system/). High confidence.
- To deny, exit 2 with the reason on stderr, or exit 0 with `{"decision":"deny","reason":"…"}`. For context, use `hookSpecificOutput.additionalContext` on `SessionStart` or `BeforeAgent`. The page says "Your script must not print any plain text to stdout" other than the final JSON. High confidence.
- MCP goes in `settings.json` under `mcpServers.fm`, as `{"command":"fm","args":["mcp"]}`. `timeout` defaults to 600000 ms (https://geminicli.com/docs/tools/mcp-server/). High confidence.
- Instructions: `~/.gemini/GEMINI.md`, with parent-directory discovery. `context.fileName: ["AGENTS.md","GEMINI.md"]` makes it read AGENTS.md too (https://geminicli.com/docs/cli/gemini-md/). High confidence.

**opencode** (https://opencode.ai/docs/plugins/, https://opencode.ai/docs/mcp-servers/, https://opencode.ai/docs/rules/, https://opencode.ai/docs/tools/ and the source file https://raw.githubusercontent.com/sst/opencode/dev/packages/plugin/src/index.ts; all primary tier, undated)
- Plugin files go in `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global). The filename is not constrained on the page. Medium confidence.
- The signature is `import type {Plugin} from "@opencode-ai/plugin"; export const X: Plugin = async ({project, client, $, directory, worktree}) => ({...})`. The input type also carries `serverUrl` and `experimental_workspace`. High confidence.
- Hook shapes from the source:
  - `tool.execute.before(input:{tool,sessionID,callID}, output:{args})`
  - `tool.execute.after(input:{tool,sessionID,callID,args}, output:{title,output,metadata})`
  - `chat.message(input:{sessionID,agent?,model?,messageID?,variant?}, output:{message,parts})`
  - `experimental.chat.system.transform(input:{sessionID?,model}, output:{system:string[]})`
  - `event({event})` and `permission.ask(input, output:{status})`
- To block, throw an Error inside `tool.execute.before`. The page's example is `throw new Error("Do not read .env files")`. High confidence.
- Context: push a string onto `output.system` in the system transform hook for every request. `chat.message` can mutate `output.parts`, so it could carry per-prompt context. That use is inferred, not documented. Medium confidence.
- Tool ids are `bash`, `edit`, `write`, `read` and `apply_patch`. The bash argument is `command` (from the plugins page). `write` takes `{content, filePath}` (from `write.ts`). I did not read the `edit` schema; I assume `filePath` plus `oldString` and `newString`, unverified.
- MCP: `{"mcp":{"fm":{"type":"local","command":["fm","mcp"],"enabled":true}}}` in `opencode.json`. Optional fields are `environment`, `cwd` and `timeout` (default 5000 ms). High confidence.
- Instructions: `~/.config/opencode/AGENTS.md` and a project `AGENTS.md`. High confidence.

3. **Risks / surprises**
- Quotes above are paraphrases from a summarising fetch tool, not verbatim page text. Re-verify before relying on them.
- The Codex docs moved to the `learn.chatgpt.com` host through a 308 redirect from developers.openai.com. I fetched it; treat it as a redirect, not independently confirmed.
- Whether the Codex `shell` tool is surfaced as `Bash` or still as `shell` with an array should be tested live. The `apply_patch` payload may arrive as a raw patch in `command`.
- Codex project hooks may need a trust step before they run (unverified).
- I did not look for evidence against any of these answers.

4. **Not checked**
- Codex `UserPromptSubmit` and `Stop` output fields.
- Gemini `AfterAgent` output contract.
- The opencode `edit` schema and `apply_patch` args.
- Whether opencode `chat.message` parts can inject context.
- Gemini project-hook trust prompts.
- Source repos for Codex and Gemini (only docs read).
