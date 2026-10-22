---
name: doctor
description: Use when asked whether Foreman is healthy, or a hook or fm command misbehaves: runs fm doctor, fixes each failure.
argument-hint: "[--full]"
---

# Foreman: doctor

1. `fm doctor $ARGUMENTS` (`--full` also runs `install.sh --no-plugins`).
2. For each failed check: say what it means and the concrete fix. Mechanical fixes that don't touch protected core (e.g. regenerate STATE, chmod +x, `fm doctor --repair` for empty git objects after a crash — it only moves them to the quarantine) can be applied right away; anything touching protected core (Foreman code, rules, evals, permissions, BUILD_PROMPT.md) needs the user's yes: `fm ask ID core --why "…"`, then ask one yes/no question.
3. Re-run `fm doctor` and report the final status in ≤ 15 lines.
