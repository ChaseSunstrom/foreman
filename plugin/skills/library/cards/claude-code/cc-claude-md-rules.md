---
name: cc-claude-md-rules
title: CLAUDE.md and rules files
area: claude-code
tags: [claude-code, claude-md, rules, memory, instructions, context]
detect: [file:.claude/rules/*.md]
related: [cc-context-budget, cc-hook-security, cc-output-styles, cc-skills]
---
CLAUDE.md and `.claude/rules/*.md` are standing instructions loaded as context; they guide Claude but enforce nothing.

## Verify
- `wc -l CLAUDE.md .claude/rules/*.md`: each file near or under 200 lines.
- `/memory` in a session: which instruction files loaded.
- `grep -n '^@' CLAUDE.md`: imports resolve to real files (imports load at launch and do not cut context cost).
- `/doctor prompt-audit`: audits instruction files for conflicts and bloat (names per current docs).

## Test first
Write the instruction as a checkable behavior, then see Claude fail it.
```bash
# rule under test: "run npm run lint before finishing"
claude -p "add a trivial function to src/a.ts" --output-format stream-json --verbose \
  | grep -q "npm run lint" || { echo "rule not followed"; exit 1; }
```
If it fails, tighten the wording or move the rule into a hook.

## Do
- Keep CLAUDE.md short and specific: commands to build and test, conventions that differ from defaults, where things live.
- Scope by place: user `~/.claude/CLAUDE.md`, project `CLAUDE.md`, subdirectory files (loaded on demand), `CLAUDE.local.md` for personal notes (git-ignore it).
- Move topic-specific guidance to `.claude/rules/` files; give a rule `paths` frontmatter globs so it loads only for matching files.
- Write concrete, verifiable lines ("run `pytest -q` before commit") instead of values ("write clean code").
- Remove or merge contradictions across files; files concatenate, root first, and conflicts resolve arbitrarily.
- Turn any must-hold rule into a PreToolUse hook or a permission rule.
- Update the file when a correction repeats; stale lines cost context every session.

## Avoid
- Files of hundreds of lines: adherence drops and every line is paid per session. Trim or split into path-scoped rules.
- Treating CLAUDE.md as a guard: Claude may ignore it. Enforce with hooks or deny rules.
- Duplicating the same rule in CLAUDE.md, rules and a style: drift and conflict. One home each.
- A `CLAUDE.md` at a plugin root expecting it to load: it does not. Put plugin guidance in a skill.
- Pasting long reference docs: import or link only what is needed, or make a skill so it loads on demand.
- Vague wording such as "be careful": untestable. State the action and the check.

## Review
- [ ] Each file is short and every line is checkable.
- [ ] Path-specific guidance lives in `rules/` with `paths`.
- [ ] No contradictions between files.
- [ ] Must-hold rules also exist as hooks or deny rules.
- [ ] Personal notes are in `CLAUDE.local.md`, ignored by git.
