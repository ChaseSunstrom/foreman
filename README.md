# Foreman

A self-orchestration layer for Claude Code. Give it a terse request (`FIX: login times out on slow wifi`) and it plans, sequences, executes, verifies, and records the work in one central place. It stays focused on the current task, captures new requests instead of jumping to them, and resumes exactly where it left off after `/compact` or a new session.

This repo starts as a **bootstrap**: `BUILD_PROMPT.md` is the spec, and Claude Code builds the full system on your machine from it, dogfooding as it goes.

## Install (one line)

Public repo:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USER/foreman/main/install.sh | bash -s -- --build
```

Private repo (uses your `gh` login):

```bash
gh repo clone YOUR_GITHUB_USER/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh --build
```

Leave off `--build` to set up without starting; later, run `/foreman:build` in any Claude Code session. Extra flags pass through to the plugin setup: `--security` (Trail of Bits security skills), `--docs` (Office/PDF skills), `--apply-conflicts` (disable plugins that compete with Foreman instead of just reporting them), `--no-plugins`, `--no-bypass` (keep your current permission mode).

## Starting from a clean slate (optional)

If you already have plugins and config, you don't need to wipe `~/.claude`: a full wipe loses your login, MCP servers, session history, and memory. `reset-claude.sh` resets only the parts that change Claude's behavior:

```bash
./reset-claude.sh            # dry run: shows exactly what would change
./reset-claude.sh --apply    # close Claude Code first
```

It backs up `~/.claude` and `~/.claude.json` to `~/.claude-reset/<timestamp>/`, uninstalls every plugin except the ones Foreman keeps (`--all-plugins` removes those too, `--keep id,id` spares more), strips user-level hooks, permissions, and ECC env vars from `settings.json`, and moves your global CLAUDE.md, rules, skills, agents, commands, and hook scripts into the archive. Login, MCP servers, history, memory, themes, claude-hud's statusline, and per-repo `.claude/` folders are untouched. The build later offers to port anything useful back from the archive. Undo with the `tar` command it prints.

## First-time publish

```bash
./configure-repo.sh <your-github-user>          # rewrites the placeholders above and commits
gh repo create foreman --private --source . --push
```

## What `install.sh` does

1. Clones this repo to `~/.claude/foreman` (or fast-forwards it if it's clean and on `main`).
2. Runs `setup-plugins.sh`: installs the curated plugins that are missing, installs language-server plugins only when the server is on your PATH, and reports conflicting or heavy plugins. It never uninstalls anything.
3. Registers this repo as a local plugin marketplace and installs `foreman@foreman`. Local marketplaces load in place, so edits under `plugin/` apply on `/reload-plugins`.
4. Sets `bypassPermissions` as your default permission mode (backing up `settings.json` first) unless you pass `--no-bypass`.
5. With `--build`, opens Claude Code and starts (or resumes) the build.

## What the build does

Recon and backup, then a plan that pauses once for your approval, then the build itself: the `fm` state CLI, hooks, skills, rules, read-only recon agents, memory hygiene, a self-check (`fm doctor`), and end-to-end tests. It commits to the `foreman/build` branch and never pushes. When it's done, `MASTER.md` explains every file and how the parts interact.

## Using it (after the build)

```
FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports
CLEAN: collapse the three date helpers into one
```

Work runs in the order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE after a baseline check. Plain one-line requests get the same treatment. Mid-task ideas are captured and queued; `NOW:` switches tasks, `PAUSE` checkpoints, `/foreman:status` shows where things stand.

## Permissions

Foreman runs in bypass mode by default: no tool-call prompts in any Claude Code session. What still stops a dangerous command is Foreman's guard hook (recursive deletes outside the project, force-pushes to main, credential files, `curl | sh`, disk/firewall/system-service changes, deploys), plus a short list of deny rules the build proposes. Bypass only affects tool prompts; Foreman still pauses for plan approval where its autonomy setting says to.

To opt a repo out (client code, anything with production credentials), put this in that repo's `.claude/settings.local.json`:

```json
{ "permissions": { "defaultMode": "auto" } }
```

To turn bypass off everywhere, set `defaultMode` back to `"auto"` (or delete it) in `~/.claude/settings.json`; the original is in `~/.claude/foreman/backups/`.

## Seeing what's going on

The build adds a visibility layer on supported surfaces (it never patches Claude Code itself): a Foreman line under claude-hud's statusline, per-subagent rows, a `[T-0012 FIX · 3/5]` badge on each reply that costs no tokens, terminal title and desktop notifications, a live `fm watch` dashboard for a tmux split, and optional OpenTelemetry export into Grafana. Today, without the build, try `/tui fullscreen` (mouse, click-to-expand tool output, a live `/diff` panel), `/focus`, and `Ctrl+O` for transcript search.

## Does it improve itself?

Yes, within limits. Foreman improves its own skills, rules, hooks, and scripts (not the model). Ideas come from its retros, your corrections, and its own metrics. `/foreman:improve` builds candidate changes in a separate git worktree, runs its `claude plugin eval` suite against the live version, and only proposes changes that score at least as well. You approve every merge, and it can't edit its own guard hook, permission settings, or eval suite.

## Layout

```
BUILD_PROMPT.md       the spec Claude Code builds from
install.sh            one-liner bootstrap
setup-plugins.sh      curated plugin setup (safe to re-run; --dry-run to preview)
configure-repo.sh     one-time: point everything at your GitHub repo
reset-claude.sh       optional: reset Claude Code's behavior layer before installing
.claude-plugin/       local marketplace "foreman"
plugin/               the Foreman plugin (bootstrap: /foreman:build)
local/ state/ backups/   machine-specific, gitignored
```

## Plugin choices

The reasoning, measured context costs, and conflicts are in `BUILD_PROMPT.md` (§4.6 and Appendix A). Preview what `setup-plugins.sh` would change with `./setup-plugins.sh --dry-run`.

## Updating and removing

- Update: rerun `~/.claude/foreman/install.sh`, or `git pull` in `~/.claude/foreman`.
- Remove the bootstrap: `claude plugin uninstall foreman@foreman && claude plugin marketplace remove foreman`. The full build adds an `uninstall.sh`.
