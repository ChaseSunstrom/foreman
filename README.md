# Foreman

A discipline layer for Claude Code. Give it a terse request (`FIX: login times out on slow wifi`, or just "fix the login timeout") and it classifies, plans, sequences, executes, verifies with recorded evidence, and records the work in one central place. It stays on the current task, captures new requests instead of chasing them, resumes at the exact step after `/compact` or a new session, blocks dangerous commands in bypass mode, and keeps going through the queue until it's done or needs you.

Everything is documented in [`MASTER.md`](MASTER.md): how to prompt it, every file, how the parts interact, operations and limitations.

## Install (one line)

Public repo:

```bash
curl -fsSL https://raw.githubusercontent.com/ChaseSunstrom/foreman/main/install.sh | bash
```

Private repo (uses your `gh` login):

```bash
gh repo clone ChaseSunstrom/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh
```

Flags: `--security` (Trail of Bits security skills), `--docs` (Office/PDF skills), `--apply-conflicts` (disable plugins that compete with Foreman instead of just reporting them), `--no-plugins`, `--no-bypass` (keep your current permission mode), `--no-wiring` (don't touch `~/.claude`), `--build` (open Claude Code on `/foreman:build` to rebuild from `BUILD_PROMPT.md`).

## What `install.sh` does

1. Clones this repo to `~/.claude/foreman` (or fast-forwards it if it's clean and on `main`).
2. Runs `setup-plugins.sh`: installs the curated plugins that are missing, installs language-server plugins only when the server is on your PATH, reports conflicting or heavy plugins. It never uninstalls anything.
3. Registers this repo as a local plugin marketplace and installs `foreman@foreman` (loads in place: edits under `plugin/` apply on `/reload-plugins`).
4. Sets `bypassPermissions` as your default permission mode (backing up `settings.json` and recording the original) unless you pass `--no-bypass`.
5. Wires Foreman into `~/.claude` with `fm install-user` unless you pass `--no-wiring`: a statusLine wrapper (your original line and claude-hud still render above the Foreman line), catastrophic-command deny rules, a raised Stop-hook continuation cap for drive mode, a marked block in `~/.claude/CLAUDE.md`, and the `~/.claude/rules/foreman.md` symlink. Every change is recorded in `state/install-manifest.json` so it can be undone exactly.

## Using it

```
fix the login timeout on slow wifi                    # plain request: classified, planned, done with evidence
FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports
CLEAN: collapse the three date helpers into one
CONTEXT: Django app; don't touch migrations
DONE-WHEN: all tests pass and the CSV opens in Excel
```

Work runs in the order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE after a baseline check. Mid-task ideas are captured and queued; `NOW:` switches tasks, `PAUSE` checkpoints, `STATUS` shows where things stand. You never have to run a command: say it in plain words ("is foreman ok?", "clean up", "this repo is sensitive") and Claude does it.

- **Open-ended requests** ("super improve it", "just get it done") get a brainstorm first: several tool-less sub-agents, each with a different lens, then Claude checks every idea against the real code and queues the best. Each brainstorm runs up to six short `claude -p` (Sonnet) sessions, which count against your plan's usage.
- **Audits before done**: finished work is checked through independent lenses (intent, adversary, edge cases, operations, maintainability) with different prompts and context; small tasks get a self-check, large ones all five.
- **Docs stay current**: bigger tasks can't close until they record which docs they changed, and those docs must exist and match the code; drift elsewhere is reported when a task closes (`fm docs` shows it any time). Long sessions compact earlier, since Foreman's state makes that cheap.
- **Full auto**: say `FULL AUTO` (or "don't ask me anything") and Claude works through the whole queue without questions, recording its decisions; anything only you can approve waits for one summary at the end. `STANDARD AUTONOMY` switches back.

## Headless: keep it working on a server

In a repo on your server, ask Claude to "serve this repo": Claude asks you once (a yes grants `remote`), then `fm serve` starts Claude Code Remote Control there as a systemd user unit that survives logout and reboot (it turns on linger, or says why it couldn't) and restarts on failure, and the project switches to full autonomy with drive on. Send feature requests from claude.ai/code or the Claude app whenever you like; they're captured, planned, built, audited and committed one after another. "Stop serving" (`fm serve stop`) undoes it, and uninstall stops every unit. Claude Code has to trust the repo first (open `claude` there once). It doesn't wait out usage limits: after five failed restarts in ten minutes the unit stops, and `fm serve status` or `fm doctor` says why. `fm run` is the other option: it works the queue in fresh `claude -p` sessions, one task each, so a long queue never piles up in one context.

## Permissions

Foreman runs in bypass mode by default: no tool-call prompts. What still stops a dangerous command is Foreman's guard hook (recursive deletes outside the project, force-pushes and hard resets on default branches, credential files, `curl | sh`, disk/firewall/system-service changes, publish/deploy commands, direct writes to Foreman state, edits to Foreman's own protected core and Claude Code's `~/.claude.json`, and starting a remote session), plus 20 deny rules for the truly catastrophic cases. A blocked command says how to authorize it for the current task. For anything that needs you (Foreman's own code, a remote session, destructive categories) Claude Code shows you its own permission prompt saying exactly what would be granted; approving it grants it, and nothing else can (chat messages don't cancel it). Other questions come as a prompt too.

To opt a repo out (client code, anything with production credentials), tell Claude "this repo is sensitive" (it runs `fm sensitive on`). That writes this to the repo's `.claude/settings.local.json` (kept out of commits via `.git/info/exclude`), and Foreman shows the repo as sensitive at session start:

```json
{ "permissions": { "defaultMode": "default" } }
```

Use `"default"` (or `"acceptEdits"`), not `"auto"`: Claude Code ignores `auto` and `bypassPermissions` in project and local settings. `fm sensitive off` undoes it.

To turn bypass off everywhere, set `defaultMode` back to `"auto"` (or delete it) in `~/.claude/settings.json`; the original is in `~/.claude/foreman/backups/`.

## Seeing what's going on

A Foreman line under your statusline (`foreman · T-0012 FIX 3/5 · q2 · in1 · guard on · bypass`), per-subagent rows, a `[T-0012 FIX · 3/5 · 14:02]` badge on each reply (screen only, zero tokens), terminal titles and desktop notifications, `fm watch`, and an optional OpenTelemetry → telegraf → InfluxDB → Grafana setup in `plugin/observability/`. `/tui fullscreen`, `/focus` and `Ctrl+O` help too.

## Does it improve itself?

Within limits. Ideas come from retros, your corrections and its own metrics, and land in Foreman's own inbox. `/foreman:improve` builds candidates in a separate git worktree, runs the `claude plugin eval` suite against the live version, and only proposes changes that score at least as well. You approve every merge, and it can't edit its own guard, permission settings, rules or eval suite without your authorization.

## Layout

```
BUILD_PROMPT.md       the spec Foreman was built from
MASTER.md             system map (start here)
CHANGELOG.md          release notes
install.sh            one-liner bootstrap
setup-plugins.sh      curated plugin setup (safe to re-run; --dry-run to preview)
configure-repo.sh     one-time for forks: point everything at your GitHub repo
reset-claude.sh       optional: reset Claude Code's behavior layer before installing
.claude-plugin/       local marketplace "foreman"
plugin/               the Foreman plugin (fm, hooks, skills, rules, agents, tests, evals)
local/ state/ backups/   machine-specific, gitignored
```

## Tests

```bash
python3 -m unittest discover -s plugin/tests -t plugin/tests   # unit + behaviour
python3 plugin/tests/bench_hooks.py --runs 50                   # hook latency
python3 plugin/tests/e2e/roundtrip.py                           # install/uninstall/reinstall in a sandbox HOME
python3 plugin/tests/e2e/scenarios.py                           # live §12 scenarios (uses claude -p; costs tokens)
```

## Starting from a clean slate (optional)

`reset-claude.sh` resets only the parts that change Claude's behavior (plugins except the ones Foreman keeps, user hooks and permissions, global CLAUDE.md, rules, skills, agents, commands), after backing up `~/.claude` and `~/.claude.json` to `~/.claude-reset/<timestamp>/`. Login, MCP servers, history, memory, themes and per-repo `.claude/` folders are untouched. Undo with the `tar` command it prints.

```bash
./reset-claude.sh            # dry run
./reset-claude.sh --apply    # close Claude Code first
```

## Updating and removing

- Update: `git pull` in `~/.claude/foreman` (then `/reload-plugins`), or rerun `install.sh`.
- Health check: ask "is foreman ok?" (`fm doctor`). Hygiene: "clean up" (`fm tidy`).
- Remove: `~/.claude/foreman/plugin/uninstall.sh` (uninstalls the plugin and marketplace, undoes the wiring, keeps `state/` unless you pass `--purge-state`; `--dry-run` previews).

## Plugin choices

The reasoning, measured context costs and conflicts are in `BUILD_PROMPT.md` (§4.6 and Appendix A) and `MASTER.md`. Preview what `setup-plugins.sh` would change with `./setup-plugins.sh --dry-run`.
