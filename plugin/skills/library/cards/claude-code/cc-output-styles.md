---
name: cc-output-styles
title: Output styles
area: claude-code
tags: [claude-code, output-styles, system-prompt, format, tone]
detect: [file:output-styles/*.md]
related: [cc-plugins, cc-plugin-manifest, cc-context-budget, cc-claude-md-rules]
---
An output style is a Markdown file under `output-styles/` that reshapes how Claude replies; its body is added to the system prompt every turn.

## Verify
- `claude plugin validate .`: the `outputStyles` path (default `output-styles/`) exists and loads.
- `claude --plugin-dir ./plugin`: `/output-style` lists the style; select it and send a prompt.
- `claude -p "/output-style"`: lists styles in headless mode (2.1.269 and later).
- `wc -c output-styles/*.md`: the body is small, since it is paid on every turn.

## Test first
Judge the format with a headless run and a regex.
```bash
claude --plugin-dir ./plugin -p "/output-style myplugin:terse" >/dev/null
claude --plugin-dir ./plugin -p "Summarize this repo" | head -c 600 | grep -qiE '^(result|done)' \
  || { echo "style header missing"; exit 1; }
```
Adjust the regex to your format; the point is a failing check before the style text.

## Do
- Frontmatter: `name`, `description`, and `keep-coding-instructions: true` when the style should keep Claude Code's coding behavior (without it the default coding instructions are dropped).
- Write the body as format rules: order of sections, length caps, what to omit, how to word errors.
- Give an exact skeleton of one good reply so the format is copyable.
- Keep it short; a style is a standing cost, not a reference manual.
- Put behavior rules in hooks, skills or CLAUDE.md instead; a style is for form.
- Name it distinctively; plugin styles appear namespaced under the plugin.

## Avoid
- Omitting `keep-coding-instructions` on a coding project: Claude loses coding guidance. Set it to true unless a non-coding persona is the goal.
- Long personas or policy text in a style: it rides on every request. Cut or move it.
- Putting hard rules (never touch X) only in a style: it is guidance, not enforcement. Use a PreToolUse hook.
- Contradicting CLAUDE.md formatting rules: Claude picks one arbitrarily. Keep one source of format truth.
- Format rules that fight tool output, such as demanding no tool narration while a hook injects notes: test with real tool-using prompts.
- Depending on a style in CI: pass the instruction with `--append-system-prompt`.

## Review
- [ ] Frontmatter has `name`, `description` and a deliberate `keep-coding-instructions`.
- [ ] Body is under a few hundred words with one skeleton reply.
- [ ] No enforcement rules hidden in the style.
- [ ] No conflict with CLAUDE.md.
- [ ] Selectable in `/output-style` from a dev copy.
