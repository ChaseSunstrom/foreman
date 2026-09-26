# Changelog

## 1.0.0 — 2026-09-26
First full build from `BUILD_PROMPT.md` (branch `foreman/build`).
- `fm` state CLI (Python stdlib): projects, briefs with evidence-gated steps/criteria/done, intake parser, canonical queue with dependency ordering, ledger, checkpoints, decisions, research notes, sensitive repos, drive mode, tidy, doctor, watch, install/uninstall wiring.
- Hooks: one dispatcher for 13 events; fail-closed guard (8 categories + self-authorize), Stop evidence gate + drive, factual SessionStart/UserPromptSubmit injection, async timeline, reply badge, terminal notifications.
- Skills, rules (51 lines), read-only agents; ECC and superpowers procedures ported with MIT attribution.
- Visibility: statusline wrapper (original + claude-hud + Foreman line), subagent rows, `fm watch`, theme, OTel/Grafana snippet.
- Verification: 170+ unit/behaviour tests, hook bench (p95 ≤ 38 ms), live `claude -p` scenarios, install round trip, `claude plugin eval` suite.

## 0.1.0
Bootstrap: `BUILD_PROMPT.md`, `install.sh`, `setup-plugins.sh`, `configure-repo.sh`, `reset-claude.sh`, `/foreman:build`.
