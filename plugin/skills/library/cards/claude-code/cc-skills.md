---
name: cc-skills
title: Claude Code skills
area: claude-code
tags: [claude-code, skills, skill-md, frontmatter, progressive-disclosure]
detect: [file:SKILL.md]
related: [cc-skill-descriptions, cc-slash-commands, cc-subagents, cc-plugin-evals, cc-context-budget]
---
A skill is `skills/<name>/SKILL.md`: short frontmatter always in context, a body loaded only when invoked, and supporting files read on demand.

## Verify
- `claude plugin validate .`: the plugin and its skill folders load.
- `claude --plugin-dir ./plugin`: type `/plugin-name:skill-name` and confirm it expands.
- `wc -l skills/*/SKILL.md`: bodies stay under about 500 lines.
- `head -5 skills/*/SKILL.md`: the opening `---` is the very first line of each file.

## Test first
Write the eval or trigger prompt before the skill text.
```markdown
---
description: Scenario - a status question loads the status skill
max_turns: 4
timeout_seconds: 120
---
Where do things stand on this project?
```
Pair it with a grader that checks the trace for the Skill tool call, then write the skill until it passes.

## Do
- Frontmatter: `name` (defaults to the directory), `description`, optional `when_to_use`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `paths`, `context: fork`, `model`, `effort`.
- Put the procedure in imperative steps; move long reference into sibling files and link them from `SKILL.md`.
- Use `$ARGUMENTS`, `$0`, `$1`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}` for inputs and paths.
- Set `disable-model-invocation: true` for side-effecting skills (deploy, commit) so only the user runs them.
- Use `context: fork` with `agent` for noisy work whose output should not fill the main context.
- Ship scripts in `scripts/` and call them; code is executed, not loaded, so it costs no context.

## Avoid
- A body of thousands of lines: it stays in context after loading. Split into reference files.
- Frontmatter not on line 1 (a blank line or comment first): the fields are not read.
- Misspelled keys: unknown fields are ignored silently, so a typo in `disable-model-invocation` leaves the skill auto-invocable.
- `allowed-tools` as a restriction: it only pre-approves tools. Use `disallowed-tools` to remove them.
- Vague descriptions: the skill never triggers or triggers always (see the description card).
- Side-effecting skills left auto-invocable: Claude may run them unprompted.

## Review
- [ ] Description names what and when, key trigger first.
- [ ] Side-effecting skills set `disable-model-invocation`.
- [ ] Body under about 500 lines, references split out.
- [ ] Every referenced file path exists.
- [ ] An eval or trigger prompt proves it loads.
