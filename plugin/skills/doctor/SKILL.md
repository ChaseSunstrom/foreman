---
name: doctor
description: Use when the user asks whether Foreman is healthy or working, when a Foreman hook or fm command misbehaves, or after changing Foreman. Runs fm doctor and fixes or explains each failure — settings, hooks and latency, guard fixtures, skills/agents, briefs vs STATE, MASTER.md file map, backups, plugin validation, git hygiene, statusline and install scripts.
argument-hint: "[--full]"
---

# Foreman: doctor

1. `fm doctor $ARGUMENTS` (`--full` also runs `install.sh --no-plugins`).
2. For each failed check: say what it means and the concrete fix. Mechanical fixes that don't touch protected core (e.g. regenerate STATE, chmod +x, `fm doctor --repair` for empty git objects after a crash — it only moves them to the quarantine) can be applied right away; anything touching protected core (Foreman code, rules, evals, permissions, BUILD_PROMPT.md) needs the user's yes: `fm ask ID core --why "…"`, then ask one yes/no question.
3. Re-run `fm doctor` and report the final status in ≤ 15 lines.
