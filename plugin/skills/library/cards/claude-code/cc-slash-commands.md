---
name: cc-slash-commands
title: Slash commands
area: claude-code
tags: [claude-code, slash-commands, commands, skills, arguments]
detect: [file:commands/*.md]
related: [cc-skills, cc-plugins, cc-plugin-manifest, cc-mods-ui]
---
A command is a Markdown file under `commands/` (or a skill) that becomes `/name`, or `/plugin:name` from a plugin; skills are the preferred form for new work.

## Verify
- `claude plugin validate .`: command files and any `commands` manifest entries resolve.
- `claude --plugin-dir ./plugin`: type `/` and confirm `/plugin:name` lists with its argument hint.
- `head -6 commands/*.md`: frontmatter is first in the file.
- `claude -p "/plugin:name arg"`: a user-invoked command expands in headless mode too.

## Test first
Run the command headless and assert on what it should do.
```bash
out=$(claude --plugin-dir ./plugin -p "/demo:greet World" --output-format json | jq -r .result)
echo "$out" | grep -q "World" || { echo "arguments were not substituted"; exit 1; }
```
Write it red against an empty command file, then add the body.

## Do
- Frontmatter: `description` (shown in the menu), `argument-hint` such as `"[file]"`, optional `allowed-tools`, `model`, `disable-model-invocation: true`.
- Use `$ARGUMENTS` for the whole input, `$0` and `$1` for words; if no placeholder takes the input, `ARGUMENTS: <value>` is appended.
- Make the body a procedure with numbered steps and a clear stopping point.
- Set `disable-model-invocation: true` on anything with side effects (deploy, publish, delete) so Claude never fires it alone.
- Declare commands in the manifest as an object map (`source` or `content`, plus `description`, `argumentHint`, `allowedTools`) to control names and defaults.
- Prefer a skill when the command needs supporting files; both create the same slash entry and the skill wins on a clash.

## Avoid
- Setting the manifest `commands` key and losing the default `commands/` folder: it replaces the default. List `./commands/` too.
- Describing a command in the description with its whole procedure: the menu shows it and context pays for it. One line.
- Relying on terminal-only built-ins in `-p` runs: `/login` and similar are unavailable.
- Quoting multi-word arguments carelessly: `$1` takes one word; ask users to quote, or use `$ARGUMENTS`.
- A command that edits files with no `allowed-tools` or guard: it prompts mid-run. Pre-approve only what it needs.

## Review
- [ ] Description and `argument-hint` are one short line each.
- [ ] Side-effecting commands are not model-invocable.
- [ ] `allowed-tools` lists only what the body uses.
- [ ] Works through `claude -p` with a sample argument.
- [ ] No duplicate name between a command and a skill.
