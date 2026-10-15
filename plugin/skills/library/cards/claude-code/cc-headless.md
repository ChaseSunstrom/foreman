---
name: cc-headless
title: Headless claude -p
area: claude-code
tags: [claude-code, headless, cli, ci, json, automation]
detect: []
related: [cc-agent-sdk, cc-settings-permissions, cc-mcp-config, cc-plugin-testing]
---
`claude -p "<prompt>"` runs one non-interactive turn and prints the result, so scripts and CI can use Claude like any command.

## Verify
- `claude -p "say ok" --output-format json | jq -r .result`: JSON mode returns `result`, `session_id`, cost and usage.
- `claude --bare -p "Summarize README.md" --allowedTools "Read"`: reproducible run that skips hooks, plugins, MCP, memory and CLAUDE.md (needs `ANTHROPIC_API_KEY`).
- `claude -p "..." --output-format json --json-schema '<schema>' | jq .structured_output`: schema-shaped output.
- `echo $?` after the run: non-zero on failure, 143 after SIGTERM.

## Test first
Assert the contract your script depends on.
```bash
out=$(claude --bare -p "Reply with the single word PONG" --output-format json --max-turns 1)
echo "$out" | jq -e '.result | test("PONG")' || { echo "headless contract broke"; exit 1; }
```

## Do
- Output: `text` (default), `json`, or `stream-json` (add `--verbose --include-partial-messages` for token deltas).
- In CI add `--bare`, and pass context explicitly: `--append-system-prompt`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`.
- Pre-approve narrowly: `--allowedTools "Bash(git diff *),Read"`; set a baseline with `--permission-mode` (`dontAsk` for locked-down runs, `acceptEdits` for edit jobs).
- Add `--permission-prompts none` when nobody can answer prompts (2.1.259 and later).
- Capture `session_id` from JSON and continue with `--resume <id>` or `--continue`.
- Read `total_cost_usd` from the JSON for spend tracking and cap runs with `--max-budget-usd` and `--max-turns`.
- Check `plugin_errors` and `mcp_server_errors` in the `system/init` event to fail CI when something did not load.
- Pipe input on stdin (capped at 10MB).

## Avoid
- Running without `--bare` in CI: the host's hooks, MCP servers and CLAUDE.md change results. Use `--bare`.
- Relying on interactive built-ins (`/login`): unavailable. Pass settings with `key=value` forms where supported.
- A bare `Bash` in `--allowedTools`: it approves every command. List prefixes.
- Parsing text output: it changes. Use `json` with `jq`, or a schema.
- Ignoring the exit code and `is_error`: a failed run can still print something. Check both.
- Project `.mcp.json` and settings hooks run under `-p` without trust prompts: do not run it in untrusted checkouts.

## Review
- [ ] CI uses `--bare` and explicit config flags.
- [ ] Tools are allowed by narrow prefix.
- [ ] Turn and budget caps are set.
- [ ] Output is parsed from JSON, not text.
- [ ] Exit code and `is_error` are checked.
