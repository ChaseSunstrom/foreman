# Changelog

## 1.1.0 — 2026-09-26
Claude works autonomously and checks its own work.
- You never run commands: consent is a yes/no question. `fm ask ID CAT…` records a one-shot request that only your next reply can grant (starts with yes) or cancel; pasted text, other sessions and requests older than 24 h never grant. `core` can no longer be granted from the command line at all.
- Audits gate `fm task done`: S self-check, M `intent` + one more lens, L all five (`intent`, `adversary`, `edge`, `operator`, `maintainer`), each with its own prompt and context slice (`skills/intake/references/audit.md`), recorded after the last edit (`fm task audit`). FINAL VERIFY adds a session-wide operator + adversary audit.
- Full autonomy (`fm autonomy full`, or `FULL AUTO`): no questions mid-run; decisions recorded with `fm decide`; what only you can grant is collected for one summary at the end.
- `/foreman:brainstorm` for open-ended requests (detected by the prompt hook): context pack, `fm ideas` runs one tool-less `claude -p` per lens in parallel (a subagent can't be tool-less), then grounding, scoring and a queued slate.
- Status, doctor, tidy and improve can be started by Claude; plain words map to Foreman actions.
- Protected core widened to all Foreman code (`plugin/lib`, `bin`, `hooks`); interpreter-code writes to protected paths are caught.
- Fixes found by the audits: `fm` rejects abbreviated options (`--allo core`); session ids come from `CLAUDE_CODE_SESSION_ID` (the env-file export is stale after a resume); `ledger_tail` honours n beyond 64 KB; a busy lock no longer drops your yes silently; uninstall on a machine without `settings.json` leaves nothing behind.

## 1.0.0 — 2026-09-26
First full build from `BUILD_PROMPT.md` (branch `foreman/build`).
- `fm` state CLI (Python stdlib): projects, briefs with evidence-gated steps/criteria/done, intake parser, canonical queue with dependency ordering, ledger, checkpoints, decisions, research notes, sensitive repos, drive mode, tidy, doctor, watch, install/uninstall wiring.
- Hooks: one dispatcher for 13 events; fail-closed guard (8 categories + self-authorize), Stop evidence gate + drive, factual SessionStart/UserPromptSubmit injection, async timeline, reply badge, terminal notifications.
- Skills, rules (51 lines at 1.0.0), read-only agents; ECC and superpowers procedures ported with MIT attribution.
- Visibility: statusline wrapper (original + claude-hud + Foreman line), subagent rows, `fm watch`, theme, OTel/Grafana snippet.
- `install.sh`: installs plugin-dev only with `--build`; `--build` starts Claude Code only when a terminal can actually be opened.
- Verification: 170+ unit/behaviour tests, hook bench (p95 ≤ 38 ms), live `claude -p` scenarios, install round trip, `claude plugin eval` suite.

## 0.1.0
Bootstrap: `BUILD_PROMPT.md`, `install.sh`, `setup-plugins.sh`, `configure-repo.sh`, `reset-claude.sh`, `/foreman:build`.
