---
name: doctor
description: Use whenever Sampo seems unhealthy or a hook or sampo command misbehaves: runs sampo doctor and fixes each failure.
argument-hint: "[--full]"
disable-model-invocation: true
---

# Sampo: doctor

1. `sampo doctor $ARGUMENTS` (`--full` also runs `install.sh --no-plugins`).
2. For each failed check: say what it means and the concrete fix. Mechanical fixes that don't touch protected core (e.g. regenerate STATE, chmod +x, `sampo doctor --repair` for empty git objects after a crash — it only moves them to the quarantine) can be applied right away; anything touching protected core (Sampo code, rules, evals, permissions, BUILD_PROMPT.md) needs the user's yes: `sampo ask ID core --why "…"`, then ask one yes/no question.
3. Re-run `sampo doctor` and report the final status in ≤ 15 lines.
4. The Ward refused something it shouldn't (or let through something it shouldn't): `sampo doctor --wrong "CMD" [--should block] --why "…"` files it as a labelled case and one FIX task for review. Never loosen the Ward here.
