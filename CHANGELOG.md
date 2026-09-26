# Changelog

## Unreleased
- Approvals and questions are Claude Code prompts, not chat: `fm ask` raises the native permission prompt (what it grants is in the prompt); a `PermissionRequest` hook confirms the dialog was shown and PostToolUse of that same call grants, so chat messages no longer cancel pending requests. Questions use AskUserQuestion. Chat "yes" remains the fallback where no dialog can appear.
- Conversation view: `foreman:Foreman` output style (selected by install-user when you have none), badge with stage (`T-0015 FEATURE · executing 3/5`), a second statusline line with a progress bar, audits, queue, autonomy and exactly what a yes grants, and `fm watch` with a stage timeline, a Recent feed (evidence, audits, captures, decisions, approvals) and "Waiting on you".
- Headless: `fm serve` runs Claude Code Remote Control in a repo as a systemd user unit (restart with a crash-loop breaker, survives logout and reboot, output discarded) with the project in full autonomy + drive; `fm serve status|stop [--all]`, uninstall stops every unit. Starting it needs the user's yes (new user-only guard category `remote`); it turns on linger, finds `claude` on the saved PATH at each start, and refuses untrusted repos or a running `fm run`; `fm doctor` warns on a dead unit. `~/.claude.json` is now protected core and user unit files count as `system`. `fm run` works the queue in fresh `claude -p` sessions, one task each (drive scoped by `FOREMAN_DRIVE_TASK`), skipping tasks waiting on you and stopping on no progress, a failed session or the timeout.

## 1.1.0 — 2026-09-26
Claude works autonomously and checks its own work.
- You never run commands: consent is a yes/no question. `fm ask ID CAT…` records a one-shot request that only your next reply can grant (starts with yes) or cancel; pasted text, other sessions and requests older than 24 h never grant. `core` can no longer be granted from the command line at all.
- Audits gate `fm task done`: S self-check, M `intent` + one more lens, L all five (`intent`, `adversary`, `edge`, `operator`, `maintainer`), each with its own prompt and context slice (`skills/intake/references/audit.md`), recorded after the last edit (`fm task audit`). FINAL VERIFY adds a session-wide operator + adversary audit.
- Full autonomy (`fm autonomy full`, or `FULL AUTO`): no questions mid-run; decisions recorded with `fm decide`; what only you can grant is collected for one summary at the end.
- `/foreman:brainstorm` for open-ended requests (detected by the prompt hook): context pack, `fm ideas` runs one tool-less `claude -p` per lens in parallel (a subagent can't be tool-less), then grounding, scoring and a queued slate.
- Harness-enforced procedure: stages derived from briefs, `fm next`, the next action injected every turn (a hint; the gates below are enforced), `fm focus` plan gate, no edits without an active task, one-command S tasks (`fm task new … --ac … --step … --focus`).
- Context rot and doc drift: M/L tasks record their Docs impact before done ("documenting" stage); `fm docs` reports markdown that drifted from the repo (tidy includes it); `fm doctor` checks Foreman's own docs against its code; auto-compaction at 70% (`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, reversible) and a context note at task boundaries.
- Status, doctor, tidy and improve can be started by Claude; plain words map to Foreman actions.
- Protected core widened to all Foreman code (`plugin/lib`, `bin`, `hooks`); interpreter-code writes to protected paths are caught.
- Approval hardening from the audits: `fm ask` is bound to the session the PreToolUse hook saw running it (not the agent's environment), requests without a trusted session are refused, a negation right after the yes cancels it ("ok, don't…"), and a task's tier can't be lowered once it has evidence.
- Audit freshness also compares a content id of the working tree (edits made any way, Bash included, make audits stale).
- State falls back to `$XDG_STATE_HOME/foreman` (or a per-user temp dir) when `~/.claude` is read-only, as in `claude plugin eval`; `fm doctor` warns and `uninstall.sh` purges whichever is in use. Eval prompts no longer break on a `---` in the rules.
- Final audit wave: a fallback-state marker can't redirect Foreman's state any more (the guard protects every fallback location and now checks archive extraction, clones, `-t` target dirs and `wget -P` by where they write; markers in dirs others can write are ignored; session start names a fallback in use), `fm doctor --restore-state` moves state back, doctor checks the env values; docs named in Docs impact must exist and show no drift before done, and drift elsewhere is reported at done; background-agent notifications no longer act as your words (approvals, override words, plan-only holds); plan-only detection ignores constraints such as "don't change the API"; a `?` in a code block doesn't stop drive; worktree ids reuse git's stat cache (fast on big repos); one Foreman-module rule in the guard; named lock waits and a shared `fm ask` TTL.
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
