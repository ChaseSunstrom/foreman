---
name: cc-plugin-manifest
title: Plugin manifest (plugin.json)
area: claude-code
tags: [claude-code, plugin, manifest, userconfig, validation, versioning]
detect: [file:.claude-plugin/plugin.json]
related: [cc-plugins, cc-marketplaces, cc-plugin-release, cc-lsp-plugins, cc-monitors]
---
`.claude-plugin/plugin.json`: only `name` is required, but set `version`, `description` and `author`, and validate it.

## Verify
- `claude plugin validate .`: authoritative manifest check (types, paths, strict objects).
- `claude plugin validate --strict .`: turns warnings (unknown top-level field, non-kebab name, missing version) into failures.
- `python3 -m json.tool .claude-plugin/plugin.json`: well-formed JSON.

## Test first
Run validate against a deliberately bad manifest first, see it fail, then fix.
```bash
mkdir -p /tmp/p/.claude-plugin
echo '{"name":"demo","commands":"commands/x.md"}' > /tmp/p/.claude-plugin/plugin.json
claude plugin validate /tmp/p   # fails: path must start with ./ and exist
```
Keep that scratch case in the repo's test script so a regression turns it red.

## Do
- Minimal good manifest: `name` (kebab-case), `version`, `description`, `author: {name}`.
- Component paths start with `./`, stay inside the root, and must exist.
- Know replace versus merge: `commands`, `agents`, `outputStyles` replace their default folder; `skills` adds to it; `hooks`, `mcpServers`, `lspServers` merge with the default file.
- A hooks file wraps events in a top-level `"hooks"` key; an inline `hooks` object in the manifest does not.
- Use `userConfig` for secrets and options (`type`, `title` and `description` are required; `sensitive: true` stores in secure storage). Read values as `${user_config.KEY}` in MCP, LSP and exec-form hook `args`, or `CLAUDE_PLUGIN_OPTION_<KEY>` in hook environments.
- Declare `dependencies` for plugins that must be enabled.
- Use `experimental.monitors` for an inline monitors array.

## Avoid
- Unknown keys inside `userConfig`, `lspServers`, `channels` or monitors entries: these are strict and the plugin fails to load. Top-level unknown keys are only stripped with a warning.
- `${user_config.*}` in shell-form hook commands or monitor commands: rejected. Use exec form `args` or the `CLAUDE_PLUGIN_OPTION_` variable.
- Names starting `claude-` or `anthropic-`: reserved, validate errors. Pick another name.
- `homepage` that is not a URL: the plugin fails to load. Omit it or fix it.
- Forgetting that a set `version` pins users: they get no update until you bump it.
- `options` on a `userConfig` field when you support older builds: it needs Claude Code 2.1.271 or later.

## Review
- [ ] Validate passes with `--strict`.
- [ ] `name` is kebab-case and unreserved.
- [ ] Every declared path exists, starts with `./` and has no `..`.
- [ ] Secrets are `sensitive` userConfig, never defaults.
- [ ] `version` bumped when behavior changed.
