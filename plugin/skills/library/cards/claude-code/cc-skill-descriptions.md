---
name: cc-skill-descriptions
title: Skill descriptions and triggering
area: claude-code
tags: [claude-code, skills, description, triggering, context-cost]
detect: [file:SKILL.md]
related: [cc-skills, cc-plugin-evals, cc-context-budget, cc-subagents]
---
The description is the only part of a skill Claude sees every session: it decides whether the skill triggers and what it costs in context.

## Verify
- `awk '/^description:/{print length($0)}' skills/*/SKILL.md`: each description's length; keep the key use case in the first lines.
- `claude plugin eval <plugin-dir> --trust-plugin --scaffold --runs 1 --no-publish --json out.json`: trigger cases score as expected.
- `head -4 skills/*/SKILL.md`: `description` is in frontmatter that starts on line 1.

## Test first
One positive and one negative trigger case per skill.
```markdown
---
description: Negative - a plain code question must not load the deploy skill
max_turns: 3
timeout_seconds: 120
---
Explain what this function does.
```
A grader on the trace (`type: regex`, `target: trace`) asserts the skill name is absent; the positive case asserts it is present.

## Do
- Lead with the situation: "Use when the user asks X, or the Y hook reports Z", then what the skill does in one clause.
- Include the literal phrases users type (command names, quoted wording) so matching is easy.
- Keep it short: `description` plus `when_to_use` are truncated at 1,536 characters in the listing, and every character is paid every session.
- Put detail in the body or sibling files, not the description.
- Make descriptions distinct from each other so two skills do not compete for one request.
- Use `paths` globs to limit automatic activation to matching files.
- For skills only a user should run, set `disable-model-invocation: true` so no listing cost is needed for triggering.

## Avoid
- Summaries such as "A helpful tool for tasks": no trigger. Name the condition.
- Paragraph-long descriptions with the trigger at the end: truncation cuts it. Put the trigger first.
- Many near-identical skills: each adds listing cost and misfires. Merge them or use `paths`.
- Description copies of the whole body: pays the cost twice. Keep the body for loading.
- Never testing a negative case: the skill triggers on unrelated work and nobody notices.
- Putting first-person text ("I help you"): write for the selecting model, in third person or imperative.

## Review
- [ ] Trigger condition comes first and uses real user phrasing.
- [ ] Under about 400 characters unless there is a reason.
- [ ] Positive and negative eval cases exist.
- [ ] No two skills overlap in trigger.
- [ ] Rarely used skills are not auto-listed more than needed.
