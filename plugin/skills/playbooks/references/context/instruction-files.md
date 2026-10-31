<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Write CLAUDE.md, rules and skill descriptions that cost little and get followed

Use when you add or trim a CLAUDE.md, a `.claude/rules/*.md` file, or a skill or slash-command description, or when sessions start with too much context.

Built on the cards `fm lib show cc-claude-md-rules`, `fm lib show cc-context-budget`, `fm lib show cc-skills`, `fm lib show cc-skill-descriptions` and `fm lib show cc-slash-commands`.

1. **Cost it:** everything always loaded is paid every turn. Count lines and what loads:
   ```bash
   wc -l CLAUDE.md .claude/rules/*.md
   grep -n '^@' CLAUDE.md
   ```
   Use `/memory` in a session to see which files loaded. An `@` import loads at launch; it does not save context.
2. **Keep each file near or under 200 lines;** move procedures into skills, which load only when used.
3. **A rule is checkable:** "run `pytest -q` before commit" beats "write good tests". Delete any rule you cannot test or that restates the model's defaults.
4. **A skill description says when to use it, in the words a user would say,** and is short; the body carries the procedure.
5. **Resolve conflicts:** two files giving opposite orders means one is ignored at random; find and cut the duplicate with `grep -rn`.
6. **Re-measure:** the new always-on size next to the old, in the report.

Pass: the line counts fell or stayed flat for the new content, every import resolves, and each rule names a command or a file it can be checked against.
