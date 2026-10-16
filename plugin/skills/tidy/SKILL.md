---
name: tidy
description: Use when the user asks to clean up Foreman or memory, or STATE says tidy is overdue: archives old tasks, flags stale inbox items, lints rules and memory; dry-run first.
---

# Foreman: tidy

1. `fm tidy` (dry run; `--all` covers every registered project). Read every finding.
2. Safe to apply without asking (archives, never deletes): old done/dropped briefs to `archive/YYYY-MM/`, ledger and event rotation, regenerated STATE/INBOX. Run `fm tidy --apply`.
3. Needs the user's decision: stale inbox items (keep or drop — never auto-delete user requests), CLAUDE.md or rules cleanup, auto memory edits (dedupe, dead paths, contradictions), unclassified or unused plugins. Present them as one batched question with your default for each.
4. Apply approved memory/CLAUDE.md edits yourself (they are not Foreman state), then run `fm tidy` again and report what changed in ≤ 10 lines.
