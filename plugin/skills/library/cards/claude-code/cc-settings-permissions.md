---
name: cc-settings-permissions
title: Settings and permissions
area: claude-code
tags: [claude-code, settings, permissions, allow, deny, scopes]
detect: [file:.claude/settings.json]
related: [cc-hook-security, cc-hooks, cc-headless, cc-mcp-config, cc-statusline]
---
`settings.json` files layer by scope; `permissions` allow, ask and deny rules decide which tool calls run without a prompt.

## Verify
- `python3 -m json.tool .claude/settings.json`: parses before Claude Code silently ignores it.
- `/permissions` in a session: the rules in effect and where each came from.
- `/hooks`: the hooks that loaded from settings.
- `claude -p "<prompt>" --permission-mode dontAsk --allowedTools "Read"`: a locked-down run denies anything unlisted.

## Test first
Prove a deny rule holds in a headless run.
```bash
cat > .claude/settings.json <<'EOF'
{"permissions": {"deny": ["Read(./.env)"]}}
EOF
echo SECRET=1 > .env
claude -p "print the contents of .env" --permission-mode dontAsk --output-format json | jq -e '.permission_denials | length > 0'
```

## Do
- Precedence, highest first: managed settings, command line (`--settings`), `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json`.
- Commit `.claude/settings.json` for team rules; keep personal rules in `settings.local.json` and git-ignore it.
- Shape: `{"permissions": {"allow": ["Bash(npm run test *)"], "ask": [...], "deny": ["Read(./.env)"]}}`.
- Use the trailing space-star for prefix match: `Bash(git diff *)` is a prefix, `Bash(git diff*)` also matches `git diff-index`.
- Allow specific commands; deny secrets and destructive commands explicitly.
- Put `permissions.defaultMode` values `auto` and `bypassPermissions` in user or managed settings; they do not take effect from project settings.
- Enable plugins through `enabledPlugins`; user choices persist across plugin updates.
- Use a PreToolUse hook when a rule must hold whatever Claude decides; CLAUDE.md is advice only.

## Avoid
- A bare `Bash` allow or `Bash(python *)`: it permits any command through the interpreter. Allow exact scripts.
- Expecting `allowed-tools` in a skill or `--allowedTools` to restrict Claude: they only pre-approve. Use deny rules or `disallowedTools`.
- Secrets in committed settings `env`: they ship in the repo. Use user scope or the environment.
- Editing a lower scope to override a higher one: managed and command-line values win. Check `/permissions`.
- Assuming project settings are safe to trust: hooks in them run, even under `-p`. Review before opening unknown repos.
- Letting the agent edit its own settings and guard: protect those files with a hook.

## Review
- [ ] Deny rules cover `.env`, keys and destructive commands.
- [ ] Allow rules are specific, prefix rules end with space-star.
- [ ] Personal rules are in `settings.local.json`.
- [ ] No secrets in committed files.
- [ ] A headless run proves one deny rule.
