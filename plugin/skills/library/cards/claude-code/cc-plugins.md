---
name: cc-plugins
title: Claude Code plugins
area: claude-code
tags: [claude-code, plugin, layout, skills, hooks, agents]
detect: [file:.claude-plugin/plugin.json]
related: [cc-plugin-manifest, cc-hooks, cc-skills, cc-subagents, cc-plugin-testing, cc-plugin-release]
---
A Claude Code plugin is a directory of components at its root, loaded in place with `claude --plugin-dir`, with only the manifest inside `.claude-plugin/`.

## Verify
- `claude plugin validate .`: manifest, component paths and MCP entries load (add `--strict` in CI so warnings fail).
- `claude --plugin-dir ./plugin`: a dev copy loads in a fresh session; check `/plugin` for an Errors tab.
- `python3 -m json.tool hooks/hooks.json`: hook file parses.
- `claude plugin list`: shows warnings such as a default folder ignored because the manifest overrides it.

## Test first
Write the failing check before the component: a validate run, a hook fixture, or an eval case.
```bash
# hooks fixture: the hook must deny a force push
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' \
  | ./hooks/guard | grep -q '"permissionDecision": *"deny"'
```
Run it red, add the component, run it green, then `claude plugin validate .`.

## Do
- Standard layout at the plugin root: `skills/<name>/SKILL.md`, `agents/*.md`, `commands/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `monitors/monitors.json`, `output-styles/`, `bin/`, `settings.json`.
- Reference bundled files as `${CLAUDE_PLUGIN_ROOT}/...`; write state to `${CLAUDE_PLUGIN_DATA}`, which survives updates.
- Prefer `skills/` over `commands/` for new work; both create slash commands, and a skill wins on a name clash.
- One dispatcher script per hook event beats many small scripts.
- Everything is namespaced under the plugin name (`plugin:skill`), so keep component names short.
- Keep a `README.md` and a `LICENSE`; keep `CLAUDE.md` out of the plugin (it is not loaded as context).

## Avoid
- Putting `skills/` or `hooks/` inside `.claude-plugin/`: only `plugin.json` belongs there. Move them up.
- Setting a manifest key such as `commands` and expecting the default `commands/` to still load: it replaces the default. List the default folder too.
- Writing state under `${CLAUDE_PLUGIN_ROOT}`: it moves on update. Use `${CLAUDE_PLUGIN_DATA}`.
- Paths without `./` or containing `..` in the manifest: they fail validation. Keep them relative and inside the root.
- Relying on `${CLAUDE_PLUGIN_ROOT}` in commands Claude runs through Bash: it is not in that environment. Use it in hook, MCP, LSP and skill content.
- Plugin agents declaring `hooks`, `mcpServers` or `permissionMode`: these are ignored. Ship them in `hooks/hooks.json` and `.mcp.json`.

## Review
- [ ] `claude plugin validate --strict .` passes.
- [ ] Every path in `plugin.json` starts with `./` and exists.
- [ ] No component sits inside `.claude-plugin/` except the manifest.
- [ ] State is written to `${CLAUDE_PLUGIN_DATA}` only.
- [ ] A dev copy loaded with `--plugin-dir` shows no Errors in `/plugin`.
