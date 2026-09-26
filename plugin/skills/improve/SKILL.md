---
name: improve
description: Use when the user asks to improve Foreman itself, or when Foreman's self-inbox has items and the queue is empty. Proposes and tests improvements from the self-inbox (source self), bounded and eval-gated — builds candidates in a git worktree, compares them with the live plugin using claude plugin eval, and needs the user's yes before any merge.
---

# Foreman: improve (bounded, eval-gated)

Foreman improves its own skills, rules, hooks and scripts — never the model — and never unreviewed.

1. **Collect.** The self-inbox: `fm state -p <foreman project slug> --json` → inbox items with `source: self` (the slug is the project registered for ~/.claude/foreman; see state/registry.md). Add signals: `fm doctor`, `fm tidy`, hook latency (`fm watch --once`), recurring task types (3+ similar tasks → propose a skill, built and evaluated with skill-creator).
2. **Propose ≤ 5 changes**, each with its evidence and expected effect. Show the proposal and ask one yes/no question; continue on yes. In full autonomy, build and evaluate without asking and bring the result to the final report.
3. **Isolate.** `git -C ~/.claude/foreman worktree add ~/.claude/foreman-improve-<date> -b improve/<date> main`. Build candidates only there. Never edit the live `~/.claude/foreman/plugin`.
4. **Protected core** — guard (lib/fmguard.py, hooks/hook, hooks/hooks.json), deny rules and permission settings, the evidence and approval rules (rules/foreman.md), the eval suite (evals/**) and BUILD_PROMPT.md: these need the user's yes for that brief: `fm ask ID core --why "…"` and one yes/no question (their reply grants it; you can't).
5. **Referee.** Run the eval suite against both, with a cost ceiling:
   `claude plugin eval ~/.claude/foreman/plugin --max-cost-usd 5 --json <tmp>/live.json`
   `claude plugin eval ~/.claude/foreman-improve-<date>/plugin --max-cost-usd 5 --json <tmp>/candidate.json`
   Compare per-category scores and per-case results. A candidate qualifies only if it scores at least as well in every category, regresses no case, stays within the §2.8 budgets (`python3 plugin/tests/bench_hooks.py`, rules ≤ 80 lines) and `fm doctor` is green in the worktree.
6. **Ask for the merge** with a table: change → evidence → eval delta → budgets, and one yes/no question. Merging is always the user's call, whatever the autonomy setting (in full autonomy it waits for the final report).
7. After the user's yes: merge to main, bump `plugin/.claude-plugin/plugin.json` version (and marketplace.json), update MASTER.md and CHANGELOG.md in the same commit, `claude plugin tag plugin`. Rollback: `git revert` + `/reload-plugins`.
