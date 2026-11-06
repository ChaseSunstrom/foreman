**Method.** I read the README, the plugins/ and examples/ directory listings, the docs overview, and the CHANGELOG (about 1.06M characters) in 100k-character slices through a summarizer. I did not read it line by line, and the examples/hooks, gateway and mdm file contents were not opened. The 2.0.x releases fell between slices and I did not verify them. Treat the version numbers below as the summarizer's reading of the changelog, not exact quotes. Sources are shortened: CL = CHANGELOG.md (raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md), OV = https://code.claude.com/docs/en/overview, PL = github.com/anthropics/claude-code/tree/main/plugins, EX = .../tree/main/examples.

## 1. Capabilities by area

**Interactive TUI and input**
- Fuzzy slash-command matching, `@`-file mentions, and Tab file completion (CL 0.2.21, 0.2.47, 0.2.75).
- Queue messages and steer the agent while it works (CL 0.2.75, 0.2.108). "Send now" key, which also backgrounds running tools (CL 2.1.275, 2.1.281).
- Paste or drag in images, and read PDFs (CL 0.2.59, 1.0.58).
- Vim bindings, later visual modes, `%` motion, and insert-mode remaps (CL 0.2.34, 2.1.118, 2.1.301, 2.1.208).
- Rebindable keys via `/keybindings`, with a readline flavor (CL 2.1.x early, 2.1.238).
- Fullscreen renderer with a diff panel (`/diff`), focus view, mouse support, scrollbars, and `/tui` (CL 2.1.260, 2.1.97, 2.1.110).
- Bash mode with `!` and path autocomplete (CL 2.1.193). `/copy` picker (CL 2.1.59, 2.1.77).
- Screen-reader mode and emoji shortcodes (CL 2.1.208, 2.1.217).
- Terminal status via OSC 7501: working, waiting or done (CL 2.1.295).
- `/btw` side questions (CL 2.1.163). Prompt suggestions (CL, unlabeled release).
- Ctrl+C draft restore with the up arrow (CL 2.1.288).

**Sessions, resume, history**
- `--continue`, `--resume`, and the `/resume` picker, which can find sessions by PR URL (CL 0.2.93, 1.0.27, 2.1.122).
- `-n/--name` and `/rename` (CL 2.1.76, 2.1.75). Search across sessions with Ctrl+R (CL 2.1.129) and Ctrl+F by name (CL 2.1.288).
- `/rewind` (alias `/undo`) restores code and conversation, even to before `/clear` (CL 2.1.108, 2.1.191). "Summarize up to here" (CL 2.1.141).
- `/branch` (formerly `/fork`) copies a session into the background (CL 2.1.77, 2.1.212).
- `/export` and `/recap` (CL 1.0.44, 2.1.108). `--from-pr` for GitHub, GitLab, Bitbucket and GHE (CL 2.1.119).
- `claude attach`, `claude logs`, `stop`, `respawn` and `rm` for named sessions (CL 2.1.290, 2.1.251).
- `/cd` (CL 2.1.169). `--add-dir` (CL 1.0.18).

**Models and providers**
- `/model` saves a default or applies to one session, and `--fallback-model` / `fallbackModel` takes up to 3 fallbacks (CL 2.1.153, 2.1.166).
- `/effort` slider up to xhigh, a `maxEffortLevel` cap, and `ultrathink` (CL 2.1.111, 2.1.267, 2.1.68).
- Fast mode, and `/advisor` (CL 2.1.36, 2.1.260).
- Provider support:
  - Bedrock, Vertex, Foundry, AWS Platform, and Bedrock Mantle (CL 2.1.198, 2.1.94).
  - Setup wizards for Bedrock and Vertex (CL 2.1.92, 2.1.98).
  - LLM gateway support, including `ANTHROPIC_CUSTOM_MODEL_OPTION` and `modelOverrides` (CL 2.1.78, 2.1.72).
  - `/model` lists gateway models (CL 2.1.126).
  - `ANTHROPIC_DEFAULT_MODEL` and the `modelPicker` setting (CL 2.1.236, 2.1.243).
- Org controls: `availableModelsMatch`, `deniedModels`, `enforceAvailableModels`, `allowedProviders` (CL 2.1.283, 2.1.175, 2.1.285).
- 1M context (CL 2.1.75).

**Permissions and safety**
- Permission modes: manual (formerly default), plan, accept-edits via Shift+Tab, auto (classifier), and bypass (CL 2.1.200, 0.2.47).
- Auto mode details: `/auto-mode-setup`, hard-deny rules, `classifyAllShell`, and an `/permissions` tab for classifier rules (CL 2.1.304, 2.1.136, 2.1.193, 2.1.246).
- Allow/deny rules in shared `.claude/settings.json`, with `Tool(param:value)` syntax and globs in deny rules (CL 0.2.67, 2.1.178, 2.1.166). `/approved-tools` and `--disallowedTools` (CL 0.2.26, 0.2.82).
- Sandbox settings: network allow/deny lists, filesystem, credential masking, `failIfUnavailable` (CL 2.1.113, 2.1.219, 2.1.221, 2.1.83).
- Restricted and safe modes: `--restricted`, `--safe-mode`, `--permission-prompts none` (CL 2.1.248, 2.1.169, 2.1.259).
- Dangerous-`rm` prompt with timeout, and prompts before writing shell-startup files (CL 2.1.281, 2.1.160).
- `permissions.blockReadsOutsideWorkingDirectories` (CL 2.1.257).
- Managed settings: drop-ins, MDM templates, HIPAA and strict/lax presets (CL 2.1.83; EX settings/ and mdm/).

**Planning and todo**
- Plan mode with a `/plan <description>` argument and a `plansDirectory` setting (CL 2.1.72, early 2.1.x).
- Built-in todo list, `/todos`, and tasks with dependency tracking (CL 0.2.93, 1.0.94, early 2.1.x).
- `/goal` sets a multi-turn completion condition (CL 2.1.139).
- Dynamic workflows and `/workflows` (CL 2.1.154, OV).

**Tools**
- Bash with background mode (Ctrl-b), the Monitor tool, and PowerShell on Windows (CL 1.0.71, 2.1.98, 2.1.84).
- Web fetch and web search (CL 0.2.53, 0.2.105). `CLAUDE_CODE_DISABLE_WEB_FETCH` (CL 2.1.285).
- Read with `allow_large`, plus PDF `pages` (CL 2.1.296, 2.1.30).
- `EnterWorktree` / `ExitWorktree` (CL 2.1.72, 2.1.105).
- Cron and `/loop` scheduling, and a push-notification tool (CL 2.1.71, 2.1.110).
- Embedded `bfs` and `ugrep` (CL 2.1.117).
- Output-size caps: `bashOutputMaxChars`, `taskOutputMaxChars` (CL 2.1.261).

**Subagents and background**
- Custom subagents via `/agents`, with frontmatter such as `effort`, `omitClaudeMd`, and `initialPrompt` (CL 1.0.60, 2.1.83, 2.1.271).
- Subagent nesting and forking: depth 3 to 5, forking on by default (CL 2.1.219, 2.1.172, 2.1.232). `/subtask` (CL 2.1.212).
- Background subagents by default, plus caps on count and concurrency (CL 2.1.198, 2.1.217, 2.1.212).
- Agent view (`claude agents`, `--json`, `--cwd`): a dashboard of parallel background sessions, with pinning (CL 2.1.139, 2.1.141, 2.1.147).
- Agent teams and cross-session `SendMessage` / `ListAgents` (CL 2.1.30, 2.1.224, 2.1.232).
- Worktree isolation: `--worktree`, `isolation: worktree`, `worktree.baseRef`, `sparsePaths` (CL 2.1.49, 2.1.133, 2.1.76).

**Hooks**
- Introduced in 1.0.38 (CL). Events added later: PreCompact, PostCompact, SessionStart, Stop, SubagentStop, StopFailure, ConfigChange, Worktree*, TeammateIdle, TaskCompleted, CwdChanged, FileChanged, PermissionDenied, Elicitation, InstructionsLoaded, PreModelSwitch, PostModelSwitch, DirectoryAdded, MessageDisplay, Setup.
- Hook types: command, HTTP, and `mcp_tool` (CL 2.1.63, 2.1.118).
- Hook options: `if` filter, a `"defer"` decision, `updatedToolOutput`, `onFailure: "block"` (CL 2.1.85, 2.1.89, 2.1.121, 2.1.295).
- Example: `examples/hooks/bash_command_validator_example.py` (EX). Its contents were not read, so its behavior is inferred from the name.

**MCP**
- Add, import, and project-scope servers (`.mcp.json`), with a setup wizard (CL 0.2.31–0.2.50).
- Transports and auth: SSE, streamable HTTP, OAuth, `claude mcp login/logout`, elicitation including URL mode (CL 0.2.54, 1.0.27, 2.1.186, 2.1.76, 2.1.281).
- Management: `/mcp reconnect all`, `alwaysLoad`, `managedMcpServers`, claude.ai connectors (CL 2.1.284, 2.1.121, 2.1.259, 2.1.45).

**Plugins, skills, slash commands**
- Custom slash commands from markdown files (CL 0.2.31).
- Skills with frontmatter, stacked invocation, `/skill-doctor`, and `/reload-skills` (CL 2.1.199, 2.1.261, 2.1.152).
- Plugins:
  - `/plugin` and marketplaces, including git, GitLab, and `archive` sources.
  - `claude plugin init`, `validate`, `eval`, `install --marketplace`, `--plugin-dir`, `--plugin-url`.
  - Plugin dependencies, `bin/` executables, and `monitors` (CL 2.1.157, 2.1.77, 2.1.269, 2.1.143, 2.1.91, 2.1.105).
- Mods: plugins that change deeper behavior (CL 2.1.287). Hooks include `tool.check` and `agent.spawn`.
- Bundled commands: `/simplify`, `/batch`, `/code-review`, `/ultrareview`, `/less-permission-prompts`, `/powerup`, `/team-onboarding`, `/claude-api` (CL 2.1.63, 2.1.147, 2.1.111, 2.1.101).

**Config and settings**
- Settings hierarchy: user, project, local, managed, with `/config key=value` and search (CL 2.1.181, early 2.1.x).
- `/doctor` (alias `/checkup`) and `prompt-audit` (CL 2.1.205, 2.1.283). `--bare`, `--debug`, `--system-prompt(-file)`, `--append-system-prompt(-file)` (CL 2.1.81, 0.2.117, 2.1.281).
- Environment-variable controls; `/release-notes` (CL 0.2.37).
- `AGENTS.md` fallback when no CLAUDE.md exists (CL 2.1.277).
- Time and timezone settings; `attribution: false` (CL 2.1.257, 2.1.281).
- `DISABLE_UPDATES`, plus stable and latest release channels (CL 2.1.118; OV).

**Output, statusline, themes**
- Custom status line with `refreshInterval` and `rate_limits` in its input (CL 1.0.71, 2.1.97, 2.1.80). `subagentStatusLine` (CL 2.1.293).
- ANSI theme, custom themes via `/theme`, `/color`, `/output-style` (list and switch), built-in Concise style (CL 0.2.30, 2.1.118, 2.1.269, 2.1.237).
- Spinner verbs and tips overrides; `maxProseWidth`; `showThinkingSummaries` (CL 2.1.2, 2.1.247, 2.1.282, 2.1.89).

**Headless, SDK, CI**
- `claude -p`, piping, streaming input, and `--output-format` (CL 1.0.18; OV). TypeScript and Python SDKs (CL 1.0.23).
- `--permission-mode`, `--permission-prompts none`, `claude ultrareview` for CI (CL 2.1.259, 2.1.120).
- GitHub Actions and GitLab CI/CD (OV). Self-hosted runner (CL 2.1.224).
- OpenTelemetry events and metrics (CL, many).
- `claude plugin ... --json` and `claude agents --json` for scripting (CL 2.1.268, 2.1.145).

**IDE and other surfaces**
- VS Code and Cursor extension, JetBrains plugin, Desktop app, web at claude.ai/code, mobile (OV).
- Remote Control, `--teleport`, `--cloud`, `/desktop`, Channels, Slack, Chrome (OV).
- Native Windows, Windows ARM64, and WinGet installs (CL 1.0.51, 2.1.36, 2.1.2–2.1.27).

**Cost and usage**
- `/usage` shows a per-category breakdown, loops, and spend limits. It replaced `/cost` and `/stats` (CL 2.1.118, 2.1.149, 2.1.243). `/usage-credits`, `/rate-limit-options` (CL 2.1.144, 2.1.284).
- Prompt-cache TTL settings and cache-miss cause (CL 2.1.243, 2.1.260).
- Resume warning on stale sessions (CL 2.1.304). Auto-continue when a usage limit resets (CL 2.1.234).

**Memory, context, compaction**
- CLAUDE.md (OV), auto memory plus `autoMemoryDirectory` (CL 2.1.59, 2.1.74). Auto-compaction, idle compaction, `/context` with suggestions (CL 0.2.47, 2.1.299, 1.0.86, 2.1.74).

**Git and PR workflow**
- Plugins `commit-commands` (`/commit`, `/commit-push-pr`, `/clean_gone`) and `code-review` (5 parallel agents with confidence scoring) (PL).
- GitHub/GitLab badges in footer and statusline (CL 2.1.234). `prUrlTemplate` (CL 2.1.119). GitHub Code Review at Quick/Standard/Deep levels (CL 2.1.304).

**Official plugins** (PL):
- `agent-sdk-dev`, `claude-opus-4-5-migration`, `feature-dev` (a 7-phase flow).
- `frontend-design`, `hookify` (rules turned into hooks), `plugin-dev`.
- `pr-review-toolkit` (6 review agents).
- `ralph-wiggum` (a Stop-hook loop until done), `security-guidance` (a PreToolUse scan for 9 risk patterns).
- Two output-style plugins: `explanatory-output-style`, `learning-output-style`.

## 2. Top 15 for fm code

1. **Agent view and background sessions** (`claude agents --json`, attach, logs, stop): this is the home-over-every-project model.
2. **Headless `-p` with JSON and stream output**: the contract for driving any CLI as a step runner.
3. **Hooks with defer, `if`, and onFailure=block**: this is how to put checks and guards around other CLIs' steps.
4. **Permission modes, allow/deny rules, and sandbox**: needed for unattended steps, with a `--permission-prompts none` equivalent.
5. **Worktree isolation (`baseRef`, sparse paths)**: parallel runs per task without clobbering the working tree.
6. **`/rewind` and checkpoints**: a safe undo for failed steps.
7. **`/goal` and the Stop-hook loop (ralph-wiggum)**: loop until the checks pass, which fits plan → checks → steps.
8. **Fallback models, `modelOverrides`, gateway model listing, and `modelPicker`**: any-model and any-provider support.
9. **`/usage` with spend limits and a per-category breakdown**: cost visibility across many projects.
10. **Plugin and skill system (marketplaces, validate, eval, dependencies)**: the extension model for "full management".
11. **MCP management (reconnect, OAuth, alwaysLoad, managed servers)**: one place to see and fix tool servers.
12. **Subagents with per-agent model, effort, and caps**: right-sizing each step's model.
13. **Compaction and `/context` suggestions**: long runs stay inside the context window.
14. **Status line, notifications (`agent_needs_input`, `agent_completed`), and OSC status**: a many-project dashboard needs a "needs me" signal.
15. **Managed-settings layers and presets (strict, lax, HIPAA)**: layered config with org policy over project over user.

## Risks and unverified

- The changelog was read through a summarizer, so version attributions may be off.
- Releases 2.0.x and some boundary stretches were not covered. Checkpoints, early plugins, Skills, and the 2.0 `/rewind` are unverified.
- The README links to docs; I read only the overview page, not settings, hooks, or the CLI reference.
- Some entries describe Anthropic-hosted and enterprise features (Slack, Claude Tag, gateway). They are probably out of scope for fm code.

Noticed: none
