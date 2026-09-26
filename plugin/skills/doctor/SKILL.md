---
name: doctor
description: Run Foreman's self-check (fm doctor) and explain any failures with a concrete fix — settings, hooks and latency, guard fixtures, skills/agents, briefs vs STATE, MASTER.md file map, backups, plugin validation, git hygiene, statusline and install scripts. Usage /foreman:doctor [--full].
argument-hint: "[--full]"
disable-model-invocation: true
---

# Foreman: doctor

1. `fm doctor $ARGUMENTS` (`--full` also runs `install.sh --no-plugins`).
2. For each failed check: say what it means and the concrete fix. Mechanical fixes that don't touch protected core (e.g. regenerate STATE, chmod +x) can be applied right away; anything touching the guard, hooks.json, rules, evals, permissions or BUILD_PROMPT.md needs the user's approval.
3. Re-run `fm doctor` and report the final status in ≤ 15 lines.
